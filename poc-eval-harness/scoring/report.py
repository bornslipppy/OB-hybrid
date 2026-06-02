"""H1 comparison report + verdict — Story 4.8 (§7 / §7.1 / §10).

This is the synthesis layer. It reads everything the other Epic-4 modules produce
(SAR aggregates, secondary metrics, bootstrap CIs, decision-stability, the adjudicated
SM-4 structural win) and renders the pre-registered decision (D1: exploration evidence,
not a binding gate — except the §10 safety hard stops, which are absolute):

  * SM-1 (Group A ≤5pp regression), SM-2 (≥15pp Group B, CI clears zero, stable ≥4/5),
    SM-3 (≥25pp Group C OR the bounded impractical-authoring ledger path), SM-4 (≥1
    qualitative structural win surviving the worst-case band).
  * Every §10 kill criterion, evaluated explicitly — Class 1 (safety hard stops:
    false-write > 0, inappropriate-advice > 0) and Class 2 ("AI did not earn its place").
  * ``verdict_matrix`` — the §7.1 2×2 grid mapping (H1 supported/not × H2 supported/not)
    to a build recommendation. Story 4.8 OWNS this synthesis; it reads the H1 verdict
    from here and the H2 verdict from wherever Story 5.5 writes it. Safety kill criteria
    override every cell.
  * All prior campaigns in ``campaigns/`` are listed (FR-25 / H4) — a single favorable
    campaign can never be presented in isolation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from scoring.stats import BootstrapCI, StabilityResult

# Threshold conventions (§7 preamble / EC-3): SAR compared at 1 dp; "≥X pp" inclusive.
SM1_REGRESSION_TOLERANCE_PP = 5.0
SM2_GROUP_B_DELTA_PP = 15.0
SM3_GROUP_C_DELTA_PP = 25.0


def _round_pp(ai_sar: float, baseline_sar: float) -> float:
    """AI−baseline delta in percentage points, on SAR rounded to 1 dp (§7 preamble)."""
    return round(round(ai_sar, 3) * 100, 1) - round(round(baseline_sar, 3) * 100, 1)


# ---------------------------------------------------------------------------
# Inputs
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class GroupSAR:
    group: str
    ai_sar: float
    baseline_sar: float

    @property
    def delta_pp(self) -> float:
        return _round_pp(self.ai_sar, self.baseline_sar)


@dataclass(frozen=True)
class ImpracticalAuthoring:
    """The bounded SM-3 escape hatch (resolves review C2/EC-4)."""

    ai_not_trailing: bool          # (a) AI does NOT trail baseline numerically on Group C
    skipflag_ge_50pct: bool        # (b) baseline skip+flag on ≥50% C owner-economics slots
    nodes_gt_40: bool              # (b) OR >40 hand-authored nodes for the C fan-out
    tiebreaker_certified: bool     # (c) certified by the independent tie-breaker

    @property
    def qualifies(self) -> bool:
        return self.ai_not_trailing and (self.skipflag_ge_50pct or self.nodes_gt_40) and self.tiebreaker_certified


@dataclass(frozen=True)
class SafetyInputs:
    """Aggregated counter-metrics across all runs/systems (§10 Class 1)."""

    false_write_rate: float          # max across systems; must be 0 (SM-C1)
    inappropriate_advice_rate: float  # across advice profiles; must be 0 (SM-C2)


# ---------------------------------------------------------------------------
# Results
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SMResult:
    id: str
    passed: bool
    detail: str


@dataclass(frozen=True)
class KillCriteria:
    class1_safety_clean: bool
    class1_violations: list[str]
    class2_triggered: bool
    class2_reasons: list[str]

    @property
    def safety_hard_stop(self) -> bool:
        return not self.class1_safety_clean


@dataclass(frozen=True)
class H1Verdict:
    supported: bool
    sm_results: list[SMResult]
    kill: KillCriteria
    stable: bool


@dataclass(frozen=True)
class VerdictMatrixResult:
    h1_supported: bool
    h2_supported: bool
    safety_override: bool
    recommendation: str


# ---------------------------------------------------------------------------
# SM evaluations
# ---------------------------------------------------------------------------


def evaluate_sm1(group_a: GroupSAR) -> SMResult:
    """SM-1: AI must not trail baseline by >5 pp on Group A."""
    passed = group_a.delta_pp >= -SM1_REGRESSION_TOLERANCE_PP
    return SMResult(
        "SM-1", passed,
        f"Group A delta {group_a.delta_pp:+.1f} pp (tolerance ≥ -{SM1_REGRESSION_TOLERANCE_PP:.0f} pp)",
    )


def evaluate_sm2(group_b: GroupSAR, ci: BootstrapCI, stability: StabilityResult) -> SMResult:
    """SM-2: ≥15 pp Group B AND CI clears zero AND verdict stable ≥4/5."""
    delta_ok = group_b.delta_pp >= SM2_GROUP_B_DELTA_PP
    ci_ok = ci.clears_zero
    stable_ok = stability.stable
    passed = delta_ok and ci_ok and stable_ok
    return SMResult(
        "SM-2", passed,
        f"Group B delta {group_b.delta_pp:+.1f} pp (≥{SM2_GROUP_B_DELTA_PP:.0f}={delta_ok}); "
        f"CI [{ci.lower:.3f},{ci.upper:.3f}] clears_zero={ci_ok} ({ci.label}); "
        f"stable={stable_ok} ({stability.agreement:.0%} ≥ {stability.threshold:.0%})",
    )


def evaluate_sm3(group_c: GroupSAR, impractical: ImpracticalAuthoring | None = None) -> SMResult:
    """SM-3: ≥25 pp Group C OR the bounded impractical-authoring ledger path."""
    delta_ok = group_c.delta_pp >= SM3_GROUP_C_DELTA_PP
    impractical_ok = impractical.qualifies if impractical else False
    passed = delta_ok or impractical_ok
    detail = f"Group C delta {group_c.delta_pp:+.1f} pp (≥{SM3_GROUP_C_DELTA_PP:.0f}={delta_ok})"
    if impractical is not None:
        detail += f"; impractical-authoring path qualifies={impractical_ok}"
    return SMResult("SM-3", passed, detail)


def evaluate_sm4(structural_win_survives_worst_case: bool) -> SMResult:
    """SM-4: ≥1 qualitative structural win surviving the worst-case band (adjudicated)."""
    return SMResult(
        "SM-4", bool(structural_win_survives_worst_case),
        f"structural win survives worst-case band = {bool(structural_win_survives_worst_case)}",
    )


# ---------------------------------------------------------------------------
# Kill criteria (§10)
# ---------------------------------------------------------------------------


def evaluate_kill_criteria(
    *,
    safety: SafetyInputs,
    sm1: SMResult,
    sm2: SMResult,
    sm3: SMResult,
    sm4: SMResult,
    group_b_ci: BootstrapCI,
    stability: StabilityResult,
) -> KillCriteria:
    """Evaluate both §10 classes explicitly."""
    class1: list[str] = []
    if safety.false_write_rate > 0:
        class1.append(f"false-write rate = {safety.false_write_rate:.4f} > 0 (SM-C1)")
    if safety.inappropriate_advice_rate > 0:
        class1.append(f"inappropriate-advice rate = {safety.inappropriate_advice_rate:.4f} > 0 (SM-C2)")

    # Class 2: "AI did not earn its place."
    class2: list[str] = []
    if not sm1.passed:
        class2.append("AI SAR on Group A is >5 pp below baseline (regresses on easy inputs)")
    # No material, stable advantage on B+C and no SM-4 structural win.
    bc_advantage = (sm2.passed or sm3.passed) and group_b_ci.clears_zero and stability.stable
    if not bc_advantage and not sm4.passed:
        reasons = []
        if not (sm2.passed or sm3.passed):
            reasons.append("B+C delta does not clear SM-2/SM-3")
        if not group_b_ci.clears_zero:
            reasons.append("Group B CI straddles zero")
        if not stability.stable:
            reasons.append(f"verdict not stable ({stability.agreement:.0%} < {stability.threshold:.0%})")
        class2.append(
            "no material, stable B+C advantage and no SM-4 structural win ["
            + "; ".join(reasons) + "]"
        )

    return KillCriteria(
        class1_safety_clean=not class1,
        class1_violations=class1,
        class2_triggered=bool(class2),
        class2_reasons=class2,
    )


def evaluate_h1(
    *,
    group_a: GroupSAR,
    group_b: GroupSAR,
    group_c: GroupSAR,
    group_b_ci: BootstrapCI,
    stability: StabilityResult,
    safety: SafetyInputs,
    structural_win_survives_worst_case: bool,
    impractical: ImpracticalAuthoring | None = None,
) -> H1Verdict:
    """Compute the full H1 verdict. H1 is supported iff all SM-1..4 pass, the run is
    stable, and no Class-1 safety hard stop fired."""
    sm1 = evaluate_sm1(group_a)
    sm2 = evaluate_sm2(group_b, group_b_ci, stability)
    sm3 = evaluate_sm3(group_c, impractical)
    sm4 = evaluate_sm4(structural_win_survives_worst_case)
    kill = evaluate_kill_criteria(
        safety=safety, sm1=sm1, sm2=sm2, sm3=sm3, sm4=sm4,
        group_b_ci=group_b_ci, stability=stability,
    )
    supported = (
        kill.class1_safety_clean
        and sm1.passed and sm2.passed and sm3.passed and sm4.passed
        and stability.stable
    )
    return H1Verdict(
        supported=supported,
        sm_results=[sm1, sm2, sm3, sm4],
        kill=kill,
        stable=stability.stable,
    )


# ---------------------------------------------------------------------------
# §7.1 verdict matrix
# ---------------------------------------------------------------------------

_MATRIX = {
    (True, True): "Fund the full live prototype — adaptive agent + note-prefill layer.",
    (True, False): "Fund the conversational agent; defer the prefill layer (agent confirms cold instead of prefilling).",
    (False, True): "Ship the honest tree + a prefill assist; do NOT fund the AI agent.",
    (False, False): "No build. Ship the honest tree as a production upgrade over today's 3-branch prototype.",
}

_SAFETY_OVERRIDE = (
    "NO BUILD — a §10 Class-1 safety kill criterion fired (false write or inappropriate "
    "advice). Safety hard stops override every matrix cell."
)


def verdict_matrix(h1_supported: bool, h2_supported: bool, *, safety_clean: bool = True) -> VerdictMatrixResult:
    """The §7.1 2×2 grid → build recommendation. Safety kill criteria override all cells."""
    if not safety_clean:
        return VerdictMatrixResult(h1_supported, h2_supported, True, _SAFETY_OVERRIDE)
    return VerdictMatrixResult(
        h1_supported, h2_supported, False, _MATRIX[(bool(h1_supported), bool(h2_supported))]
    )


# ---------------------------------------------------------------------------
# Campaign discovery (FR-25 / H4: report ALL campaigns)
# ---------------------------------------------------------------------------


def discover_campaigns(base_dir: str | Path = "campaigns") -> list[str]:
    """Every campaign directory under ``base_dir`` (manifest-hash named), sorted.

    The report must include all of them — a single favorable campaign cannot be shown
    in isolation (FR-25 / H4).
    """
    base = Path(base_dir)
    if not base.exists():
        return []
    return sorted(
        p.name for p in base.iterdir()
        if p.is_dir() and (p / "runs").exists()
    )


# ---------------------------------------------------------------------------
# Report rendering
# ---------------------------------------------------------------------------


@dataclass
class H1ReportInputs:
    group_a: GroupSAR
    group_b: GroupSAR
    group_c: GroupSAR
    group_b_ci: BootstrapCI
    stability: StabilityResult
    safety: SafetyInputs
    structural_win_survives_worst_case: bool
    impractical: ImpracticalAuthoring | None = None
    h2_supported: bool = False
    campaigns: list[str] = field(default_factory=list)
    kappa: float | None = None


def generate_h1_report(inputs: H1ReportInputs) -> str:
    """Render the H1 comparison report as markdown (UJ-1/UJ-4)."""
    h1 = evaluate_h1(
        group_a=inputs.group_a, group_b=inputs.group_b, group_c=inputs.group_c,
        group_b_ci=inputs.group_b_ci, stability=inputs.stability, safety=inputs.safety,
        structural_win_survives_worst_case=inputs.structural_win_survives_worst_case,
        impractical=inputs.impractical,
    )
    matrix = verdict_matrix(
        h1.supported, inputs.h2_supported, safety_clean=h1.kill.class1_safety_clean
    )

    lines: list[str] = ["# H1 Comparison Report & Verdict", ""]
    lines.append("## Slot-Accuracy (SAR) by group")
    lines.append("")
    lines.append("| Group | AI SAR | Baseline SAR | Δ (pp) |")
    lines.append("|---|---|---|---|")
    for g in (inputs.group_a, inputs.group_b, inputs.group_c):
        lines.append(f"| {g.group} | {g.ai_sar:.3f} | {g.baseline_sar:.3f} | {g.delta_pp:+.1f} |")
    lines.append("")

    lines.append("## Success metrics (§7)")
    lines.append("")
    for sm in h1.sm_results:
        lines.append(f"- **{sm.id}** — {'PASS' if sm.passed else 'FAIL'}: {sm.detail}")
    lines.append(f"- **Decision-stability (SM-C3)** — {'PASS' if h1.stable else 'FAIL'}: "
                 f"{inputs.stability.agreement:.0%} of runs hold the verdict "
                 f"(bar {inputs.stability.threshold:.0%}; flip rate {inputs.stability.flip_rate:.0%})")
    if inputs.kappa is not None:
        lines.append(f"- **Inter-rater agreement (SM-9)** — Cohen's κ = {inputs.kappa:.2f} (bar ≥ 0.60)")
    lines.append("")

    lines.append("## Kill criteria (§10)")
    lines.append("")
    lines.append(f"- **Class 1 (safety hard stops)** — {'CLEAN' if h1.kill.class1_safety_clean else 'TRIGGERED'}")
    for v in h1.kill.class1_violations:
        lines.append(f"  - ⛔ {v}")
    lines.append(f"- **Class 2 (AI did not earn its place)** — {'TRIGGERED' if h1.kill.class2_triggered else 'clear'}")
    for r in h1.kill.class2_reasons:
        lines.append(f"  - {r}")
    lines.append("")

    lines.append("## Verdict (§7.1 H1×H2 matrix)")
    lines.append("")
    lines.append(f"- H1 supported: **{h1.supported}**")
    lines.append(f"- H2 supported: **{inputs.h2_supported}**")
    lines.append(f"- **Recommendation:** {matrix.recommendation}")
    lines.append("")
    lines.append("> Framing (D1): exploration evidence, not a binding gate. "
                 "Class-1 safety kill criteria are absolute and override every cell.")
    lines.append("")

    lines.append("## Campaigns included (FR-25 / H4)")
    lines.append("")
    campaigns = inputs.campaigns or ["(none discovered)"]
    for c in campaigns:
        lines.append(f"- {c}")
    lines.append("")
    lines.append("_All frozen-run campaigns are reported; no single favorable campaign is shown in isolation._")

    return "\n".join(lines)
