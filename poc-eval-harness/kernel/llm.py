"""Temperature-enforced LLM client (FR-6 / D-2 / architecture §4.1).

Temperature is a property of the *call type*, not a call-site argument:

  - ``scored_completion`` — used for every turn that may emit a tool call on a
    scored slot. Temperature is HARD-CODED to 0.0; there is no override parameter,
    so no code path can issue a scored tool call at any other temperature.
  - ``glue_completion`` — the ONLY path permitted temperature 0.2. It has no
    ``tools`` parameter, so it is structurally incapable of emitting a tool call;
    a scored-slot turn cannot be routed through it by accident.
  - ``simulator_completion`` — the decorrelated OpenAI provider (FR-21). Different
    provider family from the agent; provider decorrelation is config-validated at
    startup (Story 0.2), not here.

These functions take their provider client and model injected (``_client`` /
``_model``) so they are unit-testable with a fake client and carry no global state
(a run is a pure function of its frozen inputs, D-4).
"""

from __future__ import annotations

from typing import Any, Final, Protocol

from .tools import ToolCall, parse_tool_call

# Structural constants — Final so a checker rejects reassignment.
SCORED_TEMPERATURE: Final[float] = 0.0
GLUE_TEMPERATURE: Final[float] = 0.2
SIMULATOR_TEMPERATURE: Final[float] = 0.0  # decorrelation comes from provider, not temp
MAX_TOKENS: Final[int] = 4096


class _AnthropicLike(Protocol):
    @property
    def messages(self) -> Any: ...


class _OpenAILike(Protocol):
    @property
    def chat(self) -> Any: ...


def _collect_anthropic(response: Any) -> tuple[str | None, list[Any]]:
    """Split an Anthropic response into (assistant_text | None, parsed tool calls)."""
    text_parts: list[str] = []
    tool_calls: list[Any] = []
    for block in getattr(response, "content", []) or []:
        btype = getattr(block, "type", None)
        if btype == "text":
            text_parts.append(getattr(block, "text", ""))
        elif btype == "tool_use":
            tool_calls.append(parse_tool_call(block.name, dict(block.input)))
    text = "".join(text_parts).strip() or None
    return text, tool_calls


def scored_completion(
    messages: list[dict],
    tools: list[dict],
    system: str | None = None,
    *,
    _client: _AnthropicLike,
    _model: str,
) -> tuple[str | None, list[ToolCall]]:
    """Tool-emitting completion. ALWAYS temperature 0.0 — no override exists.

    Returns ``(assistant_text | None, parsed_tool_calls)``. The caller logs a
    ``ToolCallEvent`` with ``call_type="scored"`` and ``temperature=0.0`` so FR-6 is
    auditable directly from the trace.
    """
    kwargs: dict[str, Any] = {
        "model": _model,
        "max_tokens": MAX_TOKENS,
        "temperature": SCORED_TEMPERATURE,
        "tools": tools,
        "messages": messages,
    }
    if system is not None:
        kwargs["system"] = system
    response = _client.messages.create(**kwargs)
    return _collect_anthropic(response)


def glue_completion(
    messages: list[dict],
    system: str | None = None,
    *,
    _client: _AnthropicLike,
    _model: str,
) -> str:
    """Conversational-glue completion at temperature 0.2.

    There is deliberately NO ``tools`` parameter: this path cannot attach tools, so
    it is structurally incapable of emitting a scored tool call. Used only for
    greetings / transitions that produce no state mutation.
    """
    kwargs: dict[str, Any] = {
        "model": _model,
        "max_tokens": MAX_TOKENS,
        "temperature": GLUE_TEMPERATURE,
        "messages": messages,
    }
    if system is not None:
        kwargs["system"] = system
    response = _client.messages.create(**kwargs)
    text, _ = _collect_anthropic(response)
    return text or ""


def simulator_completion(
    messages: list[dict],
    system: str | None = None,
    *,
    _client: _OpenAILike,
    _model: str,
    seed: int | None = None,
) -> str:
    """Simulated-host reply via the decorrelated OpenAI provider (FR-21).

    ``seed`` is best-effort (OpenAI only — Anthropic exposes none; see R-2). The
    simulator never receives the answer key (enforced at the call site, Story 4.1).
    """
    full_messages = list(messages)
    if system is not None:
        full_messages = [{"role": "system", "content": system}, *full_messages]
    kwargs: dict[str, Any] = {
        "model": _model,
        "temperature": SIMULATOR_TEMPERATURE,
        "messages": full_messages,
    }
    if seed is not None:
        kwargs["seed"] = seed
    response = _client.chat.completions.create(**kwargs)
    return (response.choices[0].message.content or "").strip()
