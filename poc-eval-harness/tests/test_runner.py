"""Story 4.4 — campaign orchestration (idempotent/resumable/retry) + the conversation loop."""

from __future__ import annotations

import asyncio
from pathlib import Path

import pytest

from harness.manifest import FreezeManifest
from harness.records import RunRecord, RunStatus
from harness.runner import (
    CampaignError,
    RetryPolicy,
    RunContext,
    is_transient,
    run_campaign,
    run_conversation,
)
from kernel.protocol import EndConversation, UserQuestion
from kernel.state import ProfileState, StateReducer
from kernel.tools import RecordAnswer
from kernel.trace import TraceReader, TraceWriter


# ---------------------------------------------------------------------------
# Fakes
# ---------------------------------------------------------------------------


class _FakeSimulator:
    def reply(self, question: UserQuestion) -> str:
        return f"answer to {question.primary_slot or 'open'}"


class _ScriptedSystem:
    """A System that asks one question, records one slot, then ends."""

    system_id = "agent"

    def __init__(self) -> None:
        self._step = 0

    def next_action(self, state: ProfileState, history):
        self._step += 1
        if self._step == 1:
            return UserQuestion(text="How many listings?", primary_slot="listing_count")
        if self._step == 2:
            return [RecordAnswer(field_id="listing_count", value=5, source="user_stated")]
        return EndConversation(reason="completed")


def _manifest(tmp_path) -> FreezeManifest:
    (tmp_path / "f.txt").write_text("frozen", encoding="utf-8")
    return FreezeManifest.build({"f": tmp_path / "f.txt"}, schema_version="v0.3", git_sha="abc")


# ---------------------------------------------------------------------------
# Conversation loop
# ---------------------------------------------------------------------------


class TestRunConversation:
    def test_loop_emits_canonical_trace_and_records_slot(self, tmp_path):
        trace_path = tmp_path / "t.jsonl"
        writer = TraceWriter(trace_path)
        reducer = StateReducer(frame=None)
        state, reason = run_conversation(
            _ScriptedSystem(), _FakeSimulator(),
            reducer=reducer, trace=writer, profile_id="A1",
        )
        assert reason == "completed"
        assert state.slots["listing_count"].value == 5

        kinds = [type(e).__name__ for e in TraceReader(trace_path).events()]
        # question → tool_call → session_end (harness-owned trace, R-10).
        assert kinds == ["UserFacingQuestion", "ToolCallEvent", "SessionEnd"]

    def test_turn_cap_marks_incomplete(self, tmp_path):
        class _Endless:
            system_id = "agent"
            def next_action(self, state, history):
                return UserQuestion(text="again?", primary_slot=None)

        writer = TraceWriter(tmp_path / "t.jsonl")
        _, reason = run_conversation(
            _Endless(), _FakeSimulator(),
            reducer=StateReducer(frame=None), trace=writer, profile_id="A1", max_turns=3,
        )
        assert reason == "incomplete_turn_cap"

    def test_drains_system_echo_events(self, tmp_path):
        from kernel.trace import EchoIssued

        class _Echoer:
            system_id = "agent"
            def __init__(self):
                self._step = 0
                self._pending = [EchoIssued(turn=0, slot="security_deposit_amount", value=250.0)]
            def next_action(self, state, history):
                self._step += 1
                return EndConversation(reason="completed")
            def drain_trace_events(self):
                out, self._pending = self._pending, []
                return out

        writer = TraceWriter(tmp_path / "t.jsonl")
        run_conversation(_Echoer(), _FakeSimulator(),
                         reducer=StateReducer(frame=None), trace=writer, profile_id="A1")
        kinds = [type(e).__name__ for e in TraceReader(tmp_path / "t.jsonl").events()]
        assert "EchoIssued" in kinds


# ---------------------------------------------------------------------------
# is_transient
# ---------------------------------------------------------------------------


class TestIsTransient:
    def test_429_is_transient(self):
        exc = RuntimeError("rate limited"); exc.status_code = 429
        assert is_transient(exc)

    def test_503_is_transient(self):
        exc = RuntimeError("unavailable"); exc.status = 503
        assert is_transient(exc)

    def test_400_is_not_transient(self):
        exc = RuntimeError("bad request"); exc.status_code = 400
        assert not is_transient(exc)

    def test_value_error_not_transient(self):
        assert not is_transient(ValueError("nope"))


# ---------------------------------------------------------------------------
# Campaign orchestration
# ---------------------------------------------------------------------------


def _completed_run_fn(calls: list[str]):
    async def run_fn(ctx: RunContext) -> RunRecord:
        calls.append(ctx.key)
        return RunRecord(
            manifest_hash=ctx.manifest_hash, profile_id=ctx.profile_id,
            system_id=ctx.system_id, run_index=ctx.run_index,
            status=RunStatus.COMPLETED, end_reason="completed", seed=ctx.seed,
        )
    return run_fn


class TestRunCampaign:
    def test_produces_k_runs_per_profile_per_system(self, tmp_path):
        m = _manifest(tmp_path)
        calls: list[str] = []
        res = asyncio.run(run_campaign(
            m, systems=["agent", "tree"], profiles=["A1", "B2"],
            run_fn=_completed_run_fn(calls), k=5, base_dir=tmp_path / "campaigns",
        ))
        assert len(calls) == 2 * 2 * 5  # systems × profiles × k
        assert res.completed == 20
        # Records written under campaigns/<hash>/runs/.
        runs_dir = Path(tmp_path / "campaigns" / m.manifest_hash / "runs")
        assert len(list(runs_dir.glob("*.json"))) == 20
        assert (tmp_path / "campaigns" / m.manifest_hash / "manifest.json").exists()

    def test_idempotent_second_run_recomputes_nothing(self, tmp_path):
        m = _manifest(tmp_path)
        calls: list[str] = []
        kwargs = dict(systems=["agent"], profiles=["A1"], k=3, base_dir=tmp_path / "campaigns")
        asyncio.run(run_campaign(m, run_fn=_completed_run_fn(calls), **kwargs))
        assert len(calls) == 3
        # Second invocation: every key already has a record → no recomputation.
        res2 = asyncio.run(run_campaign(m, run_fn=_completed_run_fn(calls), **kwargs))
        assert len(calls) == 3  # unchanged
        assert res2.skipped == 3

    def test_resume_runs_only_missing_keys(self, tmp_path):
        m = _manifest(tmp_path)
        # Pre-write run_index 0 only; resume must fill 1 and 2.
        runs_dir = tmp_path / "campaigns" / m.manifest_hash / "runs"
        runs_dir.mkdir(parents=True)
        RunRecord(
            manifest_hash=m.manifest_hash, profile_id="A1", system_id="agent",
            run_index=0, status=RunStatus.COMPLETED, end_reason="completed",
        ).write(runs_dir / (RunRecord.make_key("A1", "agent", 0) + ".json"))

        calls: list[str] = []
        res = asyncio.run(run_campaign(
            m, systems=["agent"], profiles=["A1"], k=3,
            run_fn=_completed_run_fn(calls), base_dir=tmp_path / "campaigns",
        ))
        assert sorted(calls) == [RunRecord.make_key("A1", "agent", i) for i in (1, 2)]
        assert res.skipped == 1

    def test_transient_error_is_retried_then_succeeds(self, tmp_path):
        m = _manifest(tmp_path)
        attempts = {"n": 0}

        async def flaky(ctx: RunContext) -> RunRecord:
            attempts["n"] += 1
            if attempts["n"] < 3:
                exc = RuntimeError("rate limited"); exc.status_code = 429
                raise exc
            return RunRecord(
                manifest_hash=ctx.manifest_hash, profile_id=ctx.profile_id,
                system_id=ctx.system_id, run_index=ctx.run_index,
                status=RunStatus.COMPLETED, end_reason="completed",
            )

        res = asyncio.run(run_campaign(
            m, systems=["agent"], profiles=["A1"], k=1, run_fn=flaky,
            base_dir=tmp_path / "campaigns",
            retry_policy=RetryPolicy(max_attempts=4, base_delay=0.0, jitter=0.0),
        ))
        assert attempts["n"] == 3
        assert res.completed == 1

    def test_exhausted_retries_records_errored(self, tmp_path):
        m = _manifest(tmp_path)

        async def always_429(ctx: RunContext) -> RunRecord:
            exc = RuntimeError("rate limited"); exc.status_code = 429
            raise exc

        res = asyncio.run(run_campaign(
            m, systems=["agent"], profiles=["A1"], k=1, run_fn=always_429,
            base_dir=tmp_path / "campaigns",
            retry_policy=RetryPolicy(max_attempts=2, base_delay=0.0, jitter=0.0),
        ))
        assert res.errored == 1
        assert res.records[0].status is RunStatus.ERRORED
        assert "RuntimeError" in (res.records[0].error or "")

    def test_hard_error_records_errored_without_retry(self, tmp_path):
        m = _manifest(tmp_path)
        attempts = {"n": 0}

        async def bad(ctx: RunContext) -> RunRecord:
            attempts["n"] += 1
            raise ValueError("non-transient")

        res = asyncio.run(run_campaign(
            m, systems=["agent"], profiles=["A1"], k=1, run_fn=bad,
            base_dir=tmp_path / "campaigns",
            retry_policy=RetryPolicy(max_attempts=4, base_delay=0.0, jitter=0.0),
        ))
        assert attempts["n"] == 1  # no retry on hard error
        assert res.errored == 1

    def test_frozen_without_manifest_aborts(self, tmp_path):
        with pytest.raises(CampaignError, match="without a freeze manifest"):
            asyncio.run(run_campaign(
                None, systems=["agent"], profiles=["A1"], k=1,
                run_fn=_completed_run_fn([]), base_dir=tmp_path / "campaigns",
            ))

    def test_frozen_with_invalid_manifest_aborts(self, tmp_path):
        m = _manifest(tmp_path)
        (tmp_path / "f.txt").write_text("CHANGED AFTER FREEZE", encoding="utf-8")
        with pytest.raises(CampaignError, match="hash mismatch"):
            asyncio.run(run_campaign(
                m, systems=["agent"], profiles=["A1"], k=1,
                run_fn=_completed_run_fn([]), base_dir=tmp_path / "campaigns",
            ))

    def test_refreeze_cap_exceeded_aborts(self, tmp_path):
        (tmp_path / "f.txt").write_text("frozen", encoding="utf-8")
        m = FreezeManifest.build(
            {"f": tmp_path / "f.txt"}, schema_version="v0.3", git_sha="abc",
            refreeze_count=3, pm_override=True,  # build allows with override
        )
        object.__setattr__(m, "pm_override", False)  # simulate missing override at run time
        with pytest.raises(Exception):
            asyncio.run(run_campaign(
                m, systems=["agent"], profiles=["A1"], k=1,
                run_fn=_completed_run_fn([]), base_dir=tmp_path / "campaigns",
            ))
