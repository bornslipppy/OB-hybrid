---
title: "PoC Respondent Specifications — Guesty Pro Onboarding Agent"
---

# PoC Respondent Specifications — Guesty Pro Onboarding Agent
**Version:** v1.2-frozen  
**Date:** 2026-06-02  
**Status:** ✅ FROZEN — reviewer pass complete (Yair Cohen, single reviewer per protocol); all changes adjudicated and applied; ready for eval  
**Dependencies:** Schema v0.3 (G1/G6 resolved, S0b added); PoC plan v1.2 §5 + Component 6; corpus analysis 2026-06-02; G3 (S4 enum casing) provisional

---

## Overview

Eight respondent specs organized into three groups, each covering a distinct challenge dimension. Each spec has four parts:

1. **Ground-truth facts** — the business reality the respondent knows and can state.
2. **Persona directive** — how the respondent communicates (style, vocabulary, behavior under pressure).
3. **Answer key** — the expected disposition per in-scope slot (below).
4. **Sales handover note (S0b seed) + expected extraction** — consolidated in **Appendix C**. The synthetic note (≤255 chars, de-identified, modeled on real corpus archetypes) is what the rep would have written; it seeds the S0b prefill layer and lets the PoC test the *confirm-don't-ask* behavior and Claim H2.

> **Archetype anchoring (v1.1).** Each profile is now tied to one or more real note archetypes (A–F) from `sales-handover-notes-corpus-analysis-2026-06-02.md`, so the synthetic profiles are representative of the 611-note corpus rather than invented. See the anchor table in Appendix C.

**Answer-key dispositions:**
   - `recorded: <value>` — agent should capture this exact value
   - `recorded: <value> [provisional G3]` — value is correct in intent but enum casing may change when G3 resolves
   - `flag_for_call_1` — agent captures context and flags for Jordan to configure
   - `flagged: <reason>` — agent flags this field (tax, advice-seek, or confirmed ambiguity)
   - `skipped` — agent legitimately does not ask / respondent explicitly defers
   - `conditional: surface_if_direct_signals` — S5 fields, per G6 resolution

**SAR denominator** for each profile = count of all `required` + `recommended` slots where expected disposition ≠ `skipped`. G3-provisional slots count if scored before G3 resolves; re-freeze if G3 closes before eval run.

**Hero-branch rule (G1):** Owner fields (name, email, listings, share) → `recorded`. Owner economics (management model, rates, split terms, who pays channel commission) → `recorded` + `flag_for_call_1`. BusinessModel creation itself = out of agent scope.

**S5 rule (G6):** Surface only when direct-booking signals present. Default disposition = `conditional: surface_if_direct_signals`.

---

## Group A — Clean Happy Path

*Cooperative respondents, clear vocabulary, no ambiguity. Tests whether the agent completes the core frame reliably. Establishes the SAR ceiling. User-simulator: scripted turns.*

---

### A1 — Clear-cut self-owner, direct booking channel

**Purpose:** Simplest possible profile. All self-owned, standard pricing, mentions "direct" as a channel → S5 surfaces. Tests baseline slot accuracy on the full schema.

---

#### Ground-truth facts

| Field | Value |
|-------|-------|
| **Business name** | Harbor Point Rentals |
| **Location** | Sarasota, Florida |
| **Listings** | 5 self-owned vacation rentals |
| **Channels** | Airbnb, VRBO, direct bookings via own website |
| **Ownership model** | Self-owned (no managed properties) |
| **Revenue recognition** | Check-in date |
| **Non-refundable rates** | No |
| **Security deposit** | $50 damage waiver (not a traditional deposit) |
| **Payment timing** | Full payment at booking |
| **Mandatory fees** | Cleaning fee: $85/stay for all units |
| **Taxes** | Florida state sales tax 6% + Sarasota county tourist development tax 2% |
| **Teammates** | None (solo operator) |
| **Focus topics** | Pricing strategy, guest messaging |
| **Pain** | "Manual pricing takes too much time. I'm adjusting rates by hand every morning." |
| **Website** | Harbored in product; brand = "Harbor Point Stays"; wants Guesty subdomain |
| **Website terms** | Guesty standard terms |

---

#### Persona directive

Cooperative, organized, answers every question directly and in full. Uses standard industry vocabulary (not Airbnb-specific jargon). Does not seek advice. Provides numbers without being asked twice. When the agent echoes back, confirms immediately. Does not volunteer off-topic information. Response style: short, professional sentences.

---

#### Answer key

**S1 — Business profile (prefill validation)**

| Slot | Expected disposition |
|------|---------------------|
| `business_name` | `recorded: Harbor Point Rentals` |
| `location` | `recorded: Sarasota, FL` |
| `listing_count` | `recorded: 5` |

**S2 — Channels**

| Slot | Expected disposition |
|------|---------------------|
| `channels` | `recorded: [airbnb, vrbo, direct]` |
| `airbnb_oauth` | `skipped` (handled in-product, not in questionnaire per CEO) |

**S3 — Operations**

| Slot | Expected disposition |
|------|---------------------|
| `checkin_method` | `recorded: self_checkin` *(or equivalent — respondent says "lockbox")* |
| `cleaning_managed_by` | `recorded: external_team` *(or "I coordinate a cleaner")* |

**S4 — Financials** *(G3 provisional on tax enum casing)*

| Slot | Expected disposition |
|------|---------------------|
| `revenue_recognition` | `recorded: checkin_date` `[provisional G3]` |
| `non_refundable_enabled` | `recorded: false` |
| `security_deposit_type` | `recorded: damage_waiver` |
| `security_deposit_amount` | `recorded: 50` |
| `payment_timing` | `recorded: at_booking` |
| `payment_split` | `skipped` *(no split — full amount)* |
| `mandatory_fees` | `recorded: [{fee_type: cleaning_fee, amount: 85, per: stay}]` |
| `taxes[0].tax_type` | `recorded: sales_tax` `[provisional G3]` |
| `taxes[0].rate` | `recorded: 6` |
| `taxes[0].scope` | `recorded: account_wide` |
| `taxes[0].jurisdiction` | `flagged: confirm_filing` *(agent records state=FL but always flags taxes for Jordan)* |
| `taxes[1].tax_type` | `recorded: tourist_tax` `[provisional G3]` |
| `taxes[1].rate` | `recorded: 2` |
| `taxes[1].scope` | `recorded: account_wide` |
| `taxes[1].jurisdiction` | `flagged: confirm_filing` |

**S5 — Booking Website** *(triggered: "direct" in channels)*

| Slot | Expected disposition |
|------|---------------------|
| `website_brand_name` | `recorded: Harbor Point Stays` |
| `website_domain` | `recorded: guesty_subdomain` |
| `website_terms` | `recorded: guesty_terms` |

**S6 — Governance**

| Slot | Expected disposition |
|------|---------------------|
| `teammates` | `skipped` *(solo operator, no teammates to add)* |

**S7 — Focus**

| Slot | Expected disposition |
|------|---------------------|
| `focus_topics` | `recorded: [pricing_strategy, guest_messaging]` |
| `pain` | `recorded: "Manual pricing takes too much time. Adjusting rates by hand every morning."` |

**S8 — Business / Ownership**

| Slot | Expected disposition |
|------|---------------------|
| `ownership_model` | `recorded: self_owned` |
| `owners` | `skipped` *(no managed properties)* |
| `rate_strategy` | `recorded: dynamic` *(inferred from pain; agent may ask or infer)* |

---

### A2 — Simple managed, flat-fee commission

**Purpose:** Introduces the ownership branch with two managed owners on straightforward flat-fee structures. Split payment. Tests fan-out of hero branch at low complexity.

---

#### Ground-truth facts

| Field | Value |
|-------|-------|
| **Business name** | Coastal Keys Management |
| **Location** | Key West, Florida |
| **Listings** | 8 total: 5 self-owned + 3 managed |
| **Managed owner 1** | Maria Chen · maria@chen-properties.com · 2 listings · $200/month flat fee each |
| **Managed owner 2** | Tom Walsh · tomw@walsh.net · 1 listing · $150/month flat fee |
| **Channels** | Airbnb, Booking.com (no direct) |
| **Ownership model** | Mixed: self-owned + managed |
| **Revenue recognition** | Check-out date |
| **Non-refundable rates** | Yes (all listings) |
| **Security deposit** | Damage Protection product (no cash deposit) |
| **Payment timing** | Split: 50% at booking, 50% 7 days before arrival |
| **Mandatory fees** | None |
| **Taxes** | FL sales tax 6%, Monroe County tourist tax 4% |
| **Teammates** | 1 VA — Alex Rivera · alex@coastalkeys.com · viewer access, all listings |
| **Focus topics** | Owner reporting, channel mix |
| **Pain** | "Keeping owners happy with transparent reports." |

---

#### Persona directive

Organized and professional. Has managed properties before and knows the vocabulary ("management fee," "flat fee," "owner statement"). Provides owner details in one go when asked (doesn't need follow-up per owner). Confirms echo-backs promptly. No advice-seeking. Does not mention a website → S5 should not surface.

---

#### Answer key

**S1 — Business profile**

| Slot | Expected disposition |
|------|---------------------|
| `business_name` | `recorded: Coastal Keys Management` |
| `location` | `recorded: Key West, FL` |
| `listing_count` | `recorded: 8` |

**S2 — Channels**

| Slot | Expected disposition |
|------|---------------------|
| `channels` | `recorded: [airbnb, booking_com]` |

**S4 — Financials**

| Slot | Expected disposition |
|------|---------------------|
| `revenue_recognition` | `recorded: checkout_date` `[provisional G3]` |
| `non_refundable_enabled` | `recorded: true` |
| `security_deposit_type` | `recorded: damage_protection` |
| `security_deposit_amount` | `skipped` *(damage protection = no amount)* |
| `payment_timing` | `recorded: split` |
| `payment_split` | `recorded: {first_pct: 50, second_pct: 50, second_trigger: 7_days_before}` |
| `mandatory_fees` | `skipped` *(none stated)* |
| `taxes[0].tax_type` | `recorded: sales_tax` `[provisional G3]` |
| `taxes[0].rate` | `recorded: 6` |
| `taxes[0].jurisdiction` | `flagged: confirm_filing` |
| `taxes[1].tax_type` | `recorded: tourist_tax` `[provisional G3]` |
| `taxes[1].rate` | `recorded: 4` |
| `taxes[1].jurisdiction` | `flagged: confirm_filing` |

**S5 — Booking Website**

| Slot | Expected disposition |
|------|---------------------|
| All S5 slots | `conditional: surface_if_direct_signals` → not surfaced *(no direct-booking signal in this profile)* |

**S6 — Governance**

| Slot | Expected disposition |
|------|---------------------|
| `teammates[0].name` | `recorded: Alex Rivera` |
| `teammates[0].email` | `recorded: alex@coastalkeys.com` |
| `teammates[0].role` | `recorded: viewer` *(or closest enum)* |
| `teammates[0].listing_scope` | `recorded: all` |

**S7 — Focus**

| Slot | Expected disposition |
|------|---------------------|
| `focus_topics` | `recorded: [owner_reporting, channel_mix]` |
| `pain` | `recorded: "Keeping owners happy with transparent reports."` |

**S8 — Business / Ownership**

| Slot | Expected disposition |
|------|---------------------|
| `ownership_model` | `recorded: mixed` |
| `owners[0].owner_name` | `recorded: Maria Chen` |
| `owners[0].email` | `recorded: maria@chen-properties.com` |
| `owners[0].listings` | `recorded: 2` |
| `owners[0].management_model` | `recorded: flat_fee` |
| `owners[0].fixed_fee_amount` | `recorded: 200` |
| `owners[0].fee_per` | `recorded: per_listing_per_month` |
| `owners[0].who_pays_channel_commission` | `recorded: owner` *(OTA fees deducted before owner payout — standard for flat fee)* |
| `owners[0]` | `flag_for_call_1: Jordan configures BusinessModel for Maria Chen (2 listings, $200/mo flat fee)` |
| `owners[1].owner_name` | `recorded: Tom Walsh` |
| `owners[1].email` | `recorded: tomw@walsh.net` |
| `owners[1].listings` | `recorded: 1` |
| `owners[1].management_model` | `recorded: flat_fee` |
| `owners[1].fixed_fee_amount` | `recorded: 150` |
| `owners[1].fee_per` | `recorded: per_listing_per_month` |
| `owners[1].who_pays_channel_commission` | `recorded: owner` |
| `owners[1]` | `flag_for_call_1: Jordan configures BusinessModel for Tom Walsh (1 listing, $150/mo flat fee)` |

---

## Group B — Ambiguity & Robustness

*Cases that require the agent to ask one targeted clarifying question, handle vocabulary mismatches, or gracefully absorb a refusal without retry loops.*

---

### B1 — Channel-dependent payment

**Purpose:** The respondent's payment timing depends on the channel — a single enum slot is not enough. Tests whether the agent recognizes the ambiguity, asks one clarifying question, and records a structured answer rather than forcing a single enum value.

---

#### Ground-truth facts

| Field | Value |
|-------|-------|
| **Business name** | Summit Stay Co |
| **Location** | Breckenridge, Colorado |
| **Listings** | 12 self-owned ski-town rentals |
| **Channels** | Airbnb, VRBO, direct |
| **Ownership model** | Self-owned |
| **Revenue recognition** | Check-in |
| **Non-refundable** | Yes on select listings (mountain season) |
| **Security deposit** | $75 damage waiver |
| **Payment timing — direct channel** | 50% at booking, 50% two weeks before arrival |
| **Payment timing — OTA channels** | Collected by OTA at booking (not managed in Guesty) |
| **Mandatory fees** | $40 hot-tub fee (select properties) |
| **Taxes** | CO state sales tax 2.9%, Summit County lodging tax 2%, Breckenridge town tax 2.5% |
| **Focus topics** | Pricing strategy, accounting setup |
| **Pain** | "Reconciling what Airbnb and VRBO pay me with what's actually in the system. It's a mess." |

---

#### Persona directive

Detailed and thorough; volunteers channel-level breakdowns without being asked. When agent asks about payment timing, respondent answers: *"Depends on the channel — Airbnb and VRBO collect at booking, but for direct bookings I take half upfront and the other half two weeks out."* Does not simplify unless agent pushes. Does not seek advice. Mentions direct bookings unprompted when discussing channels.

---

#### Answer key

| Slot | Expected disposition |
|------|---------------------|
| `channels` | `recorded: [airbnb, vrbo, direct]` |
| `payment_timing` | Agent must ask one clarifying question to resolve ambiguity, then: `recorded: {ota_channels: collected_by_channel, direct: split}` |
| `payment_split` | `recorded: {first_pct: 50, second_pct: 50, second_trigger: 14_days_before}` *(direct channel only)* |
| `mandatory_fees` | `recorded: [{fee_type: hot_tub, amount: 40, per: stay, applies_to: select_listings}]` |
| `taxes[0].tax_type` | `recorded: sales_tax` `[provisional G3]` |
| `taxes[0].rate` | `recorded: 2.9` |
| `taxes[1].tax_type` | `recorded: lodging_tax` `[provisional G3]` |
| `taxes[1].rate` | `recorded: 2` |
| `taxes[2].tax_type` | `recorded: city_tax` `[provisional G3]` |
| `taxes[2].rate` | `recorded: 2.5` |
| All tax jurisdiction slots | `flagged: confirm_filing` |
| `website_brand_name` | `conditional: surface_if_direct_signals` → **SURFACE** *(direct bookings confirmed — agent should ask about booking website)* |
| `ownership_model` | `recorded: self_owned` |

**Key eval criterion:** Did the agent ask exactly **one** clarifying question for payment timing (not zero, not two)? Did it record the channel-conditional structure rather than defaulting to a single enum?

---

### B2 — Vague commission language

**Purpose:** The respondent has 3 owners with heterogeneous commission structures described imprecisely. Tests whether the agent can ask one targeted follow-up per owner to resolve ambiguity, rather than either accepting the vague answer or spiraling into interrogation.

---

#### Ground-truth facts

| Field | Value |
|-------|-------|
| **Business name** | Blue Ridge Partners |
| **Location** | Asheville, NC |
| **Listings** | 10 managed-for-owner |
| **Owner 1** | Pat Okafor · pat@okafor.com · 4 listings · ~18% commission (negotiated, not a fixed rate) |
| **Owner 2** | Diane Novak · dnovak@gmail.com · 4 listings · flat fee, "around $180 each, I think" |
| **Owner 3** | Chris Lim · clim@limgroup.biz · 2 listings · "we have a revenue share — he gets most of it" |
| **Who pays channel commission** | Owner (deducted before split for all) |
| **Revenue recognition** | Check-out |
| **Non-refundable** | No |
| **Security deposit** | None |
| **Payment** | Full at booking |
| **Mandatory fees** | None |
| **Taxes** | NC sales tax 4.75%, Buncombe County occupancy tax 6% |
| **Focus topics** | Owner reporting, accounting setup |
| **Pain** | "Explaining to owners why their payouts are different every month." |

---

#### Persona directive

Conversational and warm. Gives approximate figures ("around," "I think," "about"). When pushed for exact numbers, admits some uncertainty and provides ranges or says "let me check my contract." For Owner 3 (Chris Lim), is genuinely vague: "We have a verbal agreement — he gets 75% of whatever comes in after the OTA takes their cut." Does not volunteer information proactively; the agent must ask for each owner in sequence.

---

#### Answer key

| Slot | Expected disposition |
|------|---------------------|
| `ownership_model` | `recorded: managed_only` |
| `owners[0].owner_name` | `recorded: Pat Okafor` |
| `owners[0].email` | `recorded: pat@okafor.com` |
| `owners[0].listings` | `recorded: 4` |
| `owners[0].management_model` | `recorded: commission` |
| `owners[0].pmc_commission_rate` | `recorded: ~18` *(agent records approximate value; echo-back confirms "around 18%")* |
| `owners[0]` | `flag_for_call_1: Exact rate TBC; Jordan to confirm before configuring BusinessModel for Pat Okafor` |
| `owners[1].owner_name` | `recorded: Diane Novak` |
| `owners[1].management_model` | `recorded: flat_fee` |
| `owners[1].fixed_fee_amount` | `recorded: ~180` *(approximate; flag)* |
| `owners[1]` | `flag_for_call_1: Amount approximate; Jordan to confirm before configuring for Diane Novak` |
| `owners[2].owner_name` | `recorded: Chris Lim` |
| `owners[2].management_model` | `recorded: revenue_split` |
| `owners[2].split_terms` | `recorded: "Owner receives 75% of revenue after OTA/channel fees are deducted"` *(75% must come from a follow-up question — "he gets most of it" is not sufficient; agent must ask e.g. "What percentage does Chris keep?" before recording)* |
| `owners[2].who_pays_channel_commission` | `recorded: owner` *(deducted before split)* |
| `owners[2]` | `flag_for_call_1: Verbal agreement; Jordan to get written terms and configure BusinessModel for Chris Lim` |
| All owner records | `flag_for_call_1` as above |
| Tax slots | `flagged: confirm_filing` (both taxes) |

**Key eval criterion:** Did the agent ask **at most one clarifying question per owner**? For Pat and Diane: did it record approximate values rather than refusing or hallucinating? For Chris Lim: did it ask one follow-up to extract the **specific percentage** (75%) rather than accepting "most of it" as the recorded value?

---

### B3 — User vocabulary mismatch (NLU normalization)

**Purpose:** The respondent speaks exclusively in Airbnb/layperson terms throughout. Tests whether the agent correctly maps non-canonical vocabulary to schema fields without correcting or confusing the user.

---

#### Ground-truth facts

*(Same underlying business as A2 — Coastal Keys Management — but told through different language.)*

| Business reality | User's words |
|------------------|-------------|
| channels: [airbnb, booking_com] | "I'm on Airbnb and Booking" |
| mandatory_fees: cleaning_fee $85 | "cleaning fee of $85" |
| revenue_recognition: checkout_date | "I get paid when they leave" |
| payment_timing: at_booking | "they pay up front when they book" |
| taxes: sales_tax 6% | "the state takes 6%" |
| owner reporting | "making sure my owners see their statements" |
| non_refundable_enabled: false | "I don't do the non-refundable thing" |
| security_deposit_type: damage_protection | "I use that damage coverage thing from Airbnb — is that what you mean?" |
| focus_topics: [owner_reporting] | "keeping owners in the loop" |
| pain | "My owners always ask me for their money breakdown and I do it by hand" |

---

#### Persona directive

Friendly, casual, uses Airbnb-ecosystem vocabulary throughout. Says "portals" not "channels." Says "cleaning fee" not "additional fee." Says "they pay when they book" not "at_booking." Says "statements" for owner payouts. Says "that damage coverage" for damage_protection. If the agent uses Guesty jargon without explanation, asks "what does that mean?" — agent must rephrase, not repeat the jargon.

---

#### Answer key

Same as A2 answer key in terms of ground-truth values. The **test** is not the values — it is whether the agent maps all non-canonical vocabulary to the correct slots.

**Key eval criterion (qualitative):** Did the agent correctly extract every slot value despite the vocabulary mismatch? Did it rephrase jargon when asked without losing context? Did it produce the same answer-key values as A2?

---

### B4 — Financials deferral / stress avoidance

**Purpose:** The respondent explicitly defers the entire financials section, pushing back three times before the agent accepts the skip. Tests that the agent records the deferral gracefully (no retry loops, no guilt trips), marks all S4 slots as `skipped`, and moves on.

---

#### Ground-truth facts

| Field | Value |
|-------|-------|
| **Business name** | Olive Tree Rentals |
| **Location** | Santa Fe, NM |
| **Listings** | 6 self-owned adobe-style properties |
| **Channels** | Airbnb, VRBO |
| **Focus topics** | Guest messaging, channel mix |
| **Pain** | "Responding to inquiries across two platforms is exhausting." |
| **Financial preference** | Defers ALL S4 questions to onboarding call |

---

#### Persona directive

Warm, a little scattered, visibly uncomfortable when money topics come up. On the first S4 question: *"Can we skip the money stuff for now? I'd rather go through that with someone on your team."* If agent asks a second financial question: *"I said I'd rather do this with Jordan."* If agent asks a third: silence or *"I thought we moved on?"* After three pushbacks, the agent must accept the skip and move on entirely. No partial answers on any S4 field.

---

#### Answer key

**S4 — Financials**

| Slot | Expected disposition |
|------|---------------------|
| `revenue_recognition` | `skipped` *(respondent deferred)* |
| `non_refundable_enabled` | `skipped` |
| `security_deposit_type` | `skipped` |
| `security_deposit_amount` | `skipped` |
| `payment_timing` | `skipped` |
| `payment_split` | `skipped` |
| `mandatory_fees` | `skipped` |
| `taxes` | `skipped` |

**All other sections** — proceed normally.

| Slot | Expected disposition |
|------|---------------------|
| `ownership_model` | `recorded: self_owned` |
| `focus_topics` | `recorded: [guest_messaging, channel_mix]` |
| `pain` | `recorded: "Responding to inquiries across two platforms is exhausting."` |

**Key eval criterion:** Did the agent accept the skip **after no more than two follow-up prompts**? Were all S4 fields marked skipped (not partially filled)? Did the agent move forward without circling back to financials?

---

## Group C — Complex Portfolio

*Multi-owner, semantically dense turns. Tests whether the agent handles long fan-out without losing state or conflating owners.*

---

### C1 — Mixed portfolio, four distinct owner economics

**Purpose:** The hardest hero-branch test. Four owners, each with a structurally different management model. Tests whether the agent can capture the full fan-out, ask targeted per-owner follow-ups, and produce a complete flag-for-call-1 summary for Jordan.

---

#### Ground-truth facts

| Field | Value |
|-------|-------|
| **Business name** | Alpine Property Group |
| **Location** | Lake Tahoe, CA/NV |
| **Listings** | 12 total: 1 self-owned + 11 managed |
| **Owner 1** | Sarah Mitchell · sarah@mitchell-tahoe.com · 3 listings · 20% commission of gross revenue |
| **Owner 2** | James Park · james@parkventures.co · 2 listings · $500/month flat fee per listing |
| **Owner 3** | Claudia Reyes · claudia@reyes-properties.com · 4 listings · 70/30 split (owner 70%, PMC 30% of net after OTA fees) |
| **Owner 4** | Marcus Webb · marcus@webbinv.net · 2 listings · "we have something in place but I'd rather work it out with your team" |
| **Self-owned** | 1 listing (Alex's own property) |
| **Channels** | Airbnb, VRBO, direct |
| **Revenue recognition** | Check-in |
| **Non-refundable** | Yes, listings 1–3 (Sarah's properties) only |
| **Security deposit** | $100 damage waiver on all managed listings |
| **Payment** | Full at booking (OTA) or 50/50 for direct |
| **Taxes** | CA state 9.25%, El Dorado/Placer County TOT 10% |
| **Teammates** | 2 cleaners (limited access, property-scoped) |
| **Focus topics** | Owner reporting, pricing strategy |
| **Pain** | "I have four different deal structures and I'm managing them in a Google spreadsheet." |

---

#### Persona directive

Knowledgeable, speaks in property management terms. When the agent asks about owners, provides all four in a single pass: *"I have four owners — Sarah Mitchell handles three cabins on a 20% commission, James Park has two units on a $500 flat monthly per unit, Claudia Reyes has four and we do a 70/30 split where she keeps 70 after channel fees, and Marcus Webb has two but we're still working out his arrangement."* Cooperative for 3 out of 4 owners; deflects on Marcus (legitimate deferral). Confirms echo-backs line by line.

---

#### Answer key

| Slot | Expected disposition |
|------|---------------------|
| `ownership_model` | `recorded: mixed` |
| `owners[0].owner_name` | `recorded: Sarah Mitchell` |
| `owners[0].email` | `recorded: sarah@mitchell-tahoe.com` |
| `owners[0].listings` | `recorded: 3` |
| `owners[0].management_model` | `recorded: commission` |
| `owners[0].pmc_commission_rate` | `recorded: 20` |
| `owners[0].who_pays_channel_commission` | `recorded: owner` *(requires one clarifying question to confirm gross-vs-net basis — e.g. "Does your 20% come out before or after Airbnb/VRBO takes their cut?" — then recorded once confirmed)* |
| `owners[0]` | `flag_for_call_1: Jordan configures BusinessModel for Sarah Mitchell — 20% commission; confirm gross-vs-net basis` |
| `owners[1].owner_name` | `recorded: James Park` |
| `owners[1].email` | `recorded: james@parkventures.co` |
| `owners[1].listings` | `recorded: 2` |
| `owners[1].management_model` | `recorded: flat_fee` |
| `owners[1].fixed_fee_amount` | `recorded: 500` |
| `owners[1].fee_per` | `recorded: per_listing_per_month` |
| `owners[1]` | `flag_for_call_1: Jordan configures BusinessModel for James Park — $500/mo flat fee x 2 listings` |
| `owners[2].owner_name` | `recorded: Claudia Reyes` |
| `owners[2].email` | `recorded: claudia@reyes-properties.com` |
| `owners[2].listings` | `recorded: 4` |
| `owners[2].management_model` | `recorded: revenue_split` |
| `owners[2].split_terms` | `recorded: "Owner receives 70% of revenue after OTA/channel fees; PMC retains 30%"` |
| `owners[2].who_pays_channel_commission` | `recorded: owner` *(deducted before split)* |
| `owners[2]` | `flag_for_call_1: Jordan configures BusinessModel for Claudia Reyes — 70/30 after channel fees` |
| `owners[3].owner_name` | `recorded: Marcus Webb` |
| `owners[3].email` | `recorded: marcus@webbinv.net` |
| `owners[3].listings` | `recorded: 2` |
| `owners[3].management_model` | `skipped` *(respondent deferred)* |
| `owners[3]` | `flag_for_call_1: Owner economics TBD; Jordan to discuss arrangement with Alex and Marcus Webb before Call 1` |
| `non_refundable_enabled` | `recorded: true` *(agent asks which listings; respondent says Sarah's 3 only)* + `flag_for_call_1: non-refundable applies to Sarah Mitchell's 3 listings only — Jordan configures per-listing/per-rate-plan` |
| All tax slots | `flagged: confirm_filing` |
| `security_deposit_type` | `recorded: damage_waiver` *(the $100 is a deposit waiver, not an additional fee — maps to security_deposit_type, not mandatory_fees)* |
| `security_deposit_amount` | `recorded: 100` |

**Key eval criterion:** Did the agent correctly fan out to all four owners without conflating them? Did it record the three clear structures and gracefully accept Marcus's deferral? Did it produce one coherent `flag_for_call_1` summary listing all four owners with their respective economics?

---

### C2 — Large managed, colloquial revenue-split

**Purpose:** A large operation described entirely in plain speech. Owner count is approximate. Revenue split is explained verbally, not in schema vocabulary. Tests semantic extraction, echo-before-write, and the one follow-up for count precision.

---

#### Ground-truth facts

| Field | Value |
|-------|-------|
| **Business name** | Lakeside Group |
| **Location** | Lake Norman, NC |
| **Listings** | 20 total: 8 self-owned + 12 managed for one family |
| **Managed owner** | The Grantham Family (estate entity) · estate@granthamholdings.com · 12 listings |
| **Management model** | Revenue split: owner (Grantham) receives 70% of revenue after channel fees are deducted |
| **Channels** | Airbnb, VRBO, direct bookings |
| **Revenue recognition** | Check-out |
| **Non-refundable** | No |
| **Security deposit** | $200 cash-equivalent deposit (refundable) |
| **Payment timing** | Full at booking |
| **Mandatory fees** | None |
| **Taxes** | NC sales tax 4.75%, Catawba County occupancy tax 3% |
| **Teammates** | 3 cleaners (limited, property-scoped); 1 admin (full access, all listings) |
| **Focus topics** | Owner reporting, accounting setup |
| **Pain** | "The family sends me emails asking where their money is. I need a proper statement." |

---

#### Persona directive

Conversational, storytelling style. Does not use business terminology. Describes the owner as "a family I've been working with for years" before providing the name. When asked listing count, says "maybe 8 or so of mine, and the rest are theirs — about 12." Agent must ask for exact counts (gets 8 and 12 confirmed). When asked about the revenue arrangement: *"I take my cut off the top after the platform fees — they end up with about 70% of what's left."* Does not use "revenue split," "PMC commission," or "BusinessModel." Mentions "direct bookings" when listing channels.

---

#### Answer key

| Slot | Expected disposition |
|------|---------------------|
| `listing_count` | `recorded: 20` *(after one clarifying question — "so 8 yours + 12 theirs = 20 total?")* |
| `ownership_model` | `recorded: mixed` |
| `owners[0].owner_name` | `recorded: Grantham Family` *(or "The Grantham Family Estate" — accept either)* |
| `owners[0].email` | `recorded: estate@granthamholdings.com` |
| `owners[0].listings` | `recorded: 12` *(after count confirmation)* |
| `owners[0].management_model` | `recorded: revenue_split` *(semantic extraction from "I take my cut after platform fees")* |
| `owners[0].split_terms` | `recorded: "Owner receives 70% of revenue after channel/platform fees are deducted"` *(70% must come from a follow-up question — "about 70%" is not sufficient; agent asks e.g. "What percentage does the family keep exactly?" and records the confirmed figure)* |
| `owners[0].who_pays_channel_commission` | `recorded: owner` *(deducted before split)* |
| `owners[0]` | `flag_for_call_1: Jordan configures BusinessModel for Grantham Family — ~70% owner revenue split after channel fees; confirm exact percentage` |
| `security_deposit_type` | `flagged: confirm_vehicle_with_jordan` *($200 refundable deposit maps to the trust-accounting Advanced Deposit, not Damage Protection/Shield — Jordan must confirm the correct Guesty vehicle before configuring)* |
| `security_deposit_amount` | `recorded: 200` |
| `payment_timing` | `recorded: at_booking` |
| `channels` | `recorded: [airbnb, vrbo, direct]` |
| `website_brand_name` | `conditional: surface_if_direct_signals` → **SURFACE** *(direct bookings confirmed)* |
| Tax slots | `flagged: confirm_filing` |
| `teammates[0..2]` | `recorded: 3 cleaners (limited/property-scoped)` *(exact role enum TBC)* |
| `teammates[3]` | `recorded: 1 admin (full access, all listings)` |
| `focus_topics` | `recorded: [owner_reporting, accounting_setup]` |
| `pain` | `recorded: "Family sends emails asking where their money is. Need a proper statement."` |

**Key eval criterion:** Did the agent ask for an exact listing count (not accept "about 8")? Did it correctly map "I take my cut after platform fees — they get about 70%" to `management_model: revenue_split` + `split_terms`? Did it echo back the owner economics before recording and flag for Call 1?

---

## Appendix A — Summary table

| Profile | Group | Key challenge | S5 surface? | Expected SAR risk |
|---------|-------|--------------|-------------|------------------|
| A1 | Happy path | — | Yes (direct channel) | Ceiling (all required+rec slots reachable) |
| A2 | Happy path | Two managed owners, flat fee | No | Ceiling minus S5 |
| B1 | Ambiguity | Channel-dependent payment timing | Yes (direct channel) | Medium — payment slot requires one follow-up |
| B2 | Ambiguity | Vague commission language | No | Medium — approximate values, multiple owners |
| B3 | Vocab | Airbnb vocabulary throughout | No | Same values as A2; tests NLU only |
| B4 | Robustness | Full S4 deferral | No | All S4 = skipped (agent should not retry) |
| C1 | Complex | Four owner structures, one deferral | Yes (direct channel) | Hard — fan-out + one legitimate skip |
| C2 | Complex | Large managed, colloquial split | Yes (direct channel) | Hard — semantic extraction + count precision |

---

## Appendix B — Open items before Phase 1 freeze

| Item | Blocking? | Owner |
|------|-----------|-------|
| G3 — canonical enum casing for tax types | Soft block (provisional values used; re-freeze if resolved before eval) | Data-model SME |
| S3 (Operations) exact enum values for `checkin_method`, `cleaning_managed_by` | Soft block (placeholders used; low SAR impact) | Product SME |
| S6 teammate role enum values | Soft block (A2, C1, C2 affected) | Product SME |
| Reviewer 2 + tie-breaker assignment | ✅ Resolved — single-reviewer protocol (Yair Cohen) | — |
| Dev profiles (≥4 additional profiles for tuning) | ✅ Complete — `poc-dev-profiles-2026-06-02.md` (6 profiles, D1–D6) | Mary |

---

## Appendix C — Archetype anchors & sales handover-note seeds (S0b)

Each profile is anchored to one or more real note archetypes (A–F) from the corpus analysis, and
given a synthetic handover note (≤255 chars, de-identified — matching the export's truncation) that
the rep would have written. The note seeds the **S0b prefill layer**; "expected extraction" is what
the LLM extractor should pull (Claim H2 / Component 6), and "flow effect" is how it should change the
conversation (confirm instead of ask).

> All notes are synthetic and de-identified. The extractor populates these as
> `status: prefilled_unconfirmed` — the agent **confirms**, never assumes (schema S0b precedence).

| Profile | Corpus archetype | One-line anchor |
|---------|------------------|-----------------|
| A1 | A (migration + add-on) + direct-website | Self-owner, names channels incl. direct, standard add-ons |
| A2 | B (managed-for-owners) | Two managed owners on flat fee, no direct |
| B1 | A + direct-website | Channel-specific payment behavior, ski-town |
| B2 | B + E (payment/term fuzziness) | Multi-owner, vague commission language |
| B3 | A + vocabulary-mismatch | Same facts as A2, layperson Airbnb vocabulary |
| B4 | C (sentiment/risk) | Financials-averse, defers money topics |
| C1 | B + C (complex managed + risk) | Four heterogeneous owner structures |
| C2 | B + F-style sparse seed | Large managed, colloquial revenue split |

### Per-profile note seeds

**A1**
- **Note:** *"Self-managed host, 5 vacation rentals in Sarasota FL. On Airbnb, VRBO + own direct site. Wants Guesty subdomain site. Manual pricing pain — adjusting rates daily. Standard cleaning fee. No managed owners."*
- **Expected extraction:** `ownership_model: self_owned` · `channels:[airbnb,vrbo,direct]` · S5 trigger (direct site) · `focus_topics:[pricing_strategy]` · `risk_flags:[]`
- **Flow effect:** Agent confirms channels + self-owned; surfaces S5; opens with the pricing pain rather than discovering it.

**A2**
- **Note:** *"Mgmt co, Key West. 8 listings: 5 own + 3 managed for 2 owners (flat monthly fee). Airbnb + Booking only, no direct. Cares about owner statements/reporting. 1 VA needs view access."*
- **Expected extraction:** `ownership_model: mixed` · `addon_intent:[accounting]` · `focus_topics:[owner_reporting]` · no S5 trigger · teammate hint
- **Flow effect:** Agent enters the hero branch already knowing managed owners exist; confirms count; does **not** surface S5.

**B1**
- **Note:** *"Ski-town, Breckenridge, 12 self-owned. Airbnb/VRBO + direct. Payments differ by channel — OTAs collect, direct is split. Reconciliation pain across channels. Non-refundable on peak listings."*
- **Expected extraction:** `ownership_model: self_owned` · `channels:[airbnb,vrbo,direct]` · S5 trigger · `risk_flags:[payment_comprehension]` (channel-split complexity) · `focus_topics:[accounting_setup]`
- **Flow effect:** Risk flag pre-warns the agent that payment is non-trivial → primes the one clarifying question rather than assuming a single enum.

**B2**
- **Note:** *"Asheville PMC, 10 managed for 3 owners. Commission structures vary + approximate ('around 18%', 'about $180'). One owner on a verbal revenue share. Owner-payout transparency is the pain."*
- **Expected extraction:** `ownership_model: all_managed_for_others` · `risk_flags:[]` · `focus_topics:[owner_reporting,accounting_setup]`
- **Flow effect:** Agent expects heterogeneous, fuzzy owner economics → records approximate values + flags for Call 1 rather than forcing precision.

**B3**
- **Note:** *"Small mgmt co. On Airbnb + Booking. Has owners she reports to. Uses 'that Airbnb damage coverage thing'. Gets paid when guests leave. Owner statements are the priority. Casual, non-technical."*
- **Expected extraction:** `ownership_model: mixed/managed` · `tech_level: low` · `addon_intent:[accounting]` · `customer_sentiment: neutral`
- **Flow effect:** `tech_level: low` cues the agent (brief-only) to use plainer language; tests that extraction handles layperson vocabulary the same as B-A2 canonical facts.

**B4**
- **Note:** *"Santa Fe, 6 self-owned adobe units. Airbnb + VRBO. Nervous about the financial setup — wants to do the money/tax part live with the specialist, not in the form. Guest-messaging is the real goal."*
- **Expected extraction:** `customer_sentiment: anxious` · `risk_flags:[]` · `focus_topics:[guest_messaging,channel_mix]` · S4-deferral hint
- **Flow effect:** The note **pre-warns** that S4 will be deferred → agent should accept the skip gracefully on the first ask (tests no-retry + sentiment-aware handling). Strong H2 case: a tree can't read "nervous about financial setup."

**C1**
- **Note:** *"Tahoe, 12 listings: 1 own + 11 managed across 4 owners w/ different deals (commission, flat fee, 70/30 split, one TBD). Airbnb/VRBO/direct. Managing 4 structures in a spreadsheet — wants owner reporting."*
- **Expected extraction:** `ownership_model: mixed` · `risk_flags:[high_addon_complexity]` (4 deal structures) · S5 trigger · `focus_topics:[owner_reporting,pricing_strategy]`
- **Flow effect:** Agent enters the hardest hero branch pre-aware of 4 owners → fan-out is expected, not discovered; one owner legitimately deferred.

**C2**
- **Note:** *"Lake Norman, ~20 units: 8 own + ~12 managed for one family on a revenue split. Airbnb/VRBO/direct. Family wants proper owner statements. Owner not precise on counts. Coming in warm/long relationship."*
- **Expected extraction:** `ownership_model: mixed` · S5 trigger · `focus_topics:[owner_reporting,accounting_setup]` · approximate-count hint
- **Flow effect:** Note flags approximate counts → agent knows to confirm exact 8 / 12; seeds the single-family revenue-split structure.

---

## Appendix D — Sparse/negative seeds for the H2 abstention test

Component 6 must prove the extractor **abstains** rather than fabricates. Use these alongside the 32
real `NA` rows:

| Seed note | Expected extraction |
|-----------|---------------------|
| *"Base PMS + Locks. Very tech savvy."* | `addon_intent:[locks]` · `tech_level: high` — **and nothing else** (no invented ownership/channels) |
| *"NA"* / blank | **Empty extraction** — no hallucinated slots; `prefill = {}` |
| *"GFH migration."* | `migration_source: guesty_for_hosts` — **only that** |

False-prefill on these is a Component-6 failure even if F1 on rich notes is high.

---

*Next steps: assign reviewers → freeze provisional answer keys as v1.1 → begin Phase 2 (decision tree authoring, independent author, blind to profiles). Handover-note seeds (Appendix C/D) feed Component 6 labeling.*
---

## Changelog

- **v1.3 (2026-06-02)** — Enum normalization. Corrected 6 answer-key values to canonical schema enums (self_owned → all_self_owned, managed_only → all_managed_for_others, booking_com → booking). Transcription error from markdown-to-JSON conversion; no ground-truth intent changed.

---

## Freeze Record

| Field | Value |
|-------|-------|
| Frozen file | `poc-respondent-specs-2026-06-02.md` |
| Version | v1.2-frozen |
| Freeze date | 2026-06-02 |
| Content checksum (sha256) | `7c2dbd7a93508211f5a7416f33b7b9480f9684e5584d1b7d6c39cd43c9514877` |
| Reviewer | Yair Cohen (single-reviewer protocol; analyst = Mary) |
| Pre-adjudication pass | Complete |
| Adjudicated changes | 5 (B2 Chris Lim follow-up requirement; B4 skip policy; C1 gross-vs-net clarifying Q; C1 non-refundable scope flag; C1 damage_waiver → security_deposit_type; C2 split_terms follow-up requirement; C2 security_deposit flagged for Advanced Deposit) |
| Provisional-G3 slots | All tax type enums marked `[provisional G3]` — re-freeze trigger if G3 resolves before eval run |
| Re-freeze triggers | G3 enum casing resolves; any schema gate change; defect found mid-run |

> **Epic 1 status: ✅ COMPLETE.** Answer keys are frozen. Unblocks Epic 4 eval run.
> Amelia (Dev) may now proceed with Epics 0, 2, 3 in parallel.
> Tree author (Epic 2) must not read this file until their tree is committed and locked.
