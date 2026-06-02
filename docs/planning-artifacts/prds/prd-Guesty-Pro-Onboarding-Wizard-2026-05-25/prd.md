---
title: "Guesty Pro Onboarding Wizard — Pre-Call-1 Questionnaire"
status: final
created: 2026-05-25
updated: 2026-05-25
revision: final (post-Session-3 finalization)
author: Yair Cohen (with John, PM agent)
based_on: docs/planning-artifacts/briefs/brief-Guesty-Pro-Onboarding-Wizard-2026-05-25/brief.md
flow_spec_source_of_truth: docs/planning-artifacts/onboarding-questionnaire-v4.md
---

# PRD: Guesty Pro Onboarding Wizard (Pre-Call-1 Questionnaire)

## 0. Document Purpose

This PRD specifies the **capabilities** of the Pre-Call-1 Questionnaire (the "Wizard") for Guesty Pro SMB customers. It is written for:

- **The downstream UX workflow** — to detail screens, micro-interactions, and edge-case UI states beyond what's already captured in V4
- **The downstream architecture workflow** — to design state persistence, Airbnb live-data polling, consent-gated writes, the Delegation Lifecycle state machine, and the Profile Output Schema artifact
- **The Sprint/Story workflow** — to slice FRs into stories with stable IDs

This PRD does **not** duplicate the V4 questionnaire spec. The V4 doc remains the source of truth for question copy, branching logic, intercept tier wording, "What's Configured" variable definitions, and Auto-Pilot Defaults. This PRD references V4 by section/question ID throughout.

**Structure:** Glossary-anchored vocabulary (§3). Features grouped, FRs nested with stable global IDs (FR-1 through FR-N). **§4.10 (Delegation Lifecycle) and §4.11 (Branching & Data Freshness Model) are the canonical behavioral specifications** for cross-cutting state machines — not feature appendages. Downstream architecture and story workflows should treat them as authoritative. Cross-cutting concerns in dedicated sections (§8–§15). Assumptions tagged inline `[ASSUMPTION: ...]` and indexed in §17 with severity.

**Companion artifacts:**
- [Brief](../../briefs/brief-Guesty-Pro-Onboarding-Wizard-2026-05-25/brief.md) — strategy, segment, outcomes
- [Brief Addendum](../../briefs/brief-Guesty-Pro-Onboarding-Wizard-2026-05-25/addendum.md) — operational depth, copy direction, V2 deferrals
- [V4 Questionnaire](../../onboarding-questionnaire-v4.md) — flow detail
- `.decision-log.md` (this folder) — audit trail
- `review-rubric.md`, `review-edge-cases.md`, `review-adversarial.md` (this folder) — Reviewer Gate outputs from draft v1

---

## 1. Vision

Guesty Pro SMB customers — owner-operators with 5–20 short-term-rental listings — sign up, schedule a Setup Call ("Call 1"), and today land in an empty enterprise UI with no clear next move. By the time Call 1 arrives, ~0% have engaged with the existing pre-call surfaces (Rocketlane, Academy), 82% of customers are off-SLA, and roughly half of all churn comes from customers who simply went silent during onboarding.

The Wizard is a guided, Typeform-style flow that runs in the dead zone between call booking and Call 1. It connects the customer's real Airbnb data in view-only mode (the "AHA moment"), captures the 8–10 operational defaults that matter, pre-configures the automated messaging that eats the most host time, locks in payment policy, and lands the customer on a populated dashboard with a personalized Call 1 agenda.

The goal is **not** full self-serve onboarding. The goal is to convert Call 1 from a generic walkthrough into a strategic review — and to ensure SMB customers arrive at Call 1 with **real account state**, momentum, and skin in the game. The product design follows a build-layer/review-layer model: the Wizard is the build layer (customers configure their account); the Setup Specialist is the review layer (Call 1 is spent reviewing and optimizing, not setting up from scratch).

---

## 1.1 Hypotheses, Premises, and Falsifiability

The V1 design rests on three load-bearing premises. **This PRD treats them as hypotheses, not assertions** — V1's instrumentation must allow each to be falsified, and the diagnoses below are phase-blocking Open Questions (§16).

### Hypothesis 1 — The AHA-moment hypothesis
- **Claim:** Connecting Airbnb in view-only mode as the *first* interactive step (rather than a verification warm-up later in the flow) converts more SMB operators into engaged Wizard users than alternative architectures.
- **Required diagnosis (phase-blocker):** Citable OAuth-in-onboarding benchmark for comparable B2B SaaS to ground SM-1 targets (see §16 BLOCKER-13).
- **Falsifiability mechanism:** SM-1 measured by end of Phase 2. If SM-1 < 30% in the Phase 2 cohort, this hypothesis is *not supported* — the surface UX is not the differentiator and Phase 3 is gated on diagnosis (see §14 Phase 2 hold-criteria).
- **What this PRD does NOT claim:** That Typeform UX alone causes engagement.

### Hypothesis 2 — Engagement-where-Rocketlane-didn't
- **Claim:** Customers who do not engage with Rocketlane (~0% pre-Call-1 task completion) *will* engage with the Wizard. The proposed causal differentiators: (a) in-product placement (vs. external email), (b) OAuth-anchored AHA moment, (c) consent-gated automation that does real work, (d) Call-1-countdown framing reducing avoidance.
- **Rocketlane failure-mode diagnosis (2026-05-25):** Qualitative feedback from CS identified three distinct failure drivers: **(1) separate login** — Rocketlane required authentication outside Guesty, creating an access barrier; **(2) complicated UI** — the interface was too complex for SMB owner-operators; **(3) format mismatch** — Rocketlane was a to-do checklist, not a questionnaire. Critically: questions sent separately via email had a *reasonable* completion rate, confirming the content/questions were not the failure mode — the container was. Exact quantitative completion data is unavailable (Rocketlane does not provide usage reports). The Wizard directly addresses all three failure modes: in-product placement eliminates the login barrier; Typeform-style UX replaces the complex checklist; questionnaire format replaces the checklist format.
- **Residual uncertainty:** Without Rocketlane usage metrics, the magnitude of each failure driver is unknown. The qualitative diagnosis is directionally strong but not quantitatively verified. SM-2 Phase 2 floor remains the live falsifiability check.
- **Falsifiability mechanism:** SM-2 (Cover Screen → Q1.1 start rate). If <50% in Phase 2, customers are not arriving at or engaging with the surface — the Wizard has not solved the access/delivery problem despite in-product placement.
- **What this PRD does NOT claim:** That booking-the-call alone produces commitment (the Rocketlane evidence already disproves that).

### Premise 3 — Role-collapse as design driver
- **Claim:** SMB Guesty Pro customers collapse executive sponsor + customer admin + process champion into one person (the owner-operator) *during the onboarding window*, which justifies the Wizard's opinionation (system supplies sequencing, defaults, pre-fills).
- **Data findings (2026-05-25, partially resolves §16 BLOCKER-8):** Multi-seat proxy data (cross-dashboard user roles, N=8,381 accounts) shows 79.2% of role-covered accounts have 2+ distinct users at steady state — but SMB role coverage is only 30.4% (vs. Mid-Market 97.9%), making direct extrapolation to the SMB cohort unreliable. Critically, single-user accounts cluster at a median of 3 listings ($194 MRR median), below the Wizard's 5–20 listing target. The data does not measure first-30-days active logins during new-account onboarding, so the onboarding-moment rate cannot be read directly from this dataset.
- **Updated interpretation:** Role-collapse is an *onboarding-moment* claim, not a steady-state account claim. The owner-operator is the primary setup actor during the pre-Call-1 window even on accounts that later grow to 3–5 functional users. The Wizard's opinionated design is appropriate for this moment. Separately: 27.1% of accounts have a recorded separate billing/finance contact — directly validating the Section 5 accountant delegation path (see §16 BLOCKER-10 resolution).
- **Falsifiability mechanism:** Q4.1 live rate in V1. If >50% of V1 users answer "Someone else owns financials," role-collapse is weaker than modeled for the onboarding moment and the delegation-first model should be elevated for V2.
- **Decision rule:** Opinionated UX survives if Q4.1 delegation rate in V1 stays ≤50%. If >50%, soften defaults and restructure for delegation-first in V2. The original ≥75% single-user threshold was pre-data and is superseded by this in-product signal.

### Premise 4 — Pre-Call-1 momentum survives Call-1 handoff
- **Claim:** The activation produced by the Wizard persists through Call 1 and into post-Call-1 work (channel integrations beyond Airbnb, GuestyPay activation, scaling listings), contributing to SLA graduation at day 20.
- **What this PRD does NOT claim:** That the Wizard alone moves SM-11 (onboarding duration). The Wizard improves Call 1 quality; sustained downstream activation requires the CSM playbook revision and remaining onboarding steps. SM-10 / SM-11 may not move even if SM-1 does.

---

## 2. Target User

### 2.1 Primary Persona

**The Owner-Operator** — a Guesty Pro SMB customer running 5–20 short-term-rental listings, with Airbnb as their primary distribution channel. They are simultaneously the **executive sponsor** (signed the contract), the **customer admin** (responsible for setup), and the **process champion** (the only user inside their account). They are time-poor, anxious about their live business, and have rejected at least one prior PMS before choosing Guesty.

Persona references: **2A (Bootstrapped Entrepreneur)** and **2B (Boutique/Family Operator)** from the Guesty persona library (see Tahini knowledge: `/personas/guesty-user-personas.md`).

**Critical design constraint — Role Collapse:** SMB Pro customers collapse executive sponsor + customer admin + process champion into one person during the onboarding window. The Wizard supplies the sequencing, defaults, and safety framing that a project manager would normally provide. Full data findings, updated decision rule, and falsifiability mechanism: **§1.1 Premise 3**.

### 2.2 Jobs To Be Done

- **Functional:** Get my listings, calendar, and inbox into Guesty before my first guest interaction inside the platform.
- **Functional:** Set up the automated guest messaging so I'm not writing the same check-in instructions 30 times a week.
- **Functional:** Lock in payment timing and mandatory fees so revenue is collected correctly from booking #1.
- **Emotional:** Feel like I'm making progress — that I haven't bought into yet another empty enterprise platform.
- **Emotional:** Feel safe — that nothing I do here will mess up my live Airbnb business.
- **Social:** Walk into Call 1 prepared, so I look competent and so the call is about my business, not about platform mechanics.
- **Contextual:** Do this between guest turnovers, on my laptop, in 3–10 minutes, possibly across multiple sittings.

### 2.3 Non-Users (V1)

- **Guesty Lite / Guesty SME / Guesty Mid-Market and Enterprise** — different segmentation, different role topology, separate flow needed (V2+).
- **Customers whose primary channel is Vrbo, Booking.com, or direct-only** — Airbnb-first design assumption breaks. V2+.
- **Property owners (third-party homeowners)** — objects of configuration in §4.6, not direct users. V1 sends them no communication.
- **Bookkeepers / accountants** — secondary recipients via the Section 5 delegation path (§4.5 + §4.10), not direct users.
- **CSMs / Setup Specialists** — downstream consumers of the Wizard's output (Call 1 prep, "What's Configured" summary), not direct users of V1. (CSM Review Mode is V2 — see Brief Addendum §7.)

### 2.4 Key User Journeys

*Six journeys inferred from the V4 questionnaire flow; all six feature instances of the §2.1 **Owner-Operator** persona unless otherwise specified. Each is the kind of session the system must support. `[ASSUMPTION: UJs inferred from V4 spec — confirm or narrate alternatives.]`*

- **UJ-1. Maya (Owner-Operator) completes the Wizard end-to-end before her Call 1.**
  Maya manages 8 listings in a coastal vacation town. She just booked a Call 1 for Thursday. She lands on the cover screen, sees the call countdown ("Thursday in 2d 14h"), checks the consent box, and clicks "Let's get started." She OAuths into Airbnb (10 seconds), sees "✓ Synced — 8 listings, 22 upcoming reservations, 3 unread messages," and feels relief that her real data is there. She walks through Operations → Communications → Team → Financials → Call 1 Focus → Quick Wins → Handoff in ~8 minutes (the median once V4 is paper-prototyped — see §16 SOFT-19). The "What's Configured" screen lists nine items. She clicks "Go to Dashboard" and lands on a populated calendar. **Climax:** the moment in Section 1 where her empty enterprise dashboard becomes her actual business. **Resolution:** populated dashboard, calendar add for Call 1, ready.

- **UJ-2. David (Owner-Operator) is urgent-routed to Financials because of an imminent check-in.**
  David has 12 listings; his next guest checks in tomorrow morning. He connects Airbnb. The post-sync routing detects `Next_Check_In_Date < 48 hours` and the bot says: *"Heads up — you have a check-in arriving in 14 hours. Let's jump to Financials first so payment is locked in safely."* He clicks "Jump to Financials," sets payment timing and fees, then continues through Operations and Communications, finishes the rest in his next sitting. **Resolution:** payment policy locked before the check-in; the urgent-route framing remains stickily visible for the rest of the session (per FR-11.1) even though the original check-in window may have passed by his next entry.

- **UJ-3. Sara (Owner-Operator) hits "Skip to Dashboard" before connecting Airbnb, gets the Tier 1 intercept, decides to connect anyway.**
  Sara is impatient. She clicks the top-right skip button on the cover screen. The Tier 1 intercept fires: *"I totally get it — but if we jump in right now, your calendar and inbox will be completely empty. Give me 10 seconds to connect your Airbnb account first."* She chooses the primary CTA, connects Airbnb, then proceeds. **Edge case:** if she had chosen "I'll connect it later," she would have hit the Auto-Pilot Acceptance Modal (FR-37.1), confirmed which defaults to apply, and landed on a dashboard with a persistent "Finish Setup" link.

- **UJ-4. Marcus (Owner-Operator) delegates Financials to his accountant Jane via Q5.1's secure link.**
  Marcus runs 15 listings and uses a bookkeeper. He hits Section 5, sees the delegation option *"Send to my accountant,"* enters Jane's email (validated ≠ his own email per FR-25.1), clicks send. Section 5 marks as `→ Delegated to Jane` in the nav. Marcus skips to Section 6 and continues. Jane receives the Accountant Secure Link via email, clicks it, lands on a Stripped Section 5 View — no Wizard nav, no other sections, just Q5.2 and Q5.3 plus a context header and an *accountant-scoped consent banner* (FR-28.1). She completes Q5.2 and Q5.3 — fees validated against an industry-relative reasonableness range (FR-31.1) — sees a "Thanks — Marcus has been notified" confirmation, and is done. Marcus's nav updates from `→ Delegated to Jane` to `✓ Done` and an in-app notice surfaces on next dashboard load. **Edge case:** if Jane had clicked *"This isn't for me"* (FR-50.4), the delegation would have moved to `cancelled` and Section 5 would revert to `unlocked` for Marcus. If Jane had not clicked the link within 14 days, the delegation would have moved to `expired` and Marcus would have received an in-app notice with options to resend or self-complete (FR-50.5).

- **UJ-5. Hannah (Owner-Operator) uses Turno and PriceLabs — sections auto-skip to confirmation.**
  Hannah's Guesty account has `Partners = ["Turno", "PriceLabs"]` in normalized form (per FR-18.1 alias table). Q2.1 detects Turno and auto-advances with *"We see you use Turno. We'll auto-route your checkout data straight to them — nothing for you to set up here. ✓"*. Q7.2 detects PriceLabs and auto-skips. **Edge case:** if `Partners` contained both `"Turno"` AND `"Breezeway"` (a CRM data hygiene scenario), Hannah sees a one-question disambiguation per FR-18.2.

- **UJ-6. Ben (Owner-Operator) closes the browser at Q3.2, returns 14 hours later with new guest activity.**
  Ben gets pulled away mid-Wizard at Q3.2. He closes the tab. Fourteen hours later he returns via dashboard "Finish Setup" link. The Wizard re-polls Airbnb on entry (FR-11) — `Unread_Message_Count` is now 8 (was 3 yesterday). He lands at Q3.2 with a subtle "We refreshed your Airbnb data — 5 new messages since you left" toast (FR-12). The Q3.2 template variant he originally saw is preserved (immutable per-session per FR-11.2) even though the data behind the variant has changed. He continues from where he left off, on the same Wizard cohort he was originally assigned (FR-NEW feature-flag stickiness).

---

## 3. Glossary

*Every domain noun the rest of the document uses. Defined once. No synonyms anywhere else in the PRD.*

- **Wizard** — The Pre-Call-1 Questionnaire surface as a whole. Synonyms used externally ("Onboarding Questionnaire," "Pre-Call-1 flow") are not used in this PRD.
- **Section** — One of the eight logical groupings of the Wizard (Sections 1–8 per V4). Plus Section 0 (Cover) as the entry surface. The Wizard contains *nine screens* (Cover + 8 Sections) but is conventionally described as *8 Sections + Cover*.
- **Question** — A single screen within a Section, identified as `Q{section}.{order}` (e.g., Q3.2). Source of truth for Question content is V4.
- **Cover Screen** — Section 0. The personalized welcome surface containing the consent gate. Renders before any interactive Question.
- **Setup Call / Call 1** — The first scheduled call between the customer and a Guesty Setup Specialist. Booked before the Wizard starts.
- **CSM** — Customer Success Manager, also referred to as Setup Specialist. The Guesty employee leading Call 1. Not a direct Wizard user in V1.
- **Decision Owner** — The customer-side individual who owns account-level decisions. In SMB V1, equals the authenticated user unless they delegate Financials via Q4.1. (Note: V4 Q4.1's user-facing copy says "primary owner" — these refer to the same concept; FRs use "Decision Owner.")
- **Financial Owner** — A separately-named individual (e.g., the customer's accountant) who completes Section 5 alone via the Accountant Secure Link.
- **Accountant Secure Link** — A unique, expiring, scoped URL emailed to the Financial Owner that opens the Stripped Section 5 View.
- **Stripped Section 5 View** — A scoped Wizard surface accessed via the Accountant Secure Link that exposes only Section 5 questions plus a context header and accountant-scoped consent banner; no other Sections or navigation reachable.
- **Delegation Lifecycle** — The state machine governing a Section 5 delegation; states are `not_offered`, `offered`, `sent`, `opened`, `completed`, `expired`, `cancelled`, `superseded`. Specified in §4.10.
- **Consent Record (Operator)** — The persisted record of the operator's cover-screen authorization for Guesty to write configuration on their behalf.
- **Consent Record (Accountant)** — The persisted record of the accountant's separate consent shown at the start of the Stripped Section 5 View, scoped to financial-configuration writes only.
- **Profile Configuration Write** — Any write the Wizard performs to the customer's live Guesty account based on their answers (e.g., payment policy, message templates, fees). Gated by the appropriate Consent Record.
- **Profile Output Schema** — The PM-owned companion artifact that maps every Question answer to specific fields in the customer's Guesty account. Required pre-engineering-kickoff per FR-44. *Not a deferred deliverable — a Phase 0 precondition (see §14).*
- **Auto-Pilot Defaults** — The conservative configuration set applied when a user skips the Wizard at any tier. Defined in V4 Appendix B. Per FR-37.1, V1 requires explicit acceptance via the Auto-Pilot Acceptance Modal before defaults are written.
- **Skip Intercept (Tier 1–4)** — The system's adaptive response to a Skip-to-Dashboard click, with weight decreasing as Wizard investment increases. Defined in V4.
- **Live Airbnb Data Hooks** — System integrations that query the customer's connected Airbnb account in near-real-time for `Next_Check_In_Date`, `Unread_Message_Count`, `Average_Length_of_Stay`, `listing_count`, `reservation_count`. Polled on every Wizard entry (FR-11) subject to the cost ceiling in §9.3.
- **Salesforce Account Data** — Customer record fields pre-fetched from the CRM at Wizard entry: `active_listing_count`, `connected_channels`, `Partners` (normalized via the Partner Alias Table — see FR-18.1), `industry`, `operative_account_segmentation`, `Expected_MRR__c`, `Owners`, `customer_churn_reason`.
- **Branching Snapshot** — The values captured at the time a Question was first answered, used immutably for re-rendering that Question on Backward navigation. See §4.11 for the freshness model.
- **Resume State** — The persisted record of a customer's Wizard progress. Captured per-Question; resume returns the user to the last-answered Question (FR-10) subject to the validity checks in §4.11.
- **Section Status** — One of `done` / `current` / `unlocked` / `locked` / `delegated`. Displayed via icons in the persistent header.
- **Wizard Cohort** — The feature-flag bucket assignment for a given customer. Sticky once assigned (FR-NEW): a customer's cohort does not change mid-session even if flag thresholds move.
- **CSM Handoff Artifact** — The structured Salesforce record produced by the Wizard for CSM consumption pre-Call-1. Field spec is a Phase 0 deliverable (FR-32.1).
- **Partner Alias Table** — The normalized-name registry used to detect partners from CRM `Partners` array strings. See FR-18.1.
- **"What's Configured" Summary** — Section 8 surface that renders the customer's completed configuration using the variables defined in V4 Appendix A.
- **"To Cover With CSM"** — Conditional Section 8 list of skipped items, surfaced to both the customer and (via the CSM Handoff Artifact) the CSM.
- **Call 1 Prep** — The bundle of skipped items, urgent flags, and priority topic surfaced for Call 1. In V1, communicated via the "What's Configured" summary + the CSM Handoff Artifact. In V2, becomes a persistent dashboard widget (deferred).
- **Unified Inbox** — The Guesty product surface that consolidates messages from all connected channels. The Wizard configures awareness and automated message activation on top of it.
- **SMB Guesty Pro** — Customers with 5–20 listings on Guesty Pro plan, primary channel Airbnb. The exclusive target segment for V1.

---

## 4. Features

*FRs are numbered globally (FR-1 … FR-N). Reference UJs inline. Use Glossary terms exactly. Inline `[ASSUMPTION: …]` tags surface inferences; all assumptions are indexed in §17 with severity.*

### 4.1 Pre-Questionnaire Entry State

**Description:** Before any interactive Question, the Wizard renders a personalized Cover Screen, persistent header, and consent gate. Account context (Salesforce Account Data, Setup Call metadata) is pre-loaded from upstream systems and made available throughout the session. Realizes UJ-1, UJ-3.

**Functional Requirements:**

#### FR-1: Cover Screen renders with personalized header

The system renders Section 0 (Cover) with the user's first name, CSM name, Call 1 date/time, timezone, and live countdown to Call 1. All time values are anchored to `{{timezone}}` (the user's booking-time timezone), not the browser's current timezone.

**Consequences (testable):**
- The Cover Screen displays `{{user_first_name}}`, `{{CSM_Name}}`, `{{call_date}}`, `{{call_time}}`, `{{timezone}}`, `{{call_countdown}}`.
- All displayed dates/times use `{{timezone}}` for day-of-week and wall-clock rendering, with the timezone label visible on first paint (e.g., "Thursday, 2:00 PM PDT").
- The countdown updates at minimum once per minute, without page reload.
- Countdown copy at T-0 displays "Your call is starting now" with a CTA to the call link; at T-negative within 24h displays "Your call was {{relative_past_time}}" with reschedule CTA.
- Countdown copy at T-≤60min displays "in {{N}} minutes"; T-≤5min displays "starting soon."
- `{{user_first_name}}` is HTML-escaped, truncated at 30 characters with ellipsis; an empty value falls back to "there" (e.g., "Welcome, there 👋").
- If any required booking value (`{{CSM_Name}}`, `{{call_date}}`, `{{call_time}}`, `{{timezone}}`) is missing, the Wizard does **not** render its standard surface. Instead, a user-facing fallback page surfaces: *"Your Setup Call info isn't ready yet — refresh in a moment, or contact your specialist."* with a retry CTA and a dashboard escape CTA. Engineering instrumentation is alerted.

#### FR-2: Consent gate blocks Wizard entry until checked; consent write is synchronous

The Cover Screen "Let's get started" CTA is disabled until the consent checkbox is checked. Checking it persists a Consent Record (Operator) **synchronously** — the CTA does not enable until the write is acknowledged by the persistence layer. Realizes UJ-1, UJ-3.

**Consequences (testable):**
- The CTA renders disabled on first paint.
- Checking the box triggers a synchronous, read-after-write-verified persist of the Consent Record (Operator) with timestamp, user ID, account ID, and the verbatim consent wording shown. Only after acknowledgment does the CTA enable.
- A consent persistence failure surfaces a blocking error state with a retry CTA — *not* a non-blocking toast. The Wizard cannot proceed without a confirmed Consent Record.
- The Consent Record (Operator) is append-only: it is created once per session start. Re-checking after uncheck does not write a second record; revocation is a separate flow (FR-46) and not reachable within the Wizard session.
- The Cover Screen consent panel includes a *"See what we'll configure"* disclosure listing the configuration domains in plain language (per the Profile Output Schema, FR-44). The disclosure is collapsed by default.
- The consent text shown is the latest legally-approved wording. **`[ASSUMPTION: final wording pending legal sign-off — see §16 BLOCKER-1.]`**

#### FR-3: Persistent header renders on every Wizard screen

A persistent header is present on every Wizard screen (Sections 0–8) with three regions: top-left Section Nav, top-center Call countdown, top-right Skip-to-Dashboard.

**Consequences (testable):**
- Header is fixed-position and survives Section transitions.
- Section Nav shows the eight Sections with their Section Status icons.
- Countdown updates live per FR-1.
- Skip button is always visible. Tier intercept fires on click (see §4.7).
- On Section 8, the Skip-to-Dashboard button is hidden (replaced by the primary "Go to Dashboard" CTA per FR-42).
- Maximum header height: 64px. Minimum supported viewport width: 1024px; below that, see FR-3.1.

#### FR-3.1: Below-minimum-viewport behavior

If the viewport is narrower than 1024px (split-screen on desktop, or mobile despite desktop-only V1), the Wizard does not render its standard surface. Instead, a "best experienced on a wider screen" landing page is shown with the call info, the call link, and a "Continue on a wider screen" message.

**Consequences (testable):**
- Mobile UA strings are detected and routed to the same landing page.
- The landing page passes accessibility AA and renders the call countdown.

#### FR-4: Salesforce Account Data pre-loads on Wizard entry

On Wizard entry, the system pre-fetches the customer's Salesforce Account Data for use in dynamic branching throughout the flow. **Snapshot semantics:** the Salesforce data fetched at entry is used for the entire Wizard session, even if Salesforce changes mid-session. See §4.11 for the full freshness model.

**Consequences (testable):**
- All listed fields are fetched: `active_listing_count`, `connected_channels`, `Partners`, `industry`, `operative_account_segmentation`, `Expected_MRR__c`, `Owners`, `customer_churn_reason`.
- `Partners` is normalized via the Partner Alias Table (FR-18.1) before use in branching.
- A fetch failure does not block Wizard entry; the system falls back to non-personalized defaults, branches as if all conditional fields were empty (see §4.11 no-data branches), and logs a degradation event.
- Data is fetched on Wizard entry, *not* on every Section render.
- If the authenticated user has more than one Guesty account in scope, FR-4.1 fires first.

#### FR-4.1: Account selection when authenticated user has multiple Guesty accounts

Before the Cover Screen renders, if the authenticated user is associated with more than one Guesty Pro account, the Wizard presents a one-screen account selector. The Wizard session is bound to a single `account_id` for the rest of the run.

**Consequences (testable):**
- Selector displays each account's name and listing count.
- The selected `account_id` is persisted in Resume State and is unchanged for the session.
- Returning to the Wizard via "Finish Setup" link resumes against the same `account_id`; if the user wants to run the Wizard for a different account, they exit and re-enter (a dashboard nav handles account switching).
- Single-account users skip the selector entirely.

#### FR-5: Wizard entry origin is dashboard-or-direct

The Wizard is reachable from (a) immediately after Setup Call booking (auto-redirect), and (b) a "Finish Setup" link in the post-Wizard dashboard navigation for users who exited.

**Consequences (testable):**
- Post-booking flow auto-redirects to Wizard URL with the Consent Record absent.
- Dashboard "Finish Setup" link is visible when at least one Section is not yet `done` or `delegated`.
- The link's visibility is computed on every dashboard load (not cached); if a Section transitions back from `delegated` to `unlocked` (per the Delegation Lifecycle, §4.10), the link re-appears.
- The link disappears when all Sections are `done` *or* `delegated` *and* there are no pending writes (FR-49).

---

### 4.2 Adaptive Questionnaire Flow

**Description:** The core flow engine. One Question per screen. Dynamic branching driven by Salesforce Account Data and Live Airbnb Data Hooks. Auto-advance on single-select. Save state every interaction. Resume to the exact last-answered Question on re-entry. Realizes all UJs.

**Functional Requirements:**

#### FR-6: One Question renders per screen with explicit interaction model

Each Question is the focal element of its screen. Auto-advance fires on a single-select choice; multi-select and free-text answers require an explicit "Continue" CTA. Per-Question skip surfaces the Tier intercept for the Section the Question is in.

**Consequences (testable):**
- A screen contains exactly one Question's content.
- Single-select answer choices trigger advance with a brief animated transition.
- Multi-select Questions render a "Continue" CTA enabled once a valid selection state is reached.
- For "None" pseudo-options in multi-select (e.g., Q5.3 fees): selecting "None" clears all other selections; selecting any other option clears "None."
- Free-text input boundaries are *hard caps* with a visible character counter at 80% of limit and at limit; values are HTML-escaped at submit. Limits: Q2.2 "Other" provider 60 chars; Q6.1 priority topic 200 chars; Q7.2 custom min-stay integer 1–14.
- Global keyboard model: `Enter` advances (when CTA is enabled); arrow keys navigate Backward/Forward where allowed; `Esc` dismisses modals only (not the main flow).
- WCAG 2.1 AA: auto-advance announces the selection via screen reader before transitioning, and a user-mode toggle (accessibility settings) replaces auto-advance with an explicit Continue CTA on every Question.

#### FR-7: Dynamic branching with explicit no-data fallback

Branch logic at each branching point evaluates against the values held in the session state per the freshness model (§4.11) and selects the appropriate Question path. Every branching predicate has an explicit *no-data* branch.

**Consequences (testable):**
- Q1.2 routes to Financials when `Next_Check_In_Date < 48 hours`. *No-data branch:* when `Next_Check_In_Date` is null (no upcoming reservations or no Airbnb sync), auto-advance to Section 2 without the urgent route.
- Q2.1 auto-advances when `Partners` (normalized) contains "Turno" or "Breezeway." *No-data branch:* when `Partners` is empty or unrecognized, present the standard A/B/C options.
- Q3.1 uses the ">5 unread" variant when `Unread_Message_Count > 5`. *No-data branch:* when `Unread_Message_Count` is null or zero, present the standard variant.
- Q3.2 selects the template variant by `access_method` from Q2.2. *No-data branch:* if Q2.2 was skipped, Q3.2 presents a generic check-in message template with an inline access-method picker.
- Q6.1 suggestion order is deterministic: first, `Financial Setup` if Section 5 was skipped; second, `Advanced Messaging Workflows` if `Unread_Message_Count > 5` AND Q3.1 = "Yes"; third, `Trust Accounting` if `customer_churn_reason` for region/size = "Accounting." If three fire, the first two in this order are shown; if none fire, only the free-text option renders.
- Q7.1 hides when `Owners = 0`. *No-data branch:* when `Owners` is null (CRM degradation), the question hides.
- Q7.2 auto-skips when `Partners` (normalized) contains "PriceLabs" or "Beyond." *No-data branch:* when `Partners` is empty, present the standard A/B options. Bot copy referencing `{{avg_los}}` falls back to a static "your guests typically stay multiple nights" copy when `Average_Length_of_Stay` is null.
- Branch evaluation is server-authoritative (no client-only branching). The branching engine's implementation, cost model, and per-request latency are owned by the architecture workflow (see §16 BLOCKER-13 for Live Airbnb cost confirmation).

#### FR-8: Non-linear Section navigation with status icons and rollback handling

Users can navigate between Sections via the persistent header nav under the V4 rules (Backward always allowed for non-delegated Sections; Forward only to visited Sections or the next unlocked Section).

**Consequences (testable):**
- Section icons display: `✓` (done), `●` (current), `○` (unlocked), `🔒` (locked), `→ Delegated to {{name}}` (delegated).
- Section 1 (Airbnb) is always unlocked.
- Sections 2–7 unlock when Section 1 is `done` *OR* explicitly skipped via Tier 1 intercept (in which case the Auto-Pilot Defaults branch applies to all Airbnb-dependent Questions per §4.11).
- Section 8 unlocks when at least one of Sections 2, 3, or 5 has been touched (any Question answered) — *and* at least one Section 1 outcome (done or skipped) is set.
- A delegated Section 5 is not revisitable from the operator's nav UNTIL the operator clicks "Cancel delegation" on the nav item (FR-50.6); cancellation invalidates the outstanding Accountant Secure Link.
- Backward navigation to a Question on the operator's side does *not* re-trigger writes to live config if the answer is unchanged (FR-45 idempotency); changing an answer overwrites prior writes per FR-45 and applies cascading invalidations per §4.11.
- After Q1.2 fast-tracks the user to Section 5, Backward navigation order is the linear V4 order (back from Section 5 → Section 4 → Section 3 → Section 2 → Section 1), *not* a route-aware back. The persistent "you fast-tracked here" affordance is visible until the user manually visits an earlier Section.

#### FR-9: Save state on every Question interaction

The Resume State persists after every Question interaction (answer selection, multi-select toggle, free-text blur).

**Consequences (testable):**
- Each interaction triggers a server-side write within 2 seconds of user action.
- A write failure surfaces a non-blocking toast (per the shared toast component spec — see §16 SOFT-23) and retries silently up to 3 times; if still failed, the user is warned ("We're having trouble saving — please copy your answer before closing").
- The Resume State stores: current Question ID, all answered Questions with values, current branch path computed so far, the Branching Snapshot for each answered Question (per §4.11), and the Wizard Cohort assignment.
- Concurrent sessions in two browser tabs: the Wizard enforces a single-active-session lock. The second tab opens read-only with a "Another tab is active — close that tab to edit here" notice.

#### FR-10: Resume returns user to last-answered Question with validity check

When a user re-enters the Wizard, they land on the Question *immediately following* the last Question they answered, *unless* the branch path is no longer valid (per §4.11).

**Consequences (testable):**
- If the user last answered Q3.1, they resume at Q3.2.
- If they have not yet answered any Question, they resume at the Cover Screen.
- If all Questions in their branch path are answered, they resume at the Section 8 "What's Configured" summary.
- If the resume target Question is now unreachable (its predecessor's branching predicate has changed after a refresh — see §4.11), the user lands at the closest valid Question with a "Picking up where we left off" toast.
- Their previously-answered Questions remain editable via Backward navigation (per FR-8).
- The Wizard Cohort assignment is preserved across resumes; a user who entered the Wizard during Phase 2 (10%) stays in the Wizard cohort through completion or expiry, regardless of subsequent flag changes.

#### FR-11: Live Airbnb re-poll on every Wizard entry

On every Wizard entry (initial or resume), the system re-polls the Live Airbnb Data Hooks before rendering the resume Question. Re-poll is rate-limited to once per Wizard entry (not per Question render); cost ceiling is bounded per §9.3.

**Consequences (testable):**
- The polled values overwrite the previously-cached values for *new* branching decisions only.
- A re-poll failure surfaces a non-blocking toast and uses the stale cached values.
- If the user has not yet completed Section 1, the re-poll is a no-op.
- If the re-poll detects that the Airbnb account has been disconnected from Guesty (e.g., via Settings in another tab), the Wizard surfaces a "Your Airbnb connection was removed — reconnect to continue" state at the current Question; Sections downstream that depend on Airbnb data become locked until reconnected.
- If the re-poll detects an additional Airbnb account has been connected to the customer's Guesty account, V1 ignores secondary accounts: the original Airbnb account's hooks remain the source of truth for the session. (V2 may aggregate.)

#### FR-11.1: Urgent-route framing is sticky

Once Q1.2 routes a user to Section 5 (urgent check-in branch), the urgent framing is preserved visually for the rest of the session, even if a later re-poll shows the check-in window has passed.

**Consequences (testable):**
- The persistent header carries a small "Urgent route active" indicator after Q1.2 fast-tracks.
- The Section 8 summary preserves the original urgent context with a *"Initially flagged urgent: check-in in 14 hours (window now passed)"* note when the data has changed.

#### FR-11.2: Branching Snapshot preserves variant copy on Backward navigation

When a user Backward-navigates to an already-answered Question, the variant copy rendered is the variant the user *originally saw at first answer*, captured as the Branching Snapshot. Re-polled data updates do not retroactively swap variant copy on already-answered Questions.

**Consequences (testable):**
- Q3.1 answered when `Unread_Message_Count = 8` shows the ">5 unread" variant on Backward, even if a subsequent re-poll shows count = 2.
- If the user actively *edits* an answered Question (changes their selection), the variant copy refreshes to the current data state and the original answer is overwritten. Cascading effects per §4.11.

#### FR-12: User-visible notice when Airbnb data changes on re-entry

When a re-poll detects a meaningful change since the user's last session, a toast surfaces the change. Realizes UJ-6.

**Consequences (testable):**
- "Meaningful change" is defined as: `Unread_Message_Count` delta ≥ 3, OR a new `reservation_count` increase, OR `Next_Check_In_Date` crossing the 48-hour threshold (in either direction), OR `listing_count` change.
- The toast is auto-dismissable, non-blocking, and shown once per re-entry.
- The toast wording follows the copy direction in Brief Addendum §6 (review-ready framing). `[ASSUMPTION: toast wording — UX to finalize.]`

---

### 4.3 Airbnb Sync as First Interactive Step

**Description:** Section 1. The architectural cornerstone — Airbnb OAuth in view-only mode is the very first interactive step after the Cover Screen, *not* a verification warm-up. The cover screen is the warm-up. Realizes UJ-1, UJ-2, UJ-3. **Validates Hypothesis 1 (§1.1).**

**Functional Requirements:**

#### FR-13: Q1.1 triggers existing Airbnb OAuth flow (single connection in V1)

Selecting "Connect Airbnb (10 sec)" on Q1.1 invokes the existing Guesty Airbnb OAuth integration in view-only scope. V1 supports a single Airbnb account connection per Wizard session.

**Consequences (testable):**
- The integration uses the same view-only scope that exists in production today.
- Successful OAuth returns the user to the Wizard's Q1.1 with a confirmation state.
- Re-OAuth from within the Wizard (after a successful first sync) is disabled in V1; the user is offered a "Manage connections in Settings" link instead.
- OAuth in-flight state: when the user has been redirected to Airbnb's OAuth screen, Q1.1's state is `oauth_pending`. If the user returns to the Wizard tab without completing OAuth (e.g., closed the Airbnb tab), the Wizard reconciles the pending OAuth state on re-entry and offers a "Retry connection" CTA rather than silently re-triggering OAuth.

#### FR-14: Post-OAuth confirmation state displays sync summary

On successful OAuth return, the Wizard displays the V4-specified confirmation: *"✓ Synced. {{listing_count}} listings, {{reservation_count}} upcoming reservations, {{unread_count}} unread messages."* Auto-advance to Q1.2 after a 2-second confirmation pause.

**Consequences (testable):**
- All three counts render from the immediate post-OAuth sync result.
- The 2-second pause is unskippable.
- The auto-advance fires without user interaction.
- An *aha_moment_fired* analytics event is emitted at this confirmation render (see §8 Observability).
- Edge case: if OAuth succeeds but `listing_count = 0` (new host, no published listings), the confirmation copy adapts: *"✓ Connected — no listings yet on Airbnb. We'll be ready when you publish."* Sections 2–8 continue normally; Airbnb-data-dependent branches use no-data fallbacks per FR-7.
- Pre-connected case: if Salesforce `connected_channels` contains "airbnb" at Wizard entry, Q1.1 pre-fills with the success state, skips the OAuth trigger, and immediately triggers a re-poll to populate hooks. The 2-second confirmation pause still applies for the AHA framing.
- Reconnect vs. fresh-import distinction: the Airbnb Integration Page Revamp (2026-05-25 full rollout) introduced explicit UX distinguishing listings being "reconnected" (previously connected, then disconnected) from listings being "imported fresh" (creating a new Guesty listing from Airbnb data). The Wizard's view-only OAuth flow should surface the same distinction to prevent duplicate listing creation — a live CSM-reported issue (46 unwanted duplicates from ambiguous import UX). The UX spec should confirm this case with the revamp team.

#### FR-15: Live Airbnb Data Hooks populate on first sync

On first successful Airbnb sync, the system populates and caches the Live Airbnb Data Hooks for downstream branching: `Next_Check_In_Date`, `Unread_Message_Count`, `Average_Length_of_Stay`, `listing_count`, `reservation_count`.

**Consequences (testable):**
- These five values are available in the session state by the time Q1.2 renders.
- The values are also stored persistently so they survive a user re-entry (re-poll behavior per FR-11 applies on subsequent entries).
- `[ASSUMPTION: hook implementation requires a separate technical spec — owned by architecture, see §16 BLOCKER-3 (Profile Output Schema) for sequencing.]`

#### FR-16: Q1.2 urgent-check-in routing

When `Next_Check_In_Date < 48 hours from current time`, the bot offers to jump to Financials first; otherwise auto-advance to Section 2. Realizes UJ-2.

**Consequences (testable):**
- The 48-hour threshold is server-evaluated, not client-evaluated.
- The user can decline the route ("Continue in order") and proceed to Section 2 normally.
- If accepted, Section 5 (Financials) is fast-tracked; Sections 2–4 are not auto-marked or auto-skipped, just visited after Section 5.
- Urgent-route framing is sticky per FR-11.1.

#### FR-17: OAuth failure handling

If the OAuth flow fails (user cancels, Airbnb error, network error, scope rejection), the Wizard returns the user to Q1.1 with an inline error state and recovery options. *Detailed failure-state copy and the "Help — what went wrong?" support article are V1 launch-blockers: either author them or remove the secondary CTA.*

**Consequences (testable):**
- Q1.1's failure state offers three CTAs: "Try again," "Skip for now (apply Auto-Pilot Defaults)," and "Help — what went wrong?" (if the support article exists at launch).
- "Skip for now" follows the Tier 1 Safe Exit path with the Auto-Pilot Acceptance Modal (FR-37.1).
- The failure reason is logged for product instrumentation.
- *"Help — what went wrong?"* surfaces a context-aware support article authored before launch (see §16 SOFT-14, owner: Support team).

---

### 4.4 Operations & Communications Configuration

**Description:** Sections 2 and 3. Captures the operational defaults (cleaning workflow, guest access) and pre-configures the automated guest messaging. Realizes UJ-1, UJ-5.

**Functional Requirements:**

#### FR-18: Q2.1 cleaning system with partner detection

Q2.1 captures the cleaning workflow. If Salesforce Account Data `Partners` (normalized via FR-18.1) contains "Turno" or "Breezeway," the system auto-advances with a confirmation. Otherwise the user selects from three options per V4.

**Consequences (testable):**
- Partner detection runs against the *normalized* `Partners` array.
- On partner detect, the system writes `cleaning_workflow = auto_routed_to_{{partner}}` to the Profile Configuration.
- On user select of A/B/C, the system writes the matching configuration domain value per the Profile Output Schema (FR-44).
- For unrecognized partner strings (not in the Alias Table), the Wizard falls through to standard A/B/C options *and* logs the unrecognized string for review.

#### FR-18.1: Partner Alias Table — normalized matching

Partner detection uses a maintained alias table that maps known string variants (case, whitespace, suffix) to canonical partner identifiers. The Partner Alias Table is a Phase 0 deliverable, owned by PM with Data team support.

**Consequences (testable):**
- The Alias Table is exposed in the Profile Output Schema artifact (FR-44).
- All FR-7 partner-detection rules use the Alias Table; bot copy uses the canonical partner display name (`Turno`, `Breezeway`, `PriceLabs`, `Beyond`) rather than raw CRM strings.
- Unknown / unmapped strings are logged for ongoing alias table maintenance; they do not surface to the user under any other partner name.
- A surfacing-to-user whitelist applies: only partners in the canonical set appear in user-facing copy. Unrecognized partner CRM data is not surfaced verbatim.

#### FR-18.2: Multi-partner disambiguation

If multiple matching partners are detected for the same Question (e.g., `Partners` contains both "Turno" and "Breezeway" for Q2.1, or both "PriceLabs" and "Beyond" for Q7.2), the user sees a one-question disambiguation: *"We see you may use both — which is your active cleaning system?"* (or equivalent).

**Consequences (testable):**
- Disambiguation lists detected partners and an "I use both" option (which routes to the standard non-partner path).
- Selected partner is written; the other detection is logged as "not active for this customer."

#### FR-19: Q2.2 guest access method capture

Q2.2 captures the guest access method (Smart Lock, Lockbox/Keypad, In-person). Smart Lock answer expands an inline provider dropdown.

**Consequences (testable):**
- The provider dropdown only renders if "Smart Lock" is selected.
- "Other" provider triggers a free-text field with a 60-character limit and validation per FR-6.
- The answer is the input to Q3.2 template branching.

#### FR-20: Q3.1 Unified Inbox awareness + automation opt-in

Q3.1 introduces Unified Inbox and offers to set up automated check-in messages + review requests. Variant copy if `Unread_Message_Count > 5`. Selecting "Yes, set them up" continues to Q3.2; "I'll do this later" skips to Section 4 and flags "Automated Messaging" as a Call 1 Prep item.

**Consequences (testable):**
- The variant copy switches at the `Unread_Message_Count > 5` threshold using the value at first-answer time (Branching Snapshot per §4.11).
- A "Yes" answer does *not* immediately activate any message template — activation happens after the user confirms templates in Q3.2/Q3.3.
- A "later" answer adds "Automated Messaging" to the To-Cover-With-CSM list.

#### FR-21: Q3.2 check-in template — pre-drafted by access method with placeholder validation

Q3.2 renders a pre-drafted check-in message template selected by the Q2.2 access method (Smart Lock, Lockbox/Keypad, In-person variants per V4). The user accepts or edits inline.

**Consequences (testable):**
- The exact wording per variant matches V4 Section 3 Q3.2 copy. V4 is version-locked concurrent with this PRD; the cross-reference must not drift (see §16 SOFT-26).
- "Let me edit it" opens an inline editor with the pre-drafted text loaded; saved edits override the default.
- *Template placeholder validation:* required placeholders per variant (`{{guest_first_name}}`, `{{pin_code}}` / `{{code}}` / `{{lockbox_location}}`, `{{check_in_time}}`, `{{check_out_time}}`) are validated on save. Missing required placeholders surface an inline warning ("Your template won't include the door code — add `{{pin_code}}` or skip the door-code variant?") with options to auto-restore or proceed.
- Templates store with UTF-8 encoding; guest names with non-Latin scripts render correctly.
- "Use it" activates the template for outbound sending on the customer's account, gated by the Consent Record (Operator) per FR-43.
- The template's send-trigger timing (2hr / 24hr / 24hr) is set per V4.
- Backward navigation that changes Q2.2 access method invalidates the Q3.2 answer: the previously-activated template is deactivated, Q3.2 reverts to its unanswered state with the new variant, and the user is notified ("Your check-in message was set up for Smart Lock — let's adjust it now").

#### FR-22: Q3.3 review request automation

Q3.3 captures whether to auto-send review requests 1 hour after every checkout. Two-option single-select.

**Consequences (testable):**
- "Yes" activates the review request automation, gated by Consent Record (Operator).
- "No" leaves the automation inactive; user can enable it later in Guesty Settings.

#### FR-23: Automated message activation requires explicit per-template opt-in

No automated message template is activated on the customer's account without an explicit per-template user choice in Q3.2/Q3.3.

**Consequences (testable):**
- A user who skips Section 3 entirely has zero message templates activated.
- A user who answers Q3.1 "Yes" but bails before completing Q3.2 has zero check-in templates activated.
- A user who answers Q3.2 "Use it" but bails before Q3.3 has only the check-in template activated, not review requests.
- Editing a Q3.2 template via "Use it → backward → edit → Use it" hot-swaps the live template content; *queued outbound messages scheduled under the old content* use the *new* content at send time. Already-sent messages are not affected. **Hot-swap semantics confirmed 2026-05-25.**

#### FR-24: Section 2 & 3 outputs feed Section 8 summary

Section 2 and Section 3 answers populate the `{{cleaning_setup_summary}}`, `{{access_method_summary}}`, `{{messaging_setup_summary}}` variables defined in V4 Appendix A.

**Consequences (testable):**
- Each variable resolves to exactly one of the V4 Appendix A possible output values.
- Skipped Sections resolve to *"Not configured — covered on your call."*

---

### 4.5 Financials with Accountant Delegation

**Description:** Sections 4 and 5. Confirms Decision Owner, optionally delegates Financials to a separately-named Financial Owner via the Accountant Secure Link. The Stripped Section 5 View is a new sub-surface introduced in V1. **The Delegation Lifecycle state machine is specified in §4.10** — the FRs in this section assert behavior; §4.10 specifies the states. Realizes UJ-4.

**Functional Requirements:**

#### FR-25: Q4.1 Decision Owner confirmation (SMB-simplified)

Q4.1 confirms the authenticated user is the Decision Owner. "Someone else owns financials" expands to capture the Financial Owner's name and email inline.

**Consequences (testable):**
- "Primary owner" answer writes `decision_owner = current_user` and transitions Delegation Lifecycle to `not_offered` (or leaves it there).
- "Someone else" answer requires name + email before "Continue" is enabled, and transitions Delegation Lifecycle to `offered`.
- Email is validated (RFC 5322 basic format) before submit.
- The captured Financial Owner pre-populates Q5.1's delegation path.

#### FR-25.1: Financial Owner email must differ from operator email

The Q4.1 "Someone else" expansion validates that the entered email is not the operator's authenticated email. If it matches (case-insensitive), the user sees a warning: *"This looks like your own email — did you mean to do it yourself?"* with "Edit" and "I'll do it myself" options. The latter clears the delegation and treats Q4.1 as "primary owner."

**Consequences (testable):**
- Match is case-insensitive after normalization.
- Subdomain variants (e.g., `alice+work@x.com` vs `alice@x.com`) are flagged but allowed with confirmation.

#### FR-25.2: Q4.1 change cascades

If the user navigates Backward to Q4.1 and changes from "Someone else" to "primary owner," any pending delegation (if Q5.1 already triggered the link send) is cancelled per the Delegation Lifecycle (§4.10) and the captured Financial Owner is cleared.

**Consequences (testable):**
- An outstanding Accountant Secure Link is invalidated immediately on Q4.1 change.
- The captured Financial Owner name/email are removed from session state.
- The operator sees a notice: *"Delegation to Jane has been cancelled."*

#### FR-26: Q5.1 delegation check with two-path branching

Q5.1 branches by Q4.1 result. Primary-owner path offers an in-flow "Send to my accountant" inline option; delegated path leads with the send-link CTA pre-filled with the Q4.1 Financial Owner. Q5.1's transitions are governed by the Delegation Lifecycle (§4.10).

**Consequences (testable):**
- "I'll handle it now" path proceeds to Q5.2.
- "Send to my accountant" / "Send to {{financial_owner_name}}" path triggers `sent` state and marks Section 5 as `→ Delegated to {{name}}` in the nav.
- Once delegated, the operator skips to Section 6; Section 5 is not revisitable from the operator's nav UNLESS the operator cancels the delegation (FR-50.6).

#### FR-27: Accountant Secure Link send and uniqueness

When delegation is chosen, the system sends an email to the Financial Owner with a unique, scoped, expiring secure URL to the Stripped Section 5 View.

**Consequences (testable):**
- The email is sent within 30 seconds of operator action.
- The URL is unique per delegation; no URL reuse across customers, operators, or accountants.
- The URL expires after 14 days. **14-day expiry confirmed 2026-05-25.**
- The URL is scoped to Section 5 only; it does not authenticate the user for any other Guesty surface.
- Each link starts a fresh, scoped accountant session; multiple links sent to the same accountant for different operators are independent (no cross-link state sharing).
- Email content follows the safety-first copy direction in Brief Addendum §6 and includes operator's first name and call date.
- Bounce / delivery-failure handling: if the email infra reports a hard bounce or non-delivery within 1 hour, the operator's next Wizard or dashboard load surfaces a notice: *"Your delegation email to Jane didn't arrive. Try a different email or do it yourself."* with "Edit email," "Resend," and "I'll do it myself" CTAs.

#### FR-28: Stripped Section 5 View

The Accountant Secure Link opens a scoped Wizard surface that renders only Section 5 (delegation-confirmation through Q5.3) plus a context header and a separate consent banner. No persistent header (no countdown, no Section nav, no Skip button). No other Sections reachable. Realizes UJ-4.

**Consequences (testable):**
- The context header reads *"Setting up financials for {{operator_first_name}}'s Guesty account"* with the operator's call date below.
- The accountant sees a one-line confirmation in place of Q5.1: *"You've been asked by {{operator_first_name}} to complete the financial setup. Should take about 90 seconds."*
- Q5.2 and Q5.3 render identically to the operator's view.
- The Stripped View includes a *"This isn't for me"* secondary CTA (per FR-50.4).
- On Q5.3 completion, the view displays a confirmation (*"Thanks — {{operator_first_name}} has been notified."*) and ends. The accountant cannot navigate to any other Wizard or Guesty surface.
- On any link error state (expired, invalid, superseded), the accountant sees a single error page with no operator data leaked and no link to other Guesty surfaces.

#### FR-28.1: Accountant-scoped Consent Record

Before the accountant can submit Q5.2 or Q5.3 writes, the Stripped Section 5 View renders an accountant-scoped consent banner. The accountant must acknowledge it (single click on a "Continue" CTA tied to a checkbox or one-tap acknowledgment). The acknowledgment is persisted as the Consent Record (Accountant), separate from the operator's Consent Record.

**Consequences (testable):**
- The banner reads (subject to legal review, see §16 BLOCKER-4): *"{{operator_first_name}} has asked you to configure their Guesty payment policy and fees. We'll apply your answers directly to their account. You're not creating an account — this is a one-time setup for {{operator_first_name}}."*
- A persistent Consent Record (Accountant) is written with timestamp, operator account ID, accountant email, link token ID, and verbatim wording.
- Writes from the Stripped View are gated on BOTH the Operator Consent Record (FR-2) AND the Accountant Consent Record being present; absence of either blocks the write.

#### FR-29: Stripped Section 5 View — data exposure constraints

The Stripped Section 5 View minimizes the Financial Owner's exposure to the operator's other configuration data.

**Consequences (testable):**
- The Financial Owner cannot see any Section 1–4, 6–8 content.
- The Financial Owner cannot see the operator's listing count, reservation count, unread message count, or any other Live Airbnb data.
- The Financial Owner *can* see the operator's `industry` (used in Q5.3 fee suggestions) and the operator's account currency (used in Q5.2/Q5.3 wording and unit). **Industry + currency exposure to accountant confirmed acceptable 2026-05-25.**
- Failed authentication (expired link, malformed URL, superseded delegation) shows a single error page with no operator data leaked.

#### FR-30: Q5.2 payment timing

Q5.2 captures default payment policy for direct bookings (100% at booking / 50-50 split / "What do you recommend?"). The "recommend" option applies the 50-50 default after the bot recommendation, with an explicit confirm step.

**Consequences (testable):**
- The three options match V4 exactly.
- The recommend path is two-step: show recommendation copy → explicit "Use 50/50" or "Choose something else" CTAs → write.
- The recommend-then-apply path writes the 50-50 configuration value, distinguishable in the `{{payment_setup_summary}}` rendering (V4 Appendix A).
- A skipped Q5.2 applies the Auto-Pilot Default ("100% at booking") only if the user explicitly accepted the Auto-Pilot Acceptance Modal per FR-37.1.

#### FR-31: Q5.3 mandatory fees with industry-based highlight and currency anchoring

Q5.3 captures mandatory fees as a multi-select with industry-based default highlighting. Per-fee amount + unit configurable inline. Per-fee amount is interpreted in the operator's account currency.

**Consequences (testable):**
- The industry-based highlight uses `industry` from Salesforce Account Data.
- Per-fee amount input accepts currency-formatted positive numbers with a 4-digit max integer part *in the operator's account currency*. Currency symbol is rendered next to the input.
- Per-fee unit selects between "per stay" and "per night."
- "None" auto-advances and writes empty fees configuration; "None" mutual-exclusion with other selections per FR-6.
- Cleaning fees are *not* offered in Q5.3 (already imported from Airbnb per V4 copy).
- If listings span multiple currencies (rare for SMB), Q5.3 surfaces a one-line note ("Your listings use multiple currencies — fees are set for your account's primary currency, {{currency}}") and proceeds with the primary currency.

#### FR-31.1: Reasonableness validation on fees

Per-fee amounts are validated against an industry-relative reasonableness range. Out-of-range entries trigger a soft warning (not a hard block).

**Consequences (testable):**
- Fee amount thresholds per industry are defined in the Profile Output Schema artifact (FR-44).
- For SMB account industries, typical max ranges might be: Damage Waiver $0–$200/stay; Resort Fee $0–$50/night; other fees $0–$300/stay. *(Exact ranges TBD in FR-44.)*
- An out-of-range entry surfaces an inline warning: *"$9,999/stay is unusually high — confirm or edit."* with "Confirm" and "Edit" CTAs.
- For accountant-submitted fees (via Stripped Section 5), any out-of-range entry creates an *operator-review-required* flag on the operator's next Wizard or dashboard load before the fee is applied to live config. See FR-50.7.

---

### 4.6 Call 1 Personalization & Quick Wins

**Description:** Sections 6 and 7. Personalizes the CSM call agenda and offers high-value, low-effort items the user can knock off while still in the Wizard. Realizes UJ-1, UJ-5.

**Functional Requirements:**

#### FR-32: Q6.1 priority topic with explicit suggestion ordering

Q6.1 surfaces up to two dynamic suggested priority topics plus a free-text option. Suggestion order is deterministic per FR-7. The Q6.1 answer feeds the CSM Handoff Artifact (FR-32.1).

**Consequences (testable):**
- Suggestion ordering per FR-7 (Q6.1 rule).
- Free-text input has a 200-character limit, sanitized on render to CSM-facing surfaces.
- Selected topic writes to `call_1_priority_topic` and is included in the CSM Handoff Artifact.
- When `customer_churn_reason` data is absent for the user's region/size cohort, the "Trust Accounting" suggestion does not surface.

#### FR-32.1: CSM Handoff Artifact

The Wizard produces a structured CSM Handoff Artifact at Section 8 completion (and partial artifacts on Safe Exit). The artifact is the canonical pre-Call-1 input for CSMs.

**Consequences (testable):**
- The artifact's Salesforce field spec is a Phase 0 deliverable (see §16 BLOCKER-11), owned by PM with CSM Leadership sign-off.
- The artifact includes, at minimum: `call_1_priority_topic`, `to_cover_with_csm` (list of skipped items), `urgent_route_active` (Boolean from FR-11.1), `wizard_completion_state`, `wizard_started_at`, `wizard_completed_at`, `auto_pilot_applied` (Boolean), `delegation_status` (per the Delegation Lifecycle), and a summary of configured items (Section 8 summary).
- The artifact is written at Section 8 render and updated on Safe Exit; CSMs see it via a defined Salesforce view (spec in FR-44).
- Free-text fields (Q6.1 priority topic) are sanitized for CSM-facing render to prevent XSS / injection.

#### FR-33: Q7.1 owner contacts upload (CSV)

Q7.1 captures property owner contacts via CSV upload if Salesforce Account Data `Owners` > 0; otherwise the Question is skipped entirely. *Owners means third-party property owners, not Guesty user owners (per Glossary).*

**Consequences (testable):**
- If `Owners` count is 0 or null, Q7.1 does not render.
- The CSV picker accepts files up to 1 MB with `.csv` extension. UTF-8 encoding required; BOM tolerated.
- A downloadable template is offered inline.
- Required columns: `owner_name`, `owner_email`, `property_ref`. Extra columns are silently ignored.
- Validation: missing required columns surface an inline error. Row-level: rows with invalid emails or missing required fields are skipped; valid rows are imported. A summary surfaces *"Imported 45 of 47 rows. 2 rows skipped: row 17 (invalid email), row 32 (missing owner_name)."*
- Deduplication: duplicate `owner_email` + `property_ref` pairs are treated as last-row-wins.
- Uploaded contacts are stored in the customer's Guesty account; no email is sent to any owner in V1.
- Owner Prep safety copy: the Q7.1 upload confirmation state must include explicit safety framing. Example: *"Added — your owners won't receive anything automatically. Set up owner communications in Settings when you're ready."* This copy is a launch requirement; the UX spec must not ship without it (per §10 safety-first phrasing guidance).

#### FR-34: Q7.2 minimum stay with pricing-partner detection

Q7.2 captures default minimum stay, with PriceLabs/Beyond detection auto-skipping the Question per V4. No-data fallback per FR-7.

**Consequences (testable):**
- Partner detection via the Partner Alias Table.
- Otherwise, user picks "Yes, 2 nights" or "Let me set a custom minimum…" (free numeric input, integer 1–14, hard cap with counter per FR-6).
- Q7.2 bot copy references `{{avg_los}}` from `Average_Length_of_Stay`. When `Average_Length_of_Stay` is null (new host), the copy falls back to a generic phrasing.

---

### 4.7 Tiered Skip Intercept System

**Description:** The Skip-to-Dashboard button's behavior adapts to the user's Wizard investment level via four Tiers. Auto-Pilot Defaults apply on Safe Exit at any Tier, **subject to FR-37.1's Auto-Pilot Acceptance Modal**. Realizes UJ-3.

**Functional Requirements:**

#### FR-35: Skip intercept Tier resolution

The Skip-to-Dashboard button's intercept Tier is computed from the current Section per V4: Tier 1 (pre-Section-1-completion), Tier 2 (Sections 2–3), Tier 3 (Sections 4–6), Tier 4 (Section 7).

**Consequences (testable):**
- Tier resolution is server-evaluated on click.
- Tier 3 inside Section 5 (financials) uses Section-5-specific intercept copy (when defined — see §16 SOFT-25), reflecting financial data sensitivity. Other Sections in Tier 3 use the V4 default copy.
- Tier 4 (Quick Wins) does *not* render an intercept modal; clicking Skip immediately triggers Safe Exit (subject to FR-37.1).

#### FR-36: Tier intercept modal rendering

Tiers 1, 2, and 3 render an intercept modal with the V4 copy, primary CTA (continue), and secondary CTA (Safe Exit).

**Consequences (testable):**
- The modal is dismissable only via one of the two CTAs (or `Esc`, which counts as dismiss without exit per FR-6 keyboard model).
- The modal copy resolves `{{CSM_Name}}` and `{{remaining_section}}` (Tier 2 only) before render.
- Primary CTA returns the user to the current Question without state change.
- Secondary CTA triggers Safe Exit per FR-37 (subject to FR-37.1).

#### FR-37: Safe Exit and dashboard landing

Safe Exit at any Tier lands the user on their Guesty dashboard *after* the Auto-Pilot Acceptance Modal (FR-37.1) is presented and acknowledged.

**Consequences (testable):**
- All in-flight writes (FR-9) are drained before evaluating Auto-Pilot scope (FR-37.2).
- Auto-Pilot Defaults apply only to Questions with no pending write *and* no prior answered value (i.e., truly unanswered).
- The dashboard "Finish Setup" link renders per FR-5.

#### FR-37.1: Auto-Pilot Acceptance Modal

Before Auto-Pilot Defaults are written on Safe Exit, the user sees a confirmation modal listing the defaults that will be applied. No writes occur until the user accepts.

**Consequences (testable):**
- The modal lists each default in plain language: *"Payment policy: 100% at booking. Automated messages: off. Minimum stay: inherited from Airbnb."* etc., scoped to Questions the user did not answer.
- The modal has two CTAs: "Apply these and go to dashboard" (primary) and "Take me back to finish" (secondary).
- Acceptance writes the defaults atomically per write domain (FR-43); rejection returns the user to the current Question.
- Tier 4 (Quick Wins) skips the modal: at Section 7, all higher-Tier Sections are already configured, so the defaults to apply are minimal and an extra confirmation step is friction. *Auto-Pilot for Quick Wins items writes silently.*
- If no Consent Record exists (Tier 1 skip from cover screen without consent), the modal is *not* shown — no writes occur. The user lands on a fully-default Guesty account and is prompted to consent in-app on first write action (V4 Appendix B "Consent record" row).

#### FR-37.2: In-flight write draining on Safe Exit

When Safe Exit fires while a write is in flight (e.g., user clicks Skip immediately after answering Q5.2), the system drains the in-flight write before determining Auto-Pilot scope.

**Consequences (testable):**
- Writes complete (success or final-failure-with-retry-queued per FR-49) before Auto-Pilot evaluates which Questions are unanswered.
- Auto-Pilot does not overwrite a successfully-written Question.

#### FR-38: Per-Tier intercept copy exposure

Each Tier's intercept copy matches V4 verbatim, with the Section-5-specific override (FR-35) for Tier 3 inside Section 5.

**Consequences (testable):**
- Tier 1 copy per V4.
- Tier 2 copy per V4.
- Tier 3 copy per V4 (Sections 4 and 6) or Section-5-specific (when defined).
- Tier 4: no modal.

#### FR-38.1: A/B test framework for intercept copy

V1 ships with an A/B test slot enabled for Tier 1 intercept copy. The slot defaults to the V4 wording; an alternate variant can be configured for cohort-level testing.

**Consequences (testable):**
- A configurable A/B framework is integrated into the Tier 1 render path.
- The cohort assignment for the A/B test is sticky alongside the Wizard Cohort (FR-10).
- An "intercept-induced abandonment" counter-metric (SM-C6) is instrumented.

---

### 4.8 Review & Handoff

**Description:** Section 8. The "What's Configured" summary, the "Coming Up" call info with calendar-add, and the conditional "To Cover With CSM" list. Realizes UJ-1, UJ-2, UJ-4, UJ-6.

**Functional Requirements:**

#### FR-39: "What's Configured" summary renders all variables

Section 8 renders the V4-specified summary with variables resolved per V4 Appendix A.

**Consequences (testable):**
- All variables in V4 Appendix A render with one of the listed possible output values.
- Variables corresponding to skipped Sections render *"Not configured — covered on your call."*
- The summary renders even if every Section was skipped: listing and reservation counts are 0 or null, and the empty-state copy reads *"Your account is set up with safe defaults. Connect Airbnb later from your dashboard."* with a "Connect Airbnb" CTA.
- If a re-poll between Q1.2 and Section 8 detected a meaningful change (e.g., the original urgent-route window has passed), the summary notes the original signal with *"Initially flagged urgent — window now passed."* See FR-11.1.

#### FR-40: "Coming Up" call info with calendar add and refresh on render

Section 8 displays the Setup Call info with three calendar-add options (Google, Apple, Outlook). Call metadata is re-fetched on Section 8 render to ensure currency.

**Consequences (testable):**
- Each calendar-add option generates a valid calendar entry with `{{CSM_Name}}`, `{{call_date}}`, `{{call_time}}`, `{{timezone}}`, and the call link.
- If the call has been rescheduled or cancelled in Salesforce during the session, Section 8 surfaces a notice: *"Your call was rescheduled to {{new_call_date}}"* (or *"Your call was cancelled — reschedule"*) with updated CTAs.
- Calendar entries are stable per session: refreshing the page does not regenerate tokens or invalidate previous adds.
- A "Calendar add failed" fallback offers a copyable details block with call time / CSM / link.

#### FR-41: "To Cover With CSM" renders only when items exist

The To-Cover-With-CSM section renders if and only if at least one item was skipped, delegated, expired, or flagged.

**Consequences (testable):**
- Empty state: section is not rendered (no empty header).
- Each rendered item maps to a human-readable label (e.g., "Financial setup," "Smart messaging templates," "Owner contacts upload").
- Items are persisted to the CSM Handoff Artifact (FR-32.1).

#### FR-42: Section 8 dashboard handoff

Section 8's primary CTA "Go to Dashboard" navigates to the customer's Guesty dashboard. Secondary CTA "View Call Prep" navigates to the V1 Call Prep view.

**Consequences (testable):**
- "Go to Dashboard" deep-links to the customer's main Guesty dashboard.
- The V1 "Call Prep" view is a minimal Salesforce-or-equivalent surface displaying the CSM Handoff Artifact contents in customer-facing form. Full dashboard widget is V2. `[ASSUMPTION: V1 Call Prep is a minimal view, not a placeholder — see §16 SOFT-15.]`

---

### 4.9 Profile Configuration Writes

**Description:** The set of system writes the Wizard performs to the customer's live Guesty account based on their answers. Gated by the Consent Record (Operator) and, for accountant writes, the Consent Record (Accountant). **The field-by-field mapping (Profile Output Schema) is a Phase 0 precondition — not a deferred deliverable. See §14 Phase 0 and FR-44.** Realizes all UJs.

**Functional Requirements:**

#### FR-43: All Profile Configuration Writes are Consent-Record-gated

No Profile Configuration Write executes without the appropriate Consent Record(s). Writes from the operator's flow require the Consent Record (Operator). Writes from the Stripped Section 5 View require BOTH the Consent Record (Operator) AND the Consent Record (Accountant) per FR-28.1.

**Consequences (testable):**
- A write attempted without the required Consent Record(s) fails the write, logs the event, and surfaces a prompt to consent (operator) or blocks the accountant from submission (accountant).
- Once the Consent Record exists, pending writes from the session execute atomically per write domain.
- Consent Record absence is detected at every write attempt (not cached per session).
- The Consent Record write itself is synchronous and read-after-write verified (FR-2); writes do not begin until consent is confirmed persistent.

#### FR-44: Profile Output Schema is a Phase 0 precondition

The Profile Output Schema artifact specifies, for every Question answer, the exact configuration domain and field(s) written to the customer's live Guesty account. **It is a Phase 0 deliverable — Phase 1 dogfood cannot begin until it is locked.** PM-owned with engineering sign-off.

**Consequences (testable):**
- The schema covers, at minimum, these configuration domains: listings (sync state), unified_inbox (active flag), automated_messages (templates + activation flags), payment_policy (timing + fees, with reasonableness ranges per FR-31.1), property_defaults (min_stay), owner_records, decision_owner, consent_record (operator and accountant), Partner Alias Table (FR-18.1).
- The schema also specifies the CSM Handoff Artifact field structure (FR-32.1).
- Phase 1 entry is gated on schema lock (§14).
- The schema is the source of truth for the write semantics that FR-43, FR-45, FR-46, FR-47, FR-49 depend on. If the schema discovers a write semantic that is not supported by the existing Guesty backend (e.g., message-template activation requires a state-machine not currently exposed), the affected FRs are renegotiated.

#### FR-45: Writes are idempotent

A Profile Configuration Write for the same Question answer is idempotent.

**Consequences (testable):**
- Editing a Question (via Backward) and re-saving the same value is a no-op at the account level.
- Editing a Question to a different value overwrites the prior value, applies cascading invalidations per §4.11 (e.g., Q2.2 change invalidates Q3.2), and logs the change.
- An automated message template activated via "Use it → backward → edit → Use it" results in a hot-swapped template with new content; queued outbound messages use the new content (per FR-23).

#### FR-46: Consent revocation behavior

If a customer revokes consent post-Wizard (via Settings), writes already made remain in place; future writes are blocked until consent is restored. **No rollback.** This applies globally, including EU customers — the EU/international exposure was evaluated and no-rollback was adopted as the V1 policy (2026-05-25, see `.decision-log.md`).

**Consequences (testable):**
- Revocation flag is checked on every new write.
- Revocation does *not* trigger rollback of existing writes.
- Revoking surfaces an in-product notice listing what's already been configured.
- An intra-Wizard revocation flow is *not* in scope for V1; revocation is a Settings-only action post-Wizard.

#### FR-47: Auto-Pilot Defaults are written conservatively (per FR-37.1 acceptance)

When Safe Exit triggers Auto-Pilot Default writes (FR-37 + FR-37.1), the writes follow V4 Appendix B and apply only to unanswered Questions.

**Consequences (testable):**
- No automated message template is activated by Auto-Pilot.
- No payment processing rule beyond the safest default (`100% at booking`) is activated.
- No third-party contact (owner email send) occurs.
- The Auto-Pilot Default set exactly matches V4 Appendix B.
- Already-answered Question writes are preserved (Auto-Pilot does not overwrite).

#### FR-48: Wizard writes are observable

Every Profile Configuration Write emits a structured event.

**Consequences (testable):**
- Event fields include: timestamp, customer ID, account ID, Question ID, configuration domain, new value, was_auto_pilot, actor (enum: `operator | accountant | csm | system_default`).
- Events are queryable by the CSM and product analytics.
- PII handling follows existing Guesty event-stream conventions. `[ASSUMPTION: existing conventions cover this — confirm with Data, see §16 SOFT-22.]`

#### FR-49: Wizard surfaces write failures non-blockingly with retry contract

If a Profile Configuration Write fails, the Wizard does not block the user's flow but surfaces a notice and retries.

**Consequences (testable):**
- A write failure does not roll back the user's Question answer.
- A non-blocking banner: *"We're having trouble saving some of your changes — we'll keep trying."* Per the shared toast component spec (§16 SOFT-23).
- Retry: 3 retries with exponential backoff; on final failure, the answer is queued and re-attempted on next Wizard entry.
- The failure is added to the CSM Handoff Artifact as an internal flag (CSM sees, customer doesn't).
- Batches are atomic per write domain: a partial batch failure rolls back the batch (or, if rollback not possible, queues a compensating retry) so the customer's account is never half-configured per domain.

---

### 4.10 Delegation Lifecycle (cross-cutting state machine)

**Description:** Section 5 financial delegation is governed by an explicit state machine that spans the Operator's Wizard session, the Accountant's Stripped Section 5 View, and the Wizard's persistent state. This section specifies the states and transitions; §4.5 FRs are evaluated against this lifecycle.

#### States

| State | Meaning |
|---|---|
| `not_offered` | Q4.1 not yet answered, OR operator chose "primary owner." Delegation is not active. |
| `offered` | Q4.1 answered "Someone else owns financials"; Financial Owner captured but Q5.1 not yet reached. |
| `sent` | Q5.1 delegation triggered; Accountant Secure Link emailed; awaiting accountant click. |
| `opened` | Accountant clicked the link, landed on Stripped Section 5 View, but has not yet submitted Q5.3. |
| `completed` | Stripped Section 5 submitted (Q5.3 answered); operator's Section 5 marks `done`. |
| `expired` | 14-day expiry passed without `opened` or `completed`. |
| `cancelled` | Operator cancelled the delegation before `completed`. |
| `superseded` | Operator self-completed Section 5 after delegation was sent; the secure link is invalidated. |

#### Transitions and FRs

#### FR-50: Delegation Lifecycle is the single source of truth

All delegation-related FRs (FR-25 through FR-31, and the Stripped View FRs) evaluate against this state machine. Section 5's nav status is derived from the current state.

**Consequences (testable):**
- The state machine is the single source of truth across operator session, accountant session, and persistence layer.
- Section 5 nav status mapping: `sent | opened` → `→ Delegated to {{name}}`; `completed` → `✓` ; `expired | cancelled | superseded` → `○` (unlocked, available to operator).

#### FR-50.1: Locking on accountant `opened`

When the accountant transitions delegation to `opened`, the operator's Section 5 view is locked from self-completion. The operator can still cancel (FR-50.6) but cannot edit Q5.2/Q5.3 while the accountant is mid-flow.

**Consequences (testable):**
- Operator's nav surfaces *"Jane is filling this out now — you can cancel to take over."* with a "Cancel delegation" CTA.
- Operator self-completion is gated until state moves to `cancelled` or `completed`.

#### FR-50.2: Last-write semantics on `completed`

When the accountant transitions delegation to `completed`, those Q5.2/Q5.3 values become canonical. If the operator had also entered Q5.2/Q5.3 values pre-delegation (e.g., started Section 5, then switched to delegate), the operator's values are overwritten by the accountant's on `completed`.

**Consequences (testable):**
- The operator sees a notice on next session: *"Jane completed your financials. Your earlier inputs were replaced — review in the summary if you'd like."*

#### FR-50.3: Operator self-completion → `superseded`

If the operator navigates back to Section 5 and self-completes Q5.2/Q5.3 while a delegation is `sent` or `opened`, the system transitions delegation to `superseded`, invalidates the outstanding Accountant Secure Link, and notifies the accountant (if state was `opened`).

**Consequences (testable):**
- The accountant's Stripped Section 5 View, if open, displays a "this delegation was completed by the operator" notice on next interaction.
- Future clicks on the secure link land on the standard error page (per FR-28).
- The operator's Section 5 transitions to `done`.

#### FR-50.4: Accountant "This isn't for me" → `cancelled`

The Stripped Section 5 View includes a *"This isn't for me"* secondary CTA. Clicking it transitions delegation to `cancelled` and notifies the operator.

**Consequences (testable):**
- The CTA is below the consent banner, less prominent than "Continue."
- An optional one-line reason field captures *"Why?"* (60 chars).
- The operator sees a notice on next session: *"{{accountant_name}} declined the delegation. Reason: '{{reason}}'."* (or no reason). Section 5 reverts to `unlocked` and the operator can self-complete or re-delegate.

#### FR-50.5: Expiry transition to `expired`

If 14 days pass with the delegation in `sent` or `opened` state without reaching `completed`, the system transitions to `expired` and notifies the operator.

**Consequences (testable):**
- Operator notification on next session: *"Your delegation to {{accountant_name}} expired. You can resend the link or do it yourself."* with "Resend" (re-issues a fresh 14-day link) and "I'll do it myself" CTAs.
- The expired link returns the standard error page on click (FR-28).
- Section 5 reverts to `unlocked`.
- If the operator has Safe-Exited the Wizard with Auto-Pilot accepted, but Section 5 was `delegated` at the time, Auto-Pilot Defaults for Section 5 (per FR-37.1) are applied on `expired`. The operator is notified that defaults were applied.

#### FR-50.6: Operator cancellation (`cancelled`)

The operator can cancel an outstanding delegation from their Section 5 nav item via a "Cancel delegation" CTA.

**Consequences (testable):**
- The CTA is visible when delegation state is `sent` or `opened`.
- Cancellation invalidates the secure link immediately and notifies the accountant (if `opened`).
- Section 5 reverts to `unlocked`; operator can self-complete or re-delegate.

#### FR-50.7: Accountant-submitted out-of-range fees → operator review

When the accountant submits fees that fall outside the reasonableness range (FR-31.1), the delegation transitions to `completed` but the fees are NOT applied to live config until the operator confirms them on next Wizard or dashboard load.

**Consequences (testable):**
- Operator sees a review prompt: *"{{accountant_name}} entered Damage Waiver $9,999/stay. Confirm or edit before this applies to bookings."*
- Operator can confirm (writes the value) or edit (writes the new value).
- Until confirmed, the fee is in a `pending_operator_review` state in the Profile Output Schema.

---

### 4.11 Branching & Data Freshness Model (cross-cutting)

**Description:** This section consolidates the data freshness model that spans multiple FRs (FR-4, FR-7, FR-10, FR-11, FR-11.2, FR-15) into a single coherent specification.

#### Freshness model

- **Salesforce Account Data:** snapshot at Wizard entry. Used for the full session. Mid-session changes in Salesforce do *not* re-evaluate branching that has already been evaluated. (See FR-4.)
- **Live Airbnb Data Hooks:** re-polled on every Wizard entry (FR-11) but only for *new* branching decisions and the Section 8 summary. Already-answered Questions render with the values captured in their Branching Snapshot (FR-11.2).
- **Branching Snapshot:** at the moment a Question is first answered, the system captures the data values used for that Question's branching predicate and variant copy. The snapshot is immutable for that Question across resumes and Backward navigation, unless the user actively edits the Question.
- **Active edits:** when the user actively edits an already-answered Question, the snapshot is refreshed to current data, and any downstream cascading invalidations apply (e.g., changing Q2.2 access method invalidates the Q3.2 template per FR-21).
- **Cascading invalidations:** changes to a Question that downstream Questions depend on (e.g., Q4.1 → Q5.1; Q2.2 → Q3.2; Q3.1 → Q3.2/Q3.3) trigger explicit notifications and re-prompts on the affected downstream Questions. The downstream Question reverts to its unanswered state with the new variant data.

#### Resume validity (per FR-10)

When resuming, if the user's last-answered Question's predecessor branch is no longer valid (e.g., Q1.2 routed them to Section 5 urgent, they answered Q5.1, came back to find no upcoming check-in), the resume target falls back to the closest valid Question with a toast notice. The previously-answered Questions remain editable; cascading invalidations may have already been applied if any earlier predicate flipped.

#### No-data branches

Every branching predicate has an explicit no-data branch (FR-7). The full mapping:

| Question | Predicate | No-data branch |
|---|---|---|
| Q1.2 | `Next_Check_In_Date < 48h` | Auto-advance to Section 2 (no urgent route) |
| Q2.1 | `Partners` contains "Turno" / "Breezeway" | Standard A/B/C options |
| Q3.1 | `Unread_Message_Count > 5` | Standard variant copy |
| Q3.2 | `access_method` from Q2.2 | Generic template with inline access-method picker |
| Q6.1 | suggestion logic with three rules | Free-text only |
| Q7.1 | `Owners > 0` | Question hides |
| Q7.2 | `Partners` contains "PriceLabs" / "Beyond" | Standard A/B options; `{{avg_los}}` falls back to generic copy |

---

## 5. Non-Goals (Explicit)

- The Wizard is not full self-serve onboarding. Call 1 remains the activation milestone.
- The Wizard is not a checklist.
- The Wizard is not a replacement for Rocketlane or Academy. Rocketlane migration is a separate decision; Academy continues to serve as ongoing education.
- The Wizard does not send any communication to property owners in V1.
- The Wizard does not support multi-role SMB accounts beyond the single Q4.1 + Q5.1 delegation in V1.

---

## 6. MVP Scope

### 6.1 In Scope

- 9-screen Wizard (Cover + 8 Sections) per FRs §4.1–§4.11.
- Airbnb view-only sync as the first interactive step (§4.3).
- Section 2–7 Question capture with all V4 dynamic branching, including explicit no-data branches (FR-7).
- Tiered Skip Intercept with Auto-Pilot Acceptance Modal (FR-37.1) and in-flight write draining (FR-37.2).
- Section 8 "What's Configured" summary + CSM Handoff Artifact (FR-32.1).
- Profile Configuration Writes gated by operator and (where applicable) accountant Consent Records (§4.9).
- Resume state at last-answered Question with validity check (FR-10).
- Live Airbnb re-poll on every Wizard entry with stickiness rules for already-answered Questions (FR-11, FR-11.1, FR-11.2).
- Accountant Secure Link + Stripped Section 5 View with accountant-scoped consent (FR-28.1).
- Full Delegation Lifecycle state machine (§4.10).
- Branching & Data Freshness Model (§4.11) with no-data branches mapped.
- Wizard Cohort stickiness for feature-flagged rollout (FR-10).
- Multi-account selection at Wizard entry (FR-4.1).
- Persistent header with live Call-1 countdown anchored to booking timezone (FR-1).
- Dashboard "Finish Setup" link for in-progress Wizards (FR-5).
- A/B framework for Tier 1 intercept copy (FR-38.1) with abandonment counter-metric.
- Partner Alias Table (FR-18.1) and partner-disambiguation (FR-18.2).
- CSM Handoff Artifact (FR-32.1) — Salesforce field spec, locked Phase 0.
- Profile Output Schema artifact (FR-44) — locked Phase 0.

### 6.2 Out of Scope for MVP

- Persistent dashboard "Call 1 Prep" widget — V2.
- CSM Review Mode — V2.
- Owner invite emails — V2.
- Notification preferences configuration — V2.
- Pre-population pipeline integration — V2.
- Mobile responsive support — V2.
- Mid-Market / SME flow with multi-role splits — V2+.
- Non-Airbnb primary channel support — V2+.
- Multilingual message templates and Wizard copy — V2+.
- Multi-Airbnb-account aggregation — V2+.
- Intra-Wizard consent revocation — V2.
- GuestyPay activation funnel — separate initiative.
- Rocketlane migration / replacement — separate decision.
- Blockers as first-class objects, readiness gates, silent-customer detection (Brief Addendum §7 V2 directions) — V2+.
- White-label / co-brand surfaces — V2+; V1 is Guesty-branded.
- Graduation handoff artifact (structured customer-facing summary of completed onboarding, separate from the CSM Handoff Artifact) — V2.
- Asymmetric UX / CSM diagnostic view (CSM can inspect a customer's Wizard state and completion without entering the Wizard session) — V2.
- Preset library expansion by vertical (property-type–specific question presets and defaults beyond V4) — V2+.

---

## 7. Success Metrics

*Targets are stated as **deltas vs. baseline** where the baseline is verified-fresh; stale baselines are flagged. Targets are also **tiered by rollout phase**: **Phase 2 floor** (10% cohort — hold-rollout gate, also the falsifiability threshold for Hypotheses 1 and 2 per §1.1), **Phase 4 ambition** (100% rollout, 12-week target), **Steady state** (sustained beyond 12 weeks). All baselines older than 30 days require refresh before locking (see §16 BLOCKER-6).*

### Primary

- **SM-1: Airbnb view-only sync completion rate.**
  - Definition: % of new SMB accounts that complete Airbnb OAuth before Call 1.
  - **Phase 2 floor:** ≥30% (Hypothesis 1 falsifiability threshold; below this, the AHA-moment hypothesis is not supported and Phase 3 is gated on diagnosis per §14).
  - **Phase 4 ambition:** 40–65% (range, not single point). Internal anchors (2026-05-25 data): ~73% of SMB accounts activate listings during onboarding (97% eventual; ~25% post-graduation). **Caveat on event data:** the ~88% connection-step rate identified in internal events appears to be from Lite Airbnb flows (`lite_airbnbflow`/`glite-airbnb`), not the Pro desktop revamp. Lite and Pro may not share the same OAuth/import path or tracking model. Do NOT use Lite data as a Pro benchmark without validation (§16, new SOFT item). The more important insight from the available funnel data: OAuth itself is not the collapse point — the post-connect listing selection/import step is. In the Lite proxy funnel, 17/19 accounts clicked connect (89.5%), but only 7/17 reached import_finished (41%). **SM-1 measures only OAuth completion. The real activation metric is Airbnb Account Readiness (see below).**
  - **Steady-state target:** >65% within 6 months of 100% rollout.
  - Validates FR-13, FR-14, FR-15.
  - *Note: the Brief's original >80% target is recast as steady-state / V2 ambition pending benchmark validation (adversarial:C-2).*
  - *CSM-side cross-check:* the same rate measured at Call 1 entry (% of Call 1 customers arriving Airbnb-synced) should match SM-1 within measurement error; use as a data-quality check, not a separate KPI.
  - **Airbnb Account Readiness Rate (companion metric, Phase 2+):** SM-1 measures only OAuth completion. The richer metric — aligned with the actual business problem — is: accounts that (1) completed OAuth AND (2) safely handled listing selection (import, link, or intentionally skipped) AND (3) created zero duplicate listings AND (4) have no unresolved pending/failed import blocker. Internal Lite funnel data shows 89% click connect but only ~41% reach import_finished — the collapse is post-connect, not during OAuth. V1 instrumentation should capture this full journey. Suggest Data team define and instrument "Airbnb Account Readiness Rate" as a Phase 2 companion to SM-1 (not a replacement — the Wizard's Section 1 is view-only, but the full readiness picture matters for CSM prep and downstream activation).

### Secondary

- **SM-2: Cover Screen → Q1.1 start rate.** % of users who reach the Cover Screen and click "Let's get started." Validates FR-1, FR-2. **Phase 2 floor: ≥50% (Hypothesis 2 falsifiability threshold);** below this signals a Rocketlane-style delivery problem, not a surface problem.
- **SM-3: Per-Section completion rate.** Tracks Sections 2–7 completion conditional on Section 1 completion. Validates FR-6 through FR-12. Flag any Section with >25% drop-off for UX review.
- **SM-4: Resume rate.** % of users who exit mid-Wizard and return at least once before Call 1. Definition: re-entry initiated by the user from outside the Wizard surface after >1 minute of inactivity; OAuth bounce excluded. Validates FR-9, FR-10, FR-11.
- **SM-5: Section 8 handoff vs. early-skip rate.** % of users reaching Section 8 vs. exiting at Tier 1/2/3. Validates the full flow.
- **SM-6: Mean configured items per completed flow.** Paired with SM-C7 (settings changes within 30 days) to detect over-configuration.
- **SM-7: Specialist-rated Call 1 quality score.** Post-Call-1 survey, 1–5. **Phase 4 ambition: baseline + ≥0.5** within 12 weeks. *Co-owned with CSM Leadership* (§12).
- **SM-8: % of Call 1 time spent on review vs. walkthrough.** CSM self-report (cross-checked against a sample of recorded calls). **Phase 4 ambition: shift to >50% review-and-strategy within 12 weeks.** *Co-owned with CSM Leadership; depends on revised CSM Call 1 playbook (a §13 dependency).*
- **SM-10: Average specialist sessions per SMB onboarding.** Delta-style: **reduce by ≥25% vs. fresh baseline** (`[ASSUMPTION: baseline refresh — see §16 BLOCKER-6]`).
- **SM-11: SMB onboarding duration (days from sign-up to graduation).** Delta-style: **reduce by ≥25% vs. fresh baseline.** *Caveat per Premise 4 (§1.1): the Wizard alone may not move this; post-Call-1 momentum is required.*
- **SM-12: SMB on-time graduation rate.** Baseline: **30.6%** (2,557 graduated accounts; 803 on-time; data pull 2026-05-25). Current median lateness among late accounts: 24 days. Target: directional improvement in Phase 4; +10pp floor by steady state.
- **SM-13: Silent/inactive/unknown churn cluster size.** Lagging directional signal (per Brief Addendum §1), not primary proof. Delta-style: directional reduction vs. fresh baseline.

### Counter-metrics (do not optimize)

- **SM-C1: Time-on-Wizard.** Don't optimize either direction. Counters SM-1, SM-3.
- **SM-C2: Sections completed per user.** Don't optimize. Counters SM-5, SM-6.
- **SM-C3: Sync rate without downstream activation.** Don't optimize in isolation. Counters SM-1.
- **SM-C4: Number of post-Wizard support tickets.** Should not increase vs. control. Guardrail.
- **SM-C5: 3-month post-onboarding MRR churn.** Must stay ≤3% (guardrail).
- **SM-C6: Tier 1 intercept-induced abandonment rate.** Should not exceed 30%. Counters SM-1. Reasoning (per adversarial:H-5): if the intercept modal *causes* abandonment, we've made the AHA moment harder.
- **SM-C7: Configurations changed in Settings within 30 days of Wizard completion.** Should remain low. Counters SM-6. Reasoning: high change rate suggests we configured wrong defaults, not that we configured a lot.
- **SM-C8: Duplicate listings created during or after Wizard Airbnb connection (Section 1).** Must stay near zero. Confirmed live risk: CSM-reported case of 46 duplicate listings created due to ambiguous import vs. link UX (Airbnb Integration Page Revamp demo, 2026-05-25). FR-14 updated to require explicit import/link decision UX. Counter to SM-1 and the Airbnb Account Readiness Rate companion metric.
- **SM-C9: Accounts stuck in pending import after Wizard Section 1.** Should not exceed 5%. Indicates OAuth succeeded but listing activation failed — a broken AHA moment. Counters SM-1.
- **SM-C10: Airbnb OAuth failure / failed-connection recovery rate.** Should not increase vs. control. Guardrail for Hypothesis 1. A rising failure-recovery rate signals OAuth anxiety or connection friction even when SM-1 appears stable (users may retry to eventual success). Counter to SM-1 and the Airbnb Account Readiness Rate companion metric. Ties to FR-17 failure handling.

### KPI Ownership

Activation metrics (SM-1, SM-3, SM-6), Call Quality metrics (SM-7, SM-8), and Business Outcome metrics (SM-10, SM-11, SM-12, SM-13) are **shared between Product and CSM**. Wizard-internal metrics (SM-2, SM-4, SM-5) are Product-owned. Counter-metrics are Product-owned.

---

## 8. Cross-Cutting NFRs

- **Performance:** First Question render under 2s P95 (desktop broadband). Subsequent Question transitions under 500ms P95.
- **State persistence:** Resume State is durable across browser sessions, devices, and up to 30 days. **30-day expiry confirmed 2026-05-25.** Wizard Cohort assignment is sticky alongside Resume State (FR-10).
- **Live Airbnb re-poll latency:** under 3s P95. Cost ceiling: re-poll rate-limited per FR-11 / §9.3. *Cost estimate from architecture required pre-Phase-1 (§16 BLOCKER-12).*
- **Accessibility:** WCAG 2.1 AA. **Confirmed as Guesty baseline 2026-05-25.**
- **Browser support:** Latest 2 versions of Chrome, Edge, Firefox, Safari desktop. Mobile UA → FR-3.1 landing page.
- **Internationalization-ready:** Wizard copy externalized into a localization layer; templates UTF-8 safe (FR-21). V1 ships English-only.
- **Observability:** Each Section transition, Question answer, Skip, Tier intercept, Profile Configuration Write, OAuth event, delegation transition, and `aha_moment_fired` event emits a structured event.
- **Error rate:** Wizard-internal error rate <0.5% of sessions. Excludes external system outages.
- **Security:** Accountant Secure Links use cryptographically secure random tokens, ≥128 bits of entropy, expire after 14 days. The Stripped Section 5 surface refuses requests whose authenticated identity matches the operator's identity (anti-self-delegation).

---

## 9. Constraints and Guardrails

### 9.1 Safety

- No write to the customer's Airbnb account, ever. OAuth scope is view-only.
- No outbound message to a guest, owner, or third party without explicit user opt-in.
- No payment processing rule activated without explicit user opt-in.
- Auto-Pilot Defaults are gated by FR-37.1's Acceptance Modal (silent writes on Tier 1 / 2 / 3 skip are not allowed; Tier 4 is an exception only because all higher-Tier Sections are configured).

### 9.2 Privacy

- The Accountant Secure Link exposes minimal operator data (industry, currency only — FR-29).
- Salesforce Account Data and Live Airbnb Data Hooks are server-side only.
- The Consent Record (Operator and Accountant) stores the verbatim wording shown to the user.
- Free-text inputs sanitized for CSM-facing surfaces and Salesforce writes (FR-32.1).
- Salesforce raw partner strings are not surfaced to the user verbatim (FR-18.1).
- Anti-self-delegation: the secure link refuses the operator's own session (§8 Security).

### 9.3 Cost

- Live Airbnb re-poll rate-limited to once per Wizard entry. Cost estimate from architecture required pre-Phase-1.
- Salesforce Account Data fetch is once per Wizard entry, cached for the session.

---

## 10. Aesthetic and Tone

- **Reference UX:** Typeform. Large type. Generous whitespace. Single focal point per screen. Animated transitions. Auto-advance on single-select (with accessibility-mode toggle per FR-6).
- **Tone:** Confident, calm, conversational. Embedded "why" in every Question. No corporate jargon.
- **Anti-references:** Multi-step wizards with stepper bars. Heavy modal-based onboarding. Setup-checklist UI. Anything that telegraphs "this will take a while."
- **Copy direction per Brief Addendum §6:**
  - *Use:* "Let's get your account ready for your first session." / "Your account is no longer blank."
  - *Avoid:* "Complete your setup." / "You must finish these steps."
  - *Review-ready framing (key phrases):* "Saved for your specialist to review." / "We'll cover this on your call." / "Your account is no longer blank — your specialist can see everything you've set up."
  - *Safety-first phrasing for Airbnb sync:* "View-only — nothing on your Airbnb is touched." / "We're just reading your data, not changing anything."
  - *Safety-first phrasing for Owner Prep:* "Stored only — your owners won't receive anything until you set that up." *(See also FR-33 consequence below.)*
  - *Safety-first phrasing for Automated Messaging:* "You can edit or turn these off any time in Settings."
- **Persistent header constraints (measurable per FR-3):** max height 64px; minimum-viewport gate per FR-3.1.
- **Bot UX surface:** Bot copy ("System (Bot):" framing in V4) is a stylized text bubble (typography-driven, not an avatar character). Defined once visually; used consistently across all bot-voiced screens.

---

## 11. Information Architecture

- **One primary Wizard surface** at a stable URL.
- **One Stripped Section 5 View** at a separate, token-gated URL (FR-28).
- **One "Finish Setup" entry point** in the post-Wizard dashboard nav (FR-5).
- **Wizard nav does not change the URL by Section in V1.** Bookmarks resolve to last-answered Question via Resume State. CSM sharing of Wizard URL is not supported.
- **Persistent header is structurally part of the Wizard layout.**
- **Bot UX surface** per §10.

---

## 12. Stakeholders and Approvals

| Role | Name | Approval needed for |
|---|---|---|
| Product (PM) | Yair Cohen | This PRD; Profile Output Schema artifact (Phase 0); CSM Handoff Artifact field spec (Phase 0); Partner Alias Table |
| Engineering Lead | TBD | NFRs; Profile Configuration Writes architecture; Live Airbnb cost estimate; branching engine implementation |
| Design / UX Lead | TBD | Final Wizard UX spec building on V4; Stripped Section 5 View; Auto-Pilot Acceptance Modal copy; A/B test variant copy |
| **CSM Leadership** | TBD | SM-7, SM-8 co-ownership; Revised Call 1 Playbook (§13 dependency); CSM Handoff Artifact sign-off; Phase rollout cadence + kill criteria |
| Legal / Compliance | TBD | Consent wording (FR-2); Accountant Consent banner (FR-28.1); Consent revocation behavior (FR-46); Accountant Secure Link scope (FR-29); industry exposure (FR-29) |
| Data / Analytics | TBD | Event-stream conventions (FR-48); SM measurement methods; baseline data refresh (BLOCKER-6); Hypothesis 3 role-collapse audit (BLOCKER-8); mobile-share data (BLOCKER-9); accountant-delegation rate (BLOCKER-10) |
| Security | TBD | Accountant Secure Link entropy + expiry; anti-self-delegation refusal logic |
| Localization Owner | TBD (or N/A V1) | Confirm English-only V1 or assign owner for +1 language |
| Support | TBD | "Help — what went wrong?" article (FR-17) |

`[ASSUMPTION: TBD names — PM to fill before Phase 0.]`

---

## 13. Integration and Dependencies

| Dependency | Status | Notes |
|---|---|---|
| Airbnb view-only OAuth integration | Built | FR-13. |
| **Airbnb Integration Page Revamp (Phase 1)** | **Live — full rollout 2026-05-25** | New view-only connection flow UX, reconnect vs. fresh-import distinction (FR-14), co-host listing indicators. Wizard Section 1 depends on this revamp being stable. Coordinate with revamp team (Yehan/EB&B integration) on shared OAuth flow. |
| Setup Call scheduling flow | Built | Provides `{{CSM_Name}}` etc. to FR-1. |
| Salesforce CRM lookup | **Built — confirmed 2026-05-25** | FR-4. |
| Live Airbnb Data Hooks | **Spec needed; cost estimate Phase 0** | FR-15. |
| Guesty message template / automation backend | Built | FR-21, FR-22. Hot-swap semantics (FR-23) need confirmation. |
| Consent Record persistence (Operator + Accountant) | **New** | FR-2, FR-28.1, FR-43. |
| Email send for Accountant Secure Link | Built | FR-27. New email template required. |
| Secure-token system for Accountant Link | **New** | FR-27. §8 Security spec. |
| Profile Configuration Write infrastructure | **New, Phase 0 precondition** | §4.9. Locked schema (FR-44) gates build. |
| Wizard dashboard "Finish Setup" link surface | **New** | FR-5. Dashboard team. |
| Wizard event-stream consumer (analytics) | **`[ASSUMPTION: standard Guesty conventions]`** | FR-48. |
| **CSM Handoff Artifact (Salesforce field spec)** | **New, Phase 0 deliverable** | FR-32.1. CSM Leadership sign-off. |
| **Partner Alias Table** | **New, Phase 0 deliverable** | FR-18.1. PM + Data. |
| **Revised CSM Call 1 Playbook** | **New** | SM-7 / SM-8 depend on this. CSM Leadership-owned. |
| **A/B test framework integration** | **New (or reuses existing Guesty A/B infra)** | FR-38.1. |
| Multi-Guesty-account routing surface | **New** | FR-4.1. |

---

## 14. Rollout and Change Management

### Phase 0 — Pre-launch preconditions (must complete BEFORE Phase 1)

Phase 1 cannot begin until ALL of:

- Profile Output Schema artifact (FR-44) — locked, PM + engineering sign-off
- CSM Handoff Artifact field spec (FR-32.1) — locked, CSM Leadership sign-off
- Partner Alias Table (FR-18.1) — locked, PM + Data sign-off
- Live Airbnb Data Hooks technical spec (FR-15) + cost estimate — locked, engineering sign-off
- Branching engine architecture (FR-7) — sketched and reviewed
- Consent wording (FR-2) and Consent revocation behavior (FR-46) and Accountant Consent banner (FR-28.1) — legal sign-off
- KPI baseline refresh (BLOCKER-6) — fresh data within 30 days
- Hypothesis 2 diagnosis (Rocketlane failure mode — BLOCKER-7) — completed
- Premise 3 audit (Role-collapse data — BLOCKER-8) — completed
- Mobile-share data (BLOCKER-9) — completed
- Accountant-delegation rate data (BLOCKER-10) — completed
- OAuth-in-onboarding benchmark (BLOCKER-13) — completed
- "Help — what went wrong?" support article (FR-17) — authored
- Revised CSM Call 1 Playbook (§13) — drafted

### Phase 1 (Weeks 1–2) — Internal dogfood

- Guesty employees simulate new-account flow with seeded test Salesforce records (per §16 SOFT-23 dogfood seeding).
- Sanity-check all FRs.
- **Kill criteria:** Any P0 incident, or any FR observed to silently fail.

### Phase 2 (Weeks 3–4) — 10% feature-flagged rollout

- **Allocation:** sticky hash on `customer_id`, 10% bucket.
- **Wizard Cohort stickiness:** once assigned, sticky through completion or expiry (FR-10).
- **Hold-rollout criteria (must all pass before Phase 3):**
  - SM-1 ≥ 30% (Hypothesis 1 floor — see §1.1)
  - SM-2 ≥ 50% (Hypothesis 2 floor)
  - SM-C4 (support ticket delta) ≤ +5% vs. control
  - SM-C5 (3-month MRR churn) within 0.5% of baseline (early signal)
  - SM-C6 (intercept-induced abandonment) ≤ 30%
  - Zero P0 incidents in 14 days
- **Kill criteria:** SM-1 < 20%, P0 incident not resolved within 24hr, legal/compliance issue.
- **Diagnosis gate:** if SM-1 falls in [20%, 30%), Phase 3 is gated on root-cause diagnosis.

### Phase 3 (Weeks 5–8) — 50% rollout

- **Hold-rollout criteria:**
  - SM-1 ≥ Phase 2 floor sustained
  - SM-7 (Call 1 quality) ≥ baseline (no degradation)
  - SM-C4 ≤ +5%
- **Kill criteria:** SM-1 regression >10pp from Phase 2, P0 incident, SM-C5 breach

### Phase 4 (Weeks 9+) — 100% rollout

- All Phase 3 criteria sustained.
- Continued tracking against §7 metrics.

### V1 Launch — Definition of Done

V1 is considered launched when ALL of:

1. 100% rollout sustained for 14 days
2. SM-1 ≥ 40% (Phase 4 ambition floor)
3. SM-7 ≥ baseline + 0.5
4. SM-C4 ≤ +10% vs. pre-launch baseline
5. SM-C5 ≤ 3% (guardrail)
6. Profile Output Schema, CSM Handoff Artifact, Partner Alias Table, and revised Call 1 Playbook all in production use

### Other rollout notes

- Existing SMB customers mid-onboarding at launch are NOT migrated; they complete via existing Rocketlane path. **Confirmed 2026-05-25.**
- CSM training: 30-min training session + FAQ before Phase 2; revised Call 1 playbook in hand.
- Rocketlane coexists in V1; retirement is a separate decision.

---

## 15. Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Customers OAuth-bounce at Q1.1 (Hypothesis 1 fails) | Medium | High | Tier 1 intercept + Auto-Pilot Acceptance Modal; SM-1 Phase 2 floor as kill criterion; A/B testing of Tier 1 copy (FR-38.1); post-Phase-2 diagnosis gate. |
| Hypothesis 2 weaker than expected despite addressing known failure modes | Low–Medium | High | Qualitative diagnosis complete (login, UI, format were root causes — not content). Quantitative data unavailable. SM-2 Phase 2 floor (≥50%) is the live check. If SM-2 <50%, Wizard needs a notification/discovery strategy. |
| Premise 3 fails (role-collapse rate <75%) | Low–Medium | Medium | Phase 0 audit (BLOCKER-8). If <75%, soften defaults or restructure for delegated workflows. |
| Profile Output Schema slips past Phase 0 | Medium | Critical | Phase 0 hard gate (no Phase 1 without lock). Schema work begins immediately post-PRD; PM owns. |
| Live Airbnb re-poll cost overrun | Low | Medium | Phase 0 cost estimate (BLOCKER-12); rate-limit per FR-11; fallback to stale cache. |
| Accountant Secure Link is forwarded / shared inappropriately | Low | Medium | Anti-self-delegation logic (§8 Security); 14-day expiry; scoped surface; accountant-scoped Consent. |
| Customers consent on Cover Screen but feel deceived about scope of writes | Medium | High | Verbatim wording stored; "See what we'll configure" disclosure (FR-2); per-template opt-in for messaging (FR-23); Section 8 summary reviewable; Auto-Pilot Acceptance Modal (FR-37.1). |
| CSM Leadership behavior change (SM-7 / SM-8) does not materialize | Medium | High | Revised Call 1 Playbook as §13 dependency; co-ownership in §12; CSM-Leadership sign-off Phase 0; cross-check via recorded calls (SM-8). |
| Accountant Link underused | Low | Medium | **RESOLVED**: 27.1% of accounts have a separate finance/billing contact (2026-05-25 data pull) — delegation path validated. Risk reduced from Medium to Low likelihood. |
| Stale-baseline-driven targets miscalibrated | High | Medium | Phase 0 baseline refresh (BLOCKER-6); targets restated as deltas (§7); Phase 2 hold-criteria are the operational gate. |
| Mobile-bound customers can't engage | Medium | Low | Platform constraint: Guesty does not support mobile web platform-wide; Wizard inherits this constraint. FR-3.1 landing page handles sub-1024px gracefully. V2 mobile scope deferred with the rest of the platform, not Wizard-specific. |
| Heroic SM-1 target sets sponsor expectation that V1 misses | Medium | Medium | SM-1 restated as Phase 2 floor (30%), Phase 4 ambition (40–65%), steady-state (>65%); sponsor briefed on tiering. |
| Wizard improves activation but masks deeper retention problem | Low | High | SM-C5 guardrail catches; SM-C7 catches over-configuration. |
| Rocketlane and Wizard create conflicting customer experiences | Medium | Medium | CSM training; Phase 0 Call 1 Playbook revision; future Rocketlane retirement decision (out of scope). |
| Tier 1 intercept *causes* abandonment | Medium | Medium | A/B framework (FR-38.1); SM-C6 monitoring; alternate copy variants ready. |

---

## 16. Open Questions

Organized by **phase-gate** status.

### [BLOCKER] — must resolve BEFORE Phase 0 closes / Phase 1 begins

1. **[BLOCKER-1]** Consent wording final lock with legal (FR-2; Brief Open Q10).
2. **[BLOCKER-2]** Stripped Section 5 accountant consent banner wording (FR-28.1) — legal review.
3. **[BLOCKER-4 — TBD]** Profile Output Schema artifact delivery (FR-44) — PM-owned, Phase 0. Deferred; revisit before Phase 0 closes.
4. **[BLOCKER-5 — TBD]** CSM Handoff Artifact (Salesforce field spec) (FR-32.1) — Phase 0; CSM Leadership sign-off required. Owner and field spec both TBD; revisit before Phase 0 closes.
5. **[BLOCKER-11 — TBD]** Partner Alias Table — initial canonical mapping locked (FR-18.1). Deferred; revisit before Phase 0 closes.
6. **[BLOCKER-12 — TBD]** Live Airbnb Data Hooks cost estimate from architecture (FR-15, §9.3). Engineering lead TBD; must resolve before Phase 1.
7. **[BLOCKER-14 — TBD]** Rollout cadence + kill criteria — CSM Leadership sign-off on §14 phasing. Owner TBD; must resolve before Phase 1.
8. **[BLOCKER-15 — TBD]** Stakeholder approval matrix names — populate §12 TBDs. Deferred.
9. **[BLOCKER-6 — REMAINING SUB-ITEMS]** KPI baselines: SM-10 (average specialist sessions per SMB onboarding) and SM-11 (onboarding duration in days from sign-up to graduation) baseline values not yet pulled. Required to set delta targets for both metrics in §7. Owner: Data team. Must resolve before Phase 0 closes. *(SM-12 baseline resolved: 30.6%; see [RESOLVED] below.)*

### [SOFT] — should resolve BEFORE Phase 2 (10% rollout)

16. OAuth failure detailed UX + "Help — what went wrong?" support article (FR-17; Brief Open Q6).
17. Section-5-specific Tier 3 intercept copy (FR-35) — UX.
18. V4 version-lock with PRD (rubric:medium-1) — engineering kickoff.
19. Mobile-detection landing page copy (FR-3.1).
20. Wizard event-stream PII handling confirmation (FR-48) — Data team.
21. Pro-specific Airbnb OAuth + import funnel data — validate whether Lite event data (`lite_airbnbflow`) applies to the Pro desktop revamp; pull Pro-specific events for: connection_popup_view → connect → listings_loaded → import/link_finished → all_set. Required to tighten SM-1 targets and instrument Airbnb Account Readiness Rate. Owner: Data / EB&B integration PM (Yehan).

### [INVESTIGATE] — can defer to Phase 3 (50%) or post-launch

22. Bot UX surface visual treatment refinement (§10).
23. SM-2 vs. SM-1 KPI hierarchy convention (`[ASSUMPTION: see §17]`).
24. Calendar add ICS for "Other" calendar users (FR-40).
25. Co-brand / white-label surfaces (out of V1).
26. UJ-5 partner-override "use Guesty instead" path (V2 candidate).
27. Wizard cohort kill-and-rollback mechanics if Phase 2 fails (rollback path TBD).
28. Multi-event Setup Calls (out of V1).

### [RESOLVED] — closed during PRD sessions

**From BLOCKER tier:**

- ~~**[BLOCKER-3]**~~ **[RESOLVED 2026-05-25]** Consent revocation behavior (FR-46). Decision: no-rollback adopted; EU exposure acknowledged. Writes made remain in place on revocation; future writes blocked until restored.
- ~~**[BLOCKER-6]**~~ **[PARTIALLY RESOLVED 2026-05-25]** KPI baseline data refresh. Known baselines from data pull: SMB on-time graduation rate **30.6%** (was 18% in prior brief — updated in SM-12); median SMB onboarding duration **31 days** (vs. 20-day SLA); active onboarding backlog overdue rate **69.9%**; post-graduation churn within 60 days **59.5%** (of churned cohort). Remaining gaps: SM-10 specialist sessions per onboarding baseline not yet pulled; SM-11 (days to first value) baseline not yet pulled. Those two sub-items remain open; overall BLOCKER partially closed.
- ~~**[BLOCKER-7]**~~ **[PARTIALLY RESOLVED 2026-05-25]** Rocketlane failure-mode diagnosis. Qualitative diagnosis complete: separate login, complex UI, and checklist format were the failure drivers — not the questions (email-based questions had reasonable completion). Quantitative data unavailable (no Rocketlane reports). Hypothesis 2 causal argument is substantively strengthened. Residual uncertainty tracked via SM-2 Phase 2 floor (≥50%).
- ~~**[BLOCKER-8]**~~ **[PARTIALLY RESOLVED 2026-05-25]** Role-collapse data (Premise 3, §1.1). Finding: single-user accounts cluster at 1–3 listings ($194 MRR median), below Wizard target. 79.2% of role-covered accounts have 2+ users at steady state, but SMB role coverage is only 30.4% and onboarding-moment logins are not directly measurable from this dataset. Role-collapse premise reframed as onboarding-moment claim; decision rule updated to Q4.1 live rate ≤50%. See §1.1 Premise 3 updated text.
- ~~**[BLOCKER-9]**~~ **[RESOLVED 2026-05-25]** Mobile-share data — desktop-only V1 confirmed. Guesty does not support mobile web platform-wide; desktop-only is a platform constraint, not a strategic tradeoff. No mobile-share data needed. Risk row updated in §15.
- ~~**[BLOCKER-10]**~~ **[RESOLVED 2026-05-25]** Accountant-delegation rate. Finding: 27.1% of accounts have a separate recorded billing/finance contact — well above the 5% kill threshold. Stripped Section 5 delegation path is validated. Risk row updated in §15.
- ~~**[BLOCKER-13]**~~ **[PARTIALLY RESOLVED 2026-05-25]** OAuth-in-onboarding benchmark. Available anchor: ~73% SMB listing activation during onboarding. Important caveat: the ~88% connection-step rate identified earlier is from Lite Airbnb flows (`lite_airbnbflow`), NOT the Pro desktop revamp. Lite and Pro may not share the same OAuth/import path or tracking model — do not use as Pro benchmark without validation (see new SOFT-21). More important insight: OAuth itself is not the collapse point. In the Lite proxy funnel, 89.5% clicked connect but only 41.2% reached import_finished — the post-connect listing selection/import step is where accounts stall. SM-1 targets (Phase 2 floor 30%, Phase 4 range 40–65%) held as directional. New companion metric defined (Airbnb Account Readiness Rate, §7 SM-1 note).

**From SOFT tier:**

- ~~Localization scope~~ **[RESOLVED 2026-05-25]** English-only V1 confirmed.
- ~~Stripped Section 5 industry exposure~~ **[RESOLVED 2026-05-25]** Industry + currency exposure to accountant confirmed acceptable.
- ~~Existing-customer migration~~ **[RESOLVED 2026-05-25]** No retroactive migration confirmed; mid-onboarding customers stay on Rocketlane.
- ~~WCAG 2.1 AA confirmation~~ **[RESOLVED 2026-05-25]** Confirmed as Guesty baseline.
- ~~Resume State expiry~~ **[RESOLVED 2026-05-25]** 30 days confirmed.
- ~~Accountant Secure Link expiry~~ **[RESOLVED 2026-05-25]** 14 days confirmed.
- ~~Shared toast component spec~~ **[RESOLVED 2026-05-25]** Shared toast component confirmed — exists in Guesty design system.
- ~~Hot-swap semantics for message templates~~ **[RESOLVED 2026-05-25]** Messaging backend hot-swap confirmed supported.
- ~~Q3.2 region/timezone template variants~~ **[RESOLVED 2026-05-25]** V1 ships one universal English template; regional variants deferred to V2.
- ~~Salesforce CRM lookup~~ **[RESOLVED 2026-05-25]** Confirmed built.
- ~~Reasonableness range thresholds~~ **[RESOLVED 2026-05-25]** FR-31.1 confirmed in scope; specific thresholds per industry to be authored by Data team before Phase 0 closes (owner TBD).

---

## 17. Assumptions Index

| Severity | Source | Description |
|---|---|---|
| BLOCKER | FR-2 / §16 BLOCKER-1 | Final consent wording pending legal. |
| BLOCKER | FR-28.1 / §16 BLOCKER-2 | Accountant consent banner wording pending legal. |
| ~~BLOCKER~~ RESOLVED | FR-46 / §16 BLOCKER-3 | No-rollback adopted 2026-05-25; EU exposure acknowledged. |
| BLOCKER | FR-44 / §16 BLOCKER-4 | Profile Output Schema is Phase 0 precondition. |
| BLOCKER | FR-32.1 / §16 BLOCKER-5 | CSM Handoff Artifact Salesforce field spec — Phase 0. |
| BLOCKER | SM-10–13 / §16 BLOCKER-6 | KPI baselines from May 3 brief, 22 days stale. |
| ~~BLOCKER~~ PARTIAL | §1.1 Hyp 2 / §16 BLOCKER-7 | Qualitative diagnosis done (login barrier + UI + format). No quantitative data available. Residual: SM-2 Phase 2 floor. |
| ~~BLOCKER~~ PARTIAL | §1.1 Prem 3 / §16 BLOCKER-8 | Role-collapse reframed as onboarding-moment claim; decision rule updated to Q4.1 live rate. Steady-state data inconclusive for onboarding window. |
| ~~BLOCKER~~ RESOLVED | §6.2 / §16 BLOCKER-9 | Desktop-only is a platform constraint — Guesty does not support mobile web. No data needed. |
| ~~BLOCKER~~ RESOLVED | FR-27/28 / §16 BLOCKER-10 | 27.1% separate finance contact confirms delegation path (2026-05-25). |
| BLOCKER | FR-18.1 / §16 BLOCKER-11 | Partner Alias Table — initial mapping locked. |
| BLOCKER | FR-15 / §16 BLOCKER-12 | Live Airbnb hooks cost estimate. |
| BLOCKER | SM-1 / §16 BLOCKER-13 | OAuth-in-onboarding benchmark to anchor SM-1. |
| BLOCKER | §14 / §16 BLOCKER-14 | Rollout phasing + kill criteria CSM Leadership sign-off. |
| BLOCKER | §12 / §16 BLOCKER-15 | Stakeholder names. |
| HIGH | §2.4 | UJs inferred from V4; user confirms. |
| ~~HIGH~~ CONFIRMED | FR-23 | Message template hot-swap semantics confirmed 2026-05-25. |
| HIGH | FR-32.1 (events) | Free-text sanitization on CSM-facing surfaces. |
| MEDIUM | FR-3.1 | Mobile-detection landing page copy. |
| MEDIUM | FR-5 | "Finish Setup" link disappearance logic. |
| MEDIUM | FR-12 | Refresh toast wording (UX to finalize). |
| MEDIUM | FR-17 | OAuth-failure support article exists at launch. |
| MEDIUM | FR-21 | V4 copy verbatim cross-references (version-lock). |
| ~~MEDIUM~~ CONFIRMED | FR-27 | Accountant Secure Link 14-day expiry confirmed 2026-05-25. |
| MEDIUM | FR-28 | Stripped Section 5 context header copy (UX to finalize). |
| ~~MEDIUM~~ CONFIRMED | FR-29 | Industry + currency exposure to accountant confirmed acceptable 2026-05-25. |
| MEDIUM | FR-31.1 | Reasonableness range thresholds. |
| MEDIUM | FR-42 | V1 Call Prep view is minimal, not placeholder. |
| MEDIUM | FR-48 | Existing Guesty event-stream PII conventions cover Wizard events. |
| ~~MEDIUM~~ CONFIRMED | §8 NFRs | Resume State 30-day expiry confirmed 2026-05-25. |
| ~~MEDIUM~~ CONFIRMED | §8 NFRs | WCAG 2.1 AA baseline confirmed 2026-05-25. |
| MEDIUM | §11 | No per-Section URL routing in V1. |
| ~~MEDIUM~~ CONFIRMED | §13 | Salesforce CRM lookup confirmed built 2026-05-25. |
| ~~MEDIUM~~ CONFIRMED | §14 | Existing-customer non-migration confirmed 2026-05-25. |
| ~~LOW~~ CONFIRMED | §5 | English-only V1 confirmed 2026-05-25. |
| LOW | UJ-1 | "8 minutes" median completion time. |
| LOW | various | Emoji rendering, font stack details. |

---

## 18. Change Log

- **draft v1 (2026-05-25):** Initial PRD draft from Fast Path.
- **draft v2 (2026-05-25):** Post-Reviewer-Gate autofix. Major changes: added §1.1 Hypotheses & Falsifiability; added §4.10 Delegation Lifecycle state machine; added §4.11 Branching & Data Freshness Model; restructured §7 SMs into tiered targets (Phase 2 floor / Phase 4 ambition / Steady state) with delta-style baselines; added FR-3.1 (viewport gate), FR-4.1 (multi-account), FR-11.1/.2 (stickiness), FR-18.1/.2 (partner alias + disambiguation), FR-25.1/.2 (anti-self-delegation, Q4.1 cascades), FR-28.1 (accountant consent), FR-31.1 (reasonableness), FR-32.1 (CSM Handoff Artifact), FR-37.1/.2 (Auto-Pilot Acceptance Modal, in-flight drain), FR-38.1 (A/B framework), FR-50 series (Delegation Lifecycle transitions); restructured §14 with Phase 0 preconditions, per-phase kill/hold criteria, V1 Launch DoD; restructured §16 by phase-gate; added SM-C6, SM-C7; added Risk and Stakeholder rows for CSM Leadership co-ownership of SM-7/SM-8. Strategic findings from adversarial review elevated to [BLOCKER] Open Questions (Hypotheses 1/2, Premise 3, KPI baselines, mobile, accountant ROI, benchmarks). See `review-rubric.md`, `review-edge-cases.md`, `review-adversarial.md` and `.decision-log.md`.
- **final (2026-05-25):** Session 3 finalization pass. Open Questions walk completed (all 15 BLOCKERs, all 16 SOFTs triaged). Key substantive changes: SM-12 baseline updated to 30.6% (was 18%); SM-1 Airbnb Account Readiness companion metric defined; Lite vs. Pro Airbnb event data caveat added and SM-1 Phase 4 range narrowed accordingly; SM-C8 (duplicate listings), SM-C9 (pending import), SM-C10 (OAuth failure recovery) counter-metrics added; FR-14 updated to require reconnect vs. fresh-import distinction UX; §13 Airbnb Integration Page Revamp live dependency added; §1.1 Hypothesis 2 Rocketlane failure-mode diagnosis added; §1.1 Premise 3 reframed as onboarding-moment claim with updated decision rule (Q4.1 ≤50%). Structural fixes: §5/§6.2 duplicates removed (7 items); §16 resolved items archived; S-6 SM-9 folded into SM-1 definition (CSM-side cross-check note); GAP-13 three V2 deferrals added to §6.2; GAP-10 SM-10/SM-11 baseline sub-items re-surfaced as BLOCKER-6 remaining in active section; GAP-11 review-ready copy phrases added to §10 and FR-33 Owner Prep safety copy added; GAP-2/3 build-layer/review-layer framing added to §1 Vision; S-1 §2.1 Role Collapse shortened to pointer; S-5 §0 canonical authority signal added for §4.10/§4.11. See `.decision-log.md` for full audit trail.

---

*Status: final — 2026-05-25. Ready for downstream workflows: UX design, architecture, epics & stories.*
