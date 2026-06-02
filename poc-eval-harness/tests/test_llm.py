"""Story 0.1 — temperature-as-call-type enforcement (FR-6 / D-2).

The headline guarantee is *structural*: scored calls cannot carry any temperature
other than 0.0, and the glue path cannot attach tools. These tests assert the
function signatures, not just runtime behavior.

Provider mapping (FR-21 / D-3):
  scored_completion / glue_completion → Cursor API (OpenAI-compatible, _CursorLike)
  simulator_completion                → Gemini (_GeminiLike callable factory)
"""

from __future__ import annotations

import inspect
import json

from kernel import llm
from kernel.tools import RecordAnswer


class _Block:
    """Minimal attribute container; missing attributes return None."""

    def __init__(self, **kw):
        self.__dict__.update(kw)

    def __getattr__(self, name: str):
        return None


# ---------------------------------------------------------------------------
# Cursor fake (OpenAI-compatible)
# ---------------------------------------------------------------------------


class _FakeCursor:
    """Records the kwargs of the last chat.completions.create call.

    Returns a response shaped like the OpenAI SDK: choices[0].message.{content,tool_calls}.
    """

    def __init__(self, text: str, tool_calls: list | None = None):
        self._text = text
        self._tool_calls = tool_calls
        self.last_kwargs: dict | None = None

    @property
    def chat(self) -> "_FakeCursor":
        return self

    @property
    def completions(self) -> "_FakeCursor":
        return self

    def create(self, **kwargs) -> _Block:
        self.last_kwargs = kwargs
        msg = _Block(content=self._text, tool_calls=self._tool_calls)
        return _Block(choices=[_Block(message=msg)])


# ---------------------------------------------------------------------------
# Gemini factory fake (_GeminiLike callable)
# ---------------------------------------------------------------------------


class _FakeGemini:
    """Callable factory: ``system_instruction -> GenerativeModel-like object``."""

    def __init__(self, text: str):
        self._text = text
        self.last_system: str | None = None
        self.last_contents: list | None = None

    def __call__(self, system_instruction: str) -> "_FakeGenerativeModel":
        self.last_system = system_instruction
        return _FakeGenerativeModel(self)


class _FakeGenerativeModel:
    def __init__(self, parent: _FakeGemini):
        self._parent = parent

    def generate_content(self, contents, **kwargs) -> _Block:
        self._parent.last_contents = contents
        return _Block(text=self._parent._text)


# ---------------------------------------------------------------------------
# Structural signature tests
# ---------------------------------------------------------------------------


def test_scored_completion_has_no_temperature_parameter():
    params = inspect.signature(llm.scored_completion).parameters
    assert "temperature" not in params


def test_glue_completion_has_no_tools_parameter():
    params = inspect.signature(llm.glue_completion).parameters
    assert "tools" not in params


# ---------------------------------------------------------------------------
# scored_completion — Cursor (OpenAI-compatible) client
# ---------------------------------------------------------------------------


def test_scored_completion_forces_zero_temperature_and_parses_tools():
    tc_obj = _Block(
        id="call_abc",
        function=_Block(
            name="record_answer",
            arguments=json.dumps(
                {"field_id": "go_live", "value": "asap", "source": "user_stated"}
            ),
        ),
    )
    client = _FakeCursor(text="Got it.", tool_calls=[tc_obj])
    text, calls = llm.scored_completion(
        messages=[{"role": "user", "content": "asap"}],
        tools=[],
        _client=client,
        _model="claude-test-snapshot",
    )
    assert client.last_kwargs["temperature"] == 0.0
    assert text == "Got it."
    assert len(calls) == 1 and isinstance(calls[0], RecordAnswer)


def test_scored_completion_text_only_returns_no_tool_calls():
    client = _FakeCursor(text="Let's start!", tool_calls=None)
    text, calls = llm.scored_completion(
        messages=[{"role": "user", "content": "hi"}],
        tools=[],
        _client=client,
        _model="claude-test-snapshot",
    )
    assert text == "Let's start!"
    assert calls == []


def test_scored_completion_prepends_system_as_message():
    client = _FakeCursor(text="ok")
    llm.scored_completion(
        messages=[{"role": "user", "content": "hi"}],
        tools=[],
        system="You are a test agent.",
        _client=client,
        _model="claude-test-snapshot",
    )
    msgs = client.last_kwargs["messages"]
    assert msgs[0]["role"] == "system"
    assert msgs[0]["content"] == "You are a test agent."


# ---------------------------------------------------------------------------
# glue_completion — Cursor (OpenAI-compatible) client
# ---------------------------------------------------------------------------


def test_glue_completion_runs_at_zero_point_two_and_no_tools_kwarg():
    client = _FakeCursor(text="Welcome!")
    out = llm.glue_completion(
        messages=[{"role": "user", "content": "hi"}],
        _client=client,
        _model="claude-test-snapshot",
    )
    assert out == "Welcome!"
    assert client.last_kwargs["temperature"] == 0.2
    assert "tools" not in client.last_kwargs


# ---------------------------------------------------------------------------
# simulator_completion — Gemini callable factory
# ---------------------------------------------------------------------------


def test_simulator_completion_calls_gemini_factory_with_system():
    client = _FakeGemini("I don't know.")
    out = llm.simulator_completion(
        messages=[{"role": "user", "content": "What's your tax rate?"}],
        system="You are a host.",
        _client=client,
        _model="gemini-test-snapshot",
        seed=42,  # silently ignored by Gemini; accepted for API compat
    )
    assert out == "I don't know."
    assert client.last_system == "You are a host."


def test_simulator_completion_converts_messages_to_gemini_contents():
    client = _FakeGemini("Two listings.")
    llm.simulator_completion(
        messages=[
            {"role": "user", "content": "How many listings?"},
            {"role": "assistant", "content": "I have two."},
            {"role": "user", "content": "Tell me more."},
        ],
        _client=client,
        _model="gemini-test-snapshot",
    )
    contents = client.last_contents
    assert contents[0]["role"] == "user"
    assert contents[1]["role"] == "model"   # "assistant" → "model" for Gemini
    assert contents[2]["role"] == "user"
    assert contents[0]["parts"][0]["text"] == "How many listings?"
