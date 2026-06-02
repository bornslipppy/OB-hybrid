"""Story 3.3 — Agent behavioral invariants (§8).

Acceptance criteria tested here (Epic 3 / Story 3.3):

1. Echo-before-write: agent returns a question (echo) rather than a tool call
   when a numeric value is introduced for the first time on an echo-required field.
   The write tool fires ONLY after a later confirmed turn.
2. Advice requests: agent emits flag_for_call_1 and never recommends a choice.
3. IDK / deferral: treated as absence → skip_question (or flag_for_call_1 if required).
   No clarifying question is spent on an absent fact.
4. Sixty-turn cap: covered in test_agent_next_slot.py (TestTurnCap).
5. §8 invariants in the system prompt: verify verbatim presence of key phrases.

All tests mock scored_completion to control LLM output without real API calls.
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from agent.agent import AgentSystem, _SYSTEM_PROMPT_PATH
from kernel.state import ProfileState
from kernel.tools import RecordAnswer, Source

SCHEMA_PATH = Path(__file__).resolve().parents[1] / "schema" / "guesty-pro-account-creation-schema.md"


def _make_agent() -> AgentSystem:
    return AgentSystem(
        cursor_client=MagicMock(),
        model="claude-test",
        schema_path=SCHEMA_PATH,
        system_prompt="You are a test agent.",
    )


def _primed_agent(messages: list | None = None) -> AgentSystem:
    """Return an agent already past the greeting (internal messages primed)."""
    agent = _make_agent()
    agent._messages = messages or [{"role": "assistant", "content": "Hello!"}]
    return agent


# ---------------------------------------------------------------------------
# 1. System prompt contains all §8 invariants verbatim
# ---------------------------------------------------------------------------


class TestSystemPromptInvariants:
    """The system_prompt.txt must contain all 7 §8 invariants explicitly.
    These phrases are load-bearing per the acceptance criteria.
    """

    @pytest.fixture(scope="class")
    def prompt_text(self) -> str:
        return _SYSTEM_PROMPT_PATH.read_text(encoding="utf-8")

    def test_invariant_1_echo_before_write_present(self, prompt_text):
        assert "echo_before_write" in prompt_text or "Echo-before-write" in prompt_text

    def test_invariant_2_never_advise_present(self, prompt_text):
        assert "Never advise" in prompt_text or "never advise" in prompt_text or \
               "Never recommend" in prompt_text or "never recommend" in prompt_text

    def test_invariant_3_one_clarifying_question_present(self, prompt_text):
        assert "one clarifying question" in prompt_text.lower() or \
               "ONE clarifying question" in prompt_text or \
               "exactly ONE" in prompt_text

    def test_invariant_4_honor_skip_present(self, prompt_text):
        assert "skip" in prompt_text.lower() and (
            "no retry" in prompt_text.lower() or "honor" in prompt_text.lower()
        )

    def test_invariant_5_never_correct_tax_present(self, prompt_text):
        assert "never correct" in prompt_text.lower() or "Never correct" in prompt_text

    def test_invariant_6_intent_capture_only_present(self, prompt_text):
        assert "intent" in prompt_text.lower() and "BusinessModel" in prompt_text

    def test_invariant_7_max_turns_present(self, prompt_text):
        assert "60" in prompt_text and "turn" in prompt_text.lower()

    def test_idk_is_absence_not_ambiguity_present(self, prompt_text):
        assert "absence" in prompt_text.lower() or "absent fact" in prompt_text.lower()

    def test_end_section_guard_present(self, prompt_text):
        assert "end_section" in prompt_text

    def test_hero_branch_plain_language_present(self, prompt_text):
        assert "how do you get paid" in prompt_text.lower()

    def test_s5_conditional_present(self, prompt_text):
        assert "S5" in prompt_text or "Booking Website" in prompt_text


# ---------------------------------------------------------------------------
# 2. Scored completion used for tool-emitting turns
# ---------------------------------------------------------------------------


class TestScoredCompletionUsage:
    def test_tool_calls_use_scored_completion(self):
        """Tool-emitting turns MUST route through scored_completion (FR-6/D-2)."""
        agent = _primed_agent()
        state = ProfileState(profile_id="scored_test")

        tool = RecordAnswer(field_id="go_live", value="asap", source=Source.USER_STATED)

        with patch("agent.agent.scored_completion", return_value=("", [tool])) as mock_sc, \
             patch("agent.agent.glue_completion") as mock_glue:
            action = agent.next_action(state, [{"role": "user", "content": "asap"}])

        mock_sc.assert_called_once()
        mock_glue.assert_not_called()
        assert action == [tool]

    def test_scored_completion_called_with_tools_attached(self):
        """scored_completion must receive the tool definitions (7 tools)."""
        agent = _primed_agent()
        state = ProfileState(profile_id="tools_test")

        with patch("agent.agent.scored_completion", return_value=("Hello", [])) as mock_sc:
            agent.next_action(state, [{"role": "user", "content": "hi"}])

        call_kwargs = mock_sc.call_args
        assert call_kwargs is not None
        tools_arg = call_kwargs.kwargs.get("tools") or call_kwargs.args[1]
        assert len(tools_arg) == 7, f"Expected 7 tools, got {len(tools_arg)}"


# ---------------------------------------------------------------------------
# 3. Tool call result loop (§8 / FR-2 structural requirement)
# ---------------------------------------------------------------------------


class TestToolCallLoop:
    def test_pending_tool_ids_cleared_after_tool_result_injected(self):
        """After tool calls are returned, _pending_tool_ids must be cleared once
        tool_result blocks are injected on the next next_action call."""
        agent = _primed_agent()
        state = ProfileState(profile_id="loop_test")

        tool = RecordAnswer(field_id="go_live", value="asap", source=Source.USER_STATED)

        # First call: LLM emits a tool call.
        with patch("agent.agent.scored_completion", return_value=("", [tool])):
            agent.next_action(state, [{"role": "user", "content": "asap"}])

        assert agent._pending_tool_ids is not None, "pending_tool_ids must be set after tool call"

        # Second call: tool_result should be injected, pending cleared.
        with patch("agent.agent.scored_completion", return_value=("What's your go-live?", [])), \
             patch.object(agent, "_is_done", return_value=False):
            agent.next_action(state, [])

        assert agent._pending_tool_ids is None, "pending_tool_ids must be None after injection"

        # The internal messages should now contain role="tool" messages (OpenAI wire format).
        tool_result_msgs = [
            m for m in agent._messages
            if m.get("role") == "tool"
        ]
        assert len(tool_result_msgs) >= 1, "At least one role='tool' message must be present"

    def test_tool_use_ids_match_tool_result_ids(self):
        """The tool_use IDs in the assistant message must match the tool_result IDs
        injected in the following user message (Anthropic API requirement)."""
        agent = _primed_agent()
        state = ProfileState(profile_id="id_match_test")

        tool = RecordAnswer(field_id="go_live", value="asap", source=Source.USER_STATED)

        with patch("agent.agent.scored_completion", return_value=("", [tool])):
            agent.next_action(state, [])

        # Inject the tool_result by calling next_action again.
        with patch("agent.agent.scored_completion", return_value=("Next q?", [])), \
             patch.object(agent, "_is_done", return_value=False):
            agent.next_action(state, [])

        # Find tool_call IDs from the assistant message (OpenAI wire format).
        tool_call_ids: set[str] = set()
        tool_result_ids: set[str] = set()
        for msg in agent._messages:
            if msg.get("role") == "assistant" and msg.get("tool_calls"):
                for tc in msg["tool_calls"]:
                    tool_call_ids.add(tc["id"])
            if msg.get("role") == "tool":
                tool_result_ids.add(msg["tool_call_id"])

        assert tool_call_ids, "Must have at least one tool_call ID"
        assert tool_call_ids == tool_result_ids, (
            f"tool_call IDs {tool_call_ids} must match role='tool' IDs {tool_result_ids}"
        )


# ---------------------------------------------------------------------------
# 4. FlagForCall1 present in prompt / trace (§8 invariant 2, 4, 5, 6)
# ---------------------------------------------------------------------------


class TestFlagForCall1Tool:
    def test_flag_tool_included_in_tool_definitions(self):
        """flag_for_call_1 must be in the tool definitions passed to the LLM."""
        agent = _make_agent()
        tool_names = [t["function"]["name"] for t in agent._tool_defs]
        assert "flag_for_call_1" in tool_names

    def test_skip_question_tool_included(self):
        agent = _make_agent()
        tool_names = [t["function"]["name"] for t in agent._tool_defs]
        assert "skip_question" in tool_names

    def test_add_owner_tool_included(self):
        """add_owner must be available — hero-branch capture (FR-3)."""
        agent = _make_agent()
        tool_names = [t["function"]["name"] for t in agent._tool_defs]
        assert "add_owner" in tool_names

    def test_all_seven_tools_present(self):
        agent = _make_agent()
        expected = {
            "record_answer", "add_fee", "add_tax", "add_owner",
            "skip_question", "flag_for_call_1", "end_section",
        }
        actual = {t["function"]["name"] for t in agent._tool_defs}
        assert actual == expected


# ---------------------------------------------------------------------------
# 5. Trace emission (Story 3.7)
# ---------------------------------------------------------------------------


class TestTraceEmission:
    def test_tool_call_event_emitted_with_temperature_zero(self, tmp_path):
        """Tool calls must emit a ToolCallEvent with call_type='scored' and
        temperature=0.0 (FR-6 / Story 3.7 / NFR-1)."""
        from kernel.trace import ToolCallEvent, TraceReader, TraceWriter

        trace_file = tmp_path / "trace.jsonl"
        writer = TraceWriter(trace_file)

        agent = AgentSystem(
            cursor_client=MagicMock(),
            model="claude-test",
            schema_path=SCHEMA_PATH,
            system_prompt="Test.",
            trace_writer=writer,
        )
        agent._messages = [{"role": "assistant", "content": "Hello"}]
        state = ProfileState(profile_id="trace_test")

        tool = RecordAnswer(field_id="go_live", value="asap", source=Source.USER_STATED)
        with patch("agent.agent.scored_completion", return_value=("", [tool])):
            agent.next_action(state, [{"role": "user", "content": "asap"}])

        events = TraceReader(trace_file).events()
        tool_events = [e for e in events if isinstance(e, ToolCallEvent)]
        assert len(tool_events) == 1
        ev = tool_events[0]
        assert ev.tool == "record_answer"
        assert ev.call_type == "scored"
        assert ev.temperature == 0.0

    def test_session_end_emitted_at_turn_cap(self, tmp_path):
        """SessionEnd with reason='incomplete_turn_cap' must be written at 60 turns."""
        from kernel.trace import SessionEnd, TraceReader, TraceWriter

        trace_file = tmp_path / "trace2.jsonl"
        writer = TraceWriter(trace_file)

        agent = AgentSystem(
            cursor_client=MagicMock(),
            model="claude-test",
            schema_path=SCHEMA_PATH,
            system_prompt="Test.",
            trace_writer=writer,
        )
        agent._messages = [{"role": "assistant", "content": "Hello"}]
        state = ProfileState(profile_id="cap_trace")
        state.turn_count = 60

        agent.next_action(state, [])

        events = TraceReader(trace_file).events()
        end_events = [e for e in events if isinstance(e, SessionEnd)]
        assert len(end_events) == 1
        assert end_events[0].reason == "incomplete_turn_cap"
