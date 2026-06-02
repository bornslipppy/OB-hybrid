"""Story 0.1 — SchemaLoader + FrameGraph depends_on reachability.

The reachability evaluator is the seed of the scoring in-scope resolver (R-5/R-6),
so the depends_on grammar is exercised directly here.
"""

from __future__ import annotations

from kernel.schema import (
    FrameGraph,
    SlotDef,
    _strip_jsonc_comments,
    evaluate_condition,
)


def test_strip_jsonc_preserves_slashes_in_strings():
    src = '{"url": "https://x.com/y", "n": 1} // trailing comment'
    out = _strip_jsonc_comments(src)
    assert "https://x.com/y" in out
    assert "trailing comment" not in out


def test_evaluate_condition_operators():
    assert evaluate_condition(None, {}) is True
    assert evaluate_condition("ownership_model == 'mixed'", {"ownership_model": "mixed"})
    assert not evaluate_condition("ownership_model == 'mixed'", {"ownership_model": "all_self_owned"})
    assert evaluate_condition(
        "ownership_model in ['all_managed_for_others','mixed']", {"ownership_model": "mixed"}
    )
    assert evaluate_condition("channels includes 'direct'", {"channels": ["airbnb", "direct"]})
    assert not evaluate_condition("channels includes 'direct'", {"channels": ["airbnb"]})
    assert evaluate_condition("website_brand_name is recorded", {"website_brand_name": "Sea Breeze"})
    assert not evaluate_condition("website_brand_name is recorded", {})


def test_evaluate_condition_disjunction_and_signals():
    cond = "payment_timing == 'split' OR user volunteers a split"
    assert evaluate_condition(cond, {"payment_timing": "split"})
    assert not evaluate_condition(cond, {"payment_timing": "at_booking"})
    # The non-evaluable clause becomes a runtime signal (FR-4 / EC-27).
    assert evaluate_condition(cond, {"payment_timing": "at_booking"}, {"user_volunteers_a_split": True})


# --- against the real frozen schema -----------------------------------------


def _by_id(slots: list[SlotDef]) -> dict[str, SlotDef]:
    return {s.id: s for s in slots}


def test_loader_parses_known_slots(schema_slots):
    by_id = _by_id(schema_slots)

    assert "ownership_model" in by_id
    om = by_id["ownership_model"]
    assert om.section == "S8"
    assert om.priority == "required"
    assert set(om.options) == {"all_self_owned", "all_managed_for_others", "mixed"}

    owners = by_id["owners"]
    assert owners.section == "S8"
    assert owners.depends_on == "ownership_model in ['all_managed_for_others','mixed']"
    assert "management_model" in owners.item_shape
    assert owners.echo_before_write is True

    dep = by_id["security_deposit_amount"]
    assert dep.echo_before_write is True
    assert dep.depends_on and "security_deposit_type" in dep.depends_on

    taxes = by_id["taxes"]
    assert taxes.echo_before_write is True
    assert taxes.human_handoff == "flag_for_call_1"


def test_loader_assigns_section_from_heading_when_absent(schema_slots):
    by_id = _by_id(schema_slots)
    # S0a objects carry no explicit "section" key — must be inferred from the heading.
    assert by_id["account_name"].section == "S0a"
    assert by_id["channels"].section == "S2"


def test_loader_skips_non_field_blocks(schema_slots):
    # The §1 runtime-state example object has no "id" and must not become a slot.
    assert all(s.id for s in schema_slots)
    assert "value" not in _by_id(schema_slots)  # runtime example {"value": ...} excluded


def test_frame_reachability_hero_branch(schema_slots):
    frame = FrameGraph(schema_slots)
    managed = frame.reachable_slots({"ownership_model": "mixed"}, ["S8"])
    self_owned = frame.reachable_slots({"ownership_model": "all_self_owned"}, ["S8"])
    assert "owners" in {s.id for s in managed}
    assert "owners" not in {s.id for s in self_owned}


def test_frame_reachability_records_depends_on_fields(schema_slots):
    frame = FrameGraph(schema_slots)
    assert "ownership_model" in frame.depends_on_fields["owners"]
