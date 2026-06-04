"""Build agent context from a Salesforce account + handover note (demo path)."""

from __future__ import annotations

import re
from typing import Any

from harness.sales_notes import SalesAccount
from kernel.protocol import UserQuestion
from kernel.state import ProfileState, SlotState, SlotStatus, StateReducer
from kernel.tools import RecordAnswer, Source

# Admin / identity fields Salesforce already has — auto-recorded for the stakeholder demo
# so the agent skips cold questions about name, country, language, etc.
_TRIVIAL_SF_RECORDED = frozenset(
    {
        "account_name",
        "country",
        "active_listing_count",
        "listing_count",
        "ob_language",
        "ob_specialist_name",
        "business_profile",
        "connected_channels",
        "channels",
    }
)

# Note-derived slots seeded as prefilled_unconfirmed until the user confirms.
_NOTE_PREFILL_SLOTS = frozenset(
    {
        "migration_source",
        "prior_pms_experience",
        "addon_intent",
        "focus_topics",
        "go_live",
        "third_party_tools",
    }
)

_MIGRATION_KEYWORDS: tuple[tuple[str, str], ...] = (
    ("hostaway", "hostaway"),
    ("lodgify", "lodgify"),
    ("smoobu", "smoobu"),
    ("avantio", "avantio"),
    ("hostfully", "hostfully"),
    ("uplisting", "uplisting"),
    ("streamline", "streamline"),
    ("ownerrez", "ownerrez"),
    ("hospitable", "hospitable"),
    ("guesty lite", "guesty_lite"),
    ("guesty for hosts", "guesty_for_hosts"),
    ("beds24", "beds24"),
    ("cloudbeds", "cloudbeds"),
)

_ADDON_KEYWORDS: tuple[tuple[str, str], ...] = (
    ("gpo", "gpo"),
    ("guesty pay", "guestypay"),
    ("guestypay", "guestypay"),
    ("damage protection", "damage_protection"),
    ("damage pro", "damage_protection"),
    ("locks", "locks"),
    ("smart lock", "locks"),
    ("remotelock", "locks"),
    ("accounting", "accounting"),
    ("abw", "abw"),
    ("auto comply", "auto_comply"),
    ("premium channel", "premium_channels"),
)

_FOCUS_KEYWORDS: tuple[tuple[str, str], ...] = (
    ("owner report", "owner_reporting"),
    ("owner reporting", "owner_reporting"),
    ("statement", "owner_reporting"),
    ("pricing", "pricing_strategy"),
    ("pricelabs", "pricing_strategy"),
    ("rate strategy", "pricing_strategy"),
    ("gpo", "pricing_strategy"),
    ("messaging", "guest_messaging"),
    ("message template", "guest_messaging"),
    ("automated message", "guest_messaging"),
    ("cleaner", "cleaner_workflows"),
    ("turnover", "cleaner_workflows"),
    ("cleaning", "cleaner_workflows"),
    ("quickbooks", "accounting_setup"),
    ("xero", "accounting_setup"),
    ("bookkeeping", "accounting_setup"),
    ("booking site", "booking_website"),
    ("booking website", "booking_website"),
    ("direct site", "booking_website"),
    ("review", "reviews_reputation"),
    ("reputation", "reviews_reputation"),
    ("channel mix", "channel_mix"),
)

_GO_LIVE_KEYWORDS: tuple[tuple[str, str], ...] = (
    ("asap", "asap"),
    ("urgent", "asap"),
    ("go live", "asap"),
    ("this week", "asap"),
    ("2-4 week", "2-4w"),
    ("2 to 4", "2-4w"),
    ("1-2 month", "1-2m"),
    ("exploring", "exploring"),
    ("just looking", "exploring"),
)

_PRIOR_PMS_KEYWORDS: tuple[tuple[str, str], ...] = (
    ("first time", "none_first_time"),
    ("first-time", "none_first_time"),
    ("never used", "none_first_time"),
    ("new to pms", "none_first_time"),
    ("manual", "manual_only"),
    ("spreadsheet", "manual_only"),
)

_THIRD_PARTY_KEYWORDS: tuple[tuple[str, str, str], ...] = (
    ("pricelabs", "pms_or_pricing", "PriceLabs"),
    ("price labs", "pms_or_pricing", "PriceLabs"),
    ("turno", "cleaning", "Turno"),
    ("remotelock", "locks", "RemoteLock"),
    ("yale", "locks", "Yale"),
    ("august", "locks", "August"),
)

_COUNTRY_HINTS: tuple[tuple[tuple[str, ...], str], ...] = (
    ((" united kingdom", " uk", " london", " britain", " england"), "United Kingdom"),
    ((" australia", " sydney", " melbourne", " brisbane"), "Australia"),
    ((" france", " paris", " french"), "France"),
    ((" spain", " barcelona", " madrid", " spanish"), "Spain"),
    ((" germany", " berlin", " german"), "Germany"),
    ((" italy", " rome", " italian"), "Italy"),
    ((" canada", " toronto", " vancouver"), "Canada"),
)

_CITY_BY_COUNTRY: dict[str, str] = {
    "United States": "San Diego",
    "United Kingdom": "London",
    "Australia": "Sydney",
    "France": "Paris",
    "Spain": "Barcelona",
    "Germany": "Berlin",
    "Italy": "Rome",
    "Canada": "Toronto",
}

_LANGUAGE_BY_COUNTRY: dict[str, str] = {
    "France": "fr",
    "Spain": "es",
    "Germany": "de",
    "Italy": "it",
}

_CONFIRM_START = re.compile(
    r"^\s*(yes|yeah|yep|yup|correct|right|accurate|exactly|affirmative|"
    r"that(?:'s| is) (?:right|correct|accurate)|still accurate|sounds good|"
    r"mostly|all good)\b",
    re.IGNORECASE,
)
_CORRECTION_HINTS = (
    "no",
    "not ",
    "n't",
    "actually",
    "instead",
    "except",
    "wrong",
    "change",
    "different",
    "correction",
)


def _slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-") or "account"


def _haystack(account: SalesAccount) -> str:
    return f"{account.account_name} {account.opportunity_name} {account.notes}".lower()


def _infer_country(account: SalesAccount) -> str:
    text = _haystack(account)
    for needles, country in _COUNTRY_HINTS:
        if any(n in text for n in needles):
            return country
    return "United States"


def _infer_city(account: SalesAccount, country: str) -> str:
    text = _haystack(account)
    for needles, _country in _COUNTRY_HINTS:
        for needle in needles:
            token = needle.strip()
            if len(token) > 3 and token in text:
                return token.title()
    return _CITY_BY_COUNTRY.get(country, "San Diego")


def _infer_language(account: SalesAccount, country: str) -> str:
    text = _haystack(account)
    if "french" in text or " en français" in text:
        return "fr"
    if "spanish" in text or " en español" in text or "espanol" in text:
        return "es"
    if "german" in text or " deutsch" in text:
        return "de"
    if "portuguese" in text or " português" in text:
        return "pt"
    return _LANGUAGE_BY_COUNTRY.get(country, "en")


def _infer_channels(account: SalesAccount) -> list[str]:
    text = _haystack(account)
    channels = ["airbnb", "booking"]
    if "vrbo" in text or "homeaway" in text:
        channels.append("vrbo")
    if "expedia" in text:
        channels.append("expedia")
    if "direct" in text or "booking site" in text or "website" in text:
        channels.append("direct")
    return channels


def _infer_business_profile(account: SalesAccount) -> dict[str, str]:
    slug = _slug(account.account_name)
    return {
        "business_name": account.account_name,
        "business_email": f"hello@{slug}.com",
        "domain_hint": f"{slug}.com",
    }


def _extract_first(text: str, keywords: tuple[tuple[str, str], ...]) -> str | None:
    for needle, value in keywords:
        if needle in text:
            return value
    return None


def _extract_list(text: str, keywords: tuple[tuple[str, str], ...], *, limit: int = 3) -> list[str]:
    hits: list[str] = []
    for needle, value in keywords:
        if needle in text and value not in hits:
            hits.append(value)
        if len(hits) >= limit:
            break
    return hits


def _extract_addons(text: str) -> list[str]:
    return _extract_list(text, _ADDON_KEYWORDS, limit=6)


def _extract_third_party_tools(text: str) -> dict[str, list[str]] | None:
    tools: dict[str, list[str]] = {}
    for needle, key, label in _THIRD_PARTY_KEYWORDS:
        if needle in text:
            tools.setdefault(key, [])
            if label not in tools[key]:
                tools[key].append(label)
    return tools or None


def note_signals_defer_financials(account: SalesAccount) -> bool:
    text = _haystack(account)
    return any(
        phrase in text
        for phrase in (
            "nervous",
            "financial",
            "tax",
            "taxes",
            "defer",
            "later on call",
            "discuss with jordan",
        )
    )


def derive_sf_demo_metadata(account: SalesAccount) -> dict[str, Any]:
    """Plausible Salesforce admin values for the stakeholder demo."""
    country = _infer_country(account)
    city = _infer_city(account, country)
    language = _infer_language(account, country)
    channels = _infer_channels(account)
    specialist = account.opportunity_owner.strip() or "Jordan"
    listing = account.listing_count if account.listing_count is not None else 10
    text = _haystack(account)

    note_extras: dict[str, Any] = {}
    migration = _extract_first(text, _MIGRATION_KEYWORDS)
    if migration:
        note_extras["migration_source"] = migration
    addons = _extract_addons(text)
    if addons:
        note_extras["addon_intent"] = addons
    focus = _extract_list(text, _FOCUS_KEYWORDS, limit=3)
    if focus:
        note_extras["focus_topics"] = focus
    go_live = _extract_first(text, _GO_LIVE_KEYWORDS)
    if go_live:
        note_extras["go_live"] = go_live
    prior = _extract_first(text, _PRIOR_PMS_KEYWORDS)
    if prior:
        note_extras["prior_pms_experience"] = prior
    elif migration and migration not in ("none", "guesty_for_hosts", "guesty_lite"):
        note_extras["prior_pms_experience"] = "experienced"
    tools = _extract_third_party_tools(text)
    if tools:
        note_extras["third_party_tools"] = tools

    return {
        "account_name": account.account_name,
        "country": country,
        "city": city,
        "active_listing_count": listing,
        "listing_count": listing,
        "ob_language": language,
        "ob_specialist_name": specialist,
        "business_profile": _infer_business_profile(account),
        "connected_channels": channels,
        "channels": list(channels),
        **note_extras,
    }


def build_demo_prompt_overlay(account: SalesAccount) -> str:
    """Compact demo rules + note — appended to the base system prompt."""
    meta = derive_sf_demo_metadata(account)
    note = account.notes or "(no handover note in export)"
    prefilled = [
        f"{slot}={meta[slot]!r}"
        for slot in sorted(_NOTE_PREFILL_SLOTS)
        if slot in meta
    ]
    defer = note_signals_defer_financials(account)

    lines = [
        "## DEMO MODE — STAKEHOLDER SCREEN SHARE",
        "",
        f"Customer: **{account.account_name}** · Rep: {account.opportunity_owner or '—'}",
        "",
        "**Rules (override generic ordering):**",
        "1. Salesforce admin is already **RECORDED** — never ask name, country, language, listings, channels, or specialist.",
        "2. **Open by reflecting the note**, then confirm note-derived items — never cold-ask migration/add-ons/focus.",
        "3. After the user confirms a PREFILL item, **record it immediately** with `record_answer` (`user_stated` or `ai_extracted_from_note`).",
        "4. Max **one question** per message; keep replies short and conversational.",
        "5. Prioritize note themes before generic schema walk-through.",
    ]
    if defer:
        lines.append(
            "6. Note signals tax/financial anxiety — **offer to skip S4** on first pass; honor deferral immediately."
        )
    lines.append(
        "7. **Mandatory fees:** If the customer lists several fee *types* without amounts "
        "(e.g. resort, pet, admin, hot tub), collect **one at a time** — ask the amount, "
        "echo it back, confirm, call `add_fee`, then move to the next type. Never skip "
        "amounts; never bundle multiple fees into one write."
    )
    lines.extend(
        [
            "",
            "**Note-derived PREFILL (confirm, then record):**",
            ", ".join(prefilled) if prefilled else "(none extracted — reflect the raw note)",
            "",
            "**Sales handover note:**",
            note,
        ]
    )
    return "\n".join(lines)


def build_account_brief(account: SalesAccount) -> str:
    """Sidebar preview — same content as the demo overlay."""
    return build_demo_prompt_overlay(account)


def build_opening_user_message(account: SalesAccount) -> str:
    """First glue-completion turn — forces a note-aware opening."""
    meta = derive_sf_demo_metadata(account)
    note = account.notes or "(empty)"
    confirm_hints: list[str] = []
    if "migration_source" in meta:
        confirm_hints.append(f"migration from {meta['migration_source']}")
    if "addon_intent" in meta:
        confirm_hints.append(f"add-ons: {', '.join(meta['addon_intent'])}")
    if "focus_topics" in meta:
        confirm_hints.append(f"focus: {', '.join(meta['focus_topics'])}")
    if not confirm_hints:
        confirm_hints.append("the main point in the sales note")

    return (
        f"Begin onboarding for {account.account_name}. "
        "Salesforce admin is already recorded — do not mention or ask for it. "
        "Write your FIRST message to the customer now. It must:\n"
        f"1. Greet them (use {account.account_name}).\n"
        "2. Show you read the sales handover note — cite 2–3 specific facts from it.\n"
        f"3. Ask exactly ONE confirmation question about: {' OR '.join(confirm_hints[:2])}.\n"
        "Do NOT call tools. Natural language only. Maximum 4 sentences.\n\n"
        f"Handover note: {note}"
    )


def seed_account_prefill(state: ProfileState, account: SalesAccount) -> ProfileState:
    """Seed demo session state from the Salesforce export row."""
    meta = derive_sf_demo_metadata(account)

    recorded: dict[str, tuple[Any, str]] = {
        field_id: (meta[field_id], "sf_prefill")
        for field_id in _TRIVIAL_SF_RECORDED
        if field_id in meta
    }

    prefilled: dict[str, tuple[Any, str]] = {
        field_id: (meta[field_id], "ai_extracted_from_note")
        for field_id in _NOTE_PREFILL_SLOTS
        if field_id in meta
    }

    new_slots = dict(state.slots)
    for field_id, (value, source) in recorded.items():
        new_slots[field_id] = SlotState(
            field_id=field_id,
            status=SlotStatus.RECORDED,
            value=value,
            source=source,
        )
    for field_id, (value, source) in prefilled.items():
        new_slots[field_id] = SlotState(
            field_id=field_id,
            status=SlotStatus.PREFILLED_UNCONFIRMED,
            value=value,
            source=source,
        )
    return state.model_copy(update={"slots": new_slots})


def is_demo_confirmation(text: str) -> bool:
    """True when the user is affirming (not correcting) a prefilled fact."""
    stripped = text.strip()
    if not stripped:
        return False
    lower = stripped.lower()
    if any(hint in lower for hint in _CORRECTION_HINTS):
        return False
    return bool(_CONFIRM_START.search(stripped))


def _prefilled_slots(state: ProfileState) -> list[tuple[str, Any, str]]:
    return [
        (fid, slot.value, slot.source or "ai_extracted_from_note")
        for fid, slot in state.slots.items()
        if slot.status is SlotStatus.PREFILLED_UNCONFIRMED and slot.value is not None
    ]


def apply_demo_auto_confirm(
    state: ProfileState,
    *,
    user_text: str,
    question: UserQuestion | None,
    reducer: StateReducer,
) -> ProfileState:
    """Record note-derived prefills when the user confirms — demo path only."""
    if not is_demo_confirmation(user_text):
        return state

    prefilled = _prefilled_slots(state)
    if not prefilled:
        return state

    primary = question.primary_slot if question else None
    if primary and any(fid == primary for fid, _, _ in prefilled):
        targets = [(fid, val, src) for fid, val, src in prefilled if fid == primary]
    else:
        # Broad opening confirm — record every note-derived prefill at once.
        targets = prefilled

    new_state = state
    for field_id, value, _source in targets:
        new_state = reducer.apply(
            new_state,
            RecordAnswer(
                field_id=field_id,
                value=value,
                source=Source.USER_STATED,
            ),
        )
    return new_state


def suggested_replies(
    account: SalesAccount | None,
    *,
    question_text: str | None,
    primary_slot: str | None,
    turn_count: int,
    state: ProfileState | None = None,
) -> list[str]:
    """Opening-turn chips only — no buttons on later questions."""
    if account is None or not question_text or turn_count > 2:
        return []

    q = question_text.lower()
    if not _is_note_confirmation_question(q, primary_slot, state, turn_count):
        return []

    defer = note_signals_defer_financials(account)
    chips = [
        "Yes, that's still accurate.",
        "Mostly right — one thing changed (I'll explain).",
    ]
    if defer:
        chips.append("Let's defer financials — Jordan can cover that on Call 1.")
    else:
        chips.append("Sounds good — what do you need next?")
    return chips


def _is_note_confirmation_question(
    q: str,
    primary_slot: str | None,
    state: ProfileState | None,
    turn_count: int,
) -> bool:
    if primary_slot in {"migration_source", "addon_intent", "third_party_tools"}:
        return True
    note_phrases = (
        "sales noted",
        "sales note",
        "handover note",
        "still accurate",
        "still right",
        "coming from hostaway",
        "coming from lodgify",
        "bundle:",
    )
    if any(p in q for p in note_phrases):
        return True
    if turn_count <= 1 and state is not None and _prefilled_slots(state):
        return any(w in q for w in ("accurate", "correct", "right", "still", "noted", "see that"))
    return False
