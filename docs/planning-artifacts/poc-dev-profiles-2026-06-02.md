---
title: "PoC Dev / Tuning Profiles — DO NOT SCORE"
author: "Mary (Business Analyst)"
date: 2026-06-02
version: 1.0
status: draft
purpose: "Tuning-only respondent profiles for prompt + decision-tree iteration. Kept physically separate from the scored 8 to guarantee no train/test leakage (PoC plan §5.1)."
companions:
  - "poc-respondent-specs-2026-06-02.md (the SCORED 8 — never tune on these)"
  - "poc-plan-ai-adaptive-onboarding-2026-06-02.md §5.1"
  - "guesty-pro-account-creation-schema.md v0.3"
  - "sales-handover-notes-corpus-analysis-2026-06-02.md (archetypes A–F)"
---

# PoC Dev / Tuning Profiles

> ## ⛔ ANTI-LEAKAGE BANNER — READ FIRST
> These profiles exist **only** to tune the agent system prompt and to author/debug the baseline
> decision tree. They are **never scored** and **never reported**. The scored 8
> (`poc-respondent-specs-2026-06-02.md`) must remain **untouched during all tuning**: the team
> freezes them, runs them **once**, and reports that single run (PoC plan §5.1 / §4.1).
>
> **Hard rules:**
> 1. No name, location, listing count, owner, or note from the scored 8 appears here (verified — see Appendix).
> 2. Anyone who reads or edits a scored profile during tuning has contaminated the eval; restart with a fresh frozen set.
> 3. The baseline-tree author works from the **schema**, blind to *both* sets where feasible; dev profiles are for debugging the tree's mechanics, not for fitting it to expected outputs.

---

## How dev profiles differ from scored profiles

| | Scored 8 | Dev profiles |
|---|---|---|
| Used for | Frozen single-run measurement (SAR, etc.) | Iterating the prompt / tree until they behave |
| Answer key | Full, reviewer-validated, frozen | **Tuning targets only** (what "good" looks like — not a graded key) |
| Coverage goal | Representative of the corpus | **Stress the same dimensions** so tuning generalizes |
| Mutability | Frozen | Freely editable while tuning |

Dev profiles deliberately cover the **same challenge dimensions** as the scored set (happy path,
one-clarifying-question ambiguity, vocabulary mismatch, hero-branch fan-out, financials deferral,
S0b extraction + abstention) with **different surface facts**, so a prompt/tree that generalizes on
dev has a fair chance on the frozen set.

---

## D1 — Happy path, self-owned, NO direct channel
*Anchor: archetype A (migration + add-on), no website signal. Mirrors A1's role but inverts the S5 trigger.*

- **Facts:** "Cedar Hollow Stays," Asheville NC alt — *use a non-scored locale*: **Bend, Oregon**. 4 self-owned cabins. Channels: Airbnb + Booking (no direct). Revenue recog: check-in. Non-refundable: no. Deposit: $0 / damage protection (Bronze). Payment: full at booking. Cleaning fee $95/stay. Taxes: OR has no state sales tax → city transient lodging tax 10.4% only. Solo operator. Focus: channel_mix, guest_messaging.
- **Persona:** Cooperative, concise, standard vocabulary. Confirms echoes immediately.
- **Handover note (S0b seed):** *"Bend OR, 4 self-owned cabins. Airbnb + Booking, no direct. Coming off spreadsheets. Wants Bronze damage protection. Cleaning fee per stay. Channel expansion is the goal."*
- **Tuning focus:** Baseline completion on the full frame; **S5 correctly NOT surfaced** (no direct signal); single-jurisdiction tax still flagged; damage_protection vs deposit disambiguation.

## D2 — Single managed owner, commission (simplest hero branch)
*Anchor: archetype B (managed-for-owners), minimal fan-out. Hero-branch entry without C-level complexity.*

- **Facts:** "Tidewater Co," Charleston SC alt → **Savannah, GA**. 6 listings: 4 self + 2 managed for one owner ("Dana Whitfield," dana@…). 2 listings, 15% commission of gross. Owner pays channel commission (deducted before split). Channels: Airbnb + VRBO. Payment: full at booking. Focus: owner_reporting.
- **Persona:** Knows PM vocabulary; gives owner details in one pass.
- **Handover note (S0b seed):** *"Savannah GA mgmt co. 6 listings, 4 own + 2 managed for one owner on 15% commission. Airbnb + VRBO. Wants owner statements. Straightforward."*
- **Tuning focus:** Hero-branch **entry** on `ownership_model: mixed`; **echo-before-write** on the 15% rate; `recorded + flag_for_call_1` disposition (G1 intent-capture); confirm-from-note (managed owner already known).

## D3 — Multi-unit / combo ambiguity (one clarifying question)
*Anchor: archetype A + multi-unit signal (9.3% of corpus). Tests the count/unit clarifying question.*

- **Facts:** "Alpenblick Apartments," → **Innsbruck, Austria**. "8 listings" — but it's 1 building with 8 apartments, plus 1 combo listing that rents the whole building. So 8 units + 1 combo = 9 sellable listings. Self-owned. Channels: Airbnb + Booking. OB language: English fine. Focus: channel_mix.
- **Persona:** Says "8 apartments, and I also rent the whole place sometimes." Ambiguous on whether the combo is a 9th listing until asked.
- **Handover note (S0b seed):** *"Innsbruck, 1 building w/ 8 apartments + sometimes rents whole building (combo). Self-owned. Airbnb + Booking. Multi-unit setup needed."*
- **Tuning focus:** **One clarifying question** to resolve units vs. combo (not zero, not three); multi-unit modeling note; extraction surfaces `multi_unit` risk/structure hint.

## D4 — Financials PARTIAL deferral (tax only, not whole section)
*Anchor: archetype C (sentiment) but milder. Distinguishes per-field flag from whole-section skip — the inverse of scored B4.*

- **Facts:** "Lago Azul Rentals," → **Tulum, Mexico**. 7 self-owned. Answers payment (full at booking), deposit ($150 damage waiver), non-refundable (yes), cleaning fee (MXN 600). **Defers only taxes** ("my accountant handles Mexican lodging tax, set that up with the specialist"). Channels: Airbnb + Booking + direct site.
- **Persona:** Comfortable with most money topics; specifically punts taxes to a professional.
- **Handover note (S0b seed):** *"Tulum, 7 self-owned. Airbnb/Booking + own site. Fine on pricing/fees; accountant handles MX lodging tax — wants to set tax up live with specialist."*
- **Tuning focus:** **Per-field flag** (`taxes → flagged`) while the rest of S4 records normally — distinct from B4's whole-section skip; S5 surfaces (direct site); tax-always-flag invariant.

## D5 — Sparse note + non-English OB (S0b extraction + abstention)
*Anchor: archetype F (sparse) + language signal. Primarily a Component-6 / S0b tuning profile.*

- **Facts:** "Conciergerie du Lac," → **Annecy, France**. 5 managed for owners. OB must be in **French**. Channels: Airbnb + Booking. Migration from a competitor (Smoobu). Otherwise sparse — rep wrote little.
- **Persona:** Non-native English; prefers French; gives short answers.
- **Handover note (S0b seed):** *"Annecy. 5 listings managed for owners. OB en français svp. Coming off Smoobu."* *(short, mixed-language — realistic)*
- **Tuning focus:** S0b extraction of `ob_language: fr`, `migration_source: smoobu`, `ownership_model: managed`; **abstention** on everything the short note doesn't state (no invented taxes/fees/deposit); `tech_level`/sentiment left null when absent.

## D6 — Mid/long-term excluded listings (scope handling)
*Anchor: archetype "mid/long-term / arbitrage" (2.1%). Tests partial-portfolio scope.*

- **Facts:** "Gulf Coast Holdings," → **Mobile, Alabama**. 12 properties total but **only 7 are short-term** (5 are long-term tenancies excluded from Guesty). Self-owned. Channels: Airbnb + VRBO. Focus: automation.
- **Persona:** Clarifies that long-term units "don't go on the system."
- **Handover note (S0b seed):** *"Mobile AL, 12 properties but only 7 STR — 5 are long-term, won't be on Guesty. Self-owned, Airbnb + VRBO. Wants automation."*
- **Tuning focus:** `listing_count` reflects **in-scope 7**, not 12; `risk_flags:[mid_long_term_excluded]`; agent doesn't try to onboard excluded units.

---

## Appendix — Leakage check (dev vs scored)

| Dimension | Scored set values | Dev set values | Collision? |
|-----------|-------------------|----------------|-----------|
| Locales | Sarasota, Key West, Breckenridge, Asheville, Santa Fe, Lake Tahoe, Lake Norman | Bend, Savannah, Innsbruck, Tulum, Annecy, Mobile | ✅ none |
| Business names | Harbor Point, Coastal Keys, Summit Stay, Blue Ridge, Olive Tree, Alpine, Lakeside | Cedar Hollow→Bend, Tidewater→Savannah, Alpenblick, Lago Azul, Conciergerie du Lac, Gulf Coast | ✅ none |
| Owner names | Maria Chen, Tom Walsh, Pat Okafor, Diane Novak, Chris Lim, Sarah Mitchell, James Park, Claudia Reyes, Marcus Webb, Grantham | Dana Whitfield (+ generic owners) | ✅ none |
| Listing counts | 5, 8, 12, 10, 6, 12, 20 | 4, 6, 9, 7, 5, 7(of 12) | ⚠️ 6 & 12 reused as counts — acceptable (counts are not identifying); facts otherwise disjoint |

> **Sign-off required:** the tuning lead confirms no scored-profile content leaked into dev before
> tuning begins, and that the scored set file's checksum is unchanged at run time.
