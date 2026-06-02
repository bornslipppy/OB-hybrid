"""Story 4.9 — free-text blind-rater protocol (FR-35 / §6.4 / SM-9)."""

from __future__ import annotations

import json

from scoring.rater_queue import (
    INDEX_FILE,
    RATINGS_FILE,
    TASKS_FILE,
    Adjudication,
    Rating,
    ScoredRun,
    adjudicate,
    adjudicated_scores,
    build_tasks,
    cohen_kappa,
    inter_rater_kappa,
    make_task_id,
    read_index,
    read_ratings,
    write_queue,
)
from scoring.sar import ProfileScore, SlotScore


def _profile_score(profile_id, slot_values: dict[str, str]) -> ProfileScore:
    slot_scores = [
        SlotScore(
            slot_id=sid, section="S7", expected_disposition="recorded",
            expected_value="gold", actual_status="recorded", actual_value=val,
            score=1, reason="free-text", requires_human_rating=True,
        )
        for sid, val in slot_values.items()
    ]
    return ProfileScore(
        profile_id=profile_id, group="B", system_id="agent", sar=1.0,
        numerator=len(slot_scores), denominator=len(slot_scores), slot_scores=slot_scores,
        human_rating_pending=list(slot_values),
    )


class TestBuildAndAnonymize:
    def test_tasks_carry_no_system_attribution(self, tmp_path):
        runs = [
            ScoredRun("agent", "B1", 0, _profile_score("B1", {"pain": "manual pricing is hard"})),
            ScoredRun("tree", "B1", 0, _profile_score("B1", {"pain": "n/a"})),
        ]
        tasks, index = build_tasks(runs)
        assert len(tasks) == 2
        # The rater-visible task must not leak the system.
        for t in tasks:
            blob = json.dumps(t.__dict__)
            assert "agent" not in blob and "tree" not in blob
            assert hasattr(t, "slot_id") and hasattr(t, "value")
        # The internal index DOES carry the mapping.
        assert {e.system_id for e in index} == {"agent", "tree"}

    def test_task_id_is_stable_and_system_specific(self):
        a = make_task_id("agent", "B1", 0, "pain")
        a2 = make_task_id("agent", "B1", 0, "pain")
        t = make_task_id("tree", "B1", 0, "pain")
        assert a == a2 and a != t

    def test_write_and_read_roundtrip(self, tmp_path):
        runs = [ScoredRun("agent", "B1", 0, _profile_score("B1", {"pain": "x"}))]
        tasks, index = build_tasks(runs)
        write_queue(tmp_path, tasks, index)
        assert (tmp_path / TASKS_FILE).exists()
        assert (tmp_path / INDEX_FILE).exists()
        assert len(read_index(tmp_path)) == 1


class TestCohenKappa:
    def test_perfect_agreement(self):
        assert cohen_kappa([1, 0, 1, 1], [1, 0, 1, 1]) == 1.0

    def test_total_disagreement_is_negative(self):
        assert cohen_kappa([1, 1, 0, 0], [0, 0, 1, 1]) < 0

    def test_single_category_perfect(self):
        # both raters all-1 → pe == 1 → convention κ = 1.0
        assert cohen_kappa([1, 1, 1], [1, 1, 1]) == 1.0

    def test_partial_agreement_between_zero_and_one(self):
        k = cohen_kappa([1, 1, 0, 1, 0, 0], [1, 0, 0, 1, 0, 1])
        assert 0.0 < k < 1.0

    def test_empty(self):
        assert cohen_kappa([], []) == 1.0


class TestInterRaterKappa:
    def test_picks_pair_with_most_shared(self):
        ratings = [
            Rating("t1", "r1", 1), Rating("t1", "r2", 1),
            Rating("t2", "r1", 0), Rating("t2", "r2", 0),
            Rating("t3", "r1", 1), Rating("t3", "r2", 0),
        ]
        res = inter_rater_kappa(ratings)
        assert res.n_shared == 3
        assert {res.rater_a, res.rater_b} == {"r1", "r2"}


class TestAdjudicate:
    def test_consensus(self):
        ratings = [Rating("t1", "r1", 1), Rating("t1", "r2", 1)]
        adj = adjudicate(ratings)
        assert adj["t1"].score == 1 and adj["t1"].method == "consensus"

    def test_disagreement_routes_to_tie_breaker(self):
        ratings = [Rating("t1", "r1", 1), Rating("t1", "r2", 0), Rating("t1", "tb", 0)]
        adj = adjudicate(ratings, tie_breaker_rater="tb")
        assert adj["t1"].score == 0 and adj["t1"].method == "tie_breaker"

    def test_disagreement_without_tie_breaker_is_unresolved(self):
        ratings = [Rating("t1", "r1", 1), Rating("t1", "r2", 0)]
        adj = adjudicate(ratings)
        assert adj["t1"].score is None and adj["t1"].method == "unresolved"

    def test_single_rater(self):
        adj = adjudicate([Rating("t1", "r1", 1)])
        assert adj["t1"].method == "single" and adj["t1"].score == 1


class TestAdjudicatedScoresBackMap:
    def test_maps_back_to_system_profile_run_slot(self):
        runs = [ScoredRun("agent", "B1", 0, _profile_score("B1", {"pain": "x", "split_terms": "y"}))]
        tasks, index = build_tasks(runs)
        # rate both tasks 1 and 0 respectively, by consensus
        ratings = []
        for t in tasks:
            score = 1 if t.slot_id == "pain" else 0
            ratings.append(Rating(t.task_id, "r1", score))
            ratings.append(Rating(t.task_id, "r2", score))
        adj = adjudicate(ratings)
        scores = adjudicated_scores(adj, index)
        assert scores[("agent", "B1", 0)] == {"pain": 1, "split_terms": 0}

    def test_unresolved_omitted(self):
        runs = [ScoredRun("agent", "B1", 0, _profile_score("B1", {"pain": "x"}))]
        tasks, index = build_tasks(runs)
        ratings = [Rating(tasks[0].task_id, "r1", 1), Rating(tasks[0].task_id, "r2", 0)]
        adj = adjudicate(ratings)
        assert adjudicated_scores(adj, index) == {}  # unresolved → not mapped


class TestScoreProfileConsumesRatings:
    def test_human_ratings_override_provisional(self):
        from pathlib import Path

        from kernel.state import ProfileState, SlotState, SlotStatus
        from scoring.sar import AnswerKey, ExpectedDisposition, score_profile

        schema = Path(__file__).resolve().parents[1] / "schema" / "guesty-pro-account-creation-schema.md"
        state = ProfileState(profile_id="B1")
        state.slots["pain"] = SlotState(field_id="pain", status=SlotStatus.RECORDED, value="some pain")
        ak = AnswerKey(
            profile_id="B1", group="B",
            slots={"pain": ExpectedDisposition(disposition="recorded", value="gold", value_type="free_text")},
        )
        # Without ratings: provisional pass (score 1, pending).
        prov = score_profile(state, ak, ["S7"], schema_path=schema, system_id="agent")
        assert "pain" in prov.human_rating_pending
        # With an adjudicated 0: slot scored 0, no longer pending.
        rated = score_profile(state, ak, ["S7"], schema_path=schema, system_id="agent",
                              human_ratings={"pain": 0})
        assert "pain" not in rated.human_rating_pending
        pain = next(ss for ss in rated.slot_scores if ss.slot_id == "pain")
        assert pain.score == 0 and pain.requires_human_rating is False
