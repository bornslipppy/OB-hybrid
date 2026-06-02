---
title: "Reconciliation Report — Brief/Addendum vs. PRD"
created: 2026-05-25
source_brief: docs/planning-artifacts/briefs/brief-Guesty-Pro-Onboarding-Wizard-2026-05-25/brief.md
source_addendum: docs/planning-artifacts/briefs/brief-Guesty-Pro-Onboarding-Wizard-2026-05-25/addendum.md
target_prd: docs/planning-artifacts/prds/prd-Guesty-Pro-Onboarding-Wizard-2026-05-25/prd.md
status: complete
---

# Reconciliation Report: Brief + Addendum → PRD

Findings are grouped by category and severity. "Gap" = present in the brief/addendum but not reflected (or only partially reflected) in the PRD. "Covered" confirmations are noted where they were close calls.

---

## 1. Strategic Framing (§1 Vision / §1.1 Hypotheses)

### GAP-1 — Brief V1 Thesis not in §1 Vision (LOW severity)

**Source:** Brief §1 (Executive Summary) — the explicit V1 thesis statement: *"Convert the dead zone between call booking and Call 1 into a guided, single-question-at-a-time flow that connects Airbnb, captures operational defaults, and lands the customer on a populated dashboard."*

**PRD status:** §1 Vision covers the concept but does not quote or foreground the thesis statement as a single anchoring sentence. The Vision prose is close but more verbose and less punchy than the brief's stated thesis. This is a documentation alignment issue rather than a missing requirement, but a UX/copy audience may reach for the brief rather than the PRD to understand the product's north star.

**Recommendation:** Add the thesis sentence (or a paraphrase) as a callout at the top of §1, before the descriptive paragraph.

---

### GAP-2 — monday.com hybrid model not referenced in §1 (SOFT)

**Source:** Brief Addendum §5 — explicitly names monday.com as the closest existing benchmark for this design and describes the hybrid model (product owns 60–80% of initial configuration; CSM owns scoping, validation, governance; product = build layer, CSM = review layer).

**PRD status:** §1 Vision and §1.1 Hypotheses do not reference this benchmark at all. The monday.com model is the brief's stated architectural analogy for why the Wizard is designed the way it is (especially the opinionated defaults + CSM review layer split). Its absence means readers of the PRD cannot trace the "why" behind the product/CSM ownership model described in §7 SM-7/SM-8 and §12.

**Recommendation:** Add a one-paragraph "Design Benchmark" note in §1 or §1.1 citing the monday.com hybrid model, including the SMB adaptation (role-collapse adjustment → more opinionated defaults). No new FRs required; this is a strategic framing gap.

---

### GAP-3 — "Review layer / Build layer" framing absent from PRD (LOW)

**Source:** Brief Addendum §5 — explicitly frames the relationship: product (Wizard) is the **build layer**; CSM is the **review layer**. The same data, split by audience.

**PRD status:** §12 Stakeholders and §7 metrics reference CSM co-ownership and the Call 1 quality goal, but the build-layer / review-layer language is never used. This framing is load-bearing for the CSM playbook revision (§13 dependency) and for communicating the product intent to CSM Leadership.

**Recommendation:** Insert the build-layer/review-layer framing in §1 or §12 to anchor CSM sign-off conversations.

---

## 2. Requirements / FRs in Brief Not Reflected in PRD

### GAP-4 — Section 4 (Team & Governance) reduced to one sentence (MEDIUM severity)

**Source:** Brief §4 Flow Structure — Section 4 is labeled "Team & Governance: Confirm decision owner (SMB-simplified)." V4 questionnaire is the spec source. Brief's role-collapse rationale (§3, Addendum §2) specifically calls out that the wizard must "supply the sequencing, defaults, safety framing, and a readiness definition that a project manager would normally provide."

**PRD status:** §4.5 covers Q4.1 (Decision Owner confirmation) in detail, including the delegation path. However, the brief explicitly names Section 4 as "Team & Governance" — but the PRD groups Sections 4 and 5 together under "4.5 Financials with Accountant Delegation." The governance / team context for Section 4 beyond the single Q4.1 question is not elaborated. If V4 contains more to Section 4 (e.g., a team-size or role question, a governance acknowledgment), it would not be caught by the current PRD grouping.

**Recommendation:** Verify that V4 Q4.x contains only Q4.1, or, if additional questions exist in Section 4, add FRs for them. Consider splitting §4.5 header to name Section 4 and Section 5 separately for clarity.

---

### GAP-5 — "Configure with consent" design principle not reflected as an FR consequence (LOW)

**Source:** Brief §4 Design Principles #5 — *"Configure with consent — single cover-screen consent enables system-level configuration on user's behalf."* This is a named design principle.

**PRD status:** FR-2 covers the consent gate and the Consent Record. However, the design principle that the *single* cover-screen consent is the authorization for all downstream system-level writes is only implied by FR-43. The PRD does not have a clear statement that the consent model is intentionally designed to be **one consent gate for all (operator-side) writes**, as opposed to per-action consent. This matters for legal review (BLOCKER-1) and for the UX decision about per-template consent vs. cover-screen consent.

**Recommendation:** Add a clarifying note in §4.9 (or FR-43) explicitly stating that the single cover-screen consent is the PRD's intentional consent architecture for operator writes, per the Design Principles, and that per-action consent is not the V1 model. This closes a potential ambiguity for the legal reviewer.

---

### GAP-6 — Auto-Pilot Defaults: brief says "applied on skip"; PRD requires Acceptance Modal (potential tension)

**Source:** Brief §5 In Scope — *"Auto-pilot defaults applied on skip (see V4 spec, Appendix B)."* This wording implies automatic application.

**PRD status:** FR-37.1 explicitly requires an Auto-Pilot Acceptance Modal before any defaults are written (except Tier 4 and the no-consent-record case). This is an intentional V1 decision (post-reviewer-gate) that makes the application *not* automatic.

**Assessment:** This is not a gap but a deliberate divergence from the brief. The PRD is more conservative than the brief's original "applied on skip" language. However, the brief never explicitly says "automatically apply without confirmation," and the brief's Design Principle #6 (Safe defaults always) is consistent with the modal approach.

**Recommendation:** Document the divergence explicitly in the PRD's §18 Change Log or in a footnote at FR-37.1, noting that the "applied on skip" brief language was interpreted as requiring the Acceptance Modal. This prevents a future reader from thinking the brief was missed.

---

### GAP-7 — Profile output schema as "separate artifact before engineering" is not framed as Phase 0 gate in the brief (LOW, already resolved in PRD)

**Source:** Brief §5 Out of Scope — *"Profile output schema — deferred; to be defined as a separate artifact before engineering implementation begins."* Brief Open Question #1 mirrors this.

**PRD status:** FR-44 and §14 Phase 0 correctly elevate this to a Phase 0 precondition (not just "deferred"). This is actually a case where the PRD is *stronger* than the brief. However, the brief's Open Question #1 is listed as a brief open question — the PRD's §16 shows it as BLOCKER-4. The reconciliation between the brief's "deferred" language and the PRD's "Phase 0 gate" is not called out explicitly.

**Recommendation:** No change needed to the PRD. But note for the record that BLOCKER-4 in §16 resolves Brief Open Q#1.

---

### GAP-8 — Resume granularity: brief says "last-completed section or last-answered question?" (SOFT)

**Source:** Brief Open Question #2 — *"Resume from last-completed section or last-answered question? UX implication for state persistence."*

**PRD status:** FR-10 resolves this: *"resume returns the user to the Question immediately following the last Question they answered."* This is a per-Question resume, not a per-Section resume. However, §16 does not explicitly close Brief Open Q#2 as resolved. The open question index in §16 does not cross-reference the brief's numbered open questions at all.

**Recommendation:** Add a note in §16 (or a cross-reference) that Brief Open Q#2 is resolved by FR-10 (per-Question resume). Similarly for other brief open questions that the PRD has resolved. This creates a clean audit trail.

---

### GAP-9 — Accountant delegation surface: what does the accountant see? (MEDIUM, partially addressed)

**Source:** Brief Open Question #4 — *"What does the accountant see on the secure link in Q5.1? Same questionnaire scoped to Section 5? Or a different surface entirely?"*

**PRD status:** FR-28 (Stripped Section 5 View) answers this question in detail — it's a separate, token-gated URL with only Section 5 content, a context header, and accountant-scoped consent. The brief's open question IS resolved. However, §16 does not explicitly cross-reference this as closed. Same pattern as GAP-8.

**Recommendation:** Same as GAP-8 — close Brief Open Q#4 explicitly in §16, citing FR-28.

---

### GAP-10 — Brief Open Q#9 (Baseline data refresh) not fully closed in §16 (BLOCKER, partially)

**Source:** Brief Open Question #9 — *"Several baselines inherited from the May 3 brief are 22 days old — verify against current data before PRD locks targets."*

**PRD status:** BLOCKER-6 in §16 shows a partial resolution — some baselines were refreshed on 2026-05-25 (SM-12 on-time rate, median duration, backlog overdue rate, 60-day post-graduation churn), but SM-10 (specialist sessions baseline) and SM-11 (days to first value baseline) remain open. The brief's question is not fully answered. This is correctly tracked as a partial resolution in §16, but the specific two remaining sub-items (SM-10 and SM-11 baselines) are not listed explicitly enough for whoever owns baseline refresh to act on them.

**Recommendation:** Add a bullet in BLOCKER-6 explicitly naming the two remaining sub-items: (a) SM-10 specialist sessions per onboarding baseline, (b) SM-11 days to first value / onboarding duration baseline. Owner assignment and due date (before Phase 0 closes) should be added.

---

## 3. Qualitative Signals / Copy Direction (Addendum §6 → PRD §10)

### GAP-11 — "Review-ready framing" copy examples present in §10 but not complete (LOW)

**Source:** Brief Addendum §6 — provides two sets of copy directions with explicit examples:
1. **Setup language → Call 1 readiness language** (4 examples, 2 use / 2 avoid)
2. **Review-ready framing** (5 specific phrases): *"Saved for your specialist to review," "Your account is no longer blank," "Your business is now visible inside Guesty," "This gives your specialist a starting point," "We'll flag this for your first session."*
3. **Safety-first framing** for three specific surfaces: Airbnb sync, Owner Prep, Automated Messaging (with verbatim copy)

**PRD status:** §10 Aesthetic and Tone references Brief Addendum §6 directly for copy direction and quotes the use/avoid examples and the safety-first phrasing. However:
- The five "Review-ready framing" phrases are **not** reproduced or cited in §10. They appear in the addendum but §10 only quotes the use/avoid and safety-first groups.
- The safety-first framing for **Owner Prep** ("No owner invitations are sent. You're only saving owner records so they are ready later.") is not reflected in FR-33 (Q7.1 owner contacts upload), which specifies the behavior but does not reference this verbatim safety framing as a copy constraint.

**Recommendation:**
(a) Add the five "Review-ready framing" phrases to §10, or at minimum add a pointer to Addendum §6 "Review-ready framing" block so the UX team knows to apply them.
(b) Add a copy note to FR-33 citing the Owner Prep safety-first framing from Addendum §6 as a required UX constraint on Q7.1 confirmation copy.

---

### GAP-12 — Bot UX "stylized text bubble" visual treatment underspecified relative to addendum intent (SOFT)

**Source:** Brief Addendum §6 — describes copy direction in a "System (Bot):" framing. The addendum's tone references (calm, conversational, embedded "why") are for the bot voice.

**PRD status:** §10 references the bot UX surface as a "stylized text bubble (typography-driven, not an avatar character)" and states it is "defined once visually; used consistently." §16 INVESTIGATE-32 marks the "Bot UX surface visual treatment refinement" as a post-Phase-2 question.

**Assessment:** This is adequately deferred for UX; no FR gap. The PRD correctly defers to UX for visual finalization while preserving the key constraint (no avatar). Low risk.

---

## 4. V2 Deferrals (Addendum §7) — Confirm Presence in §5 / §6.2

Full check against all 10 V2 items in Addendum §7:

| # | Addendum §7 V2 Item | In PRD §5 Non-Goals | In PRD §6.2 Out of Scope |
|---|---|---|---|
| 1 | CSM Review Mode | ✅ (§5 "does not implement CSM Review Mode in V1 (V2)") | ✅ (§6.2) |
| 2 | Blockers as first-class objects | ✅ (§6.2 — "Blockers as first-class objects, readiness gates, silent-customer detection") | ✅ |
| 3 | Readiness gates | ✅ (included in §6.2 item above) | ✅ |
| 4 | Silent-customer detection | ✅ (included in §6.2 item above) | ✅ |
| 5 | Pre-population integration | ✅ (§6.2) | ✅ |
| 6 | Segment expansion (mid-market) | ✅ (§5: "does not support multi-role SMB accounts beyond the single Q4.1 + Q5.1 delegation in V1") and §6.2 "Mid-Market / SME flow" | ✅ |
| 7 | Graduation handoff artifact | ❌ **NOT FOUND** | ❌ **NOT FOUND** |
| 8 | Asymmetric UX (customer simple / onboarder diagnostic) | ❌ **NOT FOUND** | ❌ **NOT FOUND** |
| 9 | Commercial opportunity prompts (GuestyPay upsell) | ✅ (§5: "The Wizard is not a GuestyPay activation funnel") and §6.2 | ✅ |
| 10 | Preset library expansion | ❌ **NOT FOUND** | ❌ **NOT FOUND** |

### GAP-13 — Three V2 deferrals from Addendum §7 are absent from §5 and §6.2 (MEDIUM)

**Missing V2 items:**

**a. Graduation handoff artifact (Addendum §7, item 7):** *"A structured summary at graduation connecting wizard output to post-graduation CSM action."* Not mentioned in §5 or §6.2. Note: this is distinct from the CSM Handoff Artifact (FR-32.1), which is a pre-Call-1 artifact. The graduation handoff would be a V2 surface produced at the end of the full onboarding journey (not just pre-Call-1). Its absence from §5/§6.2 creates ambiguity about whether V1 is intended to produce anything at graduation.

**b. Asymmetric UX / Diagnostic view (Addendum §7, item 8):** *"Customer always sees a simplified, opinionated surface; onboarder sees a diagnostic view. Same state, audience-split presentation."* Not in §5 or §6.2. This is the V2 architecture that makes the CSM Review Mode possible. Its absence from §5/§6.2 is a gap because the V1 PRD should explicitly state that the shared state model is V1-forward-compatible with V2 asymmetric presentation, but that V1 ships with only the customer-facing surface.

**c. Preset library expansion (Addendum §7, item 10):** *"A wider library of launch presets by vertical."* Not in §5 or §6.2. Low risk for V1, but the addendum explicitly says "V2 expansion direction is informed by V1 results. Do not build V1 in a way that locks any of these out." Without the V2 intent stated in the PRD's Non-Goals, an architecture review could miss the extensibility requirement.

**Recommendation:** Add the three missing items to §5 Non-Goals or §6.2 Out of Scope:
- "Graduation handoff artifact connecting Wizard output to post-graduation CSM action — V2."
- "Asymmetric UX (customer-facing simplified view + CSM/onboarder diagnostic view of the same state) — V2."
- "Preset library expansion by vertical (urban STR, vacation, serviced apartments) — V2."

Also add a forward-compatibility constraint note somewhere in §4 or §8 (e.g., in the state persistence or event-stream section): *"The V1 Wizard state model must not foreclose V2 asymmetric UX or CSM diagnostic view."*

---

## 5. Open Questions in Brief Decision Log Not Tracked in §16

Brief §8 lists 10 open questions. Status check against PRD §16:

| Brief OQ # | Topic | PRD §16 tracking |
|---|---|---|
| OQ-1 | Profile output schema field-by-field mapping | BLOCKER-4 ✅ |
| OQ-2 | Resume granularity (section vs. question) | Not explicitly closed in §16 (resolved by FR-10, but not linked) — see GAP-8 ✅ resolved, ❌ not cross-referenced |
| OQ-3 | Data freshness on re-entry (re-evaluate vs. snapshot) | Resolved by §4.11 and FR-11/FR-11.2, but not cross-referenced in §16 |
| OQ-4 | Accountant delegation surface (what does accountant see?) | Resolved by FR-28, not cross-referenced in §16 — see GAP-9 |
| OQ-5 | Consent revocation (rollback or remain?) | BLOCKER-3 ✅ RESOLVED 2026-05-25 |
| OQ-6 | OAuth failure handling | SOFT-16 ✅ |
| OQ-7 | Mobile support (desktop-only or mobile?) | BLOCKER-9 ✅ RESOLVED |
| OQ-8 | Localization scope | SOFT-17 ✅ RESOLVED |
| OQ-9 | Baseline data refresh | BLOCKER-6 ✅ PARTIALLY RESOLVED |
| OQ-10 | Consent wording | BLOCKER-1 ✅ |

### GAP-14 — Brief OQ-3 (data freshness on re-entry) not explicitly closed in §16 (LOW)

**Source:** Brief Open Question #3 — *"If the user leaves and returns after Airbnb state changes (new bookings, more unread messages), do dynamic checks re-evaluate, or are they snapshotted on first sync?"*

**PRD status:** §4.11 (Branching & Data Freshness Model) and FR-11 / FR-11.2 fully resolve this question: Live Airbnb data is re-polled on every Wizard entry, but already-answered Questions use their Branching Snapshot (immutable). New branching decisions use the fresh data. This is a complete and thoughtful answer. However, Brief OQ-3 is not referenced anywhere in §16 as "resolved."

**Recommendation:** Add a resolved item in §16 (or a cross-reference note) linking Brief OQ-3 → §4.11 resolution. No new content needed; just the audit trail.

---

### GAP-15 — Brief OQ-2 (resume granularity) not explicitly closed in §16 (LOW)

Already noted in GAP-8. Adding here for completeness of the OQ tracking section.

**Recommendation:** Same as GAP-8.

---

## 6. Design Principles / Constraints Without a Corresponding FR

### GAP-16 — "Use what we already know" principle partially covered but no explicit pre-fetch audit requirement (SOFT)

**Source:** Brief §4 Design Principles #3 — *"Use what we already know — pre-fetch Salesforce and live Airbnb data; never ask the same thing twice."*

**PRD status:** FR-4 (Salesforce pre-fetch) and FR-15 (Live Airbnb hooks) cover the technical pre-fetch. The "never ask the same thing twice" constraint is implicit in the branching logic (e.g., Q2.1 auto-advances for Turno/Breezeway partners; Q7.2 auto-skips for PriceLabs/Beyond). However, there is no explicit FR or NFR consequence that tests for "no duplicate asks." If a future question is added or the V4 spec is updated, there is no guardrail in the PRD to prevent accidentally asking something already known.

**Recommendation:** Add a consequence bullet to FR-4 or FR-7 stating: *"No Question may ask for information already present in the Salesforce Account Data or Live Airbnb Data Hooks. Any Question whose answer could be pre-populated from existing data must either auto-advance or pre-fill and offer user confirmation."* This makes the brief's "never ask the same thing twice" principle testable.

---

### GAP-17 — Tiered skip intercept "gets lighter as user invests more" is a principle but not a measurable FR consequence (LOW)

**Source:** Brief §4 Design Principles #4 — *"Skip-friendly with tiered resistance — every question optional; intercepts get lighter as user invests more."*

**PRD status:** §4.7 (Tiered Skip Intercept) and FR-35 through FR-38 correctly implement the 4-tier system. Tier 4 has no modal (correct — the intercept IS lighter). However, the principle of "lighter as user invests" is not described as a measurable property — there is no consequence that says the intercept copy becomes shorter or less persuasive across tiers.

**Assessment:** Low risk; the 4-tier architecture implicitly satisfies the "lighter" principle (Tier 4 = no modal = lightest). No new FRs needed. But the design handoff could benefit from making this explicit in §10 or §4.7 description.

**Recommendation:** Add one sentence to the §4.7 description: *"Intercept weight decreases as user investment increases: Tier 1 has the most persuasive copy; Tier 4 has no modal."* Keeps the design principle traceable.

---

## 7. Secondary Stakeholder Requirements

### GAP-18 — Addendum §3 CSM secondary-stakeholder artifacts not fully mapped to FRs (SOFT)

**Source:** Brief Addendum §3 — explicitly names CSMs as "downstream consumers" of: (a) Section 6 (Call 1 Focus) and (b) Section 8 (Handoff), both of which "produce artifacts the CSM relies on for Call 1 preparation."

**PRD status:** FR-32 (Q6.1 feeds CSM Handoff Artifact) and FR-32.1 (CSM Handoff Artifact specification) address this. §12 lists CSM Leadership as a stakeholder with approval rights over the Handoff Artifact.

**Assessment:** Adequately covered. No gap.

---

### GAP-19 — Accountant as secondary persona: addendum says accountant is "explicit secondary recipient" but PRD §2.3 Non-Users says "secondary recipients via... not direct users" (LOW)

**Source:** Brief Addendum §3 — *"The accountant is not a primary persona but is an explicit secondary recipient."*

**PRD status:** §2.3 describes bookkeepers/accountants as "secondary recipients via the Section 5 delegation path... not direct users." This matches the addendum intent. The Stripped Section 5 View is extensively specified in §4.5 and §4.10. However, the accountant is never given a UJ (user journey). All six UJs (§2.4) are Owner-Operator journeys. UJ-4 describes the delegation flow from the operator's perspective, and within it, describes Jane's (the accountant's) experience — but Jane is not the "actor" of UJ-4; Marcus is.

**Recommendation:** This is a documentation completeness issue rather than a missing FR. Consider adding a brief "Accountant micro-journey" in §2.4 (even as a single bullet, not a full UJ) to ensure the accountant experience is explicitly narrated somewhere beyond the FR consequences. This helps UX when designing the Stripped Section 5 View.

---

## 8. KPI / Success Metric Gaps

### GAP-20 — Brief's "KPI Ownership" statement (shared Product + CSM) is in PRD but differs in naming (LOW)

**Source:** Brief §6 KPI Ownership — *"Activation, Call Quality, and Business Outcome metrics are shared between Product and CSM — neither team owns them alone."*

**PRD status:** §7 KPI Ownership mirrors this accurately: activation metrics (SM-1, SM-3, SM-6), Call Quality (SM-7, SM-8), and Business Outcome (SM-10–SM-13) are listed as "shared between Product and CSM." Good alignment.

**Assessment:** Covered. No gap.

---

### GAP-21 — Brief's guardrail "No increase in Airbnb connection anxiety or failed-connection recovery issues" is absent from PRD (MEDIUM)

**Source:** Brief §6 Guardrails — four guardrails listed:
1. No degradation in 3-month post-OB MRR churn (must stay ≤3%) — ✅ PRD SM-C5
2. No increase in support tickets caused by misconfiguration — ✅ PRD SM-C4
3. **No increase in Airbnb connection anxiety or failed-connection recovery issues** — ❌ NOT IN PRD
4. No increase in specialist-reported Call 1 confusion — partially covered by SM-7 (Call 1 quality score) but not framed as a guardrail

**PRD status:** SM-C4 (support tickets) and SM-C5 (MRR churn) are present. The specific guardrail about *Airbnb connection anxiety / failed-connection recovery* is not tracked anywhere in §7 or §15. This is relevant given that Q1.1 (Airbnb OAuth) is the very first interactive step — if OAuth failure rates or post-OAuth anxiety increase (e.g., users who connected Airbnb feel surveilled), it would be a meaningful product signal.

**Recommendation:** Add a counter-metric or guardrail to §7: *"SM-C8: Airbnb connection failure rate and post-connection support tickets must not increase vs. control. Counters SM-1 — ensures AHA moment does not generate anxiety or OAuth confusion."*

Also consider adding to §15 (Risks): an explicit risk row for "Airbnb OAuth step increases connection anxiety (users feel surveilled or uncertain about view-only scope)," mitigated by the safety-first framing (FR-14 confirmation state, §10 copy direction from Addendum §6).

---

### GAP-22 — Brief guardrail "No increase in specialist-reported Call 1 confusion" not separately tracked (LOW)

**Source:** Brief §6 Guardrails #4 — *"No increase in specialist-reported Call 1 confusion."*

**PRD status:** SM-7 (Specialist-rated Call 1 quality, 1–5) is the closest metric. But quality and confusion are not the same — a CSM could rate a call highly while also reporting more confusion about pre-Wizard data. The brief's intent is that the Wizard should not make CSM prep *harder* or more confusing (e.g., CSM receives incomplete or misleading Handoff Artifact data).

**Recommendation:** Add a consequence or note to FR-32.1 (CSM Handoff Artifact): *"The artifact must not increase specialist-reported Call 1 confusion. A counter-signal — specialist feedback indicating the Handoff Artifact was confusing or incomplete — is a Phase 2 kill criterion."* Or add a qualitative counter-metric to §7.

---

## 9. Summary Table

| Gap ID | Category | Severity | Source | Resolution |
|---|---|---|---|---|
| GAP-1 | Strategic framing | LOW | Brief §1 thesis | Add thesis sentence to §1 Vision |
| GAP-2 | Strategic framing | SOFT | Addendum §5 benchmark | Add monday.com hybrid model note to §1 or §1.1 |
| GAP-3 | Strategic framing | LOW | Addendum §5 | Add build-layer/review-layer framing to §1 or §12 |
| GAP-4 | FR coverage | MEDIUM | Brief §4 Section 4 scope | Verify V4 Section 4 question count; split §4.5 header |
| GAP-5 | FR coverage | LOW | Brief §4 DP #5 | Clarify single-consent architecture in §4.9 / FR-43 |
| GAP-6 | Intentional divergence | LOW (noted) | Brief §5 "applied on skip" | Document divergence in §18 Change Log |
| GAP-7 | Already resolved | LOW | Brief OQ-1 | Note BLOCKER-4 closes Brief OQ-1 |
| GAP-8 | OQ audit trail | SOFT | Brief OQ-2 | Cross-reference FR-10 closes Brief OQ-2 in §16 |
| GAP-9 | OQ audit trail | SOFT | Brief OQ-4 | Cross-reference FR-28 closes Brief OQ-4 in §16 |
| GAP-10 | Baseline gap | BLOCKER | Brief OQ-9 / BLOCKER-6 | Name two remaining baselines (SM-10, SM-11) explicitly in BLOCKER-6 |
| GAP-11 | Copy direction | LOW | Addendum §6 review-ready phrases | Add to §10; add Owner Prep safety copy to FR-33 |
| GAP-12 | Copy direction | SOFT | Addendum §6 bot voice | Adequately deferred; no action |
| GAP-13 | V2 deferrals | MEDIUM | Addendum §7 items 7, 8, 10 | Add 3 missing V2 items to §5 / §6.2 |
| GAP-14 | OQ audit trail | LOW | Brief OQ-3 | Cross-reference §4.11 closes Brief OQ-3 in §16 |
| GAP-15 | OQ audit trail | LOW | Brief OQ-2 | Same as GAP-8 |
| GAP-16 | Design principle | SOFT | Brief §4 DP #3 | Add "never ask twice" consequence to FR-4 or FR-7 |
| GAP-17 | Design principle | LOW | Brief §4 DP #4 | Add one sentence to §4.7 description |
| GAP-18 | Secondary stakeholder | — | Addendum §3 CSM | Covered |
| GAP-19 | Secondary stakeholder | LOW | Addendum §3 accountant | Add accountant micro-journey to §2.4 |
| GAP-20 | KPI | — | Brief §6 KPI ownership | Covered |
| GAP-21 | KPI / Guardrail | MEDIUM | Brief §6 Guardrail #3 | Add SM-C8 (Airbnb connection anxiety guardrail) to §7; add risk row to §15 |
| GAP-22 | KPI / Guardrail | LOW | Brief §6 Guardrail #4 | Add Call 1 confusion counter-signal to FR-32.1 or §7 |

---

## 10. Priority Actions

**Must address before PRD is considered final:**

1. **GAP-13** — Add the three missing V2 deferrals (graduation handoff artifact, asymmetric UX, preset library) to §5 / §6.2. The addendum explicitly says "do not build V1 in a way that locks any of these out" — the PRD must reflect these as future-compatibility constraints.

2. **GAP-21** — Add the Airbnb connection anxiety guardrail (SM-C8) to §7. This is an explicit brief guardrail that has no PRD counterpart.

3. **GAP-10** — Name the two remaining open baselines in BLOCKER-6 explicitly (SM-10 and SM-11), with owner and due date.

**Should address before Design/Engineering kickoff:**

4. **GAP-11** — Add the five review-ready framing phrases to §10 and the Owner Prep safety copy constraint to FR-33.

5. **GAP-4** — Verify V4 Section 4 question count and split the PRD section header if additional Q4.x questions exist.

6. **GAP-2** — Add the monday.com hybrid model benchmark to §1 or §1.1 for strategic traceability.

**Address before Phase 2 (nice-to-have for audit trail):**

7. **GAP-8, GAP-9, GAP-14, GAP-15** — Close Brief OQ-2, OQ-3, OQ-4 explicitly in §16 with cross-references to the resolving FRs.

8. **GAP-5** — Clarify single-consent architecture intent in §4.9 or FR-43 for the legal reviewer.

---

*End of reconciliation report.*
