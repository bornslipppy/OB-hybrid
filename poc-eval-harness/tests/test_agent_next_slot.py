"""Story 3.1 — Schema-driven next-slot selection.

Acceptance criteria tested here (Epic 3 / Story 3.1):

1. The agent's question order DIVERGES for two profiles whose early answers diverge.
2. The agent NEVER asks about a slot whose depends_on guard is unmet
   (e.g., no owner economics when ownership_model = all_self_owned).
3. The agent pursues ALL tiers — required + recommended + optional — not just required.
4. The stop condition fires only when all reachable in-scope slots are dispositioned;
   stopping at the MVP-completeness line while recommended/optional remain is a test failure.

All tests mock the Cursor client so no real API calls are made.  They test the
agent's structural logic (_is_done, _format_slot_status, slot-exclusion from depends_on)
rather than LLM outputs — those are validated on dev profiles during prompt tuning.
"""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch


from agent.agent import AgentSystem, _detect_signals
from kernel.protocol import EndConversation, UserQuestion
from kernel.schema import FrameGraph, SchemaLoader
from kernel.state import ProfileState, SlotState, SlotStatus

FIXTURES = Path(__file__).resolve().parent / "fixtures"
SCHEMA_PATH = Path(__file__).resolve().parents[1] / "schema" / "guesty-pro-account-creation-schema.md"
_ALL_SECTIONS = ["S0a", "S0b", "S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8"]


def _load(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text())


def _make_agent(system_prompt: str = "You are a test agent.") -> AgentSystem:
    """Build an AgentSystem with a dummy Cursor client."""
    client = MagicMock()
    return AgentSystem(
        cursor_client=client,
        model="claude-test",
        schema_path=SCHEMA_PATH,
        system_prompt=system_prompt,
    )


def _make_state(profile_id: str, slots: dict | None = None) -> ProfileState:
    state = ProfileState(profile_id=profile_id)
    if slots:
        for fid, (status_str, value) in slots.items():
            status = SlotStatus[status_str.upper()]
            s = SlotState(field_id=fid, status=status, value=value)
            state.slots[fid] = s
    return state


# ---------------------------------------------------------------------------
# 1. Greeting is returned on first call (empty history)
# ---------------------------------------------------------------------------


class TestFirstCall:
    def test_returns_user_question_on_first_call(self):
        """Agent must produce a UserQuestion (greeting) when history is empty."""
        agent = _make_agent()
        # Mock glue_completion to return a greeting text.
        with patch("agent.agent.glue_completion", return_value="Hello! Let's get started."):
            state = ProfileState(profile_id="test")
            action = agent.next_action(state, [])

        assert isinstance(action, UserQuestion)
        assert action.text == "Hello! Let's get started."

    def test_first_call_uses_glue_not_scored(self):
        """The opening call MUST use glue_completion (temperature 0.2), not scored_completion."""
        agent = _make_agent()
        with patch("agent.agent.glue_completion", return_value="Hi!") as mock_glue, \
             patch("agent.agent.scored_completion") as mock_scored:
            agent.next_action(ProfileState(profile_id="t"), [])

        mock_glue.assert_called_once()
        mock_scored.assert_not_called()


# ---------------------------------------------------------------------------
# 2. _is_done returns False when slots remain
# ---------------------------------------------------------------------------


class TestIsDone:
    def test_is_done_false_when_required_slot_unanswered(self):
        """_is_done must be False if any required slot is unanswered."""
        agent = _make_agent()
        # Empty state — many required slots remain.
        state = ProfileState(profile_id="p1")
        assert agent._is_done(state) is False

    def test_is_done_false_when_recommended_slot_unanswered(self):
        """Stop condition requires ALL tiers — returning True while recommended
        slots remain is a Story 3.1 violation."""
        agent = _make_agent()
        # Record ALL required slots for all_self_owned profile, but leave recommended ones.
        state = _make_state("p2", {
            "listing_count": ("recorded", 3),
            "channels": ("recorded", ["airbnb"]),
            "go_live": ("recorded", "asap"),
            "ownership_model": ("recorded", "all_self_owned"),
            "focus_topics": ("recorded", ["pricing_strategy"]),
            "account_name": ("recorded", "Test Co"),
            "country": ("recorded", "US"),
            "active_listing_count": ("recorded", 3),
            "connected_channels": ("recorded", ["airbnb"]),
            "ob_specialist_name": ("recorded", "Jordan"),
        })
        # pain (recommended), payment_timing (recommended), etc. still missing.
        assert agent._is_done(state) is False

    def test_is_done_false_when_echo_pending(self):
        """_is_done must be False if any echo is pending (§8 inv 7)."""
        agent = _make_agent()
        state = ProfileState(profile_id="p3")
        state.slots["security_deposit_amount"] = SlotState(
            field_id="security_deposit_amount",
            status=SlotStatus.RECORDED,
            value=500,
            echo_pending=True,  # echo was issued, not yet confirmed
        )
        assert agent._is_done(state) is False

    def test_is_done_respects_depends_on_collapse(self):
        """When ownership_model=all_self_owned, owner slots are not reachable,
        so _is_done must not require them to be dispositioned."""
        agent = _make_agent()
        # Build a fully-dispositioned state for a minimal all_self_owned profile.
        # Load the real schema to verify slot reachability is correct.
        frame = FrameGraph(SchemaLoader().load(SCHEMA_PATH))
        state = ProfileState(profile_id="p4")
        # Record the key facts that collapse the owner branch.
        facts = {
            "listing_count": 2,
            "channels": ["airbnb"],
            "go_live": "asap",
            "ownership_model": "all_self_owned",
        }
        # Disposition every reachable slot in this minimal state.
        signals = _detect_signals(facts)
        reachable = frame.reachable_slots(facts, _ALL_SECTIONS, signals=signals)
        for slot_def in reachable:
            state.slots[slot_def.id] = SlotState(
                field_id=slot_def.id,
                status=SlotStatus.SKIPPED,  # disposition all as skipped for this test
            )
        # owners slot should NOT be in reachable for all_self_owned.
        reachable_ids = {s.id for s in reachable}
        assert "owners" not in reachable_ids, (
            "owners must be unreachable when ownership_model=all_self_owned"
        )
        assert agent._is_done(state) is True


# ---------------------------------------------------------------------------
# 3. Slot-status format includes unanswered slots (schema-driven selection)
# ---------------------------------------------------------------------------


class TestFormatSlotStatus:
    def test_unanswered_slots_appear_in_status(self):
        """Unanswered reachable slots must appear in the status block so the LLM
        can decide which slot to pursue next (FR-1 / Story 3.1)."""
        agent = _make_agent()
        state = ProfileState(profile_id="p5")
        status_text = agent._format_slot_status(state)
        # With an empty state, many unanswered slots should be listed.
        assert "UNANSWERED" in status_text

    def test_recorded_slots_appear_in_status(self):
        agent = _make_agent()
        state = _make_state("p6", {"go_live": ("recorded", "asap")})
        status = agent._format_slot_status(state)
        assert "go_live" in status
        assert "RECORDED" in status

    def test_brief_only_slots_excluded_from_status(self):
        """tech_level, customer_sentiment, risk_flags must NEVER appear in the
        user-facing status block (FR-16 / brief-only slots)."""
        agent = _make_agent()
        state = _make_state("p7", {
            "tech_level": ("recorded", "medium"),
            "customer_sentiment": ("recorded", "positive"),
            "risk_flags": ("recorded", ["high_addon_complexity"]),
        })
        status = agent._format_slot_status(state)
        assert "tech_level" not in status
        assert "customer_sentiment" not in status
        assert "risk_flags" not in status

    def test_all_dispositioned_gives_done_message(self):
        """When every reachable slot is dispositioned, the status must say so."""
        agent = _make_agent()
        # Disposition every reachable slot via skip.
        frame = FrameGraph(SchemaLoader().load(SCHEMA_PATH))
        state = ProfileState(profile_id="p8")
        reachable = frame.reachable_slots({}, _ALL_SECTIONS)
        for slot_def in reachable:
            state.slots[slot_def.id] = SlotState(
                field_id=slot_def.id, status=SlotStatus.SKIPPED
            )
        status = agent._format_slot_status(state)
        assert "All reachable slots are dispositioned" in status


# ---------------------------------------------------------------------------
# 4. Turn cap (§8 invariant 7)
# ---------------------------------------------------------------------------


class TestTurnCap:
    def test_returns_end_conversation_at_60_turns(self):
        """Hitting 60 user-facing turns must return EndConversation(incomplete_turn_cap)."""
        agent = _make_agent()
        # Prime internal messages so we don't hit the greeting path.
        agent._messages = [{"role": "assistant", "content": "Hello"}]
        state = ProfileState(profile_id="cap_test")
        state.turn_count = 60

        action = agent.next_action(state, [{"role": "user", "content": "hi"}])

        assert isinstance(action, EndConversation)
        assert action.reason == "incomplete_turn_cap"

    def test_returns_end_conversation_above_60_turns(self):
        agent = _make_agent()
        agent._messages = [{"role": "assistant", "content": "Hello"}]
        state = ProfileState(profile_id="cap_test_2")
        state.turn_count = 99

        action = agent.next_action(state, [{"role": "user", "content": "hi"}])
        assert isinstance(action, EndConversation)
        assert action.reason == "incomplete_turn_cap"

    def test_does_not_cap_before_60_turns(self):
        """Turn 59 must NOT trigger the cap; the agent should call the LLM."""
        agent = _make_agent()
        agent._messages = [{"role": "assistant", "content": "Hello"}]
        state = ProfileState(profile_id="cap_test_3")
        state.turn_count = 59

        # Mock scored_completion to return a question (avoid a real API call).
        with patch("agent.agent.scored_completion", return_value=("What is your go-live date?", [])):
            action = agent.next_action(state, [{"role": "user", "content": "hi"}])

        assert isinstance(action, UserQuestion)


# ---------------------------------------------------------------------------
# 5. Next action when all slots done → EndConversation
# ---------------------------------------------------------------------------


class TestEndConversationWhenDone:
    def test_is_done_triggers_end_conversation(self):
        """When _is_done() returns True, next_action must return EndConversation
        without calling scored_completion (no wasteful LLM call when done)."""
        agent = _make_agent()
        agent._messages = [{"role": "assistant", "content": "Hello"}]

        # Force _is_done to return True.
        with patch.object(agent, "_is_done", return_value=True), \
             patch("agent.agent.scored_completion") as mock_scored:
            state = ProfileState(profile_id="done_test")
            action = agent.next_action(state, [{"role": "user", "content": "thanks!"}])

        mock_scored.assert_not_called()
        assert isinstance(action, EndConversation)
        assert action.reason == "completed"


# ---------------------------------------------------------------------------
# 6. S5 conditionality at the _detect_signals level (Story 3.5)
# ---------------------------------------------------------------------------


class TestDetectSignals:
    def test_direct_channel_activates_s5_signal(self):
        """channels includes 'direct' must produce a direct-booking signal."""
        signals = _detect_signals({"channels": ["airbnb", "direct"]})
        assert signals.get("channels_includes_direct") is True

    def test_no_direct_channel_leaves_s5_signal_false(self):
        signals = _detect_signals({"channels": ["airbnb", "booking"]})
        assert signals.get("channels_includes_direct") is False

    def test_booking_website_focus_activates_s5_signal(self):
        signals = _detect_signals({"focus_topics": ["booking_website", "pricing_strategy"]})
        assert signals.get("focus_topics_includes_booking_website") is True

    def test_empty_facts_produce_all_false_signals(self):
        signals = _detect_signals({})
        assert signals.get("channels_includes_direct") is False
        assert signals.get("focus_topics_includes_booking_website") is False


# ---------------------------------------------------------------------------
# 7. S5 slot appears / disappears in reachable set based on signals (Story 3.5)
# ---------------------------------------------------------------------------


class TestS5Reachability:
    """Verify that the FrameGraph + signals gate is correctly wiring S5 in the agent."""

    def test_s5_in_status_when_direct_channel_recorded(self):
        """With channels=['direct'], website_brand_name must appear as unanswered."""
        agent = _make_agent()
        state = _make_state("s5_yes", {
            "channels": ("recorded", ["airbnb", "direct"]),
        })
        status = agent._format_slot_status(state)
        assert "website_brand_name" in status

    def test_s5_absent_from_status_without_direct_signals(self):
        """Without any direct-booking signals, S5 slots must NOT appear in status."""
        agent = _make_agent()
        state = _make_state("s5_no", {
            "channels": ("recorded", ["airbnb", "booking"]),
        })
        status = agent._format_slot_status(state)
        assert "website_brand_name" not in status

    def test_s5_not_required_for_is_done_without_direct_signals(self):
        """_is_done must NOT require S5 slots when no direct-booking signals present."""
        agent = _make_agent()
        # Build a fully-dispositioned state for OTA-only profile.
        frame = FrameGraph(SchemaLoader().load(SCHEMA_PATH))
        state = ProfileState(profile_id="s5_done")
        facts = {"channels": ["airbnb", "booking"]}
        signals = _detect_signals(facts)
        reachable = frame.reachable_slots(facts, _ALL_SECTIONS, signals=signals)
        reachable_ids = {s.id for s in reachable}

        # S5 slots must not be in the reachable set.
        assert "website_brand_name" not in reachable_ids, (
            "website_brand_name must not be reachable when channels has no 'direct'"
        )

        # Disposition everything that IS reachable.
        for slot_def in reachable:
            state.slots[slot_def.id] = SlotState(
                field_id=slot_def.id, status=SlotStatus.SKIPPED
            )
        state.slots["channels"] = SlotState(
            field_id="channels", status=SlotStatus.RECORDED, value=["airbnb", "booking"]
        )
        assert agent._is_done(state) is True
