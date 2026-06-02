"""Statistics honest to N=8 — Story 4.7 (FR-25 / §7).

Three concerns, each a pure NumPy function with the clustering and the
lower-bound>0 rule **implemented explicitly** so nothing hides in a library default
(architecture §1 tech-table rationale):

  * ``cluster_bootstrap_ci`` — slot-level bootstrap CI **clustered by profile**:
    resample profiles (clusters) with replacement, then slots within each. "CI clears
    zero" ⇒ lower bound **strictly > 0** (a lower bound of exactly 0 straddles — §7
    preamble / EC-3). H5 applicability: an interval is *inferential* only with ≥3
    clusters — Group B (n=4) and pooled B+C (n=6) qualify; Groups A and C (n=2 each)
    are descriptive-only and labeled "not inferential".
  * ``decision_stability`` — the §7 verdict must hold in ≥4/5 runs; reports the flip
    rate. S5 conditional flips caused by stochastic simulator phrasing are excludable
    (FR-4 / §6.4).
  * ``disposition_flip_flags`` — any slot whose recorded/flagged/skipped outcome
    changes across runs is a reliability red flag, with the same S5 exclusion (M4).
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from typing import Any, Sequence

import numpy as np

# Minimum clusters for an interval to be treated as inferential (H5).
MIN_CLUSTERS_FOR_INFERENCE = 3
# Decision-stability pass bar (§3 glossary / SM-C3): verdict holds in ≥4/5 runs.
STABILITY_THRESHOLD = 0.8


# ---------------------------------------------------------------------------
# cluster_bootstrap_ci
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class BootstrapCI:
    """A clustered bootstrap confidence interval on the mean of ``slot_scores``."""

    point: float
    lower: float
    upper: float
    n_clusters: int
    n_slots: int
    n_boot: int
    alpha: float
    inferential: bool  # H5: False ⇒ "not inferential" (descriptive-only, <3 clusters)

    @property
    def clears_zero(self) -> bool:
        """§7: the CI clears zero iff the lower bound is strictly > 0 (EC-3).

        Only meaningful for an inferential interval; a descriptive-only interval
        (Groups A/C) must not be used to assert a verdict.
        """
        return self.inferential and self.lower > 0.0

    @property
    def label(self) -> str:
        return "inferential" if self.inferential else "not inferential (descriptive-only, <3 clusters)"


def cluster_bootstrap_ci(
    slot_scores: Sequence[float],
    profile_ids: Sequence[Any],
    *,
    n_boot: int = 10_000,
    alpha: float = 0.05,
    seed: int | None = None,
    min_clusters_for_inference: int = MIN_CLUSTERS_FOR_INFERENCE,
) -> BootstrapCI:
    """Profile-clustered bootstrap CI on the mean of ``slot_scores`` (FR-25).

    The statistic is the mean (SAR for raw 0/1 scores, or the mean AI−baseline delta
    when ``slot_scores`` holds per-slot deltas — the "CI clears zero" verdict input).

    Resampling (explicit, two-stage cluster bootstrap):
      1. resample the set of profiles (clusters) with replacement;
      2. within each chosen cluster, resample its slots with replacement;
      3. the bootstrap statistic is the mean over the concatenated resample.

    The percentile interval uses ``[alpha/2, 1 - alpha/2]`` (default 95%). The RNG is
    explicitly seeded (``numpy.random.default_rng``) — no global/implicit state.
    """
    scores = np.asarray(slot_scores, dtype=float)
    pids = np.asarray(profile_ids)
    if scores.shape[0] != pids.shape[0]:
        raise ValueError("slot_scores and profile_ids must be the same length")

    n_slots = int(scores.shape[0])
    if n_slots == 0:
        return BootstrapCI(0.0, 0.0, 0.0, 0, 0, n_boot, alpha, inferential=False)

    clusters = list(dict.fromkeys(pids.tolist()))  # unique, order-preserving
    n_clusters = len(clusters)
    # Pre-index slot positions per cluster (object array of index vectors).
    cluster_indices = [np.flatnonzero(pids == c) for c in clusters]

    rng = np.random.default_rng(seed)
    point = float(scores.mean())

    boot_means = np.empty(n_boot, dtype=float)
    n_clusters_arr = np.arange(n_clusters)
    for b in range(n_boot):
        chosen = rng.choice(n_clusters_arr, size=n_clusters, replace=True)
        parts: list[np.ndarray] = []
        for ci in chosen:
            idx = cluster_indices[ci]
            resampled = rng.choice(idx, size=idx.shape[0], replace=True)
            parts.append(scores[resampled])
        boot_means[b] = np.concatenate(parts).mean()

    lower = float(np.percentile(boot_means, 100.0 * (alpha / 2.0)))
    upper = float(np.percentile(boot_means, 100.0 * (1.0 - alpha / 2.0)))

    return BootstrapCI(
        point=point,
        lower=lower,
        upper=upper,
        n_clusters=n_clusters,
        n_slots=n_slots,
        n_boot=n_boot,
        alpha=alpha,
        inferential=n_clusters >= min_clusters_for_inference,
    )


# ---------------------------------------------------------------------------
# decision_stability
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class StabilityResult:
    majority_verdict: bool | None  # None when no runs counted
    agreement: float               # fraction of counted runs matching the majority
    flip_rate: float               # 1 - agreement
    stable: bool                   # agreement >= threshold (≥4/5)
    n_runs: int                    # runs counted (after S5 exclusion)
    n_excluded: int                # runs dropped (S5 stochastic-signal flips)
    threshold: float


def decision_stability(
    per_run_verdicts: Sequence[bool],
    *,
    threshold: float = STABILITY_THRESHOLD,
    exclude_mask: Sequence[bool] | None = None,
) -> StabilityResult:
    """Verdict stability across the k runs (SM-C3): must hold in ≥``threshold`` of runs.

    ``per_run_verdicts`` is the §7 pass/fail verdict for each of the k runs. The flip
    rate is the fraction of counted runs that disagree with the majority verdict.

    ``exclude_mask`` (parallel, ``True`` = exclude) drops runs whose verdict flip is
    attributable to a stochastic simulator changing the realized S5 signal (FR-4 /
    §6.4) — those are not agent instability and must not count against stability.
    """
    verdicts = list(per_run_verdicts)
    if exclude_mask is not None:
        if len(exclude_mask) != len(verdicts):
            raise ValueError("exclude_mask must match per_run_verdicts length")
        counted = [v for v, ex in zip(verdicts, exclude_mask) if not ex]
        n_excluded = sum(1 for ex in exclude_mask if ex)
    else:
        counted = verdicts
        n_excluded = 0

    n = len(counted)
    if n == 0:
        return StabilityResult(None, 0.0, 0.0, False, 0, n_excluded, threshold)

    counts = Counter(bool(v) for v in counted)
    majority_verdict, majority_n = counts.most_common(1)[0]
    agreement = majority_n / n
    return StabilityResult(
        majority_verdict=majority_verdict,
        agreement=agreement,
        flip_rate=1.0 - agreement,
        stable=agreement >= threshold,
        n_runs=n,
        n_excluded=n_excluded,
        threshold=threshold,
    )


# ---------------------------------------------------------------------------
# disposition_flip_flags
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class DispositionFlip:
    slot: str
    dispositions: list[str]          # the distinct outcomes observed across runs
    counts: dict[str, int]           # outcome -> number of runs
    n_runs: int


@dataclass
class FlipResult:
    flagged: list[DispositionFlip] = field(default_factory=list)   # reliability red flags
    excluded: list[DispositionFlip] = field(default_factory=list)  # S5-conditional flips (FR-4)

    @property
    def has_red_flags(self) -> bool:
        return bool(self.flagged)


def disposition_flip_flags(
    runs: Sequence[dict[str, str]],
    *,
    s5_conditional_slots: Sequence[str] = (),
) -> FlipResult:
    """Flag any slot whose disposition changes across runs (FR-25 reliability red flag).

    ``runs`` is a per-run mapping ``{slot_id: disposition}`` (disposition ∈ recorded /
    flagged / skipped / unanswered…). A slot is *flagged* when it shows more than one
    distinct disposition across the runs in which it appears.

    Flips on ``s5_conditional_slots`` are routed to ``excluded`` rather than
    ``flagged``: an S5 slot scored on the realized transcript legitimately varies with
    the stochastic simulator signal and is not an agent defect (FR-4 / review M4).
    """
    s5 = set(s5_conditional_slots)

    seen: dict[str, list[str]] = {}
    for run in runs:
        for slot, disp in run.items():
            seen.setdefault(slot, []).append(disp)

    result = FlipResult()
    for slot, dispositions in seen.items():
        counts = Counter(dispositions)
        if len(counts) <= 1:
            continue  # stable across runs
        flip = DispositionFlip(
            slot=slot,
            dispositions=sorted(counts.keys()),
            counts=dict(counts),
            n_runs=len(dispositions),
        )
        if slot in s5:
            result.excluded.append(flip)
        else:
            result.flagged.append(flip)

    result.flagged.sort(key=lambda f: f.slot)
    result.excluded.sort(key=lambda f: f.slot)
    return result
