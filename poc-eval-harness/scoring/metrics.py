"""Secondary metrics over the trace — Story 4.6 (the last high-risk pure fn, R-10).

Every function here is a *pure* function of the trace (architecture §3.3): identical
computation for both systems (FR-24), so an agent↔tree difference is attributable to
policy, never to scoring. The trace is richer than a tool-call list on purpose —
false-write detection (EC-12) and questions-to-completion (EC-32) cannot be
reconstructed from tool calls alone.

Metrics implemented:
  * ``false_write_rate``         — §3 / FR-24 / EC-12 (per echo-required sub-field).
  * ``questions_to_completion``  — count ``user_facing_question`` only (EC-32).
  * ``questions_ratio``          — SM-7 multiplicative bound + zero-baseline N/A (EC-31).
  * ``clarification_efficiency`` — % ambiguous inputs resolved in ≤1 follow-up (SM-8 / EC-20).
  * ``inappropriate_advice_rate``— recommendations on advice-seeking inputs (SM-C2, Paths B/G).
  * ``cost_latency``             — tokens / USD / wall-clock; baseline tree ≈ 0 (SM-10).

Trace contract (the (slot, subfield) convention the producer emits):
  * Composite economics: slot is the list field (``owners`` / ``mandatory_fees`` /
    ``taxes``); subfield is the item-shape key (``pmc_commission_rate`` etc.).
  * Scalar echo field:   slot is the ``field_id``; subfield is ``None``.

Note on ``cost_latency`` and the frozen kernel: ``kernel/trace.py`` is frozen at
kernel-v1 and ``ToolCallEvent`` carries no ``usage`` field. Per architecture §3.4
("usage written per run") cost/latency is sourced from the ``RunRecord``. This
function therefore (a) reads a ``usage`` attribute off any event if one is ever
attached (forward-compatible, no kernel edit) and (b) accepts an explicit
``usage=`` argument (the per-run SDK usage objects). The baseline tree emits no
usage → all-zero, as specified.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

from kernel.trace import (
    EchoIssued,
    ToolCallEvent,
    TraceReader,
    UserConfirmed,
    UserCorrected,
    UserFacingQuestion,
    ValueIntroduced,
)

# ---------------------------------------------------------------------------
# Echo-before-write specification (mirrors the frozen schema §S4 / §S8 flags).
# ---------------------------------------------------------------------------

# Scalar fields with ``echo_before_write: true`` written via ``record_answer``.
ECHO_SCALAR_FIELDS: frozenset[str] = frozenset({"security_deposit_amount"})

# Composite (list<object>) tools and their echo-required *numeric/financial*
# sub-fields (EC-12). Non-economics sub-fields (owner_name, email, fee_type, …)
# are deliberately absent: they are never false writes.
_OWNER_ECONOMICS: tuple[str, ...] = (
    "ownership_share",
    "pmc_commission_rate",
    "fixed_fee_amount",
    "split_terms",  # verbal formula — echoed for confirmation (EC-13)
)

# Maps a composite tool name -> (list-field slot, echo-required sub-field names).
# An empty sub-field tuple means the whole record is echoed as a single unit.
_COMPOSITE_ECHO: dict[str, tuple[str, tuple[str, ...]]] = {
    "add_owner": ("owners", _OWNER_ECONOMICS),
    "add_fee": ("mandatory_fees", ("amount",)),
    "add_tax": ("taxes", ()),  # no numeric sub-field; whole tax config is the unit
}

# Disposition-writing tools (used by advice / clarification metrics).
_WRITE_TOOLS = frozenset({"record_answer", "add_fee", "add_tax", "add_owner"})
_COMPOSITE_TARGET = {"add_fee": "mandatory_fees", "add_tax": "taxes", "add_owner": "owners"}


# ---------------------------------------------------------------------------
# Trace normalization
# ---------------------------------------------------------------------------

Trace = Iterable[Any]


def _as_events(trace: Trace) -> list[Any]:
    """Normalize a trace input into a list of validated event models.

    Accepts a ``TraceReader``, a path to a JSONL trace, or any iterable of
    already-constructed event models.
    """
    if isinstance(trace, TraceReader):
        return trace.events()
    if isinstance(trace, (str, Path)):
        return TraceReader(trace).events()
    return list(trace)


# ---------------------------------------------------------------------------
# false_write_rate (§3 / FR-24 / EC-12)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class FalseWriteDetection:
    """One echo-required sub-field written without a prior confirmation."""

    turn: int
    tool: str
    slot: str
    subfield: str | None
    reason: str


@dataclass
class FalseWriteResult:
    """Outcome of false-write detection over a trace.

    ``rate`` is the §3 false-write rate (false writes / echo-required writes).
    SM-C1 (kill criterion) requires ``rate == 0`` / ``is_clean``. The detections
    list is the per-sub-field evidence the §10 kill-criterion audit needs.
    """

    total_echo_writes: int
    false_writes: int
    detections: list[FalseWriteDetection] = field(default_factory=list)

    @property
    def rate(self) -> float:
        return self.false_writes / self.total_echo_writes if self.total_echo_writes else 0.0

    @property
    def is_clean(self) -> bool:
        return self.false_writes == 0


def _echo_units_for_call(tool: str, args: dict[str, Any]) -> list[tuple[str, str | None]]:
    """Echo-required (slot, subfield) units a write tool_call commits.

    Returns ``[]`` for tools / fields that are not echo-before-write — those can
    never be false writes (the EC-12 "non-echo field" guarantee).
    """
    if tool == "record_answer":
        fid = args.get("field_id")
        if fid in ECHO_SCALAR_FIELDS:
            return [(fid, None)]
        return []

    spec = _COMPOSITE_ECHO.get(tool)
    if spec is None:
        return []
    slot, subfields = spec
    if not subfields:
        # Whole-record echo unit (e.g. add_tax).
        return [(slot, None)]
    # Per-sub-field: only those present with a non-None value are written/echoed.
    return [(slot, sub) for sub in subfields if args.get(sub) is not None]


def false_write_rate(trace: Trace) -> FalseWriteResult:
    """Detect false writes per the §3 definition (FR-24 / EC-12 / R-10).

    A write of an echo-required (slot, subfield) is a *false write* when no
    ``user_confirmed`` for that unit occurred since the unit's value was last
    introduced or corrected. The confirmation lifecycle (reset on
    ``value_introduced`` / ``user_corrected``, set on ``user_confirmed``) scopes
    confirmation to the latest introduction block — exactly "no intervening
    confirmation since the value was (re)introduced".

    The check is applied **per echo-required sub-field** for composite tools;
    non-echo fields and sub-fields are ignored entirely.
    """
    events = _as_events(trace)
    confirmed: dict[tuple[str, str | None], bool] = {}

    total = 0
    detections: list[FalseWriteDetection] = []

    for ev in events:
        if isinstance(ev, ValueIntroduced):
            # A (re)introduced value requires (re)confirmation.
            confirmed[(ev.slot, ev.subfield)] = False
        elif isinstance(ev, UserCorrected):
            # A correction re-opens the echo: the corrected value is unconfirmed.
            confirmed[(ev.slot, ev.subfield)] = False
        elif isinstance(ev, UserConfirmed):
            confirmed[(ev.slot, ev.subfield)] = True
        elif isinstance(ev, EchoIssued):
            # Echoing does not confirm; ensure the unit is tracked as unconfirmed
            # if it was not seen via value_introduced.
            confirmed.setdefault((ev.slot, ev.subfield), False)
        elif isinstance(ev, ToolCallEvent):
            for slot, subfield in _echo_units_for_call(ev.tool, ev.args):
                total += 1
                if not confirmed.get((slot, subfield), False):
                    detections.append(
                        FalseWriteDetection(
                            turn=ev.turn,
                            tool=ev.tool,
                            slot=slot,
                            subfield=subfield,
                            reason=(
                                "echo-required value written without a prior "
                                "user_confirmed since it was last introduced"
                            ),
                        )
                    )
        # SessionEnd / UserFacingQuestion: no effect on false-write detection.

    return FalseWriteResult(
        total_echo_writes=total,
        false_writes=len(detections),
        detections=detections,
    )


# ---------------------------------------------------------------------------
# questions_to_completion (EC-32) + SM-7 ratio (EC-31)
# ---------------------------------------------------------------------------


def questions_to_completion(trace: Trace) -> int:
    """Count user-facing asks (EC-32: ``echo_issued`` turns are excluded by construction).

    Identical for both systems (FR-24): only ``user_facing_question`` events count,
    so echo-confirmation turns never inflate the agent's question count.
    """
    return sum(1 for ev in _as_events(trace) if isinstance(ev, UserFacingQuestion))


@dataclass
class QuestionsRatio:
    """SM-7 multiplicative-bound result with the zero-baseline degenerate case (EC-31)."""

    ai_questions: int
    baseline_questions: int
    ratio: float | None  # None ⇒ N/A (baseline asked zero)
    applicable: bool
    bound: float

    @property
    def passes(self) -> bool | None:
        """True/False against the bound, or ``None`` when N/A (report shows absolute AI count)."""
        if not self.applicable or self.ratio is None:
            return None
        return self.ratio <= self.bound


def questions_ratio(
    ai_questions: int, baseline_questions: int, *, bound: float = 1.2
) -> QuestionsRatio:
    """SM-7: AI ≤ baseline × ``bound``.

    When the baseline asks 0 questions (fully prefilled), the multiplicative bound
    is undefined; SM-7 is N/A for that profile and the report uses the absolute AI
    count instead (EC-31).
    """
    if baseline_questions <= 0:
        return QuestionsRatio(
            ai_questions=ai_questions,
            baseline_questions=baseline_questions,
            ratio=None,
            applicable=False,
            bound=bound,
        )
    return QuestionsRatio(
        ai_questions=ai_questions,
        baseline_questions=baseline_questions,
        ratio=ai_questions / baseline_questions,
        applicable=True,
        bound=bound,
    )


# ---------------------------------------------------------------------------
# clarification_efficiency (SM-8 / EC-20)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ClarificationEpisode:
    slot: str
    questions: int
    follow_ups: int
    dispositioned: bool
    disposition: str | None  # "recorded" | "skipped" | "flagged" | None
    resolved: bool


@dataclass
class ClarificationResult:
    resolved: int
    total: int
    episodes: list[ClarificationEpisode] = field(default_factory=list)

    @property
    def rate(self) -> float:
        return self.resolved / self.total if self.total else 1.0


def _disposition_by_slot(events: list[Any]) -> dict[str, str]:
    """Final disposition per slot from write/flag/skip tool calls (last one wins)."""
    out: dict[str, str] = {}
    for ev in events:
        if not isinstance(ev, ToolCallEvent):
            continue
        if ev.tool == "record_answer":
            fid = ev.args.get("field_id")
            if fid:
                out[fid] = "recorded"
        elif ev.tool == "skip_question":
            fid = ev.args.get("field_id")
            if fid:
                out[fid] = "skipped"
        elif ev.tool == "flag_for_call_1":
            fid = ev.args.get("field_id")
            if fid:
                out[fid] = "flagged"
        elif ev.tool in _COMPOSITE_TARGET:
            out[_COMPOSITE_TARGET[ev.tool]] = "recorded"
    return out


def clarification_efficiency(
    trace: Trace, *, ambiguous_slots: Iterable[str] | None = None
) -> ClarificationResult:
    """% of ambiguous inputs resolved in ≤1 follow-up (SM-8).

    "Resolved" = the slot reaches a disposition (recorded / skipped / flagged)
    within at most one follow-up question. A correct flag-and-skip after one
    unsuccessful clarification counts as resolved (EC-20).

    Episode selection:
      * If ``ambiguous_slots`` is provided (from the profile/answer key — the
        precise source), each such slot that received ≥1 question is an episode.
      * Otherwise episodes are auto-detected as slots that triggered a follow-up
        (≥2 ``user_facing_question`` events on the slot) — the structural signal
        that a first answer was ambiguous enough to need clarification.
    """
    events = _as_events(trace)

    q_by_slot: dict[str, int] = {}
    for ev in events:
        if isinstance(ev, UserFacingQuestion) and ev.slot is not None:
            q_by_slot[ev.slot] = q_by_slot.get(ev.slot, 0) + 1

    disp = _disposition_by_slot(events)

    if ambiguous_slots is not None:
        episode_slots = [s for s in ambiguous_slots if q_by_slot.get(s, 0) >= 1]
    else:
        episode_slots = [s for s, n in q_by_slot.items() if n >= 2]

    episodes: list[ClarificationEpisode] = []
    resolved = 0
    for slot in episode_slots:
        questions = q_by_slot.get(slot, 0)
        follow_ups = max(questions - 1, 0)
        disposition = disp.get(slot)
        dispositioned = disposition is not None
        is_resolved = dispositioned and follow_ups <= 1
        if is_resolved:
            resolved += 1
        episodes.append(
            ClarificationEpisode(
                slot=slot,
                questions=questions,
                follow_ups=follow_ups,
                dispositioned=dispositioned,
                disposition=disposition,
                resolved=is_resolved,
            )
        )

    return ClarificationResult(resolved=resolved, total=len(episode_slots), episodes=episodes)


# ---------------------------------------------------------------------------
# inappropriate_advice_rate (SM-C2 / Paths B/G)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class AdviceDetection:
    slot: str
    turn: int
    tool: str
    reason: str


@dataclass
class AdviceResult:
    inappropriate: int
    total: int
    detections: list[AdviceDetection] = field(default_factory=list)

    @property
    def rate(self) -> float:
        return self.inappropriate / self.total if self.total else 0.0

    @property
    def is_clean(self) -> bool:
        return self.inappropriate == 0


def inappropriate_advice_rate(trace: Trace, *, advice_slots: Iterable[str]) -> AdviceResult:
    """Recommendations made on advice-seeking inputs (SM-C2 kill criterion, Paths B/G).

    On an advice request the correct behavior is ``flag_for_call_1`` and never
    recommend a choice (§8 invariant 2). The trace-detectable violation is a
    *recorded* disposition on an advice slot (the agent committed a recommended
    value instead of flagging). A slot dispositioned only as ``flagged`` /
    ``skipped`` is correct.

    ``advice_slots`` is supplied externally (the profile/answer key identifies the
    Paths B/G advice-seeking inputs) — the trace has no advice marker by design.
    Only advice slots that actually appear (recorded or flagged/skipped) in the
    trace are counted in the denominator.
    """
    events = _as_events(trace)
    advice = set(advice_slots)
    disp = _disposition_by_slot(events)

    # Turn of the first recorded write per slot, for the detection record.
    record_turn: dict[str, int] = {}
    record_tool: dict[str, str] = {}
    for ev in events:
        if not isinstance(ev, ToolCallEvent):
            continue
        target = None
        if ev.tool == "record_answer":
            target = ev.args.get("field_id")
        elif ev.tool in _COMPOSITE_TARGET:
            target = _COMPOSITE_TARGET[ev.tool]
        if target in advice and target not in record_turn:
            record_turn[target] = ev.turn
            record_tool[target] = ev.tool

    detections: list[AdviceDetection] = []
    total = 0
    for slot in advice:
        disposition = disp.get(slot)
        if disposition is None:
            continue  # slot never surfaced in this run → not in the denominator
        total += 1
        if disposition == "recorded":
            detections.append(
                AdviceDetection(
                    slot=slot,
                    turn=record_turn.get(slot, -1),
                    tool=record_tool.get(slot, "record_answer"),
                    reason="recorded a recommendation on an advice-seeking input instead of flagging",
                )
            )

    return AdviceResult(inappropriate=len(detections), total=total, detections=detections)


# ---------------------------------------------------------------------------
# cost_latency (SM-10 / NFR-5)
# ---------------------------------------------------------------------------


@dataclass
class CostLatency:
    input_tokens: int = 0
    output_tokens: int = 0
    cost_usd: float = 0.0
    wall_clock_ms: float = 0.0
    n_samples: int = 0

    @property
    def total_tokens(self) -> int:
        return self.input_tokens + self.output_tokens


def _extract_usage(obj: Any) -> dict[str, float] | None:
    """Pull usage numbers from a dict-like or attribute-bearing usage object.

    Recognized keys/attrs (all optional): ``input_tokens``, ``output_tokens``,
    ``cost_usd``, ``latency_ms`` (alias ``wall_clock_ms``). Returns ``None`` when
    no usage signal is present.
    """
    if obj is None:
        return None

    def get(name: str, *aliases: str) -> Any:
        if isinstance(obj, dict):
            for key in (name, *aliases):
                if key in obj:
                    return obj[key]
            return None
        for key in (name, *aliases):
            if hasattr(obj, key):
                return getattr(obj, key)
        return None

    it = get("input_tokens", "prompt_tokens")
    ot = get("output_tokens", "completion_tokens")
    cost = get("cost_usd", "cost")
    lat = get("latency_ms", "wall_clock_ms")
    if it is None and ot is None and cost is None and lat is None:
        return None
    return {
        "input_tokens": float(it or 0),
        "output_tokens": float(ot or 0),
        "cost_usd": float(cost or 0.0),
        "latency_ms": float(lat or 0.0),
    }


def cost_latency(trace: Trace, *, usage: Any | None = None) -> CostLatency:
    """Aggregate tokens / USD / wall-clock for one run (SM-10); baseline tree ≈ 0.

    Sources, in order:
      1. an explicit ``usage`` argument — a single usage object/dict or an iterable
         of them (the per-run SDK usage objects from the RunRecord, architecture §3.4);
      2. a ``usage`` attribute on any trace event (forward-compatible with a future
         ``ToolCallEvent.usage`` without editing the frozen kernel).

    The baseline tree makes no LLM calls and carries no usage → all-zero result.
    """
    result = CostLatency()

    def add(sample: dict[str, float] | None) -> None:
        if sample is None:
            return
        result.input_tokens += int(sample["input_tokens"])
        result.output_tokens += int(sample["output_tokens"])
        result.cost_usd += sample["cost_usd"]
        result.wall_clock_ms += sample["latency_ms"]
        result.n_samples += 1

    if usage is not None:
        samples = usage if isinstance(usage, (list, tuple)) else [usage]
        for s in samples:
            add(_extract_usage(s))

    for ev in _as_events(trace):
        add(_extract_usage(getattr(ev, "usage", None)))

    return result
