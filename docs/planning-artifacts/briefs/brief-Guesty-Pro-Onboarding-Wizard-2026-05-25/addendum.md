---
title: "Addendum — Guesty Pro Onboarding Wizard (Pre-Call-1 Questionnaire)"
created: 2026-05-25
parent: brief.md
---

# Addendum

Depth and reference material that supports the brief but doesn't belong in it. The PM agent should consult this when the brief refers here.

---

## §1 — Operational Signal Detail

These signals motivate the wizard's existence and shape its KPIs. Baselines inherited from the May 3, 2026 brief; **verify against current data before PRD targets are locked**.

| Signal | Current State |
|--------|---------------|
| SMB on-time graduation rate (April 2026) | 18% on time; 69% delayed; 28.8 days average overrun against 20-day SLA |
| Specialist call volume | 31–43 hours/month against 60-hour target; higher call volume does **not** correlate with better SLA |
| 3-month post-graduation MRR churn | Apr 2026: 2.84% / May trending toward 3.88%, breaching the 3% KPI threshold |
| Silent / inactive / non-responsive / unknown churn cluster | ~49.4% of all Guesty churn (Unknown 18.5%, Non-Responsive 17.0%, Inactive/Silent User 14.0%, Silent User 4.1%) |
| Pre-Call-1 task completion in Rocketlane | ~0% — customers do not engage with the existing pre-call surface |

**Interpretation:** the wizard targets the engagement pattern behind silent and non-responsive churn — customers who stop participating before the product has a chance to work for them. Because "Unknown Reason" is a weak taxonomy bucket, reduction in the full silent/inactive/unknown cluster should be treated as a **lagging directional signal**, not the primary proof of MVP success. The primary proof is earlier in the funnel: customers returning, syncing Airbnb, completing pre-call prep, and arriving at Call 1 with real account state for the specialist to review.

---

## §2 — Role-Collapse, Expanded

The wizard's design rests on the observation that SMB Guesty Pro customers collapse three roles into one person:

| Role | Larger orgs | SMB Guesty Pro |
|------|------------|----------------|
| Executive sponsor | Separate exec who signed the contract | Same person |
| Customer admin / project lead | Dedicated PM or implementation lead | Same person |
| Process champion / end-user advocate | Power user inside the customer org | Same person |

**Implication for the wizard:** the customer cannot self-organize the way larger implementations can. The wizard must:

- Supply the sequencing (decide the order of operations for them)
- Supply the defaults (don't ask 200 questions; ask 8–10 that matter, pre-fill the rest)
- Supply the safety framing (Airbnb view-only, no auto-send messaging without consent)
- Supply the suggested/get-ahead distinction (some sections are "do now", others are "while you're here")
- Supply the readiness definition (Section 8 — "this is what's configured, this is what's pending")

This is why the wizard is **not** a checklist. A checklist tells the user what to do; the wizard makes the decisions a project manager would otherwise make.

---

## §3 — Secondary Stakeholders (not direct users)

- **Bookkeepers / accountants** — A subset of SMB operators consult an external accountant for financials setup. The wizard's financials section (Section 5) supports a delegation path: the operator can send a secure link to their accountant to complete Section 5 alone. The accountant is not a primary persona but is an explicit secondary recipient.
- **Property owners** — For accounts managing properties on behalf of third-party owners, owners are an object of configuration (Q7.1 captures owner contacts via CSV upload) rather than a user. V1 does **not** send any communication to owners; that's V2 (owner invites).
- **CSMs (Setup Specialists)** — Not direct users of the wizard, but downstream consumers. Section 6 (Call 1 Focus) and Section 8 (Handoff) both produce artifacts the CSM relies on for Call 1 preparation.

---

## §4 — Why Airbnb-First as the AHA Moment

The questionnaire's most architecturally significant decision is putting Airbnb OAuth as the **first interactive step** after the cover screen — not after a verification warm-up question.

Reasoning:

1. **The cover screen is the warm-up.** By the time the user clicks "Let's get started" they've seen the call countdown, read the context, and granted consent. They are warmed up.
2. **The user just booked a real call with a real CSM.** They are already committed. No foot-in-the-door verification ping is needed.
3. **Personalization throughout the flow depends on Airbnb data being present early.** Q1.2 routing (urgent check-in?), Q3.1 unread message count, Q3.2 check-in template, Q6.1 priority topic suggestions, Q7.2 minimum stay default, and Section 8's "What's Configured" summary all reference Airbnb data. Sync-first maximizes downstream personalization.
4. **Typeform aesthetic favors deliberate first questions, not hesitant warm-ups.** The first step should land a real commitment.

Risk: a user who fundamentally won't OAuth may bounce at step 1. The Tier 1 skip intercept addresses this — they get auto-pilot defaults and a "Finish Setup" CTA on the dashboard.

---

## §5 — Architectural Benchmark: monday.com Hybrid Onboarding

The closest existing benchmark for this design is monday.com's hybrid onboarding model — the product owns 60–80% of initial configuration (templates, automations, defaults) and the CSM owns scoping, validation, and governance. The product is the **build layer**; the CSM is the **review layer**.

This is the model the wizard adapts for Guesty Pro SMB, with one key adjustment: in monday.com's model the customer-side roles are assumed to be separate (admin, champion, end-user). In SMB Guesty Pro the owner-operator absorbs all three. The wizard compensates by being more opinionated about defaults and more aggressive about pre-fill.

---

## §6 — Copy Direction (for PRD and Design)

Tone references the PRD and design phase can lean on.

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

**Automated messaging:**
> *"We'll never send messages on your behalf without your explicit go-ahead."*

---

## §7 — V2 Future Directions (deferred, but worth keeping in mind)

These were articulated in the May 3 brief and remain valid future directions. They should not be built in V1 but the V1 architecture should not foreclose them.

1. **CSM Review Mode** — Readiness, blockers, activity, and SLA risk for specialists. Same underlying state as the customer-facing wizard, exposed through a diagnostic operating view.
2. **Blockers as first-class objects** — Blocker type, owner, due date, impact, and resolution path captured as structured records.
3. **Readiness gates** — Validation that the account is operationally ready (not just that wizard steps were touched).
4. **Silent-customer detection** — Signals for inactivity, skipped critical steps, or no return before Call 1.
5. **Pre-population integration** — Guesty fills more fields automatically; the customer confirms or edits.
6. **Segment expansion** — Adapting the same framework to mid-market accounts with multiple stakeholders. Reintroduces role-based access, task assignment, and full Setup/Review/Governance separation.
7. **Graduation handoff artifact** — A structured summary at graduation connecting wizard output to post-graduation CSM action.
8. **Asymmetric UX** — Customer always sees a simplified, opinionated surface; onboarder sees a diagnostic view. Same state, audience-split presentation.
9. **Commercial opportunity prompts** — Upsell surfaces (GuestyPay) introduced only after core activation milestones.
10. **Preset library expansion** — A wider library of launch presets by vertical (urban STR vs. vacation vs. serviced apartments).

V2 expansion direction is informed by V1 results. **Do not build V1 in a way that locks any of these out.**

---

## §8 — Source Material

The brief and questionnaire spec draw from the following inputs collected in this session:

- The user's verbal problem statement (recorded in conversation)
- [onboarding-questionnaire-v4.md](../../onboarding-questionnaire-v4.md) (this session's deliverable)
- [product-brief-Guesty-Pro-Onboarding-Wizard-2026-05-03.md](../../product-brief-Guesty-Pro-Onboarding-Wizard-2026-05-03.md) (superseded but referenced)
- Guesty Client Data Analysis V2 (`/Users/yair.cohen/Downloads/Guesty Client Data Analysis (2).md`) — the questionnaire's V2 draft
- Guesty knowledge base (`/Users/yair.cohen/Documents/GitHub/Tahini/knowledge/`): personas, domains, product model
