---
title: "Guesty Pro Account-Creation Schema (Synthetic) — The Complete Customer Profile"
author: "Mary (Business Analyst)"
date: 2026-06-02
version: 0.3 (synthetic, knowledge-base validated, + sales-handover-note prefill layer, for PoC)
status: draft
purpose: "Canonical, finite definition of the 'complete customer profile' an onboarding agent reasons toward. The frame the agent fills; the source the OB brief synthesizes from; the surface the baseline decision tree branches over."
derived_from:
  - "OB V2 prototype — wizard.jsx / screens.jsx (field IDs, showIf branching)"
  - "Guesty Onboarding Responses.md (18 Qs / 7 sections + starter-kit appendix)"
  - "conversation_script_financials.md (field_ids, tool calls, echo/flag rules)"
  - "Inputs from Salesforce.md (sf_intake seed/prefill — STRUCTURED layer)"
  - "Notes for Tamar (Salesforce export) — 611 real sales→OB handover notes (UNSTRUCTURED layer)"
  - "ob_specialist_brief.md (section grouping, auto-setup, brief generation)"
  - "Tahini/knowledge — domains/index.md, product-model/er-core.md, personas"
companion: "research/ai-adaptive-questionnaire-onboarding-research-2026-06-02.md"
companion_2: "sales-handover-notes-corpus-analysis-2026-06-02.md"
---

# Guesty Pro Account-Creation Schema (Synthetic)

> **What this is.** A single, finite "frame" (in the slot-filling sense — see the companion
> research report) that defines everything a Guesty Pro account needs to be considered
> *complete enough* to create the account and run a productive Call 1. The AI agent's job is
> to **fill this frame**; it is *not* to follow a fixed question list. The baseline decision
> tree branches over this same frame. The OB Specialist Brief synthesizes from it.
>
> **Synthetic.** Field names, enums, and entity mappings are reconstructed from the supplied
> artifacts and the Guesty entity model. They approximate the real product closely enough to
> drive a PoC but must be validated against production before any build.

---

## 1. How to read this schema

Every field carries this metadata so the agent (and the baseline tree) know how to treat it:

| Attribute | Values | Meaning |
|-----------|--------|---------|
| `id` | snake_case | Stable semantic identifier (the agent references this, never the rendered label) |
| `section` | S1–S8 | Onboarding section (matches brief grouping) |
| `domain` | D1–D6 | Guesty product domain (`domains/index.md`) |
| `type` | enum / number / boolean / text / file / list / object | Data shape |
| `priority` | `required` / `recommended` / `optional` | Contribution to "completeness" (§3) |
| `source` | `sf_prefill` / `ai_extracted_from_note` / `user_stated` / `inferred` / `hardcoded_starter` | Where the value originates |
| `collection` | `widget` / `conversational` / `either` | How it should be gathered (research §4.5) |
| `write_target` | `Entity.field` | Source-of-truth entity it maps to (`er-core.md`) |
| `depends_on` | field + condition | Branch guard — only relevant when condition holds |
| `human_handoff` | `none` / `flag_for_call_1` | Whether the agent defers to the human onboarder |
| `echo_before_write` | true / false | Must echo the value back and get confirmation before recording (numbers) |

**Runtime per-field state** the agent maintains (not authored, observed):

```json
{ "value": "<typed>", "source": "user_stated", "confidence": 0.0,
  "provenance": "<quoted source span | null>",
  "status": "unanswered | recorded | skipped | flagged | prefilled_unconfirmed",
  "flag_ref": "<flag id|null>" }
```

> **Source precedence (conflict resolution):** `user_stated` > `sf_prefill` (structured) >
> `ai_extracted_from_note`. A note-derived value is a **hint to confirm**, never a silent truth —
> it enters as `status: prefilled_unconfirmed` and must be echoed before it becomes `recorded`.
> Conflicts surface to the brief (`⚠️ Note said Hostaway; user says Lodgify`). See §0 and §11.

---

## 2. Section / domain map

| Section | Name | Primary domain | Notes |
|---------|------|----------------|-------|
| **S0a** | Seed — Salesforce structured | D6 | Prefill only; user confirms, never re-types |
| **S0b** | Seed — Sales handover note (AI-extracted) | D6 | Free-text note → structured hints; **confirm, never assume**; see §0 |
| **S1** | Brand | D6 | Logo → guest-facing surfaces |
| **S2** | Pre-flight (Properties & Channels) | D5 / D2 | **Airbnb connection moved INSIDE the product** (CEO direction) — not a schema field |
| **S3** | Operations | D2 | Cleaning, turnover, locks |
| **S4** | Financials | D1 | Highest-risk; echo-before-write; tax = human handoff |
| **S5** | Booking Website | D5 | Direct-booking surface |
| **S6** | Governance | D6 | Decision owners, teammates |
| **S7** | Focus topics | D4 / D3 | Drives Call 1 agenda + biggest pain (free text) |
| **S8** | Business (Ownership & Pricing) | D2 / D1 | **Hero adaptive branch** — ownership → business model |

---

## 3. "Complete profile" — completeness definition

Completeness is **tiered**, so the agent knows when it can stop and when it is merely enriching.

### 3.1 Minimum Viable Profile (MVP) — account can be created + Call 1 scheduled
All `required` fields recorded *or* explicitly flagged for the human:

- `account_name`, `country`, `listing_count`, `channels` (S0/S2 — mostly prefilled)
- `ownership_model` (S8 — drives the hero branch)
- `go_live` (S2 — sets onboarding pace)
- At least one of {`focus_topics`, `pain`} (S7 — gives Call 1 a purpose)

> A financial/tax section that is **fully deferred** still satisfies MVP, because the script
> permits skipping the whole Financials section with a flag (Path F). Deferred ≠ missing.

### 3.2 Complete Profile — productive Call 1, meaningful auto-setup
All `required` + all `recommended` fields are either recorded or flagged. This is the target.

### 3.3 Enriched Profile — maximal auto-setup, minimal Call 1 setup time
`required` + `recommended` + `optional`. Diminishing returns; never block on these.

**Completion metric** (drives the brief's `completion_pct` and PoC hypothesis H1):
```
completion_pct = (recorded_required + 0.6*recorded_recommended + 0.3*recorded_optional)
                 / (total_required + 0.6*total_recommended + 0.3*total_optional)
```
Flagged-for-human counts as "addressed" for MVP gating but not as "recorded" for completeness.

---

## 4. The schema

Presented per section as machine-readable field objects followed by notes. Enums use the
identifiers seen in the prototype/scripts where available.

### S0a — Seed (Salesforce — structured prefill)
Confirmed, never re-typed. Conflicts surface to the brief (`⚠️ Conflict: SF 8 vs user 12`).

```json
[
  { "id": "account_name",        "type": "text",   "priority": "required",    "source": "sf_prefill", "write_target": "Account.name" },
  { "id": "country",             "type": "text",   "priority": "required",    "source": "sf_prefill", "write_target": "Account.country",
    "note": "Drives tax jurisdiction + rate-strategy defaults" },
  { "id": "active_listing_count","type": "number", "priority": "required",    "source": "sf_prefill", "collection": "either",
    "note": "ACTIVE listings, not total properties; user confirms in S2" },
  { "id": "connected_channels",  "type": "list<enum>", "priority": "required","source": "sf_prefill",
    "options": ["airbnb","booking","vrbo","expedia","direct","other"] },
  { "id": "third_party_tools",   "type": "object", "priority": "recommended", "source": "sf_prefill",
    "shape": { "pms_or_pricing": "list|null", "cleaning": "list|null", "accounting": "list|null", "locks": "list|null" },
    "note": "e.g. PriceLabs → skip Guesty pricing setup; Turno → cleaning; RemoteLock → locks" },
  { "id": "logo_url",            "type": "file|url","priority": "optional",   "source": "sf_prefill", "write_target": "Account.logo" },
  { "id": "business_profile",    "type": "object", "priority": "recommended", "source": "sf_prefill",
    "shape": { "business_name": "text|null", "business_email": "text|null", "domain_hint": "text|null" } },
  { "id": "ob_specialist_name",  "type": "text",   "priority": "required",    "source": "sf_prefill",
    "note": "The human onboarder (Jordan) the agent defers to" }
]
```

### S0b — Seed (Sales handover note → AI-extracted prefill)

> **New in v0.3.** Alongside the structured fields, Salesforce carries the rep's free-text
> **handover note** (the "Notes" field; 611 real examples analyzed in the companion corpus doc).
> An LLM extractor turns this note into **prefill candidates**. These are *hints to confirm*, not
> truths: each carries `confidence` + `provenance` (source span), enters as
> `status: prefilled_unconfirmed`, loses to structured `sf_prefill` and to `user_stated`
> (precedence in §1), and must be **echoed before** it becomes `recorded`. This is the
> primary AI-value case for prefill — see PoC Claim H2.

```json
[
  { "id": "handover_note_raw", "section": "S0b", "domain": "D6", "type": "text", "priority": "optional",
    "source": "sf_prefill", "collection": "none",
    "note": "The raw rep note (PII). Input to the extractor; never shown verbatim to the agent as fact." },

  { "id": "migration_source", "section": "S0b", "domain": "D6", "type": "enum|text", "priority": "recommended",
    "source": "ai_extracted_from_note", "confirm_before_use": true,
    "options": ["guesty_for_hosts","guesty_lite","hostaway","lodgify","smoobu","avantio","hostfully",
                "uplisting","streamline","cloudbeds","beds24","ownerrez","hospitable","siteminder","evolve","other","none"],
    "note": "25.7% of notes name a prior PMS. Drives migration path + import strategy on Call 1." },

  { "id": "prior_pms_experience", "section": "S0b", "domain": "D6", "type": "enum", "priority": "recommended",
    "source": "ai_extracted_from_note", "confirm_before_use": true,
    "options": ["none_first_time","manual_only","experienced"],
    "note": "7.2% explicitly first-time/manual. Sets OB pacing + guidance level." },

  { "id": "ob_language", "section": "S0b", "domain": "D6", "type": "enum", "priority": "recommended",
    "source": "ai_extracted_from_note", "confirm_before_use": true,
    "options": ["en","fr","es","de","it","pt","other"],
    "note": "French 2.5% + Spanish 1.3% + others explicitly request non-English OB. Routes specialist + content." },

  { "id": "tech_level", "section": "S0b", "domain": "D6", "type": "enum", "priority": "optional",
    "source": "ai_extracted_from_note", "confirm_before_use": false,
    "options": ["low","medium","high"],
    "note": "Communication/pacing hint for the brief. Never gates flow; never echoed to user." },

  { "id": "addon_intent", "section": "S0b", "domain": "D6", "type": "list<enum>", "priority": "recommended",
    "source": "ai_extracted_from_note", "confirm_before_use": true,
    "options": ["gpo","damage_protection","guestypay","abw","accounting","locks","gcs","premium_channels","auto_comply"],
    "note": "Bundled/intended add-ons. 'damage_protection (mandatory)' is common — sets security_deposit_type + a mandatory flag." },

  { "id": "customer_sentiment", "section": "S0b", "domain": "D6", "type": "enum", "priority": "optional",
    "source": "ai_extracted_from_note", "confirm_before_use": false,
    "options": ["positive","neutral","anxious","frustrated","at_risk"],
    "human_handoff": "flag_for_call_1",
    "note": "7.4% carry sentiment cues. Routes to the OB brief + Call-1 handling. Agent NEVER acts on this unilaterally and never echoes it to the user." },

  { "id": "risk_flags", "section": "S0b", "domain": "D6", "type": "list<enum>", "priority": "optional",
    "source": "ai_extracted_from_note", "confirm_before_use": false,
    "options": ["high_addon_complexity","white_glove_expected","payment_comprehension","mandatory_dp",
                "opt_out_clause","language_barrier","hq_subaccount_structure","mid_long_term_excluded"],
    "human_handoff": "flag_for_call_1",
    "note": "Surfaced to the brief for Jordan. Never changes agent behavior automatically." }
]
```

> **Prefill, don't interrogate.** A high-confidence extracted slot lets the agent *confirm*
> ("Sales noted you're coming from Hostaway and want locks — still right?") instead of asking
> cold. This is the direct line to the CEO's "use this data to prefill the starter kit" and to
> the PoC's "questions to completion" secondary metric. `customer_sentiment`/`risk_flags` and
> `tech_level` are **brief-only** — they never surface to the user and never gate the flow.

### S1 — Brand

```json
[
  { "id": "logo_file", "section": "S1", "domain": "D6", "type": "file", "priority": "recommended",
    "source": "sf_prefill | user_stated", "collection": "widget", "write_target": "Account.logo",
    "note": "Prefill from logo_url; appears on booking site + guest emails. PNG/SVG, square." }
]
```

### S2 — Pre-flight (Properties & Channels)

```json
[
  { "id": "listing_count", "section": "S2", "domain": "D2", "type": "number", "priority": "required",
    "source": "sf_prefill", "collection": "either", "write_target": "—(orchestration)",
    "note": "Confirm/adjust the SF number. Triggers the S8 ownership branch." },
  { "id": "channels", "section": "S2", "domain": "D5", "type": "list<enum>", "priority": "required",
    "source": "sf_prefill", "options": ["airbnb","booking","vrbo","expedia","direct","other"],
    "write_target": "Listing.channels(bridge)", "note": "Confirm SF list." },
  { "id": "other_channels_text", "section": "S2", "domain": "D5", "type": "text", "priority": "optional",
    "source": "user_stated", "depends_on": "channels includes 'other'" },
  { "id": "go_live", "section": "S2", "domain": "D6", "type": "enum", "priority": "required",
    "source": "user_stated", "options": ["asap","2-4w","1-2m","exploring"],
    "note": "Sets onboarding-call pace. Changeable later." }
]
```

> **CEO direction — Airbnb connection moved INSIDE the product.** The prototype's in-wizard
> OAuth + listing import (`Q1.4 / Q1.4b / Q1.AHA`, gated on `oauth_status === "success"`) are
> **removed from this schema.** Pre-flight confirms counts/channels and the agent reasons
> about ownership; the actual view-only Airbnb connection happens in the existing in-product
> interface. (No `oauth_status`, `selected_listings` fields here.)

### S3 — Operations

```json
[
  { "id": "cleaning_system", "section": "S3", "domain": "D2", "type": "enum", "priority": "recommended",
    "source": "user_stated", "collection": "conversational",
    "options": ["in_house","cleaning_company","marketplace_tool","mixed"],
    "note": "Prefill hint from third_party_tools.cleaning (e.g. Turno → marketplace_tool)." },
  { "id": "turnover_checklist_choice", "section": "S3", "domain": "D2", "type": "enum", "priority": "optional",
    "source": "user_stated", "options": ["upload","guesty_template","skip"] },
  { "id": "turnover_checklist_file", "section": "S3", "domain": "D2", "type": "file", "priority": "optional",
    "source": "user_stated", "collection": "widget", "depends_on": "turnover_checklist_choice == 'upload'" },
  { "id": "smart_locks", "section": "S3", "domain": "D2", "type": "enum|text", "priority": "optional",
    "source": "sf_prefill | user_stated", "write_target": "Lock(integration)",
    "note": "Prefill from third_party_tools.locks (e.g. RemoteLock)." }
]
```

### S4 — Financials  *(highest risk — echo_before_write; tax = human handoff)*

```json
[
  { "id": "revenue_recognition", "section": "S4", "domain": "D1", "type": "enum", "priority": "recommended",
    "source": "user_stated", "collection": "conversational",
    "canonical_term": "Recognized Revenue for Analytics",
    "options": ["checkin_date","checkout_date","prorated"],
    "scope": "listing-level (NOT reservation-level)",
    "write_target": "Listing.recognizedRevenue (analytics scope)", "human_handoff": "none",
    "validation": "CONFIRMED (glossary + d1-financials): options = check-in / check-out / prorated; listing-level, so changing it has listing-wide blast radius. Earlier 'split_nights' corrected to 'prorated'." },
  { "id": "non_refundable_enabled", "section": "S4", "domain": "D1", "type": "boolean", "priority": "recommended",
    "source": "user_stated", "canonical_term": "Rate Plan (cancellation policy)",
    "write_target": "RatePlan.cancellationPolicy (non-refundable variant)",
    "validation": "CONFIRMED: non-refundable is a Rate Plan / cancellation-policy concept, distinct from Rate Strategy (nightly rates).",
    "note": "Agent explains neutrally, never recommends; advice → flag_for_call_1 (Paths B/G)." },
  { "id": "security_deposit_type", "section": "S4", "domain": "D1", "type": "enum", "priority": "recommended",
    "source": "user_stated", "options": ["damage_waiver","security_deposit","damage_protection","none"],
    "write_target": "Money.settingsSnapshot.securityDepositFee | Damage Protection (Shield)",
    "validation": "PARTIAL: 'Damage Protection' is a distinct Guesty product (coverage up to $20K, replaces a deposit). Guest-facing 'security deposit' must NOT be confused with trust-accounting 'Advanced Deposit' (glossary vocab note). Confirm exact field path with SME." },
  { "id": "security_deposit_amount", "section": "S4", "domain": "D1", "type": "number", "priority": "recommended",
    "source": "user_stated", "echo_before_write": true,
    "depends_on": "security_deposit_type in ['damage_waiver','security_deposit']", "shape": { "amount": "number", "unit": "flat|percent" } },
  { "id": "payment_timing", "section": "S4", "domain": "D1", "type": "enum", "priority": "recommended",
    "source": "user_stated", "options": ["at_booking","near_arrival","split"],
    "canonical_term": "Payment Automation",
    "write_target": "PaymentAutomation (rules by channel/property/reservation type)",
    "validation": "CONFIRMED: glossary defines Payment Automation as automated collection rules by channel/property/reservation type — matches Path C ('depends on channel').",
    "note": "Path C: 'depends on channel' → record direct-booking default, note OTA handled by the channel." },
  { "id": "payment_split", "section": "S4", "domain": "D1", "type": "enum", "priority": "recommended",
    "source": "user_stated", "options": ["100","50_50","20_80","custom"],
    "canonical_term": "Payment Automation (collection schedule)",
    "depends_on": "payment_timing == 'split' OR user volunteers a split",
    "shape_if_custom": { "deposit_pct": "number", "balance_when": "text" } },
  { "id": "mandatory_fees", "section": "S4", "domain": "D1", "type": "list<object>", "priority": "optional",
    "source": "user_stated", "echo_before_write": true, "canonical_term": "Additional Fees",
    "item_shape": { "fee_type": "text", "amount": "number", "unit": "flat|percent" },
    "tool": "add_fee", "write_target": "Additional Fees (guest invoice charges)",
    "validation": "CONFIRMED: glossary 'Additional Fees' = custom guest-invoice charges (late check-out, laundry, pet, etc.). NOTE users say 'cleaning fee' — cleaning is handled per-property, NOT here.",
    "note": "Conditional fees (e.g. pet-on-checkbox) → flag_for_call_1 (Path E)." },
  { "id": "taxes", "section": "S4", "domain": "D1", "type": "list<object>", "priority": "recommended",
    "source": "user_stated", "echo_before_write": true, "human_handoff": "flag_for_call_1",
    "canonical_term": "Tax Configuration",
    "item_shape": { "tax_type": "enum[sales_vat,occupancy_tourist,city_local,gst,other]", "tax_type_other": "text|null",
                    "inclusivity": "inclusive|exclusive", "what_taxed": "list<enum[accommodation_fare,cleaning_fee,additional_fees]>",
                    "scope": "enum[listing,account_wide]" },
    "tool": "add_tax", "write_target": "Tax Configuration (per-listing or account-wide)",
    "validation": "PARTIAL: glossary confirms Tax Configuration covers city/tourism/GST applied individually OR account-wide (added 'scope'). Exact enum casing TBD with SME.",
    "note": "Agent records what the user said and ALWAYS flags for Jordan; NEVER corrects tax law (Path H)." }
]
```

### S5 — Booking Website

> **G6 resolution (2026-06-02):** S5 is in scope **conditionally**. The agent applies **AI judgment** to decide whether to surface it — ask only when context signals direct-booking interest (e.g., user lists "direct" as a channel, mentions "my website", selects `booking_website` as a focus topic, or operates without OTA exclusivity). If no such signals, S5 is silently skipped. In PoC answer keys, expected disposition is `conditional: surface_if_direct_signals_present`.

```json
[
  { "id": "website_brand_name", "section": "S5", "domain": "D5", "type": "text", "priority": "optional",
    "source": "sf_prefill | user_stated", "write_target": "Website.brandName",
    "collection": "conversational_conditional",
    "surface_when": "channels includes 'direct' OR focus_topics includes 'booking_website' OR user volunteers website intent",
    "note": "Prefill from business_profile.business_name." },
  { "id": "website_domain", "section": "S5", "domain": "D5", "type": "enum|text", "priority": "optional",
    "source": "user_stated", "options": ["guesty_subdomain","custom_domain"],
    "collection": "conversational_conditional",
    "surface_when": "website_brand_name is recorded",
    "shape_if_custom": { "domain": "text" }, "note": "Prefill hint from domain_hint." },
  { "id": "website_terms", "section": "S5", "domain": "D5", "type": "enum", "priority": "optional",
    "source": "user_stated", "options": ["guesty_terms","own_terms"],
    "collection": "conversational_conditional",
    "surface_when": "website_domain is recorded" }
]
```

### S6 — Governance

```json
[
  { "id": "decision_owner", "section": "S6", "domain": "D6", "type": "enum", "priority": "recommended",
    "source": "user_stated", "options": ["just_me","shared"], "write_target": "User.roles[]" },
  { "id": "teammates", "section": "S6", "domain": "D6", "type": "list<object>", "priority": "optional",
    "source": "user_stated", "depends_on": "decision_owner == 'shared'",
    "item_shape": { "name": "text", "email": "text",
                    "role": "enum[admin,agent,cleaner,custom]", "listing_scope": "list<listing_ref>|all" },
    "canonical_term": "User Management",
    "write_target": "User[] + Role[] (roles[] embedded with listingIds[] — permissions are listing-scoped)",
    "validation": "ADJUSTED: glossary canonical roles = admin/agent/cleaner (+ property-specific permissions); er-core confirms User.roles[] carries listingIds[]. Earlier ops/finance/viewer replaced with canonical set + custom." }
]
```

### S7 — Focus topics

```json
[
  { "id": "focus_topics", "section": "S7", "domain": "D4", "type": "list<enum>", "priority": "required",
    "source": "user_stated", "max_select": 3,
    "options": ["pricing_strategy","channel_mix","guest_messaging","cleaner_workflows",
                "accounting_setup","owner_reporting","booking_website","reviews_reputation"],
    "note": "Drives the brief's suggested Call 1 agenda + TL;DR bullet 1." },
  { "id": "pain", "section": "S7", "domain": "D3", "type": "text", "priority": "recommended",
    "source": "user_stated", "collection": "conversational",
    "note": "Biggest blocker, in the user's own words. Brief quotes verbatim (no paraphrase)." }
]
```

### S8 — Business: Ownership & Pricing  *(HERO ADAPTIVE BRANCH)*

This is the branch the CEO described and the prototype does **not** yet implement adaptively
(today owners are a flat CSV upload at Q7.2). Modeled as the PoC's primary scenario.

```json
[
  { "id": "ownership_model", "section": "S8", "domain": "D2", "type": "enum", "priority": "required",
    "source": "user_stated", "collection": "conversational",
    "options": ["all_self_owned","all_managed_for_others","mixed"],
    "write_target": "BusinessModel(selection)",
    "note": "ENTRY of the hero branch. Triggered after listing_count is known." },

  { "id": "owners", "section": "S8", "domain": "D2", "type": "list<object>", "priority": "recommended",
    "source": "user_stated", "collection": "either",
    "depends_on": "ownership_model in ['all_managed_for_others','mixed']",
    "tool": "add_owner",
    "item_shape": {
      "owner_name": "text",
      "email": "text",
      "listings": "list<listing_ref>",
      "ownership_share": "number|null",           // ListingOwnerships.share (fractional ownership)
      "management_model": "enum[commission,fixed_fee,revenue_split,other]",  // PMC↔owner split = Business Models
      "pmc_commission_rate": "number|null",       // depends_on management_model == 'commission' — PMC management commission
      "fixed_fee_amount": "number|null",          // depends_on management_model == 'fixed_fee'
      "split_terms": "text|null",                 // depends_on management_model in ['revenue_split','other']
      "who_pays_channel_commission": "enum[owner,pmc,split]|null"  // Channel Commission (OTA fees) — DISTINCT from PMC commission
    },
    "canonical_term": "Owners (D2) + Business Models (D1)",
    "write_target": "Owner[] (owners-master) + ListingOwnerships[] {ownerId, share}",
    "echo_before_write": true,
    "human_handoff": "intent_capture_only",
    "g1_resolution": "RESOLVED 2026-06-02: agent CAPTURES intent only. Owner records (name, email, listings, share) are recorded. BusinessModel configuration (commission splits, counterparty rules) is NOT written by the agent — Jordan configures it on Call 1 using the captured data. Expected disposition in answer keys: owner fields = recorded:<value>; BusinessModel creation = out of agent scope; flag_for_call_1 with the captured owner economics so Jordan has full context.",
    "validation": "DISAMBIGUATED: two separate 'commission' concepts — (1) PMC management commission = Business Models (PMC↔owner↔vendor split); (2) Channel Commission = OTA fees per connected channel. The hero branch's 'commission' = #1. 'who_pays_channel_commission' = #2. NOTE users find the term 'Business Models' confusing (glossary vocab) — the agent should ask in plain language ('how do you get paid for managing these?').",
    "note": "CSV upload (owners_csv) is the bulk alternative to per-owner conversational capture." },

  { "id": "owners_csv", "section": "S8", "domain": "D2", "type": "file", "priority": "optional",
    "source": "user_stated", "collection": "widget",
    "depends_on": "ownership_model in ['all_managed_for_others','mixed']",
    "note": "Bulk path: name,email,listings (+share). Parsed into owners[]." },

  { "id": "rate_strategy", "section": "S8", "domain": "D1", "type": "object", "priority": "optional",
    "source": "user_stated",
    "shape": { "varies": "boolean",
               "seasons": "list<{ name, start_date, end_date, adjustment_pct }>" },
    "write_target": "RateStrategy", "human_handoff": "none",
    "note": "Skip if third_party_tools.pms_or_pricing present (e.g. PriceLabs) → flag integration instead." }
]
```

#### The hero branch as a decision graph (for the baseline tree + agent reasoning)

```
listing_count (S2)
   │
   ▼
ownership_model? ──"all_self_owned"──► (no owner records) ──► rate_strategy / pricing-tool check
   │
   ├─"all_managed_for_others"─┐
   └─"mixed"──────────────────┤
                              ▼
                    capture owners[]  (per owner OR owners_csv)
                              │
                   for each owner ▼
                    management_model?
                       ├─"commission"────► commission_rate + who_pays_channel_fees
                       ├─"fixed_fee"──────► fixed_fee_amount
                       ├─"revenue_split"──► split_terms
                       └─"other"──────────► split_terms (free text) ──► flag_for_call_1
                              │
                              ▼
                    map → Owner + ListingOwnerships + BusinessModel (6 counterparty types)
```

> **Why this is the AI value scenario (research §4.2):** the depth × per-owner × per-model
> fan-out is exactly the combinatorial tree the CEO doesn't want to hand-author, and owner
> descriptions arrive as free text / messy CSV (research §4.1). It also maps cleanly to the
> real entity model: `Owner`, `ListingOwnerships {ownerId, share}`, and `BusinessModel`
> (6 counterparties incl. commission, PMC, owner, vendor, GOV, channel) per `er-core.md`.

---

## 5. Agent tool surface (from the conversation scripts)

The schema is operated through this fixed tool vocabulary. The agent never free-writes to entities.

| Tool | Purpose | Schema link |
|------|---------|-------------|
| `record_answer({field_id, value, source})` | Record a scalar/enum/bool slot | any single field |
| `add_fee({fee_type, amount, unit})` | Append a mandatory fee | `mandatory_fees[]` |
| `add_tax({tax_type, tax_type_other, inclusivity, what_taxed})` | Append a tax | `taxes[]` |
| `add_owner({...owner item_shape})` | Append an owner record | `owners[]` (hero branch) |
| `skip_question({field_id, reason})` | Defer a field | sets status `skipped` |
| `flag_for_call_1({topic, user_quote, note})` | Hand off to human | sets `human_handoff` flagged |
| `end_section({section_id})` | Close a section | section transition |

**Invariants the schema encodes (research §4.5):**
1. `echo_before_write: true` fields fire their write tool **only after** the user confirms the echoed number.
2. `human_handoff: flag_for_call_1` fields (taxes; conditional fees; any advice request) are recorded-as-stated **and** flagged; the agent never corrects or recommends.
3. `skip_question` is honored immediately — no retry loop, no "are you sure," no upsell.

---

## 6. Source-of-truth mapping (to the Guesty entity model)

So the recorded profile lands in the right place (per `product-model/er-core.md`):

| Schema area | Canonical term / entity | Caveat (validated against glossary + er-core) |
|-------------|------------------------|-----------------------------------------------|
| Brand / logo | `Account` | account-level |
| Listings / counts | `Listing` (+ `Property`/Complex if multi-unit) | listing is per-`Stay` in v3; "units/apartments" = sub-units |
| Channels | **Distribution / Channel Manager** (per-channel bridge/mirror) | not source of truth; users say "channels"/"portals"/"OTAs" |
| Owners & ownership | **Owners** (D2) + `Owner` + `ListingOwnerships {ownerId, share}` | `ownerId` opaque string; fractional `share` supported |
| PMC↔owner split | **Business Models** (D1, versioned; 6 counterparties) | users find term "Business Models" confusing — ask plainly |
| Channel (OTA) commission | **Channel Commission** (D1) | DISTINCT from PMC management commission above |
| Fees | **Additional Fees** (guest-invoice charges) | users say "cleaning fee"; cleaning handled per-property |
| Taxes | **Tax Configuration** (per-listing or account-wide) | **human-verified** before activation (Path H) |
| Payments / split | **Payment Automation** (rules by channel/property/res type) | payment fields not on `Money`; live on `Invoice.billing` |
| Revenue recognition | **Recognized Revenue for Analytics** | **listing-level**, analytics-scoped: check-in/check-out/prorated |
| Non-refundable | **Rate Plans** (cancellation policy) | distinct from **Rate Strategy** (nightly rates) |
| Teammates / governance | **User Management** — `User` + `Role` (`roles[]` w/ `listingIds[]`) | roles admin/agent/cleaner; permissions listing-scoped |
| Website | **Guesty Websites** + **Booking Engine** | users merge the two; website = content, engine = checkout |
| Rate strategy | **Rate Strategy** (vs **PriceOptimizer**) | skip if external pricing tool present (PriceLabs/Wheelhouse) |
| Security deposit | **Damage Protection** (Shield) vs guest "security deposit" | NOT the trust-accounting "Advanced Deposit" |

---

## 7. Hardcoded starter-kit (NOT agent questions)

Per the responses-doc appendix, these are **auto-provisioned on account creation**,
independent of answers — they belong to the profile as `source: hardcoded_starter` but are
**out of the agent's question scope** (and out of the baseline tree). They feed the brief's
"What's been auto-set-up" block.

- 5 auto-messages in DRAFT (booked / cancelled / altered / owner-stay / long-stay) + gap-night custom
- Sample **test listing** (Pro), marked as test
- Saved-reply library (listing level)
- Auto-response toggles (all ON) with fixed texts
- Owner portal defaults
- Promotions (all created then DISABLED) — length-of-stay + early-bird
- Guest app shell (logo from brand)
- Rate-strategy defaults by country (holidays, weekend, high/low season)

---

## 8. Validation checklist (schema ↔ sources)

| Source | Covered by schema? |
|--------|--------------------|
| Prototype field IDs (`listing_count`, `channels`, `go_live`, `cleaning_system`, `revenue_recognition`, `nonrefundable`, `pay_timing`, `split_type`, `fees_list`, `taxes`, `owner_split`, `teammates_count`, `focus_topics`, `pain`, `owners_csv`, `rate_strategy`, `logo_file`) | ✅ all mapped |
| Prototype branching (`pay_timing==split`, channels `airbnb_only`, oauth gate) | ✅ split kept; oauth **removed** per CEO; channels confirm-only |
| Financials script field_ids + tools (`add_fee`, `add_tax`, `flag_for_call_1`, `skip_question`, `end_section`, echo-before-write) | ✅ §4 S4 + §5 |
| SF intake (`account_name`…`ob_specialist_name`, `third_party_tools`) | ✅ §4 S0a |
| Sales handover note (611 real notes) → AI-extracted prefill (`migration_source`, `ob_language`, `addon_intent`, `customer_sentiment`, `risk_flags`…) | ✅ §4 S0b (v0.3); corpus analysis companion |
| OB brief sections (Brand, Properties&Channels, Operations, Financials, Booking Website, Governance) | ✅ S1–S6 + S7/S8 |
| Entity model (Owner, ListingOwnerships, BusinessModel, etc.) | ✅ §6 |
| CEO ownership→management→commission example | ✅ §4 S8 hero branch |
| CEO "Airbnb connection inside the product" | ✅ S2 note (oauth removed) |

---

## 9. Validation log (knowledge-base pass, 2026-06-02)

Cross-checked against `Tahini/knowledge`: `product-glossary.md`, `d1-financials.md`,
`d2-operations.md`, `product-model/er-core.md`. Status: **✅ confirmed · ✏️ corrected · ⚠️ needs human SME**.

| Item | Status | Evidence / change |
|------|--------|-------------------|
| `revenue_recognition` options | ✏️ corrected | `split_nights` → `prorated`; canonical "Recognized Revenue for Analytics"; **listing-level** (d1 support escalation #6) |
| `non_refundable_enabled` mapping | ✅ confirmed | Rate Plan / cancellation policy (distinct from Rate Strategy) |
| `mandatory_fees` → Additional Fees | ✅ confirmed | Glossary; users say "cleaning fee"; cleaning excluded |
| `taxes` types + scope | ✏️ corrected | Added `scope: listing|account_wide`; types aligned to city/tourism/GST/sales-VAT; still ⚠️ on exact enum casing |
| `payment_timing`/`split` → Payment Automation | ✅ confirmed | Glossary def matches Path C behavior |
| Owner "commission" ambiguity | ✏️ corrected | Split into **PMC commission (Business Models)** vs **Channel Commission (OTA fees)** |
| Teammate roles | ✏️ corrected | `admin/agent/cleaner/custom` + listing-scoped permissions (`roles[]` w/ `listingIds[]`) |
| Security deposit vs Advanced Deposit | ✏️ clarified | Damage Protection (Shield) ≠ trust-accounting Advanced Deposit |
| Multi-unit / combo properties | ✅ confirmed real | d2 §5 "combo properties / Multi-unit Management" — model in `listings` refs |
| Entity field paths (e.g. tax write target) | ⚠️ needs SME | Glossary gives surfaces, not field paths — confirm with data-model owners |
| `required` vs `recommended` priorities | ⚠️ needs SME | My judgment; onboarding team must ratify the MVP line (§3.1) |
| Booking Website (S5) in questionnaire scope | ✅ resolved 2026-06-02 | AI-judgment call: surface S5 only when direct-booking signals present in conversation |

### Specific questions for the product-data / onboarding SME
1. Exact write paths for **Tax Configuration**, **Additional Fees**, **Recognized Revenue for Analytics**, and **Payment Automation** (field-level, not just surface).
2. Canonical enum casing for tax types and `what_taxed` line items.
3. Is **non-refundable** a global Rate Plan toggle or per-listing/per-rate-plan?
4. For **mixed/managed** owners, does the agent create **Business Models** during onboarding, or only capture intent for Jordan to configure? (Affects `human_handoff` on the hero branch.)
5. **MVP-completeness line** ratification (§3.1) — which fields truly block account creation.
6. **Booking Website** — in questionnaire scope, or fully in-product like Airbnb connect?

---

## 10. NLU vocabulary normalization (agent aid)

Onboarding users rarely use canonical Guesty terms. The agent's intent/slot layer must map
user vocabulary → canonical slot (research §3, mechanism 2/3). High-frequency mappings from
the glossary's Modjo-call analysis:

| User says | → Canonical slot/term | Schema field |
|-----------|----------------------|--------------|
| "prices" / "my prices" | Rate Strategy / Rate Plans | `rate_strategy`, `non_refundable_enabled` |
| "cleaning fee" | Additional Fees (but cleaning is per-property) | `mandatory_fees` (exclude cleaning) |
| "channels" / "portals" / "OTAs" | Distribution / Channel Manager | `channels` |
| "owner login" / "owner access" | Owners Portal | (starter-kit / owners) |
| "business model" (confused) | Business Models (PMC↔owner split) | `owners[].management_model` |
| "security deposit" | Damage Protection vs Advanced Deposit (disambiguate) | `security_deposit_type` |
| "payout" | Disbursements vs Owner Statements | (downstream, not a question) |
| "PriceLabs" / "Wheelhouse" | external pricing tool (≠ PriceOptimizer) | `third_party_tools.pms_or_pricing` → skip `rate_strategy` |
| "host channel fee" / "accommodation fare" | Airbnb terms → map to Channel Commission / nightly rate | `owners[].who_pays_channel_commission` |

> **Implication for the hero branch:** when asking about owner economics, the agent should
> use plain language ("How do you get paid for managing these — a % commission, a flat fee,
> or a revenue split?") rather than the term "Business Models," which users find confusing.

---

## 11. Changelog

- **v0.3 (2026-06-02)** — **Sales handover-note prefill layer.** Added a second Salesforce seed layer (S0b) driven by the rep's free-text handover note (611 real notes; see corpus analysis companion). New `source: ai_extracted_from_note`; new fields `handover_note_raw`, `migration_source`, `prior_pms_experience`, `ob_language`, `tech_level`, `addon_intent`, `customer_sentiment`, `risk_flags`. Added source-precedence rule (`user_stated > sf_prefill > ai_extracted_from_note`), `provenance` + `prefilled_unconfirmed` runtime state, and the "confirm-don't-assume" / "prefill-don't-interrogate" invariants. Renamed S0 → S0a.
- **v0.2 (2026-06-02)** — Knowledge-base validation pass. Corrected revenue-recognition enum + scope, tax scope, teammate roles; disambiguated PMC vs Channel commission; clarified security-deposit vs Advanced-Deposit; added canonical terms, NLU vocabulary map (§10), validation log (§9). Outstanding items routed to SME questions.
- **v0.1 (2026-06-02)** — Initial synthetic schema from prototype, scripts, SF intake, brief, entity model.
