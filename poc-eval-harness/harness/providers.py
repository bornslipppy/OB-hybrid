"""Provider-client construction (FR-21 / D-3) — the decorrelated agent/simulator clients.

  agent     → OpenAI-compatible REST via the ``openai`` SDK (``_CursorLike``).
              Three sub-paths, selected by environment:
              1. CURSOR_BASE_URL = https://generativelanguage.googleapis.com/... → Gemini
                 (uses GEMINI_API_KEY as the bearer token).
              2. CURSOR_BASE_URL = any other URL → Cursor bridge / proxy
                 (uses CURSOR_API_KEY as the bearer token).
              3. ANTHROPIC_API_KEY set, no CURSOR_BASE_URL → direct Anthropic
                 (via ``_AnthropicClientAdapter``).
  simulator → Google Gemini via ``google-genai`` SDK (a ``_GeminiLike`` factory).

Keys load from the repo ``.env`` (``CURSOR_API_KEY`` / ``ANTHROPIC_API_KEY``, ``GEMINI_API_KEY``)
without adding a ``python-dotenv`` dependency (the lockfile is part of the freeze manifest — no
post-freeze dependency churn).

``_AnthropicClientAdapter`` wraps ``anthropic.Anthropic()`` behind the same
``client.chat.completions.create(...)`` interface that ``kernel.llm.scored_completion`` and
``kernel.llm.glue_completion`` expect, so no changes are needed in the completion kernel.
The adapter translates OpenAI-format tool definitions → Anthropic format and converts the
Anthropic response back into OpenAI-compatible mock objects consumed by ``_collect_openai``.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable


class ProviderError(RuntimeError):
    """Raised when a provider client cannot be constructed (missing key / base URL)."""


def load_env(path: str | Path | None = None) -> None:
    """Minimal ``.env`` loader (no dependency). Sets keys not already in the environment.

    Searches, in order: an explicit ``path``, ``./.env`` (harness cwd), and the repo-root
    ``../.env``. Existing environment variables always win (never overwritten).
    """
    candidates: list[Path] = []
    if path is not None:
        candidates.append(Path(path))
    cwd = Path.cwd()
    candidates += [cwd / ".env", cwd.parent / ".env"]
    for c in candidates:
        if not c.is_file():
            continue
        for line in c.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, val = line.split("=", 1)
            os.environ.setdefault(key.strip(), val.strip().strip('"').strip("'"))


# ---------------------------------------------------------------------------
# Anthropic → OpenAI-interface adapter
# ---------------------------------------------------------------------------


@dataclass
class _MockFn:
    name: str
    arguments: Any  # dict (passed through to parse_tool_call without re-encoding)


@dataclass
class _MockToolCall:
    function: _MockFn


@dataclass
class _MockMessage:
    content: str | None
    tool_calls: list[_MockToolCall] | None


@dataclass
class _MockChoice:
    message: _MockMessage


@dataclass
class _MockResponse:
    choices: list[_MockChoice]


class _AnthropicCompletionsProxy:
    """Translates ``chat.completions.create(...)`` calls into ``anthropic.messages.create``."""

    def __init__(self, anthropic_client: Any) -> None:
        self._client = anthropic_client

    def create(
        self,
        *,
        model: str,
        messages: list[dict],
        max_tokens: int,
        temperature: float,
        tools: list[dict] | None = None,
        **_kwargs: Any,
    ) -> _MockResponse:
        # Split the OpenAI-style system message out (Anthropic takes it as a kwarg)
        system: str | None = None
        api_messages: list[dict] = []
        for msg in messages:
            if msg.get("role") == "system":
                system = msg.get("content") or ""
            else:
                api_messages.append({"role": msg["role"], "content": msg.get("content") or ""})

        # Convert OpenAI tool schema → Anthropic tool schema
        anthropic_tools: list[dict] | None = None
        if tools:
            anthropic_tools = []
            for t in tools:
                fn = t.get("function", t)  # handle both {type,function} and bare dicts
                anthropic_tools.append({
                    "name": fn["name"],
                    "description": fn.get("description", ""),
                    "input_schema": fn.get(
                        "parameters", {"type": "object", "properties": {}}
                    ),
                })

        create_kwargs: dict[str, Any] = {
            "model": model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": api_messages,
        }
        if system is not None:
            create_kwargs["system"] = system
        if anthropic_tools:
            create_kwargs["tools"] = anthropic_tools

        resp = self._client.messages.create(**create_kwargs)

        # Convert Anthropic response blocks → OpenAI-compatible mock
        text: str | None = None
        tool_calls: list[_MockToolCall] = []
        for block in resp.content:
            if block.type == "text":
                text = block.text or None
            elif block.type == "tool_use":
                tool_calls.append(
                    _MockToolCall(function=_MockFn(name=block.name, arguments=block.input))
                )

        msg_obj = _MockMessage(content=text, tool_calls=tool_calls or None)
        return _MockResponse(choices=[_MockChoice(message=msg_obj)])


class _AnthropicChatProxy:
    def __init__(self, anthropic_client: Any) -> None:
        self.completions = _AnthropicCompletionsProxy(anthropic_client)


class _AnthropicClientAdapter:
    """Wraps ``anthropic.Anthropic()`` behind the ``_CursorLike`` interface.

    ``scored_completion`` and ``glue_completion`` call ``_client.chat.completions.create(...)``;
    this adapter satisfies that contract by translating to/from the Anthropic API surface.
    """

    def __init__(self, anthropic_client: Any) -> None:
        self.chat = _AnthropicChatProxy(anthropic_client)


# ---------------------------------------------------------------------------
# Public client constructors
# ---------------------------------------------------------------------------


def build_agent_client(*, api_key: str | None = None, base_url: str | None = None) -> Any:
    """Construct the agent client, auto-selecting Cursor or direct Anthropic.

    Priority:
      1. ``CURSOR_BASE_URL`` set (or explicit ``base_url``) → OpenAI-compatible Cursor client,
         requires ``CURSOR_API_KEY`` (or explicit ``api_key``).
      2. ``ANTHROPIC_API_KEY`` set → ``_AnthropicClientAdapter`` wrapping ``anthropic.Anthropic()``.
      3. Neither configured → :class:`ProviderError`.

    Both paths return an object that satisfies the ``_CursorLike`` protocol so the rest of
    the harness is path-agnostic.
    """
    resolved_base_url = base_url or os.environ.get("CURSOR_BASE_URL")

    if resolved_base_url:
        from openai import OpenAI

        # For Google Gemini's OpenAI-compatible endpoint, use GEMINI_API_KEY;
        # for all other base URLs (Cursor bridge, proxies, etc.) use CURSOR_API_KEY.
        is_gemini_endpoint = "googleapis.com" in resolved_base_url
        if is_gemini_endpoint:
            resolved_api_key = api_key or os.environ.get("GEMINI_API_KEY")
            key_hint = "GEMINI_API_KEY"
        else:
            resolved_api_key = api_key or os.environ.get("CURSOR_API_KEY")
            key_hint = "CURSOR_API_KEY"

        if not resolved_api_key:
            raise ProviderError(
                f"{key_hint} is not set (agent provider). Add it to the repo .env."
            )
        return OpenAI(api_key=resolved_api_key, base_url=resolved_base_url)

    anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY")
    if anthropic_api_key:
        import anthropic as _anthropic

        return _AnthropicClientAdapter(_anthropic.Anthropic(api_key=anthropic_api_key))

    raise ProviderError(
        "Agent provider not configured. Set either:\n"
        "  CURSOR_BASE_URL + CURSOR_API_KEY  (Cursor API bridge / proxy), or\n"
        "  ANTHROPIC_API_KEY                 (direct Anthropic API)"
    )


def build_cursor_client(*, api_key: str | None = None, base_url: str | None = None) -> Any:
    """Backward-compatible alias for :func:`build_agent_client`."""
    return build_agent_client(api_key=api_key, base_url=base_url)


class _GenAIModelProxy:
    """Adapts a ``google.genai`` client to the ``_GeminiLike`` inner-object contract.

    ``simulator_completion`` expects ``_client(system_instruction)`` to return an object
    with ``generate_content(contents, generation_config=dict)``. This proxy satisfies
    that interface using the new ``google.genai`` client, translating ``generation_config``
    to ``types.GenerateContentConfig`` and baking the per-call system instruction in.
    """

    def __init__(self, client: Any, model: str, system_instruction: str) -> None:
        self._client = client
        self._model = model
        self._system = system_instruction

    def generate_content(self, contents: list[dict], generation_config: dict | None = None) -> Any:
        from google.genai import types

        cfg: dict[str, Any] = {}
        if self._system:
            cfg["system_instruction"] = self._system
        if generation_config:
            cfg.update(generation_config)
        return self._client.models.generate_content(
            model=self._model,
            contents=contents,
            config=types.GenerateContentConfig(**cfg) if cfg else None,
        )


def build_gemini_client_factory(model: str, *, api_key: str | None = None) -> Callable[[str], Any]:
    """Construct the decorrelated Gemini factory ``(system_instruction) -> GenerativeModel-like``.

    Uses the ``google-genai`` SDK (``google.genai``). The returned factory satisfies the
    ``_GeminiLike`` protocol — calling it with a system instruction yields a proxy object
    whose ``generate_content(contents, generation_config=...)`` maps to the new SDK surface.
    """
    from google import genai

    api_key = api_key or os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ProviderError(
            "GEMINI_API_KEY is not set (simulator provider). Add it to the repo .env."
        )
    client = genai.Client(api_key=api_key)

    def factory(system_instruction: str) -> Any:
        return _GenAIModelProxy(client, model, system_instruction)

    return factory


class LazyGeminiClientFactory:
    """Deferred ``_GeminiLike`` factory — builds the real Gemini client on first call.

    The CLI always passes a factory to ``make_run_fn``, even for ``--systems tree`` runs
    where Group A profiles never touch the Gemini path. Constructing ``LazyGeminiClientFactory``
    is free; the underlying ``genai.Client`` is only created (and ``GEMINI_API_KEY`` checked)
    when a Group B/C profile is first encountered. Tree-only runs against all-Group-A profiles
    never hit the Gemini key check.
    """

    def __init__(self, model: str, *, api_key: str | None = None) -> None:
        self._model = model
        self._api_key = api_key
        self._factory: Callable[[str], Any] | None = None

    def __call__(self, system_instruction: str) -> Any:
        if self._factory is None:
            self._factory = build_gemini_client_factory(self._model, api_key=self._api_key)
        return self._factory(system_instruction)
