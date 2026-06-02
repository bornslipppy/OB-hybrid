"""Story 4.6 enablement — agent emits echo-lifecycle events from markers (R-10).

These verify the agent turns its ``[[ECHO]]`` / ``[[CONFIRM]]`` / ``[[CORRECT]]`` markers
into the trace events ``false_write_rate`` consumes, strips them before the user sees
them, and — end-to-end through ``run_conversation`` — produces a trace where a properly
confirmed echo write is clean and an unconfirmed one is a false write (fail-safe SM-C1).
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

from agent.agent import AgentSystem
from harness.runner import run_conversation
from kernel.state import ProfileState, StateReducer
from kernel.tools import RecordAnswer
from kernel.trace import TraceReader, TraceWriter, UserConfirmed, UserCorrected
from scoring.metrics import false_write_rate

SCHEMA_PATH = Path(__file__).resolve().parents[1] / "schema" / "guesty-pro-account-creation-schema.md"


def _agent(trace_writer=None) -> AgentSystem:
    return AgentSystem(
        cursor_client=MagicMock(), model="claude-test",
        schema_path=SCHEMA_PATH, system_prompt="Test agent.", trace_writer=trace_writer,
    )


def _primed(agent: AgentSystem) -> None:
    """Skip the greeting branch so scored_completion is exercised."""
    agent._messages = [{"role": "assistant", "content": "hi"}]


class TestMarkerParsing:
    def test_echo_marker_emits_value_introduced_and_echo_issued_and_strips(self):
        agent = _agent()
        _primed(agent)
        text = "[[ECHO slot=security_deposit_amount subfield=- value=250]] Just to confirm — a $250 deposit?"
        with patch("agent.agent.scored_completion", return_value=(text, [])):
            action = agent.next_action(ProfileState(profile_id="P"), [{"role": "user", "content": "250"}])
        assert action.text == "Just to confirm — a $250 deposit?"  # marker stripped
        ev = agent.drain_trace_events()
        assert [type(e).__name__ for e in ev] == ["ValueIntroduced", "EchoIssued"]
        assert ev[0].slot == "security_deposit_amount" and ev[0].subfield is None and ev[0].value == 250
        assert agent.drain_trace_events() == []  # drained once

    def test_confirm_marker_on_tool_turn_emits_user_confirmed(self):
        agent = _agent()
        _primed(agent)
        tool = RecordAnswer(field_id="security_deposit_amount", value=250, source="user_stated")
        text = "[[CONFIRM slot=security_deposit_amount subfield=-]]"
        with patch("agent.agent.scored_completion", return_value=(text, [tool])):
            action = agent.next_action(ProfileState(profile_id="P"), [{"role": "user", "content": "yes"}])
        assert isinstance(action, list)
        ev = agent.drain_trace_events()
        assert [type(e).__name__ for e in ev] == ["UserConfirmed"]
        assert ev[0].slot == "security_deposit_amount"

    def test_correct_marker_emits_user_corrected_with_value(self):
        agent = _agent()
        _primed(agent)
        text = "[[CORRECT slot=owners subfield=pmc_commission_rate value=12]] Got it, 12%."
        with patch("agent.agent.scored_completion", return_value=(text, [])):
            agent.next_action(ProfileState(profile_id="P"), [{"role": "user", "content": "no, 12"}])
        ev = agent.drain_trace_events()
        assert isinstance(ev[0], UserCorrected)
        assert ev[0].subfield == "pmc_commission_rate" and ev[0].corrected_value == 12

    def test_composite_per_subfield_confirms(self):
        agent = _agent()
        _primed(agent)
        text = ("[[CONFIRM slot=owners subfield=ownership_share]] "
                "[[CONFIRM slot=owners subfield=pmc_commission_rate]]")
        with patch("agent.agent.scored_completion", return_value=(text, [])):
            agent.next_action(ProfileState(profile_id="P"), [{"role": "user", "content": "yes"}])
        ev = agent.drain_trace_events()
        subs = {e.subfield for e in ev if isinstance(e, UserConfirmed)}
        assert subs == {"ownership_share", "pmc_commission_rate"}


class TestEndToEndThroughRunConversation:
    """Drive a real AgentSystem through run_conversation and score the resulting trace."""

    def _drive(self, tmp_path, confirm_turn_text):
        agent = _agent()  # harness owns the trace → no own writer
        reducer = StateReducer(frame=None)
        writer = TraceWriter(tmp_path / "t.jsonl")

        class _Sim:
            def reply(self, q):
                return "yes"

        scored_seq = [
            ("[[ECHO slot=security_deposit_amount subfield=- value=250]] Confirm $250 deposit?", []),
            (confirm_turn_text, [RecordAnswer(field_id="security_deposit_amount", value=250, source="user_stated")]),
            ("", []),  # nothing left to say → EndConversation(completed)
        ]
        with patch("agent.agent.glue_completion", return_value="Welcome — let's begin."), \
             patch("agent.agent.scored_completion", side_effect=scored_seq):
            run_conversation(agent, _Sim(), reducer=reducer, trace=writer, profile_id="P")
        return TraceReader(tmp_path / "t.jsonl").events()

    def test_confirmed_echo_write_is_clean(self, tmp_path):
        events = self._drive(tmp_path, "[[CONFIRM slot=security_deposit_amount subfield=-]]")
        kinds = [type(e).__name__ for e in events]
        # Lifecycle present and ordered: value/echo → confirm → tool_call.
        assert "ValueIntroduced" in kinds and "EchoIssued" in kinds
        assert kinds.index("UserConfirmed") < kinds.index("ToolCallEvent")
        result = false_write_rate(events)
        assert result.total_echo_writes == 1 and result.is_clean

    def test_unconfirmed_echo_write_is_false_write(self, tmp_path):
        # The confirm turn fires the write but omits the [[CONFIRM]] marker → fail-safe.
        events = self._drive(tmp_path, "Sounds good.")
        result = false_write_rate(events)
        assert result.total_echo_writes == 1 and result.false_writes == 1
        assert result.detections[0].slot == "security_deposit_amount"
