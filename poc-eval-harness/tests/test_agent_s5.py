"""Story 3.5 — Conditional Booking-Website (S5) surfacing.

Acceptance criteria tested here (Epic 3 / Story 3.5):

1. With NO direct-booking signal → S5 slots are NOT in the reachable set.
   Surfacing them would score wrong.
2. With a direct-booking signal → S5 slots ARE in the reachable set.
   Not surfacing them would score wrong.
3. The three S5 sub-slots chain correctly
   (website_brand_name → website_domain → website_terms).
4. Direct-booking signals recognised:
     a. channels includes 'direct'
     b. focus_topics includes 'booking_website'
   (Conversational signals like "my website" are handled by the LLM; not tested here.)

Direct-booking signal detection is structural (kernel FrameGraph + _detect_signals),
not a matter of LLM prompt-following. These tests verify the structural gating.
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

import pytest

from agent.agent import AgentSystem, _detect_signals
from kernel.schema import FrameGraph, SchemaLoader
from kernel.state import ProfileState, SlotState, SlotStatus

SCHEMA_PATH = Path(__file__).resolve().parents[1] / "schema" / "guesty-pro-account-creation-schema.md"
_ALL_SECTIONS = ["S0a", "S0b", "S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8"]


@pytest.fixture(scope="module")
def frame() -> FrameGraph:
    return FrameGraph(SchemaLoader().load(SCHEMA_PATH))


@pytest.fixture(scope="module")
def agent() -> AgentSystem:
    return AgentSystem(
        cursor_client=MagicMock(),
        model="claude-test",
        schema_path=SCHEMA_PATH,
        system_prompt="Test.",
    )


# ---------------------------------------------------------------------------
# 1. S5 slots absent when no direct-booking signals (G6 resolution)
# ---------------------------------------------------------------------------


class TestS5NotSurfacedWithoutSignals:
    def test_s5_not_reachable_ota_only_channels(self, frame):
        """OTA-only channels must exclude all S5 slots from the reachable set."""
        facts = {"channels": ["airbnb", "booking", "vrbo"]}
        signals = _detect_signals(facts)
        reachable_ids = {s.id for s in frame.reachable_slots(facts, ["S5"], signals=signals)}
        assert not reachable_ids, (
            f"No S5 slots must be reachable for OTA-only channels; got {reachable_ids}"
        )

    def test_s5_not_reachable_empty_channels(self, frame):
        """Empty channels → no direct signal → S5 unreachable."""
        facts: dict = {}
        signals = _detect_signals(facts)
        reachable_ids = {s.id for s in frame.reachable_slots(facts, ["S5"], signals=signals)}
        assert "website_brand_name" not in reachable_ids

    def test_s5_not_reachable_no_booking_website_focus(self, frame):
        """focus_topics without 'booking_website' must not open S5."""
        facts = {"focus_topics": ["pricing_strategy", "guest_messaging"]}
        signals = _detect_signals(facts)
        reachable_ids = {s.id for s in frame.reachable_slots(facts, ["S5"], signals=signals)}
        assert "website_brand_name" not in reachable_ids

    def test_s5_excluded_from_is_done_when_no_signals(self, agent):
        """_is_done must not require S5 slots when there are no direct-booking signals.
        This matches the answer-key disposition 'conditional:surface_if_direct_signals_present'."""
        state = ProfileState(profile_id="s5_none")
        # Record channels as OTA-only.
        state.slots["channels"] = SlotState(
            field_id="channels",
            status=SlotStatus.RECORDED,
            value=["airbnb", "booking"],
        )
        # Disposition all non-S5 reachable slots.
        facts = agent._frame.reachable_slots({"channels": ["airbnb", "booking"]}, _ALL_SECTIONS,
                                              signals=_detect_signals({"channels": ["airbnb", "booking"]}))
        for slot_def in facts:
            if slot_def.section != "S5":
                state.slots[slot_def.id] = SlotState(
                    field_id=slot_def.id, status=SlotStatus.SKIPPED
                )
        # _is_done should be True — S5 is not required.
        assert agent._is_done(state) is True

    def test_s5_not_in_slot_status_without_signals(self, agent):
        """website_brand_name must not appear in the status block for an OTA-only profile."""
        state = ProfileState(profile_id="s5_status_no")
        state.slots["channels"] = SlotState(
            field_id="channels",
            status=SlotStatus.RECORDED,
            value=["airbnb"],
        )
        status = agent._format_slot_status(state)
        assert "website_brand_name" not in status
        assert "website_domain" not in status
        assert "website_terms" not in status


# ---------------------------------------------------------------------------
# 2. S5 slots present when direct-booking signals exist (G6 resolution)
# ---------------------------------------------------------------------------


class TestS5SurfacedWithSignals:
    def test_s5_reachable_when_direct_channel(self, frame):
        """channels includes 'direct' must make website_brand_name reachable."""
        facts = {"channels": ["airbnb", "direct"]}
        signals = _detect_signals(facts)
        reachable_ids = {s.id for s in frame.reachable_slots(facts, ["S5"], signals=signals)}
        assert "website_brand_name" in reachable_ids, (
            "website_brand_name must be reachable when channels includes 'direct'"
        )

    def test_s5_reachable_when_booking_website_in_focus_topics(self, frame):
        """focus_topics includes 'booking_website' must make website_brand_name reachable."""
        facts = {"focus_topics": ["booking_website", "pricing_strategy"]}
        signals = _detect_signals(facts)
        reachable_ids = {s.id for s in frame.reachable_slots(facts, ["S5"], signals=signals)}
        assert "website_brand_name" in reachable_ids, (
            "website_brand_name must be reachable when focus_topics includes 'booking_website'"
        )

    def test_s5_in_slot_status_with_direct_channel(self, agent):
        """website_brand_name must appear as unanswered in status when channels includes 'direct'."""
        state = ProfileState(profile_id="s5_yes_status")
        state.slots["channels"] = SlotState(
            field_id="channels",
            status=SlotStatus.RECORDED,
            value=["airbnb", "direct"],
        )
        status = agent._format_slot_status(state)
        assert "website_brand_name" in status

    def test_s5_not_done_when_direct_channel_and_s5_unanswered(self, agent):
        """_is_done must be False when direct channel is recorded and S5 slots remain."""
        state = ProfileState(profile_id="s5_not_done")
        state.slots["channels"] = SlotState(
            field_id="channels",
            status=SlotStatus.RECORDED,
            value=["direct"],
        )
        # S5 is reachable and unanswered → not done.
        assert agent._is_done(state) is False

    def test_s5_done_when_direct_and_s5_dispositioned(self, agent):
        """_is_done must be True when direct channel present but S5 slots are dispositioned."""
        state = ProfileState(profile_id="s5_done")
        state.slots["channels"] = SlotState(
            field_id="channels",
            status=SlotStatus.RECORDED,
            value=["airbnb", "direct"],
        )
        # Disposition all reachable slots (skip everything for simplicity).
        facts = {"channels": ["airbnb", "direct"]}
        signals = _detect_signals(facts)
        reachable = agent._frame.reachable_slots(facts, _ALL_SECTIONS, signals=signals)
        for slot_def in reachable:
            state.slots[slot_def.id] = SlotState(
                field_id=slot_def.id, status=SlotStatus.SKIPPED
            )
        # Re-record channels so it stays recorded.
        state.slots["channels"] = SlotState(
            field_id="channels",
            status=SlotStatus.RECORDED,
            value=["airbnb", "direct"],
        )
        assert agent._is_done(state) is True


# ---------------------------------------------------------------------------
# 3. S5 sub-slot chain (website_brand_name → website_domain → website_terms)
# ---------------------------------------------------------------------------


class TestS5SubSlotChain:
    def test_website_domain_requires_brand_name_recorded(self, frame):
        """website_domain must only be reachable after website_brand_name is recorded."""
        # Without brand name recorded — domain should not be reachable.
        facts_no_brand = {"channels": ["direct"]}
        signals = _detect_signals(facts_no_brand)
        reachable_ids = {
            s.id for s in frame.reachable_slots(facts_no_brand, ["S5"], signals=signals)
        }
        assert "website_domain" not in reachable_ids, (
            "website_domain must not be reachable until website_brand_name is recorded"
        )

    def test_website_domain_reachable_after_brand_name(self, frame):
        """website_domain must be reachable once website_brand_name is recorded."""
        facts_with_brand = {
            "channels": ["direct"],
            "website_brand_name": "Beachfront Rentals",
        }
        signals = _detect_signals(facts_with_brand)
        reachable_ids = {
            s.id for s in frame.reachable_slots(facts_with_brand, ["S5"], signals=signals)
        }
        assert "website_domain" in reachable_ids, (
            "website_domain must be reachable after website_brand_name is recorded"
        )

    def test_website_terms_requires_domain_recorded(self, frame):
        """website_terms must only be reachable after website_domain is recorded."""
        facts_no_domain = {
            "channels": ["direct"],
            "website_brand_name": "Beachfront Rentals",
        }
        signals = _detect_signals(facts_no_domain)
        reachable_ids = {
            s.id for s in frame.reachable_slots(facts_no_domain, ["S5"], signals=signals)
        }
        assert "website_terms" not in reachable_ids, (
            "website_terms must not be reachable until website_domain is recorded"
        )

    def test_website_terms_reachable_after_domain(self, frame):
        facts_with_domain = {
            "channels": ["direct"],
            "website_brand_name": "Beachfront Rentals",
            "website_domain": "custom_domain",
        }
        signals = _detect_signals(facts_with_domain)
        reachable_ids = {
            s.id for s in frame.reachable_slots(facts_with_domain, ["S5"], signals=signals)
        }
        assert "website_terms" in reachable_ids


# ---------------------------------------------------------------------------
# 4. Detect signals function (pure unit)
# ---------------------------------------------------------------------------


class TestDetectSignalsS5:
    """_detect_signals must correctly derive S5-relevant signals from recorded facts."""

    def test_direct_only_channel(self):
        s = _detect_signals({"channels": ["direct"]})
        assert s["channels_includes_direct"] is True
        assert s["focus_topics_includes_booking_website"] is False

    def test_mixed_channels_with_direct(self):
        s = _detect_signals({"channels": ["airbnb", "direct", "booking"]})
        assert s["channels_includes_direct"] is True

    def test_booking_website_focus(self):
        s = _detect_signals({"focus_topics": ["booking_website", "channel_mix"]})
        assert s["focus_topics_includes_booking_website"] is True
        assert s["channels_includes_direct"] is False

    def test_both_signals(self):
        s = _detect_signals({
            "channels": ["airbnb", "direct"],
            "focus_topics": ["booking_website"],
        })
        assert s["channels_includes_direct"] is True
        assert s["focus_topics_includes_booking_website"] is True

    def test_empty_lists_give_no_signals(self):
        s = _detect_signals({"channels": [], "focus_topics": []})
        assert s["channels_includes_direct"] is False
        assert s["focus_topics_includes_booking_website"] is False

    def test_none_values_give_no_signals(self):
        s = _detect_signals({"channels": None, "focus_topics": None})
        assert s["channels_includes_direct"] is False
        assert s["focus_topics_includes_booking_website"] is False
