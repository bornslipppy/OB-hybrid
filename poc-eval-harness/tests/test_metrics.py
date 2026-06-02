"""Story 4.6 — secondary metrics other than false-write (EC-32 / EC-31 / EC-20 / SM-C2 / SM-10)."""

from __future__ import annotations

from kernel.trace import EchoIssued, ToolCallEvent, UserConfirmed, UserFacingQuestion
from scoring.metrics import (
    clarification_efficiency,
    cost_latency,
    inappropriate_advice_rate,
    questions_ratio,
    questions_to_completion,
)


def _q(turn, slot=None, text="?"):
    return UserFacingQuestion(turn=turn, slot=slot, text=text)


def _record(turn, field_id, value="x", source="user_stated"):
    return ToolCallEvent(turn=turn, tool="record_answer",
                         args={"field_id": field_id, "value": value, "source": source})


def _flag(turn, field_id):
    return ToolCallEvent(turn=turn, tool="flag_for_call_1",
                         args={"topic": field_id, "user_quote": "q", "note": "n", "field_id": field_id})


def _skip(turn, field_id):
    return ToolCallEvent(turn=turn, tool="skip_question", args={"field_id": field_id, "reason": "r"})


class TestQuestionsToCompletion:
    def test_counts_only_user_facing_questions(self):
        trace = [
            _q(1, "listing_count"),
            EchoIssued(turn=2, slot="security_deposit_amount", value=250.0),  # excluded (EC-32)
            UserConfirmed(turn=3, slot="security_deposit_amount"),
            _q(4, "channels"),
        ]
        assert questions_to_completion(trace) == 2

    def test_empty_trace(self):
        assert questions_to_completion([]) == 0


class TestQuestionsRatio:
    def test_within_bound_passes(self):
        r = questions_ratio(12, 10, bound=1.2)
        assert r.applicable and r.ratio == 1.2 and r.passes is True

    def test_over_bound_fails(self):
        r = questions_ratio(13, 10, bound=1.2)
        assert r.passes is False

    def test_zero_baseline_is_na(self):
        r = questions_ratio(7, 0)
        assert r.applicable is False and r.ratio is None and r.passes is None
        assert r.ai_questions == 7  # absolute count retained (EC-31)


class TestClarificationEfficiency:
    def test_auto_detect_resolved_in_one_followup(self):
        # listing_count asked twice (1 follow-up) then recorded → resolved.
        trace = [_q(1, "listing_count"), _q(2, "listing_count"), _record(3, "listing_count", 5)]
        res = clarification_efficiency(trace)
        assert res.total == 1 and res.resolved == 1 and res.rate == 1.0

    def test_flag_and_skip_after_one_clarification_counts_resolved(self):
        # EC-20: a correct flag+skip after one unsuccessful clarification is "resolved".
        trace = [_q(1, "taxes"), _q(2, "taxes"), _flag(3, "taxes"), _skip(4, "taxes")]
        res = clarification_efficiency(trace)
        assert res.resolved == 1 and res.rate == 1.0

    def test_two_followups_not_resolved(self):
        trace = [_q(1, "channels"), _q(2, "channels"), _q(3, "channels"), _record(4, "channels", ["airbnb"])]
        res = clarification_efficiency(trace)
        assert res.total == 1 and res.resolved == 0 and res.rate == 0.0

    def test_explicit_ambiguous_slots_resolved_first_answer(self):
        # Marked ambiguous but resolved on first answer (0 follow-ups) → resolved.
        trace = [_q(1, "payment_timing"), _record(2, "payment_timing", "at_booking")]
        res = clarification_efficiency(trace, ambiguous_slots=["payment_timing"])
        assert res.total == 1 and res.resolved == 1

    def test_no_episodes_rate_is_one(self):
        assert clarification_efficiency([_q(1, "listing_count")]).rate == 1.0


class TestInappropriateAdviceRate:
    def test_flagging_advice_input_is_clean(self):
        trace = [_q(1, "rate_strategy"), _flag(2, "rate_strategy")]
        res = inappropriate_advice_rate(trace, advice_slots=["rate_strategy"])
        assert res.total == 1 and res.is_clean and res.rate == 0.0

    def test_recording_recommendation_is_inappropriate(self):
        trace = [_q(1, "rate_strategy"), _record(2, "rate_strategy", "dynamic", source="inferred")]
        res = inappropriate_advice_rate(trace, advice_slots=["rate_strategy"])
        assert res.inappropriate == 1 and res.rate == 1.0
        assert res.detections[0].slot == "rate_strategy"

    def test_advice_slot_never_surfaced_not_in_denominator(self):
        trace = [_q(1, "listing_count"), _record(2, "listing_count", 5)]
        res = inappropriate_advice_rate(trace, advice_slots=["rate_strategy"])
        assert res.total == 0 and res.rate == 0.0


class TestCostLatency:
    def test_baseline_no_usage_is_zero(self):
        trace = [_q(1, "listing_count"), _record(2, "listing_count", 5)]
        cl = cost_latency(trace)
        assert cl.total_tokens == 0 and cl.cost_usd == 0.0 and cl.n_samples == 0

    def test_explicit_usage_dicts_aggregate(self):
        usage = [
            {"input_tokens": 100, "output_tokens": 20, "cost_usd": 0.001, "latency_ms": 800},
            {"input_tokens": 50, "output_tokens": 10, "cost_usd": 0.0005, "latency_ms": 400},
        ]
        cl = cost_latency([], usage=usage)
        assert cl.input_tokens == 150 and cl.output_tokens == 30
        assert abs(cl.cost_usd - 0.0015) < 1e-9
        assert cl.wall_clock_ms == 1200 and cl.n_samples == 2

    def test_usage_attribute_on_events_is_read(self):
        ev = _record(1, "listing_count", 5)
        object.__setattr__(ev, "usage", {"input_tokens": 10, "output_tokens": 5})
        cl = cost_latency([ev])
        assert cl.total_tokens == 15 and cl.n_samples == 1
