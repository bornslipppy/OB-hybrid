"""Story 0.1 — the 7-tool contract (FR-2). Validation is the acceptance gate."""

from __future__ import annotations

import pytest
from pydantic import TypeAdapter, ValidationError

from kernel.tools import (
    AddFee,
    AddOwner,
    AddTax,
    EndSection,
    FlagForCall1,
    RecordAnswer,
    SkipQuestion,
    Source,
    ToolCall,
    parse_tool_call,
    to_anthropic_tools,
)

_ADAPTER = TypeAdapter(ToolCall)


def test_exactly_seven_tools_exported():
    from kernel.tools import TOOL_MODELS, TOOL_NAMES

    assert len(TOOL_MODELS) == 7
    assert set(TOOL_NAMES) == {
        "record_answer",
        "add_fee",
        "add_tax",
        "add_owner",
        "skip_question",
        "flag_for_call_1",
        "end_section",
    }


def test_record_answer_roundtrips():
    tc = RecordAnswer(field_id="go_live", value="asap", source=Source.USER_STATED)
    assert tc.tool == "record_answer"
    parsed = parse_tool_call("record_answer", {"field_id": "go_live", "value": "asap", "source": "user_stated"})
    assert parsed == tc


def test_discriminated_union_selects_model():
    tc = _ADAPTER.validate_python(
        {"tool": "add_fee", "fee_type": "pet", "amount": 50.0, "unit": "flat"}
    )
    assert isinstance(tc, AddFee)


def test_add_tax_free_tax_type_but_constrained_enums():
    # tax_type is free (G3 casing provisional, OPEN-3) — odd casing accepted.
    tax = AddTax(
        tax_type="Occupancy_Tourist",
        inclusivity="exclusive",
        what_taxed=["accommodation_fare", "cleaning_fee"],
        scope="account_wide",
    )
    assert tax.tax_type == "Occupancy_Tourist"
    # what_taxed is enum-constrained.
    with pytest.raises(ValidationError):
        AddTax(
            tax_type="gst",
            inclusivity="inclusive",
            what_taxed=["not_a_real_line_item"],
            scope="listing",
        )


def test_add_owner_depends_on_commission_ok():
    owner = AddOwner(
        owner_name="Dana",
        email="dana@x.com",
        listings=["L1", "L2"],
        management_model="commission",
        pmc_commission_rate=15.0,
        who_pays_channel_commission="pmc",
    )
    assert owner.pmc_commission_rate == 15.0


def test_add_owner_rejects_mismatched_economics_field():
    # fixed_fee_amount is only valid under management_model == 'fixed_fee'.
    with pytest.raises(ValidationError):
        AddOwner(
            owner_name="Dana",
            email="dana@x.com",
            listings=["L1"],
            management_model="commission",
            fixed_fee_amount=500.0,
        )
    # split_terms only under revenue_split | other.
    with pytest.raises(ValidationError):
        AddOwner(
            owner_name="Dana",
            email="dana@x.com",
            listings=["L1"],
            management_model="commission",
            split_terms="70/30 after fees",
        )


def test_add_owner_revenue_split_and_other_accept_split_terms():
    for mm in ("revenue_split", "other"):
        owner = AddOwner(
            owner_name="O",
            email="o@x.com",
            listings=["L1"],
            management_model=mm,
            split_terms="70% of whatever comes in after fees",
        )
        assert owner.split_terms


def test_flag_for_call_1_optional_field_id():
    with_field = FlagForCall1(topic="taxes", user_quote="q", note="n", field_id="taxes")
    without_field = FlagForCall1(topic="sentiment", user_quote="q", note="n")
    assert with_field.field_id == "taxes"
    assert without_field.field_id is None


def test_simple_tools_validate():
    assert SkipQuestion(field_id="rate_strategy", reason="defer").tool == "skip_question"
    assert EndSection(section_id="S4").tool == "end_section"


def test_parse_tool_call_unknown_name_raises():
    with pytest.raises(KeyError):
        parse_tool_call("not_a_tool", {})


def test_anthropic_tool_export_strips_discriminator():
    defs = to_anthropic_tools()
    assert len(defs) == 7
    names = {d["name"] for d in defs}
    assert names == {
        "record_answer",
        "add_fee",
        "add_tax",
        "add_owner",
        "skip_question",
        "flag_for_call_1",
        "end_section",
    }
    for d in defs:
        assert "tool" not in d["input_schema"].get("properties", {})
        assert "tool" not in d["input_schema"].get("required", [])
        assert d["description"]
