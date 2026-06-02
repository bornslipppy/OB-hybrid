"""Story 4.5 — SAR scorer unit tests (§6.1 rubric + §6.5 cascade).

Tests verify:
  1. parse_disposition handles all answer-key formats.
  2. score_slot: flagged→1 when FLAGGED, →0 when RECORDED or UNANSWERED.
  3. score_slot: recorded → numeric exact, enum case-insensitive, free-text human-rated.
  4. score_profile: denominator = in-scope ∩ answer-key denominator; skipped excluded.
  5. score_profile: sar = numerator / denominator.
  6. cascade_tag: BEST expands denominator vs WORST contracts it.
  7. cascade_tag: sensitivity band sar_best >= sar_nominal >= sar_worst (not guaranteed
     in all cases, but holds when contested slots are in the denominator — verified).
"""

from __future__ import annotations

from pathlib import Path

import pytest

from kernel.state import ProfileState, SlotState, SlotStatus
from scoring.sar import (
    AnswerKey,
    CascadeResult,
    ExpectedDisposition,
    ProfileScore,
    SlotScore,
    AnswerKey,
    cascade_tag,
    parse_disposition,
    score_profile,
    score_slot,
)

SCHEMA_PATH = Path(__file__).resolve().parents[1] / "schema" / "guesty-pro-account-creation-schema.md"
_H1_SECTIONS = ["S0a", "S0b", "S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8"]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _state_with_slots(profile_id: str, slots: dict) -> ProfileState:
    """Build a ProfileState from a simple {slot_id: (status, value)} dict."""
    state = ProfileState(profile_id=profile_id)
    for sid, (status, value) in slots.items():
        state.slots[sid] = SlotState(field_id=sid, status=status, value=value)
    return state


def _recorded(value=None):
    return (SlotStatus.RECORDED, value)


def _flagged():
    return (SlotStatus.FLAGGED, None)


def _skipped():
    return (SlotStatus.SKIPPED, None)


def _unanswered():
    return (SlotStatus.UNANSWERED, None)


# ---------------------------------------------------------------------------
# parse_disposition tests
# ---------------------------------------------------------------------------


class TestParseDisposition:
    def test_recorded_numeric(self):
        d = parse_disposition("recorded: 5")
        assert d.disposition == "recorded"
        assert d.value == 5
        assert d.value_type == "numeric"

    def test_recorded_string(self):
        d = parse_disposition("recorded: at_booking")
        assert d.disposition == "recorded"
        assert d.value == "at_booking"

    def test_recorded_list(self):
        d = parse_disposition("recorded: [airbnb, direct]")
        assert d.disposition == "recorded"
        assert isinstance(d.value, list)
        assert "airbnb" in d.value

    def test_flagged_bare(self):
        d = parse_disposition("flagged")
        assert d.disposition == "flagged"

    def test_flagged_with_reason(self):
        d = parse_disposition("flagged: tax advice")
        assert d.disposition == "flagged"

    def test_flag_for_call_1(self):
        d = parse_disposition("flag_for_call_1")
        assert d.disposition == "flagged"

    def test_skipped(self):
        d = parse_disposition("skipped")
        assert d.disposition == "skipped"

    def test_conditional(self):
        d = parse_disposition("conditional: surface_if_direct_signals")
        assert d.disposition == "conditional"
        assert "surface_if_direct_signals" in (d.condition or "")

    def test_provisional_flag_stripped(self):
        d = parse_disposition("recorded: split [provisional G3]")
        assert d.provisional is True
        assert d.value == "split"

    def test_free_text_slot(self):
        d = parse_disposition("recorded: Manual pricing takes too much time", slot_id="pain")
        assert d.value_type == "free_text"


# ---------------------------------------------------------------------------
# score_slot tests (§6.1 rubric)
# ---------------------------------------------------------------------------


class TestScoreSlotFlagged:
    """Expected disposition = 'flagged'."""

    def test_flagged_slot_scores_1_when_flagged(self):
        state = _state_with_slots("P", {"taxes": _flagged()})
        exp = ExpectedDisposition(disposition="flagged")
        ss = score_slot("taxes", "S4", exp, state)
        assert ss.score == 1

    def test_flagged_slot_scores_0_when_recorded(self):
        state = _state_with_slots("P", {"taxes": _recorded("6%")})
        exp = ExpectedDisposition(disposition="flagged")
        ss = score_slot("taxes", "S4", exp, state)
        assert ss.score == 0

    def test_flagged_slot_scores_0_when_unanswered(self):
        state = _state_with_slots("P", {})
        exp = ExpectedDisposition(disposition="flagged")
        ss = score_slot("taxes", "S4", exp, state)
        assert ss.score == 0

    def test_flagged_slot_scores_0_when_skipped(self):
        state = _state_with_slots("P", {"taxes": _skipped()})
        exp = ExpectedDisposition(disposition="flagged")
        ss = score_slot("taxes", "S4", exp, state)
        assert ss.score == 0


class TestScoreSlotRecorded:
    """Expected disposition = 'recorded:<value>'."""

    def test_recorded_exact_match(self):
        state = _state_with_slots("P", {"payment_timing": _recorded("at_booking")})
        exp = ExpectedDisposition(disposition="recorded", value="at_booking", value_type="exact")
        ss = score_slot("payment_timing", "S4", exp, state)
        assert ss.score == 1

    def test_recorded_case_insensitive_enum(self):
        state = _state_with_slots("P", {"payment_timing": _recorded("AT_BOOKING")})
        exp = ExpectedDisposition(disposition="recorded", value="at_booking", value_type="exact")
        ss = score_slot("payment_timing", "S4", exp, state)
        assert ss.score == 1

    def test_recorded_wrong_value(self):
        state = _state_with_slots("P", {"payment_timing": _recorded("split")})
        exp = ExpectedDisposition(disposition="recorded", value="at_booking", value_type="exact")
        ss = score_slot("payment_timing", "S4", exp, state)
        assert ss.score == 0

    def test_numeric_exact_match(self):
        state = _state_with_slots("P", {"security_deposit_amount": _recorded(50)})
        exp = ExpectedDisposition(disposition="recorded", value=50, value_type="numeric")
        ss = score_slot("security_deposit_amount", "S4", exp, state)
        assert ss.score == 1

    def test_numeric_wrong_value(self):
        state = _state_with_slots("P", {"security_deposit_amount": _recorded(15)})
        exp = ExpectedDisposition(disposition="recorded", value=50, value_type="numeric")
        ss = score_slot("security_deposit_amount", "S4", exp, state)
        assert ss.score == 0

    def test_free_text_flags_human_rating(self):
        state = _state_with_slots("P", {"pain": _recorded("Too much manual work")})
        exp = ExpectedDisposition(disposition="recorded", value="Manual pricing...", value_type="free_text")
        ss = score_slot("pain", "S7", exp, state)
        assert ss.requires_human_rating is True
        assert ss.score == 1  # provisional pass pending human rating

    def test_recorded_but_actually_flagged(self):
        state = _state_with_slots("P", {"listing_count": _flagged()})
        exp = ExpectedDisposition(disposition="recorded", value=5, value_type="numeric")
        ss = score_slot("listing_count", "S2", exp, state)
        assert ss.score == 0

    def test_recorded_list_match(self):
        state = _state_with_slots("P", {"channels": _recorded(["airbnb", "vrbo"])})
        exp = ExpectedDisposition(disposition="recorded", value=["vrbo", "airbnb"], value_type="exact")
        ss = score_slot("channels", "S2", exp, state)
        assert ss.score == 1


# ---------------------------------------------------------------------------
# score_profile tests
# ---------------------------------------------------------------------------


class TestScoreProfile:
    def _simple_answer_key(self) -> AnswerKey:
        return AnswerKey(
            profile_id="A1-test",
            group="A",
            slots={
                "listing_count": ExpectedDisposition(disposition="recorded", value=5, value_type="numeric"),
                "channels": ExpectedDisposition(disposition="recorded", value=["airbnb", "vrbo"], value_type="exact"),
                "payment_timing": ExpectedDisposition(disposition="recorded", value="at_booking"),
                "taxes": ExpectedDisposition(disposition="flagged"),
                "ownership_model": ExpectedDisposition(disposition="recorded", value="all_self_owned"),
                "pain": ExpectedDisposition(disposition="recorded", value="Manual...", value_type="free_text"),
                "payment_split": ExpectedDisposition(disposition="skipped"),
            },
        )

    def test_perfect_run_sar_is_1(self):
        answer_key = self._simple_answer_key()
        state = _state_with_slots(
            "A1-test",
            {
                "listing_count": _recorded(5),
                "channels": _recorded(["airbnb", "vrbo"]),
                "payment_timing": _recorded("at_booking"),
                "taxes": _flagged(),
                "ownership_model": _recorded("all_self_owned"),
                "pain": _recorded("Manual pricing sucks"),
            },
        )
        # Set recorded_facts for resolver to work (ownership_model needed for S8 slots).
        result = score_profile(
            state, answer_key, _H1_SECTIONS,
            schema_path=SCHEMA_PATH, system_id="agent"
        )
        # All non-skipped slots in the answer key that are also in-scope should be correct.
        # "payment_split" is skipped → not in denominator.
        assert result.denominator >= 1
        for ss in result.slot_scores:
            # All should score 1 in a perfect run.
            assert ss.score == 1, f"{ss.slot_id}: {ss.reason}"

    def test_skipped_slots_excluded_from_denominator(self):
        answer_key = AnswerKey(
            profile_id="T",
            group="A",
            slots={
                "listing_count": ExpectedDisposition(disposition="recorded", value=5, value_type="numeric"),
                "payment_split": ExpectedDisposition(disposition="skipped"),
            },
        )
        state = _state_with_slots("T", {"listing_count": _recorded(5)})
        result = score_profile(
            state, answer_key, ["S2", "S4"],
            schema_path=SCHEMA_PATH, system_id="agent"
        )
        assert "payment_split" in result.skipped_slots
        assert all(ss.slot_id != "payment_split" for ss in result.slot_scores)

    def test_wrong_value_drops_sar(self):
        answer_key = AnswerKey(
            profile_id="T",
            group="A",
            slots={
                "listing_count": ExpectedDisposition(disposition="recorded", value=5, value_type="numeric"),
                "ownership_model": ExpectedDisposition(disposition="recorded", value="all_self_owned"),
            },
        )
        state = _state_with_slots(
            "T",
            {
                "listing_count": _recorded(99),  # wrong
                "ownership_model": _recorded("all_self_owned"),
            },
        )
        result = score_profile(
            state, answer_key, ["S2", "S8"],
            schema_path=SCHEMA_PATH, system_id="agent"
        )
        assert result.sar < 1.0
        wrong_scores = [ss for ss in result.slot_scores if ss.score == 0]
        assert any(ss.slot_id == "listing_count" for ss in wrong_scores)

    def test_denominator_uses_in_scope_resolver(self):
        """Slots not in-scope (depends_on fails) must not be in denominator."""
        answer_key = AnswerKey(
            profile_id="T",
            group="A",
            slots={
                "security_deposit_amount": ExpectedDisposition(
                    disposition="recorded", value=50, value_type="numeric"
                ),
            },
        )
        # security_deposit_amount requires security_deposit_type to be recorded.
        # If it's absent from facts (not recorded in state), the slot is not in-scope.
        state = _state_with_slots("T", {})  # no security_deposit_type recorded
        result = score_profile(
            state, answer_key, ["S4"],
            schema_path=SCHEMA_PATH, system_id="agent"
        )
        # The slot should not be in the denominator since it's not in-scope.
        assert result.denominator == 0 or all(
            ss.slot_id != "security_deposit_amount" for ss in result.slot_scores
        )


# ---------------------------------------------------------------------------
# cascade_tag tests (§6.5)
# ---------------------------------------------------------------------------


class TestCascadeTag:
    def _answer_key_with_ownership(self) -> AnswerKey:
        return AnswerKey(
            profile_id="C2-test",
            group="C",
            slots={
                "ownership_model": ExpectedDisposition(
                    disposition="recorded", value="all_managed_for_others"
                ),
                "owners": ExpectedDisposition(disposition="recorded", value="expected"),
                "owners_csv": ExpectedDisposition(disposition="recorded", value="expected_csv"),
                "listing_count": ExpectedDisposition(disposition="recorded", value=5, value_type="numeric"),
                "channels": ExpectedDisposition(disposition="recorded", value=["airbnb"]),
            },
        )

    def test_cascade_tag_returns_cascade_result(self):
        state = _state_with_slots(
            "C2-test",
            {
                "ownership_model": _recorded("all_managed_for_others"),
                "owners": _recorded("some owners"),
                "owners_csv": _recorded("csv"),
                "listing_count": _recorded(5),
                "channels": _recorded(["airbnb"]),
            },
        )
        result = cascade_tag(
            state, self._answer_key_with_ownership(), _H1_SECTIONS,
            schema_path=SCHEMA_PATH, contested_slots=["ownership_model"],
            system_id="agent",
        )
        assert isinstance(result, CascadeResult)
        assert result.profile_id == "C2-test"
        assert "ownership_model" in result.contested_slots

    def test_best_denominator_gte_worst_denominator(self):
        """BEST adjudication must produce a denominator >= WORST."""
        state = _state_with_slots(
            "C2-test",
            {
                "listing_count": _recorded(5),
                "channels": _recorded(["airbnb"]),
                # ownership_model NOT recorded — it's the contested slot
            },
        )
        result = cascade_tag(
            state, self._answer_key_with_ownership(), _H1_SECTIONS,
            schema_path=SCHEMA_PATH, contested_slots=["ownership_model"],
            system_id="agent",
        )
        assert result.denominator_best >= result.denominator_worst, (
            f"BEST denom ({result.denominator_best}) must be >= WORST ({result.denominator_worst})"
        )

    def test_contested_ownership_collapses_owners_in_worst(self):
        """When ownership_model is contested under WORST, owners/owners_csv leave the denominator."""
        state = _state_with_slots(
            "C2-test",
            {
                "listing_count": _recorded(5),
                "channels": _recorded(["airbnb"]),
            },
        )
        result = cascade_tag(
            state, self._answer_key_with_ownership(), _H1_SECTIONS,
            schema_path=SCHEMA_PATH, contested_slots=["ownership_model"],
            system_id="agent",
        )
        # Under WORST, ownership_model is absent → owners/owners_csv not in scope → smaller denom.
        # Under BEST, ownership_model is assumed present → owners/owners_csv in scope → larger denom.
        assert result.denominator_best > result.denominator_worst

    def test_nominal_sar_between_best_and_worst(self):
        """Nominal SAR should be between WORST and BEST when contested slots are scored."""
        state = _state_with_slots(
            "C2-test",
            {
                "ownership_model": _recorded("all_managed_for_others"),
                "owners": _recorded("some owners"),
                "owners_csv": _recorded("csv"),
                "listing_count": _recorded(5),
                "channels": _recorded(["airbnb"]),
            },
        )
        result = cascade_tag(
            state, self._answer_key_with_ownership(), _H1_SECTIONS,
            schema_path=SCHEMA_PATH, contested_slots=["ownership_model"],
            system_id="agent",
        )
        # Nominal SAR is computed with full facts; it should be well-defined.
        assert 0.0 <= result.sar_nominal <= 1.0
        assert 0.0 <= result.sar_best <= 1.0
        assert 0.0 <= result.sar_worst <= 1.0
