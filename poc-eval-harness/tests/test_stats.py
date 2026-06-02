"""Story 4.7 — statistics honest to N=8 (FR-25 / §7 / H5 / EC-3 / M4)."""

from __future__ import annotations

from scoring.stats import (
    cluster_bootstrap_ci,
    decision_stability,
    disposition_flip_flags,
)


class TestClusterBootstrapCI:
    def test_all_ones_ci_clears_zero(self):
        scores = [1.0] * 8
        pids = ["A1", "A1", "B1", "B1", "B2", "B2", "B3", "B4"]
        ci = cluster_bootstrap_ci(scores, pids, n_boot=500, seed=1)
        assert ci.point == 1.0 and ci.lower == 1.0 and ci.upper == 1.0
        assert ci.clears_zero is True

    def test_all_zeros_does_not_clear_zero(self):
        # Lower bound is exactly 0 → straddles → does NOT clear (EC-3).
        scores = [0.0] * 6
        pids = ["B1", "B1", "B2", "B2", "B3", "B4"]
        ci = cluster_bootstrap_ci(scores, pids, n_boot=500, seed=1)
        assert ci.lower == 0.0
        assert ci.clears_zero is False

    def test_strong_positive_delta_clears_zero(self):
        # Per-slot AI-baseline deltas, all clearly positive across 4 clusters.
        scores = [0.6, 0.7, 0.5, 0.8, 0.6, 0.9, 0.7, 0.6]
        pids = ["B1", "B1", "B2", "B2", "B3", "B3", "B4", "B4"]
        ci = cluster_bootstrap_ci(scores, pids, n_boot=2000, seed=7)
        assert ci.inferential is True
        assert ci.lower > 0.0 and ci.clears_zero is True

    def test_h5_two_clusters_not_inferential(self):
        # Group A / Group C: n=2 clusters → descriptive-only.
        scores = [1.0, 1.0, 1.0, 0.0]
        pids = ["A1", "A1", "A2", "A2"]
        ci = cluster_bootstrap_ci(scores, pids, n_boot=300, seed=2)
        assert ci.n_clusters == 2
        assert ci.inferential is False
        assert ci.clears_zero is False  # never clears when not inferential
        assert "not inferential" in ci.label

    def test_h5_four_clusters_inferential(self):
        scores = [1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0]
        pids = ["B1", "B1", "B2", "B2", "B3", "B3", "B4", "B4"]
        ci = cluster_bootstrap_ci(scores, pids, n_boot=300, seed=2)
        assert ci.n_clusters == 4 and ci.inferential is True

    def test_reproducible_with_seed(self):
        scores = [1.0, 0.0, 1.0, 1.0, 0.0, 1.0]
        pids = ["B1", "B1", "B2", "B2", "B3", "B3"]
        a = cluster_bootstrap_ci(scores, pids, n_boot=500, seed=42)
        b = cluster_bootstrap_ci(scores, pids, n_boot=500, seed=42)
        assert (a.lower, a.upper) == (b.lower, b.upper)

    def test_empty_input(self):
        ci = cluster_bootstrap_ci([], [], n_boot=10)
        assert ci.n_slots == 0 and ci.inferential is False


class TestDecisionStability:
    def test_five_of_five_stable(self):
        r = decision_stability([True] * 5)
        assert r.stable and r.flip_rate == 0.0 and r.majority_verdict is True

    def test_four_of_five_is_stable(self):
        r = decision_stability([True, True, True, True, False])
        assert r.stable is True
        assert abs(r.flip_rate - 0.2) < 1e-9

    def test_three_of_five_not_stable(self):
        r = decision_stability([True, True, True, False, False])
        assert r.stable is False
        assert abs(r.agreement - 0.6) < 1e-9

    def test_s5_excluded_run_dropped(self):
        # 5 runs, one flip excluded as S5-stochastic → 4/4 stable.
        r = decision_stability(
            [True, True, True, True, False],
            exclude_mask=[False, False, False, False, True],
        )
        assert r.n_runs == 4 and r.n_excluded == 1
        assert r.stable is True and r.flip_rate == 0.0

    def test_no_runs(self):
        r = decision_stability([])
        assert r.majority_verdict is None and r.stable is False


class TestDispositionFlipFlags:
    def test_stable_slot_not_flagged(self):
        runs = [{"listing_count": "recorded"}, {"listing_count": "recorded"}]
        res = disposition_flip_flags(runs)
        assert res.flagged == [] and not res.has_red_flags

    def test_flip_is_flagged(self):
        runs = [
            {"taxes": "flagged"},
            {"taxes": "recorded"},
            {"taxes": "flagged"},
        ]
        res = disposition_flip_flags(runs)
        assert res.has_red_flags
        flip = res.flagged[0]
        assert flip.slot == "taxes"
        assert set(flip.dispositions) == {"flagged", "recorded"}
        assert flip.counts == {"flagged": 2, "recorded": 1}

    def test_s5_flip_excluded_not_flagged(self):
        runs = [
            {"website_brand_name": "recorded", "taxes": "flagged"},
            {"website_brand_name": "skipped", "taxes": "flagged"},
        ]
        res = disposition_flip_flags(runs, s5_conditional_slots=["website_brand_name"])
        assert [f.slot for f in res.flagged] == []  # taxes stable, website excluded
        assert [f.slot for f in res.excluded] == ["website_brand_name"]
