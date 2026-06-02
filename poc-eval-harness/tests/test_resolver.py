"""R-5 / R-6 — resolve_inscope_slots() unit tests.

These are the acceptance gate for the in-scope resolver (architecture §6.1 / R-5).
They are written BEFORE the implementation (red-green-refactor). Every test must
FAIL until scoring/resolver.py provides a conforming implementation.

Key invariants under test:
  1. The resolver is the single source of truth for the SAR denominator.
  2. The same resolver computes SAR denominator AND cascade re-resolution (D-1).
  3. ownership_model flip cascades correctly through the S8 depends_on chain (C2 / R-5).
  4. C1 4-owner fan-out: each management_model variant adds its own sub-fields.
  5. Adjudication choice (best/worst) propagates through dependency chains (R-6 / §6.5).
  6. The resolver consumes only the *public schema* + profile facts — never the answer key.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from scoring.resolver import AdjudicationChoice, ResolvedSlot, resolve_inscope_slots

FIXTURES = Path(__file__).resolve().parent / "fixtures"
SCHEMA_PATH = Path(__file__).resolve().parents[1] / "schema" / "guesty-pro-account-creation-schema.md"

_H1_SECTIONS = ["S0a", "S0b", "S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8"]


def _load(name: str) -> dict[str, Any]:
    return json.loads((FIXTURES / name).read_text())


# --- C2 ownership flip (cascade R-5/R-6) ------------------------------------


class TestOwnershipFlipCascade:
    """When ownership_model changes, the entire owner-economics branch must flip."""

    def test_owners_slot_in_scope_when_managed(self):
        c2 = _load("profile_c2.json")
        result = resolve_inscope_slots(
            c2["facts_managed"], _H1_SECTIONS, schema_path=SCHEMA_PATH
        )
        slot_ids = {r.slot_id for r in result}
        assert "owners" in slot_ids, "owners must be in scope when ownership_model=all_managed_for_others"

    def test_owners_slot_NOT_in_scope_when_self_owned(self):
        c2 = _load("profile_c2.json")
        result = resolve_inscope_slots(
            c2["facts_self_owned"], _H1_SECTIONS, schema_path=SCHEMA_PATH
        )
        slot_ids = {r.slot_id for r in result}
        assert "owners" not in slot_ids, "owners must be OUT of scope when ownership_model=all_self_owned"

    def test_owners_csv_collapses_with_flip(self):
        c2 = _load("profile_c2.json")
        managed = resolve_inscope_slots(c2["facts_managed"], _H1_SECTIONS, schema_path=SCHEMA_PATH)
        self_owned = resolve_inscope_slots(c2["facts_self_owned"], _H1_SECTIONS, schema_path=SCHEMA_PATH)
        assert "owners_csv" in {r.slot_id for r in managed}
        assert "owners_csv" not in {r.slot_id for r in self_owned}

    def test_denominator_shrinks_on_flip(self):
        """SAR denominator must be strictly smaller for all_self_owned."""
        c2 = _load("profile_c2.json")
        managed = resolve_inscope_slots(c2["facts_managed"], _H1_SECTIONS, schema_path=SCHEMA_PATH)
        self_owned = resolve_inscope_slots(c2["facts_self_owned"], _H1_SECTIONS, schema_path=SCHEMA_PATH)
        assert len(managed) > len(self_owned), (
            f"managed denominator ({len(managed)}) must exceed self-owned ({len(self_owned)})"
        )

    def test_flip_does_not_change_unrelated_slots(self):
        """S4 / S7 slots are ownership-independent and must appear in both sets."""
        c2 = _load("profile_c2.json")
        managed_ids = {r.slot_id for r in resolve_inscope_slots(c2["facts_managed"], _H1_SECTIONS, schema_path=SCHEMA_PATH)}
        self_ids = {r.slot_id for r in resolve_inscope_slots(c2["facts_self_owned"], _H1_SECTIONS, schema_path=SCHEMA_PATH)}
        for slot in ("focus_topics", "go_live", "payment_timing", "taxes"):
            assert slot in managed_ids and slot in self_ids, f"{slot} must be in both scope sets"


# --- C1 4-owner fan-out (R-5) ------------------------------------------------


class TestFourOwnerFanOut:
    """The S8 hero branch must include the full owner + economics slot surface."""

    def test_owners_in_scope(self):
        c1 = _load("profile_c1.json")
        result = resolve_inscope_slots(c1["facts"], _H1_SECTIONS, schema_path=SCHEMA_PATH)
        slot_ids = {r.slot_id for r in result}
        assert "owners" in slot_ids

    def test_ownership_model_in_scope(self):
        c1 = _load("profile_c1.json")
        result = resolve_inscope_slots(c1["facts"], _H1_SECTIONS, schema_path=SCHEMA_PATH)
        assert "ownership_model" in {r.slot_id for r in result}

    def test_direct_channel_makes_s5_conditional_reachable(self):
        """channels includes 'direct' -> website_brand_name is conditionally in scope (S5)."""
        c1 = _load("profile_c1.json")
        assert "direct" in c1["facts"]["channels"]
        result = resolve_inscope_slots(c1["facts"], _H1_SECTIONS, schema_path=SCHEMA_PATH)
        slot_ids = {r.slot_id for r in result}
        assert "website_brand_name" in slot_ids, "S5 slots must be reachable when direct channel is present"

    def test_deposit_amount_in_scope_when_type_is_damage_waiver(self):
        c1 = _load("profile_c1.json")
        assert c1["facts"]["security_deposit_type"] == "damage_waiver"
        result = resolve_inscope_slots(c1["facts"], _H1_SECTIONS, schema_path=SCHEMA_PATH)
        assert "security_deposit_amount" in {r.slot_id for r in result}

    def test_payment_split_not_in_scope_for_at_booking(self):
        c1 = _load("profile_c1.json")
        assert c1["facts"]["payment_timing"] == "at_booking"
        result = resolve_inscope_slots(c1["facts"], _H1_SECTIONS, schema_path=SCHEMA_PATH)
        assert "payment_split" not in {r.slot_id for r in result}

    def test_security_deposit_amount_out_of_scope_without_type(self):
        c1 = _load("profile_c1.json")
        facts_no_deposit = {k: v for k, v in c1["facts"].items() if k != "security_deposit_type"}
        result = resolve_inscope_slots(facts_no_deposit, _H1_SECTIONS, schema_path=SCHEMA_PATH)
        assert "security_deposit_amount" not in {r.slot_id for r in result}


# --- ResolvedSlot contract (R-6) ---------------------------------------------


class TestResolvedSlotContract:
    """Each ResolvedSlot carries the metadata the SAR scorer needs."""

    def test_resolved_slot_has_required_fields(self):
        c2 = _load("profile_c2.json")
        result = resolve_inscope_slots(c2["facts_managed"], _H1_SECTIONS, schema_path=SCHEMA_PATH)
        assert result, "must resolve at least some slots"
        slot = result[0]
        assert isinstance(slot, ResolvedSlot)
        assert isinstance(slot.slot_id, str) and slot.slot_id
        assert slot.priority in ("required", "recommended", "optional")
        assert slot.section  # e.g. "S8"
        assert slot.echo_before_write is not None

    def test_denominator_only_covers_requested_sections(self):
        c2 = _load("profile_c2.json")
        s8_only = resolve_inscope_slots(c2["facts_managed"], ["S8"], schema_path=SCHEMA_PATH)
        all_sections = resolve_inscope_slots(c2["facts_managed"], _H1_SECTIONS, schema_path=SCHEMA_PATH)
        s8_ids = {r.slot_id for r in s8_only}
        all_ids = {r.slot_id for r in all_sections}
        assert s8_ids.issubset(all_ids)
        assert len(all_ids) > len(s8_ids), "all sections must include more slots than S8 alone"

    def test_resolver_is_deterministic(self):
        c1 = _load("profile_c1.json")
        r1 = resolve_inscope_slots(c1["facts"], _H1_SECTIONS, schema_path=SCHEMA_PATH)
        r2 = resolve_inscope_slots(c1["facts"], _H1_SECTIONS, schema_path=SCHEMA_PATH)
        assert [s.slot_id for s in r1] == [s.slot_id for s in r2]

    def test_no_duplicate_slot_ids(self):
        c1 = _load("profile_c1.json")
        result = resolve_inscope_slots(c1["facts"], _H1_SECTIONS, schema_path=SCHEMA_PATH)
        ids = [r.slot_id for r in result]
        assert len(ids) == len(set(ids)), f"duplicate slot ids: {[x for x in ids if ids.count(x) > 1]}"


# --- Adjudication band propagation (R-6 / §6.5) -----------------------------


class TestAdjudicationBandPropagation:
    """§6.5 sensitivity band: best/worst adjudication propagates through dependency chain."""

    def test_adjudication_choice_accepted(self):
        c2 = _load("profile_c2.json")
        # Must not raise with either adjudication choice.
        resolve_inscope_slots(
            c2["facts_managed"], _H1_SECTIONS, schema_path=SCHEMA_PATH,
            adjudication=AdjudicationChoice.BEST
        )
        resolve_inscope_slots(
            c2["facts_managed"], _H1_SECTIONS, schema_path=SCHEMA_PATH,
            adjudication=AdjudicationChoice.WORST
        )

    def test_contested_root_in_worst_case_collapses_dependents(self):
        """Worst-case adjudication of a root slot propagates: dependents become unreachable."""
        # Simulate: ownership_model is contested; worst-case = treated as absent (not recorded).
        # All owner-branch slots must become unreachable under worst-case.
        c2 = _load("profile_c2.json")
        facts_contested_root = {k: v for k, v in c2["facts_managed"].items()
                                 if k != "ownership_model"}
        worst = resolve_inscope_slots(
            facts_contested_root, _H1_SECTIONS, schema_path=SCHEMA_PATH,
            adjudication=AdjudicationChoice.WORST
        )
        worst_ids = {r.slot_id for r in worst}
        assert "owners" not in worst_ids, (
            "when ownership_model is contested (absent) under WORST adjudication, "
            "owners must be unreachable"
        )

    def test_contested_root_in_best_case_expands_dependents(self):
        """Best-case adjudication of an absent root: dependents become reachable."""
        c2 = _load("profile_c2.json")
        facts_contested_root = {k: v for k, v in c2["facts_managed"].items()
                                 if k != "ownership_model"}
        best = resolve_inscope_slots(
            facts_contested_root, _H1_SECTIONS, schema_path=SCHEMA_PATH,
            adjudication=AdjudicationChoice.BEST
        )
        best_ids = {r.slot_id for r in best}
        assert "owners" in best_ids, (
            "under BEST adjudication, contested ownership_model should be assumed "
            "present (most favorable path) making owners reachable"
        )
