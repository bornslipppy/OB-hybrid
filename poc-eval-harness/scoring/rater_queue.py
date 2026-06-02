"""Free-text blind-rater protocol — Story 4.9 (FR-35 / §6.4 / SM-4 / SM-9).

Free-text slots (``pain``, ``split_terms``, verbal-ownership captures) cannot be
scored by string equality (sar.py flags them ``requires_human_rating=True``). This
module is the **async rating queue** (R-4: human-in-the-loop must not be an inline
blocker):

  1. ``build_tasks`` collects ``requires_human_rating`` slots from scored runs and emits
     **system-anonymized** rating tasks — the rater sees the slot value + rubric and an
     opaque ``task_id``, never which system produced it (blind protocol).
  2. ``write_queue`` writes ``rater_tasks.jsonl`` (what raters see) and a separate
     ``rater_index.jsonl`` (the internal task_id → system/profile/run/slot map, NOT
     shown to raters).
  3. ``read_ratings`` reads back ``rater_ratings.jsonl`` (≥2 raters per task).
  4. ``cohen_kappa`` / ``inter_rater_kappa`` compute agreement (SM-9 bar: κ ≥ 0.6).
  5. ``adjudicate`` resolves each task: consensus, or tie-breaker when raters disagree.
  6. ``adjudicated_scores`` maps adjudicated results back through the index to
     ``(system, profile, run, slot)`` for ``sar.score_profile(..., human_ratings=...)``.

The "captures the same fact" rubric (Story 4.9 AC): correct = captures the substance;
incorrect = missing, fabricated, or wrong substance.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Iterable

from scoring.sar import ProfileScore

DEFAULT_RUBRIC = (
    "Does this value capture the SAME FACT as the respondent stated? "
    "Score 1 (correct) if it captures the substance; score 0 (incorrect) if it is "
    "missing, fabricated, or captures the wrong substance. Judge substance, not wording."
)

TASKS_FILE = "rater_tasks.jsonl"
INDEX_FILE = "rater_index.jsonl"
RATINGS_FILE = "rater_ratings.jsonl"


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class RatingTask:
    """What a blind rater sees — NO system attribution."""

    task_id: str
    slot_id: str
    value: Any
    rubric: str = DEFAULT_RUBRIC


@dataclass(frozen=True)
class TaskIndexEntry:
    """Internal reverse map (never presented to raters)."""

    task_id: str
    system_id: str
    profile_id: str
    run_index: int
    slot_id: str


@dataclass(frozen=True)
class Rating:
    """One rater's judgement of one task."""

    task_id: str
    rater_id: str
    score: int  # 1 correct / 0 incorrect
    note: str = ""


@dataclass(frozen=True)
class Adjudication:
    """The resolved score for one task, with the audit trail attached."""

    task_id: str
    score: int | None  # None ⇒ unresolved (disagreement, no tie-breaker)
    method: str         # "single" | "consensus" | "tie_breaker" | "unresolved"
    rater_scores: dict[str, int] = field(default_factory=dict)


@dataclass(frozen=True)
class ScoredRun:
    """A scored (system, profile, run) — input to the rating queue."""

    system_id: str
    profile_id: str
    run_index: int
    profile_score: ProfileScore


def make_task_id(system_id: str, profile_id: str, run_index: int, slot_id: str) -> str:
    """Opaque, stable id. The system_id is folded into the hash but cannot be derived
    back from the digest — so the visible task list reveals no system attribution."""
    raw = f"{system_id}|{profile_id}|{run_index}|{slot_id}".encode("utf-8")
    return hashlib.sha1(raw).hexdigest()[:16]


# ---------------------------------------------------------------------------
# Build + write the queue
# ---------------------------------------------------------------------------


def build_tasks(
    scored_runs: Iterable[ScoredRun], *, rubric: str = DEFAULT_RUBRIC
) -> tuple[list[RatingTask], list[TaskIndexEntry]]:
    """Collect ``requires_human_rating`` slots into anonymized tasks + an internal index."""
    tasks: list[RatingTask] = []
    index: list[TaskIndexEntry] = []
    for run in scored_runs:
        for ss in run.profile_score.slot_scores:
            if not ss.requires_human_rating:
                continue
            tid = make_task_id(run.system_id, run.profile_id, run.run_index, ss.slot_id)
            tasks.append(RatingTask(task_id=tid, slot_id=ss.slot_id, value=ss.actual_value, rubric=rubric))
            index.append(
                TaskIndexEntry(
                    task_id=tid,
                    system_id=run.system_id,
                    profile_id=run.profile_id,
                    run_index=run.run_index,
                    slot_id=ss.slot_id,
                )
            )
    return tasks, index


def write_queue(
    campaign_dir: str | Path, tasks: list[RatingTask], index: list[TaskIndexEntry]
) -> tuple[Path, Path]:
    """Write the anonymized task file (for raters) and the internal index (for scoring)."""
    base = Path(campaign_dir)
    base.mkdir(parents=True, exist_ok=True)
    tasks_path = base / TASKS_FILE
    index_path = base / INDEX_FILE
    with tasks_path.open("w", encoding="utf-8") as fh:
        for t in tasks:
            fh.write(json.dumps(asdict(t), sort_keys=True) + "\n")
    with index_path.open("w", encoding="utf-8") as fh:
        for e in index:
            fh.write(json.dumps(asdict(e), sort_keys=True) + "\n")
    return tasks_path, index_path


def read_tasks(campaign_dir: str | Path) -> list[RatingTask]:
    path = Path(campaign_dir) / TASKS_FILE
    if not path.exists():
        return []
    return [RatingTask(**json.loads(line)) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def read_index(campaign_dir: str | Path) -> list[TaskIndexEntry]:
    path = Path(campaign_dir) / INDEX_FILE
    if not path.exists():
        return []
    return [TaskIndexEntry(**json.loads(line)) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def read_ratings(campaign_dir: str | Path) -> list[Rating]:
    """Read completed ratings from ``rater_ratings.jsonl`` (≥2 raters per task)."""
    path = Path(campaign_dir) / RATINGS_FILE
    if not path.exists():
        return []
    out: list[Rating] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        d = json.loads(line)
        out.append(Rating(task_id=d["task_id"], rater_id=str(d["rater_id"]),
                          score=int(d["score"]), note=d.get("note", "")))
    return out


# ---------------------------------------------------------------------------
# Cohen's kappa (explicit — no library default)
# ---------------------------------------------------------------------------


def cohen_kappa(labels_a: list[Any], labels_b: list[Any]) -> float:
    """Cohen's κ between two raters over paired labels (categorical; here 0/1).

    κ = (p_o − p_e) / (1 − p_e). When chance agreement p_e == 1 (a single category
    used by both raters), κ is conventionally 1.0 on perfect agreement else 0.0.
    """
    if len(labels_a) != len(labels_b):
        raise ValueError("paired label lists must be equal length")
    n = len(labels_a)
    if n == 0:
        return 1.0

    po = sum(1 for a, b in zip(labels_a, labels_b) if a == b) / n
    cats = set(labels_a) | set(labels_b)
    pe = 0.0
    for c in cats:
        pa = sum(1 for a in labels_a if a == c) / n
        pb = sum(1 for b in labels_b if b == c) / n
        pe += pa * pb

    if abs(1.0 - pe) < 1e-12:
        return 1.0 if po >= 1.0 - 1e-12 else 0.0
    return (po - pe) / (1.0 - pe)


def _ratings_by_rater(ratings: Iterable[Rating]) -> dict[str, dict[str, int]]:
    out: dict[str, dict[str, int]] = {}
    for r in ratings:
        out.setdefault(r.rater_id, {})[r.task_id] = r.score
    return out


@dataclass(frozen=True)
class KappaResult:
    kappa: float | None  # None when no pair shares ≥1 task
    rater_a: str | None
    rater_b: str | None
    n_shared: int


def inter_rater_kappa(ratings: Iterable[Rating]) -> KappaResult:
    """Cohen's κ across rated slots for the two primary raters (SM-9).

    Picks the rater pair with the most shared tasks (deterministic on rater id) and
    computes κ over those shared tasks. Reported in the comparison report against the
    κ ≥ 0.6 bar.
    """
    by_rater = _ratings_by_rater(ratings)
    raters = sorted(by_rater)
    best: KappaResult = KappaResult(None, None, None, 0)
    for i in range(len(raters)):
        for j in range(i + 1, len(raters)):
            a, b = raters[i], raters[j]
            shared = sorted(set(by_rater[a]) & set(by_rater[b]))
            if len(shared) > best.n_shared:
                la = [by_rater[a][t] for t in shared]
                lb = [by_rater[b][t] for t in shared]
                best = KappaResult(cohen_kappa(la, lb), a, b, len(shared))
    return best


# ---------------------------------------------------------------------------
# Adjudication + back-mapping to scores
# ---------------------------------------------------------------------------


def adjudicate(
    ratings: Iterable[Rating], *, tie_breaker_rater: str | None = None
) -> dict[str, Adjudication]:
    """Resolve each task to a single score with an audit trail.

    * one rater  → ``single``;
    * ≥2 raters agree → ``consensus``;
    * raters disagree → the ``tie_breaker_rater``'s score if present (``tie_breaker``),
      otherwise ``unresolved`` (score ``None``) so it is surfaced, never silently dropped.
    """
    by_task: dict[str, dict[str, int]] = {}
    for r in ratings:
        by_task.setdefault(r.task_id, {})[r.rater_id] = r.score

    out: dict[str, Adjudication] = {}
    for tid, rater_scores in by_task.items():
        primary = {rid: s for rid, s in rater_scores.items() if rid != tie_breaker_rater}
        distinct = set(primary.values())
        if len(primary) <= 1:
            score = next(iter(primary.values())) if primary else rater_scores.get(tie_breaker_rater)
            method = "single"
        elif len(distinct) == 1:
            score = distinct.pop()
            method = "consensus"
        elif tie_breaker_rater is not None and tie_breaker_rater in rater_scores:
            score = rater_scores[tie_breaker_rater]
            method = "tie_breaker"
        else:
            score = None
            method = "unresolved"
        out[tid] = Adjudication(task_id=tid, score=score, method=method, rater_scores=dict(rater_scores))
    return out


def adjudicated_scores(
    adjudications: dict[str, Adjudication], index: Iterable[TaskIndexEntry]
) -> dict[tuple[str, str, int], dict[str, int]]:
    """Map adjudicated scores back to ``(system, profile, run) → {slot: score}``.

    The per-run inner dict is exactly the ``human_ratings`` argument
    ``sar.score_profile`` consumes (unresolved tasks are omitted so the slot retains
    its provisional pending state rather than a fabricated score).
    """
    by_task = {e.task_id: e for e in index}
    out: dict[tuple[str, str, int], dict[str, int]] = {}
    for tid, adj in adjudications.items():
        if adj.score is None:
            continue
        entry = by_task.get(tid)
        if entry is None:
            continue
        key = (entry.system_id, entry.profile_id, entry.run_index)
        out.setdefault(key, {})[entry.slot_id] = adj.score
    return out
