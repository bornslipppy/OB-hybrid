"""Session-context builder for the OB-V2 wizard merge demo.

Reuses the brain's deterministic extractors (`harness.account_context`) and the
Salesforce-export loader (`harness.sales_notes`) to turn one Tamar xlsx row into
the context payload the wizard consumes at session init.

PII boundary: the raw note (emails, contact names, free text) never leaves this
process. The browser receives only the SF prefill fields, a first name for the
greeting, extracted enum signals, and note-summary bullets derived from those
enums — not the raw note string.
"""

from __future__ import annotations

import re
from datetime import date, timedelta
from typing import Any

from harness.account_context import (
    derive_sf_demo_metadata,
    note_signals_defer_financials,
)
from harness.sales_notes import (
    SalesAccount,
    get_account,
    resolve_notes_path,
    search_accounts,
)

# The onboarding specialist who runs Call 1 (matches the wizard avatar asset).
# Distinct from the Salesforce opportunity owner, who is the *sales* rep.
ONBOARDING_SPECIALIST = "Amanda"

# Human-readable labels for extracted enum values (browser-safe, no PII).
_MIGRATION_LABELS = {
    "hostaway": "Hostaway",
    "lodgify": "Lodgify",
    "smoobu": "Smoobu",
    "avantio": "Avantio",
    "hostfully": "Hostfully",
    "uplisting": "Uplisting",
    "streamline": "Streamline",
    "ownerrez": "OwnerRez",
    "hospitable": "Hospitable",
    "guesty_lite": "Guesty Lite",
    "guesty_for_hosts": "Guesty for Hosts",
    "beds24": "Beds24",
    "cloudbeds": "Cloudbeds",
}
_ADDON_LABELS = {
    "gpo": "GPO (dynamic pricing)",
    "guestypay": "Guesty Pay",
    "damage_protection": "Damage Protection",
    "locks": "Smart locks",
    "accounting": "Accounting",
    "abw": "Advanced bookings widget",
    "auto_comply": "AutoComply",
    "premium_channels": "Premium channels",
}
_FOCUS_LABELS = {
    "owner_reporting": "owner reporting",
    "pricing_strategy": "pricing strategy",
    "guest_messaging": "guest messaging",
    "cleaner_workflows": "cleaner workflows",
    "accounting_setup": "accounting setup",
    "booking_website": "a direct booking site",
    "reviews_reputation": "reviews & reputation",
    "channel_mix": "channel mix",
}
_GO_LIVE_LABELS = {
    "asap": "as soon as possible",
    "2-4w": "in 2–4 weeks",
    "1-2m": "in 1–2 months",
    "exploring": "still exploring timing",
}

# Note-derived signals surfaced to the wizard as prefilled_unconfirmed context.
_NOTE_SLOTS = (
    "migration_source",
    "prior_pms_experience",
    "addon_intent",
    "focus_topics",
    "go_live",
    "third_party_tools",
)

_CONTACT_LINE = re.compile(
    r"(?:primary\s+contact|main\s+poc|poc|contact)s?\b[^\n:]*:?\s*\*?\s*([A-Z][a-z]+)",
    re.IGNORECASE,
)


def _first_name(account: SalesAccount) -> str:
    """Best-effort greeting name from the note's contact line; neutral fallback."""
    match = _CONTACT_LINE.search(account.notes or "")
    if match:
        token = match.group(1).strip()
        if token.lower() not in {"main", "primary", "the", "for", "ob"}:
            return token
    head = (account.account_name or "").split()
    if head and head[0][0].isupper() and head[0].isalpha():
        return head[0]
    return "there"


def _source_call_date() -> str:
    return (date.today() - timedelta(days=7)).isoformat()


def build_sf_prefill(account: SalesAccount, meta: dict[str, Any]) -> dict[str, Any]:
    """Map derived metadata onto the wizard's SF_PREFILL shape (real per-account)."""
    profile = meta.get("business_profile", {})
    tools = meta.get("third_party_tools", {}) or {}
    cleaning = tools.get("cleaning") or []
    pricing = tools.get("pms_or_pricing") or []
    channels = [c for c in meta.get("channels", []) if c]
    standard = {"airbnb", "booking", "vrbo", "expedia", "direct"}
    return {
        "business_name": profile.get("business_name", account.account_name),
        "contact_email": profile.get("business_email"),
        "first_name": _first_name(account),
        "listing_count": meta.get("listing_count"),
        "channels": channels,
        "domain_hint": profile.get("domain_hint"),
        "partner_cleaning": cleaning[0] if cleaning else None,
        "partner_pricing": pricing[0] if pricing else None,
        "source_call_date": _source_call_date(),
        "other_channel_names": [c for c in channels if c not in standard],
    }


def build_note_summary(meta: dict[str, Any]) -> list[str]:
    """Browser-safe recap bullets built from extracted enums (no raw note text)."""
    bullets: list[str] = []
    migration = meta.get("migration_source")
    if migration:
        bullets.append(
            f"Coming over from {_MIGRATION_LABELS.get(migration, migration.title())}"
        )
    elif meta.get("prior_pms_experience") == "none_first_time":
        bullets.append("First time on a property-management system")

    addons = meta.get("addon_intent") or []
    if addons:
        labels = [_ADDON_LABELS.get(a, a) for a in addons]
        bullets.append("Interested in " + ", ".join(labels))

    focus = meta.get("focus_topics") or []
    if focus:
        labels = [_FOCUS_LABELS.get(f, f.replace("_", " ")) for f in focus]
        bullets.append("Wants to focus on " + ", ".join(labels))

    tools = meta.get("third_party_tools") or {}
    tool_names = sorted({name for names in tools.values() for name in names})
    if tool_names:
        bullets.append("Already using " + ", ".join(tool_names))

    go_live = meta.get("go_live")
    if go_live:
        bullets.append("Looking to go live " + _GO_LIVE_LABELS.get(go_live, go_live))
    return bullets


def _note_prefill(meta: dict[str, Any]) -> dict[str, Any]:
    return {slot: meta[slot] for slot in _NOTE_SLOTS if slot in meta}


def build_session_context(account: SalesAccount) -> dict[str, Any]:
    """Full payload for GET /api/session/init."""
    meta = derive_sf_demo_metadata(account)
    return {
        "account": account.account_name,
        "csm_name": ONBOARDING_SPECIALIST,
        "sf_prefill": build_sf_prefill(account, meta),
        "ob_context": {
            "account": account.account_name,
            "rep": account.opportunity_owner or None,
            "specialist": ONBOARDING_SPECIALIST,
            "note": {
                "summary_bullets": build_note_summary(meta),
                "present": bool((account.notes or "").strip()),
            },
            "prefill": _note_prefill(meta),
            "flags": {"defer_financials": note_signals_defer_financials(account)},
        },
    }


def list_accounts(query: str, *, limit: int = 25, notes_path: Any = None) -> list[dict[str, Any]]:
    path = notes_path or resolve_notes_path()
    if path is None:
        return []
    hits = search_accounts(path, query, limit=limit)
    return [
        {
            "name": a.account_name,
            "listing_count": a.listing_count,
            "has_note": bool((a.notes or "").strip()),
        }
        for a in hits
    ]


def session_for(account_name: str, *, notes_path: Any = None) -> dict[str, Any] | None:
    path = notes_path or resolve_notes_path()
    if path is None:
        return None
    account = get_account(path, account_name)
    if account is None:
        return None
    return build_session_context(account)
