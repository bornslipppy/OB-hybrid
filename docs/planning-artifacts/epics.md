---
title: "AI Adaptive Onboarding PoC - Epic Breakdown"

stepsCompleted: ["step-01-validate-prerequisites", "step-02-design-epics", "step-03-create-stories"]
inputDocuments:
  - docs/planning-artifacts/prds/prd-AI-Adaptive-Onboarding-PoC-2026-06-02/prd.md
  - docs/planning-artifacts/poc-plan-ai-adaptive-onboarding-2026-06-02.md
  - docs/planning-artifacts/guesty-pro-account-creation-schema.md
project: "AI Adaptive Onboarding PoC"
created: 2026-06-02
author: John (PM agent)
---

# AI Adaptive Onboarding PoC - Epic Breakdown

## Overview

This document decomposes the requirements from the [AI Adaptive Onboarding PoC PRD](prds/prd-AI-Adaptive-Onboarding-PoC-2026-06-02/prd.md) into implementable epics and stories for the build team. The PoC is an **offline evaluation harness** that tests two falsifiable claims: **H1** (an AI agent fills a more complete/accurate onboarding profile than an honest decision tree) and **H2** (an LLM extracts better prefill from real sales handover notes than a regex baseline).

Epics are organized by **deliverable value to the eval team**, not technical layers. Each epic is standalone and produces a usable artifact. Build order: **Epic 0 (shared kernel + scaffold) must be completed and frozen before Epics 2 and 3 can be accepted.** Epics 1–3 author in parallel; the kernel (Epic 0) and the Epic 4 simulator are prerequisites for running/acceptance of Epics 2 and 3. Epic 4 (the harness + verdict) consumes the outputs of 0–3; Epic 5 (H2) is fully independent and runs in parallel throughout.

> Decisions D1–D6 governing this breakdown live in [`.decision-log.md`](prds/prd-AI-Adaptive-Onboarding-PoC-2026-06-02/.decision-log.md). Owners for each epic are tracked in §"Resourcing (D6)" at the foot of this document.

## Requirements Inventory

### Functional Requirements

- **FR-1** Schema-driven next-slot selection (agent)
- **FR-2** Fixed tool surface (agent)
- **FR-3** Hero-branch ownership fan-out, intent-capture only (agent)
- **FR-4** Conditional Booking-Website (S5) surfacing (agent)
- **FR-5** Vocabulary normalization to canonical slots (agent)
- **FR-6** Model & temperature configuration (agent)
- **FR-7** Branch on every schema `depends_on` (tree)
- **FR-8** Behavioral-path parity: echo / flag / skip (tree)
- **FR-9** Authored blind to the test profiles — anti-leakage (tree)
- **FR-10** Independent authorship (tree author ≠ agent-prompt author)
- **FR-11** Fairness sign-off (tree)
- **FR-12** Tooling parity: same NLU map + canonical enums (tree)
- **FR-13** Capability ledger + authoring-hours + time-to-update (tree)
- **FR-13b** Tree tool-call trace parity — tree emits the identical FR-2 tool vocabulary and trace event schema as the agent
- **FR-14** Structured extraction with provenance (H2 extractor)
- **FR-15** Confirm-before-use precedence (H2 extractor)
- **FR-16** Brief-only sensitive slots (H2 extractor)
- **FR-17** Regex baseline comparator (H2)
- **FR-18** Abstention on sparse/empty notes (H2 extractor)
- **FR-19** Faithful, spec-bounded simulator answers
- **FR-20** No target leakage (simulator)
- **FR-21** Decorrelated from the agent (simulator provider)
- **FR-22** Drive both systems, k≥5 runs (harness)
- **FR-23** SAR scoring by disposition (harness)
- **FR-24** Secondary-metric computation incl. false-write detection (harness)
- **FR-25** Statistical reporting honest to N=8 (harness)
- **FR-26** Dev/test freeze discipline (harness/process)
- **FR-27** Eight scored respondent specs across A/B/C
- **FR-28** ≥4 dev/calibration profiles
- **FR-29** Two-reviewer + tie-breaker answer-key validation
- **FR-30** Contested-slot adjudication + sensitivity band
- **FR-31** Simulator validation spot-check
- **FR-32** Full-length, de-identified note pull (H2)
- **FR-33** Stratified gold labeling + dev/test split (H2)
- **FR-34** Flag-quality blind rating (H2)
- **FR-35** Free-text blind-rater protocol — ≥2 raters blind to system score `pain`, `split_terms`, and verbal-ownership slots; tie-breaker adjudicates SM-4 structural win

### NonFunctional Requirements

- **NFR-1** (PRD §4.1) The agent emits, per completed profile, a machine-readable tool-call trace sufficient for false-write detection and questions-to-completion counting.
- **NFR-2** (PRD §8) Determinism on financial/numeric fields comes from the echo-before-write gate, not from temperature; the build must enforce the gate structurally.
- **NFR-3** (PRD §9) PII governance: no raw (PII-bearing) handover notes committed to the repo; de-identify before any human labeling or extractor run; raw-note access restricted to the data/RevOps owner; provenance spans de-identified.
- **NFR-4** (PRD §4.5 / FR-26) Reproducibility: seeds pinned where the API supports it; scored set frozen and run once; any post-freeze change requires re-freeze + re-run noted in the report.
- **NFR-5** (PRD §7 SM-10) Cost/latency (tokens, USD, wall-clock) measured and reported per completed profile for the agent.

### Additional Requirements

- **Agent invariants (PRD §8):** echo-before-write; never advise; one clarifying question then flag+skip; honor skip immediately; never correct tax/legal; intent-capture only on the hero branch. These are acceptance gates on Epic 3 and (where applicable) Epic 2.
- **Success metrics (PRD §7):** SM-1…SM-11 + counter-metrics SM-C1…SM-C3 are the pre-registered decision heuristics the Epic 4 report must compute and the Epic 5 report must compute for H2.
- **Kill criteria (PRD §10):** hard stops (false-write > 0, inappropriate-advice > 0, Group-A regression > 5pp, no stable B+C advantage) — the Epic 4 verdict must evaluate these explicitly.

### UX Design Requirements

None. This is an offline eval harness with no UI by design (PRD §5 Non-Goals). The simulated host is *modeled* by Epic 4, not served by a UI.

### FR Coverage Map

- FR-1: Epic 3 — agent next-slot selection
- FR-2: Epic 3 — agent tool surface
- FR-3: Epic 3 — hero branch intent-capture
- FR-4: Epic 3 — conditional S5
- FR-5: Epic 3 — vocabulary normalization
- FR-6: Epic 3 — model/temperature config
- FR-7: Epic 2 — tree depends_on branching
- FR-8: Epic 2 — tree behavioral parity
- FR-9: Epic 2 — tree blind authoring
- FR-10: Epic 2 — independent authorship
- FR-11: Epic 2 — fairness sign-off
- FR-12: Epic 2 — tooling parity
- FR-13: Epic 2 — capability ledger
- FR-13b: Epic 2 — tree tool-call trace parity
- FR-14: Epic 5 — extractor provenance
- FR-15: Epic 5 — confirm-before-use precedence
- FR-16: Epic 5 — brief-only slots
- FR-17: Epic 5 — regex baseline
- FR-18: Epic 5 — abstention
- FR-19: Epic 4 — simulator faithfulness
- FR-20: Epic 4 — simulator no-leakage
- FR-21: Epic 4 — simulator decorrelation
- FR-22: Epic 4 — harness k≥5 runs
- FR-23: Epic 4 — SAR scoring
- FR-24: Epic 4 — secondary metrics
- FR-25: Epic 4 — statistical reporting
- FR-26: Epic 4 — freeze discipline
- FR-27: Epic 1 — scored respondent specs
- FR-28: Epic 1 — dev profiles
- FR-29: Epic 1 — answer-key validation
- FR-30: Epic 1 — contested-slot adjudication
- FR-31: Epic 4 — simulator validation spot-check
- FR-32: Epic 5 — de-identified note pull
- FR-33: Epic 5 — stratified labeling
- FR-34: Epic 5 — flag-quality blind rating
- FR-35: Epic 4 — free-text blind-rater protocol

> **Total FR-level items: 36** (FR-1..FR-35 + FR-13b)

## Epic List

### Epic 0: Shared Kernel & Scaffold
Build the neutral foundation the experiment depends on — the 7-tool contract, `ProfileState` reducer, richer trace event schema (carrying `value_introduced`, `echo_issued`, `user_confirmed` per architecture §3.3), `System` protocol, dual-provider LLM client with enforced `scored_completion`/`glue_completion` temperature modes, project scaffold, pinned lockfile (freeze manifest), run-config TOML with provider-decorrelation + temperature validation, and the CI PII commit-guard. This kernel must be frozen before Epics 2 and 3 begin acceptance. Owner = neutral harness engineer (FR-10 / architecture R-8).
**Architecture drivers:** D-1, D-8, R-8 | **NFRs:** NFR-1 (trace schema), NFR-2 (structural determinism gate), NFR-3 (CI PII guard), NFR-4 (freeze-manifest lockfile)

### Epic 1: Ground-Truth Test Bench
Produce the frozen, human-validated dataset the whole H1 experiment scores against: 8 scored respondent specs (facts + persona + per-slot expected dispositions) across Groups A/B/C, ≥4 dev/calibration profiles, two-reviewer + tie-breaker validation, and the contested-slot adjudication protocol. After this epic the eval team has an answer key they trust.
**FRs covered:** FR-27, FR-28, FR-29, FR-30

### Epic 2: Honest Baseline Tree
Build the deterministic comparator the AI must beat — authored from the schema, blind to the profiles, with behavioral-path parity (echo/flag/skip), tooling parity (NLU map + enums), independent authorship, a fairness sign-off, and a capability ledger that records authoring hours and time-to-update. After this epic the eval team has a runnable, certified-fair baseline plus the maintenance-cost evidence.
**FRs covered:** FR-7, FR-8, FR-9, FR-10, FR-11, FR-12, FR-13, FR-13b

### Epic 3: AI Adaptive Agent
Build the system under test — a schema-driven LLM agent that fills the frame through conversation, decides the next slot itself, obeys the §8 invariants, captures the hero-branch ownership fan-out as intent-only, surfaces S5 conditionally, and normalizes user vocabulary. After this epic the eval team has a runnable agent that produces traceable tool calls.
**FRs covered:** FR-1, FR-2, FR-3, FR-4, FR-5, FR-6 (+ agent invariants §8, NFR-1, NFR-2, NFR-5)

### Epic 4: Eval Harness & H1 Verdict
Build the rig that turns the above into a defensible answer: a faithful, decorrelated user simulator; a harness that drives both systems k≥5 times through it; SAR scoring by disposition; secondary metrics with programmatic false-write detection; bootstrap CIs + decision-stability honest to N=8; and a comparison report that evaluates the §7 thresholds and §10 kill criteria. After this epic the eval team has the H1 verdict.
**FRs covered:** FR-19, FR-20, FR-21, FR-22, FR-23, FR-24, FR-25, FR-26, FR-31, FR-35 (+ NFR-4)

### Epic 5: H2 Note → Prefill Extraction
Build the separable, real-data sub-experiment: a full-length de-identified note pull, stratified gold labeling with dev/test split, an LLM extractor with provenance and abstention, confirm-before-use precedence, a regex baseline, and a blind flag-quality rating — scored on the ≥15pp F1 margin and ≤10% false-prefill ceiling. After this epic the eval team has the H2 verdict, independent of H1.
**FRs covered:** FR-14, FR-15, FR-16, FR-17, FR-18, FR-32, FR-33, FR-34 (+ NFR-3)

---

## Epic 0: Shared Kernel & Scaffold

Build the neutral foundation that both the agent (Epic 3) and baseline tree (Epic 2) depend on. This kernel must be frozen and committed to the freeze manifest before acceptance of Epics 2 and 3.

### Story 0.1: Build the shared neutral kernel

As a neutral harness engineer,
I want a shared library that defines the 7-tool contract, `ProfileState` reducer, richer trace event schema, `System` protocol, and a dual-provider LLM client with enforced temperature modes,
So that both the agent and the tree are implemented against an identical, auditable interface that cannot be optimized for either arm.

**Acceptance Criteria:**

**Given** architecture §3 (tool surface + state machine), §4 (LLM client), §3.3 (trace event schema)
**When** the shared kernel is built
**Then** it exports exactly the 7 tools: `record_answer`, `add_fee`, `add_tax`, `add_owner`, `skip_question`, `flag_for_call_1`, `end_section` — with schema-validated argument shapes
**And** `ProfileState` is a pure reducer — all state transitions are mediated by the kernel; no direct field mutation is permitted
**And** the trace event schema emits `value_introduced`, `echo_issued`, and `user_confirmed` per event (richer than raw tool-calls, per architecture §3.3)
**And** the `System` protocol specifies per-turn input/output shapes for both the agent and the tree client
**And** the dual-provider LLM client exposes exactly two call modes: `scored_completion` (temperature locked to 0.0, for all tool-call-emitting turns) and `glue_completion` (temperature 0.2, for conversational transitions only); the temperature enforcement is structural — no call site can override it
**And** the kernel is authored by the neutral harness engineer, not the Epic 2 tree author or the Epic 3 agent-prompt author (FR-10 / architecture R-8)
**And** the kernel is version-tagged and recorded in the freeze manifest before any Epic 2 or Epic 3 acceptance run begins

### Story 0.2: Project setup — scaffold, lockfile, run-config TOML, and CI PII commit-guard

As a harness engineer,
I want a complete project scaffold with a pinned lockfile, a validated run-config TOML, and an automated CI PII commit-guard,
So that the experiment is reproducible from a clean checkout and PII cannot be accidentally committed (architecture D-8).

**Acceptance Criteria:**

**Given** a clean repository checkout
**When** the scaffold is applied
**Then** the project directory structure follows the architecture-defined layout (dirs for `kernel/`, `profiles/`, `runs/`, `reports/`)
**And** all dependency versions are pinned in the lockfile; the lockfile is part of the freeze manifest (NFR-4)
**And** a `run-config.toml` exists specifying at minimum: agent provider/model, simulator provider/model, temperature policy, k (number of runs), seed strategy, and freeze-manifest path; the config is validated on load — a temperature value other than 0.0 on any scored-slot code path is a startup error
**And** the CI pipeline includes a PII commit-guard (architecture D-8) that blocks any commit touching `profiles/raw/` or matching a configurable PII filename pattern (NFR-3)
**And** the guard is active before any note-pull work begins (Epic 5 / Story 5.1 dependency)

---

## Epic 1: Ground-Truth Test Bench

Produce the frozen, human-validated answer key the H1 experiment scores against.

### Story 1.1: Author the eight scored respondent specs across Groups A/B/C

As an eval engineer,
I want eight scored respondent specs, each split into ground-truth facts, a persona/behavior directive, and a per-slot expected-disposition answer key,
So that the same spec can drive both systems and a correctly-flagged slot can score as correct.

**Acceptance Criteria:**

**Given** the PoC plan §5 profile roster (A1–A2, B1–B4, C1–C2)
**When** the specs are authored
**Then** each spec contains the three parts (facts, persona directive, answer key)
**And** each scored slot in the answer key carries exactly one disposition: `recorded:<value>`, `flagged`, `skipped`, or `conditional:surface_if_direct_signals`
**And** Group A ground-truth values align with the existing "Pinkie Flamingo" sample where they overlap
**And** the answer keys use provisional G3 enum casing, marked for re-freeze if G3 closes before the run (OPEN-3)
**And** at least one scored profile seeds a handover-note prefill value that conflicts with a spec fact (e.g., note says one PMS but spec says another) — this seeds the FR-15 H1 precedence/conflict-surfacing test (EC-17)

### Story 1.2: Author the dev/calibration profile set

As an eval engineer,
I want at least four dev profiles spanning the same A/B/C dimensions but disjoint from the scored eight,
So that I can tune prompts and debug the tree without overfitting the scored set.

**Acceptance Criteria:**

**Given** the scored eight from Story 1.1
**When** the dev profiles are authored
**Then** there are ≥4 dev profiles covering Group A, B, and C dimensions
**And** no dev profile duplicates a scored profile's facts or answer key
**And** the dev set is clearly labeled as tuning-only (never scored)

### Story 1.3: Validate answer keys with two reviewers and a tie-breaker

As an answer-key reviewer,
I want each answer key independently validated by two reviewers with a third tie-breaker for disagreements,
So that "correct" is agreed before any system is scored.

**Acceptance Criteria:**

**Given** the eight scored answer keys
**When** validation runs
**Then** each answer key records two independent reviewer validations
**And** every disagreement is routed to the tie-breaker and an adjudication record is attached
**And** validation completes before any eval run begins

### Story 1.4: Establish the contested-slot adjudication and sensitivity-band protocol

As a decision-maker,
I want contested slots adjudicated rather than dropped, and reported as a best/worst sensitivity band,
So that the cases that most test AI's advantage do not silently bias the result toward the null.

**Acceptance Criteria:**

**Given** a slot where reviewers cannot agree on the ground-truth disposition
**When** the protocol is applied
**Then** the slot is adjudicated by the tie-breaker and retained in the SAR denominator
**And** the protocol specifies the report shows SAR with adjudicated values AND as a best/worst sensitivity band
**And** no contested slot is removed from scoring

---

## Epic 2: Honest Baseline Tree

Build the certified-fair deterministic comparator and the maintenance-cost evidence.

### Story 2.1: Author the decision tree over the schema's depends_on graph, blind to the profiles

As a tree author,
I want to author the tree from the schema's `depends_on` graph and documented behavioral paths only, without seeing the test profiles,
So that the baseline cannot be reverse-engineered to pass the known cases (anti-leakage).

**Acceptance Criteria:**

**Given** the account-creation schema (v0.3) and no access to the scored profiles or answer keys
**When** the tree is authored
**Then** every `depends_on` guard in the schema maps to a tree branch or an explicitly documented fallback
**And** the full S8 ownership × management-model × per-owner fan-out and the S4 payment-split path are branched
**And** a written attestation records authoring was frozen before any profile exposure

### Story 2.2: Encode behavioral-path parity (echo / flag / skip)

As a tree author,
I want the tree to apply echo-before-write, flag-for-call-1, and skip+flag fallback exactly where the schema's behavioral paths require,
So that the baseline is judged on capability, not on missing safety behaviors the agent has.

**Acceptance Criteria:**

**Given** the schema's echo/flag/skip behavioral paths
**When** the tree runs any profile
**Then** the tree's false-write rate is 0 on numeric/financial fields
**And** tax slots are flagged and never corrected
**And** ambiguous inputs the schema implies route to a `skip+flag` fallback node

### Story 2.3: Wire tooling parity (NLU map + canonical enums)

As a tree author,
I want the tree to receive the same NLU vocabulary-normalization map and canonical enums the agent gets,
So that the comparison isolates reasoning capability, not synonym-matching handicaps.

**Acceptance Criteria:**

**Given** the schema §10 normalization map and canonical enums
**When** the tree processes user vocabulary (e.g., "portals", "cut")
**Then** the tree resolves them to canonical slots the same way the agent can
**And** failures attributable to literal string matching are not counted as tree weakness
**And** the tree emits the identical FR-2 tool vocabulary (the same 7 tools with schema-validated argument shapes from the shared kernel) and the shared trace event schema (`value_introduced`, `echo_issued`, `user_confirmed`) as the agent; FR-24 false-write detection and FR-23 disposition scoring run unmodified on the tree's trace (FR-13b)

### Story 2.4: Produce the capability ledger with authoring time and time-to-update

As a decision-maker,
I want a documented ledger of what the tree can and cannot do, plus authoring hours and the time to extend the tree for one realistic schema change,
So that I have the evidence for the authoring-cost argument and the Group-C "impractical-authoring" alternative.

**Acceptance Criteria:**

**Given** the completed tree
**When** the ledger is produced
**Then** it lists which `depends_on` paths the tree branches and where it falls back to `skip+flag`
**And** it records authoring hours for the tree
**And** it records time-to-update for one realistic schema change (e.g., adding a `management_model` enum value), measured for both tree and agent

### Story 2.5: Obtain independent authorship and fairness sign-off

As an eval engineer,
I want the tree authored by someone other than the agent-prompt author and certified competent by a second reviewer before scoring,
So that neither artifact is optimized to make the other look bad.

**Acceptance Criteria:**

**Given** the build staffing
**When** authorship is assigned
**Then** the tree author is a different person than the agent-prompt author (or, under FR-10's compensating-control path, the deviation is documented with an explicit interpretation-discount naming which metrics are discounted and by how much — "documented as a fairness caveat" alone is insufficient)
**And** a second reviewer certifies in writing the tree is a competent, good-faith attempt
**And** the fairness certification exists before the frozen run

---

## Epic 3: AI Adaptive Agent

Build the runnable system-under-test that fills the frame conversationally and traceably.

### Story 3.1: Implement schema-driven next-slot selection

As an eval engineer,
I want the agent to choose the next slot from the frame's unanswered fields and their `depends_on` guards rather than a fixed list,
So that it demonstrates genuine adaptivity, not a scripted order.

**Acceptance Criteria:**

**Given** two profiles whose early answers diverge
**When** the agent runs each
**Then** its question order diverges accordingly
**And** it never asks about a slot whose `depends_on` guard is unmet (e.g., no owner economics when `ownership_model = all_self_owned`)
**And** it pursues every slot in the in-scope scored slot set (all tiers — `required` + `recommended` + `optional` — reachable for the profile), not just the `required` MVP line
**And** it stops only when all reachable in-scope slots are dispositioned or the §8 max-turn guard fires; stopping at the MVP-completeness line while reachable `recommended`/`optional` in-scope slots remain undispositioned is a SAR penalty, not a valid stop (FR-1 / C1 / EC-10)

### Story 3.2: Implement the fixed tool surface and profile-state mutation

As an eval engineer,
I want the agent to mutate profile state only through the seven fixed tools,
So that every state change is traceable and scorable.

**Acceptance Criteria:**

**Given** a running conversation
**When** the agent records, skips, or flags any slot
**Then** every mutation corresponds to exactly one of `record_answer`, `add_fee`, `add_tax`, `add_owner`, `skip_question`, `flag_for_call_1`, `end_section`
**And** tool arguments conform to the schema `item_shape` for the targeted slot
**And** no entity is free-written outside the tool surface

### Story 3.3: Enforce the agent behavioral invariants

As a decision-maker,
I want the agent to obey the §8 invariants without exception,
So that the experiment is safe and the determinism guarantee holds where it matters.

**Acceptance Criteria:**

**Given** a numeric/financial field with `echo_before_write`
**When** the user states a value
**Then** the agent echoes it and fires the write tool only after a later confirmation turn (false-write rate 0)
**Given** an advice-seeking turn
**When** the user asks for a recommendation
**Then** the agent flags for Call 1 and never recommends a choice, even under pressure
**And** an ambiguous answer triggers at most one clarifying question, then flag+skip
**And** a skip/defer is honored immediately with no retry, no "are you sure", no upsell
**And** tax/legal facts are recorded as stated and flagged, never corrected
**Given** a user answer of "I don't know", a deferral, or an absent fact
**When** the agent encounters it
**Then** the agent treats IDK / absent-fact as absence of the value and routes to `skip_question` or `flag_for_call_1` — it does not spend a clarifying question on an absent fact (PRD §8 inv 7)
**Given** a conversation that reaches 60 turns without all reachable in-scope slots dispositioned
**When** the turn counter fires
**Then** the session terminates with status `incomplete` — the agent does not continue past 60 turns
**And** `end_section` is forbidden while any reachable in-scope slot in that section remains undispositioned; attempting to end a section early is a protocol error (architecture §3.2/§3.4)

### Story 3.4: Implement the hero-branch ownership fan-out as intent-capture only

As an eval engineer,
I want the agent to capture per-owner records and economics in plain language and flag them for Call 1, without writing BusinessModel records,
So that it realizes the CEO's combinatorial scenario within the G1 intent-capture boundary.

**Acceptance Criteria:**

**Given** a profile with `ownership_model` in {`all_managed_for_others`, `mixed`}
**When** the agent runs the hero branch
**Then** owner fields (name, email, listings, share, management_model + economics) are captured via `add_owner` and score against `recorded:<value>`
**And** no BusinessModel creation appears in the tool trace
**And** captured owner economics are accompanied by a `flag_for_call_1` carrying the owner context
**And** `who_pays_channel_commission` is captured distinctly from `pmc_commission_rate`
**And** the agent asks "how do you get paid for managing these?" rather than using the term "Business Models"

### Story 3.5: Implement conditional Booking-Website (S5) surfacing

As an eval engineer,
I want the agent to surface S5 only when direct-booking signals are present,
So that it matches the G6 resolution and is scored against the `conditional` disposition.

**Acceptance Criteria:**

**Given** a profile with no direct-booking signal
**When** the agent runs
**Then** S5 slots are skipped (and surfacing them would score wrong)
**Given** a profile with a direct-booking signal (channel includes `direct`, "my website", `booking_website` focus topic, or non-OTA-exclusive operation)
**When** the agent runs
**Then** S5 slots are surfaced (and not surfacing them would score wrong)

### Story 3.6: Implement vocabulary normalization to canonical slots

As an eval engineer,
I want the agent to map user vocabulary to canonical slots using the schema §10 map,
So that messy real-world phrasing is captured correctly.

**Acceptance Criteria:**

**Given** profile B3 (vocabulary mismatch: "prices", "portals", "payout", "cleaning fee")
**When** the agent runs it
**Then** all slots normalize to canonical terms
**And** un-normalized literal values score wrong

### Story 3.7: Configure model/temperature and emit a machine-readable trace

As an eval engineer,
I want the agent to run at temperature 0.0 on every scored slot (all extraction that feeds SAR, plus all numeric-echo and financial writes) and 0.2 only on unscored conversational glue, and emit a complete tool-call trace per profile,
So that determinism is enforced structurally on the headline deltas (FR-6 / M5 resolution) and false-write/questions-to-completion can be computed.

**Acceptance Criteria:**

**Given** the agent run configuration
**When** any turn emits a tool call on a scored slot (extraction, numeric-echo, or financial write)
**Then** it is issued under temperature 0.0 (verifiable from run config/logs), enforced by construction (no scored-slot code path permits temperature ≠ 0.0)
**And** temperature 0.2 is permitted only on unscored conversational glue (greetings, transitions) that emits no tool calls
**And** the agent emits a machine-readable tool-call trace per completed profile sufficient for false-write detection and question counting (NFR-1)
**And** token/USD/latency are captured per completed profile (NFR-5)

---

## Epic 4: Eval Harness & H1 Verdict

Build the rig that produces a defensible H1 answer.

### Story 4.1: Build a faithful, spec-bounded, leak-free user simulator

As an eval engineer,
I want a simulator that answers from the respondent spec's facts and persona only, never sees the answer key, and never invents facts,
So that both systems face an identical, honest user and outcome differences are attributable to the system.

**Acceptance Criteria:**

**Given** a respondent spec and a question from either system
**When** the simulator replies
**Then** the reply contains no facts absent from the spec
**And** if asked something the spec doesn't cover, it answers "I don't know" or defers per persona
**And** the simulator's input payload excludes the answer-key dispositions (verifiable from the call signature)

### Story 4.2: Decorrelate the simulator from the agent

As an eval engineer,
I want the simulator to use a different model family/provider than the agent (or scripted turns for Group A),
So that correlated blind spots don't flatter the AI.

**Acceptance Criteria:**

**Given** the run configuration
**When** the harness is set up
**Then** it records distinct providers for agent vs. simulator
**And** Group A replies may be deterministic scripted canned turns

### Story 4.3: Validate the simulator before the frozen run

As an answer-key reviewer,
I want to spot-check simulator transcripts before scoring,
So that a bad simulator cannot silently corrupt both arms.

**Acceptance Criteria:**

**Given** simulator transcripts on dev profiles
**When** reviewers spot-check them
**Then** they confirm faithful answers and no leakage/fabrication
**And** a spot-check sign-off exists before the frozen run

### Story 4.4: Drive both systems k≥5 times under freeze discipline

As an eval engineer,
I want the harness to run each frozen profile through both systems at least five times with seeds pinned where supported,
So that I can report variance and the scored set is run once on frozen systems.

**Acceptance Criteria:**

**Given** the frozen eight profiles and both systems
**When** the harness runs
**Then** it produces ≥5 runs per profile per system with seeds pinned where the API supports it
**And** all prompt tuning and tree debugging happened only on the dev set (verifiable from the run record)
**And** any post-freeze change to a system triggers a documented re-freeze + re-run (NFR-4)

### Story 4.5: Score SAR by expected disposition

As an eval engineer,
I want the harness to score each slot against the answer key's expected disposition per the §6.1 rubric,
So that flagged/skipped/recorded outcomes are scored correctly, not by naive value match.

**Acceptance Criteria:**

**Given** a slot with disposition `flagged`
**When** the system flags it for Call 1 without correcting
**Then** it scores 1; recording it as a definitive answer scores 0
**Given** a slot with disposition `recorded:<value>` of money/percentage type
**When** the recorded value differs from ground truth (e.g., 15% vs 50%)
**Then** it scores 0 (exact match required for numbers)
**And** SAR is aggregated at the slot level, separated per group (A/B/C) and per section (S4/S8/cross-section)

### Story 4.6: Compute secondary metrics with programmatic false-write detection

As a decision-maker,
I want the harness to compute questions-to-completion, clarification efficiency, false-write rate, inappropriate-advice rate, and agent cost/latency,
So that the verdict covers safety and efficiency, not just accuracy.

**Acceptance Criteria:**

**Given** the tool-call traces from both systems
**When** the harness computes metrics
**Then** false-write rate is computed programmatically per the §3 definition (write on an echo field in the same turn, no intervening confirmation)
**And** questions-to-completion counts user-facing asks identically for both systems
**And** clarification efficiency, inappropriate-advice rate, and agent token/USD/latency per profile are reported

### Story 4.7: Report statistics honest to N=8

As a decision-maker,
I want slot-level bootstrap CIs clustered by profile, per-profile case studies, and a decision-stability figure,
So that I am not misled by a lucky run or false profile-level significance.

**Acceptance Criteria:**

**Given** the k≥5 runs per profile
**When** the report is generated
**Then** it reports slot-level SAR with bootstrap CIs clustered by profile
**And** per-profile results are presented as illustrative case studies, not population estimates
**And** any slot whose disposition flips across runs is flagged as a reliability red flag
**And** no profile-level significance claims are made

### Story 4.8: Produce the H1 comparison report and verdict

As a decision-maker,
I want a comparison report that evaluates the §7 thresholds and §10 kill criteria,
So that I get a clear, defensible recommendation on whether to fund the live build.

**Acceptance Criteria:**

**Given** the computed SAR, CIs, secondary metrics, and stability
**When** the report is compiled
**Then** it states pass/fail against SM-1 (Group A ≤5pp regression), SM-2 (≥15pp Group B, CI clears zero, stable), SM-3 (≥25pp Group C or impractical-authoring ledger), and SM-4 (≥1 qualitative structural win)
**And** it evaluates each §10 kill criterion explicitly (false-write 0, advice 0, Group-A regression, stable B+C advantage)
**And** it carries a go/no-go-style recommendation framed as exploration evidence (D1), not a binding gate
**And** it produces the combined H1×H2 verdict matrix (PRD §7.1 / UJ-4): a 2×2 grid (H1 supported/not × H2 supported/not → build-recommendation), reading the H1 verdict from this story and the H2 verdict from Story 5.5; Story 4.8 owns this synthesis

### Story 4.9: Implement the free-text blind-rater protocol and adjudicate SM-4

As a decision-maker,
I want free-text scored slots (`pain`, `split_terms`, verbal-ownership captures) rated by ≥2 raters blind to the producing system, with a tie-breaker and inter-rater κ reported,
So that SM-4 (the required qualitative structural win) can be adjudicated and free-text SAR has a defined, auditable scorer.

**Acceptance Criteria:**

**Given** free-text slot values emitted by either the agent or the tree (including `pain`, `split_terms`, and verbal-ownership capture slots)
**When** the rating pipeline runs
**Then** all free-text values are queued to the async rating queue (architecture §6.4) with system attribution stripped before presentation to raters
**And** ≥2 raters independently score each value against the "captures the same fact" rubric (correct: captures the substance; incorrect: missing, fabricated, or wrong substance)
**And** disagreements are routed to the tie-breaker and adjudicated; the adjudication record is attached to the slot rating
**And** Cohen's κ (or equivalent inter-rater agreement) is computed across all rated slots and reported in the comparison report
**And** SM-4 (≥1 qualitative structural win for the agent vs. the tree on a free-text slot) is adjudicated from the rated results, not by single-rater judgment
**And** the rating-protocol document (rubric, rater instructions, tie-breaker criteria) exists and is approved before the frozen run begins

---

## Epic 5: H2 Note → Prefill Extraction

Build the separable real-data extraction sub-experiment and its verdict.

### Story 5.1: Pull and de-identify full-length handover notes

As a data/RevOps owner,
I want a full-length re-pull of the handover notes from Salesforce, de-identified before any use,
So that the extractor and labelers work on complete, PII-safe text.

**Acceptance Criteria:**

**Given** the Salesforce export truncates notes at 255 chars
**When** the re-pull runs
**Then** notes are pulled at full length
**And** notes are de-identified before any human labeling or extractor run
**And** no raw (PII-bearing) note is committed to the repo (NFR-3)
**And** the de-identification method is confirmed with the data/RevOps owner before pulling (OPEN-2)

### Story 5.2: Build the stratified gold label set with dev/test split

As an answer-key reviewer,
I want ~40–60 notes hand-labeled across all six archetypes into gold S0b slots and risk flags, with two raters + tie-breaker and a dev/test split,
So that the extractor is tuned and scored without leakage.

**Acceptance Criteria:**

**Given** the de-identified corpus
**When** labeling runs
**Then** labels cover all six archetypes (A–F), including sparse/empty (F)
**And** each label is set by two raters with a tie-breaker for disagreements
**And** the set is split into a dev subset (tuning) and a held-out test subset (scoring)

### Story 5.3: Build the LLM extractor with provenance and abstention

As an eval engineer,
I want an LLM extractor that emits structured JSON with confidence and provenance per slot and abstains on sparse/empty notes,
So that it produces auditable prefill that doesn't fabricate.

**Acceptance Criteria:**

**Given** a handover note
**When** the extractor runs
**Then** every emitted slot carries a non-null provenance span quotable from the note plus a confidence value
**Given** a sparse/empty note (Archetype-F or an `NA` row)
**When** the extractor runs
**Then** it emits nothing rather than fabricating prefill
**And** the extractor prompt is tuned only on the dev subset (mirrors freeze discipline)

### Story 5.4: Enforce confirm-before-use precedence and brief-only slots

As an eval engineer,
I want extracted slots to enter as `prefilled_unconfirmed`, lose to structured and user-stated values, and require echo before becoming recorded; and sentiment/risk/tech slots to stay brief-only,
So that note-derived hints are confirmed, never silently trusted, and sensitive slots never leak to the user.

**Acceptance Criteria:**

**Given** an extracted slot and a conflicting `user_stated` value
**When** precedence is applied
**Then** `user_stated` wins and the conflict surfaces (e.g., "Note said Hostaway; user says Lodgify")
**And** no extracted slot is treated as recorded truth without a confirmation step
**And** `customer_sentiment`, `risk_flags`, and `tech_level` never appear in a user-facing turn and never gate the flow

### Story 5.5: Build the regex baseline and score the H2 verdict

As a decision-maker,
I want a regex baseline scored against the same held-out test notes on micro-F1 and false-prefill rate,
So that I know whether the LLM extractor clears the ≥15pp F1 margin and ≤10% false-prefill ceiling.

**Acceptance Criteria:**

**Given** the held-out test subset
**When** both extractors run
**Then** slot precision/recall/F1 (per field and micro-averaged) and confidence calibration are computed for both
**And** H2 is reported as supported only if the LLM beats regex by ≥15pp micro-F1 (SM-5)
**And** false-prefill rate on sparse/empty strata is ≤10% (SM-6); >10% fails H2 regardless of F1

### Story 5.6: Rate risk-flag quality blind to the producing system

As an answer-key reviewer,
I want risk flags rated by ≥2 raters blind to whether the LLM or regex produced them, with inter-rater agreement reported,
So that flag-quality scoring is not gameable.

**Acceptance Criteria:**

**Given** risk flags from both extractors
**When** raters score them
**Then** flags carry no system attribution at rating time
**And** ≥2 raters score each flag
**And** inter-rater agreement (e.g., Cohen's κ or % exact) is reported alongside the mean

---

## Resourcing (D6)

Per decision D6, owners are tracked here. **Constraint:** the Epic 2 tree author must be a different person than the Epic 3 agent-prompt author (FR-10).

| Role | Epics | Owner |
|------|-------|-------|
| **DRI / experiment gating authority** | All | **Yair Cohen** |
| **Engineer — neutral kernel + scaffold (≠ tree author, ≠ agent-prompt author)** | **0** | `[OWNER TBD]` |
| Reviewer 1 (answer keys + flags) | 1, 4, 5 | `[OWNER TBD]` |
| Reviewer 2 (answer keys + flags) | 1, 4, 5 | `[OWNER TBD]` |
| Tie-breaker reviewer | 1, 4, 5 | `[OWNER TBD]` |
| Data/RevOps (note pull + de-identify) | 5 | `[OWNER TBD]` |
| Engineer — agent + harness + extractor | 3, 4, 5 | `[OWNER TBD]` |
| Engineer/author — baseline tree (≠ agent author) | 2 | `[OWNER TBD]` |
| Fairness reviewer (tree sign-off) | 2 | `[OWNER TBD]` |

> **Yair Cohen** gates every phase transition. Operational roles must be assigned before the Phase 1 answer-key freeze (OPEN-1). Hard constraint: tree author ≠ agent-prompt engineer (FR-10).
