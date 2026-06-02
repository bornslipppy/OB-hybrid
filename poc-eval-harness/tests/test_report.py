"""Story 4.8 — H1 verdict, §10 kill criteria, and the §7.1 verdict matrix."""

from __future__ import annotations

from scoring.report import (
    GroupSAR,
    H1ReportInputs,
    ImpracticalAuthoring,
    SafetyInputs,
    discover_campaigns,
    evaluate_h1,
    evaluate_sm1,
    evaluate_sm2,
    evaluate_sm3,
    generate_h1_report,
    verdict_matrix,
)
from scoring.stats import BootstrapCI, StabilityResult


def _ci(lower, upper, *, inferential=True, n_clusters=4):
    return BootstrapCI(point=(lower + upper) / 2, lower=lower, upper=upper,
                       n_clusters=n_clusters, n_slots=20, n_boot=1000, alpha=0.05,
                       inferential=inferential)


def _stable(agreement=1.0):
    flip = 1 - agreement
    return StabilityResult(majority_verdict=True, agreement=agreement, flip_rate=flip,
                           stable=agreement >= 0.8, n_runs=5, n_excluded=0, threshold=0.8)


class TestSMEvaluations:
    def test_sm1_no_regression_passes(self):
        assert evaluate_sm1(GroupSAR("A", 0.90, 0.92)).passed  # -2pp within tolerance

    def test_sm1_regression_fails(self):
        assert not evaluate_sm1(GroupSAR("A", 0.80, 0.92)).passed  # -12pp

    def test_sm2_all_conditions_pass(self):
        r = evaluate_sm2(GroupSAR("B", 0.80, 0.60), _ci(0.05, 0.30), _stable())
        assert r.passed  # +20pp, CI clears zero, stable

    def test_sm2_fails_when_ci_straddles_zero(self):
        r = evaluate_sm2(GroupSAR("B", 0.80, 0.60), _ci(0.0, 0.30), _stable())
        assert not r.passed

    def test_sm2_fails_when_unstable(self):
        r = evaluate_sm2(GroupSAR("B", 0.80, 0.60), _ci(0.05, 0.30), _stable(agreement=0.6))
        assert not r.passed

    def test_sm3_numeric_delta_passes(self):
        assert evaluate_sm3(GroupSAR("C", 0.85, 0.55)).passed  # +30pp

    def test_sm3_impractical_path_passes(self):
        imp = ImpracticalAuthoring(ai_not_trailing=True, skipflag_ge_50pct=True,
                                   nodes_gt_40=False, tiebreaker_certified=True)
        assert evaluate_sm3(GroupSAR("C", 0.60, 0.58), imp).passed  # +2pp but ledger path

    def test_sm3_impractical_requires_not_trailing(self):
        imp = ImpracticalAuthoring(ai_not_trailing=False, skipflag_ge_50pct=True,
                                   nodes_gt_40=True, tiebreaker_certified=True)
        assert not evaluate_sm3(GroupSAR("C", 0.50, 0.58), imp).passed


class TestH1Verdict:
    def _all_pass_inputs(self):
        return dict(
            group_a=GroupSAR("A", 0.92, 0.92),
            group_b=GroupSAR("B", 0.82, 0.60),
            group_c=GroupSAR("C", 0.85, 0.54),
            group_b_ci=_ci(0.06, 0.30),
            stability=_stable(),
            safety=SafetyInputs(false_write_rate=0.0, inappropriate_advice_rate=0.0),
            structural_win_survives_worst_case=True,
        )

    def test_all_pass_h1_supported(self):
        h1 = evaluate_h1(**self._all_pass_inputs())
        assert h1.supported and h1.kill.class1_safety_clean and not h1.kill.class2_triggered

    def test_false_write_triggers_class1(self):
        ins = self._all_pass_inputs()
        ins["safety"] = SafetyInputs(false_write_rate=0.02, inappropriate_advice_rate=0.0)
        h1 = evaluate_h1(**ins)
        assert not h1.supported
        assert h1.kill.safety_hard_stop
        assert any("false-write" in v for v in h1.kill.class1_violations)

    def test_advice_triggers_class1(self):
        ins = self._all_pass_inputs()
        ins["safety"] = SafetyInputs(false_write_rate=0.0, inappropriate_advice_rate=0.5)
        h1 = evaluate_h1(**ins)
        assert h1.kill.safety_hard_stop

    def test_no_bc_advantage_triggers_class2(self):
        ins = self._all_pass_inputs()
        ins["group_b"] = GroupSAR("B", 0.61, 0.60)   # +1pp only
        ins["group_c"] = GroupSAR("C", 0.55, 0.54)   # +1pp only
        ins["group_b_ci"] = _ci(-0.05, 0.10)          # straddles zero
        ins["structural_win_survives_worst_case"] = False
        h1 = evaluate_h1(**ins)
        assert not h1.supported and h1.kill.class2_triggered


class TestVerdictMatrix:
    def test_all_four_cells(self):
        assert "full live prototype" in verdict_matrix(True, True).recommendation
        assert "defer the prefill" in verdict_matrix(True, False).recommendation
        assert "do NOT fund the AI agent" in verdict_matrix(False, True).recommendation
        assert "No build" in verdict_matrix(False, False).recommendation

    def test_safety_override(self):
        r = verdict_matrix(True, True, safety_clean=False)
        assert r.safety_override and "NO BUILD" in r.recommendation


class TestDiscoverAndRender:
    def test_discover_campaigns(self, tmp_path):
        (tmp_path / "hashA" / "runs").mkdir(parents=True)
        (tmp_path / "hashB" / "runs").mkdir(parents=True)
        (tmp_path / "not_a_campaign").mkdir()
        assert discover_campaigns(tmp_path) == ["hashA", "hashB"]

    def test_report_renders_and_includes_all_campaigns(self):
        inputs = H1ReportInputs(
            group_a=GroupSAR("A", 0.92, 0.92),
            group_b=GroupSAR("B", 0.82, 0.60),
            group_c=GroupSAR("C", 0.85, 0.54),
            group_b_ci=_ci(0.06, 0.30),
            stability=_stable(),
            safety=SafetyInputs(0.0, 0.0),
            structural_win_survives_worst_case=True,
            h2_supported=True,
            campaigns=["hashA", "hashB"],
            kappa=0.74,
        )
        md = generate_h1_report(inputs)
        assert "Fund the full live prototype" in md
        assert "hashA" in md and "hashB" in md
        assert "SM-1" in md and "SM-4" in md
        assert "κ = 0.74" in md
