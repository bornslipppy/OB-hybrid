"""Sales notes loader + account prefill (stakeholder demo path)."""

from __future__ import annotations

from harness.account_context import (
    apply_demo_auto_confirm,
    build_account_brief,
    build_demo_prompt_overlay,
    build_opening_user_message,
    derive_sf_demo_metadata,
    is_demo_confirmation,
    seed_account_prefill,
    suggested_replies,
)
from harness.sales_notes import SalesAccount, get_account, load_sales_accounts, search_accounts
from kernel.protocol import UserQuestion
from kernel.state import ProfileState, SlotStatus, StateReducer


def _city_coastal() -> SalesAccount:
    return SalesAccount(
        account_name="City and Coastal",
        listing_count=11,
        opportunity_name="City and Coastal - deal",
        opportunity_owner="Jesse Grumet",
        notes="BUNDLE: PMS + GPO. Coming from Hostaway. Wants locks.",
    )


def test_build_account_brief_mentions_confirm():
    brief = build_account_brief(_city_coastal())
    assert "City and Coastal" in brief
    assert "DEMO MODE" in brief
    assert "Hostaway" in brief


def test_demo_prompt_overlay_mandatory_fees_rule():
    overlay = build_demo_prompt_overlay(_city_coastal())
    assert "Mandatory fees" in overlay
    assert "one at a time" in overlay.lower()

    msg = build_opening_user_message(_city_coastal())
    assert "City and Coastal" in msg
    assert "Handover note" in msg
    assert "Do NOT call tools" in msg


def test_derive_sf_demo_metadata_infers_country_and_language():
    account = SalesAccount(
        account_name="Paris Stays",
        listing_count=8,
        opportunity_name="",
        opportunity_owner="Marie Dupont",
        notes="French-speaking team. Airbnb + Booking.",
    )
    meta = derive_sf_demo_metadata(account)
    assert meta["country"] == "France"
    assert meta["ob_language"] == "fr"
    assert meta["ob_specialist_name"] == "Marie Dupont"
    assert "airbnb" in meta["channels"]


def test_derive_sf_demo_metadata_extracts_focus_and_addons():
    meta = derive_sf_demo_metadata(_city_coastal())
    assert meta["migration_source"] == "hostaway"
    assert "gpo" in meta["addon_intent"]
    assert "locks" in meta["addon_intent"]
    assert "pricing_strategy" in meta["focus_topics"]


def test_seed_account_prefill_records_trivial_and_note_slots():
    account = SalesAccount(
        account_name="Harbor Point",
        listing_count=5,
        opportunity_name="",
        opportunity_owner="",
        notes="Moving from Hostaway. Wants GPO. Owner reporting is a priority.",
    )
    state = seed_account_prefill(ProfileState(profile_id="live"), account)

    assert state.slots["account_name"].status is SlotStatus.RECORDED
    assert state.slots["channels"].status is SlotStatus.RECORDED
    assert state.slots["migration_source"].status is SlotStatus.PREFILLED_UNCONFIRMED
    assert state.slots["focus_topics"].value == ["owner_reporting", "pricing_strategy"]


def test_apply_demo_auto_confirm_records_prefills_on_yes():
    account = _city_coastal()
    state = seed_account_prefill(ProfileState(profile_id="live"), account)
    reducer = StateReducer(frame=None)
    question = UserQuestion(text="Sales noted Hostaway and GPO — still right?", primary_slot=None)

    updated = apply_demo_auto_confirm(
        state,
        user_text="Yes, that's still accurate.",
        question=question,
        reducer=reducer,
    )
    assert updated.slots["migration_source"].status is SlotStatus.RECORDED
    assert updated.slots["addon_intent"].status is SlotStatus.RECORDED


def test_apply_demo_auto_confirm_ignores_corrections():
    state = seed_account_prefill(ProfileState(profile_id="live"), _city_coastal())
    reducer = StateReducer(frame=None)
    question = UserQuestion(text="Still on Hostaway?", primary_slot="migration_source")

    updated = apply_demo_auto_confirm(
        state,
        user_text="No, we actually moved to Lodgify.",
        question=question,
        reducer=reducer,
    )
    assert updated.slots["migration_source"].status is SlotStatus.PREFILLED_UNCONFIRMED


def test_is_demo_confirmation():
    assert is_demo_confirmation("Yes, that's still accurate.")
    assert not is_demo_confirmation("No, that's wrong.")


def test_suggested_replies_only_on_opening_turn():
    state = seed_account_prefill(ProfileState(profile_id="live"), _city_coastal())
    opening = suggested_replies(
        _city_coastal(),
        question_text="Sales noted Hostaway — still accurate?",
        primary_slot=None,
        turn_count=1,
        state=state,
    )
    assert any("accurate" in c.lower() for c in opening)

    later = suggested_replies(
        _city_coastal(),
        question_text="When are you looking to go live? ASAP, 2-4 weeks, or exploring?",
        primary_slot="go_live",
        turn_count=3,
        state=state,
    )
    assert later == []


def test_load_tamar_export_if_present():
    path = "/Users/yair.cohen/Downloads/Notes for Tamar-2026-06-02-13-51-50 (1).xlsx"
    try:
        accounts = load_sales_accounts(path)
    except FileNotFoundError:
        return
    assert len(accounts) > 100
    hit = get_account(path, "City and Coastal")
    assert hit is not None
    assert hit.listing_count == 11
    assert "GPO" in hit.notes or "PMS" in hit.notes
    matches = search_accounts(path, "Coastal", limit=5)
    assert any("Coastal" in m.account_name for m in matches)
