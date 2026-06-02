---
title: "Sales → Onboarding Handover Notes — Corpus Analysis & Prefill-Extraction Design"
author: "Mary (Business Analyst)"
date: 2026-06-02
version: 1.0
status: draft
source_file: "Notes for Tamar-2026-06-02-13-51-50.xlsx (Salesforce export)"
companions:
  - "guesty-pro-account-creation-schema.md"
  - "poc-plan-ai-adaptive-onboarding-2026-06-02.md"
  - "research/ai-adaptive-questionnaire-onboarding-research-2026-06-02.md"
---

# Sales → Onboarding Handover Notes — Corpus Analysis

> **One line.** Before sales sends a closed-won account the onboarding link, the rep writes a
> free-text handover note ("wants locks, nervous about Airbnb, coming off Hostaway, French OB").
> The onboarding specialist reads it. **This note is a real, unstructured prefill source** — and
> turning it into structured starter-kit prefill is a textbook case where an LLM beats rules.

---

## 1. What this file is

A Salesforce report titled **"Notes for Tamar,"** generated 2026-06-02 by Ella Ofir.

**Filters (from the export header):**
- Close Date = current fiscal quarter (01/04/2026 – 30/06/2026)
- Stage = Closed Won (Billing in)
- Customer Onboarding Preference = Onboarding

**Columns:** `Opportunity Owner` (sales rep) · `Account Name` · `Number of Listings` · `Opportunity Name` · **`Notes`** (free text).

**Volume:**
- **643** closed-won account rows
- **611** with substantive notes (32 are `NA`/`N/A`/blank)
- Note length: min 2 / **median 155** / **max 255** characters

> ⚠️ **Truncation caveat.** The max length is *exactly* 255 characters across the corpus — the
> export caps the Notes preview at 255 chars. **Real Salesforce notes are longer than what we
> see here.** Every frequency below is a **lower bound**; the production extractor would run on
> full note text, not this truncated preview.

> ⚠️ **PII caveat.** The raw notes contain real customer names, personal emails, and deal terms.
> This analysis uses **paraphrased / de-identified** examples only. The raw file must **not** be
> committed to the repo; handle under the same controls as Salesforce contact data. See §7.

---

## 2. Why this matters (the connective insight)

The schema (`guesty-pro-account-creation-schema.md`) already models a **structured** Salesforce
seed (S0: `account_name`, `country`, `listing_count`, `connected_channels`, `third_party_tools`…).
This file reveals the **second, unstructured Salesforce layer** sitting right next to it: the
rep's narrative. Two consequences:

1. **New prefill source.** The handover note is a distinct `source` from structured `sf_prefill`.
   It carries signals the structured fields don't (sentiment, fears, OB language, migration
   source, add-on intent, business model) — exactly the things that should *pre-seed* the
   questionnaire and the starter kit so the agent doesn't ask what sales already learned.

2. **The cleanest AI-value case we have.** A deterministic rule/regex layer can pull a few
   keywords, but it cannot reliably turn *"Nestor and Jimena are both owners and managers,
   starting with 6 of 18 listings, still fuzzy on payment processing"* into structured slots +
   a risk flag. **Free-text → structured slots is the canonical unbounded-input task** the
   research report (§4.1) names as where AI is categorically better than a tree. And now we have
   **611 real examples** to prove it on, instead of only synthetic profiles.

---

## 3. Signal taxonomy (measured across the 611 substantive notes)

Keyword-based lower bounds (truncation + paraphrase mean true rates are higher — that gap is the
AI opportunity). Each signal maps to a schema slot it should **prefill or flag**.

| Signal | Lower-bound freq | Maps to schema |
|--------|-----------------|----------------|
| Migration from a competitor PMS | 25.7% (157) | `third_party_tools.pms_or_pricing` + new `migration_source` + `prior_pms_experience` |
| Revenue mgmt / dynamic pricing (GPO, PriceLabs, Wheelhouse, Beyond) | 21.3% (130) | `third_party_tools.pms_or_pricing` → skip `rate_strategy`; `focus_topics: pricing_strategy` |
| Channels named (Airbnb / VRBO / Booking / Expedia / Agoda) | 16.7% (102) | `channels` (confirm, don't ask) |
| Accounting / owner statements / trust accounting | 16.2% (99) | `focus_topics: accounting_setup / owner_reporting`; signals managed model |
| Growth / expansion plans | 14.2% (87) | `go_live` pace; Call-1 agenda; `listing_count` (start-vs-target) |
| Booking website / direct / ABW | 12.1% (74) | **S5 direct-booking signal** (G6 trigger) |
| Locks / smart access (Schlage, Nuki, Eufy, RemoteLock, GLM) | 9.8% (60) | `third_party_tools.locks`; S3 `checkin_method: self_checkin` |
| Damage Protection / Shield / S&P (often **mandatory**) | 9.3% (57) | `security_deposit_type: damage_protection`; **mandatory flag** |
| Multi-unit / combo / hotel-like / rooms | 9.3% (57) | listing modeling (Property/Complex), multi-unit flag |
| Risk / sentiment cues (worried, neutral, careful, frustrated, "smooth," "mandatory") | 7.4% (45) | **new `customer_sentiment` / `risk_flags`** (Call-1 handling) |
| First-time / never used a PMS / fully manual | 7.2% (44) | `prior_pms_experience: none`; OB pacing; needs-guidance |
| GuestyPay / payment processing (incl. Stripe) | 6.1% (37) | `payment_*`; processor intent; sometimes "confused about payments" → flag |
| Go-live urgency (ASAP / eager / live-by-date) | 5.7% (35) | `go_live: asap` |
| Managed-for-owners signals (on behalf of, conciergerie, exclusivity) | 4.4% (27) | **`ownership_model` hero-branch prefill** |
| HQ / sub-accounts (nesting) | 3.8% (23) | account-structure flag (out of single-account scope) |
| Tech-savvy | 2.6% (16) | OB pacing / communication style |
| French OB required | 2.5% (15) | **new `ob_language: fr`** |
| Mid/long-term / arbitrage | 2.1% (13) | business-model nuance; some listings excluded |
| Not tech-savvy / needs step-by-step | 1.5% (9) | OB pacing; communication style |
| Spanish OB required | 1.3% (8) | **new `ob_language: es`** |

**Reading the table:** the most valuable extraction targets (migration source, pricing tools,
managed-vs-owned, OB language, mandatory add-ons, sentiment/risk) are *narrative* signals that
the current structured S0 does **not** capture — and several map directly to gates we already
resolved (S5 direct-booking trigger; hero-branch `ownership_model`).

---

## 4. De-identified note archetypes

Representative shapes (names/emails/figures changed). These become grounding for PoC respondent
profiles (PoC plan §5) and labeled examples for the extraction eval (§6 below).

**Archetype A — Migration + add-on bundle (most common).**
> *"GFH upgrade. 4 listings. Currently just on Airbnb, wants VRBO. Pricing done manually using
> AirDNA. Will use Guesty Shield DP (Bronze)."*
→ `migration_source: guesty_for_hosts`, `channels:[airbnb]` + intent `[vrbo]`,
`third_party_tools.pms_or_pricing:[airdna]`, `security_deposit_type: damage_protection`,
`focus_topics:[channel_mix, pricing_strategy]`.

**Archetype B — Managed-for-owners / hero branch.**
> *"Co-owner of 25 managed properties. Came off [competitor] over connectivity issues. Listed on
> Airbnb, Booking, VRBO."*
→ `ownership_model: all_managed_for_others`, `listing_count: 25`, `migration_source: <x>`,
`channels:[airbnb, booking, vrbo]`, `focus_topics:[owner_reporting]`.

**Archetype C — Sentiment / risk-flagged.**
> *"Smart user, very worried about the OB stage. Has A LOT of add-ons — set everything up calmly.
> Demanding but technical."*
→ `customer_sentiment: anxious`, `risk_flags:[high_addon_complexity, white_glove_expected]`,
`tech_level: high`.

**Archetype D — Language + pacing.**
> *"OB in French. Aware onboarding takes ~1 month. Expects step-by-step guidance and task
> tracking."*
→ `ob_language: fr`, `go_live: 1-2m`, `tech_level: low`, `focus_topics:[guided_setup]`.

**Archetype E — Payment confusion (flag, don't resolve).**
> *"Both owner and manager, starting with 6 of 18 listings. Still confused about payment
> processing — explained multiple times, didn't fully grasp it."*
→ `ownership_model: mixed`, `payment_*: flag_for_call_1 (confusion noted)`,
`risk_flags:[payment_comprehension]`.

**Archetype F — Sparse (regex would get ~nothing).**
> *"Base PMS + Locks. Very tech savvy."*
→ `third_party_tools.locks: true`, `tech_level: high`. (Short, but still structured signal.)

---

## 5. Proposed extraction-prefill flow

```
Salesforce closed-won
      │
      ├─ structured fields ──────────────► S0 sf_prefill        (existing; high confidence)
      │
      └─ handover note (free text) ──► [ LLM extractor ] ──► prefill candidates
                                              │                 source: ai_extracted_from_note
                                              │                 confidence: 0.0–1.0
                                              ▼                 provenance: <quoted span>
                                   merge into starter-kit seed
                                              │
                                   ┌──────────┴───────────┐
                                   ▼                      ▼
                        high-confidence slots      low-confidence / risk
                        → pre-filled, agent         → agent asks to CONFIRM,
                          confirms ("Sales said       never assumes; risk_flags
                          you're on Airbnb +          surface in the OB brief
                          VRBO — still right?")       for Jordan
```

**Design rules (carry into the schema):**
1. **Extracted ≠ asserted.** Note-derived slots are *hints to confirm*, never silent truths.
   Every one carries `confidence` + `provenance` (the source span) and is echoed before write.
2. **Sentiment/risk never auto-acts.** `customer_sentiment` and `risk_flags` route to the OB
   brief and Call-1 agenda; the agent does not change behavior unilaterally on them.
3. **Note loses to structured + user.** Precedence: `user_stated` > `sf_prefill` (structured) >
   `ai_extracted_from_note`. Conflicts surface (`⚠️ Note said Hostaway; user says Lodgify`).
4. **Skip-what-we-know.** A high-confidence extracted slot lets the agent *confirm* instead of
   *ask* — this is the direct line to the user's "prefill the starter kit" goal and to fewer
   questions (PoC secondary metric "questions to completion").

---

## 6. How this plugs into the PoC

This corpus upgrades the PoC from "synthetic-only" to "grounded in real input," and adds a
**second, independently falsifiable AI-value claim**:

- **Claim H2 (note → prefill extraction).** *Given a real handover note, an LLM extractor fills
  more correct prefill slots — and flags more legitimate risks — than a rules/regex baseline,
  at acceptable precision.* This is the unbounded-input case the tree provably cannot do.
- **Eval set.** Hand-label a stratified sample (~40–60 notes spanning the §4 archetypes) into
  gold prefill slots + risk flags. Score extractor vs. regex baseline on **slot precision/recall**
  and **risk-flag quality** (blind raters, per PoC plan §6.3). Hold out a dev subset for prompt
  tuning (no leakage; PoC plan §5.1).
- **Grounding for profiles.** The 8 respondent specs (`poc-respondent-specs-2026-06-02.md`) can
  now be **anchored to real archetypes** (A–F above) instead of invented from scratch — cheaper
  to defend and more representative.

See the new component added to `poc-plan-ai-adaptive-onboarding-2026-06-02.md`.

---

## 7. Data governance / open items

| Item | Status / action |
|------|-----------------|
| Raw notes contain PII (names, personal emails, deal terms) | **Do not commit raw file.** De-identify before any labeling; restrict access. |
| Export truncates at 255 chars | Re-pull full note text from Salesforce for production extraction + labeling. |
| Labeling effort (~40–60 notes) | Needs an owner + a 2-rater protocol (reuse PoC §6.3 raters). |
| Note quality varies (2 → 255 chars; 32 are `NA`) | Extractor must degrade gracefully on sparse/empty notes (Archetype F). |
| Field availability in real SF | Confirm the note field + structured fields are reliably populated at handoff time (SME). |

---

## 8. Recommended next steps

1. Add the extraction layer + new fields to the schema (done in v0.3 — see schema changelog).
2. Add Claim H2 + the extraction component to the PoC plan (done — see plan changelog).
3. Re-pull **full-length** notes from Salesforce (de-identified) for a labeling pass.
4. Anchor the 8 respondent specs to archetypes A–F.
