---
title: "Implementation Readiness Assessment Report"
---

# Implementation Readiness Assessment Report

**Date:** 2026-06-02
**Project:** AI Adaptive Onboarding PoC — Eval Harness
**Assessor:** Winston (System Architect)
**Inputs:** PRD v2 (post Reviewer Gate), epics.md (5 epics / 30 stories), architecture.md v1, PoC plan v1.2, schema v0.3

---

## 1. Document Inventory

| Type | File | Status |
|------|------|--------|
| PRD | `prds/prd-AI-Adaptive-Onboarding-PoC-2026-06-02/prd.md` | ✅ Found (whole) — Reviewer-Gate-approved v2 |
| Architecture | `architecture.md` | ✅ Found (whole) — v1, DRI-ratified 2026-06-02 |
| Epics & Stories | `epics.md` | ✅ Found (whole) — 5 epics, 30 stories, FR Coverage Map present |
| UX Design | — | ⚪ **None — correct by design** (PRD §5 Non-Goal: offline harness, no UI; epics §"UX Design Requirements: None") |
| Source-of-truth inputs | `poc-plan-…v1.2`, `guesty-pro-account-creation-schema.md v0.3` | ✅ Loaded as context |

**No duplicates** (no whole+sharded conflicts). UX absence is a documented design decision, **not** a warning.

---

## 2. PRD Analysis

### Functional Requirements (36 FR-level items)
The PRD defines **FR-1 … FR-35**, plus **FR-13b** (Tree tool-call trace parity) inserted between FR-13 and FR-14. That is **36 FR-level requirements**, not 34.

- **Agent (Epic 3):** FR-1 next-slot selection, FR-2 fixed tool surface, FR-3 hero fan-out, FR-4 conditional S5, FR-5 vocab normalization, FR-6 model/temp.
- **Tree (Epic 2):** FR-7 depends_on branching, FR-8 behavioral parity, FR-9 blind authoring, FR-10 independent authorship, FR-11 fairness sign-off, FR-12 tooling parity, FR-13 capability ledger, **FR-13b tree trace parity**.
- **H2 extractor (Epic 5):** FR-14 provenance, FR-15 confirm-before-use, FR-16 brief-only slots, FR-17 regex baseline, FR-18 abstention.
- **Simulator (Epic 4):** FR-19 faithful answers, FR-20 no leakage, FR-21 decorrelation.
- **Harness (Epic 4):** FR-22 k≥5, FR-23 SAR by disposition, FR-24 secondary metrics, FR-25 stats honest to N=8, FR-26 freeze discipline.
- **Profiles/keys (Epic 1):** FR-27 scored specs, FR-28 dev profiles, FR-29 two-reviewer validation, FR-30 contested-slot adjudication.
- **Simulator validation (Epic 4):** FR-31 spot-check + per-run fidelity.
- **H2 corpus (Epic 5):** FR-32 de-identified pull, FR-33 stratified labeling, FR-34 flag-quality blind rating.
- **Cross-cutting:** **FR-35 free-text blind-rater protocol.**

### Non-Functional Requirements (5)
NFR-1 machine-readable trace; NFR-2 determinism-from-echo (structural); NFR-3 PII governance; NFR-4 reproducibility/freeze; NFR-5 cost/latency per profile. All five appear in the epics inventory.

### Additional governing requirements
Agent invariants §8 (7 invariants), success metrics §7 (SM-1…SM-11 + SM-C1…C3), kill criteria §10 (2 classes), the §7.1 combined H1×H2 verdict matrix, and §9 PII governance.

### PRD completeness
**Strong.** The PRD is unusually complete — pre-registered metrics, explicit reviewer-gate resolutions (§15), inline assumptions index (§14), and consequence-level testability on every FR. The gaps below are almost all **epics ↔ PRD/architecture traceability drift**, not PRD defects.

---

## 3. Epic Coverage Validation

### Coverage matrix (deltas only — 32 of 36 are cleanly traced)

| FR | PRD requirement | Epic coverage | Status |
|----|-----------------|---------------|--------|
| FR-1 … FR-12 | (agent + tree) | Epics 2/3 per coverage map | ✅ Covered |
| **FR-13b** | Tree emits the identical fixed tool vocabulary + machine-readable trace schema as the agent | **NOT in inventory or FR Coverage Map; no explicit story AC** | ❌ **Missing trace** |
| FR-14 … FR-34 | (extractor, simulator, harness, profiles, H2) | Epics 1/4/5 per coverage map | ✅ Covered |
| **FR-35** | Free-text scored slots (`pain`, `split_terms`, verbal ownership) + SM-4 structural-win scored by ≥2 blind raters w/ tie-breaker | **NOT in inventory or FR Coverage Map; no dedicated story** | ❌ **Missing** |
| **(arch) Shared kernel** | tool contract, ProfileState reducer, trace event schema, System protocol, LLM client (architecture §3, driver D-1) | **No story builds it** | ❌ **Missing (blocks sequencing)** |

### Coverage statistics
- Total PRD FR-level items: **36** (FR-1..FR-35 + FR-13b)
- Explicitly traced in epics: **34**
- **Untraced: FR-13b, FR-35** → explicit coverage **≈ 94%**
- Architecture-introduced foundational work (the neutral kernel) has **0 stories**.

---

## 4. UX Alignment

**N/A by design.** PRD §5 declares no UI; epics confirm "No UX Design Requirements." Architecture builds an offline, file-based harness with no UI surface. No alignment gap, no warning. The simulated host is *modeled* by Epic 4, not served by a UI — correctly reflected across all three artifacts.

---

## 5. Epic Quality Review

### Epic structure & value
Epics are framed by **deliverable value to the eval team** (Epic 1 = "an answer key they trust," Epic 2 = "a certified-fair baseline," etc.). For an internal experiment whose "users" are the eval engineer, reviewers, and decision-maker (PRD §2.1), this is legitimate user-value framing — **not** technical-milestone epics. ✅

### Epic independence — one real violation
- Epic 5 (H2): genuinely independent ✅.
- Epic 4 consumes Epics 1–3: backward dependency, allowed ✅.
- **🟠 Finding:** epics.md claims "Epics 1–3 are independent and can run in parallel." But **Epic 3's acceptance criteria cannot be verified without the Epic 4 user simulator and Epic 1 profiles** (Story 3.1: "*When the agent runs each [profile]*" presupposes a simulator to answer it). Same for Epic 2's runnable ACs. This is a **forward dependency (Epic 2/3 → Epic 4 simulator)** hiding under "parallel." Authoring can parallelize; *acceptance* cannot.

### Within-epic story dependencies
No forward story references found. 4.8 → 4.5–4.7, 5.5 → 5.2/5.3, 1.3 → 1.1 are all backward. ✅

### Greenfield setup
**🟠 Finding:** greenfield builds need an explicit "set up the project" story (scaffold, lockfile pinned for the freeze manifest, run-config TOML, CI PII-guard). None exists — Story 1.1 is about respondent specs, not project setup. This compounds the missing-kernel gap (§3).

### Acceptance-criteria quality
Generally excellent — BDD Given/When/Then, testable, specific. The two temperature/stop-condition drifts (Stories 3.7, 3.1) were **corrected today**. ✅

### Findings by severity

#### 🔴 Critical
- **C-1 — The shared kernel has no story.** Architecture §3 makes the tool contract + `ProfileState` reducer + trace event schema + `System` protocol + LLM client the *neutral foundation* that guarantees fairness (driver D-1) and must be built and **frozen before** Epics 2 and 3 (which both assume the tool surface exists). No epic or story creates it, and FR-10 requires it be owned by neither the tree nor agent author. **This blocks the build sequence as written.**
- **C-2 — FR-35 (free-text blind-rater protocol) is unhomed.** It is load-bearing for SM-4 (the *required* qualitative structural win) and for scoring `pain`/`split_terms`/verbal ownership. Story 4.5 scores numbers; Story 5.6 rates *H2 flags* (FR-34); neither implements the FR-35 protocol for H1 free-text + SM-4. Without it, SM-4 cannot be adjudicated and free-text SAR has no defined scorer.

#### 🟠 Major
- **M-1 — FR-13b (tree trace parity)** absent from the inventory and FR Coverage Map; no story AC requires the tree to emit the identical FR-2 trace schema. Architecture §3 treats this as central; the epics don't trace it.
- **M-2 — Epic independence claim is partly false** (Epic 2/3 acceptance depends on Epic 4 simulator + Epic 1 profiles). See above.
- **M-3 — Agent invariant 7 untraced.** Termination & absent-fact guards (IDK = absence, 60-turn cap → `incomplete`, `end_section` forbidden while reachable slots undispositioned) appear in PRD §8 inv 7 and architecture §3.2/§3.4 but have **no story AC**. Invariants 1–6 are covered by Stories 3.3/3.4; inv 7 falls through.
- **M-4 — No project-setup / scaffold story** (greenfield). Also no story for the CI **PII commit-guard** that architecture D-8 relies on (Story 5.1 covers de-id + "no raw note committed" as an outcome, but not the automated guard that enforces it).

#### 🟡 Minor
- **m-1 — Combined H1×H2 verdict matrix (§7.1 / UJ-4) has no single owner.** Story 4.8 produces the H1 verdict, Story 5.5 the H2 verdict; the *combined* 2×2 → build-recommendation synthesis is owned by neither.
- **m-2 — Story 2.5 softens FR-10.** "tree author ≠ agent author *(or the deviation is documented as a fairness caveat)*" — acceptable under FR-10's compensating-control path, but the story should reference the FR-10 interpretation-discount requirement explicitly, not just "documented."
- **m-3 — FR-15 H1 seed not in an Epic 1 AC.** The precedence/conflict-surfacing half of FR-15 must be seeded into ≥1 scored profile (PRD note / EC-17); no Story 1.1 AC requires it (architecture R-11 flags the same).

---

## 6. Summary and Recommendations

### Overall Readiness Status

**🟠 NEEDS WORK** *(initial pass — superseded by the Re-Run Verification in §7; status is now ✅ READY)*

The planning package is high-quality and internally rigorous (Reviewer-Gate-approved PRD, strong ACs, clean stats philosophy). The issues are concentrated where the **epics predate the architecture** — the architecture introduced a neutral shared kernel and surfaced two FRs (FR-13b, FR-35) that the epics never traced. None of this is a redesign; it's traceability repair plus one missing foundational epic.

### Critical Issues Requiring Immediate Action
1. **C-1 — Add a foundation epic/story for the shared kernel** (tool contract, `ProfileState`, trace schema, `System` protocol, LLM client + scaffold), owned by the neutral harness engineer, **sequenced before Epics 2 and 3** and frozen with the manifest. This is the real sequencing blocker.
2. **C-2 — Add a story for the FR-35 free-text blind-rater protocol** (Epic 4 or Epic 1), wiring `pain`/`split_terms`/verbal-ownership scoring and the SM-4 structural-win adjudication into the async rating queue (architecture §6.4).

### Recommended Next Steps
1. Have **John (PM)** add: the foundation epic (C-1), the FR-35 story (C-2), an FR-13b AC on Epic 2 (M-1), an invariant-7 AC on Epic 3 (M-3), and a project-setup + PII-guard story (M-4). Update the **FR Coverage Map** to include FR-13b and FR-35 (raising the explicit count to 36).
2. **Re-label Epic dependencies** (M-2): "Epics 1–3 author in parallel; the kernel (foundation) and the simulator (Epic 4) are prerequisites for *running/acceptance* of Epics 2–3." This protects the build plan from a false-parallelism assumption.
3. **Assign the combined-verdict owner** (m-1) — fold the §7.1 matrix synthesis into Story 4.8 or a new closing story that reads both verdicts.
4. Resolve the carried PRD opens that gate work: **OPEN-1** (resourcing / FR-10 two authors — also gates the kernel owner, architecture R-8), **OPEN-2** (de-id method — gates Epic 5 / Story 5.1).

### Final Note
This assessment identified **9 issues across 3 severity tiers** (2 Critical, 4 Major, 3 Minor) — all traceability/sequencing gaps from epics-before-architecture ordering, none requiring a spec redesign. Address C-1 and C-2 before implementation; M-1…M-4 are quick epic edits; the minors can ride into the first sprint. The PRD, schema, and PoC-plan themselves are implementation-ready.

---

## 7. Re-Run Verification (2026-06-02, post-PM revision)

John (PM) revised `epics.md` (618 → 696 lines) in response to §1–§6. Re-traced every finding:

| ID | Finding | Resolution in revised epics | Status |
|----|---------|------------------------------|--------|
| **C-1** | Shared kernel had no story | **New Epic 0** — Story 0.1 (7-tool contract, `ProfileState`, trace event schema, `System` protocol, dual-provider temp-enforced LLM client; neutral owner; frozen before Epics 2/3) + Story 0.2 (scaffold, pinned lockfile, validated run-config, CI PII guard). Build order + Resourcing updated. | ✅ Closed |
| **C-2** | FR-35 unhomed | **New Story 4.9** — async blind-rater queue, ≥2 raters, tie-breaker, κ reported, SM-4 adjudicated, protocol approved pre-freeze. FR-35 → Epic 4 in coverage map. | ✅ Closed |
| **M-1** | FR-13b untraced | Added to inventory, FR Coverage Map, Epic 2 FR list, and Story 2.3 AC (tree emits identical tool vocab + trace events; FR-23/FR-24 run unmodified). | ✅ Closed |
| **M-2** | False epic parallelism | Overview relabeled: Epic 0 + Epic 4 simulator are prerequisites for *acceptance* of Epics 2/3. | ✅ Closed |
| **M-3** | Invariant 7 untraced | Story 3.3 ACs added: IDK = absence, 60-turn `incomplete` cap, `end_section` guard. | ✅ Closed |
| **M-4** | No setup / PII-guard story | Story 0.2 (scaffold, lockfile, run-config validation, CI PII commit-guard). | ✅ Closed |
| **m-1** | Combined verdict owner | Story 4.8 AC now owns the §7.1 H1×H2 matrix synthesis (reads H1 here, H2 from 5.5). | ✅ Closed |
| **m-2** | Story 2.5 softened FR-10 | Now requires explicit interpretation-discount naming which metrics + by how much; "caveat alone insufficient." | ✅ Closed |
| **m-3** | FR-15 H1 seed missing | Story 1.1 AC: ≥1 scored profile seeds a note-prefill conflicting with a spec fact (EC-17). | ✅ Closed |

**Coverage:** FR Coverage Map now traces all **36** FR-level items (FR-1..FR-35 + FR-13b); count stated explicitly. NFR-1..5 covered. Agent invariants 1–7 now all traced.

### Updated Overall Status: ✅ **READY for implementation**

All 9 findings closed; no regressions introduced.

**Two non-blocking notes (no action required to proceed):**
- **N-1 (acknowledged, acceptable):** Epic 0 is a *technical-foundation* epic, not user-value-framed — normally an epic-quality red flag, but it's the legitimate greenfield exception (a neutral shared kernel genuinely must precede the SUTs, and FR-10 requires neutral ownership). Correct call.
- **N-2 (optional polish):** Story 4.5 (SAR scoring) doesn't explicitly note that free-text slots route to Story 4.9 rather than the automatic disposition scorer. The ownership is unambiguous (4.9 clearly owns free-text), so this is a one-line cross-reference at most — fine to leave or fold into the first sprint.

### Remaining gates (process, not artifacts)
- **OPEN-1** — resourcing; must name the neutral Epic 0 engineer + tree author + agent author (FR-10) before freeze. Now explicitly tracked in Resourcing (D6).
- **OPEN-2** — de-identification method; gates Epic 5 / Story 5.1.
