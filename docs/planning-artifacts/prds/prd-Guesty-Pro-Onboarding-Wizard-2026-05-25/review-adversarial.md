---
title: "Adversarial Review — Guesty Pro Onboarding Wizard PRD"
reviewer: Adversarial reviewer (BMAD `bmad-review-adversarial-general` skill)
date: 2026-05-25
target: docs/planning-artifacts/prds/prd-Guesty-Pro-Onboarding-Wizard-2026-05-25/prd.md
posture: Cynical. Assume problems exist. Find what's missing, not just what's wrong.
---

# Adversarial Review

## Verdict

The PRD is well-organized, glossary-disciplined, and tracks its assumptions honestly — it survives as a *document*. But as a **product bet**, it leans on three load-bearing premises that are not empirically supported in the artifact: (a) the AHA-moment thesis (Airbnb OAuth first); (b) the conviction that a populated dashboard will convert engagement where Rocketlane did not; (c) the role-collapse-justifies-opinionation argument. The PRD also locks numeric targets (>80% sync, ≤5 sessions, ≤20 days) onto baselines it explicitly admits are 22+ days stale. If any one of the three premises is wrong, V1 ships with the same ~0% engagement Rocketlane already produces — and the PRD has no instrumentation strategy that would let you find out *which* premise broke before the post-launch retro.

Recommendation: **do not lock the PRD until SM targets are decoupled from stale baselines and at least one falsifiability mechanism is added for the AHA-moment hypothesis.**

---

## CRITICAL Findings

### C-1. The "engage where Rocketlane didn't" premise is asserted, not argued.
**Location:** §1 Vision; Brief §2; Addendum §1.
**Challenge:** Rocketlane sees ~0% pre-Call-1 engagement. The Wizard's job is to *not* be 0%. The PRD never articulates the causal differentiator beyond "Typeform UX + AHA moment." That is a UI hypothesis dressed as a strategy. If the root cause of Rocketlane's failure is *customer non-engagement* (they're working, their guests are real, the call hasn't happened yet), the surface won't matter. The PRD does not enumerate why Rocketlane fails — is it (i) the surface, (ii) the lack of OAuth-as-anchor, (iii) lack of in-product placement, (iv) lack of consent-gated automation, (v) the customer fundamentally doesn't have time? — and therefore cannot claim its replacement will succeed on any specific differentiator.
**Counter-position:** Add a §2 "Why this won't be another Rocketlane" subsection enumerating the *specific* causal differences. If the PM can't write that subsection with conviction, V1 is a UI re-skin with a strategy story attached.

### C-2. SM-1 >80% Airbnb sync is an asserted ceiling, not a calibrated target.
**Location:** §7 SM-1; Brief §6.
**Challenge:** The current pre-Call-1 engagement is ~0%. Jumping to 80% in V1 — for a *single* metric that requires OAuth (a high-friction step where security-sensitive operators historically resist) — is heroic. There is no benchmark cited: no monday.com sync rate, no comparable SaaS OAuth-in-onboarding rate, no internal A/B basis. The 80% is the kind of number a sponsor wants on a slide. The counter-metric SM-C3 ("Wizard sync rate alone without downstream activation is a vanity metric") implicitly admits this — but the PRD still picks 80% as the headline.
**Counter-position:** State the target as a *range with a confidence interval* — e.g., "We expect 40–65% sync at V1; >80% is the V2 target after iterating on Cover Screen and OAuth-explainer copy." If 80% is genuinely the floor, cite the benchmark.

### C-3. SM-10, SM-11, SM-12, SM-13 targets are locked against baselines the PRD admits are 22 days stale.
**Location:** §7 SM-10/11/12/13 with `[ASSUMPTION: baseline inherited from May 3 brief; verify]`; §17.
**Challenge:** ≤5 sessions, ≤20 days, directional 18%→better, directional 49%→reduction. Each `[ASSUMPTION]` flag acknowledges the baseline is stale. You cannot lock a target against an unverified baseline; you can only lock a *delta*. Worse: SM-10 and SM-11 are 8–12 week lagging signals against baselines that are already 3+ weeks behind. By the time the PRD ships and engineering builds, the baseline is 4+ months old.
**Counter-position:** Refuse to lock the PRD until §16 Open Q6 (KPI baseline refresh) is closed. Re-pull the data this week. Then re-state targets as *deltas* (e.g., "reduce sessions per onboarding by ≥25%") so they remain valid as baselines drift.

### C-4. Profile Output Schema deferral is a structural risk, not just a "deferred deliverable."
**Location:** §0; FR-44; §6.2; §15 risk table.
**Challenge:** The PRD admits engineering cannot begin write implementation until the schema is locked. But the rest of the PRD (FR-43, FR-45, FR-47, FR-49) is written *as if* the write semantics are known. If the schema discovers that, say, message-template activation requires a state-machine the existing API doesn't support, FR-21 collapses. If payment policy writes can't be made idempotent (FR-45), FR-30 collapses. The schema work is **deeply coupled** to the FRs, not a downstream mapping exercise. Treating it as a post-PRD artifact misrepresents the dependency graph.
**Counter-position:** The Profile Output Schema is not a "companion artifact" — it is a precondition for PRD validity. Either inline the schema, or downgrade the PRD's status from "draft v1, ready for review" to "draft — pending schema lock."

### C-5. The "fresh data on re-entry but don't re-route retroactively" rule is a UX time bomb.
**Location:** FR-11, FR-12; UJ-6.
**Challenge:** The PRD says (a) re-poll Airbnb on every entry, (b) overwrite cached values, (c) do NOT retroactively re-route earlier branches, but (d) "flag the changed signal in §8 summary." The user is now in a state where: they answered Q1.2 routing based on "check-in in 14 hours," that check-in has now happened and is gone, but Section 5 was prioritized as if it was still imminent. The summary's "this signal changed" footnote is the worst of both worlds: the *system* didn't change behavior, the *summary* acknowledges the data did. That makes the system look broken to the user ("why am I being routed to Financials urgently when the check-in already happened?").
**Counter-position:** Either commit to (i) retroactive re-routing with a "we updated your path because data changed" notice, or (ii) snapshot-at-first-sync semantics with NO re-poll. The hybrid stance is the worst option.

---

## HIGH Findings

### H-1. Role-collapse argument is asserted from intuition, not data.
**Location:** §2.1 Critical design constraint; Brief §3; Addendum §2.
**Challenge:** The role-collapse table in Addendum §2 is a model, not data. There is no citation that SMB Guesty Pro customers actually collapse executive sponsor + admin + champion into one person. The personas (2A, 2B) presumably support this, but the PRD never quotes them, never cites a sample size, never says how many SMB accounts have a single user vs. multiple seats. If even 20% of SMB accounts have a delegating owner-operator who hands off to a VA or family member, the "Wizard must make PM-decisions" framing under-serves them. This is the kind of premise that, if wrong, invalidates the design's opinionation.
**Counter-position:** Cite the data. How many SMB Pro accounts have one user vs. >1? How many have admin role separation? If the answer is "we haven't checked," that's a phase-blocker, not a footnote.

### H-2. Desktop-only V1 is a strategic miss for owner-operators.
**Location:** §6.2; §8 NFRs; §15 risks.
**Challenge:** Owner-operators run their business from phones. They check Airbnb messages on phones. They book Setup Calls on phones. The PRD's own UJ-2 (David, urgent check-in in 14 hours) is *exactly* the user who'd open the Wizard email on his phone between guests. The "best experienced on desktop" landing page (§15 mitigation) is the kind of friction that pushes engagement back toward 0%. The PRD does not estimate what % of pre-Call-1 sessions originate on mobile. If it's >30%, V1 is undermining its own SM-1 target.
**Counter-position:** Either (i) make V1 mobile-responsive at minimum (no native, but no desktop-only gate), or (ii) cite the mobile-share data that justifies the deferral. Adding "best experienced on desktop" copy is a tax, not a mitigation.

### H-3. SM-7 and SM-8 rely on CSM behavior change that the PRD does not own.
**Location:** §7 SM-7, SM-8; §14 CSM training.
**Challenge:** SM-8 targets a shift from "~80% walkthrough" to ">50% review-and-strategy" within 12 weeks. That is *CSM behavior change*, not Wizard output. The PRD assumes a 30-minute training session + FAQ will retool CSM habits. CSM teams adapt slowly; if CSMs default to their existing Call 1 walkthrough because it's safer, SM-8 misses regardless of Wizard quality. The Wizard could be perfect and SM-8 still fails. The PRD doesn't own the CSM playbook revision.
**Counter-position:** SM-7 and SM-8 should be co-owned with explicit CSM-Leadership accountability and a CSM-side artifact (revised Call 1 agenda template) listed as a §13 dependency, not a §14 training note.

### H-4. The "they just booked a real call, they're committed" premise (Addendum §4) is not falsifiable as stated.
**Location:** Addendum §4 reason 2; PRD §2.2 emotional JTBD.
**Challenge:** The brief argues that because the customer booked a real call, they are "already committed" and therefore Airbnb-first is safe. But the entire problem statement is that ~0% engage with Rocketlane *after booking a real call*. The booking did not produce commitment in the Rocketlane evidence. The PRD reuses the booking-as-commitment claim to justify the AHA-moment design without acknowledging that this exact claim has already been disproven in the Rocketlane data.
**Counter-position:** Either reconcile (booking does/doesn't produce commitment) or remove this argument from the design rationale.

### H-5. Skip Intercept tier copy is opinionated and unvalidated.
**Location:** §4.7 FR-35–FR-38; V4 spec.
**Challenge:** The tier copy ("I totally get it…," "You're 80% set…") is voiced, casual, and assumes a tone the customer will receive as friendly rather than manipulative. There is a meaningful risk that Tier 1's "Give me 10 seconds…" reads as wheedling, increases reactance, and *raises* abandonment. The PRD treats this copy as fixed (V4 is source of truth) without any A/B framing, copy-test plan, or guardrail. SM-C2 says "don't optimize for completion" — but if the intercepts *cause* completion drops, you'll attribute that to the wrong cause.
**Counter-position:** Add an explicit A/B test plan for Tier 1 copy at minimum (it's the highest-leverage one). Add a counter-metric specifically for "intercept-induced abandonment" — % of Tier-1-modal-shown users who Safe Exit vs. continue.

### H-6. Live Airbnb re-poll on EVERY entry is over-engineering with unclear cost ceiling.
**Location:** FR-11; §8 NFR; §9.3.
**Challenge:** The PRD specifies live re-poll on every Wizard entry, falls back to stale cache on failure, and has a 3s P95 latency budget. But §9.3 only says "rate-limited to once per Wizard entry, not per Question render." There is no cost model. If 10,000 SMB customers re-enter the Wizard 3x each over their pre-Call-1 window, that's 30,000 Airbnb API calls *just for re-poll*. The PRD's risk table acknowledges "Live Airbnb hook adds API cost beyond budget" as Low likelihood — but offers no estimate. And FR-11's "if user hasn't completed Section 1, re-poll is a no-op" suggests engineering doesn't yet know when to poll vs. not.
**Counter-position:** Either (i) demand a cost estimate from engineering before locking FR-11, or (ii) downgrade to "re-poll if last poll >N minutes ago." The "every entry" rule is naive.

### H-7. Accountant Secure Link is a new sub-surface with disproportionate build cost.
**Location:** §4.5 FR-27–FR-29; UJ-4.
**Challenge:** The Stripped Section 5 View is a *new authenticated surface* with its own token system, scoped data exposure rules (FR-29 industry/currency exposure), expiry policy, separate UI shell (no header, no nav), and email infrastructure. For what is presumably a single-digit percentage of SMB operators who actually delegate financials to an external accountant. The PRD never estimates this share. The build cost is non-trivial — secure tokens, scoped session, separate UI, legal/security review. Is the value worth the cost in V1?
**Counter-position:** Either (i) provide the data that says >X% of SMB operators delegate financials to a named external accountant (and that X justifies the build), or (ii) defer the Accountant Link to V2 and let V1 operators self-complete Section 5 or skip. The current PRD treats this as a marquee V1 feature without supporting data.

### H-8. The PRD only addresses pre-Call-1 — but post-Call-1 momentum is what produces graduation.
**Location:** §1; §6.1; §7 SM-11, SM-12.
**Challenge:** The strategic thesis is "convert the dead zone before Call 1," but SLA graduation is 20 days *after sign-up* and the dead zone is days 0–N pre-Call-1. After Call 1, the customer still has to add the rest of their listings, integrate channels beyond Airbnb, set up actual GuestyPay, etc. The PRD does not address whether the Wizard's momentum survives the Call 1 handoff into the rest of the journey. SM-11 (≤20 days) implicitly bets it does. There is no mechanism in the PRD that ensures post-Call-1 continuation.
**Counter-position:** Acknowledge explicitly: "The Wizard improves Call 1 quality but does not guarantee post-Call-1 completion. SM-11 may not move even if SM-1 does." Or expand scope to address post-Call-1.

### H-9. ~0% Rocketlane engagement could mean the customer never sees the link — not that they reject the surface.
**Location:** §1; Brief §2.
**Challenge:** The PRD assumes Rocketlane fails because customers don't engage with *the surface*. An alternative explanation: Rocketlane emails go to spam, are sent at the wrong time, or the customer simply doesn't open them. If the failure mode is *delivery/notification*, the Wizard inherits the same failure mode — because §14 says "no marketing campaign; no email pre-announcement" and the Wizard is reachable only via auto-redirect post-booking or a dashboard link. Customers who don't return to the dashboard before Call 1 will never see the Wizard either.
**Counter-position:** Diagnose Rocketlane's actual failure mode. If it's delivery, the Wizard needs a notification/email strategy. If it's surface, the current architecture is fine.

---

## MEDIUM Findings

### M-1. Phased rollout of 10% → 50% → 100% over 8 weeks: where does the kill switch live?
**Location:** §14.
**Challenge:** The rollout phases name guardrails (SM-C4 support tickets, SM-1, SM-2, SM-7) but no explicit kill criteria. What SM-1 number triggers "hold at 10%"? What's the rollback path if Phase 2 trips SM-C5 (3-month churn)? "Hold rollout if any guardrail breaches" is hand-wavy.
**Counter-position:** Add numeric kill criteria per phase. e.g., "Phase 2 → 3 if SM-1 ≥ 40% AND SM-C4 delta < +5% AND zero P0 incidents in 14 days."

### M-2. UJ-1 "Maya completes in 6 minutes" sets an expectation the FRs don't validate.
**Location:** §2.4 UJ-1.
**Challenge:** Six minutes for 9 screens + OAuth + multiple multi-select Questions is fast. The PRD never validates this timing assumption against the V4 question count and copy-length. If the realistic median is 12 minutes, the cover-screen framing ("3–10 minutes") is wrong and resume rate (SM-4) will be higher than expected.
**Counter-position:** Time-box the V4 flow with a paper prototype before launch. Update Cover Screen copy if needed.

### M-3. FR-7 (server-authoritative branching) and FR-9 (2-second write) imply non-trivial server complexity that no FR enumerates.
**Location:** FR-7, FR-9.
**Challenge:** Server-authoritative branching means the server computes branch state on every interaction and the client renders accordingly. With FR-9's 2-second write deadline + FR-11's 3-second re-poll latency + FR-7's server evaluation per branch, the per-interaction request load is non-trivial. The PRD does not specify whether the branching engine is a separate service, where state lives, or how it interacts with the (deferred) Profile Output Schema. This is hidden in "architecture's problem" but it is a PRD-scope constraint.
**Counter-position:** Add an architectural sketch as a §11 sub-section or defer FR-7's server-authoritative claim to architecture review.

### M-4. Consent revocation default (FR-46) commits to a behavior legal hasn't reviewed.
**Location:** FR-46.
**Challenge:** The PRD writes "If a customer revokes consent post-Wizard, writes already made remain in place; future writes are blocked." This is a legal posture, not a product choice. Different jurisdictions (e.g., GDPR) may require rollback. Picking the no-rollback default in the PRD risks engineering building one behavior and legal demanding another.
**Counter-position:** Mark FR-46 as **PROVISIONAL — legal review required** explicitly in the FR body, not just in §16.

### M-5. "Mean configured items per completed flow" (SM-6) is a perverse incentive.
**Location:** SM-6.
**Challenge:** Higher mean configured items = more dashboard activation evidence. But the V4 flow has a fixed number of Questions, and answering more of them = configuring more = higher SM-6. This conflates flow-completion with configuration depth and rewards a Wizard that prevents skips — directly contradicting the "skip-friendly with tiered resistance" principle. SM-C2 covers "sections completed" but not "items configured."
**Counter-position:** Either drop SM-6 or pair it with a "configurations the user later changed in Settings" signal, which would catch over-configuration.

### M-6. The PRD treats the 22-day stale baseline (Addendum §1) as if it's fine because it's flagged.
**Location:** §7 multiple `[ASSUMPTION]` flags; Addendum §1 "verify against current data."
**Challenge:** Flagging a stale baseline is not the same as refreshing it. The same Addendum that says "verify against current data before PRD targets are locked" is used as the source for the PRD's targets, which are now locked. The honesty of the flag does not make the data fresher.
**Counter-position:** Either refresh the data before PRD lock, or remove all numeric targets that depend on it.

### M-7. UJ-5 (Hannah, Turno + PriceLabs) auto-skips two Questions on partner detect — is Partner-array exact-match safe?
**Location:** UJ-5; FR-18, FR-34.
**Challenge:** FR-18 says partner detection is "exact-string match against `Partners` array." Real-world CRM data is messy — "Turno", "TurnoApp", "Turno Inc.", "turno", "Turno (legacy)" all exist. Exact-match will silently fail to detect 30% of legitimate Turno users, and they will see Q2.1's full options instead of the auto-skip. This is a quiet failure mode that erodes "we know your stack" trust.
**Counter-position:** Specify normalized matching (lowercase, trim, alias table). Defer string-match logic to the Profile Output Schema or a Partner Mapping artifact.

### M-8. No explicit "what does the CSM actually receive" artifact spec.
**Location:** FR-32 ("made available to the CSM (V1 via Salesforce write; V2 via dashboard widget)"); FR-41.
**Challenge:** The PRD says CSMs read Wizard outputs "via Salesforce" in V1. What field(s)? Free text? Structured? Does the CSM open a different system tab? Read a notes field? The Call 1 prep handoff is the *entire* point of the Wizard, and the PRD specifies it as "via Salesforce" without further detail. CSM behavior change (H-3) is impossible without a clear handoff artifact.
**Counter-position:** Add an FR or §11 sub-section specifying the V1 CSM-side handoff format (Salesforce field names, view, ordering). Make CSM Leadership sign it off in §12.

### M-9. The persistent header's "always visible, never the focal point" is a design instruction, not an FR.
**Location:** FR-3; §10.
**Challenge:** "Never the focal point" is unfalsifiable. How will design know they've crossed the line? How will QA test it?
**Counter-position:** Either remove this aesthetic claim from the FR body or replace it with measurable constraints (e.g., "max header height: 64px, max contrast ratio against body: 2:1 unless interacted").

### M-10. Auto-Pilot Defaults could silently mis-configure customers who Safe Exit at Tier 1.
**Location:** FR-37, FR-47.
**Challenge:** Tier 1 Safe Exit applies Auto-Pilot Defaults *without* the user having seen Sections 2–7. The customer's `payment_policy = 100% at booking` is set by Auto-Pilot, even though that customer may have wanted 50-50. The PRD says this is "conservative" — but conservative is not the same as correct. A customer who hits Skip on the cover, gets defaults, then opens Settings later expecting a blank state may be surprised to find policies already set. Counter-metric SM-C4 (support tickets) may catch this *after* it harms customers.
**Counter-position:** Either (i) require explicit acceptance of Auto-Pilot Defaults at the Tier-1 Safe Exit modal ("These defaults will be applied: 100% at booking, no automated messaging…"), or (ii) defer Auto-Pilot writes until the user takes a first action in the dashboard. Silent writes on skip are a trust risk.

---

## LOW Findings

### L-1. §17 Assumptions Index repeats every inline `[ASSUMPTION]` but adds no priority/severity field.
**Location:** §17.
**Challenge:** All assumptions are listed flat. Some are cosmetic (toast wording), some are foundational (Salesforce CRM is built). The reader cannot triage.
**Counter-position:** Add a `severity` column (blocker/high/low) — mirroring the §16 BLOCKER convention.

### L-2. The "9-screen Wizard" branding (§6.1) is inconsistent with "8 Sections + Cover" (§3).
**Location:** §6.1 vs. §3.
**Challenge:** Section 0 (Cover) is sometimes counted as a screen, sometimes as a non-Section. The PRD switches between 8 and 9 depending on context.
**Counter-position:** Pick one: "9 screens (Cover + 8 Sections)" or "8 Sections plus a Cover Screen." Use it consistently.

### L-3. FR-1 says "countdown updates at minimum once per minute" — but doesn't say what happens at T-0.
**Location:** FR-1.
**Challenge:** What happens when the Call 1 starts during a live Wizard session? Does the countdown go negative? Show "Now"? Auto-close the Wizard?
**Counter-position:** Specify the T-0 and T-negative behaviors.

### L-4. FR-33 owner CSV upload validation rules are under-specified.
**Location:** FR-33.
**Challenge:** "Required columns are `owner_name`, `owner_email`, `property_ref`. Missing required columns surface an inline error." What about: extra columns? duplicate emails? invalid emails? non-UTF-8 encoding? Excel-exported CSVs with BOM? `property_ref` matching against the user's actual listings? CSV-handling is a long-tail bug source.
**Counter-position:** Either fully specify validation in the FR or move it to an explicit CSV Spec sub-artifact.

### L-5. FR-2 consent gate: unchecking "does not revoke" but FR-46 revocation is post-Wizard via Settings — leaving a gap.
**Location:** FR-2, FR-46.
**Challenge:** Within the Wizard session, can the user revoke consent without leaving the Wizard? FR-2 says unchecking the box does not revoke; FR-46 implies revocation lives in Settings. So mid-Wizard, the only way to revoke is to leave the Wizard, navigate to Settings, revoke, and return. This is an unusual gap.
**Counter-position:** Specify intra-Wizard revocation behavior or add it to §16 as an open question.

### L-6. The "Help — what went wrong?" support article in FR-17 is `[ASSUMPTION: support article exists or will be authored]` — but no owner.
**Location:** FR-17.
**Challenge:** Who writes it? When? Without an owner, this assumption silently leaves a broken link in production.
**Counter-position:** Assign in §12 stakeholders.

### L-7. "Internationalization-ready" NFR is performative without a localization plan.
**Location:** §8 NFRs.
**Challenge:** "Copy is externalized into a localization layer" is the minimum bar. Without a target language, a translator workflow, or a copy review by a localization specialist, this NFR is a checkbox.
**Counter-position:** Either drop the NFR or commit to one target language and an i18n process owner.

### L-8. Cover Screen consent text is shown as "I authorize Guesty to configure…" — but the actual consent scope is opaque to the user.
**Location:** FR-2.
**Challenge:** "Configure my account (listings, messaging templates, payment rules) based on my responses" — but the actual set of writes is the deferred Profile Output Schema. The user is consenting to a set of writes they cannot inspect.
**Counter-position:** Provide a "See what we'll configure" expandable section on the Cover Screen consent gate. (This is also a hedge against H-3's trust risk.)

### L-9. SM-2 "drop-offs >15% from cover impression to Q1.1" is asserted as a flag threshold but not as a number to beat.
**Location:** SM-2.
**Challenge:** Inconsistent with SM-1's hard target. Some SMs have targets, some have flags. The convention is not made explicit.
**Counter-position:** Either give every SM a target OR explicitly state "Primary SM has a target; secondary SMs are observability flags."

### L-10. The PRD has no explicit "definition of done" for V1 launch.
**Location:** absent.
**Challenge:** What triggers "V1 launched"? 100% rollout per §14? SM-1 hitting target? A stakeholder sign-off? Without a DoD, scope creep is invited.
**Counter-position:** Add a §14 sub-section "V1 Launch Definition of Done" with explicit criteria.

---

## Summary Counts

| Severity | Count |
|---|---|
| Critical | 5 |
| High | 9 |
| Medium | 10 |
| Low | 10 |
| **Total** | **34** |

## The Five Most Load-Bearing Challenges

1. **C-1 — Causal differentiator from Rocketlane is asserted, not argued.** If ~0% Rocketlane engagement isn't diagnosed, V1 may reproduce it.
2. **C-2 — SM-1 >80% sync is heroic without benchmark.** The headline metric is asserted at a level no comparable artifact supports.
3. **C-3 — All business-outcome targets ride on stale baselines.** Acknowledging the stale flag is not the same as refreshing it.
4. **C-4 — Profile Output Schema is a precondition, not a companion artifact.** Treating it as deferred misrepresents the dependency graph.
5. **H-1 — Role-collapse premise is a model, not data.** The opinionation that follows ("Wizard makes PM decisions for you") is only justified if SMB customers actually collapse roles 1:1.

---

## File Path

`/Users/yair.cohen/Documents/GitHub/BMAD-METHOD/docs/planning-artifacts/prds/prd-Guesty-Pro-Onboarding-Wizard-2026-05-25/review-adversarial.md`
