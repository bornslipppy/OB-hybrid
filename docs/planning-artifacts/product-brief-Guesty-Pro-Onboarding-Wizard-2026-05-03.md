---
stepsCompleted: [1, 2, 3, 4, 5]
inputDocuments:
  - '/Users/yair.cohen/Downloads/Draft Brief (2).md'
  - '/Users/yair.cohen/Downloads/Feedback Document.md'
  - '/Users/yair.cohen/Downloads/prototyping v2 (4).html'
  - '/Users/yair.cohen/Documents/GitHub/Tahini/knowledge/personas/guesty-user-personas.md'
  - '/Users/yair.cohen/Documents/GitHub/Tahini/knowledge/personas/persona-evaluation-rules.md'
  - '/Users/yair.cohen/Documents/GitHub/Tahini/knowledge/product-model/cross-domain-pain-points.md'
  - '/Users/yair.cohen/Documents/GitHub/Tahini/knowledge/product-model/reservation-lifecycle-map.md'
  - '/Users/yair.cohen/Documents/GitHub/Tahini/knowledge/domains/d1-financials.md'
  - '/Users/yair.cohen/Documents/GitHub/Tahini/knowledge/domains/d2-operations.md'
  - '/Users/yair.cohen/Documents/GitHub/Tahini/knowledge/domains/d5-distribution.md'
  - '/Users/yair.cohen/Documents/GitHub/Tahini/knowledge/domains/d6-global-platform.md'
  - '/Users/yair.cohen/Documents/GitHub/Tahini/knowledge/ux-guidelines/guesty-ux-principles.md'
  - '/Users/yair.cohen/Documents/GitHub/Tahini/knowledge/ux-guidelines/guesty-ux-governance.md'
  - '/Users/yair.cohen/Documents/GitHub/Tahini/knowledge/ux-guidelines/design-guidelines.md'
  - '/Users/yair.cohen/Documents/GitHub/Tahini/knowledge/ux-guidelines/components/empty-state.md'
  - '/Users/yair.cohen/Documents/GitHub/Tahini/knowledge/ux-guidelines/components/skeleton.md'
  - '/Users/yair.cohen/Documents/GitHub/Tahini/knowledge/ux-guidelines/components/progress-bar.md'
  - '/Users/yair.cohen/Documents/GitHub/Tahini/knowledge/ux-guidelines/components/dialog.md'
  - '/Users/yair.cohen/Documents/GitHub/Tahini/knowledge/ux-guidelines/components/drawer.md'
  - '/Users/yair.cohen/Documents/GitHub/Tahini/knowledge/ux-guidelines/components/tooltip.md'
  - '/Users/yair.cohen/Documents/GitHub/Tahini/knowledge/ux-guidelines/components/form.md'
  - '/Users/yair.cohen/Documents/GitHub/Tahini/knowledge/ux-guidelines/components/card.md'
  - '/Users/yair.cohen/Documents/GitHub/Tahini/knowledge/ux-guidelines/components/toast.md'
  - '/Users/yair.cohen/Documents/GitHub/Tahini/knowledge/ux-guidelines/components/accordion.md'
  - '/Users/yair.cohen/Documents/GitHub/Tahini/knowledge/ux-guidelines/components/breadcrumb.md'
  - '/Users/yair.cohen/Documents/GitHub/Tahini/knowledge/ux-guidelines/components/tabs.md'
  - '/Users/yair.cohen/Documents/GitHub/Tahini/knowledge/ux-guidelines/components/button.md'
  - '/Users/yair.cohen/Documents/GitHub/Tahini/knowledge/ux-guidelines/components/link.md'
  - '/Users/yair.cohen/Documents/GitHub/Tahini/knowledge/ux-guidelines/components/input.md'
  - '/Users/yair.cohen/Documents/GitHub/Tahini/knowledge/ux-guidelines/components/combobox.md'
  - '/Users/yair.cohen/Documents/GitHub/Tahini/knowledge/ux-guidelines/components/select.md'
date: '2026-05-03'
author: 'Yair Cohen'
lastUpdated: '2026-05-04'
---

# Product Brief: Guesty Pro Onboarding Wizard

## 1. Executive Summary

The Guesty Pro Onboarding Wizard solves the highest-risk moment in SMB onboarding: **the gap between registration and the first specialist call.**

Today, customers sign, create an account, book a call, and then wait. During that wait, they enter a blank and complex enterprise platform, lose momentum, return to their old PMS, or arrive at Call 1 unprepared.

V1 turns that passive wait into active launch preparation. It guides customers through a scoped setup path, safely connects Airbnb in view-only mode, captures migration complexity, applies Guesty's recommended defaults, and produces a review-ready account before the first specialist session.

The goal is not to make customers fully live without a specialist. The goal is to make Call 1 dramatically better: less walkthrough, more review, validation, and edge-case resolution.

> **V1 Thesis: Turn new Guesty Pro SMB customers from blank, inactive, and cold into synced, oriented, and review-ready before Call 1.**

---

## 2. Strategic Problem

Guesty Pro SMB onboarding has a structural dead zone between registration and the first specialist call.

Customers are financially committed and motivated when they sign, but the onboarding team cannot always meet them immediately. During this gap, the customer lands in an empty enterprise platform, receives disconnected references to Rocketlane and Docebo, and has no clear sense of which steps will make the biggest difference before the first call.

This creates four failure modes:

1. **Cold start** — the homepage, calendar, and inbox are empty, so Guesty does not yet feel like the customer's business.
2. **No clear path** — customers do not know which steps will make the biggest difference before Call 1 and what can safely wait.
3. **Enterprise overload** — small operators face a feature surface designed for much larger teams.
4. **Momentum decay** — the old PMS remains the safer fallback while Guesty feels incomplete and unfamiliar.

The wizard addresses this specific gap. It does not solve the entire onboarding journey. It converts pre-Call-1 waiting time into guided preparation.

### Why This Matters Now — Operational Context

The data confirms a structural failure that more calls cannot fix:

| Signal | Current State |
|--------|---------------|
| SMB on-time graduation rate (April 2026) | **18%** on time; 69% delayed; 28.8 days average overrun against 20-day SLA |
| Specialist call volume | 31–43 hours/month against 60-hour target; **higher call volume does not correlate with better SLA** |
| 3-month post-graduation MRR churn | Apr 2026: 2.84% / May trending toward 3.88%, breaching the 3% KPI threshold |
| Silent / inactive / non-responsive / unknown churn cluster | **~49.4% of all Guesty churn** (Unknown 18.5%, Non-Responsive 17.0%, Inactive/Silent User 14.0%, Silent User 4.1%) |
| Pre-Call-1 task completion in Rocketlane | ~0% — customers do not engage with the existing pre-call surface |

The wizard directly targets the engagement pattern behind silent and non-responsive churn: customers who stop participating before the product has a chance to work for them. Because "Unknown Reason" is a weak taxonomy bucket, reduction in the full silent / inactive / unknown cluster should be treated as a **lagging directional signal**, not the primary proof of MVP success. The primary proof of V1 is earlier in the funnel: customers returning, syncing Airbnb, completing pre-call prep, and arriving at Call 1 with real account state for the specialist to review.

---

## 3. Target Segment

V1 is designed for **Guesty Pro SMB customers**: owner-operators and very small teams managing roughly **5–70 properties**, with the segment averaging around 50–70.

These customers are not enterprise implementation teams. They are time-pressed operators who want Guesty to tell them what to do, in what order, with safe defaults.

### The Critical Design Constraint: Role-Collapse

In larger implementations, onboarding usually involves an executive sponsor, a customer admin, and a process champion. **In Guesty Pro SMB, those roles often collapse into one person: the owner-operator.**

That means the wizard cannot assume the customer will self-organize. It must supply the sequencing, defaults, safety framing, suggested/get-ahead distinction, and readiness definition that a project manager or champion would normally provide.

This is the primary reason a normal checklist is not enough — and it's the reason this V1 architecture does not scale unmodified to mid-market, where role-separation returns.

### Secondary Stakeholders Affected (not direct users)

- **Bookkeepers / accountants** — a subset of operators consult an external accountant for financials setup. The wizard's financials section must be legible to an operator working with their accountant's instructions.
- **Property owners** — for accounts managing on behalf of third parties, owners are an object of configuration (bulk uploaded, never invited in V1) rather than a user.

---

## 4. Product Thesis

The product is **not a setup checklist. It is a guided implementation system delivered through a wizard UI.**

A checklist tells customers what to do. A guided implementation system helps customers and specialists turn the customer's business into a working operating model.

For V1, this means:

- The customer starts by selecting a **launch intent**, not by filling configuration fields.
- The wizard **scopes the first launch** before asking the customer to configure.
- **Airbnb view-only sync** turns the platform from empty software into a mirror of the customer's real business.
- Guesty provides **opinionated defaults**, so the customer confirms or edits instead of starting from blank.
- Configuration happens **before Call 1**, so the specialist call becomes review and validation instead of walkthrough.
- The output is not "steps completed." The output is **a customer who is synced, oriented, and review-ready**.

### Core Principle

The wizard is **editable infrastructure, not education content**. Every wizard step must create durable onboarding value: either writing configuration to the live account, capturing decision context for the specialist, or resolving cold-start orientation.

This is intentionally broader than "every step writes configuration." Some valuable steps — intent selection, migration gate, feature interests, governance capture — do not configure product settings but capture high-value onboarding context that the specialist needs.

### Architectural Benchmark: monday.com's Hybrid Onboarding

The closest benchmark for this design is monday.com's hybrid onboarding model, where the product owns 60–80% of initial configuration (templates, automations, defaults) and the CSM owns scoping, validation, and governance. The product is the build layer; the CSM is the review layer. This is the model the wizard adapts for Guesty Pro SMB — with the key adjustment that the SMB owner-operator absorbs the customer-side roles that monday's model assumes are separate.

---

## 5. V1 Product Concept

V1 has **five core modules**.

### Module 1: Launch Path

The customer selects what they are trying to launch first and whether they are starting fresh or migrating existing operations.

This includes:
- **Intent selection** — *"What is the first operational workflow you need to launch?"*
- **Migration gate** — *"Are you starting fresh or migrating existing operations?"*
- **Launch path / preset selection** — Fast Launch, Migrate Existing, Channel Sync, Payments First, Team Operations
- **Early risk surfacing** for complex migrations (flagged for specialist review before the customer proceeds)

The goal is to **scope before configuring**.

### Module 2: Cold-Start Resolution

The customer safely connects Airbnb in view-only mode.

The wizard makes the safety explicit:
- nothing changes on Airbnb
- listings are not edited
- pricing is not changed
- availability is not changed
- the import is read-only

After connection, Guesty shows the customer's real listings, bookings, and messages. **This is the AHA moment** — the moment Guesty stops being software and starts being the customer's business.

### Module 3: Core Call 1 Preparation

The customer confirms or edits Guesty's recommended defaults for the setup areas most relevant before Call 1:

- **Operations setup** — confirm-or-edit defaults for housekeeping, cleaning schedule, inspection workflow
- **Financial setup** — fees (curated to the 4 most common, not the full 200+), cancellation policy, revenue calculation, payment automation
- **Feature interests** — what the customer wants to focus on, used to personalize Call 1's agenda

The goal is **not to finalize every setting**. The goal is to give the specialist a meaningful starting point.

### Module 4: Ownership and Governance

The wizard captures who owns the account, financial decisions, and go-live approval.

For most SMBs this is one person, so the default path is simple:

> *"I'm the admin, financials owner, and go-live approver."*

The purpose is to create a lightweight governance record for the specialist — not a full role-assignment system.

### Module 5: Readiness and Handoff

The wizard ends with a readiness summary and a platform handoff.

The customer enters Guesty for the first time with:
- real listings visible
- calendar populated
- inbox populated
- configuration started
- Call 1 agenda clearer

The handoff should make the customer feel that **Guesty is no longer blank**.

### Additional Prep (post-suggested path, time-permitting)

After the suggested pre-Call-1 path, the wizard can offer additional prep steps for motivated customers who want to get ahead. Examples: Booking Engine basics, Owner Prep, Logo upload, GuestyPay application start, Historical Data prep, Rate Strategy input.

These are **not the core proof of V1**. They are acceleration opportunities. The primary V1 proof remains Airbnb sync and Call 1 readiness.

---

## 6. What V1 Must Prove

### MVP Hypotheses

1. **H1.** If customers connect Airbnb before Call 1, they are more likely to return to Guesty before the call and less likely to arrive cold.
2. **H2.** If the wizard captures launch intent and migration complexity before Call 1, specialists can personalize the first session and identify high-risk accounts earlier.
3. **H3.** If customers see real listings, bookings, and messages before entering the full platform, cold-start abandonment will decrease.
4. **H4.** If operations and financials are pre-filled with confirm/edit defaults, customers will complete more meaningful pre-work than they do today in Rocketlane (~0% baseline).
5. **H5.** If Call 1 becomes review instead of walkthrough, Guesty can reduce session count without degrading post-graduation retention.

### What "Ready for Call 1" Means

V1 does not try to make the customer fully live without a specialist. It produces a customer who is **ready for a higher-quality Call 1**.

> **Important: Nothing in this flow is mandatory.** Customers can enter Guesty at any point without completing any step — including scheduling a call. The entire wizard, including call booking, is a strong suggestion, not a requirement. Customers who skip steps or don't book a call will automatically receive reminder emails prompting them to do so.

**Strongly suggested (all optional — customers may enter Guesty at any time):**
- The customer selected a launch path
- The customer answered the migration gate
- Airbnb view-only sync is complete
- Call 1 is booked (if not booked, the customer receives automated reminder emails)

**Also strongly suggested:**
- Operations setup has been started or completed
- Financial setup has been started or completed
- Governance owner is captured
- Feature interests are selected

**Specialist should know before the call:**
- Whether the account is starting fresh or migrating
- Whether Airbnb sync succeeded
- How many listings were imported
- Whether financials need review
- Whether the customer marked anything as "not sure"
- Which features the customer cares about most
- Whether any migration complexity was flagged

The intended outcome is a better first specialist session: **less walkthrough, more review.**

### Airbnb Sync as Activation Gate, Not Full Readiness

For MVP, Airbnb view-only sync is the **primary activation gate**. It is **not** the full definition of onboarding readiness.

It proves that the wizard resolved the cold-start problem, created early customer investment, and gave the specialist something real to review on Call 1.

A customer who completes Airbnb sync is not necessarily ready to go live. They are **no longer starting from zero**.

### Reframing Session Compression

The existing organizational plan is to compress onboarding from ~7–8 sessions (kickoff + 6–7 follow-ups) to 5 sessions (Setup Call + 4 follow-ups), eliminating the standalone kickoff call.

The wizard's role in this is precise:

> The wizard creates the conditions required to safely remove the standalone kickoff call. It absorbs the orientation function of that call and reduces walkthrough load on Call 1. Session compression is the downstream operational outcome — not the immediate product proof.

The immediate product proof is a better Call 1. If that succeeds, the operational decision to remove the kickoff call becomes safer.

---

## 7. Success Measures

### Primary V1 Activation Metric

**Airbnb view-only sync before Call 1**

> Target: more than **80%** of new Guesty Pro SMB accounts complete Airbnb view-only sync before their scheduled Call 1.

Why it matters: Airbnb sync is the AHA moment and the clearest proof that the wizard solved the cold-start problem.

### Supporting Product Metrics

Track and report; establish baselines in the first 90 days. No hard targets at launch.

- Wizard start rate
- Intent selection completion
- Migration gate completion
- Airbnb sync start rate
- Airbnb sync completion rate
- Airbnb sync failure rate
- Operations setup completion
- Financial setup completion
- Feature interest selection
- Readiness summary viewed
- Platform handoff clicked
- Returning-user resume rate
- Per-step drop-off (flag any step >25%)

### Call Quality Metrics

- Specialist-reported Call 1 quality score (1–5 post-call rating)
- % of Call 1 spent on review vs. walkthrough
- % of customers arriving with Airbnb synced
- % of customers arriving with financials or operations already started
- Number of unresolved blockers discovered during Call 1

### Business Outcome Metrics

Lagging indicators — measure after at least one full onboarding cycle (~8–12 weeks post-launch).

- Average specialist sessions per SMB onboarding (current ~7–8 → target ≤5)
- SMB onboarding duration (current 30–100+ days → target ≤20 days SLA)
- SMB on-time graduation rate (current 18% → directional improvement)
- Silent / inactive / non-responsive churn trend (current ~49.4% → directional reduction; treated as lagging signal, not primary proof)
- Post-graduation 3-month MRR churn

### Guardrail Metrics

The wizard should not improve speed at the cost of quality.

- No degradation in 3-month post-OB MRR churn (must stay ≤3%)
- No increase in support tickets caused by misconfiguration
- No increase in Call 1 confusion
- No increase in Airbnb connection anxiety or failed-connection recovery issues

### KPI Ownership

Core outcome metrics (Activation, Call Quality, Business Outcome) are **shared between Product and CSM** — neither team owns them alone. Supporting Product Metrics and Guardrails are Product's continuous improvement signals.

---

## 8. Explicit Boundaries

### What V1 Does Not Solve

- Onboarding team capacity
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

### What V1 Does Solve

- The blank state before first platform entry
- Lack of clear pre-Call-1 action
- Missing launch intent
- Missing migration complexity signal
- Customer anxiety around Airbnb sync
- Lack of meaningful specialist prep before Call 1
- The absence of a simple readiness summary for the customer

### Out-of-Scope Features (deferred to V2 or other initiatives)

- Notification settings configuration (V2)
- Consent to configure on behalf (legal/product alignment pending)
- Pre-population pipeline (separate in-flight initiative; V1 is forward-compatible)
- Owner invites (V1 captures owners; sending invites is V2)
- OTA integrations beyond Airbnb (Booking.com, VRBO/Expedia — Call 2 scope)
- Automated messages, Guest App, Auto Tasks, Inbox setup (Call 3 scope)
- Full-fidelity readiness dashboard for customers (V2 — see Future Direction)
- Full CSM Review Mode (V2 — see Future Direction)

### Open PRD Questions

- **Wizard-vs-pre-population scope split.** Which configuration domains are wizard-only, pre-pop-only, or hybrid?
- **Activation-check definition per task.** What counts as "complete enough" for each step?
- **Migration gate depth in V1.** Is V1's migration handling: (a) warning + CSM flag only, (b) lightweight guided import for listings-only, or (c) full migration tracks? Likely (a) or (b) for V1.
- **Governance capture format in V1.** Single acknowledgement, inline questions, or derived from preset?
- **SLA visibility in V1.** Is any time-awareness ("Your Call 1 is in 3 days") in V1, or strictly deferred?
- **Preset distribution validation.** Do real Guesty Pro SMB accounts actually sort cleanly into the five presets?

---

## 9. Future Direction

If V1 succeeds, the wizard can evolve into a full **onboarding momentum-control system** that covers the entire onboarding journey, not just the pre-call gap.

Future capabilities may include:

1. **CSM Review Mode** — Readiness, blockers, activity, and SLA risk for specialists. Same underlying state as the customer-facing wizard, exposed through a diagnostic operating view.
2. **Blockers as first-class objects** — Blocker type, owner, due date, impact, and resolution path captured as structured records rather than scattered across calls and Slack.
3. **Readiness gates** — Validation that the account is operationally ready (listings active, channel connected, payments complete, no critical blockers open), not just that wizard steps were touched.
4. **Silent-customer detection** — Signals for inactivity, skipped critical steps, or no return before Call 1, routed to the right intervention.
5. **Pre-population integration** — Guesty fills more fields automatically; the customer confirms or edits. Reduces wizard time and raises completion rates.
6. **Segment expansion** — Adapting the same framework to mid-market accounts with multiple stakeholders. Reintroduces role-based access, task assignment, and full Setup/Review/Governance separation. Migration tracks for complex PMS-to-Guesty moves also belong here.
7. **Graduation handoff artifact** — A structured summary at graduation that connects wizard output to post-graduation CSM action:

   ```
   Graduation summary for [Account]

   Completed:
   - Listings imported
   - Primary channel connected
   - First users invited
   - Payments setup completed

   Risks:
   - Accounting not configured
   - GuestyPay not activated
   - Customer has low login frequency

   Recommended CSM follow-up:
   - Review payments adoption in 14 days
   - Schedule accounting setup
   - Check first booking cycle
   ```

8. **Asymmetric UX** — Customer always sees a simplified, opinionated surface ("3 things left before launch"). Onboarder sees a diagnostic operating view (SLA risk, blockers, next best action). Same underlying state; presentation split by audience.
9. **Commercial opportunity prompts** — Upsell surfaces (particularly GuestyPay) introduced only after core activation milestones, never during setup.
10. **Preset library expansion** — V1 ships with five presets. Over time the library expands by vertical (urban STR vs. vacation vs. serviced apartments), by OTA configuration, and by team composition.

The V1 architecture should support these directions, but **V1 should not attempt to build all of them**.

---

## Appendix: Copy Direction

A short reference for the PRD and design phase. These set the tone for V1.

### Setup language → Call 1 readiness language

- ✅ *"Let's get your account ready for your first session."*
- ✅ *"You can start using Guesty now — or take a few minutes to prepare first."*
- ❌ *"Complete your setup."*
- ❌ *"You must finish these steps before continuing."*

### Review-ready framing

- *"Saved for your specialist to review."*
- *"Your account is no longer blank."*
- *"Your business is now visible inside Guesty."*
- *"This gives your specialist a starting point."*
- *"We'll flag this for your first session."*

### Safety-first framing

**Airbnb sync:**
> *"Nothing changes on Airbnb. We can only view your listings, reservations, and messages. We cannot change your pricing, calendar, availability, or listing content from this step."*

**Owner Prep:**
> *"No owner invitations are sent. You're only saving owner records so they are ready later."*

**Migration:**
> *"This does not move your full history yet. It tells your specialist what needs review before go-live."*
