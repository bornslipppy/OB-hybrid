---
title: "Guesty Pro Onboarding Wizard — Pre-Call-1 Questionnaire"
status: draft
created: 2026-05-25
updated: 2026-05-25
author: Yair Cohen
supersedes: docs/planning-artifacts/product-brief-Guesty-Pro-Onboarding-Wizard-2026-05-03.md
audience: PM agent (drives PRD)
---

# Product Brief: Guesty Pro Onboarding Wizard (Pre-Call-1 Questionnaire)

## 1. Executive Summary

Guesty Pro SMB customers today sign up, schedule a Setup Call (Call 1), then wait — landing in an empty enterprise platform with no clear path forward. By the time they reach Call 1, they are cold, overwhelmed, or absent. The existing pre-call surface (Rocketlane, Academy) sees ~0% engagement.

**V1 builds an online questionnaire** that runs between authentication+call-booking and Call 1. It guides new SMB accounts through a focused, Typeform-style flow that:

1. Connects Airbnb in view-only mode (the AHA moment — real listings, calendar, inbox)
2. Captures operational defaults (cleaning workflow, guest access method)
3. Pre-configures high-impact automated guest messaging (check-in instructions, review requests)
4. Locks in payment policy and mandatory fees
5. Hands the user off to the dashboard with state, momentum, and a Call 1 agenda

The goal is **not** full self-serve onboarding. The goal is to make Call 1 dramatically better — less walkthrough, more strategy — and to ensure SMB customers arrive at Call 1 with real account state for the specialist to review.

> **V1 Thesis:** Convert the dead zone between call booking and Call 1 into a guided, single-question-at-a-time flow that connects Airbnb, captures operational defaults, and lands the customer on a populated dashboard.

---

## 2. Problem Statement

SMB Guesty Pro onboarding has a structural failure between sign-up and Call 1:

1. **Cold start** — dashboard, calendar, and inbox are empty on first entry
2. **No clear path** — customers don't know what to do, what to do first, or what can wait
3. **Enterprise overload** — SMB users land in a UI designed for much larger teams
4. **Momentum decay** — without a guided experience, customers drift back to their old PMS or arrive at Call 1 unprepared
5. **Existing pre-call surfaces ignored** — Rocketlane sees ~0% task completion before Call 1

The wizard targets this specific gap. It does not solve the full onboarding journey. Detailed operational context is in `addendum.md §1`.

---

## 3. Target Segment

**Guesty Pro SMB** — owner-operators with **5–20 listings**, primary channel **Airbnb**.

Persona reference: 2A (Bootstrapped Entrepreneur) and 2B (Boutique/Family Operator) from the Guesty persona library.

### Critical Design Constraint: Role-Collapse

In SMB Guesty Pro, the executive sponsor, customer admin, and process champion **collapse into one person** — the owner-operator. The wizard cannot assume the customer will self-organize. It must supply sequencing, defaults, safety framing, and a readiness definition that a project manager would normally provide.

This is why a generic checklist is insufficient, and why this V1 architecture **does not scale unmodified** to mid-market (role separation returns there).

---

## 4. Solution Approach

### Design Principles

1. **One question per screen** (Typeform pattern) — large type, single CTA, auto-advance on selection
2. **Conversational copy with embedded "why"** — every question explains the benefit, not just the ask
3. **Use what we already know** — pre-fetch Salesforce and live Airbnb data; never ask the same thing twice
4. **Skip-friendly with tiered resistance** — every question optional; intercepts get lighter as user invests more
5. **Configure with consent** — single cover-screen consent enables system-level configuration on user's behalf
6. **Safe defaults always** — never auto-enable messaging, payments, or third-party contact without explicit opt-in

### Flow Structure (9 screens / 8 sections)

| # | Section | Purpose |
|---|---------|---------|
| 0 | Cover | Welcome, call countdown, consent gate |
| 1 | Connect Airbnb | The AHA moment — OAuth as first interactive step |
| 2 | Operations | Cleaning workflow + guest access method |
| 3 | Communications | Unified Inbox awareness + automated check-in & review messages |
| 4 | Team & Governance | Confirm decision owner (SMB-simplified) |
| 5 | Financials | Payment timing + mandatory fees + accountant delegation path |
| 6 | Call 1 Focus | Priority topic for the CSM call |
| 7 | Quick Wins | Owner upload, minimum stay (post-suggested path) |
| 8 | Review & Handoff | "What's configured" summary + dashboard handoff |

### Reference Specification

The detailed questionnaire spec — including dynamic branching logic, copy, message templates, tiered skip intercepts, "What's Configured" variable definitions, and Auto-Pilot Defaults — lives in [onboarding-questionnaire-v4.md](../../onboarding-questionnaire-v4.md). The PRD should treat that document as the source of truth for flow detail.

---

## 5. V1 Scope

### In Scope

- 9-screen / 8-section questionnaire as described
- Tiered skip intercept system (4 tiers based on user investment level)
- Persistent header with live call countdown
- Non-linear navigation (jump between sections; status icons: done / current / unlocked / locked)
- Single-consent model on cover screen (lighter wording — pending legal review)
- Auto-pilot defaults applied on skip (see V4 spec, Appendix B)
- Dynamic branching based on Salesforce account data and live Airbnb data
- Section 8 "What's Configured" summary screen
- Resume state — user can leave and return anytime before Call 1

### Out of Scope (V1)

- **Profile output schema** — deferred; to be defined as a separate artifact before engineering implementation
- **Persistent dashboard "Call 1 Prep" widget** — deferred to V2
- **Non-Airbnb primary channel** — V1 assumes Airbnb-primary
- **SME / Mid-Market role splits** — separate flow needed; out of V1
- **Multilingual templates** — V1 English only [ASSUMPTION: confirm with stakeholder]
- **Owner invite emails** — V1 captures owners (CSV), no send
- **Notification preferences configuration** — V2
- **Pre-population pipeline integration** — forward-compatible but not built in V1
- **Rocketlane migration / replacement** — separate decision
- **GuestyPay activation funnel** — separate initiative

### Out of Scope (handled by adjacent systems)

- Airbnb OAuth integration itself — already built
- Setup-call scheduling — happens before the questionnaire starts
- Authentication — happens before the questionnaire starts

---

## 6. Success Measures

### Primary Activation Metric

**>80% of new SMB accounts complete Airbnb view-only sync before Call 1.**

This is the AHA moment and the clearest evidence the wizard solved the cold-start problem.

### Supporting Product Metrics (track from day 1, no hard targets at launch)

- Cover screen → Q1.1 (Airbnb sync) start rate
- Airbnb sync completion vs. failure rate
- Per-section completion rate (flag any section with >25% drop-off)
- Resume rate (users returning after first exit, before Call 1)
- Section 8 handoff vs. early-skip rate
- Mean number of configured items per completed flow

### Call Quality Metrics (post-launch)

- Specialist-rated Call 1 quality score (1–5)
- % of Call 1 time spent on review vs. walkthrough
- % of Call 1 customers arriving Airbnb-synced
- Number of unresolved blockers discovered during Call 1

### Business Outcome (lagging, 8–12 weeks post-launch)

- Avg specialist sessions per SMB onboarding — current ~7–8 → target ≤5 [ASSUMPTION: baseline inherited from May 3 brief; verify]
- SMB onboarding duration — current 30–100+ days → target ≤20 days [ASSUMPTION: same]
- SMB on-time graduation rate — current 18% → directional improvement
- Silent/inactive/unknown churn cluster — current ~49% → directional reduction (treated as lagging signal, not primary proof)

### Guardrails

- No degradation in 3-month post-OB MRR churn (must stay ≤3%)
- No increase in support tickets caused by misconfiguration
- No increase in Airbnb connection anxiety or failed-connection recovery issues
- No increase in specialist-reported Call 1 confusion

### KPI Ownership

Activation, Call Quality, and Business Outcome metrics are **shared between Product and CSM** — neither team owns them alone. Supporting Product Metrics and Guardrails are Product's continuous improvement signals.

---

## 7. Dependencies

| Dependency | Status | Notes |
|------------|--------|-------|
| Airbnb OAuth (view-only) | Built | Out of scope for V1 build |
| Setup-call scheduling flow | Built | Provides `{{CSM_Name}}`, `{{call_date}}`, `{{call_time}}`, `{{timezone}}` |
| Salesforce CRM lookup | [ASSUMPTION: built] | Required fields: `active_listing_count`, `connected_channels`, `Partners`, `industry`, `operative_account_segmentation`, `Expected_MRR__c`, `Owners`, `customer_churn_reason` |
| Live Airbnb data hooks | [ASSUMPTION: requires technical spec] | Required signals: `Next_Check_In_Date`, `Unread_Message_Count`, `Average_Length_of_Stay`, `listing_count`, `reservation_count` |
| Message template / automation backend | Exists | Needs API for templated writes (check-in messages, review requests) |
| Consent record persistence | New requirement | Pending legal review of wording and storage requirements |

---

## 8. Open Questions (for PRD)

1. **Profile output schema.** What does each questionnaire answer write to the live account? PM should produce a field-by-field mapping before engineering implementation begins.
2. **Resume granularity.** Resume from last-completed *section* or last-answered *question*? UX implication for state persistence.
3. **Data freshness on re-entry.** If the user leaves and returns after Airbnb state changes (new bookings, more unread messages), do dynamic checks re-evaluate, or are they snapshotted on first sync?
4. **Accountant delegation surface.** What does the accountant see on the secure link in Q5.1? Same questionnaire scoped to Section 5? Or a different surface entirely?
5. **Consent revocation.** If the user revokes consent later, do auto-configured items roll back or remain?
6. **OAuth failure handling.** What happens if Airbnb OAuth fails mid-flow? Tier 1 intercept doesn't cover this case — need a specific "OAuth failed, retry or skip" state.
7. **Mobile support.** Is V1 desktop-only, or must it work on mobile? Typeform UX usually fine on mobile, but skip intercepts and progress nav need responsive review.
8. **Localization scope.** V1 English-only, or one additional language?
9. **Baseline data refresh.** Several baselines inherited from the May 3 brief are 22 days old — verify against current data before PRD locks targets.
10. **Consent wording.** Tentative copy is `"I authorize Guesty to configure my account based on my responses. I can review and change everything later in Settings."` — needs final legal sign-off.

---

## 9. Reference Artifacts

- **Detailed questionnaire spec:** [onboarding-questionnaire-v4.md](../../onboarding-questionnaire-v4.md) — source of truth for flow, copy, branching, intercept tiers, variable definitions, auto-pilot defaults
- **Superseded brief:** [product-brief-Guesty-Pro-Onboarding-Wizard-2026-05-03.md](../../product-brief-Guesty-Pro-Onboarding-Wizard-2026-05-03.md) — broader initiative context including operational metrics
- **Persona context:** guesty-user-personas.md — Personas 2A and 2B are primary
- **Addendum:** [`addendum.md`](addendum.md) — operational signal detail, deferred-V2 list, copy direction reference, role-collapse rationale

---

*Status: draft. Awaiting review.*
