"""Temperature-enforced LLM client (FR-6 / D-2 / architecture §4.1).

Temperature is a property of the *call type*, not a call-site argument:

  - ``scored_completion`` — used for every turn that may emit a tool call on a
    scored slot. Temperature is HARD-CODED to 0.0; there is no override parameter,
    so no code path can issue a scored tool call at any other temperature.
  - ``glue_completion`` — the ONLY path permitted temperature 0.2. It has no
    ``tools`` parameter, so it is structurally incapable of emitting a tool call;
    a scored-slot turn cannot be routed through it by accident.
  - ``simulator_completion`` — the decorrelated Gemini provider (FR-21). Different
    provider family from the Cursor-SDK agent; provider decorrelation is config-
    validated at startup (Story 0.2), not here.

These functions take their provider client and model injected (``_client`` /
``_model``) so they are unit-testable with a fake client and carry no global state
(a run is a pure function of its frozen inputs, D-4).

Provider mapping (FR-21 / D-3):
  Agent   → Cursor API (OpenAI-compatible REST, family="cursor")
  Simulator → Google Gemini via google-genai SDK (family="gemini")
"""

from __future__ import annotations

import json
from typing import Any, Final, Protocol

from .tools import ToolCall, parse_tool_call

# Structural constants — Final so a checker rejects reassignment.
SCORED_TEMPERATURE: Final[float] = 0.0
GLUE_TEMPERATURE: Final[float] = 0.2
SIMULATOR_TEMPERATURE: Final[float] = 0.0  # decorrelation comes from provider, not temp
MAX_TOKENS: Final[int] = 4096


# ---------------------------------------------------------------------------
# Provider protocols
# ---------------------------------------------------------------------------


class _CursorLike(Protocol):
    """Minimal interface expected from an OpenAI-compatible client (Cursor API)."""

    @property
    def chat(self) -> Any: ...


class _GeminiLike(Protocol):
    """Callable factory: ``system_instruction -> GenerativeModel``.

    ``_client(system)`` returns a model object with a ``generate_content(contents, ...)``
    method. Wrapping the factory in a callable keeps ``simulator_completion`` free of
    direct Gemini imports and makes it trivially unit-testable with a fake.
    """

    def __call__(self, system_instruction: str) -> Any: ...


# ---------------------------------------------------------------------------
# Response collectors
# ---------------------------------------------------------------------------


def _collect_openai(response: Any) -> tuple[str | None, list[Any]]:
    """Split an OpenAI-compatible response into (assistant_text | None, parsed tool calls)."""
    choice = response.choices[0].message if response.choices else None
    if choice is None:
        return None, []
    text = (choice.content or "").strip() or None
    tool_calls: list[Any] = []
    if choice.tool_calls:
        for tc in choice.tool_calls:
            fn = tc.function
            args = json.loads(fn.arguments) if isinstance(fn.arguments, str) else dict(fn.arguments)
            tool_calls.append(parse_tool_call(fn.name, args))
    return text, tool_calls


def _to_gemini_contents(messages: list[dict]) -> list[dict]:
    """Convert OpenAI-style ``role/content`` messages to Gemini ``role/parts`` format.

    Gemini uses ``"model"`` for the assistant role; ``"user"`` stays ``"user"``.
    Non-text content (e.g. empty strings) is passed verbatim — Gemini tolerates them.
    """
    contents = []
    for msg in messages:
        role = "user" if msg.get("role") == "user" else "model"
        text = msg.get("content") or ""
        contents.append({"role": role, "parts": [{"text": text}]})
    return contents


# ---------------------------------------------------------------------------
# Agent completions — Cursor API (OpenAI-compatible, temperature-enforced)
# ---------------------------------------------------------------------------


def scored_completion(
    messages: list[dict],
    tools: list[dict],
    system: str | None = None,
    *,
    _client: _CursorLike,
    _model: str,
) -> tuple[str | None, list[ToolCall]]:
    """Tool-emitting completion via Cursor API. ALWAYS temperature 0.0 — no override exists.

    Returns ``(assistant_text | None, parsed_tool_calls)``. The caller logs a
    ``ToolCallEvent`` with ``call_type="scored"`` and ``temperature=0.0`` so FR-6 is
    auditable directly from the trace.
    """
    full_messages: list[dict] = []
    if system is not None:
        full_messages.append({"role": "system", "content": system})
    full_messages.extend(messages)
    response = _client.chat.completions.create(
        model=_model,
        max_tokens=MAX_TOKENS,
        temperature=SCORED_TEMPERATURE,
        tools=tools,
        messages=full_messages,
    )
    return _collect_openai(response)


def glue_completion(
    messages: list[dict],
    system: str | None = None,
    *,
    _client: _CursorLike,
    _model: str,
) -> str:
    """Conversational-glue completion at temperature 0.2 via Cursor API.

    There is deliberately NO ``tools`` parameter: this path cannot attach tools, so
    it is structurally incapable of emitting a scored tool call. Used only for
    greetings / transitions that produce no state mutation.
    """
    full_messages: list[dict] = []
    if system is not None:
        full_messages.append({"role": "system", "content": system})
    full_messages.extend(messages)
    response = _client.chat.completions.create(
        model=_model,
        max_tokens=MAX_TOKENS,
        temperature=GLUE_TEMPERATURE,
        messages=full_messages,
    )
    text, _ = _collect_openai(response)
    return text or ""


# ---------------------------------------------------------------------------
# Simulator completion — Gemini (decorrelated provider, FR-21)
# ---------------------------------------------------------------------------


def simulator_completion(
    messages: list[dict],
    system: str | None = None,
    *,
    _client: _GeminiLike,
    _model: str,
    seed: int | None = None,  # unused by Gemini (no seed param); kept for API compatibility
) -> str:
    """Simulated-host reply via the decorrelated Gemini provider (FR-21).

    ``_client`` is a callable factory ``(system_instruction) -> GenerativeModel`` so
    the per-call system prompt (respondent facts) is baked in fresh each call without
    this function importing ``google.genai`` directly. The ``seed`` param is
    accepted but silently discarded — Gemini has no equivalent (see R-2).
    """
    model_instance = _client(system or "")
    contents = _to_gemini_contents(messages)
    response = model_instance.generate_content(
        contents=contents,
        generation_config={"temperature": SIMULATOR_TEMPERATURE, "max_output_tokens": MAX_TOKENS},
    )
    return (getattr(response, "text", None) or "").strip()
