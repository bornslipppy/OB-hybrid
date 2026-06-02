---
title: "PRD Quality Review — Guesty Pro Onboarding Wizard (Pre-Call-1 Questionnaire)"
---

# PRD Quality Review — Guesty Pro Onboarding Wizard (Pre-Call-1 Questionnaire)

## Overall verdict

This is a strong PRD that earns its length: it has a real thesis (convert Call 1 from walkthrough to strategic review by giving SMB owner-operators "skin in the game" before the call), a load-bearing persona ("Role Collapse"), and FRs whose consequences are mostly testable. The main risks are concentrated in one place — the deferred Profile Output Schema (FR-44) is the project's critical-path dependency and the PRD acknowledges it but does not yet enforce sequencing in §14 Rollout — and in a small number of FRs that lean on V4 verbatim copy without quoting it (FR-38, FR-21), which will create downstream story friction if V4 drifts. Substance is high; theater is low.

## Decision-readiness — strong

Decisions are stated as decisions, not buried. The PRD takes clear positions on several real tensions: live re-poll vs. snapshot-at-sync (FR-11 picks live, called out in §13 Dependencies as "this PRD specifies live re-poll on every entry"), no retroactive re-routing on changed signals (FR-11 consequence 3), consent-revocation chooses no-rollback (FR-46), and the Wizard explicitly *is not* a checklist (§5 Non-Goals). The Role Collapse framing in §2.1 names the trade-off — "the Wizard cannot assume the customer will self-organize. It must **supply** the sequencing." Open Questions in §16 are genuinely open (legal sign-off, baseline refresh, schema ownership) rather than rhetorical. `[BLOCKER]` tags on Q1 and Q3 honestly mark what cannot ship without resolution.

One soft spot: §13 lists "Profile Configuration Write infrastructure" as "New" and "Live Airbnb Data Hooks" as "Spec needed" but §14 Rollout schedules Phase 1 dogfood in Weeks 1–2 without explicit sequencing of the schema → infra → dogfood chain. A reader can infer it from §6.2 ("Required before engineering implementation; not before PRD lock") plus the §15 Risks row, but the rollout calendar doesn't itself reflect this dependency.

### Findings
- **medium** Rollout calendar does not reflect critical-path dependency (§14 Phase 1 vs. FR-44 / §6.2) — Phase 1 dogfood is dated Weeks 1–2 but the Profile Output Schema and write infrastructure ("New" per §13) must precede it. *Fix:* add a "Week 0" or "Pre-Phase-1" row to §14 covering schema lock + write-infra build, and gate Phase 1 entry on it.

## Substance over theater — strong

Persona discipline is tight: one primary persona (Owner-Operator) with two referenced library variants (2A, 2B), and a sharp "Non-Users (V1)" list that excludes Lite/SME/Mid-Market/Enterprise, Vrbo/Booking-primary, third-party owners, bookkeepers, and CSMs. The Role Collapse constraint in §2.1 is the persona doing actual work — it's cited in §1 Vision ("connects the customer's real Airbnb data"), §4.5 (Accountant delegation exists because of role collapse + delegation safety valve), and §10 Aesthetic ("Confident, calm, conversational" copy is the persona response).

Vision in §1 is product-specific: it names the dead zone between booking and Call 1, the empty-enterprise problem, the ~0% engagement on existing surfaces, 82% off-SLA, and the explicit goal *not* to replace Call 1. This Vision cannot swap into a generic onboarding PRD.

NFRs in §8 mostly have numeric bounds (2s P95, 500ms P95, 30-day Resume, 3s re-poll, <0.5% error rate, ≥128 bits entropy). WCAG 2.1 AA is named with a soft assumption tag for confirmation. No NFR-theater detected.

The six UJs in §2.4 are each grounded in a V4 scenario and name a climax + resolution. UJ-2 (David, urgent check-in) and UJ-4 (Marcus delegates to accountant) are doing real work — they're the only place where the FR-16 urgent routing and FR-27/28/29 delegation paths are exercised as user-visible narrative.

No findings.

## Strategic coherence — strong

The PRD has a thesis and bets on it: Call 1 conversion from walkthrough to strategic review (§1, restated as the explicit goal). The thesis cascades:
- §1 Vision → "skin in the game" → §2.1 Role Collapse → §4.3 Airbnb sync as *first* interactive step (not warm-up) → SM-1 as the only Primary metric.
- §4.7 Tiered Skip Intercept is coherent with the thesis — adaptive resistance preserves user autonomy while protecting completion at investment milestones.
- §4.9 Profile Configuration Writes is where the thesis becomes account state ("the writes are the actual product outcome" — §4.9 description).

Success Metrics validate the thesis rather than measuring activity. SM-7 (Specialist-rated Call 1 quality) and SM-8 (% review vs. walkthrough) directly measure the thesis. Counter-metrics in SM-C1 through SM-C5 are real counter-pressure, not boilerplate: SM-C1 (time-on-Wizard not to be optimized either direction), SM-C2 (sections-completed not to be optimized — preserves skip-friendly principle), SM-C3 (sync without downstream activation = vanity), SM-C4 (support tickets must not increase), SM-C5 (3-month MRR churn guardrail).

MVP scope kind: this is an "experience" PRD (one cohesive flow) with "platform" elements (write infrastructure). §6 MVP Scope reflects that — In Scope is the experience surface; Out of Scope correctly defers infrastructure-adjacent things (CSM Review Mode widget, dashboard widget, pre-population pipeline) without de-scoping silently.

No findings.

## Done-ness clarity — strong

This is the dimension most at risk in PRDs of this length, and it holds up. Every FR has explicit "Consequences (testable):" bullets with verifiable conditions. Sampling:
- FR-9 (save state): "Each interaction triggers a server-side write within 2 seconds of user action" + 3-retry behavior + warning copy.
- FR-15 (Live Airbnb hooks): "These five values are available in the session state by the time Q1.2 renders" — testable as a fixture assertion.
- FR-27 (Accountant Secure Link): 30-second send latency, 14-day expiry, unique-per-delegation, Section-5-only scope.
- FR-31 (Q5.3 fees): "4-digit max integer part," "per stay / per night," "None auto-advances and writes empty fees" — exact bounds.
- FR-45 (idempotency): explicit "re-writing the same value does not produce duplicate records" with a "Use it → backward → Use it" worked example.

Where the PRD points to V4 instead of duplicating, it does so consistently and cites a section/question ID. This is the right move for downstream story creation (V4 is source of truth for copy).

Two soft spots worth flagging:
- FR-38 says "Each Tier's intercept copy matches V4 verbatim" and lists Tier 1/2/3 copy lines. The lines shown are first-line excerpts ("I totally get it — you're ready to see Guesty in action…"). This is fine as a cross-reference but a story author writing the acceptance test will need to load V4 to know the full copy block boundaries. The cross-reference resolves; just flagging that this is a V4-dependency hotspot.
- FR-21 ("the exact wording per variant matches V4 Section 3 Q3.2 copy") has the same V4-dependency shape.
- FR-12 "meaningful change" thresholds are specified numerically (Unread delta ≥ 3, new reservation, 48-hour crossing) but the toast copy is left to "UX to finalize" `[ASSUMPTION]`. Done-ness is preserved (the *behavior* is testable); copy is deferred. Acceptable.

### Findings
- **low** V4 copy cross-references are dense in §4.7 and §4.4 (FR-38, FR-21) — downstream story authors must load V4 every time to write tests. *Fix:* none required at PRD time; flag in the engineering kickoff that V4 needs version-locking concurrent with PRD lock so the cross-references don't drift.

## Scope honesty — strong

§5 Non-Goals does real work and is unusually explicit: ten Non-Goals, each with a one-line rationale. The "not a checklist" Non-Goal directly counters a natural reader assumption. "Not full self-serve onboarding" / "Call 1 remains the activation milestone" forecloses a scope-creep direction.

§6.2 Out of Scope for MVP is honest about what's deferred: Profile Output Schema (with `[NOTE FOR PM: highest-priority post-PRD deliverable.]` callout), CSM Review Mode, mobile, owner invite emails, persistent Call-1-prep widget. Each deferral has an explicit V2 marker.

`[ASSUMPTION]` density is appropriate: 25 inline tags, all rounding back to §17 Assumptions Index. The `[BLOCKER]` marker in §16 Open Q1 and Q3 separates phase-blockers from soft-confirms. The PRD does not pretend to be ready-to-build — it names where it isn't.

Per the reviewer note, the deferred Profile Output Schema is the explicit decision, not a substance gap. It is flagged as a *risk* in §15 Risks row 5 ("Profile Output Schema is not delivered before engineering kickoff") with PM-owned mitigation. That's the right place for it.

No findings.

## Downstream usability — strong

This PRD is explicitly chain-top: §0 names UX, Architecture, and Sprint/Story workflows as the readers. It earns the downstream-usability bar.

- **Glossary (§3):** present, comprehensive, defines 25 terms including the new V1 surfaces (Accountant Secure Link, Stripped Section 5 View, Live Airbnb Data Hooks). Section-naming convention `Q{section}.{order}` is defined once and used consistently.
- **FR IDs:** FR-1 through FR-49, contiguous, no gaps. SM-1 through SM-13 plus SM-C1 through SM-C5, contiguous. UJ-1 through UJ-6.
- **Cross-references:** FRs cite other FRs by ID ("per FR-43," "per FR-11," "see §16 Open Q1") rather than "see above." UJs are cited by ID inside FR descriptions ("Realizes UJ-1, UJ-3").
- **UJ persona linkage:** every UJ names the persona scenario inline (Maya, David, Sara, Marcus, Hannah, Ben) and each ties back to the §2.1 Owner-Operator persona by implication of segment fit. The UJs do not name "Owner-Operator" by exact label in each UJ heading — they use first names. This is a minor downstream-usability nick: a story author who pulls UJ-3 out alone has to infer the persona.
- **Section pull-out:** §4 features can each be pulled out alone and remain readable. Glossary terms carry the load.

### Findings
- **low** UJs name first names rather than the §2.1 persona label (§2.4 UJ-1 through UJ-6) — "Maya," "David," "Sara," etc., without restating "Owner-Operator (SMB Guesty Pro)." *Fix:* add a one-line preamble to §2.4 ("All six UJs feature instances of the §2.1 Owner-Operator persona"), or suffix each UJ heading with "(Owner-Operator)."

## Shape fit — strong

This is a consumer-product-shaped, multi-stakeholder B2B PRD (operator + accountant + CSM, with role collapse on the operator side) with meaningful UX. UJs and personas are load-bearing — and they are present, named, and cited. The FR structure is right for the product type (experience flow with state, branching, and writes — not a capability spec).

The Accountant Secure Link / Stripped Section 5 View introduces a *second* user surface with its own constraints (FR-28, FR-29). The PRD treats this as a sub-surface inside §4.5 rather than spinning up a separate persona, which is the right call — the Financial Owner is a one-shot user, not a primary persona.

Chain-top usage is appropriate: §0 names the downstream workflows; §13 Dependencies splits Built vs. New vs. Spec-needed; §14 Rollout reflects the multi-phase nature. Not over-formalized for the product shape; not under-formalized either.

No findings.

## Mechanical notes

- **Glossary drift:** none detected. "Wizard," "Section," "Question," "Setup Call," "Consent Record," "Profile Configuration Write" all used identically across §1 through §17. Note one minor case-sensitivity inconsistency: §1 Vision uses "AHA moment" (caps), §4.3 description says "AHA moment" (caps), §1 also uses lower-case "moment" in flow. Acceptable as stylistic.
- **ID continuity:** FR-1 through FR-49 contiguous (verified by sampling). SM-1 through SM-13 + SM-C1 through SM-C5 contiguous. UJ-1 through UJ-6 contiguous. No duplicates spotted.
- **Cross-reference resolution:** §16 Open Qs cross-reference Brief Open Qs (Brief Q1, Q5, Q6, Q8, Q9, Q10). FR cross-references to other FRs all resolve. §17 Assumptions Index entries all match inline `[ASSUMPTION]` tags (sampling: FR-2 → §16 Open Q1 → §17 entry — round-trip works).
- **Assumptions Index roundtrip:** 25 inline `[ASSUMPTION]` tags; §17 lists ~25 entries. Spot-check: FR-5 dashboard link disappearance, FR-6 per-Question skip tier, FR-12 toast wording, FR-15 hook spec, FR-27 14-day expiry — all present in §17. No orphan index entries detected.
- **Required sections present:** Vision, Target User, Glossary, Features (FRs), Non-Goals, MVP Scope, Success Metrics with counter-metrics, NFRs, Constraints, Aesthetic, IA, Stakeholders, Dependencies, Rollout, Risks, Open Questions, Assumptions Index. Complete for a chain-top experience PRD at this stakes level.
- **Stakeholder names (§12):** all "TBD" except PM. Flagged in §16 Open Q11 and §17.

---

*Review complete. No critical findings. The PRD is ready for downstream UX/Architecture/Sprint workflows pending §14 sequencing clarification and the standing `[BLOCKER]` Open Questions (consent wording, Profile Output Schema).*
