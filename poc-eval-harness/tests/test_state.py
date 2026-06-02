"""Story 0.1 — ProfileState pure reducer + §3.2 end_section guard."""

from __future__ import annotations

import pytest

from kernel.schema import FrameGraph, SlotDef
from kernel.state import (
    EndSectionError,
    ProfileState,
    SlotStatus,
    StateReducer,
)
from kernel.tools import (
    AddFee,
    AddOwner,
    AddTax,
    EndSection,
    FlagForCall1,
    RecordAnswer,
    SkipQuestion,
    Source,
)
from kernel.trace import EchoIssued, UserConfirmed


@pytest.fixture
def reducer_no_frame() -> StateReducer:
    return StateReducer()


@pytest.fixture
def state() -> ProfileState:
    return ProfileState(profile_id="B1")


def test_record_answer_dispositions_slot(reducer_no_frame, state):
    out = reducer_no_frame.apply(
        state, RecordAnswer(field_id="go_live", value="asap", source=Source.USER_STATED)
    )
    assert out.slots["go_live"].status is SlotStatus.RECORDED
    assert out.slots["go_live"].value == "asap"
    assert out.slots["go_live"].source == "user_stated"


def test_apply_is_pure(reducer_no_frame, state):
    reducer_no_frame.apply(
        state, RecordAnswer(field_id="go_live", value="asap", source=Source.USER_STATED)
    )
    assert state.slots == {}  # input untouched


def test_skip_and_flag(reducer_no_frame, state):
    out = reducer_no_frame.apply(state, SkipQuestion(field_id="rate_strategy", reason="defer"))
    assert out.slots["rate_strategy"].status is SlotStatus.SKIPPED

    out2 = reducer_no_frame.apply(
        out, FlagForCall1(topic="taxes", user_quote="q", note="n", field_id="taxes")
    )
    assert out2.slots["taxes"].status is SlotStatus.FLAGGED
    assert out2.slots["taxes"].flag_ref == "taxes"


def test_flag_without_field_id_goes_to_topic_flags(reducer_no_frame, state):
    out = reducer_no_frame.apply(
        state, FlagForCall1(topic="customer_sentiment", user_quote="q", note="anxious")
    )
    assert out.flags and out.flags[0]["topic"] == "customer_sentiment"
    assert "customer_sentiment" not in out.slots  # no slot dispositioned


def test_composite_tools_append_and_disposition(reducer_no_frame, state):
    s = reducer_no_frame.apply(state, AddFee(fee_type="pet", amount=50.0, unit="flat"))
    assert s.fees[0]["fee_type"] == "pet"
    assert s.slots["mandatory_fees"].status is SlotStatus.RECORDED

    s = reducer_no_frame.apply(
        s,
        AddTax(
            tax_type="gst",
            inclusivity="inclusive",
            what_taxed=["accommodation_fare"],
            scope="account_wide",
        ),
    )
    assert s.taxes[0]["tax_type"] == "gst"

    s = reducer_no_frame.apply(
        s,
        AddOwner(
            owner_name="O",
            email="o@x.com",
            listings=["L1"],
            management_model="commission",
            pmc_commission_rate=15.0,
        ),
    )
    assert s.owners[0]["owner_name"] == "O"
    assert s.slots["owners"].status is SlotStatus.RECORDED


def test_echo_lifecycle_sets_and_clears_pending(reducer_no_frame, state):
    s = reducer_no_frame.observe(state, EchoIssued(turn=8, slot="security_deposit_amount", value=500))
    assert s.slots["security_deposit_amount"].echo_pending is True
    s = reducer_no_frame.observe(s, UserConfirmed(turn=9, slot="security_deposit_amount"))
    assert s.slots["security_deposit_amount"].echo_pending is False


def test_observe_ignores_non_echo_events(reducer_no_frame, state):
    from kernel.trace import SessionEnd

    out = reducer_no_frame.observe(state, SessionEnd(turn=1, reason="completed"))
    assert out is state  # no-op returns same object


# --- end_section guard (§3.2) -----------------------------------------------


@pytest.fixture
def s4_frame() -> FrameGraph:
    # Two S4 slots: one unconditional, one gated on a deposit-type fact.
    return FrameGraph(
        [
            SlotDef(id="payment_timing", section="S4", priority="recommended"),
            SlotDef(
                id="security_deposit_amount",
                section="S4",
                priority="recommended",
                depends_on="security_deposit_type in ['damage_waiver','security_deposit']",
            ),
        ]
    )


def test_end_section_without_frame_is_usage_error(reducer_no_frame, state):
    with pytest.raises(EndSectionError, match="without a frame"):
        reducer_no_frame.apply(state, EndSection(section_id="S4"))


def test_end_section_blocked_until_reachable_slots_dispositioned(s4_frame, state):
    reducer = StateReducer(s4_frame)
    # payment_timing is unconditional and undispositioned -> blocked.
    with pytest.raises(EndSectionError, match="payment_timing"):
        reducer.apply(state, EndSection(section_id="S4"))

    s = reducer.apply(state, RecordAnswer(field_id="payment_timing", value="at_booking", source=Source.USER_STATED))
    # security_deposit_amount is gated on a deposit-type fact not present -> not reachable -> allowed.
    out = reducer.apply(s, EndSection(section_id="S4"))
    assert out is not None


def test_end_section_blocked_when_dependent_slot_becomes_reachable(s4_frame, state):
    reducer = StateReducer(s4_frame)
    s = reducer.apply(state, RecordAnswer(field_id="payment_timing", value="split", source=Source.USER_STATED))
    # Now record a deposit type that makes security_deposit_amount reachable + undispositioned.
    s = reducer.apply(
        s, RecordAnswer(field_id="security_deposit_type", value="security_deposit", source=Source.USER_STATED)
    )
    with pytest.raises(EndSectionError, match="security_deposit_amount"):
        reducer.apply(s, EndSection(section_id="S4"))


def test_end_section_blocked_on_pending_echo(s4_frame, state):
    reducer = StateReducer(s4_frame)
    s = reducer.apply(state, RecordAnswer(field_id="payment_timing", value="at_booking", source=Source.USER_STATED))
    s = reducer.observe(s, EchoIssued(turn=3, slot="payment_timing", value="at_booking"))
    with pytest.raises(EndSectionError, match="echo_pending"):
        reducer.apply(s, EndSection(section_id="S4"))
