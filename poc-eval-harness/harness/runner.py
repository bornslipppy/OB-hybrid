"""Campaign runner — Story 4.4 (drive both systems k≥5 times under freeze discipline).

Two layers:

* ``run_conversation`` — the system-agnostic loop (ask → simulator answers → policy
  emits tool calls or the next question → reduce → repeat, until ``EndConversation`` or
  the turn cap). The **harness owns the canonical trace** (architecture §3.4 /
  ``protocol.py``): neither system owns the tool surface, the reducer, or the trace, so
  an agent↔tree difference is attributable to the policy (D-1). The runner emits
  ``user_facing_question`` / ``tool_call`` / ``session_end`` and drains any
  echo-lifecycle events a system chooses to surface via ``drain_trace_events()``.

* ``run_campaign`` — orchestration: async, bounded-concurrency, **idempotent** and
  **resumable**. Keyed on ``(manifest_hash, profile_id, system_id, run_index)``; a
  written ``RunRecord`` is never recomputed (resume runs only the missing keys).
  Transient API errors (429/5xx) are retried with backoff; exhausted retries record an
  ``errored`` run (not ``incomplete``). Refuses ``--frozen`` without a valid manifest and
  enforces the re-freeze cap. Every campaign directory is retained (FR-25 / H4).
"""

from __future__ import annotations

import asyncio
import random
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Awaitable, Callable

from kernel.protocol import EndConversation, UserQuestion
from kernel.state import ProfileState, StateReducer
from kernel.trace import SessionEnd, ToolCallEvent, TraceWriter, UserFacingQuestion

from harness.manifest import FreezeManifest
from harness.records import RunRecord, RunStatus

# ---------------------------------------------------------------------------
# Transient-error classification + retry policy (perf-notes: 429/5xx → backoff)
# ---------------------------------------------------------------------------

_TRANSIENT_STATUS = frozenset({429, 500, 502, 503, 504})


class CampaignError(RuntimeError):
    """Raised on a freeze-discipline violation that must abort the whole campaign."""


def is_transient(exc: BaseException) -> bool:
    """True for retryable API errors: rate limits (429) and 5xx server errors.

    Recognizes a ``status_code``/``status`` attribute (Anthropic/OpenAI SDK errors) or
    common transient exception class names. Everything else is treated as a hard error
    that records an ``errored`` run immediately (no retry).
    """
    code = getattr(exc, "status_code", None) or getattr(exc, "status", None)
    if isinstance(code, int) and code in _TRANSIENT_STATUS:
        return True
    name = type(exc).__name__.lower()
    return any(tok in name for tok in ("ratelimit", "timeout", "apiconnection", "internalserver"))


@dataclass(frozen=True)
class RetryPolicy:
    max_attempts: int = 4
    base_delay: float = 0.5  # seconds
    max_delay: float = 30.0
    jitter: float = 0.1

    def delay_for(self, attempt: int) -> float:
        """Exponential backoff with jitter for the given 1-based attempt number."""
        raw = min(self.base_delay * (2 ** (attempt - 1)), self.max_delay)
        return raw + random.uniform(0, self.jitter)


# ---------------------------------------------------------------------------
# The conversation loop (system-agnostic; harness owns the trace)
# ---------------------------------------------------------------------------

# A hard ceiling on loop iterations (tool turns + question turns) guarding against a
# non-terminating policy; far above any legitimate run (60 user-facing turns).
_MAX_ITERATIONS = 1000


def _drain_trace_events(system: Any, trace: TraceWriter | None) -> None:
    """Append any echo-lifecycle events the system surfaces this turn (forward-compat).

    A system may expose ``drain_trace_events() -> list[event]`` to emit
    ``value_introduced`` / ``echo_issued`` / ``user_confirmed`` / ``user_corrected``
    into the canonical trace without the runner understanding echo semantics (R-10).
    Systems without the hook simply contribute no extra events.
    """
    drain = getattr(system, "drain_trace_events", None)
    if trace is None or not callable(drain):
        return
    for ev in drain() or []:
        trace.append(ev)


def run_conversation(
    system: Any,
    simulator: Any,
    *,
    reducer: StateReducer,
    trace: TraceWriter | None = None,
    profile_id: str,
    initial_state: ProfileState | None = None,
    max_turns: int = 60,
) -> tuple[ProfileState, str]:
    """Drive one system through one profile. Returns ``(final_state, end_reason)``.

    ``end_reason`` is one of ``"completed"`` / ``"incomplete_turn_cap"`` / ``"errored"``
    (the ``SessionEnd`` vocabulary). The runner increments ``turn_count`` once per
    user-facing turn; the §8 invariant-7 cap is enforced both by the policy and here.
    """
    state = initial_state or ProfileState(profile_id=profile_id)
    history: list[dict[str, Any]] = []
    end_reason = "completed"

    for _ in range(_MAX_ITERATIONS):
        if state.turn_count >= max_turns:
            end_reason = "incomplete_turn_cap"
            break

        action = system.next_action(state, history)
        _drain_trace_events(system, trace)

        if isinstance(action, EndConversation):
            end_reason = action.reason
            break

        if isinstance(action, UserQuestion):
            if trace is not None:
                trace.append(
                    UserFacingQuestion(
                        turn=state.turn_count, slot=action.primary_slot, text=action.text
                    )
                )
            reply = simulator.reply(action)
            history.append({"role": "assistant", "content": action.text})
            history.append({"role": "user", "content": reply})
            state = state.model_copy(update={"turn_count": state.turn_count + 1})
            continue

        if isinstance(action, list):  # list[ToolCall]
            for tc in action:
                if trace is not None:
                    trace.append(
                        ToolCallEvent(
                            turn=state.turn_count,
                            tool=tc.tool,
                            args=tc.model_dump(exclude={"tool"}),
                        )
                    )
                state = reducer.apply(state, tc)
            continue

        # Unknown action type — treat as a policy error.
        end_reason = "errored"
        break
    else:
        end_reason = "errored"  # iteration ceiling hit

    if trace is not None:
        valid = {"completed", "incomplete_turn_cap", "errored"}
        trace.append(
            SessionEnd(turn=state.turn_count, reason=end_reason if end_reason in valid else "errored")  # type: ignore[arg-type]
        )
    return state, end_reason


# ---------------------------------------------------------------------------
# Per-run context + run function contract
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class RunContext:
    """Everything a single run needs. A run is a pure function of this (D-4)."""

    manifest_hash: str
    profile_id: str
    system_id: str
    run_index: int
    seed: int | None
    campaign_dir: Path
    tag: str = "scored"

    @property
    def key(self) -> str:
        return RunRecord.make_key(self.profile_id, self.system_id, self.run_index)

    @property
    def record_path(self) -> Path:
        return self.campaign_dir / "runs" / f"{self.key}.json"

    @property
    def trace_path(self) -> Path:
        return self.campaign_dir / "runs" / f"{self.key}.trace.jsonl"


# A run function maps a RunContext to a RunRecord. It may be async. Transient errors
# should be raised (so the runner can retry); exhausted retries / hard errors become
# an ``errored`` RunRecord. Inject a fake in tests; the default wires agent/tree + sim.
RunFn = Callable[[RunContext], Awaitable[RunRecord]]


@dataclass
class CampaignResult:
    """Summary of a campaign invocation (this invocation only, not cumulative)."""

    manifest_hash: str
    campaign_dir: Path
    completed: int = 0
    incomplete: int = 0
    errored: int = 0
    skipped: int = 0  # already-present records (resume)
    records: list[RunRecord] = field(default_factory=list)

    def tally(self, record: RunRecord) -> None:
        self.records.append(record)
        if record.status is RunStatus.COMPLETED:
            self.completed += 1
        elif record.status is RunStatus.INCOMPLETE:
            self.incomplete += 1
        else:
            self.errored += 1


# ---------------------------------------------------------------------------
# run_campaign — idempotent, resumable orchestration
# ---------------------------------------------------------------------------


async def _run_with_retry(
    ctx: RunContext, run_fn: RunFn, policy: RetryPolicy
) -> RunRecord:
    """Run one key with backoff retry on transient errors; exhaustion → errored record."""
    last_exc: BaseException | None = None
    for attempt in range(1, policy.max_attempts + 1):
        try:
            return await run_fn(ctx)
        except BaseException as exc:  # noqa: BLE001 — classify, then retry or record
            last_exc = exc
            if is_transient(exc) and attempt < policy.max_attempts:
                await asyncio.sleep(policy.delay_for(attempt))
                continue
            # Hard error, or transient retries exhausted → errored RunRecord.
            return RunRecord(
                manifest_hash=ctx.manifest_hash,
                profile_id=ctx.profile_id,
                system_id=ctx.system_id,
                run_index=ctx.run_index,
                status=RunStatus.ERRORED,
                end_reason="errored",
                seed=ctx.seed,
                tag=ctx.tag,
                error=f"{type(exc).__name__}: {exc}",
            )
    # Unreachable, but keep the type-checker happy.
    raise CampaignError(str(last_exc))  # pragma: no cover


async def run_campaign(
    manifest: FreezeManifest | None,
    systems: list[str],
    profiles: list[str],
    *,
    run_fn: RunFn,
    k: int = 5,
    base_dir: str | Path = "campaigns",
    frozen: bool = True,
    seed_base: int = 42,
    tag: str = "scored",
    max_concurrency: int = 4,
    retry_policy: RetryPolicy | None = None,
) -> CampaignResult:
    """Run ``k`` runs of every (profile × system) under one frozen manifest.

    Idempotent + resumable: each key ``(manifest_hash, profile_id, system_id,
    run_index)`` writes exactly one ``RunRecord``; an already-present record is skipped
    (resume runs only the missing keys). ``run_fn`` is injected so the orchestration is
    testable without live LLM calls.

    Freeze discipline:
      * ``frozen=True`` requires a manifest that ``validate()``s clean — else abort.
      * the re-freeze cap (FR-26) is enforced before any run.
      * the campaign is written to ``base_dir/<manifest_hash>/runs/`` and every prior
        campaign directory is retained (FR-25 / H4).
    """
    if frozen:
        if manifest is None:
            raise CampaignError(
                "refusing to run in --frozen mode without a freeze manifest (D-5 / §5.2)."
            )
        FreezeManifest.check_refreeze_cap(manifest.refreeze_count, manifest.pm_override)
        mismatches = manifest.validate()
        if mismatches:
            raise CampaignError(
                "frozen-input hash mismatch — a re-freeze is required before running. "
                f"Changed inputs: {sorted(mismatches)} (EC-25)."
            )

    if manifest is None:
        raise CampaignError("a manifest is required to scope the campaign directory.")

    policy = retry_policy or RetryPolicy()
    campaign_dir = Path(base_dir) / manifest.manifest_hash
    (campaign_dir / "runs").mkdir(parents=True, exist_ok=True)
    # Stamp the manifest into its own campaign directory once (audit trail).
    manifest_copy = campaign_dir / "manifest.json"
    if not manifest_copy.exists():
        manifest.save(manifest_copy)

    result = CampaignResult(manifest_hash=manifest.manifest_hash, campaign_dir=campaign_dir)
    semaphore = asyncio.Semaphore(max_concurrency)

    async def _execute(ctx: RunContext) -> None:
        # Idempotency / resume: a written record is never recomputed.
        if ctx.record_path.exists():
            result.skipped += 1
            result.tally(RunRecord.load(ctx.record_path))
            return
        async with semaphore:
            record = await _run_with_retry(ctx, run_fn, policy)
        record.write(ctx.record_path)  # write-once
        result.tally(record)

    tasks: list[Awaitable[None]] = []
    for profile_id in profiles:
        for system_id in systems:
            for run_index in range(k):
                ctx = RunContext(
                    manifest_hash=manifest.manifest_hash,
                    profile_id=profile_id,
                    system_id=system_id,
                    run_index=run_index,
                    seed=seed_base + run_index,
                    campaign_dir=campaign_dir,
                    tag=tag,
                )
                tasks.append(_execute(ctx))

    await asyncio.gather(*tasks)
    return result
