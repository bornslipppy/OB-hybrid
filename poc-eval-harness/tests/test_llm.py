"""Story 0.1 — temperature-as-call-type enforcement (FR-6 / D-2).

The headline guarantee is *structural*: scored calls cannot carry any temperature
other than 0.0, and the glue path cannot attach tools. These tests assert the
function signatures, not just runtime behavior.
"""

from __future__ import annotations

import inspect

from kernel import llm
from kernel.tools import RecordAnswer


class _Block:
    def __init__(self, **kw):
        self.__dict__.update(kw)


class _AnthropicResponse:
    def __init__(self, content):
        self.content = content


class _FakeAnthropic:
    """Records the kwargs of the last messages.create call."""

    def __init__(self, content):
        self._content = content
        self.last_kwargs: dict | None = None

    @property
    def messages(self):
        return self

    def create(self, **kwargs):
        self.last_kwargs = kwargs
        return _AnthropicResponse(self._content)


class _FakeOpenAI:
    def __init__(self, text):
        self._text = text
        self.last_kwargs: dict | None = None

    @property
    def chat(self):
        return self

    @property
    def completions(self):
        return self

    def create(self, **kwargs):
        self.last_kwargs = kwargs
        msg = _Block(message=_Block(content=self._text))
        return _Block(choices=[msg])


def test_scored_completion_has_no_temperature_parameter():
    params = inspect.signature(llm.scored_completion).parameters
    assert "temperature" not in params


def test_glue_completion_has_no_tools_parameter():
    params = inspect.signature(llm.glue_completion).parameters
    assert "tools" not in params


def test_scored_completion_forces_zero_temperature_and_parses_tools():
    content = [
        _Block(type="text", text="Got it."),
        _Block(type="tool_use", name="record_answer", input={"field_id": "go_live", "value": "asap", "source": "user_stated"}),
    ]
    client = _FakeAnthropic(content)
    text, calls = llm.scored_completion(
        messages=[{"role": "user", "content": "asap"}],
        tools=[],
        _client=client,
        _model="claude-test-snapshot",
    )
    assert client.last_kwargs["temperature"] == 0.0
    assert text == "Got it."
    assert len(calls) == 1 and isinstance(calls[0], RecordAnswer)


def test_glue_completion_runs_at_zero_point_two_and_no_tools_kwarg():
    client = _FakeAnthropic([_Block(type="text", text="Welcome!")])
    out = llm.glue_completion(
        messages=[{"role": "user", "content": "hi"}],
        _client=client,
        _model="claude-test-snapshot",
    )
    assert out == "Welcome!"
    assert client.last_kwargs["temperature"] == 0.2
    assert "tools" not in client.last_kwargs


def test_simulator_completion_passes_seed_and_returns_text():
    client = _FakeOpenAI("I don't know.")
    out = llm.simulator_completion(
        messages=[{"role": "user", "content": "What's your tax rate?"}],
        system="You are a host.",
        _client=client,
        _model="gpt-test-snapshot",
        seed=42,
    )
    assert out == "I don't know."
    assert client.last_kwargs["seed"] == 42
    assert client.last_kwargs["messages"][0]["role"] == "system"
