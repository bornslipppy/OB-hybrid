---
title: "Structural Editorial Review — PRD: Guesty Pro Onboarding Wizard"
reviewer: Claude Code (structural editorial agent)
date: 2026-05-25
document_reviewed: prd.md (draft v2)
---

# Structural Editorial Review

## Verdict

**Structurally sound. No reorganization required.** The document is well-organized, the hierarchy is coherent, and the Glossary-anchored cross-referencing is executed consistently. The length is earned. Findings below are targeted fixes, not rewrites. Five issues warrant action before downstream workflows consume this PRD.

---

## Findings

### FINDING-1 — §1.1 Premise 3 vs. §2.1: Near-duplicate role-collapse content [True Redundancy]

**What:** §1.1 "Premise 3 — Role-collapse as design driver" (lines 63–67) and §2.1 "Primary Persona" (lines 79–83) both explain the role-collapse premise with similar detail. §2.1's "Critical design constraint" block re-narrates the same concept (owner-operator collapses three roles) and cross-references back to §1.1. The cross-reference is correct, but the narrative is repeated.

**Impact:** LLM agents consuming §2 without context from §1 will receive a partial second explanation, potentially treating them as additive rather than the same claim. Engineers skimming §2.1 see the claim but not the data/decision rule, which lives only in §1.1.

**Recommended fix:** In §2.1's "Critical design constraint" block, reduce the narrative to a one-sentence forward pointer: *"Role-collapse is the design driver behind the Wizard's opinionation — the premise, data, and decision rule are specified in §1.1 Premise 3."* The current two-paragraph explanation in §2.1 can be deleted.

---

### FINDING-2 — §6 MVP Scope: structural duplication of §5 Non-Goals [True Redundancy]

**What:** §6.2 "Out of Scope for MVP" is essentially a reformatted subset of §5 "Non-Goals (Explicit)." Several items appear verbatim or near-verbatim in both sections:
- "CSM Review Mode — V2" (§5 and §6.2)
- "Mobile responsive support — V2" (§5 as "Wizard is not mobile in V1" / §6.2 as "Mobile responsive support")
- "Intra-Wizard consent revocation — V2" (§5 and §6.2)
- "Non-Airbnb-primary customers — V2+" (§5 and §6.2)
- "Multi-Airbnb-account aggregation — V2+" (§5 and §6.2)
- "Multilingual support — V2+" (§5 and §6.2)

**Impact:** Downstream agents querying for out-of-scope items will find two lists, neither of which is authoritative. Either list could diverge across edits.

**Recommended fix:** One of two approaches — pick one and note it in the Change Log:
- **Option A (preferred):** Collapse §5 and §6.2 into a single "Non-Goals / Out of Scope" section. §6.1 ("In Scope") stands alone. This is the correct structure for an LLM-primary document.
- **Option B:** Keep §5 as the authoritative non-goals list and reduce §6.2 to a single sentence: *"Out-of-scope items are enumerated in §5. V2+ deferrals are indicated per item."*

---

### FINDING-3 — §16 Open Questions: resolved items are structural noise at scale [Structural clarity]

**What:** §16 contains 38 items. Approximately 16 of them are resolved (struck-through). The resolved items are mixed throughout the list, making it hard for a downstream agent to quickly identify the current action surface. The struck-through format works for human audit trail but adds parsing overhead.

**Impact:** Agents consuming §16 to identify open blockers must parse and discard ~42% of the items. The list length overstates the current open question count by a factor of ~1.7.

**Recommended fix:** Move all resolved items (struck-through) to a collapsed subsection at the bottom of §16, titled "Resolved (archived)." The three active sublists ([BLOCKER], [SOFT], [INVESTIGATE]) then contain only open items. The audit trail is preserved; the signal-to-noise ratio improves significantly. The §17 Assumptions Index has a cleaner version of this pattern (CONFIRMED items are identifiable but not dominant) — apply the same approach to §16.

---

### FINDING-4 — §4.9 Profile Configuration Writes: scope violation — architecture-level content [Scope violation → move to addendum]

**What:** FR-48 ("Wizard writes are observable") and FR-49 ("Wizard surfaces write failures non-blockingly with retry contract") contain content that belongs in two different documents:
- FR-48's event field schema (timestamp, customer ID, account ID, Question ID, configuration domain, new value, was_auto_pilot, actor enum) is an architecture spec detail, not a PM-level capability spec.
- FR-49's retry contract (3 retries, exponential backoff, queuing mechanics, atomic-per-write-domain batch rollback) is an implementation-level contract, not a feature requirement.

**Impact:** Architecture agents will find PM-authored retry semantics that may conflict with engineering decisions. The PRD is authoring below its abstraction level in these two FRs.

**Recommended fix:** In FR-48, remove the event field schema from the FR body. Replace with: *"Each write emits a structured event. Event schema is a Phase 0 deliverable in the Profile Output Schema artifact (FR-44)."* In FR-49, strip the retry count and backoff specification. Replace with: *"Write failures are surfaced non-blockingly with retry. Retry contract and queue mechanics are architecture-owned."* Move the full current FR-48/49 text to the addendum as input for the architecture workflow.

---

### FINDING-5 — §0 Document Purpose: "§4.10 Delegation Lifecycle" and "§4.11 Branching & Data Freshness" are mentioned but not explained [Missing scaffolding]

**What:** §0 Document Purpose (lines 24–24) references §4.10 and §4.11 as "two cross-cutting state-machine sections" that "consolidate behavior spanning multiple Features." This is accurate, but it gives readers no signal for *why* these sections are architecturally separate from the Feature sections (§4.1–§4.8). First-time LLM readers of §0 who start processing §4 will not understand the structural intent when they hit §4.10 mid-stream.

**Impact:** Agents constructing architecture specs from this PRD may not recognize §4.10 and §4.11 as the canonical sources for their respective behavioral models, and instead stitch together a model from the individual FR cross-references.

**Recommended fix:** In §0 Document Purpose, add one sentence after the §4.10/§4.11 mention: *"These two sections are the canonical behavioral specifications for their respective concerns; all individual FRs that touch delegation or branching are subordinate to them."* This is a one-line addition that eliminates ambiguity for downstream consumers.

---

### FINDING-6 — §7 Success Metrics: SM-9 is structurally redundant with SM-1 [True Redundancy — minor]

**What:** SM-9 is defined as "% of Call 1 customers arriving Airbnb-synced — Same as SM-1 measured at the CSM side." The definition acknowledges it is the same metric, measured from a different vantage point. It has no separate target, no separate phase floor, and no separate owner (it is listed under Secondary without a distinct owner row in §12).

**Impact:** Downstream analytics agents will instantiate two separate measurement tasks for what is operationally one count, potentially causing tracking divergence (if SM-1 and SM-9 report different numbers, it creates a resolution burden rather than useful signal).

**Recommended fix:** Remove SM-9 as a standalone metric. In SM-1, add a parenthetical: *"Cross-check: CSM-side verification of this rate is the same signal; any discrepancy between product-measured SM-1 and CSM-reported arrival sync rate flags a data integrity issue."* This preserves the dual-vantage rationale without instantiating a second metric that will silently diverge.

---

## Summary Table

| # | Section | Type | Priority | Action |
|---|---|---|---|---|
| 1 | §1.1 / §2.1 | True Redundancy | High | Remove duplicated role-collapse narrative from §2.1; replace with pointer to §1.1 |
| 2 | §5 / §6.2 | True Redundancy | High | Collapse into single non-goals list (Option A) or make §6.2 a pointer to §5 (Option B) |
| 3 | §16 | Structural Clarity | Medium | Archive resolved items into a subsection; preserve open items in clean sublists |
| 4 | §4.9 FR-48/49 | Scope Violation | Medium | Strip architecture/implementation detail from PRD body; move to addendum as architecture input |
| 5 | §0 | Missing Scaffolding | Low | Add one sentence clarifying §4.10/§4.11 as canonical behavioral specs, not Feature appendages |
| 6 | §7 SM-9 | True Redundancy | Low | Remove SM-9; fold CSM-side rationale into SM-1 definition |

---

## Items Reviewed and Found Structurally Sound (no action needed)

- **§1.1 Hypotheses vs. §15 Risks:** These overlap topically but serve different structural roles (§1.1 = falsifiable premises with decision rules; §15 = operational risk register). Not redundant.
- **§4.10 Delegation Lifecycle vs. §4.5 FRs:** The section-level spec (§4.10) and FR-level assertions (§4.5) are correctly organized — §4.10 is the state machine; §4.5 FRs are testable consequences. The forward pointer in §4.5's description is adequate.
- **§14 Rollout vs. §16 Blockers:** Phase 0 preconditions in §14 and BLOCKER items in §16 overlap in topic, but §14 is the authoritative gating list and §16 is the Q&A detail log. The cross-references are consistent.
- **§8 Cross-Cutting NFRs vs. §9 Constraints:** §8 is performance/accessibility/security NFRs; §9 is business-level safety/privacy/cost guardrails. Distinct enough — not redundant.
- **§3 Glossary length:** 28 definitions. All are used in FRs. No orphan definitions detected. Length justified.
- **§2.4 User Journeys length:** Six detailed journeys. Each exercises a distinct branch of the system. All six are referenced in Feature sections. Length justified.
- **§17 Assumptions Index vs. inline [ASSUMPTION] tags:** Dual representation is intentional and aids both inline reading (author) and bulk audit (reviewer). Not redundant.

---

*End of review. Six findings; two high, two medium, two low. No structural reorganization required.*
