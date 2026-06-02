---
title: "PRD: Guesty Pro Onboarding Wizard — Prototype"
---

# PRD: Guesty Pro Onboarding Wizard — Prototype

**Status:** Draft  
**Author:** Yair Cohen  
**Date:** 2026-05-03  
**Last Updated:** 2026-05-04  
**Version:** 1.6 (requirements update — clarifies that nothing in the flow is mandatory, including scheduling a call; users can begin and enter Guesty without completing any steps; all presented paths are strong suggestions; automated reminder emails serve as the re-engagement mechanism for users who do not complete steps or book a call)  
**Source documents:**
- Product Brief: Guesty Pro Onboarding Wizard (2026-05-03, refined)
- Draft Brief (2).md — Guesty Pro Onboarding Initiative
- Executive Summary: Guesty Pro Onboarding Wizard

---

## Table of Contents

0. [Prototype vs. Production Boundary + V1 Decisions](#0-prototype-vs-production-boundary--v1-decisions)
1. [Overview](#1-overview)
2. [Problem Statement](#2-problem-statement)
3. [Goals & Non-Goals](#3-goals--non-goals)
4. [Target Users](#4-target-users)
5. [Prototype Scope & Objectives](#5-prototype-scope--objectives)
6. [Wizard Architecture](#6-wizard-architecture)
7. [Detailed Screen & Step Requirements](#7-detailed-screen--step-requirements)
8. [UX & Interaction Requirements](#8-ux--interaction-requirements)
9. [Data & State Requirements](#9-data--state-requirements)
10. [Success Metrics](#10-success-metrics)
11. [Out of Scope](#11-out-of-scope)
12. [Open Questions](#12-open-questions)
13. [Required Edge Cases](#13-required-edge-cases)
14. [Event Tracking Requirements (production handoff)](#14-event-tracking-requirements-production-handoff)
15. [Builder Guardrails](#15-builder-guardrails)
16. [Final Builder Summary](#16-final-builder-summary)

---

## 0. Prototype vs. Production Boundary + V1 Decisions

This is the **execution contract** between the PRD and the prototype builder. Read this first — it disambiguates what the prototype must demonstrate vs. what the production team will build later, and it locks in the V1 product decisions that govern every screen-level requirement that follows.

### 0.1 Prototype vs. Production Boundary

This PRD specifies a **functional prototype**, not the final production implementation. The two have different acceptance bars.

#### 0.1.1 Prototype must demonstrate

- End-to-end wizard flow (Welcome → Platform Handoff)
- Clickable navigation across all suggested steps (all skippable)
- Mocked but realistic account-level data
- Simulated Airbnb connection flow with reveal animation
- Simulated configuration writes with confirmation summaries
- Preset-driven variation (at minimum: Fast Launch and Migrate Existing Operations)
- Migration gate branching (fresh vs. migrating, with risk flags)
- Readiness view logic (per-domain Ready / In progress / At risk / Needs review / Not started)
- Additional prep unlock after the suggested path
- Platform handoff into a populated Guesty homepage
- Returning-user resume states (at least two)
- A representative set of edge cases (see Section 13)

#### 0.1.2 Prototype does not need to implement

- Real backend writes
- Real Airbnb OAuth
- Real Salesforce updates
- Real Rocketlane or Docebo integrations
- Real email reminders
- Real production analytics
- Full mobile responsiveness
- Full accessibility certification
- A complete CSM Review mode (the V2 dual-audience surface)

#### 0.1.3 Production PRD will need to define (out of scope here)

- API contracts for every wizard configuration write
- Real account state persistence and conflict resolution
- Auth and magic-link behavior across sessions
- Salesforce integration (specialist routing, OB events, churn signature tagging)
- Rocketlane integration (post-Call-1 task surface)
- Docebo integration (Academy deep links, completion tracking)
- Airbnb OAuth handling, token refresh, and disconnection flow
- Legal consent and permissions ("configure on my behalf")
- Event taxonomy and analytics pipeline (annotated in Section 14)
- Production error handling, retry logic, and SLAs
- Accessibility compliance (WCAG audit, screen-reader passes, keyboard navigation)

### 0.2 V1 Product Decisions

These decisions are **locked for V1**. The prototype must reflect every row; deviations require updating this table first, not redesigning the prototype.

| Area | V1 Decision |
|------|-------------|
| Primary user | Guesty Pro SMB owner-operator (5–70 properties, role-collapsed) |
| Primary job | Become synced, oriented, and review-ready before Call 1 |
| Primary product moment | Airbnb view-only sync (the AHA moment) |
| Hard activation gate (sole KPI) | Airbnb sync completed before Call 1 |
| Entry sequence | Intent Selection → Migration Gate → Airbnb Sync (strongly suggested order; none are gates) |
| Main UX pattern | Confirm or edit Guesty-recommended defaults — never blank fields |
| Primary status surface | Readiness view (per-domain), not progress bar |
| Scope model | Pilot launch (1–5 listings, 1 channel, core payments), not full account configuration |
| Review model | Customer prepares now; specialist reviews on Call 1 |
| Mandatory steps | **None.** Every step — including call booking — is optional. Customers may enter Guesty at any point without completing any wizard steps. |
| Re-engagement model | Automated reminder emails sent to users who haven't booked a call or completed key steps |
| Suggested prep | Strongly suggested (not required) pre-Call-1 path: Intent → Migration Gate → Airbnb Sync → Operations → Financials → Governance → Orientation → Features |
| Additional prep | Unlocked after the suggested track; further accelerates Call 1 quality |
| Governance model | Single-person fast path is the default; multi-person path is secondary |
| CSM Review mode | Not built in V1; V1 state model must support it without refactor |
| Platform handoff | Customer enters Guesty with real synced data visible (cold-start resolution); accessible at any point |
| Definition of done | "Ready for Call 1" (see Section 3.5) — *not* "ready to go live" |

This table is the prototype's plumb-line. If a screen, copy choice, or interaction implies a different decision, the screen is wrong, not the table.

---

## 1. Overview

### What this PRD covers

This PRD specifies the requirements for a **functional prototype** of the Guesty Pro Onboarding Wizard — a high-fidelity, interactive build that demonstrates the full end-to-end wizard flow with representative data, real interactions, and clickable states. Its purpose is concept validation, stakeholder alignment, and an implementation spec handoff for the production build. Data interactions are mocked where no production API exists.

### Why the wizard exists (root framing)

The structural problem is not that customers fail to complete setup tasks. It is that **Guesty's onboarding team cannot scale to meet new contract volume**, which creates an unavoidable wait between contract signing and the first specialist call — and that wait is where customers go silent, revert to their old PMS, and eventually churn.

The wizard does not eliminate this wait. It **converts it from passive idle into active, value-generating engagement** — so that by the time the specialist call finally happens, the customer is already configured, oriented, and invested. This framing matters for the prototype: every screen, copy decision, and interaction should be evaluated against the question *"does this hold the customer's momentum during the wait?"* — not just *"does this make setup easier?"*

Concretely, the wizard runs after registration and call booking, but before the customer enters the Guesty platform proper. It replaces the eliminated standalone kick-off call with a pre-platform configuration surface designed for small Guesty Pro accounts.

The broader organizational goal is session compression: from ~7–8 sessions (kickoff + 6–7 follow-ups) to 5 sessions (Setup Call + 4 follow-ups), removing the standalone kickoff call. The wizard's precise role in this is: **it creates the conditions required to safely remove that call** — by absorbing the orientation function of the kickoff and reducing walkthrough load on Call 1. Session compression is the downstream operational outcome; it is not the immediate product proof. The immediate proof is a better Call 1. If that succeeds, the operational decision to remove the kickoff call becomes safer to execute.

### Wizard vs. guided implementation system

This is a critical distinction that governs the prototype. The product being built is **a guided implementation system, delivered through an onboarding wizard UI** — not a setup wizard. The difference:

| A setup wizard | A guided implementation system |
|---------------|-------------------------------|
| Helps the customer complete setup steps | Helps the customer and CSM jointly turn the customer's business into a working operating model on Guesty |
| Optimizes for "steps completed" | Optimizes for "ready to operate" |
| Output is a configured account | Output is a *launchable* account — bounded scope, validated readiness, declared owners, surfaced blockers |
| Works the same for every customer | Adapts to the customer's stated launch intent through preset paths |

The prototype must demonstrably build toward "ready to operate," not "form complete." Specifically, the prototype must show that the wizard's value layer is launch readiness, not progress tracking — see the Five Core Objects below.

### The Five Core Objects of the Implementation System

The implementation system is built around five first-class objects. These are not derived UI patterns or progress signals — they are the operating model the prototype must encode in its data and reflect in its UI:

| Object | What it solves | Wizard manifestation |
|--------|---------------|---------------------|
| **Pilot** | Keeps scope small and outcome-driven — prevents over-onboarding | Bounded first-launch scope: typically 1–5 listings, 1 primary channel, core payments. Enforced by the preset and the migration gate. |
| **Milestones** | Tracks real activation events, not cosmetic field completion | Binary pass/fail checks: Airbnb sync (AHA), first booking-ready state, Call 1 readiness, graduation. No progress percentage. |
| **Blockers** | Makes delay manageable and visible — turns invisible momentum loss into actionable records | Captured per step (type, owner, due date, SLA impact, resolution path). V1 captures lightweight structured records; V2 elevates them to first-class operational objects. |
| **Owners** | Prevents "nobody owns it" failure — every configuration domain has a declared responsible party | Lightweight governance capture: admin, financials owner, go-live approver. For SMB, often one person — but the *explicit declaration* creates the governance record. |
| **Readiness gates** | Prevents premature graduation — validates account state, not just step touch | Per-domain readiness flags: listings active, channel connected, payments complete, financial rules reviewed, no critical blockers open. V1 tracks step touches but distinguishes them from readiness. |

The implication for V1 UI: **a readiness view is the right primary surface, not a progress bar.** A progress bar measures none of the five core objects. The prototype's primary "where am I?" surface should be a small readiness indicator (per-domain Ready / At risk / Not started) — even if a progress percentage appears as a secondary indicator.

### Architectural pattern: editable infrastructure, not education content

The wizard is **editable infrastructure**, not training, documentation, or guidance content. This is the structural difference from every previous Guesty onboarding surface — Rocketlane (project plan), Docebo (training videos), the in-app onboarding hub (dashboard) — all of which are education and guidance content wrapped around a static product.

Every wizard step must create **durable onboarding value** in one of three forms:

1. **Configuration write** — writing settings to the live Guesty account (Operations, Financials, GuestyPay, Owner records)
2. **Decision context capture** — capturing high-value onboarding context for the specialist (Intent selection, Migration gate, Feature interests, Governance capture)
3. **Cold-start orientation** — resolving the empty-platform problem so the product feels like the customer's business (Airbnb sync, Platform handoff)

This is intentionally broader than "every step writes configuration." Steps like intent selection, migration gate, feature interests, and governance capture do not configure product settings — but they capture context that the specialist needs, and that the wizard would lose if they were removed. A step belongs in the wizard if it produces durable onboarding value; it does not belong if it only explains, guides, or teaches.

**The principle: if a step does not write configuration, capture decision context, or resolve cold-start, it does not belong in the wizard.** The single exception is the Rocketlane + Docebo orientation checkpoint — one lightweight acknowledgement step where the customer clicks through to confirm they know these tools exist as reference points between sessions. This is navigation orientation, not education content.

The reference architecture is monday.com's hybrid CSM-guided build model — not because it's the same product, but because it solves the same structural problem: how does a product do 60–80% of configuration work while keeping the CSM layer as the **scoping, review, and governance layer**, rather than the delivery layer? Three-layer architecture:

| Layer | Role |
|-------|------|
| **The wizard** | Editable infrastructure — confirm-or-edit defaults, opinionated simplifications of the enterprise surface, real configuration writes |
| **Call 1 (Setup Call)** | CSM review and correction layer — not build time, but validation time |
| **Suggested / additional-prep split + Pilot scope** | Pilot scope guidance — the wizard presents a clear recommended path without blocking the customer from wandering |

One important difference from monday's model: monday assumes three distinct roles per account (exec sponsor, customer admin, process champion). For Guesty Pro SMB, **all three roles collapse into one person — the owner-operator**. The wizard must therefore supply *all of the structure that role-separation normally provides:* a clear suggested sequencing, suggested/additional-prep distinction, safety language on risky steps, and a clear definition of "ready." The product cannot assume the customer will self-organize. (See Target Users section for the full role-collapse implication.)

### Three modes / two audiences (V2 architecture, V1 implications)

The same underlying state model is intended to drive three presentation modes, serving two audiences. V1 ships only the customer-facing **Setup mode**, but the data model and prototype must be structured so the other two modes can be added in V2 without refactoring.

| Mode | User | Purpose | V1 status |
|------|------|---------|-----------|
| **Setup** | Customer | Completes guided configuration actions, confirms defaults, uploads data | Built in V1 (this prototype) |
| **Review** | CSM / Specialist | Checks readiness, identifies blockers, flags SLA risk before Call 1 | Out of scope for V1 prototype; data model must support it |
| **Governance** | CSM / Admin | Confirms the account is safe to scale — go-live approval, owner access, role review | Out of scope for V1 prototype; data model must support it |

Example same-state-different-view: Customer sees *"Connect your first booking channel."* CSM Review mode would see *"Channel connection: incomplete · SLA risk: High · Customer last active: 6 days ago."*

### Prototype objectives

The prototype must:

- Validate the UX concept with users and stakeholders
- Pressure-test the Airbnb AHA moment and step sequencing
- Demonstrate that the wizard is engaging *during the wait*, not just usable when the customer chooses to engage
- Demonstrate the **editable infrastructure principle** — every step the test user sees should produce a tangible configuration outcome they can point to ("I just set my cancellation policy"), never a "learn more about cancellation policies" outcome
- Demonstrate the **intent-driven preset path** — the customer's launch goal selected at wizard entry visibly shapes the task sequence and defaults that follow
- Demonstrate the **migration gate** — branching to fresh-setup vs. migration-aware flows based on a single early decision
- Demonstrate the **readiness view** as the wizard's primary "where am I?" surface (rather than a progress bar)
- Serve as the implementation spec handoff for the production build

---

## 2. Problem Statement

New Guesty Pro SMB customers sign a contract, create an account, and land on a blank enterprise platform with no guidance. The standalone kick-off CSM call — previously the first human orientation point — is being eliminated. Without a replacement:

- Customers arrive at Call 1 (the Setup Call) with zero pre-work done
- **~49.4% of all Guesty churn carries a silent/non-responsive/unknown signature** — customers who stopped engaging before the product could succeed for them
- Specialist calls are consumed by walkthrough labor ("go here, click here") instead of review and judgement
- The SMB SLA machine is structurally failing: only **18% of SMB accounts graduated on time in April 2026**, with 69% delayed and an average finish 28.8 days past the 20-day target
- Adding more call hours does not fix it: months with higher specialist volume show no better SLA outcomes — the bottleneck is momentum, not effort. The SME segment graduates on time at 57.5% despite a longer 60-day SLA, suggesting the SMB *operating model* (not complexity) is the failure driver

Four compounding failure modes drive this:

1. **Cold start:** Empty homepage, empty calendar, empty inbox. Customers revert to old PMS and wait.
2. **No clarity on priority steps:** Customers don't know which actions have the biggest impact before Call 1. They build Google Sheets to compensate.
3. **Enterprise UI in SMB context:** 200+ fee types, 10-step flows, and granular controls overwhelm a 5-property owner-operator on day one.
4. **The wait itself is the risk.** The OB team cannot absorb new contract volume at the rate contracts are signed. The gap between registration and Call 1 is not a design flaw — it is a capacity constraint. Without something to do during that gap, customers decay: motivation fades, the old PMS gets a second chance, and momentum that was high at contract-signing is gone by the time the specialist calls. **The wizard's primary job is to capture that intent window before it closes.**

### What the wizard does *not* attempt to solve

These are explicitly out of scope so the prototype is not measured against them:

- **OB team capacity.** The wizard reduces the quality bar needed from each call; it does not add headcount or shorten the contract-to-Call-1 wait.
- **Inter-call momentum loss.** The wizard owns only the pre-Call-1 gap. A future momentum-control system (V2) extends across the full journey.
- **Churn reason taxonomy.** "Unknown Reason" is the largest single churn category (18.5%); fixing the diagnostic gap is an ops/tooling problem outside this initiative.
- **GuestyPay activation funnel.** GuestyPay drives ~82% of onboarding-period upsell revenue and deserves its own funnel. The wizard includes a "start application" optional step but does not replace a dedicated GuestyPay activation path.
- **Platform education, product walkthroughs, and feature training.** This initiative is not a training surface. It does not produce videos, guided tours, tooltips, help content, or feature explainers. Docebo, the in-app onboarding hub, and Rocketlane already serve that function. The wizard's output is **configuration writes, decision context, and cold-start resolution** — every step must produce at least one of these. Steps that only explain, guide, or teach do not belong in the wizard. The single exception is the Rocketlane + Docebo orientation checkpoint, which is navigation orientation (a single click-through acknowledgement), not education content.

---

## 3. Goals & Non-Goals

### Goals (this PRD / prototype)

| # | Goal |
|---|------|
| G1 | Demonstrate the complete wizard flow from intent selection through platform handoff in a single, navigable prototype |
| G2 | Validate the Airbnb view-only sync as the AHA moment — show real data populating the homepage, calendar, and inbox UI within the wizard |
| G3 | Demonstrate the **intent-driven preset path** — show that the customer's launch goal selected at wizard entry visibly shapes the task sequence and defaults that follow (at minimum, two preset paths must be visualized end-to-end: Fast Launch and Migrate Existing Operations) |
| G4 | Demonstrate the **migration gate** — branching from a single early decision into either fresh-setup or migration-aware flows |
| G5 | Demonstrate the confirm/edit interaction pattern for pre-configured defaults across all suggested steps |
| G6 | Show non-linear navigation: forward, backward, and section-jump from the progress sidebar |
| G7 | Show the suggested vs. additional-prep track split, and how additional tasks unlock |
| G8 | Demonstrate the **wait-conversion mechanic** — that the customer stays engaged during the days between registration and Call 1 (call countdown, returning-user resume flow, "what to finish before your call" prompts) |
| G9 | Demonstrate the **readiness view** — a per-domain Ready / At risk / Not started indicator as the wizard's primary "where am I?" surface |
| G10 | Demonstrate **lightweight governance capture** — a single declaration of who owns admin, financials, and go-live approval (often one person for SMB, but the explicit declaration is the V1 deliverable) |
| G11 | Produce screens and interaction specs detailed enough to hand off to an engineering team for production implementation |

### Non-Goals (explicitly excluded from prototype)

- Live API integration with Guesty's production backend
- Live Airbnb OAuth integration (mocked in prototype)
- Real financial configuration writes to production accounts
- Mobile responsiveness (desktop-first for prototype)
- Localization / internationalization
- Accessibility (WCAG) certification — a11y notes included as requirements for production

### 3.5 "Ready for Call 1" — definition

This is the V1 product's **definition of done**. It governs the readiness view, the success metrics, and the prototype's acceptance bar. The prototype must reflect this definition exactly — and must not imply any stronger claim (e.g., "ready to go live").

A customer is **Ready for Call 1** when they have enough account state for the specialist to *review, validate, and personalize* the first session — instead of walking the customer through basic platform configuration.

> **Critical framing: Nothing in this flow is mandatory.** Customers can enter Guesty at any point — before, during, or after the wizard — without completing any step, including scheduling a call. The wizard is a strong suggestion system, not a gate. Customers who do not complete steps or book a call will automatically receive reminder emails. The prototype must never block platform entry or imply that steps are required.

#### Strongly suggested (all optional — improves Call 1 quality when completed)

- Intent selection is complete
- Migration Gate is complete
- Airbnb view-only sync is complete (the primary activation KPI when achieved)
- Call 1 is booked (if not booked, automated reminder emails are triggered)

#### Also strongly suggested (further improves Call 1 quality)

- Operations setup completed
- Financials setup completed
- Governance Capture completed
- At least one feature interest selected

#### CSM-visible risk flags (do not block customer; do create review flags)

These do not stop the customer from proceeding, but each one creates a structured `reviewFlag` (see Section 9.2 Core State Model) that the specialist sees on Call 1 prep:

- Airbnb sync skipped
- Airbnb sync failed
- Migration complexity selected (listings + reservations, accounting, from another PMS)
- Tight migration timeline selected (within 2 weeks + complex)
- Tax setup marked "I'm not sure"
- GuestyPay not started
- Customer inactive after starting the wizard (V2 hookpoint; V1 captures the timestamp)
- Financials incomplete
- Operations incomplete

#### Important distinction (must never be obscured in copy)

> **"Ready for Call 1" does not mean "ready to go live."**
>
> It means the specialist can use Call 1 for review, validation, and edge cases instead of basic walkthrough. Go-live readiness is a downstream milestone the specialist signs off after Call 1 (and is the V2 Readiness Gates concept).

This distinction must be visible in the Readiness Summary screen (Section 7.11) and the Platform Handoff screen (Section 7.12). The prototype must never state or imply that wizard completion equals go-live readiness.

---

## 4. Target Users

### Primary: Guesty Pro SMB Operator

A property management company owner-operator or very lean team running **5–70 properties** on Guesty Pro (segment average: ~50–70 properties). Financially committed (contract signed). Time-pressed. Not technical in an IT sense. Looking for Guesty to tell them what to do, in what order, with sensible defaults pre-filled.

### The role-collapse reality (critical design constraint)

For Guesty Pro SMB accounts, **all three onboarding roles that an enterprise vendor like monday.com would negotiate separately collapse into a single person**:

| Role (in enterprise model) | Function | In SMB |
|---------------------------|----------|--------|
| Executive sponsor | Authorizes scope, holds vendor accountable | Owner-operator (same person) |
| Customer admin | Owns the configuration build | Owner-operator (same person) |
| Process champion | Internal stakeholder management, escalates blockers | Owner-operator (same person) |

There is no internal project manager to compensate for ambiguity, no champion to escalate blockers, and no exec to reauthorize scope. **The wizard must therefore supply all of the structure that role-separation normally provides:**

| What role-separation normally does | How the wizard substitutes |
|-----------------------------------|---------------------------|
| Customer champion enforces sequencing | Wizard enforces a suggested sequencing through the recommended-path ordering and additional-prep unlock |
| Customer admin clarifies "what matters most" | Wizard's suggested/additional-prep distinction is visually unmistakable in the sidebar |
| Exec sponsor frames risk acceptance | Wizard delivers explicit safety language on every risky step (Airbnb sync, owner upload) |
| Customer champion holds the team to "done" | Wizard provides a clear definition of "ready for Call 1" — derived from the readiness view (per-domain Ready / At risk / Not started), not a step count |

This is why opinionated defaults are non-negotiable: the wizard cannot wait for the customer to self-organize because there is no internal organization to wait on.

### Key pain points the prototype must address

| Pain Point | Prototype Response |
|-----------|-------------------|
| "It's a firehose of information" | Full-screen wizard with one task at a time; no platform chrome visible |
| "I was nervous to hit the sync button" | Explicit safety copy before every "connect" or "allow" action; risk-zero framing |
| "I don't know what I should do first" | Visual suggested/additional-prep distinction throughout; progress sidebar labels each section; all steps clearly skippable |
| "After the call I had no recap" | Wizard progress is persistent and visible; each completed section shows what was configured |
| "I built my own checklist" | The wizard IS the checklist — remove the need for external scaffolding |
| "There's no one to tell me what's important" (role-collapse) | Wizard's opinionated defaults and suggested-path sequencing replace the absent internal champion |

### Secondary: Guesty Onboarding Specialist (Call 1 reviewer)

Not a wizard user in V1 (Setup mode is customer-only). The specialist will need a CSM-facing **Review mode** that surfaces readiness, blockers, SLA risk, and customer activity — but this is V2 scope. The V1 prototype does not build this interface; however, the V1 data model is structured (Section 9.2) so the V2 Review mode can be added as a *projection* of the same state, not as a separate model. All wizard outputs are reviewable by the specialist via the readiness view that appears at Step 7.11 (which V2 will extend with SLA and activity signals hidden from the customer view).

---

## 5. Prototype Scope & Objectives

### V1 product structure — five modules

V1 is built from five core modules. Every prototype screen belongs to one of these modules. Use this as a quick orientation before reading the detailed step requirements in Section 7.

| Module | Steps in scope | Purpose |
|--------|---------------|---------|
| **1. Launch Path** | Intent Selection, Migration Gate | Scope before configure — establish what the customer is launching and whether they're starting fresh or migrating |
| **2. Cold-Start Resolution** | Airbnb Sync | The AHA moment — turn the platform from empty software into a mirror of the customer's real business |
| **3. Core Call 1 Preparation** | Operations, Financials, Feature Interests | Confirm/edit Guesty defaults; give the specialist a meaningful starting point for Call 1 |
| **4. Ownership & Governance** | Governance Capture | Lightweight record of who owns admin, financials, and go-live approval |
| **5. Readiness & Handoff** | Orientation, Suggested Path Complete, Readiness Summary, Platform Handoff | Produce a review-ready account and a populated Guesty homepage |

**Optional Prep** (Booking Engine, Owner Prep, Logo Upload, GuestyPay start, Rate Strategy, Historical Data) sits outside the five modules — it is post-required, time-permitting acceleration for motivated customers. It is not the core V1 proof.

### What the prototype must demonstrate

The prototype covers the following flow exactly:

```
[Wizard Welcome]
   ↓
[Intent Selection]   ← what is the first workflow you need to launch? (5 presets)
   ↓
[Migration Gate]     ← starting fresh or migrating existing operations?
   ↓
[Airbnb Sync]        ← AHA moment, populates homepage/calendar/inbox
   ↓
[Operations]
   ↓
[Financials]
   ↓
[Governance Capture] ← who owns admin / financials / go-live approval (lightweight)
   ↓
[Rocketlane + Docebo Orientation]
   ↓
[Interesting Features]
   ↓
[Suggested Path Complete] → unlocks Additional Prep Track
   ↓
[Additional Prep Steps]
   ↓
[Readiness Summary]  ← per-domain Ready / At risk / Not started view
   ↓
[Platform Handoff screen]
```

All suggested steps, plus the additional-prep unlock and readiness summary, must be clickable and navigable. Every step must show a visible skip path — no step may block the customer from continuing or exiting to Guesty. The prototype must show:

1. **Intent selection driving downstream content** — selecting a different preset on the welcome screen visibly changes the task sequence, default values, and readiness criteria the customer sees in subsequent steps. At minimum, the prototype must demonstrate this for two presets (Fast Launch and Migrate Existing Operations)
2. **Migration gate branching** — the answer to "starting fresh vs. migrating" routes the customer into different downstream paths; migration paths surface SLA warnings and CSM-validation flags before configuration begins
3. **Pre-populated defaults** in every form-based step — the customer sees Guesty's best-practice choices pre-filled, not blank fields
4. **Confirm / Edit interactions** — clicking "confirm" advances the step; clicking "edit" opens field-level editing in context
5. **The AHA moment** — a before/after state where the Guesty homepage, calendar, and inbox widgets inside the wizard visibly transform after Airbnb sync completes
6. **Non-linear navigation** — a persistent left-sidebar that lets the customer jump to any unlocked step
7. **The scheduled call reminder** — the specialist name, call date/time, and "X days away" counter visible in the wizard as a persistent motivator
8. **Additional prep unlock** — after all suggested steps are complete, the additional-prep track visibly unlocks in the navigation and a contextual prompt appears
9. **Lightweight governance capture** — a single screen (or inline question set) where the customer declares the admin, financials owner, and go-live approver. For SMB, the prototype's mock customer fills all three slots with the same name; the prototype demonstrates the *capture pattern*, not the multi-role workflow
10. **Readiness view** — a per-domain summary (Listings · Channels · Payments · Financial setup · Team access) showing Ready / At risk / Not started — visible at the readiness summary screen and surfaced in miniature at the top of the wizard sidebar throughout the flow
11. **Platform transition** — a clear "You're ready for Call 1" end screen with a readiness summary of what was configured

### Editable-infrastructure validation (audit checklist)

The prototype must pass this checklist before stakeholder review. For each wizard step, the test is: *what configuration outcome does this produce on the customer's account?*

| Step | Required configuration outcome | Pass / fail criterion |
|------|------------------------------|----------------------|
| Intent Selection | A preset is selected, stored on the account, and used to drive downstream defaults and task sequencing | Subsequent steps visibly reflect the selected preset (e.g., different task order, different defaults) |
| Migration Gate | A migration-mode flag is stored ("fresh" / "listings only" / "listings + reservations" / "accounting + payments" / "from another PMS") | Subsequent steps reflect the branch; migration paths show SLA warnings and CSM-validation flags |
| Airbnb Sync | A live OAuth grant; listings, bookings, and messages imported | Outcome is visible in the populated homepage / calendar / inbox widgets |
| Operations | Operations settings written (cleaning windows, check-in/out times, inspection rule) | Step ends with a confirmation summary listing what was saved |
| Financials | Fees, cancellation policy, revenue calculation, payment automation, and tax settings written | Step ends with a confirmation summary listing what was saved |
| Governance Capture | Admin owner, financials owner, and go-live approver fields are written to the account | Step ends with a confirmation summary; the readiness view shows "Team access: Ready" |
| Rocketlane + Docebo Orientation | An acknowledgement flag stored against the account ("customer has been oriented to supporting tools") | This is the explicit exception — a navigation acknowledgement, not a configuration write. Must be flagged as the single exception. |
| Interesting Features | A list of customer-selected feature interests stored on the account, used to personalize Call 1 agenda | Step ends with a "your specialist will focus on…" summary |
| Each optional step | A specific configuration write or saved input (logo file, booking engine flags, owner records, etc.) | Step ends with a confirmation summary |

If any step in the prototype produces only "the customer has read about this feature" or "the customer has watched a video", that step has violated the editable-infrastructure principle and must be redesigned.

### Pilot scope demonstration

The prototype must visibly enforce **pilot scope** — the bounded first-launch scope of 1–5 listings, 1 primary channel, and core payments. This is shown by:

- Surfacing only what the pilot needs: the wizard hides advanced accounting, owner statements, complex automation, and additional OTA channels, with explicit copy that these are deferred to later sessions ("we'll cover this with your specialist in your second session")
- Showing the "see all options" path as a deliberately demoted, secondary affordance — never the primary CTA
- Surfacing the customer's pilot scope on the readiness view ("Pilot: 3 listings, Airbnb only, Guesty Pay") so the customer can see what they're launching with

### Prototype fidelity level

| Dimension | Level |
|-----------|-------|
| Visual design | High fidelity — production-quality UI using Guesty's design system (Nebula) or a close approximation |
| Interactions | Clickable — all navigation, CTA buttons, form confirms, and back-navigation functional |
| Data | Mocked — realistic fake data representing a 12-property Airbnb operator |
| API calls | Simulated — connection flows show loading states and success states; no live API |
| Edge cases | Representative — one "unhappy path" per major step (e.g., Airbnb connection failure) |

---

## 6. Wizard Architecture

### 6.1 Entry Point & Trigger

The wizard is triggered automatically for every new Guesty Pro SMB customer. It is accessed via a unique URL delivered in the registration email after the customer completes:

1. Password + MFA setup
2. Payment info entry
3. Call 1 booking (optional — the wizard loads whether or not the customer books a call)

The wizard loads immediately after step 2 completes (or after call booking if the customer chooses to book). **The wizard is not a gate** — customers may exit the wizard and enter the Guesty platform at any point without completing any steps. Customers who have not booked a call will see a persistent prompt to book one, and will receive automated reminder emails until they do.

### 6.2 Layout Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│  [Guesty Logo]                          [Next call: May 18 · 3d] │
├────────────────┬────────────────────────────────────────────────┤
│                │                                                  │
│  READINESS     │                                                  │
│  View          │                                                  │
│  Listings  ✓   │                                                  │
│  Channels  !   │          MAIN CONTENT AREA                      │
│  Payments  ○   │                                                  │
│  Financial !   │                                                  │
│  Team      ○   │                                                  │
│  ─────────────  │                                                  │
│  STEPS         │                                                  │
│  ✓ Intent      │                                                  │
│  ✓ Migration   │                                                  │
│  ● Airbnb Sync │                                                  │
│  ○ Operations  │                                                  │
│  ○ Financials  │                                                  │
│  ○ Governance  │                                                  │
│  ○ Orientation │                                                  │
│  ○ Features    │                                                  │
│  ─────────────  │                                                  │
│  Optional      │                                                  │
│  ○ Booking Eng │                                                  │
│  ○ Owner Prep  │                                                  │
│  ○ Logo Upload │                                                  │
│  ○ Rate Strat  │                                                  │
│  ○ Guesty Pay  │                                                  │
│  ○ Hist. Data  │                                                  │
│                │                                                  │
└────────────────┴────────────────────────────────────────────────┘
```

**Top bar:** Guesty logo (left) + persistent call reminder (right): "Your next session with [Specialist Name] is on [Date] — [N days away]"

**Left sidebar (top section): Readiness view.** Per-domain readiness summary using three states: ✓ Ready · ! At risk · ○ Not started. This is the primary "where am I?" surface — a customer-facing simplification of the readiness dashboard. The five domains visible in V1: **Listings · Channels · Payments · Financial setup · Team access**. The readiness state is *derived* from underlying step completions and configuration writes — not from a manual progress percentage.

**Left sidebar (bottom section): Step list.** Per-step navigation showing all wizard steps with their completion state. Suggested steps labeled as "Recommended." Completed steps show checkmark. Current step highlighted. Additional prep section visually separated (dimmed until suggested path is complete).

**Main content area:** Full-width step content. Navigation buttons (Back / Continue) at the bottom of each step.

**Note on the readiness view vs. progress bar.** A traditional "X% complete" indicator may appear as a *secondary* element (e.g., small text under the readiness view), but is not the primary surface. The readiness view conveys what is operationally ready to launch — the progress bar conveys only how many fields have been touched. The first is the implementation system's value layer; the second is a setup-wizard relic. The prototype must lead with the first.

### 6.3 Navigation Rules

| Rule | Behavior |
|------|----------|
| Forward navigation | Customer clicks "Continue" or "Confirm" at the bottom of each step |
| Backward navigation | Customer clicks "Back" or clicks any previously completed step in the sidebar |
| Step jumping | Customer can click any completed or current step in the sidebar to jump directly |
| Suggested prep steps | Shown in primary style in sidebar; grayed-out additional prep steps unlock once suggested path is complete |
| Skipping any step | Customer can navigate away from any step — including suggested ones — without completing it; step shows "incomplete" state in sidebar |
| Exit to platform | "Enter Guesty" CTA is always accessible — never blocked by incomplete steps |
| Browser back button | Should mirror the in-wizard back navigation (does not break flow) |
| Session persistence | Wizard state persists across sessions — returning customer resumes at last incomplete step |

### 6.4 Wizard Step Map

| # | Step | Track | Type | Strongly suggested before Call 1 |
|---|------|-------|------|----------------------------------|
| 0 | Welcome | Entry | Self-serve orientation | n/a |
| 1 | **Intent Selection** (preset path selection) | Suggested · Entry | Alone — drives downstream defaults and task sequencing | Yes (strongly suggested — skippable) |
| 2 | **Migration Gate** (fresh / migrating + branch) | Suggested · Entry | Alone — branches downstream path; surfaces SLA risk for migration paths | Yes (strongly suggested — skippable) |
| 3 | Airbnb Sync | Suggested | Alone (Self-serve) | **Yes — primary activation KPI (skippable; triggers review flag if skipped)** |
| 4 | Operations Setup | Suggested | Alone + OB Review | Yes (strongly suggested — skippable) |
| 5 | Financials Setup | Suggested | Alone + OB Review | Yes (strongly suggested — skippable) |
| 6 | **Governance Capture** (admin / financials owner / go-live approver) | Suggested | Alone — lightweight declaration | Yes (strongly suggested — skippable) |
| 7 | Rocketlane + Docebo Orientation | Suggested | Alone (orientation acknowledgement) | Yes (strongly suggested — skippable) |
| 8 | Interesting Features | Suggested | Alone (selection drives Call 1 agenda) | Yes (strongly suggested — skippable) |
| 9 | Booking Engine | Additional prep | Alone + OB Review (Call 1) | No |
| 10 | Owner Prep | Additional prep | Alone | No |
| 11 | Logo Upload | Additional prep | Alone | No |
| 12 | Rate Strategy | Additional prep | Alone + OB Review (Call 3) | No |
| 13 | Guesty Pay | Additional prep | Alone | No |
| 14 | Historical Data | Additional prep | Alone + OB Review | No |
| 15 | **Readiness Summary** (per-domain Ready / At risk / Not started view + pilot scope) | Exit | n/a | n/a — pre-platform handoff |
| 16 | Platform Handoff | Exit | n/a | n/a |

**New steps added in v1.3:** Intent Selection (1), Migration Gate (2), Governance Capture (6), Readiness Summary (15). These reflect the brief's expansion from "wizard" to "guided implementation system."

### 6.5 Step interaction modes (per the role-collapse / CSM-guided architecture)

Because all onboarding roles collapse into one owner-operator (see Target Users), the wizard cannot rely on a customer admin to "schedule the review with the specialist." The wizard itself must signal which steps the customer is finishing alone vs. which steps will be reviewed live with the specialist on a call. Two interaction modes apply:

| Mode | What it means for the customer | What the prototype must show |
|------|------------------------------|------------------------------|
| **Alone** | The customer's input is final once confirmed. No specialist review expected. Examples: Airbnb Sync, Owner Prep, Logo Upload. | Standard "Saved · Continue →" completion state. No "your specialist will review" copy. |
| **Alone + OB Review** | The customer configures opinionated defaults and confirms; the specialist reviews and refines on the relevant call. The customer's input is *initial*, not *final.* Examples: Operations, Financials, Booking Engine, Rate Strategy, Historical Data. | Completion state must explicitly say *"Your specialist will review these with you on Call [N]"* and (optionally) what edge cases the specialist will help with. This sets expectations and reduces "did I do this right?" anxiety. |

The Alone vs. Alone + OB Review distinction is the open question (Q3) that the team must finalize per task. The prototype must visualize both modes' completion patterns so stakeholders can pressure-test which steps belong in which mode.

### 6.6 Canonical Prototype Flow

This is the locked screen sequence the prototype must implement. Builders may not reorder, merge, or skip these screens. Step labels here match Section 7's screen specs.

```
1.  Welcome
2.  Intent Selection
3.  Migration Gate
4.  Airbnb Sync
5.  Operations Setup
6.  Financials Setup
7.  Governance Capture
8.  Rocketlane + Docebo Orientation
9.  Interesting Features
10. Suggested Path Complete (transition screen)
11. Optional Prep
12. Readiness Summary
13. Platform Handoff
14. Mock Guesty Homepage (populated, post-handoff)
```

#### Flow rules (non-negotiable)

These rules protect the core thesis: *scope before configure, then resolve cold start, then prepare for review.*

- Welcome always comes first.
- Intent Selection must happen before any configuration step.
- Migration Gate must happen before Airbnb Sync.
- Airbnb Sync is the primary activation step and the sole hard KPI.
- Operations and Financials must use confirm/edit defaults, never blank fields.
- Governance Capture must default to the single-person SMB path ("I'm all three").
- Orientation must be lightweight (click-through acknowledgement) and must not become training content.
- Interesting Features must drive Call 1 agenda personalization.
- Additional Prep unlocks after the suggested path is complete; however, users may exit to Guesty at any point before or after.
- Readiness Summary must appear before Platform Handoff.
- Platform Handoff must lead into a populated Guesty homepage, never an empty state.

### 6.7 Required Prototype Paths

The prototype must demonstrate **two complete end-to-end paths** through the canonical flow. Both paths must be clickable from start (Welcome) to end (Mock Guesty Homepage), with the readiness view, copy adaptations, and review flags reflecting the path's choices.

#### Path A — Fast Launch (the dominant SMB path)

Customer profile:
- 12-property Airbnb operator
- Starting fresh (no existing PMS migration)
- Wants to launch quickly
- Solo owner-operator

Flow steps:

1. Selects **Fast Launch** at Intent Selection
2. Selects **Starting Fresh** at Migration Gate
3. Completes **Airbnb sync** successfully (12 listings, 4 bookings, 3 messages imported)
4. Confirms all **Operations** defaults without edits
5. Confirms **Financials** defaults; tax answered "Yes · 10% Occupancy" (no review flag)
6. Uses **"I'm all three"** governance shortcut
7. Completes **Orientation** (clicks both Rocketlane and Docebo cards)
8. Selects **Booking Engine** and **Automated Messaging** as feature interests
9. Reaches **Readiness Summary**
10. Enters **populated Guesty homepage**

Expected readiness states at the Summary screen:

| Domain | State |
|--------|-------|
| Listings | Ready |
| Channels | Ready |
| Payments | Not started OR In progress (depending on whether the customer touched the optional GuestyPay step) |
| Financial setup | Ready (or Needs review if any sub-flag) |
| Team access | Ready |

Active review flags: 0 (clean Path A run) — but the prototype must visualize what zero flags looks like in the Specialist Handoff Output (Section 7.11).

#### Path B — Migrate Existing Operations

Customer profile:
- Existing property manager
- Moving from another PMS
- Has listings + reservations
- Wants to go live within 2 weeks

Flow steps:

1. Selects **Migrate Existing Operations** at Intent Selection
2. Selects **Migrating** at Migration Gate
3. Selects **Listings + reservations** in migration items (multi-select)
4. Selects **From another PMS**
5. Selects **"Within 2 weeks"** target go-live window
6. Sees **migration complexity warning** with a "your specialist will validate the right plan" frame
7. Completes **Airbnb sync** successfully
8. **Operations** copy adapts to migration context (e.g., "we'll review against your existing operational rules during migration")
9. **Financials** includes at least one specialist-review flag (e.g., tax answered "I'm not sure," or accounting marked for migration)
10. Reaches **Readiness Summary** showing At risk / Needs review states
11. Enters **populated Guesty homepage** with a small migration-review banner ("Your specialist will validate your migration on Call 1")

Expected readiness states at the Summary screen:

| Domain | State |
|--------|-------|
| Listings | Ready or Needs review |
| Channels | At risk |
| Payments | Not started |
| Financial setup | Needs review |
| Team access | Ready |

Active review flags (at minimum):
- `migration_complexity_high` (listings + reservations + from another PMS)
- `migration_timeline_tight` (within 2 weeks + complex)
- One financials review flag

These two paths together prove **intent-driven branching** — the prototype isn't just displaying preset tiles, it's adapting downstream copy, defaults, and readiness based on the customer's choices.

### 6.8 Skip Rules

Skipping must not break the flow, but consequences must be clear. The matrix below governs every step's skip behavior in the prototype.

| Step | Can skip? | Result if skipped |
|------|-----------|------------------|
| Welcome | n/a | Customer can postpone with "I'll come back later" — saves state |
| **Intent Selection** | **No** | Continue is disabled until a launch path is selected |
| **Migration Gate** | **No** | Continue is disabled until "Fresh" or "Migrating" is answered |
| Airbnb Sync | Yes, but discouraged | Listings and Channels become At risk; review flag `airbnb_sync_skipped` is created |
| Operations | Yes | Step incomplete; review flag `operations_incomplete` created |
| Financials | Yes | Financial setup becomes At risk; review flag `financials_incomplete` created |
| Governance Capture | Yes, but discouraged | Team access stays Not started; review flag `governance_missing` created |
| Orientation | Yes | Step remains incomplete; no readiness blocker, no review flag |
| **Interesting Features** | **No** | Continue is disabled until at least one feature is selected (drives Call 1 agenda) |
| Optional Prep | Yes (always) | No blocker; step remains skipped; no review flag |

#### Airbnb skip copy (mandatory)

When the customer attempts to skip Airbnb sync, the prototype must show this confirmation:

> **You can continue, but your account will still be empty when you enter Guesty.**
>
> Your specialist can help you connect Airbnb on Call 1, but you'll miss the chance to see your real listings, calendar, and messages before then.

CTAs:
- **Primary:** "Connect Airbnb now"
- **Secondary:** "Continue without syncing"

If the customer chooses "Continue without syncing," the readiness view shows Listings and Channels as **At risk** (not Not started), and the review flag `airbnb_sync_skipped` is created.

---

## 7. Detailed Screen & Step Requirements

### 7.0.0 Universal Acceptance Criteria (applies to every screen below)

Every screen in Section 7 must pass this checklist before it's treated as deliverable. Per-screen sections below add screen-specific criteria *on top of* this universal set.

- User understands the purpose of the step within 5 seconds of landing
- Primary CTA is visually unambiguous (one clear "next" button per screen)
- User can navigate back without losing state already entered
- User can leave the wizard and resume later (returning-user resume; see Section 8.7)
- The sidebar shows the current step highlighted
- The sidebar shows previously completed steps with a check mark
- The readiness view (sidebar + Section 7.11) updates when this step impacts a domain
- The completion state of the step explicitly confirms what was saved
- Any "connect," "import," or "upload" action includes inline safety copy above the CTA (never hidden in tooltips)
- Any **Alone + OB Review** step's completion state explicitly says the specialist will review it on the relevant call (see Section 8.8)
- The screen does not imply the customer is "fully ready" or "ready to go live" — only "Ready for Call 1" (see Section 3.5)

If a screen fails any of these, it must be reworked before stakeholder review.

---

### 7.0 Wizard Welcome Screen

**Purpose:** Establish that this is **preparation for Call 1**, not full onboarding completion. Set the right expectation, surface the call reminder, and create forward momentum into Intent Selection.

**Screen content:**

| Element | Spec |
|---------|------|
| Headline | "Let's get your account ready for your first session" |
| Sub-copy | "In the next few steps, we'll help you choose your launch path, safely bring in your Airbnb data, and prepare the key settings your specialist will review with you." |
| Call reminder card | Specialist photo, name, date/time, "X days to go" — if booked. If not booked: "Booking a session is recommended — your specialist can review what you set up. [Book now]" (soft prompt; not a blocker) |
| Time hint | "Most customers complete the suggested path in about 30 minutes — or you can enter Guesty now and come back anytime." |
| Save assurance | "Progress saves automatically. You can come back anytime." |
| Primary CTA | "Start preparing →" |
| Secondary | "I'll come back later" (saves state, shows return URL) |

**Prototype requirements:**
- The welcome screen must show the call reminder in two states: booked and unbooked
- The welcome screen must show a visible "Enter Guesty now" or "Skip setup" path — the wizard is never a gate
- "Start preparing" navigates to **Step 1 (Intent Selection)** — not directly to Airbnb Sync
- "I'll come back later" shows a modal with a magic link / return email confirmation
- Copy explicitly frames the wizard as preparation for the first session, not a required completion step

---

### 7.1 Step 1 — Intent Selection (Preset Path)

**Purpose:** Scope before configure. The customer's launch goal determines the task sequence, default values, and readiness criteria for everything that follows. This is the structural difference between a setup wizard and a guided implementation system.

#### 7.1.1 Layout

| Element | Spec |
|---------|------|
| Step label in sidebar | "Choose your launch path" with a "🎯 Start here" badge |
| Headline | "What's the first workflow you need to launch on Guesty?" |
| Sub-copy | "We'll set up the right path for you — different goals need different starting points. You can change this later." |
| Selection format | Five tile cards in a vertical or 2-column grid; single-select (radio behavior) |
| Time hint | "This takes about 30 seconds and shapes the rest of your setup" |

#### 7.1.2 The five preset paths (V1)

| Preset ID | Tile headline | Sub-copy | Intended for |
|-----------|--------------|---------|--------------|
| `fast_launch` | **Fast Launch** | "I want to get listings live and accept bookings as quickly as possible" | Solo operators starting fresh, channel-primary setup |
| `migrate_existing` | **Migrate Existing Operations** | "I'm moving an existing business — listings, reservations, and operations — into Guesty" | Accounts moving from another PMS with existing listings + reservations |
| `channel_sync` | **Channel Sync Setup** | "I want to sync multiple OTAs and centralize everything in one place" | Channel-heavy customers with multiple OTA integrations |
| `payments_first` | **Payments & Financials First** | "Getting accounting and payment processing right is my main priority" | Finance-heavy setups where accounting structure is the primary blocker |
| `team_ops` | **Team Operations Setup** | "I have a team — I need to set up roles, access, and operational handoffs" | Accounts with 2+ team members who need role and access structure |

Each tile shows: a short headline, a one-line plain-English sub-copy framed in customer voice, and a small visual indicator (icon or count) suggesting the path's scope (e.g., "5–7 setup steps · most common").

#### 7.1.3 What happens after selection

- The selected preset is written to the account state (`activePreset: "fast_launch"`)
- The downstream task sequence, default values, and readiness criteria are configured to that preset
- The customer cannot proceed without making a selection
- Selection can be revised later via a "Change launch path" link in the sidebar (rare; flagged as needing CSM consultation if changed mid-flow)

#### 7.1.4 Example: how preset selection visibly changes downstream flow

The prototype must demonstrate the preset effect with at least two concrete examples:

| Step | If `fast_launch` selected | If `migrate_existing` selected |
|------|--------------------------|-------------------------------|
| Migration Gate (Step 2) | Default branch: "Starting fresh" pre-selected; "Migrating" still available | Default branch: "Migrating" pre-selected; explicit migration sub-questions surface |
| Airbnb Sync framing | "Connect Airbnb to populate your listings" | "Connect Airbnb so we can compare with your existing listings during migration" |
| Operations defaults | Standard SMB defaults (3-hour cleaning window, 11 AM check-out) | Pre-populated from migration data import where possible; explicit "we'll review during migration" copy |
| Optional prep step ordering | Logo, Booking Engine, Guesty Pay first | Historical Data, Owner Prep first |

**Prototype requirements:**
- All five preset tiles must be visible and clickable
- At least two presets (Fast Launch and Migrate Existing Operations) must demonstrate visibly different downstream flows
- The other three presets may share a stub flow with a "preset variation TBD" label, but their selection must visibly persist to the readiness view and change the wizard's headline copy
- Selection state is saved before advancing
- A clear "you selected: [preset name]" recap appears at the top of every subsequent step
- Copy at the top of the screen makes the consequence explicit: *"Your answer changes what we show next."*

#### 7.1.5 Intent Selection — Acceptance Criteria

In addition to the universal criteria (Section 7.0.0), this screen must pass:

- All five launch paths are visible without scrolling
- Only one launch path can be selected at a time (radio behavior)
- Continue is disabled until a launch path is selected
- The selected path persists in `wizard.activePreset` and is shown as a recap on every later step
- Fast Launch and Migrate Existing Operations visibly change downstream flow (Migration Gate default, Airbnb Sync framing, Operations defaults — at minimum)
- The customer can change the launch path before completing Migration Gate without warning
- Changing the launch path **after** completing later steps shows a confirmation modal warning that already-completed configuration may be revisited

---

### 7.2 Step 2 — Migration Gate

**Purpose:** Branch the path based on whether the customer is starting fresh or migrating existing operations. Surface migration-related blockers and SLA risk *before* configuration starts — not on day 15 when they've discovered them mid-process.

#### 7.2.1 Layout

| Element | Spec |
|---------|------|
| Step label in sidebar | "Tell us about your starting point" |
| Headline | "Are you starting fresh or migrating existing operations?" |
| Sub-copy | "Your answer shapes what we set up next — and we'll flag anything that needs your specialist's help before you go live." |
| Selection format | Two large tile cards (Fresh / Migrating); selecting "Migrating" reveals follow-up sub-questions |

#### 7.2.2 Migration sub-questions (revealed if "Migrating" is selected)

| Question | Options | Path implication |
|----------|---------|-----------------|
| "What are you bringing over?" (multi-select) | Listings only · Listings + reservations · Accounting / payment history · Owner records · From another PMS | Each selection adds visible items to a "things we'll handle in your migration" summary |
| "When do you want to be live?" | Within 2 weeks · 2–4 weeks · 4+ weeks · Not sure | If "Within 2 weeks" + complex migration → SLA risk warning shown |
| "Are you currently taking bookings?" | Yes, on Airbnb · Yes, on multiple channels · No, not yet | Drives the dual-running plan — calendar safety, double-booking prevention |

#### 7.2.3 SLA risk and CSM-validation flags

For migration paths that combine high complexity with tight timelines, the wizard surfaces explicit warnings before allowing the customer to proceed:

| Combination | Surface |
|------------|--------|
| Listings + reservations migration | "Your specialist will validate calendar integrity before you go live — there's a check on Call 1 to prevent double-bookings." |
| Accounting / payment history migration | "Specialist review required. We'll capture your accounting structure now, but final approval happens with your specialist." Flag set: `requires_csm_validation: true`. |
| From another PMS + within 2 weeks | "Heads up — moving from another PMS in 2 weeks is fast. Your specialist may suggest a 3-week timeline. We'll discuss this in your first session." |

#### 7.2.4 Completion state

| Element | Spec |
|---------|------|
| Summary card | "Got it. Here's what we're handling in your launch:" + bulleted list of migration items + CSM validation flags |
| Path indicator | "Path: Migrating Existing Operations · 3 listings · 12 active reservations · accounting flagged for specialist review" |
| Primary CTA | "Continue to Airbnb sync →" |

**Prototype requirements:**
- Both branches (Fresh, Migrating) must be clickable and produce visibly different downstream flows
- The migration sub-questions must reveal smoothly when "Migrating" is selected (no full page reload)
- At least one CSM-validation flag must be triggered and shown in the completion summary
- The selection persists to the sidebar's readiness view (e.g., affects the "Listings" readiness state)
- For the Fresh path, the SLA warning section is hidden and the completion state is simpler

#### 7.2.5 Migration Gate V1 Boundary (critical scope guardrail)

The Migration Gate is a **risk detector and capture screen**, not a migration product. The V1 boundary is hard:

**The V1 Migration Gate does three things:**

1. Captures whether the customer is starting fresh or migrating
2. Identifies migration complexity (multi-select items + timeline + current channels)
3. Creates Call 1 review flags when complexity is high

**The V1 Migration Gate explicitly does NOT:**

- Migrate from another PMS (no API integration with competitor PMSes)
- Import accounting history
- Resolve reservation conflicts or calendar overlaps
- Validate full calendar integrity
- Promise a specific go-live timeline
- Complete historical data migration
- Generate an automated migration plan

**Required framing copy at the top of the screen:**

> "We'll capture what you're bringing over now, so your specialist can validate the right migration path on Call 1. Complex migration items are not completed in this wizard."

This copy must be visible (not hidden behind a tooltip or a "learn more"). It protects V1 from overpromising and protects the customer from the "I thought the wizard migrated my account" failure mode.

**Required warning copy (when complex migration + tight timeline):**

> "Heads up: this is a fast timeline for a migration. We'll flag this for your specialist so you can avoid calendar or reservation issues."

#### 7.2.6 Migration Gate — Acceptance Criteria

In addition to the universal criteria (Section 7.0.0), this screen must pass:

- The "Fresh" and "Migrating" cards are visible and clickable
- Continue is disabled until either is selected
- Selecting "Migrating" smoothly reveals the three sub-questions (no full page reload)
- At least one selectable migration combination produces a CSM-validation flag visible in the completion summary
- The completion summary lists every selected migration item in plain language
- The framing copy ("Complex migration items are not completed in this wizard") is visible above the fold
- For migration + tight timeline combinations, the warning copy appears before the customer can proceed
- The selection writes to `wizard.migrationMode`, `migrationItems`, `targetGoLiveWindow`, `currentBookingChannels`, and (where applicable) appends to `reviewFlags`

---

### 7.3 Step 3 — Airbnb View-Only Sync

**Purpose:** The AHA moment. Transform an empty platform into a mirror of the customer's real business. Establish trust. Framing of this step adapts based on the active preset (Step 1) and migration mode (Step 2) — e.g., for `migrate_existing` paths, the headline becomes "Connect Airbnb so we can compare with your existing listings."

#### 7.3.1 Pre-connect state

| Element | Spec |
|---------|------|
| Step label in sidebar | "Connect Airbnb" with a "🔑 Start here" badge |
| Headline | "See your Airbnb listings inside Guesty — in seconds" (preset-adaptive) |
| Safety block (prominent, above CTA) | Icon + "No impact on your Airbnb account. Nothing changes on your listings, pricing, or calendar. This is a read-only import — you're in full control." |
| Preview widget | Three greyed-out cards labeled "Your listing", "Your calendar", "Your inbox" — showing blurred placeholder UI to convey what will appear after sync |
| What you'll see block | "After connecting, your Guesty account will show: all your Airbnb listings, your next 90 days of bookings, your guest messages" |
| Primary CTA | "Connect Airbnb" (launches OAuth flow simulation) |
| Secondary link | "I'll do this later" (marks step incomplete, advances to step 4) |

#### 7.3.2 OAuth flow (simulated in prototype)

| Screen | Content |
|--------|---------|
| OAuth modal / redirect | Airbnb branding, "Guesty is requesting access to view your listings and reservations. No changes will be made to your Airbnb account." |
| Permissions listed | "View listings · View reservations · View messages" — nothing write-related |
| Loading state | "Importing your listings…" progress animation, 2–3 second delay |

#### 7.3.3 Post-connect success state (the AHA moment)

This is the most important screen in the prototype. Must convey transformation.

| Element | Spec |
|---------|------|
| Animation | The three blurred placeholder cards from the pre-connect state "reveal" with a smooth fade-in, populating with real listing data |
| Listing cards | Show 2–3 representative listings from the mock dataset (property name, photo, city, active/inactive badge) |
| Calendar widget | Mini calendar showing the next 2–3 bookings, guest names, check-in/check-out dates |
| Inbox widget | 2–3 mock guest messages with guest names and message previews |
| Headline | "Your business is now in Guesty" |
| Sub-copy | "These are your real listings, bookings, and messages — synced from Airbnb. Nothing on Airbnb has changed." |
| Confirmation badge | ✓ "Airbnb connected (view only)" |
| Readiness impact | The readiness view in the sidebar visibly updates — Listings: Ready, Channels: Ready (or At risk if migration paths require additional channels) |
| Primary CTA | "Continue →" |

#### 7.3.4 Error / connection failure state

| Element | Spec |
|---------|------|
| Error message | "We couldn't connect to your Airbnb account. This sometimes happens if the connection was cancelled or timed out." |
| Actions | "Try again" + "I'll do this in my first session" |
| Safety reminder | Repeat the no-risk framing so the customer doesn't fear they caused damage |

**Prototype requirements:**
- Both the pre-connect and post-connect states must be fully clickable
- The "reveal" animation is required — this is the AHA moment
- At least one error state must be shown
- The sidebar must update to show "✓ Airbnb Connected" after completion
- The readiness view in the sidebar must visibly flip Listings (and Channels, where appropriate) to Ready

#### 7.3.5 Airbnb AHA Moment Requirements (the most important sequence in the prototype)

This is the single most important screen sequence in the entire prototype. Make it impossible to under-design. The success state must show a **visible before/after transformation**.

**Required safety copy (verbatim, above the connect CTA):**

> "Nothing changes on Airbnb. We can only view your listings, reservations, and messages. We cannot change your pricing, calendar, availability, or listing content from this step."

**Required success headline:** "Your business is now in Guesty"

**Required success sub-copy:** "Your listings, upcoming bookings, and recent guest messages are now visible here. Airbnb has not been changed."

**Three-state sequence the prototype must implement:**

| State | Required content |
|-------|-----------------|
| **Before sync** | Empty or blurred listing cards · Empty calendar preview · Empty inbox preview · Safety block above CTA · Clear "view-only" language |
| **During sync** | Simulated OAuth · Loading state ("Importing your Airbnb listings…") · Optional progress messages: "Reading your listings" / "Importing upcoming reservations" / "Loading guest messages" |
| **After sync** | 2–3 listing cards appear with images and names · Calendar preview shows upcoming bookings · Inbox preview shows guest messages · Confirmation badge: "Airbnb connected · view only" · Required headline and sub-copy above |

**Mandatory visual effect:** The prototype must include a reveal animation or a clear transition from empty state to populated state. This is **not decorative**. It is the proof point that the cold-start resolution promise — the entire reason the wizard exists — is real.

**Critical framing distinction (important for the prototype and for the specialist handoff):**

Airbnb sync is the activation gate, but it is **not** the full definition of onboarding readiness. A customer who completes Airbnb sync is not necessarily ready to go live — they are **no longer starting from zero**. The prototype's copy and completion states must reflect this precisely: the success state says "your business is now in Guesty" (cold-start resolved), not "you're ready to go live."

This distinction protects against over-claiming in the UX and sets the right expectation for the specialist review on Call 1.

#### 7.3.6 Airbnb Sync — Acceptance Criteria

In addition to the universal criteria (Section 7.0.0), this screen must pass:

- The customer sees the safety copy *before* the connect CTA — not after, not in a tooltip
- The safety copy explicitly says nothing changes on Airbnb
- The permission list shows: view listings, view reservations, view messages — and nothing write-related
- The OAuth flow is simulated end-to-end (modal/redirect, permission grant, return)
- The loading state lasts long enough (2–3 seconds) to feel like an import is happening, not a toggle
- The success state reveals listings, calendar, and inbox via animation or transition (not instant swap)
- The success state headline is exactly "Your business is now in Guesty"
- The sidebar marks Airbnb Sync complete
- `airbnb.connectionStatus = "connected"`, `listingsImported / bookingsImported / messagesImported` populated
- `readiness.listings` changes to **Ready**
- `readiness.channels` changes to **Ready** (Path A) or **At risk** (Path B)
- An error state exists and is reachable from the prototype
- A skip path exists with the mandatory skip-confirmation copy from Section 6.8

---

### 7.4 Step 4 — Operations Setup

**Purpose:** Capture housekeeping, cleaning, and operational workflow preferences. Guesty pre-fills defaults; customer confirms or edits. Defaults are shaped by the active preset (Step 1).

#### 7.4.1 Layout pattern: Question → Default → Confirm/Edit

Each operations configuration item follows the same interaction pattern:

```
┌─────────────────────────────────────────────────────┐
│  [Question / topic label]                            │
│                                                      │
│  Guesty's recommendation:                            │
│  [Pre-filled default value] — [brief why this works] │
│                                                      │
│  [✓ Looks good]   [Edit]                            │
└─────────────────────────────────────────────────────┘
```

When the customer clicks "Edit", the field opens inline for editing. "Save" returns to the confirmed state.

#### 7.4.2 Operations questions (MVP)

| # | Question | Guesty Default | Notes |
|---|----------|---------------|-------|
| 1 | Do you use a housekeeping team or manage cleaning yourself? | "I manage cleaning myself" | Triggers different downstream config |
| 2 | How long is your standard cleaning window between check-out and next check-in? | "3 hours" | Applied as default buffer block |
| 3 | Do you require a property inspection after cleaning? | "Yes — auto-scheduled after each clean" | Best practice default |
| 4 | What is your standard minimum stay? | "2 nights" | Editable per listing later |
| 5 | What is your check-in window? | "3:00 PM – 8:00 PM" | Editable per listing later |
| 6 | What is your check-out time? | "11:00 AM" | Editable per listing later |

#### 7.4.3 Section completion state

After all questions are confirmed or edited:

| Element | Spec |
|---------|------|
| Summary card (Alone + OB Review pattern) | **"Saved. Your specialist will review these operational settings with you on Call 1."** |
| What happens next | "These settings apply to all your listings. You can fine-tune per-listing settings after your first call." |
| Readiness impact | The sidebar's readiness view updates: this step does not yet flip a domain to "Ready" — Operations contributes to the Listings domain readiness, which becomes Ready after Operations + Airbnb Sync + at least one listing-level action complete |
| CTA | "Continue →" |

The completion copy must use the Alone + OB Review pattern from Section 8.8 — the customer's input is a starting point for the specialist's review, not a final decision. This framing reduces "did I do this right?" anxiety.

**Prototype requirements:**
- All 6 questions must be shown with pre-filled defaults
- At least 2 questions must show the edit interaction (field opens inline)
- Completion summary must appear after all questions are confirmed
- Sidebar step must update to "✓ Operations" on completion
- The readiness view in the sidebar must visibly update at least one domain state when Operations completes

---

### 7.5 Step 5 — Financials Setup

**Purpose:** Configure fees, cancellation policy, revenue calculation, and payment automation. Revenue safety is the primary framing. Guesty pre-fills SMB-segment defaults shaped by the active preset.

#### 7.5.1 Framing

| Element | Spec |
|---------|------|
| Section headline | "Protect your revenue from day one" |
| Contextual copy | "Getting financials right before your first booking means you don't lose money to missing taxes or fees. We've pre-configured the most common settings for a property manager like you — confirm or adjust below." |

#### 7.5.2 Sub-sections

**A. Additional Fees**

| Element | Spec |
|---------|------|
| Copy | "Guesty supports 200+ fee types. Here are the 4 most common for property managers your size:" |
| Default fees shown | Cleaning fee, Pet fee, Late check-out fee, Security deposit |
| Interaction | Each fee row: toggle on/off + editable amount field. Additional link: "See all fee types" (opens drawer, out of scope for prototype MVP) |
| Default values | Cleaning: $150, Pet: $75, Late checkout: $50, Security deposit: $500 |

**B. Cancellation Policy**

| Element | Spec |
|---------|------|
| Options | Flexible / Moderate / Strict / Super Strict (radio select) |
| Guesty default | Moderate (pre-selected) |
| Context copy | "Moderate cancellation gives guests flexibility while protecting your revenue. Most Airbnb operators in your segment use Moderate." |
| Policy detail | Each option shows a one-line summary of its terms |

**C. Revenue Calculation**

| Element | Spec |
|---------|------|
| Options | "Owner Revenue" vs "Gross Revenue" (toggle/radio) |
| Guesty default | Owner Revenue (pre-selected) |
| Context copy | "Owner Revenue is the standard for property managers who remit earnings to owners. Gross Revenue is more common for owner-operators who keep all revenue." |

**D. Payment Automation**

| Element | Spec |
|---------|------|
| Options | 100% on confirmation / 50% on confirmation + 50% 7 days before check-in / Custom |
| Guesty default | 100% on confirmation (pre-selected) |
| Context copy | "100% collect on confirmation is the most common setting for short-term rental operators and reduces no-show risk." |

#### 7.5.3 Tax Setup

| Element | Spec |
|---------|------|
| Framing | "Do you collect occupancy or lodging tax from guests?" |
| Options | Yes / No / I'm not sure |
| If "Yes" | Show a simple tax name + % rate input. Default: "Occupancy Tax · 10%" |
| If "Not sure" | "No problem — your specialist can help you get this right in your first session. We'll flag this as a topic for your call." |

#### 7.5.4 Section completion state

| Element | Spec |
|---------|------|
| Summary card (Alone + OB Review pattern) | **"Saved. Your specialist will validate these financial settings with you on Call 1."** |
| Configured summary | Bullet list of what was set: fees selected, cancellation policy, payment automation rule |
| Tax review-flag copy (if "I'm not sure" was selected) | "We'll flag your tax setup for your specialist." |
| Readiness impact | The Financial setup domain in the readiness view flips from "Not started" to "Needs review" (or "Ready" if no specialist-required flags are present) |
| CTA | "Continue →" |

**Prototype requirements:**
- All four sub-sections must be fully interactive
- Pre-filled defaults must be visible before any customer interaction
- The "See all fee types" link can show a placeholder drawer or be a static callout
- Tax "Not sure" path must show the call-flag state
- Sidebar updates to "✓ Financials" on completion
- The Financial setup domain in the readiness view must visibly update

---

### 7.6 Step 6 — Governance Capture (lightweight)

**Purpose:** Establish a governance record on the account — who owns admin, who owns financials, who approves go-live. For SMB this is often one person, but the *explicit declaration* is the V1 deliverable. Without it, the CSM has no governance handoff record at graduation.

**Critical UX principle:** The default path must assume **one owner-operator**. Avoid making SMB customers feel like they are doing enterprise admin work. The three-slot detailed layout is the secondary path, surfaced only on user request.

#### 7.6.1 Framing

| Element | Spec |
|---------|------|
| Section headline | "Who's running this account?" |
| Sub-copy | "For most accounts your size, this is just you. We capture it once so your specialist knows who owns setup decisions." |

#### 7.6.2 Required layout (primary path)

The screen must lead with a single, prominent decision card — not a three-field form.

```
┌─────────────────────────────────────────────────────┐
│  I'm the admin, financials owner, and go-live      │
│  approver.                                          │
│                                                      │
│  [ I'm all three ]   ← primary CTA                  │
│                                                      │
│  Add different people →   ← secondary link          │
└─────────────────────────────────────────────────────┘
```

**Behavior:**

- Clicking **"I'm all three"** fills all three owner slots (`owners.admin`, `owners.financialsOwner`, `owners.goLiveApprover`) with the registered user's name and email in one click — no form to complete
- The three separate fields are **only expanded** if the user clicks the secondary "Add different people" link
- `governanceRoleCollapse` is set to `true` for the fast path, `false` for the multi-person path

#### 7.6.3 Secondary path (multi-person)

When the customer clicks "Add different people," the three-slot layout expands inline:

| Slot | What it controls | Field type | Default behaviour |
|------|----------------|-----------|-------------------|
| **Admin** | Who has full account access and can invite other users | Name + email | Pre-filled with registered user |
| **Financials owner** | Contact for financial questions, statements, accounting | Name + email | Pre-filled with registered user; "Same as admin" toggle |
| **Go-live approver** | Person who signs off the account is ready for real bookings | Name + email | Pre-filled with registered user; "Same as admin" toggle |

Customer can fill these independently or use the per-slot "Same as admin" toggle.

#### 7.6.4 Section completion state

| Element | Spec |
|---------|------|
| Summary card (Alone pattern) | **"Got it. Your specialist will know who owns setup decisions."** |
| Owners recap | Visible list of the three roles → name(s) (collapsed to "All three: Sarah Cohen" for the fast path; expanded list for multi-person) |
| Readiness impact | `readiness.teamAccess = "ready"` — the Team access domain flips to **Ready** in the sidebar |
| CTA | "Continue →" |

#### 7.6.5 Governance Capture — Acceptance Criteria

In addition to the universal criteria (Section 7.0.0), this screen must pass:

- The "I'm all three" primary card is the most prominent element on the screen
- Clicking "I'm all three" populates all three `owners` slots and advances state without showing the multi-person form
- The "Add different people" secondary link is discoverable but visually subordinate
- The multi-person form expands inline (no full page reload) when the secondary link is clicked
- `governanceRoleCollapse` is set correctly based on which path is taken
- Completion flips `readiness.teamAccess` to **Ready**
- The captured values persist and appear on the Readiness Summary screen (Section 7.11) in the Governance summary section

---

### 7.7 Step 7 — Rocketlane + Docebo Orientation

**Purpose:** Familiarize the customer with supporting systems so they know where to find help between sessions. This is an orientation checkpoint, **not a task list and not training**.

#### 7.7.0 Rocketlane + Docebo role in V1 (explicit scope)

Rocketlane and Docebo are **not the pre-Call-1 task surface for SMB V1**. The wizard owns pre-Call-1 action. The orientation step exists only so customers know where these tools live for **later reference**, especially after Call 1.

**UX requirements (non-negotiable):**

- Orientation must be **lightweight** — not a project plan walkthrough
- **No long training content**, no embedded videos that auto-play
- **No mandatory video watching** — clicking "See the Academy" is acknowledgement, not video completion
- **No deep project plan** — clicking "Take a look" shows a static placeholder, not an editable task surface
- Two simple cards are enough — never more
- Each card requires only a click-through acknowledgement

This protects the wizard's role as the primary action surface. If Rocketlane or Docebo become prominent here, the customer will treat them as the next step instead of moving forward in the wizard.

#### 7.7.1 Layout

Two side-by-side cards (or sequential reveals):

**Rocketlane card:**
| Element | Spec |
|---------|------|
| Logo / brand mark | Rocketlane |
| Headline | "Your onboarding project plan" |
| Copy | "After your first session, your specialist may add tailored tasks here. You don't need to manage this before Call 1." |
| CTA | "Take a look →" (opens a simulated Rocketlane project view in a modal or side drawer — a simplified placeholder screenshot) |
| Completion trigger | Customer must click "Take a look" to mark this as seen |

**Docebo card:**
| Element | Spec |
|---------|------|
| Logo / brand mark | Docebo / Guesty Academy |
| Headline | "Self-serve training videos" |
| Copy | "Guesty Academy has training videos for later. It is most useful once your account is already set up." |
| CTA | "See the Academy →" (opens a simulated Docebo landing in modal or side drawer) |
| Completion trigger | Customer must click "See the Academy" to mark this as seen |

#### 7.7.2 Completion state

| Element | Spec |
|---------|------|
| Confirmation | "You know where to find help between sessions." |
| CTA | "Continue →" |

**Prototype requirements:**
- Both "Take a look" and "See the Academy" links must open something (modal, drawer, or external tab to a placeholder) — the click must be tracked to mark the step complete
- Sidebar updates to "✓ Orientation" on completion
- Neither card must visually compete with the wizard's primary suggested steps in size, color, or position

---

### 7.8 Step 8 — Interesting Features

**Purpose:** Customer selects which Guesty features are most relevant to their business. Output is used by the OB specialist to personalize Call 1 agenda. Make the selection feel **explicitly useful** — not a survey, but a way to direct the first session.

**Required framing copy at the top of the screen:**

> "Pick what you care about most. Your specialist will use this to focus your first session."

#### 7.8.1 Layout: Selection grid

A grid of feature tiles (6–8 options), each with an icon, feature name, and one-line value description. Customer can select multiple.

| Feature | Icon | Value copy |
|---------|------|-----------|
| Channel Management | 🔗 | "Sync listings across Airbnb, Booking.com, Vrbo" |
| Automated Messaging | 💬 | "Send guests the right message at the right time — automatically" |
| Revenue Management | 📈 | "Optimize your nightly rates based on demand" |
| Booking Engine | 🖥️ | "Accept direct bookings with your own website" |
| Owner Portal | 👤 | "Give property owners a view of their performance and statements" |
| Payment Processing | 💳 | "Collect payments directly through Guesty" |
| Reporting & Analytics | 📊 | "Track performance across all your properties" |
| Guest Experience | ⭐ | "Automate reviews, digital check-in, and the Guest App" |

| Interaction | Behavior |
|------------|---------|
| Tile select | Click toggles selection (highlighted state); minimum 1 required |
| "Why does this matter?" | Optional tooltip or info icon on each tile explaining how this shapes the Call 1 agenda |
| Selection summary | "You've selected X features. Your specialist will cover these first in your session." |

#### 7.8.2 Completion state

| Element | Spec |
|---------|------|
| Headline | "Your setup path is personalized" |
| Summary (Alone pattern) | **"Saved. Your specialist will focus on: [list of selected features]."** |
| CTA | "Continue →" |

**Prototype requirements:**
- Minimum 1 feature should be selected to continue; if the customer skips without selecting, a gentle prompt is shown ("Selecting at least one helps us personalize your first session") but the step is skippable
- At least 3 tiles must have a clickable tooltip/info state
- Selection summary must update dynamically as selections change
- Selected features must persist into `featuresSelected` and appear in the V1 Specialist Handoff Output (Section 7.11) as part of the recommended Call 1 focus

---

### 7.9 Suggested Path Completion + Additional Prep Unlock

**Purpose:** Bridge between the suggested path and additional prep. Celebrate completion, explain what unlocks, and create optional motivation to do more prep.

#### 7.9.1 Completion screen

| Element | Spec |
|---------|------|
| Headline | "You're ready for your first session" |
| Sub-copy | "You've completed the recommended setup. Your specialist can now review your configuration and focus on the details that matter most to your business." |
| What was completed | Collapsed summary list of completed suggested steps (Intent Selection, Migration Gate, Airbnb Sync, Operations, Financials, Governance, Orientation, Features) with a checkmark each |
| Call reminder | Prominent card: "Your setup call with [Specialist Name] is on [Date] at [Time]" — CTA "Add to calendar" |
| Optional prep invitation | "Want to get even more out of your first session? Complete these optional steps to get a head start:" — shows the 6 optional step tiles in a card grid |
| CTA for optional | "Keep going →" (scrolls to or navigates to optional prep section) |
| CTA for readiness review | "See your readiness summary →" (navigates to step 7.11 Readiness Summary) |
| CTA to exit | "Enter Guesty →" (exits wizard to platform via 7.12 Platform Transition) |

**Prototype requirements:**
- All three CTAs ("Keep going", "See your readiness summary", "Enter Guesty") must be functional
- The platform entry state must show the populated homepage (not an empty state) — this is critical for the prototype
- Optional steps unlock in the sidebar simultaneously when this screen renders

---

### 7.10 Optional Prep Steps — Overview

#### 7.10.0 Additional Prep Scope (V1 boundary)

Additional prep is **secondary**. It must not visually compete with the suggested pre-Call-1 path. The customer's clearest path to "Ready for Call 1" is the suggested track — additional prep is "get ahead," not required.

**Additional prep rules (the prototype must enforce these):**

- Additional prep unlocks after the suggested path steps are complete (`wizard.additionalPrepUnlocked = true`); however, platform entry is never blocked
- Additional prep is framed as "get ahead of your specialist" — never "required" or "complete your setup"
- Additional prep can be skipped without creating any blockers or review flags
- Additional prep should **never** delay platform handoff — the "Enter Guesty" CTA must remain visible at all times
- Additional prep is **not** required for "Ready for Call 1" (Section 3.5)

**V1 build scope for optional steps:**

The prototype must show **all optional steps in the sidebar** so stakeholders can see the full intended scope, but it must fully build only the **two highest-priority optional interactions**:

1. **Booking Engine basics** (Section 7.10.1)
2. **Owner Prep / bulk upload** (Section 7.10.2)

The remaining optional steps (Logo Upload, Rate Strategy, Guesty Pay, Historical Data) can be represented with lighter interaction states — a placeholder screen with the entry copy and a "saved" stub — unless full fidelity is needed for a specific stakeholder demo.

This priority is intentional: the prototype's core hypothesis is **Airbnb sync + Call 1 readiness**, not "the customer also did six optional prep tasks." Building all six optional steps to full fidelity dilutes attention away from the AHA moment and the readiness view.

#### 7.10.0.1 Pattern shared by all optional steps

All additional prep steps follow the same interaction pattern as suggested steps (pre-filled defaults + confirm/edit). Each step includes:

- A "Why do this now?" one-liner
- Pre-filled defaults where applicable
- An explicit "I'll do this later" skip option
- A completion state that confirms what was saved

Detailed specs below for the two highest-priority optional steps. Remaining steps follow the same pattern at lighter fidelity.

---

### 7.10.1 Optional Step 9 — Booking Engine Setup

| Element | Spec |
|---------|------|
| Entry copy | "Set up your direct booking channel before your first session — and your specialist can review it during the call." |
| Questions | Do you have a website? (Y/N) · What's your direct booking domain? · Do you want to require guests to log in? |
| Defaults | No website (most common for this segment) · Login not required |
| Completion | "Your booking engine basics are saved. Your specialist will help you activate it in your first session." |

---

### 7.10.2 Optional Step 10 — Owner Prep (Bulk Upload)

| Element | Spec |
|---------|------|
| Entry copy | "Add your property owners to Guesty now — so your account is ready to show them statements and reports when you go live." |
| Safety block (verbatim) | **"No owner invitations are sent. You're only saving owner records so they are ready later."** |
| Upload interaction | CSV template download link + file upload area |
| Upload success state | "X owners added. No invitations have been sent." (Alone pattern — this is a final action; no specialist review needed) |
| Skip option | "I'll add owners later" |

---

### 7.11 Readiness Summary Screen

**Purpose:** Show the customer a per-domain operational readiness view of the account before platform handoff. This screen is the primary V1 manifestation of the Five Core Objects — Pilot scope, Milestones touched, Blockers (if any), Owners, and Readiness gates — collapsed into a customer-friendly readout. This is what replaces "X% complete" as the wizard's value layer.

**Critical framing:** Make this screen **operational, not motivational.** No celebratory "100% complete" headlines, no generic congratulations. The customer is being prepared for a review, not awarded a badge.

#### 7.11.1 Required sections (six, in this order)

The Readiness Summary screen must contain these six sections, in this order:

1. **Pilot scope** (small framed card at the top)
2. **Readiness domains** (per-domain table)
3. **Review flags / blockers** (active items captured during the wizard)
4. **Governance summary** (the three-slot owners record)
5. **Recommended Call 1 focus** — the V1 Specialist Handoff Output (Section 7.11.5)
6. **CTA to enter Guesty**

The screen must explicitly **avoid**:

- "100% complete" framing
- Generic celebration without operational detail
- Implying go-live readiness (the Section 3.5 distinction must hold)

#### 7.11.2 Layout

| Element | Spec |
|---------|------|
| Headline | "Here's where your account stands" |
| Sub-copy | "This is what your specialist will review with you on Call 1. Anything marked 'Needs review' or 'At risk' is what your call will focus on." |
| Pilot scope card | "Your pilot launch: [N] listings · [Channel] · [Payment method]" — derived from `wizard.activePreset`, `airbnb`, and `readiness.payments` |
| Readiness table | Per-domain rows with status indicator and one-line description (see 7.11.3) |
| Review flags panel | A list of active items from `reviewFlags`, each with a short label and a "your specialist will help with this on Call 1" note |
| Governance summary | "Account governance: Admin: [name] · Financials: [name] · Go-live approval: [name]" — from `owners` (collapsed to "All three: [name]" when `governanceRoleCollapse === true`) |
| Recommended Call 1 focus | The V1 Specialist Handoff Output (Section 7.11.5) — "What your specialist will review" |
| Primary CTA | "I'm ready — enter Guesty →" |

#### 7.11.3 Readiness domains (V1)

| Domain | Legal states | Derived from |
|--------|-------------|-------------|
| Listings | Ready / At risk | Airbnb sync complete + at least 1 listing imported (Ready); skipped (At risk) |
| Channels | Ready / At risk | Airbnb sync complete (Ready); migration path with multi-channel intent (At risk until Call 1) |
| Payments | Not started / In progress / Ready | GuestyPay optional step state |
| Financial setup | Not started / Needs review / Ready / At risk | Step 5 completion + presence of `reviewFlags` (e.g., `tax_setup_unsure`) |
| Team access | Not started / Ready | Step 6 (Governance Capture) complete |
| (V2 only) SLA risk, Customer activity | hidden in customer view | Surfaces in CSM Review mode in V2 |

The status icons are limited to the five states from Section 8.6: ✓ Ready · ! At risk · ◐ In progress · ⚠ Needs review · ○ Not started. **No progress percentages**.

#### 7.11.4 Customer-facing copy framing

The readiness view must speak in operational language, not setup-completion language. Good examples:

| Bad copy | Good copy |
|---------|----------|
| "Operations: 100% complete" | "Operations: Ready. Your cleaning windows, check-in/out, and inspection workflow are configured." |
| "Financials: 80% complete" | "Financials: Needs review. Your specialist will validate the tax setup with you on Call 1." |
| "Channels: 50% complete" | "Channels: At risk. You have one channel connected. Your specialist will help you connect Booking.com and Vrbo." |

#### 7.11.5 V1 Specialist Handoff Output (the "What your specialist will review" section)

Even though CSM Review mode is out of scope for the V1 prototype build, the prototype **must generate a basic Call 1 prep summary**. This is the bridge that connects the wizard to the specialist's Call 1 workflow. Without it, the wizard is disconnected from the specialist; with it, even a V1 build proves the wizard has handoff value.

This appears on the Readiness Summary screen as the **"What your specialist will review"** section.

**Handoff must include (these fields are required):**

- Customer name
- Company name
- Selected launch path (`wizard.activePreset`)
- Migration mode (`wizard.migrationMode`)
- Airbnb sync status + imported listing count
- Operations status
- Financial setup status
- Active review flags (full list)
- Governance owners (collapsed or expanded)
- Selected feature interests
- Recommended Call 1 focus (top 3 priorities, derived from review flags + selected features)

**"Specialist should know before the call" — recommended checklist:**

The handoff summary must make the following directly answerable from the readiness summary screen (the specialist must not have to navigate elsewhere to find them):

- Whether the account is starting fresh or migrating
- Whether Airbnb sync succeeded
- How many listings were imported
- Whether financials need review
- Whether the customer marked anything as "not sure"
- Which features the customer cares about most
- Whether any migration complexity was flagged

This list is the specialist's pre-call prep surface in V1. In V2, this becomes the input to CSM Review mode. The prototype must demonstrate that all seven items are **directly visible** on the Readiness Summary screen without expanding any panel or navigating away.

**Example output (Path A — Fast Launch, clean run):**

```
Call 1 Prep Summary
───────────────────
Customer:         Sarah Cohen
Company:          Urban Stay TLV
Launch path:      Fast Launch
Migration mode:   Starting fresh
Airbnb sync:      Complete · 12 listings imported · 4 bookings · 3 messages
Operations:       Ready
Financials:       Ready
Team access:      Ready
Owners:           Sarah Cohen (admin / financials / go-live approver)
Feature interests: Booking Engine, Automated Messaging

Recommended Call 1 focus:
1. Walk through the Booking Engine setup (selected feature interest)
2. Validate Operations defaults against actual properties
3. Confirm Automated Messaging templates
```

**Example output (Path B — Migration with flags):**

```
Call 1 Prep Summary
───────────────────
Customer:         Sarah Cohen
Company:          Urban Stay TLV
Launch path:      Migrate Existing Operations
Migration mode:   Migrating · listings + reservations · from another PMS · within 2 weeks
Airbnb sync:      Complete · 12 listings imported
Operations:       Complete (review needed against existing rules)
Financials:       Needs review · tax setup marked "I'm not sure"
Team access:      Ready · Sarah Cohen (admin / financials / go-live approver)
Feature interests: Booking Engine, GuestyPay, Automated Messaging

Active review flags:
• migration_complexity_high
• migration_timeline_tight
• tax_setup_unsure

Recommended Call 1 focus:
1. Validate the migration plan and timeline
2. Resolve tax setup uncertainty
3. Confirm Booking Engine and GuestyPay relevance for the migration cutover
```

The prototype must show **both example outputs** — one for each Required Prototype Path (Section 6.7) — so stakeholders can see how the handoff adapts to the customer's actual run.

#### 7.11.6 V1/V2 boundary

V1 ships only the customer-facing readiness view + V1 Specialist Handoff Output as specified above. The same data model must support V2's CSM-facing Review mode, which adds:

- **SLA risk** (e.g., "7 days until SLA breach")
- **Customer activity signal** (e.g., "Last active 5 days ago")
- **Operational diagnostic detail per domain** (e.g., "Channel connection: Airbnb OAuth granted; Booking.com pending; customer hasn't responded to credentials request")

The V1 prototype must demonstrate that the customer-facing view is a *simplified projection* of a richer underlying state — not a separate data model. This is achieved by:

- Storing per-domain readiness state explicitly (not deriving it on the fly from a global progress percentage)
- Storing blockers, owners, and active flags as structured records, not free-form notes
- Tagging each readiness state with the underlying source(s) so the CSM Review mode can expand it in V2

**Prototype requirements:**
- All five customer-facing readiness domains must be visible with at least three different status states across them (e.g., Ready, At risk, Needs review)
- The pilot scope card must accurately reflect the wizard's earlier selections (preset, Airbnb sync, optional GuestyPay)
- The governance summary must reflect the Step 6 capture (collapsed for solo operator, expanded for multi-person)
- At least one review flag entry must be shown (e.g., `tax_setup_unsure`) to demonstrate the review-flags panel
- Both Required Prototype Paths (Section 6.7) must produce a readable V1 Specialist Handoff Output
- The "I'm ready — enter Guesty →" CTA leads to the Platform Transition screen

---

### 7.12 Platform Transition Screen

**Purpose:** The exit from the wizard. The customer enters Guesty proper for the first time. This screen is the **final validation** of the cold-start resolution promise — the customer is not entering a blank product.

#### 7.12.1 Layout

| Element | Spec |
|---------|------|
| Headline | "Your account is ready for your first session" |
| Sub-copy | "Here's what's waiting for you inside Guesty:" |
| Preview tiles | Homepage (shows listing count), Calendar (shows bookings), Inbox (shows messages) — all populated with Airbnb sync data |
| Setup summary | "Completed before your call: Airbnb connected · Operations configured · Financials set · Governance captured · Features selected" |
| Call reminder (final) | "Your next session: [Date] · [Time] · [Specialist Name]" |
| (Path B only) Migration banner | A small banner: "Your specialist will validate your migration on Call 1." |
| Primary CTA | "Go to Guesty →" |

#### 7.12.2 Platform Handoff — Acceptance Criteria

In addition to the universal criteria (Section 7.0.0), this transition must pass:

**Required (must happen):**

- The handoff screen explicitly says what was completed before Call 1
- The handoff screen shows the next Call 1 reminder (date / time / specialist)
- Preview tiles show the homepage, calendar, and inbox **populated** (not empty)
- "Go to Guesty" leads to a **mocked Guesty homepage**
- The mocked Guesty homepage must include:
  - Visible listing count (matches `airbnb.listingsImported`)
  - **At least 2 listing cards** with images, names, and basic detail
  - A calendar view with upcoming reservations (from the Airbnb sync)
  - An inbox with guest messages
  - A visible confirmation that Airbnb is connected · view-only

**Must NOT happen:**

- The handoff must **not** lead to a blank dashboard
- The handoff must **not** show generic empty states ("No listings yet — get started!")
- The handoff must **not** reset the customer into another onboarding hub
- The handoff must **not** display a "100% complete" or "you're done" framing

This is the proof point that the wizard solved the cold-start problem. If the customer arrives at Guesty and sees an empty product, the entire wizard's value proposition collapses — the wizard becomes pointless instead of transformative.

---

## 8. UX & Interaction Requirements

### 8.0 Governing UX principles

These principles take precedence over any individual interaction requirement below. If a screen, copy choice, or interaction violates one of these, it should be reworked before being treated as final.

| Principle | What it means |
|-----------|--------------|
| **Scope before configure** | The first wizard screen (Intent Selection) sets the launch goal; the second (Migration Gate) sets the path complexity. No configuration step appears before these two are answered. This is the structural difference between a setup wizard and a guided implementation system. |
| **Editable infrastructure, not education content** | Every screen must result in a tangible configuration outcome. No tutorials, no walkthroughs of the platform, no "learn more about X" detours that don't write to the account. The single exception is the Rocketlane + Docebo orientation checkpoint, which is navigation acknowledgement only. |
| **Readiness, not progress** | The primary "where am I?" surface is the readiness view (per-domain Ready / At risk / Not started), not a progress percentage. A progress bar measures field touches; the readiness view measures launch viability. The first is a setup-wizard relic; the second is the implementation system's value layer. The prototype must lead with the readiness view. |
| **Confirm or edit, never fill from blank** | Every form-style step must arrive with Guesty's opinionated default already in place. The customer's primary action is "Looks good" or "Edit". A blank field is a UX failure — it forces the role-collapsed customer to invent structure the wizard should have provided. |
| **Safety framing is explicit, not implied** | Any step that involves a "connect", "import", or "upload" action must include a no-risk header block before the CTA, listing what will *not* happen. Implicit safety is not safety; the customer needs to read the assurance. |
| **Pilot scope, not full feature surface** | The wizard surfaces only what is needed to launch the bounded pilot (1–5 listings, 1 channel, core payments). Everything else is explicitly deferred to "later sessions" with a visible mention but a demoted CTA. The customer cannot wander into the full platform feature surface during the wizard. |
| **Hold momentum during the wait** | The wait between registration and Call 1 is the primary failure period. Every wizard exit point (between sections, on partial completion, at the end of optional prep) must offer a clear forward path or a clear resume hook. No interaction may dead-end the customer. |
| **The wizard is the checklist** | Customers in this segment build shadow Google Sheets to compensate for the missing checklist. The wizard's progress sidebar replaces those shadow systems — it must be visible, persistent, and unambiguously complete/incomplete per step. |
| **Same state, different views (V2-ready)** | The data model must support the V2 three-mode architecture (Setup / Review / Governance). V1 ships only Setup mode, but no V1 UI element should be derived from a representation that cannot extend to the other two modes. Concretely: the readiness view's customer-facing simplification must be a *projection* of richer underlying state, not a separate model. |

### 8.1 Design Language

| Requirement | Spec |
|------------|------|
| Design system | Guesty Nebula (or close approximation in prototype tooling) |
| Reference UX pattern | Monday.com onboarding wizard — full-screen, single-task-at-a-time, left sidebar progress. The CSM-guided build architecture: wizard = editable infrastructure, Call 1 = review layer, suggested/additional-prep split = pilot scope guidance |
| Typography | Guesty brand type stack |
| Color | Guesty brand palette; suggested steps in primary blue; additional prep steps in neutral grey |
| Icons | Nebula icon set |

### 8.2 Progress & Feedback Patterns

| Pattern | Requirement |
|---------|------------|
| Step completion | Sidebar step transitions from "○ In progress" → "✓ Completed" with animation |
| Section progress | Each multi-question section shows "X of Y questions answered" indicator |
| Suggested badge | All suggested steps show a small "Recommended before call" label in the sidebar |
| Additional prep badge | All additional prep steps show "Get ahead — optional" label |
| Call countdown | Top-right call reminder updates dynamically (e.g., "3 days to your session"). Visual urgency increases as the call approaches: neutral at >5 days, mild emphasis at 3–5 days, prominent at ≤2 days. |
| Save state | "Progress saved automatically" toast appears after each step completion |

### 8.2.1 Wait-conversion patterns (critical for V1 framing)

The wizard's primary job is to keep the customer engaged across the days between registration and Call 1. The prototype must demonstrate the following patterns that explicitly serve this:

| Pattern | Requirement |
|---------|------------|
| Persistent call reminder | Top-bar reminder is visible on every wizard screen — never collapsed, never dismissed |
| Returning-user resume flow | Customer returning after a session-break sees: "Welcome back, [Name]. You last completed [Step X]. [N days] until your call with [Specialist]. Continue from where you left off?" |
| "Finish before your call" prompt | When the customer reaches the optional prep section, surface contextual copy: "You have [N days] before your call. Most customers spend this time on [top 2 optional steps]." |
| Email re-engagement copy hook (referenced, not built) | The prototype's wizard exit screen and resume flow must include placeholder copy that mirrors what re-engagement emails will say between sessions — for stakeholder alignment on tone |
| No empty inter-section gaps | After completing any step, the next contextual CTA is always visible — no "click to continue" dead-ends, no decision-fatigue moments where the customer can stall |

### 8.3 Empty/Loading States

| State | Requirement |
|-------|------------|
| Airbnb connecting | Full-screen loading animation with copy: "Importing your listings from Airbnb…" |
| Airbnb connected | Success animation then reveal of populated widgets |
| Configuration saving | Inline spinner on CTA button; "Saving…" state |
| Returning user | "Welcome back. You last stopped at [step name]. Continue from there?" |

### 8.4 Safety Framing (Critical)

The following explicit safety patterns must appear at every step that involves a "connection" or "import" action:

1. **No-risk header block** — appears at the top of the action step before any CTA, with an icon and copy that explicitly states what will NOT happen (e.g., "Nothing on Airbnb changes")
2. **Permission list** — a list of exactly what Guesty is requesting access to do (read-only actions only)
3. **Undo/decouple link** — "You can disconnect Airbnb at any time from your account settings"

### 8.5 Copy Tone

| Principle | Example |
|-----------|---------|
| Opinionated and confident | "We've set this to Moderate — this is what works best for most property managers your size." |
| Risk-zero | "No impact on your Airbnb account." "No invitations are sent to owners." |
| Time-aware | "Most customers complete this in under 5 minutes." |
| Outcome-oriented | "Getting this right now means your first booking won't lose money." |
| First-person Guesty voice | "We've configured this for you." "We recommend…" |

### 8.6 Readiness view — the primary V1 UI primitive

The readiness view is the wizard's primary "where am I?" surface and a first-class UI element across multiple screens. It is not a single screen — it is a primitive that appears in three forms throughout the prototype.

| Surface | Role of the readiness view |
|---------|----------------------------|
| Sidebar (always visible) | Compact per-domain summary at the top of the left sidebar — five rows (Listings, Channels, Payments, Financial setup, Team access) with a small icon and a single state label |
| Step completion summaries | Each step's completion state explicitly references which readiness domain it impacts ("Listings is now Ready") so the customer can tie individual actions to operational outcomes |
| Readiness Summary screen (Step 7.11) | The full readiness view as a dedicated page — including the pilot scope card, blockers panel, and governance summary |

**State semantics (V1) — five states, operational meanings:**

The readiness view must use **operational states**, not progress percentages. There are five legal states; each has an icon, a precise meaning, an example trigger, and a customer-facing copy pattern.

| State | Icon | Meaning | Example trigger | Customer copy pattern |
|-------|------|--------|----------------|----------------------|
| Not started | ○ | No meaningful action has happened in this domain yet | Customer hasn't reached the step; GuestyPay never opened | "Not started. You can handle this later." |
| In progress | ◐ | The customer started but has not completed the domain | GuestyPay application started but not submitted | "In progress. Finish this before go-live." |
| Needs review | ⚠ | Customer-side input is complete, but specialist validation is expected | Financials completed, tax setup marked uncertain | "Needs review. Your specialist will validate this on Call 1." |
| At risk | ! | A known blocker or complexity may affect launch | Migrating from another PMS within 2 weeks; Airbnb sync skipped | "At risk. Your specialist will help resolve this." |
| Ready | ✓ | Enough has been completed for Call 1 review or pilot launch | Airbnb synced + listings imported; Operations confirmed | "Ready. This is configured for your first session." |

**Hard rules (the readiness view must obey these):**

- The readiness view must **not** show "100% complete" or any progress percentage as the primary state. A small secondary indicator is acceptable; a progress bar replacing the per-domain readout is not.
- Step completion does **not** automatically equal readiness. A domain only becomes Ready when the underlying account state — Airbnb sync done, Operations confirmed, no review flags blocking — supports it. (See Section 9.2.2 Required state behavior for the deterministic rules.)
- Readiness domains must be **derived** from underlying state (`airbnb`, `wizard`, `owners`, `reviewFlags`) — never set directly from a "step touched" boolean.
- The readiness view must be visible in **two places**: the wizard sidebar (compact, always visible) and the Readiness Summary screen (Section 7.11, full layout).
- The five states are the legal states. A sixth state cannot be invented in V1 without updating Section 9.2 first.

**What the readiness view must NOT show in V1:**

- SLA risk indicators (e.g., "7 days until breach")
- "Customer last active X days ago"
- Operational diagnostic detail (e.g., per-channel connection status with credentials)

These are V2 CSM-Review-mode additions. In V1 these data points may be *captured* (see Section 9.2) but must not be *surfaced* in the customer view.

**Anti-pattern: progress bar as primary surface.** A traditional "X% complete" progress bar may appear as a small secondary element (e.g., text under the readiness summary), but it must not be the primary "where am I?" surface. Progress bars measure field touches; the readiness view measures launch viability. Confusing the two is the failure mode this section exists to prevent.

### 8.7 Returning-User Resume Scenarios

The wizard's primary job is **holding the customer's momentum during the wait** between contract signing and Call 1. Returning-user states are not a polish detail — they are the core product. The prototype must demonstrate at least the first two scenarios below; ideally all five.

#### 8.7.1 Scenario 1 — Started but did not complete Airbnb sync

> "Welcome back. Connect Airbnb before your call so your account isn't empty when you meet your specialist."

| CTA | Action |
|-----|--------|
| **Primary** | "Connect Airbnb" — jumps directly to Step 3 (Airbnb Sync) |
| **Secondary** | "Continue where I left off" — resumes at `wizard.currentStep` |

This is the **highest-priority** returning-user state. Airbnb sync is the sole hard activation gate (Section 0.2), so a returning user without sync gets the most direct push to the AHA moment.

#### 8.7.2 Scenario 2 — Completed Airbnb sync but not Financials

> "Your listings are in Guesty. Next, protect your revenue by reviewing financial settings."

| CTA | Action |
|-----|--------|
| **Primary** | "Continue to Financials" — jumps to Step 5 |

The framing leans into revenue safety (matching the Financials section copy) and treats Airbnb sync as a baseline accomplishment, not a stopping point.

#### 8.7.3 Scenario 3 — Suggested path complete, additional prep not started

> "You're ready for Call 1. You have 3 days left if you want to get ahead."

| CTA | Action |
|-----|--------|
| **Primary** | "See optional prep" — opens the Optional Prep section |
| **Secondary** | "Enter Guesty" — bypasses optional prep, goes to Platform Handoff |

Note: this scenario must **not** force optional prep. The customer is already Ready for Call 1; optional prep is "get ahead," not gating.

#### 8.7.4 Scenario 4 — Call is within 48 hours

> "Your call is coming up. Completing a few more steps will help your specialist hit the ground running."

| CTA | Action |
|-----|--------|
| **Primary** | "Continue recommended setup" — jumps to next incomplete suggested step |
| **Secondary** | "Enter Guesty" — exits wizard to platform |

The countdown urgency increases as the call approaches; copy reflects this. (See Section 8.2.1 for the broader wait-conversion patterns.)

#### 8.7.5 Scenario 5 — No call booked

> "When you're ready, booking a session lets your specialist review what you've set up — but you can keep going now."

| CTA | Action |
|-----|--------|
| **Primary** | "Book Call 1" — opens the booking flow |
| **Secondary** | "Continue without booking" — resumes wizard or enters Guesty |

The no-call-booked prompt is a persistent soft recommendation, not a gate. Customers who have not booked receive automated reminder emails to schedule a session. The prompt should feel helpful, not alarming. Automated re-engagement emails handle follow-up for customers who do not respond to in-wizard prompts.

#### 8.7.6 Resume state requirements

- The prototype must implement at least **scenarios 1 and 2** end-to-end (these correspond to the most common drop-off points)
- The remaining three scenarios must be visible as static screens for stakeholder review
- Each scenario reads from the existing Core State Model (no separate "resume state" data structure)
- The "Continue where I left off" path always uses `wizard.currentStep` to determine the entry point

### 8.8 Alone vs. Alone + OB Review — Completion Copy Rules

The wizard has two interaction modes (Section 6.5). Each mode has a **distinct completion copy pattern** so the customer always knows whether their input is final or whether the specialist will review it. This dramatically reduces "did I do this right?" anxiety — the most common drop-off cause in self-serve flows.

#### 8.8.1 Alone steps

Use when the customer's action is final enough for now and the specialist is **not expected** to revisit it.

**Examples:** Airbnb Sync · Logo Upload · Owner Prep (bulk upload)

**Required completion copy pattern:**

> "Saved. This part is complete."

Variations are acceptable when the action is more specific (e.g., for Airbnb sync, "Your business is now in Guesty"), but the *underlying message* must be: this is done, no further action expected.

#### 8.8.2 Alone + OB Review steps

Use when the customer's input is a **starting point** that the specialist will review on the relevant call.

**Examples:** Operations · Financials · Booking Engine · Rate Strategy · Historical Data

**Required completion copy pattern (Call 1 review):**

> "Saved. Your specialist will review this with you on Call 1."

**Variant for steps reviewed in a later call:**

> "Saved. Your specialist will review this with you in your third session."

The variant must be used when the review timing is known. Otherwise, default to the Call 1 pattern.

#### 8.8.3 Review-flag copy

Use when the customer marks uncertainty (e.g., tax setup "I'm not sure"):

> "We'll flag this for your specialist."

This appears inline next to the field, *in addition to* the step's completion copy.

#### 8.8.4 Why this matters

The Alone vs. Alone+OB Review distinction is the explicit answer to one of the role-collapse failure modes: a solo SMB operator has no internal review chain. They cannot ask their colleague "is this right?" — the wizard must signal whether the input is *final* or *initial*. Without this signal, the customer either:
- treats every step as final (over-anxiety, abandonment), or
- treats every step as draft (no commitment, low-quality data)

The completion copy is the structural guidance that prevents both failure modes.

### 8.9 Copy System (V1 vocabulary rules)

The wizard's copy is part of the product. The following rules govern the entire wizard's tone and word choice. This is the **lexical guardrail** for the prototype builder.

#### 8.9.1 Use Call 1 readiness language

| Use | Avoid |
|-----|-------|
| "Get ready for your first session" | "Complete setup" |
| "Saved for your specialist to review" | "You're fully ready" |
| "We'll flag this for Call 1" | "You're done" |
| "Your account is no longer blank" | "100% complete" |
| "Your business is now visible inside Guesty" | "Launch now" |
| "This gives your specialist a starting point" | "Go live now" |

The right column language is forbidden in V1. It either implies completion ("done", "100%", "fully ready") or implies premature launch ("launch now", "go live now"). The wizard's job is to prepare for review, not to declare completion.

#### 8.9.2 Safety copy pattern

For any risky action ("connect," "import," "upload," "configure"), copy must follow this three-part structure — visible inline above the action CTA, never in a tooltip:

1. **What we will do** — concrete, plain language
2. **What we will not do** — explicit list of safety guarantees
3. **Who stays in control** — assurance that the customer can undo or override

**Example (Airbnb Sync):**

> "We'll import your Airbnb listings, bookings, and messages so you can see them in Guesty. We will not change your pricing, availability, listing content, or calendar. You stay in control and can disconnect anytime."

**Example (Owner Prep):**

> "No owner invitations are sent. You're only saving owner records so they are ready later."

**Example (Migration Gate):**

> "This does not move your full history yet. It tells your specialist what needs review before go-live."

These three are the canonical safety-copy patterns for the three highest-anxiety actions in the wizard. All other safety blocks should be written from the same three-part structure. This pattern must apply to every safety block in the prototype — not just Airbnb. (See Section 8.4 for the inline safety-block layout.)

#### 8.9.3 First-person Guesty voice

The wizard speaks in first-person as Guesty (we / our). This signals an opinionated, confident product — not a passive form. Examples:

- "We've set this to Moderate."
- "We recommend a 3-hour cleaning window."
- "We'll capture what you're bringing over now."

Avoid passive voice ("This has been set to Moderate") and avoid second-person directives ("You should set this to Moderate"). The first-person voice is the structural signal that the wizard is doing the work *with* the customer, not assigning the customer homework.

---

## 9. Data & State Requirements

### 9.1 Mock Dataset

The prototype requires a representative mock dataset for an SMB operator. The following mock data must be defined:

| Data item | Prototype value |
|-----------|----------------|
| Account owner | Sarah Thompson |
| Company name | Suncoast Properties |
| Portfolio | 12 Airbnb listings in Miami Beach, FL |
| Specialist | Casey Waisman |
| Call 1 date | 7 days from today (dynamic) |
| Listings | 3 representative listings with photos, names, ratings |
| Upcoming bookings | 4 bookings across the next 30 days |
| Guest messages | 3 unread messages with realistic guest names |
| Owners | 4 property owners (for Owner Prep step) |

### 9.2 Wizard State Model

The state model is structured around the **Five Core Objects** (Pilot, Milestones, Blockers, Owners, Readiness gates). Each object has a V1 representation that is intentionally a simplified projection of its V2 form — never a divergent model. The model is designed to be **forward-compatible with V2 capabilities** — three-mode architecture (Setup / Review / Governance), silent-customer detection, blockers as first-class objects, readiness gates, asymmetric UX. See Section 11 for full V2 forward-compatibility analysis.

#### 9.2.1 Core State Model (the canonical JSON shape)

The prototype must maintain a single mocked account-level state object. This is the **canonical shape** — every interaction in the wizard reads from and writes to this structure. The prototype builder should treat this as the contract. Field names map to the per-domain detail tables that follow.

```json
{
  "accountId": "mock_account_001",
  "customer": {
    "name": "Sarah Cohen",
    "company": "Urban Stay TLV",
    "propertyCount": 12
  },
  "call1": {
    "booked": true,
    "specialistName": "Maya Levi",
    "date": "2026-05-18T10:00:00Z",
    "daysAway": 3
  },
  "wizard": {
    "activePreset": null,
    "migrationMode": null,
    "currentStep": "welcome",
    "suggestedPathComplete": false,
    "additionalPrepUnlocked": false,
    "lastCompletedStep": null
  },
  "airbnb": {
    "connectionStatus": "not_started",
    "listingsImported": 0,
    "bookingsImported": 0,
    "messagesImported": 0
  },
  "readiness": {
    "listings": "not_started",
    "channels": "not_started",
    "payments": "not_started",
    "financialSetup": "not_started",
    "teamAccess": "not_started"
  },
  "blockers": [],
  "owners": {
    "admin": null,
    "financialsOwner": null,
    "goLiveApprover": null
  },
  "featuresSelected": [],
  "reviewFlags": []
}
```

#### 9.2.2 Required state behavior

These are the deterministic state transitions the prototype must implement. Every screen's "Continue" / "Confirm" / "Save" action triggers one or more of these:

| Trigger | State change |
|---------|-------------|
| Intent Selection completes | `wizard.activePreset` set to selected preset ID |
| Migration Gate completes | `wizard.migrationMode` set; if migration is complex, append to `reviewFlags` |
| Migration risk detected | One or more entries appended to `reviewFlags` (e.g., `migration_complexity_high`, `migration_timeline_tight`) |
| Airbnb sync succeeds | `airbnb.connectionStatus = "connected"`, `listingsImported / bookingsImported / messagesImported` populated |
| Airbnb sync succeeds | `readiness.listings = "ready"` |
| Airbnb sync succeeds | `readiness.channels = "ready"` (Path A) or `"at_risk"` (Path B with multi-channel intent) |
| Airbnb sync skipped | `readiness.listings = "at_risk"`, `readiness.channels = "at_risk"`, append `airbnb_sync_skipped` to `reviewFlags` |
| Airbnb sync fails | `airbnb.connectionStatus = "failed"`, append `airbnb_sync_failed` to `reviewFlags` |
| Operations completes | `readiness.listings` may upgrade from `at_risk` to `ready` once both Airbnb sync + Operations are complete |
| Financials completes | `readiness.financialSetup = "ready"` (or `"needs_review"` if any sub-flag set) |
| Tax answered "I'm not sure" | Append `tax_setup_unsure` to `reviewFlags`, `readiness.financialSetup = "needs_review"` |
| Governance completes | `readiness.teamAccess = "ready"`, `owners.admin / financialsOwner / goLiveApprover` populated |
| GuestyPay optional step started | `readiness.payments = "in_progress"` |
| GuestyPay optional step submitted | `readiness.payments = "ready"` |
| Suggested path completes | `wizard.suggestedPathComplete = true`, `wizard.additionalPrepUnlocked = true` |
| Any step completes | `wizard.lastCompletedStep` set to that step's ID |

The prototype's sidebar readiness view, the Readiness Summary screen, and the V1 Specialist Handoff Output all read directly from this same object — there is no parallel state tree. This is the structural guarantee that makes V2's CSM Review mode a *projection* of the same data.

#### 9.2.3 Per-domain state detail (V1 + V2 forward-compatibility)

The tables below provide the V2-forward-compatible field detail underlying the canonical JSON shape above. Every field listed in the JSON has a corresponding row here.

**Intent + preset state (new in v1.3):**

| State item | Type | Notes |
|-----------|------|-------|
| `selectedIntent` | enum | `accept_direct_bookings` / `connect_channels` / `migrate_existing` / `payments_first` / `team_ops` — captured at Step 1 |
| `activePreset` | enum | `fast_launch` / `migrate_existing` / `channel_sync` / `payments_first` / `team_ops` — derived from selectedIntent and used to drive defaults and task ordering |
| `presetSelectedAt` | timestamp | Timestamp of original selection; flagged separately from any later revision |
| `presetRevisionCount` | integer | Captures the rare case of mid-flow path change (V2 will surface this as a CSM-attention flag) |

**Migration state (new in v1.3):**

| State item | Type | Notes |
|-----------|------|-------|
| `migrationMode` | enum | `fresh` / `listings_only` / `listings_plus_reservations` / `accounting_payments` / `from_another_pms` |
| `migrationItems` | string[] | Multi-select capture: `listings`, `reservations`, `accounting`, `payment_history`, `owner_records` |
| `targetGoLiveWindow` | enum | `within_2_weeks` / `2_to_4_weeks` / `4_plus_weeks` / `not_sure` |
| `currentBookingChannels` | string[] | What the customer is currently taking bookings on (drives dual-running plan) |
| `requiresCsmValidation` | boolean | Set true when migration combination triggers specialist-review flag (e.g., accounting/payment migration) |

**Pilot scope state (Five Core Objects: Pilot):**

| State item | Type | Notes |
|-----------|------|-------|
| `pilotListingCount` | integer | Number of listings in the bounded first launch (typically 1–5) |
| `pilotPrimaryChannel` | string | The primary channel for the pilot (e.g., "airbnb") |
| `pilotPaymentMethod` | string | The selected payment processor (e.g., "guesty_pay" or "external") |
| `pilotScopeConfirmedAt` | timestamp | When the pilot scope was finalized (V1 derives from migration + Airbnb sync; V2 surfaces explicit confirmation) |

**Governance state (Five Core Objects: Owners) — new in v1.3:**

| State item | Type | Notes |
|-----------|------|-------|
| `governanceAdmin` | `{ name, email }` | The account admin (full access, can invite users) |
| `governanceFinancialsOwner` | `{ name, email }` | Financial-questions and statements contact |
| `governanceGoLiveApprover` | `{ name, email }` | The person who signs off on go-live readiness |
| `governanceRoleCollapse` | boolean | Derived: true if all three are the same person (the SMB default) |

**Readiness state (Five Core Objects: Readiness gates):**

The readiness view is a projection of underlying step completions plus blocker state. The customer-facing model:

| State item | Type | Notes |
|-----------|------|-------|
| `readinessByDomain` | `{ listings, channels, payments, financialSetup, teamAccess }` each with state `ready / in_progress / at_risk / needs_review / not_started` | Per-domain readiness, derived from step completions + blockers. See Section 8.6 for full state semantics. |
| `readinessByDomainSources` | per-domain array of contributing step IDs | Lets V2 CSM Review mode expand each domain into its underlying audit trail |
| `pilotScopeReady` | boolean | Derived: true when listings + channels + payments + financialSetup are all `ready` or `needs_review` and no critical blockers are open |

**V2-only readiness state (captured in V1, hidden from customer view):**

| State item | Type | Why it matters for V2 |
|-----------|------|----------------------|
| `slaRiskLevel` | enum (V2 only) | Used by V2 CSM Review mode and V2 Graduation Health Layer |
| `customerActivitySignal` | derived from `lastActivityAt` (V2 only) | Used by V2 silent-customer detection model |
| `lastActivityAt` | timestamp | V1 captures this; V2 surfaces it in CSM mode |

**Blockers state (Five Core Objects: Blockers) — new in v1.3:**

For V1, blockers are captured as lightweight structured records on the account. For V2, they will be elevated to first-class operational objects with their own dashboard. The V1 schema must already support this.

```
{
  blockerId: string,
  type: enum,                    // e.g., "tax_unsure" / "csm_validation_required" / "migration_specialist_review"
  capturedAtStepId: string,
  description: string,           // Customer-friendly label for V1 readiness-screen display
  owner: enum,                   // "customer" | "csm" | "both" — V1 defaults to "csm" for SMB role-collapse
  dueRelativeTo: enum,           // "before_call_1" | "during_call_1" | "before_go_live"
  impact: enum,                  // "low" | "medium" | "high" — V2 drives SLA risk; V1 drives copy framing
  resolutionPath: string         // "Your specialist will help with this on Call 1" or similar
}
```

**Milestones state (Five Core Objects: Milestones):**

Milestones are binary, non-percentage events. V1 tracks them as part of the wizard flow; V2 elevates them into the activation telemetry layer.

| Milestone | Trigger |
|-----------|---------|
| `intentSelected` | Step 1 complete |
| `migrationGateAnswered` | Step 2 complete |
| `aha` | Airbnb sync complete (Step 3) — the AHA milestone |
| `pilotScopeReady` | All readiness domains reach Ready/Needs review and no critical blockers |
| `call1Ready` | Suggested path complete + governance captured (or customer entered Guesty directly) |

**Core wizard state (existing, retained):**

| State item | Type | Notes |
|-----------|------|-------|
| `airbnbConnected` | boolean | The most critical state; drives AHA moment |
| `operationsCompleted` | boolean | All 6 questions answered |
| `financialsCompleted` | boolean | All 4 sub-sections confirmed |
| `governanceCompleted` | boolean | Step 6 complete (new in v1.3) |
| `orientationCompleted` | boolean | Both links clicked |
| `featuresSelected` | string[] | Array of selected feature IDs |
| `suggestedPathComplete` | boolean | Derived: all suggested steps complete |
| `additionalPrepUnlocked` | boolean | Same as `suggestedPathComplete` |
| `currentStep` | string | Step ID of the customer's current location |
| `call1ScheduledAt` | timestamp | Drives the call countdown and urgency escalation |

**Engagement / momentum state (V2 forward-compatibility):**

| State item | Type | Why it matters for V2 |
|-----------|------|----------------------|
| `lastActivityAt` | timestamp | Required for V2 silent-customer detection ("no login in 7 days") |
| `sessionCount` | integer | Distinguishes "completes in one go" from "comes back repeatedly" |
| `stepHistory` | array of `{ stepId, firstViewedAt, completedAt, skippedAt, editCount }` | Derives V2 signals: "wizard started but no AHA milestone", "repeatedly returns but does not complete a section" |
| `skipFlags` | array of `{ stepId, reason }` | V1 captures the skip event so V2 can elevate persistent skips into structured blockers |

**Per-step state pattern:**

For each wizard step (suggested and additional prep), persist:

```
{
  stepId: string,
  status: "not_started" | "in_progress" | "completed" | "skipped",
  data: {},                        // The configuration values themselves
  firstViewedAt: timestamp,
  completedAt: timestamp | null,
  skippedAt: timestamp | null,
  editCount: integer,              // How many times the customer revised their answer
  readinessContribution: string[], // Which readiness domain(s) this step contributes to
  readinessConfirmed: boolean      // V1 = always equals (status === "completed"); V2 = real account state validation
}
```

The distinction between `status === "completed"` and `readinessConfirmed === true` is the V2 readiness-gate hook. In V1 they are the same; documenting them separately makes the V2 upgrade non-breaking.

### 9.3 Configuration Write Simulation

In the prototype, configuration writes to the Guesty backend are simulated. Each step's "Confirm" or "Save" action triggers:

1. A brief loading state (0.8–1.5 seconds)
2. A success confirmation
3. A state update that persists in the prototype's local state store

No real API calls are made. The prototype uses a client-side state layer (React state or similar) to simulate persistence.

---

## 10. Success Metrics

### For the prototype specifically:

| Metric | Target |
|--------|--------|
| Usability testing: % of test users who complete Airbnb sync without assistance | ≥80% |
| Usability testing: % of test users who correctly understand that all steps are optional, with the suggested path most impactful | ≥85% |
| Usability testing: % of test users who recognize the AHA reveal as their "real business" (open question / interview signal) | Qualitative — every interview should produce explicit recognition of the populated platform as theirs |
| Wait-conversion validation: in a simulated 5-day-wait return-flow test, % of test users who resume the wizard rather than abandon | ≥70% (qualitative, set during usability sessions) |
| Stakeholder review: Alignment on wizard flow and step sequencing | Sign-off by Product, CSM lead, Design lead |
| Prototype coverage: % of production user stories the prototype demonstrates | 100% of suggested path; ≥70% of additional prep track |

### Primary V1 Activation Metric

**Airbnb view-only sync before Call 1**

> Target: more than **80%** of new Guesty Pro SMB accounts complete Airbnb view-only sync before their scheduled Call 1.

This is the sole hard KPI. It is the clearest proof that the wizard resolved the cold-start problem and created early customer investment. It is the gating metric that determines whether the wizard succeeded in V1.

### Supporting Product Metrics

Track and report. Establish baselines in the first 90 days. No hard targets at launch — these are the instrumentation layer that makes V1 learnable.

- Wizard start rate
- Intent selection completion rate
- Migration gate completion rate
- Airbnb sync start rate
- Airbnb sync completion rate
- Airbnb sync failure rate
- Operations setup completion rate
- Financial setup completion rate
- Feature interest selection rate
- Readiness summary viewed rate
- Platform handoff clicked rate
- Returning-user resume rate
- Per-step drop-off (flag any step where drop-off exceeds 25%)

### Call Quality Metrics

These prove whether Call 1 became review instead of walkthrough — the intended downstream effect.

- Specialist-reported Call 1 quality score (1–5 post-call rating)
- % of Call 1 time spent on review and validation vs. walkthrough
- % of customers arriving at Call 1 with Airbnb synced
- % of customers arriving at Call 1 with financials or operations already started
- Number of unresolved blockers discovered during Call 1 (not flagged by wizard)

### Business Outcome Metrics

Lagging indicators. Measure after at least one full onboarding cycle (~8–12 weeks post-launch).

| KPI | Baseline | Target |
|-----|----------|--------|
| Average specialist sessions per SMB onboarding | ~7–8 sessions (kickoff + 6–7 follow-ups) | ≤5 sessions (Setup Call + 4 follow-ups) |
| SMB onboarding duration | Avg 28.8 days past the 20-day SLA | ≤20 days (SLA) |
| SMB on-time graduation rate | **18%** (April 2026), 69% delayed | Directional improvement; specific target tied to OB capacity recovery |
| Silent/inactive/non-responsive/unknown churn cluster | **~49.4%** of all Guesty churn (Unknown 18.5% + Non-Responsive 17.0% + Inactive/Silent 14.0% + Silent User 4.1%) | Directional reduction; treated as lagging signal, not primary V1 proof |
| Post-graduation 3-month MRR churn | Trending 2.84% (Apr 2026) → 3.88% (May 2026) — **breaching the 3% threshold** | Maintain ≤3%; recover toward 2.5% |

**Note on baseline trends:** Post-graduation MRR churn is currently *deteriorating*. The wizard is being launched into a softening retention environment. The "no degradation" guardrail below is not advisory — it is a hard gate. The wizard must not enable premature graduation that worsens this trend.

### Guardrail Metrics

The wizard should not improve speed at the cost of quality. These guardrails protect against acceleration at the cost of retention or experience.

- **No degradation in 3-month post-OB MRR churn** — must stay ≤3%; any upward movement while the wizard is in production is an escalation signal
- **No increase in support tickets caused by misconfiguration** — the wizard's opinionated defaults must not introduce configuration errors at scale
- **No increase in Call 1 confusion** — specialist-reported confusion scores must not worsen vs. pre-wizard baseline
- **No increase in Airbnb connection anxiety or failed-connection recovery issues** — the safety framing must work; any increase in anxiety or failed-recovery tickets is a signal that the safety copy needs revision

### KPI Ownership

Core outcome metrics (Activation, Call Quality, Business Outcomes) are **shared between Product and CSM** — neither team owns them alone. Supporting Product Metrics and Guardrail Metrics are Product's continuous improvement signals.

This shared ownership is intentional. A single-team KPI creates the wrong incentive: Product might optimize Airbnb sync rate at the cost of call quality; CSM might optimize call quality at the cost of wizard completion. The shared model requires both sides to win together.

---

## 11. Out of Scope

### 11.0 What V1 Does Not Solve

These are explicitly outside the wizard's scope. The prototype must not imply it solves any of these:

- Onboarding team capacity (the wizard reduces call quality bar; it does not add headcount)
- The full contract-to-graduation timeline
- Inter-call momentum loss after Call 1
- Full migration from another PMS
- Accounting or payment history migration
- GuestyPay activation as a complete funnel
- Full platform education
- Rocketlane adoption as the main task surface
- Docebo training consumption
- Post-graduation CSM handoff
- Churn reason taxonomy cleanup
- CSM Review mode as a full operational dashboard

### 11.0.1 What V1 Does Solve

- The blank state before first platform entry (cold-start resolution)
- Lack of clear pre-Call-1 action
- Missing launch intent signal for the specialist
- Missing migration complexity signal before Call 1
- Customer anxiety around Airbnb sync
- Lack of meaningful specialist prep before Call 1
- The absence of a simple readiness summary for the customer

### 11.1 Out-of-scope features (deferred to V2 or other initiatives)

The following are real product features that the wizard should not build in V1, organized by when they are expected to become in-scope:

| Item | When | Reason |
|------|------|--------|
| Live Airbnb OAuth integration | Production build | Engineering scope; mocked in prototype |
| Real configuration writes to Guesty backend | Production build | Mocked in prototype |
| Notification settings configuration | V2 | Explicitly deferred |
| Consent checkbox ("configure on my behalf") | Pending | Deferred pending legal/product alignment |
| Pre-population pipeline integration | V2 | Separate in-flight initiative; wizard is forward-compatible |
| Owner invitations | V2 | V1 captures owner records only (bulk upload); invite sending is deferred |
| OTA integrations beyond Airbnb (Booking.com, VRBO/Expedia) | **Call 2 scope** | Airbnb is the V1 activation channel; additional OTAs are introduced in the second specialist session |
| Automated messages, Guest App, Auto Tasks, Inbox setup | **Call 3 scope** | These are post-baseline operational features; not pre-Call-1 setup |
| Rate strategy show-back UI | V2 | Task is wizard scope; the show-back UI requires platform changes |
| Full-fidelity readiness dashboard for customers | V2 | V1 ships a simplified 5-domain readiness view |
| Full CSM Review Mode | V2 | V1 data model supports it; the mode itself is V2 |
| Mobile responsiveness | Production build | Desktop-first for prototype |
| Accessibility certification (WCAG) | Production build | A11y notes in requirements; full audit for production |
| Multi-language support | Post-launch | English-only for prototype |

### 11.2 V2 directions the prototype should be forward-compatible with

V1 owns only the pre-Call-1 wait. If it succeeds, the wizard evolves into a full **momentum-control system** covering the entire onboarding journey. The prototype does not build these capabilities, but its data model and UX patterns should not foreclose them:

| V2 direction | Implication for V1 prototype |
|-------------|-----------------------------|
| **Three-mode architecture (Setup / Review / Governance)** — same underlying state drives three presentation modes for two audiences. V1 ships only Setup mode; V2 adds the CSM Review mode (readiness, SLA risk, blockers, last-active date) and the Governance mode (admin/owner role review, go-live approval workflow). | The V1 state model is structured so the V2 modes are *projections* of the same data, never separate models. Concretely: the `readinessByDomain` field (Section 9.2) is the customer simplification; the same data plus `slaRiskLevel`, `customerActivitySignal`, and `readinessByDomainSources` produces the V2 CSM Review view without state model changes. The V1 prototype must demonstrate that the customer view is a projection — no V1 UI element may be wired to a model that cannot extend to the other two modes. |
| **Homework packets between sessions** — after each specialist call (Call 1 onward), the wizard generates a structured asynchronous work packet for the customer (bounded, specific tasks to complete before the next session). Replaces inter-call CSM dependency; makes progress visible to both sides. | V1 is pre-Call-1 only — no homework packets are generated. But the V1 state model captures all configuration writes with timestamps and per-step `data`, so V2 homework-packet generation can read directly from V1 wizard state without retrofit. The "Interesting Features" step (V1 Step 8) is the structural seed: it captures customer-selected feature interests that will drive Call-1-and-beyond agenda generation in V2. |
| **Preset library expansion** — V1 ships with 5 SMB presets (Fast Launch, Migrate Existing, Channel Sync, Payments First, Team Ops). V2 expands the library: vertical-specific presets (urban STR, vacation market, serviced apartments), OTA-configuration presets, team-composition presets. Each new preset is a configuration of the same framework — task sequence, defaults, readiness criteria — not a new product. | The V1 preset model must treat presets as *data*, not as hardcoded code paths. Concretely: the `activePreset` field drives a configuration table (task list, defaults, readiness criteria) — adding a new preset in V2 is a data change, not a code change. The prototype must demonstrate that adding a sixth preset would not require any UI or state model rework — it would only require a new row in the preset configuration table. |
| **Graduation health layer** — visible SLA risk for both customer ("You're almost ready — finish channel connection to stay on track") and onboarder ("7 days until SLA breach, customer hasn't responded in 5 days") | V1 includes a passive call countdown only. The state model already has the `slaRiskLevel` field (Section 9.2) hidden from customer view but populated; V2 surfaces it. No state model changes required to add the layer. |
| **Silent-customer detection model** — signal-based system that flags momentum decay (no login in 7 days, wizard started but no AHA, no Call 1 booked, etc.) and triggers interventions | V1 wizard state captures timestamps and step-completion events with enough granularity that V2 signals can be derived from them. Specifically: `lastActivityAt`, `sessionCount`, per-step `firstViewedAt` and `completedAt`, and the milestones list (`aha`, `pilotScopeReady`, `call1Ready`). |
| **Blockers as first-class objects** — every onboarding blocker captured as a structured record (type, owner, due date, impact on graduation, recommended resolution, escalation path) | V1 captures blockers in lightweight form (Section 9.2 Blockers schema). V2 elevates them to a dedicated dashboard with full lifecycle (assigned, in progress, resolved, escalated). The V1 schema is the V2 schema's subset — no migration required. |
| **Readiness gates** — V2 validates real account state ("listings imported and active", "at least one channel connected"), not just step completion | V1 tracks step touches and per-domain readiness states; V2 adds programmatic validation against the real account. The state model already distinguishes `status === "completed"` from `readinessConfirmed === true` — V1 uses only the former, V2 enables the latter without refactor. |
| **Graduation handoff summary** — wizard auto-generates a structured CSM brief at graduation (completed items, known risks, recommended follow-up) | V1 does not generate handoffs. But every wizard configuration write is timestamped and attributable, so V2 can reconstruct a graduation summary from V1 data. The Readiness Summary screen (V1 Step 7.11) is the structural ancestor of this V2 brief. |
| **Asymmetric UX** — customer sees simplified opinionated surface; onboarder sees diagnostic operational view; same state model drives both | This is captured by the three-mode architecture above. V1 is customer-only (Setup mode). The state model is designed as a single source of truth that can later be projected into a different UI for the onboarder, rather than embedding presentation logic in the data layer. |
| **Commercial opportunity prompts** — upsell surfaces (especially GuestyPay) introduced *after* core activation milestones, never during setup | V1 includes "Guesty Pay application start" as an optional step — this is the only commercial surface in V1 and it is framed as *velocity* (start the application early), not upsell. The prototype must not introduce any "upgrade" or "add-on" prompts during setup. |
| **Segment expansion (mid-market)** — wizard architecture extends to mid-market accounts with a relaxed role-collapse assumption (mid-market typically has a customer admin distinct from the exec sponsor, enabling a 2–3 role onboarding model closer to the monday.com reference architecture). The migration wizard tracks (full PMS migration, complex historical data imports) also belong primarily in this segment expansion. | V1 is SMB-only and explicitly built around the role-collapse assumption. The state model and step definitions should not embed the SMB-only assumption deeply — for example, the governance state already captures *three* role slots (admin / financials / go-live approver) with a `governanceRoleCollapse` derived flag. In V2 mid-market, the three slots remain but the collapse flag becomes false more often, and the per-step `assignedTo` field can be added without breaking V1. |

---

## 12. Open Questions

| # | Question | Owner | Priority |
|---|----------|-------|----------|
| Q1 | **Wizard-vs-pre-population scope split.** Which configuration domains are wizard-only, pre-pop-only, or hybrid? This changes which fields in subsequent steps are pre-filled by the wizard's opinionated defaults vs. the pre-population pipeline. | Product + Engineering | High — resolve before prototype build |
| Q2 | **Activation-check definition per task.** What is the explicit "complete enough for Call 1" criterion for each non-Airbnb step? This drives the readiness view's domain-state derivation rules and the specialist's Call 1 review checklist. | Product + CSM | High — resolve before prototype build |
| Q3 | **Role-collapse vs. guided-session task split (Alone vs. Alone + OB Review).** Because all onboarding roles collapse into one SMB owner-operator, the CSM-guided build model operates differently than the 3-role enterprise version. The PRD must decide per task: is it fully self-serve ("Alone") or does it expect the customer and CSM to work through it together live ("Alone + OB Review")? This decision drives wizard UX (step instructions, review prompts, save-vs-submit states) and specialist prep (what the CSM expects the customer to have completed vs. what they expect to review on the call). The brief currently labels Operations, Financials, Booking Engine, and Rate Strategy as "Alone + OB Review" — the prototype must visualize how that combined-mode is presented to the customer (does the step show "you'll review this with your specialist on Call 1"?). | Product + CSM | **High — directly affects the prototype's per-step UX** |
| Q4 | **SLA visibility in V1.** The full Graduation Health Layer (visible SLA risk for both customer and onboarder) is confirmed for V2. The PRD must decide whether any form of time-awareness — even lightweight ("Your Call 1 is in 3 days — here's what to finish first") — belongs in V1, or whether that is strictly deferred. The prototype currently includes a passive call countdown in the top bar; this question is whether that countdown should escalate into proactive prompts as the call approaches. | Product + CSM | High — affects prototype copy and UX patterns |
| Q5 | **Measurable exit criteria for the 7→5 compression claim.** The brief commits to reducing total specialist sessions. The metric and threshold for declaring success need to be defined (e.g., "X% of small accounts complete onboarding in five or fewer sessions within Y days"). | Product + CSM | High — affects KPI #4 measurement |
| Q6 | **Readiness dashboard scope in V1.** The five core objects (Pilot, Milestones, Blockers, Owners, Readiness gates) call for a readiness dashboard rather than a progress bar as the primary V1 UI primitive. The PRD must decide what portion of this dashboard is visible to the customer ("3 things left before launch") vs. exclusively to the onboarder (SLA risk, blocker detail, last-active date) in V1. The PRD currently scopes V1 to a customer-facing readiness view (5 domains, 4 simple states) and treats the CSM-facing operational dashboard as V2 — but the team must confirm whether even a minimum-viable readiness view for the CSM (without the full dual-audience build) belongs in V1. | Product + CSM | **High — directly affects the prototype's primary UI primitive** |
| Q7 | **Migration gate depth in V1.** The wizard branches on "starting fresh vs. migrating." In V1, how deep does the migration path go? Three options: (a) surface a warning and CSM flag only — the migration itself is handled offline; (b) provide a lightweight guided import for listings-only; (c) full migration wizard tracks for all migration types. Given MVP scope, option (a) or (b) is likely the right V1 boundary, with full migration tracks as a V2 segment-expansion item. The prototype currently demonstrates option (a) with structured capture; option (b) would extend Step 7.2 with a guided listings-import sub-flow. | Product + CSM | **High — directly affects the prototype's Step 7.2 (Migration Gate) build** |
| Q8 | **Governance scope in V1.** The wizard captures who owns admin / financials / go-live approval to create a governance record for the CSM (Step 7.6). The PRD must decide: is this a dedicated screen (current spec), inline questions per section, or derived automatically from the preset selection? For SMB accounts where all roles are one person, this may be a single-question acknowledgement rather than a full role-assignment flow. The PRD currently specifies a dedicated screen with a single-person fast path — confirm this is the right shape, or simplify further. | Product + CSM | High — affects whether Step 7.6 is a full screen or a prompt |
| Q9 | **Intent selection and preset validation.** The five presets (Fast Launch, Migrate Existing, Channel Sync, Payments First, Team Ops) need validation against real account data: do actual Guesty Pro SMB accounts sort cleanly into these five paths? Is "Fast Launch" the dominant preset that 80%+ of accounts should land in? The PRD should specify a pilot validation approach — either A/B testing preset vs. no-preset, or tracking which preset was selected in the first 90-day cohort to validate distribution. The prototype demonstrates the *mechanism* of preset-driven flow adaptation; the question is whether the *content* of the five presets is the right segmentation. | Product + Data + CSM | **High — affects whether the prototype's Step 7.1 ships with five presets or fewer** |
| Q10 | **Rate strategy show-back interaction.** When the wizard writes a rate strategy based on the customer's answers, how does the customer see what was created? There is no direct UI feedback in the current platform. | Design + Engineering | Medium — required for optional prep step |
| Q11 | **Consent to configure on behalf.** Legal/product alignment pending. If consent is required, where does it appear in the wizard flow, and what happens if the customer declines? | Legal + Product | Medium — may affect Operations and Financials steps |
| Q12 | **"Skip all" and minimum viable exit.** Can a customer click through the entire wizard without completing a single step? What state does the platform launch in if they do? What does the specialist see in the readiness view? | Product + CSM | Medium — edge case with significant UX implications |
| Q13 | **Rocketlane role clarification.** For accounts ≤20 properties, does Rocketlane appear at all before Call 1? If hidden, what does the Orientation step show instead? | Product + CS Operations | Medium |
| Q14 | **Wizard entry for edge cases.** What happens if the customer did not book a call (skipped the booking screen)? Does the call reminder block show "Book your call" instead? | Product | Low — design question, answer in prototype |
| Q15 | **Session timeout and magic link behavior.** If the customer returns after more than 7 days, does the wizard state persist? Is a magic link required, or does standard Guesty auth suffice? | Engineering | Low — production concern, not prototype blocker |
| Q16 | **Preset revision mid-flow.** What is the UX when a customer wants to change their selected preset mid-wizard (e.g., realizes they're a migration case after starting Fast Launch)? Does this require CSM consultation? Does it preserve already-completed configuration writes? | Product + Engineering | Low — edge case but affects state model design |

---

## 13. Required Edge Cases

The prototype must include the following edge cases. These are not optional polish — they are the cases that pressure-test product logic and prevent the prototype from drifting into a happy-path-only demo.

### 13.1 The required list

The prototype must include and demonstrate at least these ten edge cases:

| # | Edge case | Tests |
|---|----------|------|
| 1 | Airbnb connection failure | Error UI, retry, safe skip path, review flag creation |
| 2 | Customer skips Airbnb sync | Confirmation copy, At risk readiness states, review flag |
| 3 | Customer selects migration + tight timeline (within 2 weeks + complex items) | Warning surface, multiple review flags, At risk states |
| 4 | Customer selects "I'm not sure" in tax setup | Review flag, Needs review readiness state, copy framing |
| 5 | Customer has no Call 1 booked when entering the wizard | Persistent soft "Book your first session" recommendation (not a gate); customer can proceed fully without booking; automated reminder emails are the re-engagement mechanism |
| 6 | Customer returns after partial completion | Returning-user resume scenarios (Section 8.7) |
| 7 | Customer tries to open additional prep before the suggested path is complete | Dimmed state with copy explaining what unlocks it; customer can still exit to Guesty; no broken navigation |
| 8 | Customer changes launch path mid-flow | Confirmation modal, behavior on already-completed steps, `presetRevisionCount` increments |
| 9 | Customer opens "See all fee types" drawer in Financials | Drawer or placeholder opens, customer can dismiss without losing state |
| 10 | Customer uses "Add different people" in Governance Capture | The 3-slot detailed layout opens, all three fields are editable, completion still updates `readiness.teamAccess` |

### 13.2 Required behavior for each edge case

For every edge case, the prototype must show:

- A **clear explanation** in plain language — what just happened, what it means
- A **safe next action** — at least one CTA that lets the customer continue without anxiety
- **Whether a review flag is created** (and if so, which one — see `reviewFlags` in the Core State Model)
- **Whether a readiness state changes** (and which domain — see Section 8.6)
- **How the customer continues** — no dead ends, no "contact support" exits in V1

### 13.3 Edge cases NOT required in V1 prototype

The following edge cases are real production concerns but are out of scope for the V1 prototype:

- Airbnb token expiration / re-auth flow
- Concurrent edits from multiple browser tabs
- Network-level failure handling beyond the simulated Airbnb error
- Deep accessibility edge cases (screen reader navigation, high-contrast mode)
- Customer changes their email mid-wizard

These should be flagged for the production PRD (Section 0.1.3).

---

## 14. Event Tracking Requirements (production handoff)

Analytics do not need to be **built** in the V1 prototype, but the events that production must emit should be **annotated** in the prototype so the engineering team has a clear contract for the analytics pipeline. This section is the contract.

### 14.1 Required event taxonomy

| Event | Trigger | Properties |
|------|---------|-----------|
| `wizard_started` | User lands on the Welcome screen | `account_id`, `call_booked`, `days_to_call` |
| `intent_selected` | User selects a launch path on Step 1 | `preset_id` |
| `migration_gate_completed` | User completes Step 2 | `migration_mode`, `complexity_flags[]` |
| `airbnb_sync_started` | User clicks "Connect Airbnb" | `preset_id`, `migration_mode` |
| `airbnb_sync_completed` | Airbnb sync succeeds | `listings_count`, `bookings_count`, `messages_count` |
| `airbnb_sync_failed` | Airbnb sync fails | `error_type` |
| `step_confirmed` | User completes any wizard step | `step_id`, `edited_fields_count` |
| `step_skipped` | User skips a skippable step | `step_id` |
| `readiness_state_changed` | Any readiness domain state transitions | `domain`, `from_state`, `to_state`, `trigger_step` |
| `blocker_created` | A review flag or blocker is appended to `reviewFlags` | `blocker_type`, `source_step`, `severity` |
| `additional_prep_unlocked` | Suggested path completes | `completed_steps_count` |
| `platform_handoff_clicked` | User clicks "Go to Guesty" on the Platform Handoff screen | `readiness_summary` (snapshot of `readiness` and `reviewFlags`) |

### 14.2 What the prototype must do

The prototype is **not** required to emit these events to a real analytics system. It must:

- Annotate each interaction with the event name it would emit (this can be a console.log, a comment in the code, or a tooltip in dev-mode — visible to the builder/reviewer)
- Include this taxonomy in the implementation handoff so the production team can wire each event to the analytics pipeline without re-deriving the taxonomy

### 14.3 Why this matters

KPIs in Section 10 (Airbnb sync completion before Call 1, wizard step drop-off, silent-customer detection signals) all depend on this event stream. Defining the taxonomy at prototype time saves implementation time later and ensures the prototype's interaction patterns are measurable in production.

---

## 15. Builder Guardrails

These are the most likely ways the prototype could drift away from the intended product strategy. Each item in this list is a **do-not-build** instruction. Builders should treat this list as veto-power: if the prototype starts to look like one of these, it must be reworked.

### 15.1 Do not build

- A generic progress-bar-led setup wizard
- A flow that starts with Airbnb before Intent Selection and Migration Gate
- Blank forms as the primary interaction model
- Safety copy hidden behind tooltips or "Learn more" links — safety must be inline, above the fold, and impossible to miss
- Rocketlane or Docebo as the primary task surface
- Optional prep that visually competes with required setup
- A full enterprise Guesty UI before the Platform Handoff (the wizard is the entire pre-platform surface)
- A final state that says "100% complete" — the correct framing is "Ready for Call 1"
- A CSM Review mode as a separate data model — V2 Review must be a *projection* of the V1 state
- A full migration product inside V1 — the Migration Gate captures and flags, it does not migrate
- A flow that suggests the customer is ready to go live just because they completed the wizard

### 15.2 Why this matters

Each guardrail above corresponds to a specific risk:

- "Progress-bar-led" → reverts the product to a setup wizard, loses the implementation system framing
- "Airbnb before intent" → loses scope-before-configure, makes the wizard generic
- "Blank forms" → forces the role-collapsed customer to invent structure
- "Tooltip safety" → fails the explicit-safety principle, customer doesn't read it
- "Rocketlane/Docebo as primary" → reverts to the failed pre-Call-1 task surface
- "Additional prep competes with suggested path" → dilutes the recommended track and confuses what the biggest wins are before Call 1
- "Full Guesty UI early" → reintroduces the cold-start problem the wizard exists to solve
- "100% complete" → implies go-live readiness, exposes the post-graduation churn cliff
- "Separate V2 model" → creates a data debt that prevents the V2 Review mode from shipping
- "Full migration in V1" → V1 overpromises and under-delivers
- "Wizard = ready to go live" → catastrophic expectation mismatch with reality

---

## 16. Final Builder Summary

> Build a high-fidelity functional prototype of the Guesty Pro Onboarding Wizard.
>
> The prototype must prove that a new Guesty Pro SMB customer can move from a blank, passive waiting period into an active pre-Call-1 preparation flow.
>
> The flow must start with **launch intent** and **migration complexity**, then safely connect Airbnb in view-only mode, reveal the customer's real business data inside Guesty, let the customer **confirm or edit** recommended defaults, capture **lightweight ownership**, show a **readiness summary**, and hand the customer into a **populated Guesty platform**.
>
> The primary validation is **not** that the customer completed a setup checklist. The primary validation is that the customer is **synced, oriented, and review-ready before Call 1**.

If a screen, copy choice, or interaction contradicts this paragraph, that screen is wrong — fix it before treating the prototype as deliverable.

---

*End of PRD v1.4 — Guesty Pro Onboarding Wizard Prototype*
