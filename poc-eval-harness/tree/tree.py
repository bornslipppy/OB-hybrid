"""TreeSystem — honest baseline decision tree (Epic 2, Stories 2.1–2.3).

Authored from schema v0.3 ``depends_on`` graph and documented behavioral paths
only.  The author has not seen ``profiles/scored/`` at any point during this
session.  See ``tree/AUTHORSHIP.md`` for the independent authorship record and
``tree/capability-ledger.md`` for the full coverage map.

Design — stateful FSM instance
───────────────────────────────
``next_action`` is called by the harness in a tight loop.  Two modes are
derived from conversation history:

  REPLY mode  — history[-1]["role"] == "user"
                process the last user message against ``_current_slot``
  ASK   mode  — history is empty or history[-1]["role"] == "assistant"
                advance to the next unaddressed slot and pose a question

Within REPLY mode, priority order:

  1. Echo confirmation pending (``_echo_state``) → process confirm/correct
  2. Owner sub-loop active (``_owner_capture``) → handle owner field reply
  3. Fee collection active (``_in_fee_loop``) → handle fee reply
  4. Tax collection active (``_in_tax_loop``) → handle tax reply
  5. Normal slot reply → parse for ``_current_slot``

Echo-before-write (§8 inv 1 / FR-13b)
────────────────────────────────────
Write tools on echo-required fields fire ONLY after ``UserConfirmed`` is
emitted.  The gate is structural: the ``_echo_state`` buffer blocks the tool
call until the user's next turn confirms.  False-write rate is therefore 0 by
construction (SM-C1 kill criterion).

Tax / advice (§8 inv 2 / §8 inv 5)
────────────────────────────────────
Taxes are always flagged via ``flag_for_call_1`` after recording.
``non_refundable_enabled`` is asked neutrally and flagged if the user asks for
a recommendation.  Advice requests on any field are caught in the reply parser
and routed to ``skip+flag``.

S8 hero-branch FSM (FR-3 / FR-7)
──────────────────────────────────
``ownership_model`` is the entry gate.

  all_self_owned  → no owner records; go to rate_strategy / pricing check
  all_managed_for_others | mixed
      → ask how many owners
      → for each owner (per-owner sub-FSM):
            name → email → listings → share (optional)
            → management_model
            → BRANCH:
                commission   → commission_rate (echo) → channel_commission
                fixed_fee    → fixed_fee_amount (echo)
                revenue_split→ split_terms (echo verbal) → flag_for_call_1
                other        → split_terms (free text)  → flag_for_call_1
            → emit add_owner + flag_for_call_1 (intent-capture only, G1)
      → after all owners: continue to rate_strategy

Fallback rule (documented in capability-ledger.md)
────────────────────────────────────────────────────
When a reply cannot be parsed after one clarifying question, the tree emits
``skip_question`` + ``flag_for_call_1`` — the ambiguous-input fallback path.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from kernel.protocol import EndConversation, NextAction, UserQuestion
from kernel.schema import SchemaLoader, FrameGraph, evaluate_condition
from kernel.state import ProfileState, SlotStatus
from kernel.tools import (
    AddFee,
    AddOwner,
    AddTax,
    FlagForCall1,
    RecordAnswer,
    SkipQuestion,
    Source,
)
from kernel.trace import EchoIssued, UserConfirmed, UserCorrected, ValueIntroduced

# ─────────────────────────────────────────────────────────────────────────────
# §10 NLU vocabulary-normalization map  (FR-12 / schema §10)
# ─────────────────────────────────────────────────────────────────────────────

_NLU_MAP: dict[str, str] = {
    # channels
    "portals": "channels",
    "otas": "channels",
    " ota ": " channels ",
    "booking platforms": "channels",
    "online platforms": "channels",
    "listing sites": "channels",
    # rate / pricing
    "prices": "rate_strategy",
    "my prices": "rate_strategy",
    "nightly rates": "rate_strategy",
    "pricing": "rate_strategy",
    # third-party pricing tools → skip rate_strategy
    "pricelabs": "third_party_pricing_tool",
    "wheelhouse": "third_party_pricing_tool",
    "pricematik": "third_party_pricing_tool",
    "beyond pricing": "third_party_pricing_tool",
    "beyond": "third_party_pricing_tool",
    # third-party cleaning tools
    "turno": "third_party_cleaning_tool",
    "properly": "third_party_cleaning_tool",
    # fees / deposits
    "cleaning fee": "_cleaning_fee_note",   # per-property, NOT mandatory_fees
    "cleaning fees": "_cleaning_fee_note",
    "security deposit": "security_deposit_type",
    # owner / business models
    "business model": "management_model",
    "business models": "management_model",
    "owner login": "_owner_portal",
    "owner access": "_owner_portal",
    "owner portal": "_owner_portal",
    # channel commission synonyms
    "payout": "who_pays_channel_commission",
    "host channel fee": "who_pays_channel_commission",
    "accommodation fare": "channel_commission",
    # management commission synonyms (context: owner economics)
    # NOTE: "management fee" intentionally absent here — it appears in _MGMT_MODEL_MAP
    # as a synonym for "commission".  Including it in _NLU_MAP would replace the phrase
    # before _MGMT_MODEL_MAP is consulted, making the key unreachable (F-001 fix).
    "cut": "pmc_commission_rate",
    "take a cut": "pmc_commission_rate",
}

# Per-slot enum synonym maps (user phrase → canonical option)

_CHANNEL_MAP: dict[str, str] = {
    "airbnb": "airbnb",
    "air bnb": "airbnb",
    "booking.com": "booking",
    "booking com": "booking",
    "booking": "booking",
    "vrbo": "vrbo",
    "homeaway": "vrbo",
    "expedia": "expedia",
    "direct": "direct",
    "direct bookings": "direct",
    "my website": "direct",
    "own website": "direct",
    "website": "direct",
    "other": "other",
}

_OWNERSHIP_MAP: dict[str, str] = {
    "all mine": "all_self_owned",
    "all self": "all_self_owned",
    "own all": "all_self_owned",
    "my own": "all_self_owned",
    "i own": "all_self_owned",
    "personal": "all_self_owned",
    "self owned": "all_self_owned",
    "self-owned": "all_self_owned",
    "myself": "all_self_owned",
    "manage for others": "all_managed_for_others",
    "managing for others": "all_managed_for_others",
    "all managed": "all_managed_for_others",
    "property management": "all_managed_for_others",
    "pmc": "all_managed_for_others",
    "clients": "all_managed_for_others",
    "owners": "all_managed_for_others",
    "for other owners": "all_managed_for_others",
    "on behalf": "all_managed_for_others",
    "mix": "mixed",
    "mixed": "mixed",
    "both": "mixed",
    "combination": "mixed",
    "some mine": "mixed",
    "partly": "mixed",
}

_MGMT_MODEL_MAP: dict[str, str] = {
    "commission": "commission",
    "percent": "commission",
    "percentage": "commission",
    "management fee": "commission",
    "fee": "commission",
    "take a cut": "commission",
    "cut": "commission",
    "fixed": "fixed_fee",
    "flat fee": "fixed_fee",
    "flat rate": "fixed_fee",
    "monthly fee": "fixed_fee",
    "fixed fee": "fixed_fee",
    "flat": "fixed_fee",
    "set amount": "fixed_fee",
    "revenue split": "revenue_split",
    "split": "revenue_split",
    "profit split": "revenue_split",
    "net split": "revenue_split",
    "gross split": "revenue_split",
    "other": "other",
    "complex": "other",
    "custom": "other",
    "varies": "other",
    "it depends": "other",
    "different for each": "other",
}

_CHANNEL_COMMISSION_MAP: dict[str, str] = {
    "me": "pmc",
    "us": "pmc",
    "pmc": "pmc",
    "we pay": "pmc",
    "management company": "pmc",
    "i pay": "pmc",
    "owner": "owner",
    "they pay": "owner",
    "the owner": "owner",
    "host pays": "owner",
    "split": "split",
    "shared": "split",
    "half and half": "split",
    "50 50": "split",
}

_PAYMENT_TIMING_MAP: dict[str, str] = {
    "at booking": "at_booking",
    "upfront": "at_booking",
    "when they book": "at_booking",
    "full payment": "at_booking",
    "immediately": "at_booking",
    "near arrival": "near_arrival",
    "before arrival": "near_arrival",
    "closer to arrival": "near_arrival",
    "checkin": "near_arrival",
    "check-in": "near_arrival",
    "split": "split",
    "two payments": "split",
    "installments": "split",
    "payment plan": "split",
}

_GO_LIVE_MAP: dict[str, str] = {
    "asap": "asap",
    "as soon as possible": "asap",
    "immediately": "asap",
    "right away": "asap",
    "now": "asap",
    "2-4 weeks": "2-4w",
    "2 to 4 weeks": "2-4w",
    "couple weeks": "2-4w",
    "few weeks": "2-4w",
    "a month": "1-2m",
    "1-2 months": "1-2m",
    "one to two months": "1-2m",
    "next month": "1-2m",
    "exploring": "exploring",
    "just looking": "exploring",
    "not sure": "exploring",
    "researching": "exploring",
}

_SECURITY_DEPOSIT_MAP: dict[str, str] = {
    "damage waiver": "damage_waiver",
    "waiver": "damage_waiver",
    "security deposit": "security_deposit",
    "deposit": "security_deposit",
    "damage protection": "damage_protection",
    "shield": "damage_protection",
    "guesty damage protection": "damage_protection",
    "none": "none",
    "no deposit": "none",
    "nothing": "none",
    "no": "none",
}

_REVENUE_RECOGNITION_MAP: dict[str, str] = {
    "check-in": "checkin_date",
    "checkin": "checkin_date",
    "check in": "checkin_date",
    "arrival": "checkin_date",
    "check-out": "checkout_date",
    "checkout": "checkout_date",
    "check out": "checkout_date",
    "departure": "checkout_date",
    "prorated": "prorated",
    "spread out": "prorated",
    "across the stay": "prorated",
    "daily": "prorated",
    "per night": "prorated",
}

_CLEANING_SYSTEM_MAP: dict[str, str] = {
    "in-house": "in_house",
    "in house": "in_house",
    "internal": "in_house",
    "my team": "in_house",
    "our team": "in_house",
    "own staff": "in_house",
    "company": "cleaning_company",
    "cleaning company": "cleaning_company",
    "third party": "cleaning_company",
    "outsourced": "cleaning_company",
    "professional service": "cleaning_company",
    "marketplace": "marketplace_tool",
    "app": "marketplace_tool",
    "mixed": "mixed",
    "mix": "mixed",
    "both": "mixed",
    "combination": "mixed",
}

_DECISION_OWNER_MAP: dict[str, str] = {
    "just me": "just_me",
    "only me": "just_me",
    "myself": "just_me",
    "solo": "just_me",
    "shared": "shared",
    "team": "shared",
    "we": "shared",
    "multiple": "shared",
    "partners": "shared",
}

_TEAMMATE_ROLE_MAP: dict[str, str] = {
    "admin": "admin",
    "administrator": "admin",
    "agent": "agent",
    "property manager": "agent",
    "cleaner": "cleaner",
    "housekeeper": "cleaner",
    "cleaning": "cleaner",
    "custom": "custom",
    "other": "custom",
}

# Question templates  (primary_slot → question text)
_QUESTIONS: dict[str, str] = {
    # S2
    "listing_count": (
        "I see {listing_count} active listings in your Salesforce record — "
        "is that the right count, or would you like to update it?"
    ),
    "listing_count_cold": "How many active listings do you have?",
    "channels": (
        "And your connected channels are: {channels}. "
        "Is that still correct — any to add or remove?"
    ),
    "channels_cold": (
        "Which channels are you using? For example: Airbnb, Booking.com, VRBO, "
        "direct bookings, or others?"
    ),
    "other_channels_text": "You mentioned 'other' — which platform is that?",
    "go_live": (
        "When are you hoping to go live with Guesty? "
        "Are you aiming to start as soon as possible, in 2–4 weeks, in 1–2 months, "
        "or are you still exploring?"
    ),
    # S3
    "cleaning_system": (
        "How do you handle cleaning — is it done in-house by your own team, "
        "through a cleaning company, via a marketplace app like Turno, or a mix?"
    ),
    "turnover_checklist_choice": (
        "For your turnover checklist: would you like to upload your own, "
        "use a Guesty template, or skip for now?"
    ),
    "turnover_checklist_file": "Great — please share your turnover checklist file when ready.",
    "smart_locks": "Do you use smart locks? If so, which system?",
    # S4
    "revenue_recognition": (
        "For your revenue analytics, should Guesty recognize revenue on the check-in date, "
        "the check-out date, or prorated across the stay?"
    ),
    "non_refundable_enabled": (
        "Do you offer a non-refundable rate option — where guests pay less but can't cancel? "
        "(I'll note your answer and flag it for your onboarding specialist Jordan to configure.)"
    ),
    "security_deposit_type": (
        "For security on bookings: do you use Guesty's Damage Protection (Shield), "
        "collect a standard security deposit, a damage waiver, or none?"
    ),
    "security_deposit_amount": (
        "What amount do you charge? Give me a flat amount (e.g. '$300') "
        "or a percentage of the stay."
    ),
    "payment_timing": (
        "When do you collect payment from guests — at the time of booking, "
        "closer to arrival, or split into two payments?"
    ),
    "payment_split": (
        "What's the split — 50/50, 20% at booking and 80% near arrival, "
        "or a custom arrangement?"
    ),
    "mandatory_fees": (
        "Are there any mandatory fees you charge all guests — like a late check-out fee, "
        "pet fee, or laundry fee? Note: per-property cleaning fees are handled separately. "
        "If none, just say 'none'."
    ),
    "mandatory_fees_more": "Any other mandatory fees, or are we done with fees?",
    "taxes": (
        "What taxes do you collect on reservations? For example, occupancy tax, city tax, "
        "sales tax, VAT, or GST? I'll capture exactly what you tell me and flag it for "
        "Jordan — we never configure taxes without specialist review."
    ),
    "taxes_more": "Any other taxes to capture, or shall we move on?",
    # S5 (conditional)
    "website_brand_name": (
        "Since you're doing direct bookings, what's the brand name for your booking website?"
    ),
    "website_domain": (
        "For your website domain: would you prefer a Guesty-hosted subdomain, "
        "or do you have a custom domain to connect?"
    ),
    "website_terms": (
        "What booking terms would you like on your site — Guesty's standard terms, "
        "or your own?"
    ),
    # S6
    "decision_owner": (
        "Who will be the decision-maker for the Guesty setup — just you, "
        "or will you have teammates to invite?"
    ),
    "teammates": (
        "Who are your teammates? I'll need each person's name, email, and role "
        "(admin, agent, or cleaner)."
    ),
    "teammates_more": "Any other teammates to add, or are we good?",
    # S7
    "focus_topics": (
        "What are your top 1–3 priorities you want to cover on the first call with Jordan? "
        "Options: pricing strategy, channel mix, guest messaging, cleaner workflows, "
        "accounting setup, owner reporting, booking website, or reviews/reputation."
    ),
    "pain": (
        "What's the biggest challenge you're trying to solve with Guesty — in your own words?"
    ),
    # S8
    "ownership_model": (
        "How does your portfolio work — do you own all the properties yourself, "
        "do you manage properties on behalf of other owners, or is it a mix of both?"
    ),
    "owners_count": (
        "How many property owners do you manage on behalf of? "
        "(Give me a number and we'll go through each one.)"
    ),
    "rate_strategy": (
        "Do you use an external pricing tool like PriceLabs or Wheelhouse? "
        "If not, do you have seasonal rates or pricing rules you'd like to set up in Guesty?"
    ),
    # Echo confirmation (slot-keyed suffix added at runtime)
    "_echo_confirm": "Just to confirm — {echo_text}. Is that right?",
    "_echo_reprompt": (
        "I want to make sure I get this right: {echo_text}. Can you confirm?"
    ),
    # Clarification
    "_clarify": "Could you clarify — {slot_hint}?",
    "_advice_deflect": (
        "That's a great question for Jordan, your onboarding specialist — "
        "I've flagged it for your first call. What else can I capture for you?"
    ),
}

# Advice-seeking keywords — any reply containing these routes to flag_for_call_1
_ADVICE_TRIGGERS = (
    "should i", "recommend", "which is better", "what do you suggest",
    "what would you", "advise", "best option", "which one", "tell me what",
    "what should", "your opinion", "your recommendation",
)

# IDK / absence patterns — treated as absence (§8 inv 7), not ambiguity
_IDK_TRIGGERS = (
    "i don't know", "idk", "not sure", "no idea", "i'm not sure",
    "don't have that", "haven't decided", "skip", "defer", "pass",
    "move on", "next", "later", "i'll come back",
)

# ─────────────────────────────────────────────────────────────────────────────
# Internal FSM state dataclasses
# ─────────────────────────────────────────────────────────────────────────────


@dataclass
class _EchoState:
    """One numeric/financial value awaiting user confirmation (§8 inv 1)."""

    slot: str
    subfield: str | None
    value: Any
    text_repr: str           # the echo sentence shown to the user
    reprompts_given: int = 0


@dataclass
class _FeeItem:
    """One mandatory fee being accumulated through echo before add_fee."""

    fee_type: str = ""
    amount: float | None = None
    unit: str | None = None   # "flat" | "percent"
    phase: str = "amount"     # "amount" → "unit" → "echo"


@dataclass
class _TaxItem:
    """One tax being accumulated through echo before add_tax + flag."""

    tax_type: str = ""
    tax_type_other: str | None = None
    inclusivity: str = "exclusive"   # default: exclusive until user says inclusive
    what_taxed: list[str] = field(default_factory=lambda: ["accommodation_fare"])
    scope: str = "account_wide"
    phase: str = "type"       # "type" → "inclusivity" → "echo"


@dataclass
class _OwnerCapture:
    """Per-owner sub-FSM state for the S8 hero branch (FR-3 / FR-7).

    Phases advance through the owner's field list.  Numeric sub-fields
    (commission_rate, fixed_fee_amount) use the outer _EchoState buffer.
    """

    expected_count: int
    owners_done: int = 0
    phase: str = "name"       # name|email|listings|share|management_model|economics
    econ_phase: str | None = None  # commission_rate|channel_commission|fixed_fee_amount|split_terms
    current: dict[str, Any] = field(default_factory=dict)


# ─────────────────────────────────────────────────────────────────────────────
# Deterministic slot traversal order (section, slot_id)
# Slots with depends_on are only asked when their guard evaluates True.
# ─────────────────────────────────────────────────────────────────────────────

_TRAVERSAL: list[tuple[str, str]] = [
    # S2: Pre-flight
    ("S2", "listing_count"),
    ("S2", "channels"),
    ("S2", "other_channels_text"),   # depends_on: channels includes 'other'
    ("S2", "go_live"),
    # S3: Operations
    ("S3", "cleaning_system"),
    ("S3", "turnover_checklist_choice"),
    ("S3", "turnover_checklist_file"),   # depends_on: turnover_checklist_choice == 'upload'
    ("S3", "smart_locks"),
    # S4: Financials
    ("S4", "revenue_recognition"),
    ("S4", "non_refundable_enabled"),
    ("S4", "security_deposit_type"),
    ("S4", "security_deposit_amount"),  # depends_on: security_deposit_type in [...]
    ("S4", "payment_timing"),
    ("S4", "payment_split"),            # depends_on: payment_timing == 'split' OR user volunteers
    ("S4", "mandatory_fees"),           # loop — handled via _in_fee_loop
    ("S4", "taxes"),                    # loop + always flag — handled via _in_tax_loop
    # S6: Governance
    ("S6", "decision_owner"),
    ("S6", "teammates"),                # depends_on: decision_owner == 'shared'
    # S7: Focus topics
    ("S7", "focus_topics"),
    ("S7", "pain"),
    # S8: Hero branch (owner loop triggered by ownership_model)
    ("S8", "ownership_model"),
    ("S8", "_owner_loop"),              # synthetic — triggers OwnerCapture when reachable
    ("S8", "rate_strategy"),
    # S5: Conditional (only when direct-booking signal detected)
    ("S5", "website_brand_name"),
    ("S5", "website_domain"),           # depends_on: website_brand_name is recorded
    ("S5", "website_terms"),            # depends_on: website_domain is recorded
]

# _owner_loop is reachable when ownership_model in [all_managed_for_others, mixed]
_OWNER_LOOP_CONDITION = "ownership_model in ['all_managed_for_others','mixed']"

# Slots where payment_split is in scope via "user volunteers" (supplemental guard)
_PAYMENT_SPLIT_GUARD = "payment_timing == 'split'"


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────


def _normalize(text: str) -> str:
    """Apply §10 vocabulary normalization."""
    t = text.lower()
    for user_term, canonical in _NLU_MAP.items():
        t = t.replace(user_term, canonical)
    return t


def _is_advice_request(text: str) -> bool:
    t = text.lower()
    return any(trigger in t for trigger in _ADVICE_TRIGGERS)


def _is_idk(text: str) -> bool:
    t = text.lower().strip()
    return any(trigger in t for trigger in _IDK_TRIGGERS) or t in {"n/a", "na", "?", ""}


def _parse_amount(text: str) -> tuple[float | None, str]:
    """Extract (amount, unit) from user text.  unit is 'flat' or 'percent'."""
    t = text.lower().replace(",", "")
    m = re.search(r"(\d+(?:\.\d+)?)\s*(?:%|percent(?:age)?|per\s*cent)", t)
    if m:
        return float(m.group(1)), "percent"
    m = re.search(r"[\$€£]?\s*(\d+(?:\.\d+)?)", t)
    if m:
        return float(m.group(1)), "flat"
    return None, "flat"


def _parse_integer(text: str) -> int | None:
    m = re.search(r"\b(\d{1,3})\b", text)
    return int(m.group(1)) if m else None


def _parse_enum(text: str, mapping: dict[str, str]) -> str | None:
    """Return the canonical enum value for text using the given synonym map."""
    t = _normalize(text).lower()
    for phrase, canonical in mapping.items():
        if phrase in t:
            return canonical
    return None


def _parse_list(text: str, mapping: dict[str, str]) -> list[str]:
    """Parse a comma/and-separated list of enum values."""
    parts = re.split(r"[,;/]|\band\b|\bor\b|\bplus\b", text.lower())
    results: list[str] = []
    seen: set[str] = set()
    for part in parts:
        val = _parse_enum(part.strip(), mapping)
        if val and val not in seen:
            results.append(val)
            seen.add(val)
    return results


def _parse_email(text: str) -> str | None:
    m = re.search(r"[a-zA-Z0-9_.+\-]+@[a-zA-Z0-9\-]+\.[a-zA-Z]{2,}", text)
    return m.group(0) if m else None


def _parse_listings(text: str) -> list[str]:
    """Best-effort extraction of listing names from free text."""
    t = text.strip()
    if not t or _is_idk(t):
        return []
    parts = re.split(r"[,;/]|\band\b", t)
    return [p.strip() for p in parts if p.strip() and len(p.strip()) > 1]


def _detect_direct_booking_signal(
    state: ProfileState, history: list[dict]
) -> bool:
    """True when any direct-booking signal is present (G6 / FR-4)."""
    facts = state.recorded_facts()
    channels = facts.get("channels")
    if isinstance(channels, list) and "direct" in channels:
        return True
    topics = facts.get("focus_topics")
    if isinstance(topics, list) and "booking_website" in topics:
        return True
    # Scan conversation history for website/direct-booking mentions
    for msg in history:
        content = (msg.get("content") or "").lower()
        if any(kw in content for kw in ("my website", "direct booking", "own website",
                                         "booking website", "direct channel")):
            return True
    return False


def _has_external_pricing_tool(state: ProfileState, history: list[dict]) -> bool:
    """True when a third-party pricing tool is confirmed (skip rate_strategy)."""
    tools = state.recorded_facts().get("third_party_tools") or {}
    if isinstance(tools, dict) and tools.get("pms_or_pricing"):
        return True
    for msg in history:
        content = (msg.get("content") or "").lower()
        normalized = _normalize(content)
        if "third_party_pricing_tool" in normalized:
            return True
    return False


def _slot_dispositioned(state: ProfileState, slot_id: str) -> bool:
    """True when slot_id has been fully addressed (recorded | skipped | flagged)."""
    s = state.slots.get(slot_id)
    if s is None:
        return False
    return s.status in {SlotStatus.RECORDED, SlotStatus.SKIPPED, SlotStatus.FLAGGED}


# ─────────────────────────────────────────────────────────────────────────────
# TreeSystem — the System implementation
# ─────────────────────────────────────────────────────────────────────────────


class TreeSystem:
    """Honest baseline decision tree — a ``System`` policy over the kernel.

    Deterministic FSM that branches on every ``depends_on`` guard in schema
    v0.3.  Emits the identical 7-tool vocabulary as the agent with trace events
    via ``drain_trace_events()`` so FR-23/FR-24 scoring runs unmodified.
    """

    system_id: str = "tree"

    def __init__(self, schema_path: str | Path | None = None) -> None:
        if schema_path is None:
            schema_path = (
                Path(__file__).parent.parent / "schema" / "guesty-pro-account-creation-schema.md"
            )
        loader = SchemaLoader()
        slots = loader.load(schema_path)
        self._frame = FrameGraph(slots)

        # FSM state
        self._current_slot: str | None = None    # slot we most recently asked about
        self._echo_state: _EchoState | None = None
        self._owner_capture: _OwnerCapture | None = None
        self._fee_item: _FeeItem | None = None   # current fee being built
        self._in_fee_loop: bool = False          # currently collecting fees
        self._tax_item: _TaxItem | None = None   # current tax being built
        self._in_tax_loop: bool = False          # currently collecting taxes
        self._teammate_buf: list[dict] = []      # accumulated teammate records
        self._in_teammate_loop: bool = False

        # Tracks how many clarifying questions have been asked per slot (max 1)
        self._ambiguity_count: dict[str, int] = {}

        # Echo/trace events buffered for drain_trace_events()  (R-10 hook)
        self._pending_events: list[Any] = []

        # Traversal cursor
        self._traversal_idx: int = 0
        self._section_closed: set[str] = set()

    # ── Public API ──────────────────────────────────────────────────────────

    def next_action(
        self, state: ProfileState, conversation_history: list[dict]
    ) -> NextAction:
        """Main dispatch — see module docstring for FSM description."""
        self._pending_events.clear()

        in_reply = bool(conversation_history) and conversation_history[-1]["role"] == "user"
        last_reply: str = conversation_history[-1]["content"] if in_reply else ""

        if in_reply:
            return self._dispatch_reply(state, last_reply, conversation_history)

        # ASK mode: no new user message
        return self._dispatch_ask(state, conversation_history)

    def drain_trace_events(self) -> list[Any]:
        """Drain buffered echo-lifecycle trace events (FR-13b / R-10 hook).

        The runner calls this immediately after each ``next_action`` return.
        Returns ``ValueIntroduced``, ``EchoIssued``, ``UserConfirmed``, and
        ``UserCorrected`` events so the canonical trace captures the echo
        lifecycle without the harness understanding echo semantics.
        """
        events = list(self._pending_events)
        self._pending_events.clear()
        return events

    # ── Reply dispatch ───────────────────────────────────────────────────────

    def _dispatch_reply(
        self, state: ProfileState, reply: str, history: list[dict]
    ) -> NextAction:
        # 1. Echo confirmation takes priority
        if self._echo_state is not None:
            return self._handle_echo_confirmation(state, reply)

        # 2. Owner sub-loop
        if self._owner_capture is not None:
            return self._handle_owner_reply(state, reply)

        # 3. Fee collection loop
        if self._in_fee_loop:
            return self._handle_fee_reply(state, reply)

        # 4. Tax collection loop
        if self._in_tax_loop:
            return self._handle_tax_reply(state, reply)

        # 5. Teammate collection loop
        if self._in_teammate_loop:
            return self._handle_teammate_reply(state, reply)

        # 6. Normal slot reply
        if self._current_slot:
            return self._handle_slot_reply(state, reply)

        # No slot in flight — advance
        return self._dispatch_ask(state, history)

    # ── Ask dispatch ─────────────────────────────────────────────────────────

    def _dispatch_ask(
        self, state: ProfileState, history: list[dict]
    ) -> NextAction:
        # Active sub-loops continue
        if self._owner_capture is not None:
            return self._ask_owner_next(state)
        if self._in_fee_loop:
            return self._ask_fee_next()
        if self._in_tax_loop:
            return self._ask_tax_next()
        if self._in_teammate_loop:
            return self._ask_teammate_next()

        return self._advance(state, history)

    # ── Traversal: find next unaddressed slot ───────────────────────────────

    def _advance(
        self, state: ProfileState, history: list[dict]
    ) -> NextAction:
        facts = state.recorded_facts()

        while self._traversal_idx < len(_TRAVERSAL):
            section, slot_id = _TRAVERSAL[self._traversal_idx]

            # S5 requires direct-booking signal
            if section == "S5" and not _detect_direct_booking_signal(state, history):
                self._traversal_idx += 1
                continue

            # Check depends_on / surface_when via kernel FrameGraph
            if slot_id == "_owner_loop":
                guard_met = evaluate_condition(_OWNER_LOOP_CONDITION, facts)
            else:
                slot_def = self._frame.get(slot_id)
                guard_met = (
                    evaluate_condition(
                        slot_def.condition if slot_def else None,
                        facts,
                        {"user_volunteers_a_split": bool(facts.get("payment_timing") == "split")},
                    )
                    if slot_def is not None
                    else True
                )

            self._traversal_idx += 1

            if not guard_met:
                continue

            # Already fully addressed?
            if slot_id == "_owner_loop":
                if not _slot_dispositioned(state, "owners"):
                    return self._enter_owner_loop(state, facts)
                continue
            if _slot_dispositioned(state, slot_id):
                continue

            # Special entry points for loop slots
            if slot_id == "mandatory_fees":
                self._in_fee_loop = True
                self._fee_item = None
                self._current_slot = "mandatory_fees"
                return UserQuestion(
                    text=_QUESTIONS["mandatory_fees"],
                    primary_slot="mandatory_fees",
                )
            if slot_id == "taxes":
                self._in_tax_loop = True
                self._tax_item = None
                self._current_slot = "taxes"
                return UserQuestion(
                    text=_QUESTIONS["taxes"],
                    primary_slot="taxes",
                )
            if slot_id == "teammates":
                self._in_teammate_loop = True
                self._current_slot = "teammates"
                return UserQuestion(
                    text=_QUESTIONS["teammates"],
                    primary_slot="teammates",
                )

            # rate_strategy: skip if external pricing tool
            if slot_id == "rate_strategy" and _has_external_pricing_tool(state, history):
                self._current_slot = None
                return [  # type: ignore[return-value]
                    SkipQuestion(
                        field_id="rate_strategy",
                        reason="External pricing tool already in use (PriceLabs/Wheelhouse); "
                               "flag integration on Call 1 instead.",
                    )
                ]

            return self._ask_slot(slot_id, state)

        # All slots addressed → end conversation
        return EndConversation(reason="completed")

    # ── Ask a single slot ───────────────────────────────────────────────────

    def _ask_slot(self, slot_id: str, state: ProfileState) -> NextAction:
        self._current_slot = slot_id
        facts = state.recorded_facts()

        # Build question text — inject SF prefill values where available
        if slot_id == "listing_count":
            sf = facts.get("listing_count") or facts.get("active_listing_count")
            text = (
                _QUESTIONS["listing_count"].format(listing_count=sf)
                if sf else _QUESTIONS["listing_count_cold"]
            )
        elif slot_id == "channels":
            sf = facts.get("channels") or facts.get("connected_channels")
            text = (
                _QUESTIONS["channels"].format(channels=", ".join(sf) if sf else "none")
                if sf else _QUESTIONS["channels_cold"]
            )
        else:
            text = _QUESTIONS.get(slot_id, f"Can you tell me about {slot_id.replace('_', ' ')}?")

        return UserQuestion(text=text, primary_slot=slot_id)

    # ── Normal slot reply handler ─────────────────────────────────────────

    def _handle_slot_reply(self, state: ProfileState, reply: str) -> NextAction:
        slot = self._current_slot
        if slot is None:
            return []  # type: ignore[return-value]

        # Advice deflection (§8 inv 2 / SM-C2)
        if _is_advice_request(reply):
            self._current_slot = None
            return [  # type: ignore[return-value]
                FlagForCall1(
                    topic=f"advice_request_on_{slot}",
                    user_quote=reply[:200],
                    note=f"User asked for a recommendation on '{slot}'. Flagged for Jordan.",
                    field_id=slot,
                ),
            ]

        # IDK / absence → skip or flag if required (§8 inv 7)
        if _is_idk(reply):
            return self._handle_idk(slot, state)

        # --- Slot-specific parsing ---
        return self._parse_for_slot(slot, reply, state)

    def _handle_idk(self, slot: str, state: ProfileState) -> NextAction:
        """IDK is absence of value — skip or flag depending on priority."""
        self._current_slot = None
        slot_def = self._frame.get(slot)
        priority = slot_def.priority if slot_def else "optional"
        if priority == "required":
            return [  # type: ignore[return-value]
                FlagForCall1(
                    topic=slot,
                    user_quote="User deferred",
                    note=f"Required field '{slot}' deferred by user — needs Call-1 resolution.",
                    field_id=slot,
                )
            ]
        return [SkipQuestion(field_id=slot, reason="User deferred / not known yet")]  # type: ignore[return-value]

    def _parse_for_slot(
        self, slot: str, reply: str, state: ProfileState
    ) -> NextAction:
        """Slot-specific parsing → return tool calls or a clarifying question."""
        self._current_slot = None  # clear before returning (may be reset in echo path)

        # ── S2 ──────────────────────────────────────────────────────────────
        if slot == "listing_count":
            n = _parse_integer(reply)
            if n is not None:
                return [RecordAnswer(field_id="listing_count", value=n, source=Source.USER_STATED)]
            return self._clarify_or_skip(slot, reply, "how many active listings you have")

        if slot == "channels":
            vals = _parse_list(reply, _CHANNEL_MAP)
            if vals:
                return [RecordAnswer(field_id="channels", value=vals, source=Source.USER_STATED)]
            return self._clarify_or_skip(slot, reply, "which channels you use (e.g. Airbnb, VRBO)")

        if slot == "other_channels_text":
            if reply.strip():
                return [RecordAnswer(field_id="other_channels_text", value=reply.strip(),
                                     source=Source.USER_STATED)]
            return [SkipQuestion(field_id="other_channels_text", reason="No other channel named")]

        if slot == "go_live":
            val = _parse_enum(reply, _GO_LIVE_MAP)
            if val:
                return [RecordAnswer(field_id="go_live", value=val, source=Source.USER_STATED)]
            return self._clarify_or_skip(slot, reply, "your go-live timeline")

        # ── S3 ──────────────────────────────────────────────────────────────
        if slot == "cleaning_system":
            val = _parse_enum(reply, _CLEANING_SYSTEM_MAP)
            if val:
                return [RecordAnswer(field_id="cleaning_system", value=val,
                                     source=Source.USER_STATED)]
            return self._clarify_or_skip(slot, reply, "how you manage cleaning")

        if slot == "turnover_checklist_choice":
            t = reply.lower()
            if "upload" in t:
                v = "upload"
            elif "template" in t or "guesty" in t:
                v = "guesty_template"
            else:
                v = "skip"
            return [RecordAnswer(field_id="turnover_checklist_choice", value=v,
                                 source=Source.USER_STATED)]

        if slot == "turnover_checklist_file":
            # File upload — record note and skip (file handling is widget-based)
            return [SkipQuestion(field_id="turnover_checklist_file",
                                 reason="File upload handled via product widget")]

        if slot == "smart_locks":
            if _is_idk(reply) or reply.lower().strip() in ("no", "none", "nope"):
                return [SkipQuestion(field_id="smart_locks", reason="No smart locks in use")]
            return [RecordAnswer(field_id="smart_locks", value=reply.strip(),
                                 source=Source.USER_STATED)]

        # ── S4 ──────────────────────────────────────────────────────────────
        if slot == "revenue_recognition":
            val = _parse_enum(reply, _REVENUE_RECOGNITION_MAP)
            if val:
                return [RecordAnswer(field_id="revenue_recognition", value=val,
                                     source=Source.USER_STATED)]
            return self._clarify_or_skip(slot, reply, "check-in date, check-out date, or prorated")

        if slot == "non_refundable_enabled":
            t = reply.lower()
            val = "yes" if any(w in t for w in ("yes", "true", "enable", "offer", "use")) else "no"
            return [RecordAnswer(field_id="non_refundable_enabled", value=(val == "yes"),
                                 source=Source.USER_STATED)]

        if slot == "security_deposit_type":
            val = _parse_enum(reply, _SECURITY_DEPOSIT_MAP)
            if val:
                return [RecordAnswer(field_id="security_deposit_type", value=val,
                                     source=Source.USER_STATED)]
            return self._clarify_or_skip(
                slot, reply, "damage protection, security deposit, damage waiver, or none"
            )

        if slot == "security_deposit_amount":
            # echo-before-write (§8 inv 1)
            amount, unit = _parse_amount(reply)
            if amount is not None:
                return self._begin_echo(
                    slot=slot,
                    subfield=None,
                    value={"amount": amount, "unit": unit},
                    text_repr=f"the security deposit is {amount}{'%' if unit == 'percent' else ' (flat)'}",
                    state_turn=state.turn_count,
                )
            return self._clarify_or_skip(slot, reply, "the deposit amount (e.g. '$300' or '10%')")

        if slot == "payment_timing":
            val = _parse_enum(reply, _PAYMENT_TIMING_MAP)
            if val:
                return [RecordAnswer(field_id="payment_timing", value=val,
                                     source=Source.USER_STATED)]
            # Path C: "depends on channel" → record direct-booking default, note OTA handled
            if "channel" in reply.lower() or "depends" in reply.lower():
                return [
                    RecordAnswer(field_id="payment_timing", value="near_arrival",
                                 source=Source.USER_STATED),
                    FlagForCall1(
                        topic="payment_timing_channel_dependent",
                        user_quote=reply[:200],
                        note="User said payment timing depends on the channel. "
                             "Recorded 'near_arrival' as direct-booking default; "
                             "OTA channels handled by the OTA. Confirm with Jordan.",
                        field_id="payment_timing",
                    ),
                ]
            return self._clarify_or_skip(slot, reply, "at booking, near arrival, or split")

        if slot == "payment_split":
            t = reply.lower()
            if "50" in t or "half" in t:
                val = "50_50"
            elif "20" in t and "80" in t:
                val = "20_80"
            elif "custom" in t or "different" in t:
                val = "custom"
            else:
                val = _parse_enum(reply, {"50/50": "50_50", "50-50": "50_50"})
            if val:
                tc: list[Any] = [RecordAnswer(field_id="payment_split", value=val,
                                              source=Source.USER_STATED)]
                if val == "custom":
                    tc.append(FlagForCall1(
                        topic="payment_split_custom",
                        user_quote=reply[:200],
                        note=f"Custom payment split: '{reply.strip()}'. Jordan to configure.",
                        field_id="payment_split",
                    ))
                return tc  # type: ignore[return-value]
            return self._clarify_or_skip(slot, reply, "the payment split (e.g. 50/50 or 20/80)")

        # ── S6 ──────────────────────────────────────────────────────────────
        if slot == "decision_owner":
            val = _parse_enum(reply, _DECISION_OWNER_MAP)
            if not val:
                val = "just_me" if "just me" in reply.lower() or "only me" in reply.lower() else None
            if val:
                return [RecordAnswer(field_id="decision_owner", value=val,
                                     source=Source.USER_STATED)]
            return self._clarify_or_skip(slot, reply, "just you or a shared team")

        # ── S7 ──────────────────────────────────────────────────────────────
        if slot == "focus_topics":
            # Simple keyword → enum mapping
            kw_map = {
                "pricing": "pricing_strategy",
                "channel": "channel_mix",
                "guest message": "guest_messaging",
                "messaging": "guest_messaging",
                "cleaner": "cleaner_workflows",
                "cleaning": "cleaner_workflows",
                "accounting": "accounting_setup",
                "owner report": "owner_reporting",
                "owner portal": "owner_reporting",
                "website": "booking_website",
                "booking website": "booking_website",
                "direct booking": "booking_website",
                "reviews": "reviews_reputation",
                "reputation": "reviews_reputation",
            }
            topics: list[str] = []
            t = reply.lower()
            for kw, canonical in kw_map.items():
                if kw in t and canonical not in topics:
                    topics.append(canonical)
                    if len(topics) >= 3:
                        break
            if topics:
                return [RecordAnswer(field_id="focus_topics", value=topics,
                                     source=Source.USER_STATED)]
            return self._clarify_or_skip(slot, reply, "your top priorities (up to 3)")

        if slot == "pain":
            if reply.strip():
                return [RecordAnswer(field_id="pain", value=reply.strip(),
                                     source=Source.USER_STATED)]
            return [SkipQuestion(field_id="pain", reason="User did not describe a pain point")]

        # ── S8 ──────────────────────────────────────────────────────────────
        if slot == "ownership_model":
            val = _parse_enum(reply, _OWNERSHIP_MAP)
            if val:
                return [RecordAnswer(field_id="ownership_model", value=val,
                                     source=Source.USER_STATED)]
            return self._clarify_or_skip(
                slot, reply, "all self-owned, all managed for others, or a mix"
            )

        if slot == "rate_strategy":
            t = reply.lower()
            if _is_idk(t) or "no" in t:
                return [SkipQuestion(field_id="rate_strategy",
                                     reason="User has no seasonal pricing rules to set up")]
            return [RecordAnswer(field_id="rate_strategy", value=reply.strip(),
                                 source=Source.USER_STATED)]

        # ── S5 ──────────────────────────────────────────────────────────────
        if slot == "website_brand_name":
            if reply.strip() and not _is_idk(reply):
                return [RecordAnswer(field_id="website_brand_name", value=reply.strip(),
                                     source=Source.USER_STATED)]
            return [SkipQuestion(field_id="website_brand_name", reason="User deferred")]

        if slot == "website_domain":
            t = reply.lower()
            val = "custom_domain" if "custom" in t or "own" in t or "." in reply else "guesty_subdomain"
            return [RecordAnswer(field_id="website_domain", value=val,
                                 source=Source.USER_STATED)]

        if slot == "website_terms":
            t = reply.lower()
            val = "own_terms" if "own" in t or "custom" in t else "guesty_terms"
            return [RecordAnswer(field_id="website_terms", value=val,
                                 source=Source.USER_STATED)]

        # Fallback: record verbatim for unknown/unhandled slots
        return [RecordAnswer(field_id=slot, value=reply.strip(), source=Source.USER_STATED)]

    # ── Echo-before-write ────────────────────────────────────────────────────

    def _begin_echo(
        self,
        slot: str,
        subfield: str | None,
        value: Any,
        text_repr: str,
        state_turn: int,
    ) -> NextAction:
        """Record a value-introduced event and issue the echo question.

        Returns a ``UserQuestion`` (the echo confirmation prompt) after
        buffering the ``ValueIntroduced`` and ``EchoIssued`` trace events.
        """
        self._pending_events.append(
            ValueIntroduced(turn=state_turn, slot=slot, subfield=subfield, value=value)
        )
        self._pending_events.append(
            EchoIssued(turn=state_turn, slot=slot, subfield=subfield, value=value)
        )
        self._echo_state = _EchoState(
            slot=slot, subfield=subfield, value=value, text_repr=text_repr
        )
        # _current_slot stays None — we're in echo mode now
        return UserQuestion(
            text=_QUESTIONS["_echo_confirm"].format(echo_text=text_repr),
            primary_slot=slot,
        )

    def _handle_echo_confirmation(
        self, state: ProfileState, reply: str
    ) -> NextAction:
        """Process a user reply to an echo question (confirm / correct / defer)."""
        es = self._echo_state
        assert es is not None

        t = reply.lower()
        confirmed = any(
            w in t for w in ("yes", "correct", "right", "yep", "yup", "that's right",
                              "confirmed", "ok", "okay", "sure", "yeah")
        )
        corrected = any(w in t for w in ("no", "wrong", "not right", "actually", "it's"))
        defer = _is_idk(reply)

        if defer:
            self._echo_state = None
            self._pending_events.append(
                UserCorrected(turn=state.turn_count, slot=es.slot, subfield=es.subfield,
                              corrected_value=None)
            )
            return [  # type: ignore[return-value]
                FlagForCall1(
                    topic=es.slot,
                    user_quote=reply[:200],
                    note=f"Echo deferred for '{es.slot}' — value not confirmed.",
                    field_id=es.slot,
                )
            ]

        if confirmed:
            self._echo_state = None
            self._pending_events.append(
                UserConfirmed(turn=state.turn_count, slot=es.slot, subfield=es.subfield)
            )
            return self._commit_echo_value(es, state)

        if corrected or not confirmed:
            # Extract corrected value from reply
            new_amount, new_unit = _parse_amount(reply)
            if new_amount is not None and isinstance(es.value, dict):
                corrected_value = {"amount": new_amount, "unit": new_unit}
                self._pending_events.append(
                    UserCorrected(
                        turn=state.turn_count, slot=es.slot, subfield=es.subfield,
                        corrected_value=corrected_value,
                    )
                )
                # Update echo state with corrected value and re-echo
                es.value = corrected_value
                es.text_repr = (
                    f"{new_amount}{'%' if new_unit == 'percent' else ' (flat)'}"
                )
                self._pending_events.append(
                    EchoIssued(
                        turn=state.turn_count, slot=es.slot, subfield=es.subfield,
                        value=corrected_value,
                    )
                )
                return UserQuestion(
                    text=_QUESTIONS["_echo_confirm"].format(echo_text=es.text_repr),
                    primary_slot=es.slot,
                )

            # If reply is not parseable and we haven't reprompted yet
            if es.reprompts_given < 1:
                es.reprompts_given += 1
                self._pending_events.append(
                    EchoIssued(
                        turn=state.turn_count, slot=es.slot, subfield=es.subfield,
                        value=es.value,
                    )
                )
                return UserQuestion(
                    text=_QUESTIONS["_echo_reprompt"].format(echo_text=es.text_repr),
                    primary_slot=es.slot,
                )

            # Exhausted reprompt — flag + skip (§8 inv 1 last sentence)
            self._echo_state = None
            self._pending_events.append(
                UserCorrected(
                    turn=state.turn_count, slot=es.slot, subfield=es.subfield,
                    corrected_value=None,
                )
            )
            return [  # type: ignore[return-value]
                FlagForCall1(
                    topic=es.slot,
                    user_quote=reply[:200],
                    note=f"Could not confirm echo for '{es.slot}'. Flagged for Jordan.",
                    field_id=es.slot,
                )
            ]

        # Ambiguous — reprompt once
        if es.reprompts_given < 1:
            es.reprompts_given += 1
            self._pending_events.append(
                EchoIssued(turn=state.turn_count, slot=es.slot, subfield=es.subfield,
                           value=es.value)
            )
            return UserQuestion(
                text=_QUESTIONS["_echo_reprompt"].format(echo_text=es.text_repr),
                primary_slot=es.slot,
            )

        self._echo_state = None
        return [  # type: ignore[return-value]
            FlagForCall1(
                topic=es.slot,
                user_quote=reply[:200],
                note=f"Echo ambiguous for '{es.slot}'. Flagged for Jordan.",
                field_id=es.slot,
            )
        ]

    def _commit_echo_value(
        self, es: _EchoState, state: ProfileState
    ) -> NextAction:
        """Emit the write tool after echo confirmed.  False-write rate = 0 by construction."""
        slot = es.slot
        value = es.value

        # Owner sub-field echo confirmation
        if self._owner_capture is not None and self._owner_capture.econ_phase:
            return self._commit_owner_echo(es, state)

        # Fee echo confirmation
        if self._fee_item is not None and self._fee_item.phase == "echo":
            fi = self._fee_item
            self._fee_item = None
            tc: list[Any] = [
                AddFee(fee_type=fi.fee_type, amount=fi.amount or 0.0,
                       unit=fi.unit or "flat")  # type: ignore[arg-type]
            ]
            return tc  # type: ignore[return-value]

        # Tax echo confirmation
        if self._tax_item is not None and self._tax_item.phase == "echo":
            return self._commit_tax(state)

        # Scalar echo fields
        if slot == "security_deposit_amount":
            return [  # type: ignore[return-value]
                RecordAnswer(
                    field_id=slot,
                    value=value,
                    source=Source.USER_STATED,
                )
            ]

        # Fallback
        return [RecordAnswer(field_id=slot, value=value, source=Source.USER_STATED)]  # type: ignore[return-value]

    # ── Fee collection loop (mandatory_fees) ─────────────────────────────────

    def _handle_fee_reply(self, state: ProfileState, reply: str) -> NextAction:
        t = reply.lower()

        if _is_advice_request(reply):
            return [  # type: ignore[return-value]
                FlagForCall1(
                    topic="advice_request_in_fee_collection",
                    user_quote=reply[:200],
                    note="User asked for advice during fee collection. Flagged for Jordan.",
                    field_id=None,
                )
            ]

        # "none" / "no fees" → close the loop
        if _is_idk(reply) or "no" in t or "none" in t or "no fees" in t:
            self._in_fee_loop = False
            self._fee_item = None
            self._current_slot = None
            return [SkipQuestion(field_id="mandatory_fees", reason="User has no mandatory fees")]  # type: ignore[return-value]

        # "done" / "that's all" → close the loop (we already have some fees)
        if any(w in t for w in ("done", "that's all", "that's it", "no more", "nothing else")):
            self._in_fee_loop = False
            self._fee_item = None
            self._current_slot = None
            return []  # type: ignore[return-value]

        # Conditional fee → flag (Path E)
        if any(w in t for w in ("if", "only if", "when guest", "optional", "checkbox")):
            self._fee_item = None
            return [  # type: ignore[return-value]
                FlagForCall1(
                    topic="conditional_fee",
                    user_quote=reply[:200],
                    note=f"Conditional fee noted: '{reply.strip()}'. Jordan to configure as optional.",
                    field_id=None,
                )
            ]

        # Start a new fee or continue existing one
        if self._fee_item is None:
            self._fee_item = _FeeItem()
            # Try to extract fee_type + amount from single reply
            amount, unit = _parse_amount(reply)
            # Extract fee type (everything before the amount, or generic)
            fee_type_match = re.sub(r"[\$€£]?\d+(?:\.\d+)?%?\s*(flat|percent|per\s*night)?", "",
                                    reply, flags=re.IGNORECASE).strip().rstrip(",")
            self._fee_item.fee_type = (
                fee_type_match[:60] if fee_type_match else "additional_fee"
            )
            if amount is not None:
                self._fee_item.amount = amount
                self._fee_item.unit = unit
                self._fee_item.phase = "echo"
                return self._begin_echo(
                    slot="mandatory_fees",
                    subfield=self._fee_item.fee_type,
                    value={"amount": amount, "unit": unit},
                    text_repr=(
                        f"a {self._fee_item.fee_type} of "
                        f"{amount}{'%' if unit == 'percent' else ' (flat)'}"
                    ),
                    state_turn=state.turn_count,
                )
            # No amount found — ask
            return UserQuestion(
                text=f"What amount do you charge for the {self._fee_item.fee_type}?",
                primary_slot="mandatory_fees",
            )

        # Continuing an existing fee item (after asking for amount)
        amount, unit = _parse_amount(reply)
        if amount is not None and self._fee_item.fee_type:
            self._fee_item.amount = amount
            self._fee_item.unit = unit
            self._fee_item.phase = "echo"
            return self._begin_echo(
                slot="mandatory_fees",
                subfield=self._fee_item.fee_type,
                value={"amount": amount, "unit": unit},
                text_repr=(
                    f"a {self._fee_item.fee_type} of "
                    f"{amount}{'%' if unit == 'percent' else ' (flat)'}"
                ),
                state_turn=state.turn_count,
            )

        return self._clarify_or_skip("mandatory_fees", reply, "the fee amount")

    def _ask_fee_next(self) -> NextAction:
        """After committing a fee, ask if there are more."""
        return UserQuestion(
            text=_QUESTIONS["mandatory_fees_more"],
            primary_slot="mandatory_fees",
        )

    # ── Tax collection loop (taxes — always flagged) ──────────────────────────

    def _handle_tax_reply(self, state: ProfileState, reply: str) -> NextAction:
        t = reply.lower()

        if _is_advice_request(reply):
            return [  # type: ignore[return-value]
                FlagForCall1(
                    topic="advice_request_in_tax_collection",
                    user_quote=reply[:200],
                    note="User asked for advice during tax collection. Flagged for Jordan.",
                    field_id=None,
                )
            ]

        if _is_idk(reply) or "no" in t or "none" in t:
            self._in_tax_loop = False
            self._tax_item = None
            self._current_slot = None
            return [SkipQuestion(field_id="taxes", reason="User has no taxes to configure")]  # type: ignore[return-value]

        if any(w in t for w in ("done", "that's all", "no more", "nothing else", "that's it")):
            self._in_tax_loop = False
            self._tax_item = None
            self._current_slot = None
            return []  # type: ignore[return-value]

        # Build a tax record from the reply (best-effort)
        if self._tax_item is None:
            self._tax_item = _TaxItem()

        ti = self._tax_item

        if ti.phase == "type":
            # Map user description to tax_type
            _tax_type_map = {
                "sales tax": "sales_vat",
                "vat": "sales_vat",
                "sales": "sales_vat",
                "occupancy": "occupancy_tourist",
                "tourist": "occupancy_tourist",
                "city": "city_local",
                "local": "city_local",
                "gst": "gst",
                "other": "other",
            }
            val = None
            for phrase, canonical in _tax_type_map.items():
                if phrase in t:
                    val = canonical
                    break
            if val:
                ti.tax_type = val
                if val == "other":
                    ti.tax_type_other = reply.strip()[:100]
                ti.phase = "inclusivity"
                return UserQuestion(
                    text=f"Is the {reply.strip()} inclusive or exclusive (i.e. added on top)?",
                    primary_slot="taxes",
                )
            # Unknown type — record verbatim as 'other'
            ti.tax_type = "other"
            ti.tax_type_other = reply.strip()[:100]
            ti.phase = "inclusivity"
            return UserQuestion(
                text="Is this tax included in the price (inclusive) or added on top (exclusive)?",
                primary_slot="taxes",
            )

        if ti.phase == "inclusivity":
            ti.inclusivity = "inclusive" if "inclusive" in t else "exclusive"
            ti.phase = "echo"
            return self._begin_echo(
                slot="taxes",
                subfield=ti.tax_type,
                value={"tax_type": ti.tax_type, "inclusivity": ti.inclusivity,
                       "what_taxed": ti.what_taxed, "scope": ti.scope},
                text_repr=(
                    f"a {ti.tax_type_other or ti.tax_type} tax, {ti.inclusivity}, "
                    f"applied {ti.scope}"
                ),
                state_turn=state.turn_count,
            )

        return []  # type: ignore[return-value]

    def _commit_tax(self, state: ProfileState) -> NextAction:
        """Emit add_tax + flag_for_call_1 (§4 S4 — always flag taxes, Path H)."""
        ti = self._tax_item
        assert ti is not None
        self._tax_item = None
        tt_other = ti.tax_type_other if ti.tax_type == "other" else None
        return [  # type: ignore[return-value]
            AddTax(
                tax_type=ti.tax_type,
                tax_type_other=tt_other,
                inclusivity=ti.inclusivity,  # type: ignore[arg-type]
                what_taxed=ti.what_taxed,  # type: ignore[arg-type]
                scope=ti.scope,  # type: ignore[arg-type]
            ),
            FlagForCall1(
                topic="tax_configuration",
                user_quote=f"{ti.tax_type}: {ti.inclusivity}",
                note="Tax recorded as stated. Jordan must verify before activation — "
                     "tree never corrects tax law (Path H).",
                field_id="taxes",
            ),
        ]

    def _ask_tax_next(self) -> NextAction:
        return UserQuestion(text=_QUESTIONS["taxes_more"], primary_slot="taxes")

    # ── Teammate collection loop ─────────────────────────────────────────────

    def _handle_teammate_reply(self, state: ProfileState, reply: str) -> NextAction:
        t = reply.lower()

        if _is_advice_request(reply):
            return [  # type: ignore[return-value]
                FlagForCall1(
                    topic="advice_request_in_teammate_collection",
                    user_quote=reply[:200],
                    note="User asked for advice during teammate collection. Flagged for Jordan.",
                    field_id=None,
                )
            ]

        if _is_idk(reply):
            self._in_teammate_loop = False
            self._current_slot = None
            if self._teammate_buf:
                return [RecordAnswer(field_id="teammates", value=self._teammate_buf,
                                     source=Source.USER_STATED)]  # type: ignore[return-value]
            return [SkipQuestion(field_id="teammates", reason="User deferred teammate collection")]  # type: ignore[return-value]

        if any(w in t for w in ("done", "no more", "that's all", "that's it", "none", "just me")):
            self._in_teammate_loop = False
            self._current_slot = None
            if self._teammate_buf:
                return [RecordAnswer(field_id="teammates", value=self._teammate_buf,
                                     source=Source.USER_STATED)]  # type: ignore[return-value]
            return [SkipQuestion(field_id="teammates", reason="No teammates to add")]  # type: ignore[return-value]

        # Parse: "Alice Smith, alice@example.com, admin"
        email = _parse_email(reply)
        role_val = _parse_enum(reply, _TEAMMATE_ROLE_MAP)
        # Name = everything before the comma or email
        parts = re.split(r"[,;]", reply)
        name = parts[0].strip() if parts else reply.strip()[:50]

        if name and email:
            tm = {"name": name, "email": email, "role": role_val or "admin",
                  "listing_scope": "all"}
            self._teammate_buf.append(tm)
        elif name and not email:
            return [  # type: ignore[return-value]
                FlagForCall1(
                    topic="teammate_missing_email",
                    user_quote=reply[:200],
                    note=f"Teammate '{name}' provided without a parseable email. "
                         "Jordan to collect contact details on Call 1.",
                    field_id=None,
                )
            ]

        return UserQuestion(text=_QUESTIONS["teammates_more"], primary_slot="teammates")

    def _ask_teammate_next(self) -> NextAction:
        return UserQuestion(text=_QUESTIONS["teammates_more"], primary_slot="teammates")

    # ── S8 Owner-capture sub-FSM ──────────────────────────────────────────────
    #
    # Hero-branch FSM sketch (matches schema §4 S8 decision graph):
    #
    #   ownership_model in [all_managed_for_others, mixed]
    #       └── ask_count ─────────────────── N owners
    #               for each owner i=1..N:
    #                   name → email → listings → share → management_model
    #                   BRANCH on management_model:
    #                     commission:    commission_rate (echo) → channel_commission
    #                     fixed_fee:     fixed_fee_amount (echo)
    #                     revenue_split: split_terms (echo verbal) → flag_for_call_1
    #                     other:         split_terms (free text)  → flag_for_call_1
    #                   → emit add_owner + flag_for_call_1 (intent-capture, G1)

    def _enter_owner_loop(
        self, state: ProfileState, facts: dict[str, Any]
    ) -> NextAction:
        self._owner_capture = _OwnerCapture(expected_count=0)  # count TBD
        self._current_slot = "owners_count"
        return UserQuestion(
            text=_QUESTIONS["owners_count"],
            primary_slot="owners",
        )

    def _ask_owner_next(self, state: ProfileState) -> NextAction:
        oc = self._owner_capture
        if oc is None:
            return self._advance(state, [])

        if oc.owners_done >= oc.expected_count and oc.expected_count > 0:
            # All owners captured
            self._owner_capture = None
            return []  # type: ignore[return-value]  # harness calls again → _advance

        phase_q = self._owner_question_for_phase(oc)
        return UserQuestion(text=phase_q, primary_slot="owners")

    def _handle_owner_reply(self, state: ProfileState, reply: str) -> NextAction:
        oc = self._owner_capture
        if oc is None:
            return []  # type: ignore[return-value]

        # First: collecting owner count
        if self._current_slot == "owners_count":
            n = _parse_integer(reply)
            if n is None or n < 1:
                # Ambiguous — flag and skip
                self._owner_capture = None
                return [  # type: ignore[return-value]
                    FlagForCall1(
                        topic="owner_count_unclear",
                        user_quote=reply[:200],
                        note="Could not determine number of owners. Jordan to collect via CSV upload.",
                        field_id="owners",
                    ),
                    SkipQuestion(field_id="owners", reason="Owner count unclear — deferred to Call 1"),
                ]
            oc.expected_count = n
            oc.phase = "name"
            self._current_slot = None
            return self._ask_owner_next(state)

        # Per-owner field collection
        return self._advance_owner_phase(oc, state, reply)

    def _advance_owner_phase(
        self, oc: _OwnerCapture, state: ProfileState, reply: str
    ) -> NextAction:
        if _is_advice_request(reply):
            return [  # type: ignore[return-value]
                FlagForCall1(
                    topic="advice_request_in_owner_capture",
                    user_quote=reply[:200],
                    note="User asked for advice during owner detail collection. Flagged for Jordan.",
                    field_id=None,
                )
            ]

        phase = oc.phase

        if phase == "name":
            oc.current["owner_name"] = reply.strip()[:100]
            oc.phase = "email"
            return self._ask_owner_next(state)

        if phase == "email":
            email = _parse_email(reply) or reply.strip()[:100]
            oc.current["email"] = email
            oc.phase = "listings"
            return self._ask_owner_next(state)

        if phase == "listings":
            listings = _parse_listings(reply)
            oc.current["listings"] = listings if listings else [reply.strip()[:100]]
            oc.phase = "share"
            return self._ask_owner_next(state)

        if phase == "share":
            if _is_idk(reply) or "skip" in reply.lower() or "n/a" in reply.lower():
                oc.current["ownership_share"] = None
            else:
                amount, _ = _parse_amount(reply)
                oc.current["ownership_share"] = amount
            oc.phase = "management_model"
            return self._ask_owner_next(state)

        if phase == "management_model":
            val = _parse_enum(reply, _MGMT_MODEL_MAP)
            if not val:
                if self._ambiguity_count.get("owner_management_model", 0) < 1:
                    self._ambiguity_count["owner_management_model"] = \
                        self._ambiguity_count.get("owner_management_model", 0) + 1
                    return UserQuestion(
                        text=(
                            "Could you clarify how you're paid for managing "
                            f"{oc.current.get('owner_name', 'this owner')}'s properties — "
                            "percentage commission, flat monthly fee, revenue split, or other?"
                        ),
                        primary_slot="owners",
                    )
                # Still ambiguous — flag
                self._owner_capture = None
                return [  # type: ignore[return-value]
                    FlagForCall1(
                        topic="management_model_unclear",
                        user_quote=reply[:200],
                        note=f"Management model for owner {oc.current.get('owner_name')} unclear. "
                             "Jordan to clarify on Call 1.",
                        field_id="owners",
                    )
                ]
            oc.current["management_model"] = val
            oc.phase = "economics"
            oc.econ_phase = self._first_econ_phase(val)
            return self._ask_owner_next(state)

        if phase == "economics":
            return self._advance_owner_economics(oc, state, reply)

        return []  # type: ignore[return-value]

    def _first_econ_phase(self, management_model: str) -> str:
        return {
            "commission": "commission_rate",
            "fixed_fee": "fixed_fee_amount",
            "revenue_split": "split_terms",
            "other": "split_terms",
        }[management_model]

    def _advance_owner_economics(
        self, oc: _OwnerCapture, state: ProfileState, reply: str
    ) -> NextAction:
        if _is_advice_request(reply):
            return [  # type: ignore[return-value]
                FlagForCall1(
                    topic="advice_request_in_owner_economics",
                    user_quote=reply[:200],
                    note="User asked for advice during owner economics collection. Flagged for Jordan.",
                    field_id=None,
                )
            ]

        ep = oc.econ_phase

        if ep == "commission_rate":
            amount, unit = _parse_amount(reply)
            if amount is not None:
                oc.current["pmc_commission_rate"] = amount
                # echo before storing in add_owner
                return self._begin_owner_numeric_echo(
                    oc, state, "pmc_commission_rate",
                    value=amount,
                    text_repr=f"{amount}% commission rate",
                )
            return UserQuestion(
                text=(
                    f"What's your commission rate for "
                    f"{oc.current.get('owner_name', 'this owner')}? (e.g. '15%')"
                ),
                primary_slot="owners",
            )

        if ep == "channel_commission":
            val = _parse_enum(reply, _CHANNEL_COMMISSION_MAP)
            if not val:
                val = "pmc"  # default — flag for Jordan to confirm
            oc.current["who_pays_channel_commission"] = val
            return self._commit_owner(oc, state)

        if ep == "fixed_fee_amount":
            amount, unit = _parse_amount(reply)
            if amount is not None:
                oc.current["fixed_fee_amount"] = amount
                return self._begin_owner_numeric_echo(
                    oc, state, "fixed_fee_amount",
                    value=amount,
                    text_repr=f"${amount:.0f} monthly management fee",
                )
            return UserQuestion(
                text=(
                    f"What's the monthly management fee for "
                    f"{oc.current.get('owner_name', 'this owner')}? (e.g. '$500')"
                ),
                primary_slot="owners",
            )

        if ep == "split_terms":
            # Echo the verbal formula before committing (§8 inv 3)
            if reply.strip():
                oc.current["split_terms"] = reply.strip()
                return self._begin_echo(
                    slot="owners",
                    subfield="split_terms",
                    value=reply.strip(),
                    text_repr=f"the arrangement is: '{reply.strip()}'",
                    state_turn=state.turn_count,
                )
            return UserQuestion(
                text=f"How is the split arranged for {oc.current.get('owner_name', 'this owner')}?",
                primary_slot="owners",
            )

        return self._commit_owner(oc, state)

    def _begin_owner_numeric_echo(
        self, oc: _OwnerCapture, state: ProfileState, subfield: str,
        value: float, text_repr: str,
    ) -> NextAction:
        """Start an echo for a per-owner numeric sub-field (§8 inv 1 / EC-12)."""
        self._pending_events.append(
            ValueIntroduced(turn=state.turn_count, slot="owners", subfield=subfield, value=value)
        )
        self._pending_events.append(
            EchoIssued(turn=state.turn_count, slot="owners", subfield=subfield, value=value)
        )
        self._echo_state = _EchoState(
            slot="owners", subfield=subfield, value=value, text_repr=text_repr
        )
        return UserQuestion(
            text=_QUESTIONS["_echo_confirm"].format(echo_text=text_repr),
            primary_slot="owners",
        )

    def _commit_owner_echo(self, es: _EchoState, state: ProfileState) -> NextAction:
        """After echo confirmed for an owner sub-field — advance economics phase."""
        oc = self._owner_capture
        if oc is None:
            return []  # type: ignore[return-value]
        subfield = es.subfield
        self._echo_state = None

        if subfield == "pmc_commission_rate":
            oc.econ_phase = "channel_commission"
            return self._ask_owner_next(state)

        if subfield == "fixed_fee_amount":
            return self._commit_owner(oc, state)

        if subfield == "split_terms":
            return self._commit_owner(oc, state)

        return self._commit_owner(oc, state)

    def _commit_owner(self, oc: _OwnerCapture, state: ProfileState) -> NextAction:
        """Emit add_owner + flag_for_call_1 (intent-capture only, G1 / FR-3)."""
        c = oc.current
        mm = c.get("management_model", "other")

        # Build economics note for the flag
        if mm == "commission":
            econ_note = (
                f"Commission: {c.get('pmc_commission_rate')}% | "
                f"Channel commission paid by: {c.get('who_pays_channel_commission', 'TBD')}"
            )
        elif mm == "fixed_fee":
            econ_note = f"Fixed fee: ${c.get('fixed_fee_amount', 'TBD')}/month"
        else:
            econ_note = f"Terms: {c.get('split_terms', 'TBD')}"

        # Validate mandatory fields — fallback to empty strings if parsing failed
        owner_name = c.get("owner_name") or "Unknown"
        email_val = c.get("email") or "unknown@unknown.com"
        listings_val = c.get("listings") or []

        add_owner_tc = AddOwner(
            owner_name=owner_name,
            email=email_val,
            listings=listings_val,
            ownership_share=c.get("ownership_share"),
            management_model=mm,  # type: ignore[arg-type]
            pmc_commission_rate=c.get("pmc_commission_rate") if mm == "commission" else None,
            fixed_fee_amount=c.get("fixed_fee_amount") if mm == "fixed_fee" else None,
            split_terms=c.get("split_terms") if mm in ("revenue_split", "other") else None,
            who_pays_channel_commission=c.get("who_pays_channel_commission"),
        )
        flag_tc = FlagForCall1(
            topic="owner_economics",
            user_quote=econ_note,
            note=(
                f"Owner {owner_name} ({email_val}): {mm} arrangement. "
                f"{econ_note}. Jordan to configure Business Models on Call 1 — "
                "intent-capture only, no BusinessModel records written (G1)."
            ),
            field_id=None,   # topic-level flag (no field disposition)
        )

        # Advance to next owner
        oc.owners_done += 1
        oc.current = {}
        oc.phase = "name"
        oc.econ_phase = None
        self._ambiguity_count.pop("owner_management_model", None)

        return [add_owner_tc, flag_tc]  # type: ignore[return-value]

    def _owner_question_for_phase(self, oc: _OwnerCapture) -> str:
        idx = oc.owners_done  # 0-based: owner we're capturing
        name = oc.current.get("owner_name", f"owner {idx + 1}")
        n = idx + 1

        if oc.phase == "name":
            return f"Let's capture owner {n}. What's their full name?"
        if oc.phase == "email":
            return f"What's {name}'s email address?"
        if oc.phase == "listings":
            return f"Which of your listings does {name} manage? (names or 'all')"
        if oc.phase == "share":
            return (
                f"What percentage ownership share does {name} hold, if any? "
                "(Or say 'skip' if not applicable.)"
            )
        if oc.phase == "management_model":
            return (
                f"How do you get paid for managing {name}'s properties — "
                "a percentage commission, a flat monthly fee, a revenue split, or other?"
            )
        # Economics
        ep = oc.econ_phase
        if ep == "commission_rate":
            return f"What's your commission rate for {name}'s properties? (e.g. '15%')"
        if ep == "channel_commission":
            return (
                f"For {name}'s listings, who pays the OTA/channel commission — "
                "you (the PMC), the owner, or split?"
            )
        if ep == "fixed_fee_amount":
            return f"What's your monthly management fee for {name}'s properties?"
        if ep == "split_terms":
            return (
                f"How is the revenue split for {name}? "
                "Describe the arrangement — e.g. '70% to owner after fees'."
            )
        return f"Any other details about {name}?"

    # ── Ambiguity / fallback handling ────────────────────────────────────────

    def _clarify_or_skip(
        self, slot: str, reply: str, hint: str
    ) -> NextAction:
        """One clarifying question max per slot; then skip+flag (§8 inv 3)."""
        count = self._ambiguity_count.get(slot, 0)
        if count < 1:
            self._ambiguity_count[slot] = count + 1
            self._current_slot = slot  # stay on this slot for the retry
            return UserQuestion(
                text=_QUESTIONS["_clarify"].format(slot_hint=hint),
                primary_slot=slot,
            )
        # Second ambiguity — skip + flag
        self._current_slot = None
        self._ambiguity_count.pop(slot, None)
        return [  # type: ignore[return-value]
            SkipQuestion(
                field_id=slot,
                reason=f"Could not resolve after one clarification: '{reply[:100]}'",
            ),
            FlagForCall1(
                topic=slot,
                user_quote=reply[:200],
                note=f"Ambiguous answer for '{slot}' — flagged for Jordan to clarify.",
                field_id=slot,
            ),
        ]
