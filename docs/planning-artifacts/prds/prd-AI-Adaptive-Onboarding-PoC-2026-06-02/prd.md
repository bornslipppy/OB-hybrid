---
title: "AI Adaptive Onboarding PoC — Eval-Harness Build Spec"
status: draft (v2 — post Reviewer Gate)
created: 2026-06-02
updated: 2026-06-02
author: John (PM agent) with Yair Cohen
framing: "Funded exploration (D1). Decision heuristics inform a build recommendation; safety kill-criteria are hard stops."
based_on:
  - docs/planning-artifacts/brief-for-pm-2026-06-02.md
  - docs/planning-artifacts/poc-plan-ai-adaptive-onboarding-2026-06-02.md  # v1.2 — experiment design, source of truth
  - docs/planning-artifacts/guesty-pro-account-creation-schema.md  # v0.3 — the frame / SAR ground truth
  - docs/planning-artifacts/research/ai-adaptive-questionnaire-onboarding-research-2026-06-02.md
  - docs/planning-artifacts/sales-handover-notes-corpus-analysis-2026-06-02.md  # 611-note corpus (Claim H2)
---

# PRD: AI Adaptive Onboarding PoC (Eval-Harness Build Spec)

## 0. Document Purpose

This PRD specifies the **capabilities to build** for the AI Adaptive Onboarding Proof-of-Concept — a bounded, offline **evaluation harness** that tests, head-to-head against an honestly-built decision tree, whether an AI agent collects a more complete and accurate Guesty Pro customer profile than a tree can. It is written for:

- **The build engineer(s)** — to implement the agent, the baseline tree, the user simulator, the extractor, and the eval harness as discrete, testable components with stable FR references.
- **The reviewers and PM** — to know exactly which decision heuristics, kill criteria, and metrics govern the verdict (decisions D1–D6, ratified in `.decision-log.md`).
- **The downstream live-prototype PRD** — which is gated on a passing PoC and is **not** this document.

This PRD does **not** redesign the experiment. The **PoC plan (v1.2)** remains the source of truth for experimental rigor (anti-leakage protocol §4.1, dev/test split §5.1, statistical interpretation §6.2, repeated-runs §7-C4). The **account-creation schema (v0.3)** remains the source of truth for the frame, field semantics, and SAR ground truth. This PRD references both by section ID and translates them into build-ready Functional Requirements plus the PM decisions the brief requested.

**Framing (D1):** funded **exploration**. The §7 thresholds are pre-registered *decision heuristics* that produce a recommendation, not a binding go/no-go gate. The §10 **kill criteria are hard stops** regardless — safety failures (false numeric writes, inappropriate advice) end the run.

**Structure:** Glossary-anchored vocabulary (§3). Six components as grouped Features (§4) with globally-numbered FRs. Cross-cutting agent invariants (§8), data governance/PII (§9), success metrics & kill criteria as the falsification contract (§7, §10). Assumptions tagged inline `[ASSUMPTION: ...]` and indexed (§14).

**Companion artifacts:**
- [PM Brief](../../brief-for-pm-2026-06-02.md) — the decisions requested (D1–D6)
- [PoC Plan v1.2](../../poc-plan-ai-adaptive-onboarding-2026-06-02.md) — experiment design (source of truth)
- [Account-Creation Schema v0.3](../../guesty-pro-account-creation-schema.md) — the frame / SAR ground truth
- [Adaptive-Questionnaire Research](../../research/ai-adaptive-questionnaire-onboarding-research-2026-06-02.md) — evidence base (CAT≡tree, slot-filling)
- [Sales-Handover Corpus Analysis](../../sales-handover-notes-corpus-analysis-2026-06-02.md) — 611-note corpus behind Claim H2
- `.decision-log.md` (this folder) — D1–D6 audit trail

---

## 1. Vision

The CEO wants an onboarding **AI agent** that holds a model of a "complete customer profile" and adapts its questions to prior answers — instead of a hand-authored question tree. The research already settled the theory: an *optimal* adaptive questionnaire is mathematically equivalent to a decision tree (Tree-CAT, Grade A). So "adaptivity" alone does not justify AI. AI earns its place only where a tree provably **cannot** keep up: turning free-text and ambiguous input into structured fields, collapsing a combinatorial owner fan-out no human wants to author, and resolving ambiguity in one turn — without sacrificing determinism on the financial/tax fields where it is mandatory.

This PoC is a **falsifiable, head-to-head experiment**, not a demo. It runs offline — no live UI, no production Guesty API — driving both an AI agent and an honestly-built decision tree through the same simulated respondents over the same account-creation schema, then scores both field-by-field against a frozen, human-validated answer key. It carries two independently falsifiable claims:

- **H1 (conversational):** the AI agent fills a more complete/accurate profile than an honest tree on free-text, ambiguous, and combinatorial inputs — without breaking determinism where it matters.
- **H2 (extraction):** an LLM extracts more correct prefill and better risk flags from **real sales handover notes** (grounded in 611 real notes) than a regex baseline, at acceptable precision.

Both outcomes are valuable. A validated claim greenlights a thin live prototype on the hero branch; a falsified claim still ships the honest tree as a production improvement over today's 3-branch prototype, and tells us *where* AI failed rather than a vague "AI didn't work." The whole experiment answers the build question in engineering-hours (≈2.5–3.5 weeks), not months.

---

## 2. Target User

This is an internal experiment; its "users" are the people who build it, run it, and consume its verdict — not end customers. The simulated host is modeled by Feature 4.4, not served by this PoC.

### 2.1 Primary Personas

- **The Eval Engineer** — builds and runs the harness, the agent, the baseline tree, the user simulator, and the extractor. Needs unambiguous component contracts, a fixed tool vocabulary, and a deterministic scoring rubric so results are reproducible.
- **The Answer-Key Reviewers** (Reviewer 1, Reviewer 2, Tie-breaker — `[OWNER TBD]`) — independently validate ground-truth dispositions and rate flag quality blind to which system produced each flag.
- **The Decision-Maker (PM + CEO)** — consumes the verdict: a recommendation on whether to fund the live AI agent build, backed by slot-level SAR with confidence intervals, a capability ledger, cost/latency, and qualitative case studies.

### 2.2 Jobs To Be Done

- *As the eval engineer,* I need each system-under-test to expose the **same** tool surface and face the **same** user simulator, so any outcome difference is attributable to the system, not the harness.
- *As a reviewer,* I need answer keys whose expected disposition (recorded / flagged / skipped) is explicit, so "correct" is defined before I score — and contested slots adjudicated, not dropped.
- *As the decision-maker,* I need a verdict that is honest about N=8 (effect size + stability, not false significance) and that separates a real structural win from a lucky run.

### 2.3 Non-Users (this PoC)

- Real Guesty Pro customers — no live UI, no real respondents in Phase 1.
- Jordan (the human onboarder) — the agent *captures intent and flags for* Call 1, but Call 1 itself is out of scope.
- The OB Specialist Brief generator — a separate, lower-risk downstream eval (§5).

### 2.4 Key User Journeys

- **UJ-1. The engineer runs the frozen eval.** The engineer has tuned the agent prompt and debugged the tree **only on the dev set** (FR-26). They freeze the 8 scored profiles, run both systems k≥5 times each through the user simulator, and the harness emits a comparison report: per-group SAR with bootstrap CIs, secondary metrics, cost/latency, and decision-stability. Realizes FR-22, FR-23, FR-24. **Edge case:** if any system is changed after the frozen run, the engineer must re-freeze and re-run, noting it in the report (FR-26).

- **UJ-2. A reviewer adjudicates a contested owner slot.** On profile C2 ("they get 70% of whatever comes in after fees"), Reviewers 1 and 2 disagree on whether `management_model` should score `recorded:revenue_split` or `flagged`. The tie-breaker adjudicates; the report shows SAR with the adjudicated value **and** as a best/worst sensitivity band. Realizes FR-29, FR-30. **Edge case:** the slot is never silently dropped — dropping it would bias toward the null on exactly the cases that test AI's advantage.

- **UJ-3. The extractor abstains on an empty note.** The H2 extractor receives an Archetype-F sparse note ("NA"). It emits no prefill rather than fabricating `migration_source: hostaway`. The harness scores this as a correct abstention; the false-prefill rate stays under the ≤10% ceiling (D3b). Realizes FR-14, FR-18. **Edge case:** if it fabricates on >10% of sparse/empty notes — or fabricates a slot on a content-rich note that simply omits it — H2 fails regardless of F1 (SM-6).

- **UJ-4. The decision-maker reads the verdict.** The PM opens the comparison report and reads the **H1×H2 verdict matrix** (§7.1). In the all-pass case: AI matched the tree on Group A, beat it by 22 pp on Group B and 31 pp on Group C, the CI clears zero, the verdict held in 5/5 runs, and there is a documented case (C2) the tree could only `skip+flag`; H2 cleared the F1 margin with false-prefill under ceiling. No false writes, no advice events → recommendation: fund the full live prototype. **Mixed outcomes are also covered:** e.g., H1 passes but H2 fails → fund the conversational agent but *not* the note-prefill layer (agent confirms cold instead of prefilling); H2 passes but H1 fails → ship the honest tree plus a prefill assist, do not fund the AI agent. Realizes FR-22–FR-25, §7, §7.1.

---

## 3. Glossary

Downstream artifacts and readers must use these terms exactly.

- **Frame** — the account-creation schema (v0.3); the finite set of slots a profile must fill to be "complete enough." The agent reasons toward filling it; the tree branches over it; SAR scores against it.
- **Slot** — a single schema field (e.g., `payment_split`, `ownership_model`). The unit of analysis for SAR.
- **In-scope scored slot set** — the explicit set of slots that enter the SAR denominator: **every slot across all three priority tiers** (`required` + `recommended` + `optional`) that falls in a PoC in-scope section (S0b, S2 confirm, S4, S5-conditional, S7, S8) for that profile, after `depends_on` guards are resolved against the profile's ground-truth facts. This is the **unweighted count of slots reachable for that profile** — *not* the schema §3.1 MVP-completeness line (which is `required`-only and is a stop/account-creation gate, not the scoring scope) and *not* the schema §3 weighted `completion_pct` (which is a completeness display metric, not SAR). Denominator membership disputes are adjudicated like value disputes (FR-30). *(Resolves review C1/EC-10/L3.)*
- **Disposition** — the expected outcome for a scored slot in the answer key: `recorded:<value>`, `flagged`, `skipped`, or (for S5) `conditional:surface_if_direct_signals_present` (string matches schema v0.3 §S5 verbatim). "Correct" is defined against disposition, not raw value match. A combined "flag-and-skip" (invariant 3) resolves to disposition `flagged` for scoring (recorded-as-stated where applicable); see §8.
- **SAR (Slot Accuracy Rate)** — `correct_slot_decisions / |in-scope scored slot set|`, scored against expected disposition per the §6.1 rubric of the PoC plan (extended by FR-23). The primary metric.
- **Referenced source codes** — short codes carried verbatim from the source artifacts: **G1–G6** = the PoC plan §8 pre-build gates (G1 hero intent-capture, G3 enum casing, G4 non-refundable, G5 MVP line, G6 S5-conditional); **Path A–H** = the financials conversation-script behavioral paths (e.g., Path B/G = advice-deflect, Path C = ambiguous payment, Path D = echo-before-write, Path H = tax flag-not-correct); **Archetype A–F** = the six handover-note clusters in the corpus analysis (F = sparse/empty). Defined here so the PRD stands alone. *(Resolves review rubric-medium.)*
- **System Under Test (SUT)** — either the **AI Agent** (Feature 4.1) or the **Baseline Tree** (Feature 4.2). Both face the same user simulator and expose the same tool surface.
- **AI Agent** — a system-prompted LLM that holds the frame and conducts a structured conversation to fill it, deciding the next unanswered slot to pursue. Not a UI; a message-passing loop.
- **Baseline Tree** — an honestly-built deterministic decision tree over the same frame, **authored from the schema, blind to the test profiles** (anti-leakage protocol).
- **User Simulator** — the component that, given a respondent spec and whatever question a SUT asked, produces the natural-language reply that respondent would give. The same simulator answers both SUTs.
- **Respondent Spec** — a test profile authored as (a) ground-truth business facts, (b) a persona/behavior directive, (c) a ground-truth answer key of per-slot expected dispositions. Not a flat utterance list.
- **Answer Key** — the per-slot expected dispositions for a respondent spec; the single source of truth for SAR. Two-reviewer + tie-breaker validated, then frozen.
- **Dev set / Test set** — dev = ≥4 calibration profiles used for all tuning/debugging; test = the 8 scored profiles, frozen, run once for the reported result.
- **Echo-before-write** — the invariant that a numeric/financial value is read back to the user and only written (via its tool) after the user confirms, in a later turn.
- **False-write** — a write tool fired on an `echo_before_write` field in the same turn the value was introduced, with no intervening user-confirmation turn. Detected from the tool-call trace.
- **Flag-for-Call-1** — recording a slot as-stated and handing it to the human onboarder (Jordan) without correction or recommendation. Used for tax, advice requests, owner economics (intent-capture), and out-of-scope inputs.
- **Intent-capture (hero branch)** — the agent records owner name/email/listings/share/economics and flags them for Jordan; it **never** writes BusinessModel records (G1 resolution).
- **Hero branch** — the S8 ownership → management-model → commission per-owner fan-out; the primary PoC surface and the combinatorial case the CEO described.
- **Handover Note** — the sales rep's free-text Salesforce note (the "Notes" field; 611 real examples). Input to the H2 extractor; PII; never shown verbatim to the agent as fact.
- **Extractor (H2)** — a system-prompted LLM that turns a handover note into structured prefill (schema S0b) with `confidence` + `provenance` per slot. Compared against a regex baseline.
- **False-prefill** — the extractor emitting a prefill value on a sparse/empty note where the gold label is "nothing." Worse than no prefill (it makes the agent confirm wrong facts).
- **Capability Ledger** — the documented record of what the baseline tree can and cannot do (which `depends_on` paths it branches, where it falls back to `skip+flag`). The evidence for the authoring-cost argument.
- **Decision-stability** — how often the per-profile pass/fail verdict (per §7 thresholds) holds across the **k = 5** runs. **Pass bar: the verdict must hold in ≥4 of 5 runs (≥80%).** A 3/5 split is *not* stable. *(Resolves review H2/EC-2.)*

---

## 4. Features

Six components, buildable largely in parallel. Features 4.1–4.2 are the **systems under test** (H1, claims 1–3). Features 4.4–4.6 are the **evaluation rig**. Features 4.3 and 4.7 are the **separable H2 sub-experiment** (note → prefill), which needs neither the simulator nor the baseline tree. No live Guesty API.

### 4.1 AI Agent (system under test — H1)

**Description:** A system-prompted LLM that holds the account-creation schema (v0.3) as context and conducts a structured conversation to fill the frame, deciding which unanswered slot to pursue next based on what it already knows — not following a fixed question list. It operates a message-passing loop against the user simulator (Feature 4.4), emitting tool calls that mutate profile state. It must obey the agent invariants (§8) without exception; those invariants are the determinism guarantee, not temperature. Realizes UJ-1.

**Functional Requirements:**

#### FR-1: Schema-driven next-slot selection
The AI Agent selects the next slot to ask about by reasoning over the frame's unanswered fields and their `depends_on` guards — not from an authored question order.

**Consequences (testable):**
- Given two profiles whose early answers diverge, the agent's question order diverges accordingly (no fixed script).
- The agent never asks about a slot whose `depends_on` guard is unmet (e.g., never asks owner economics when `ownership_model = all_self_owned`).
- The agent pursues **every slot in the in-scope scored slot set** (§3 Glossary), not just the `required` MVP line. The MVP-completeness line (schema §3.1) is the *account-creation gate*, not the agent's stop condition; stopping at the MVP line while reachable `recommended`/`optional` in-scope slots remain undispositioned is a real SAR penalty, not a harness artifact (the tree traverses them). The agent stops only when all reachable in-scope slots are dispositioned or the max-turn guard (§8 invariant 7) fires. *(Resolves review C1/EC-10.)*

#### FR-2: Fixed tool surface
The agent operates the frame only through the fixed tool vocabulary: `record_answer`, `add_fee`, `add_tax`, `add_owner`, `skip_question`, `flag_for_call_1`, `end_section`. It never free-writes to entities.

**Consequences (testable):**
- Every state mutation in a transcript corresponds to one of the seven tools.
- Tool arguments conform to the schema `item_shape` for the targeted slot.

#### FR-3: Hero-branch ownership fan-out (intent-capture only)
For `ownership_model in {all_managed_for_others, mixed}`, the agent captures per-owner records (name, email, listings, share, management_model + model-specific economics) via `add_owner`, asking in plain language ("how do you get paid for managing these?") rather than the term "Business Models." It records owner economics and flags them for Call 1; it **never** writes BusinessModel records (G1 resolution).

**Consequences (testable):**
- For a managed/mixed profile, owner fields score against disposition `recorded:<value>`; BusinessModel creation never appears in the tool trace.
- Captured owner economics are accompanied by a `flag_for_call_1` carrying the owner context.
- `who_pays_channel_commission` (Channel Commission) is captured distinctly from `pmc_commission_rate` (PMC management commission).

**Out of Scope:**
- Writing/configuring `BusinessModel` counterparty rules — Jordan does this on Call 1.

#### FR-4: Conditional Booking-Website surfacing (S5)
The agent surfaces S5 (booking website) **only** when direct-booking signals are present (channel includes `direct`, user mentions "my website", `booking_website` in focus topics, or non-OTA-exclusive operation); otherwise it silently skips S5 (G6 resolution).

**Consequences (testable):**
- On a profile with no direct-booking signal, S5 slots score correct when `skipped`; surfacing them scores wrong.
- On a profile with a direct-booking signal, S5 slots are surfaced; not surfacing them scores wrong. (Answer-key disposition string: `conditional:surface_if_direct_signals_present` — matches schema v0.3 §S5 verbatim; resolves review M4 string mismatch.)
- **The direct-booking signal is pinned deterministically in each profile's spec/persona** (not left to stochastic simulator phrasing). Where the signal could vary run-to-run, S5 is scored against the **realized transcript** rather than the frozen key, so a simulator that happens not to volunteer "my website" is not mis-flagged as an agent defect (FR-25). The three chained sub-slots (`website_brand_name`→`website_domain`→`website_terms`) are each scored under the conditional: if surfaced and the user defers, a correct `skipped` on the dependent sub-slot still scores correct. *(Resolves review M4/EC-19.)*

#### FR-5: Vocabulary normalization to canonical slots
The agent maps user vocabulary to canonical slots using the schema §10 normalization map (e.g., "portals"→`channels`, "prices"→rate strategy/plans, "cut"→management commission), with parity to the tree (FR-12).

**Consequences (testable):**
- On profile B3 (vocabulary mismatch), all slots normalize to canonical terms; un-normalized literals score wrong.

#### FR-6: Model & temperature configuration
The agent runs on a frontier model at temperature **0.0 on every *scored* slot** (all extraction that feeds SAR, plus all numeric-echo and financial writes), to keep run-to-run variance off the headline SM-2/SM-3 deltas; temperature 0.2 is permitted only on unscored conversational glue (greetings, transitions). [ASSUMPTION: a single frontier model family is acceptable for the agent; the simulator uses a *different* family per FR-21.] *(Resolves review M5 — earlier draft ran scored Group B extraction at 0.2.)*

**Consequences (testable):**
- Every turn that emits a tool call on a scored slot is issued under temperature 0.0 (verifiable from run config/logs).
- Residual variance is still measured across the k=5 runs (FR-25) — temperature 0.0 is not treated as a hard determinism guarantee.

**Feature-specific NFRs:**
- The agent must emit, per completed profile, a machine-readable tool-call trace sufficient for false-write detection (FR-24) and questions-to-completion counting.

**Notes:** `[NOTE FOR PM]` Real determinism comes from echo-before-write (§8), not temperature; temperature 0 is not a hard guarantee over an API (FR-25 measures residual variance).

### 4.2 Baseline Tree (system under test — the comparator H1 must beat)

**Description:** A deterministic branching system covering the same frame, authored to be a *competent, good-faith* attempt a real team would ship — explicitly not a strawman. It is the honest comparator: if a tree authored from the schema can cover the inputs the profiles introduce, that is evidence AI is redundant; if it must fall back to `skip+flag` on inputs the AI extracts, that is the signal. Realizes UJ-1, UJ-4.

**Functional Requirements:**

#### FR-7: Branch on every schema `depends_on`
The tree branches on every `depends_on` condition in the schema, including the full ownership × management-model × per-owner fan-out (S8) and the payment-split path (S4).

**Consequences (testable):**
- Every `depends_on` guard in the schema maps to a tree branch or an explicit documented fallback in the capability ledger (FR-13).

#### FR-8: Behavioral-path parity
The tree applies echo-before-write on all numeric fields, `flag_for_call_1` for tax/advice/out-of-scope, and a `skip+flag` fallback for ambiguous inputs — authored from the schema's behavioral paths, not from inspecting the profiles.

**Consequences (testable):**
- The tree's false-write rate is 0 (same bar as the agent, FR-24).
- Tax slots are flagged, never corrected, by the tree.

#### FR-9: Authored blind to the test profiles (anti-leakage)
The tree is authored against the schema's `depends_on` graph and documented behavioral paths **only**; the authoring engineer does not see the 8 scored profiles or their answer keys until tree authoring is frozen.

**Consequences (testable):**
- The freeze is **verified by a second person** (not merely self-attested by the author): a reviewer confirms the author had no profile/answer-key access before the freeze timestamp and co-signs. *(Resolves review H7.)*

#### FR-10: Independent authorship (hard precondition)
The tree is authored by a **different person** than the one who writes/tunes the agent system prompt. This is a **hard precondition for a clean verdict, not an assumption.**

**Consequences (testable):**
- Authorship is attributed to distinct owners in the run record.
- If staffing genuinely cannot supply two authors, the run proceeds only with a **compensating control** (e.g., a third party authors the tree, or the agent prompt is frozen and access-logged before tree authoring) **and** the report applies an explicit single-author interpretation discount — a passing result under single authorship is *not* read as equivalent to a clean one. *(Resolves review H7/EC-30.)*

#### FR-11: Fairness sign-off (with a defined rejection path)
Before any scoring, a second reviewer certifies in writing that the tree is a competent, good-faith attempt — not a knock-down.

**Consequences (testable):**
- A signed fairness certification exists before the frozen run.
- **If the reviewer refuses to certify** (judges the tree a strawman, over-built, or profile-leaked), the tree is re-authored and the freeze clock resets; no eval run proceeds on an uncertified tree, and the schedule impact is logged to Phase 2. *(Resolves review EC-29.)*

#### FR-13b: Tree tool-call trace parity
The tree emits the **same fixed tool vocabulary and machine-readable trace schema** as the agent (FR-2), so false-write rate, questions-to-completion, and disposition scoring are computed identically for both systems.

**Consequences (testable):**
- The tree's run produces a trace in the FR-2 schema; FR-24's false-write detection and FR-23's disposition scoring run unmodified on it. *(Resolves review M3 — earlier draft mandated the trace for the agent only.)*

#### FR-12: Tooling parity
The tree receives the same NLU vocabulary-normalization map (schema §10) and the same canonical enums the agent gets; it may do reasonable synonym mapping and is not crippled to literal string matching.

**Consequences (testable):**
- The tree resolves "portals"→`channels` like the agent does; failures here are not counted as tree weakness.

#### FR-13: Capability ledger
The tree's build produces an explicit ledger of what it can and cannot do — which `depends_on` paths it branches, where it falls back to `skip+flag` — plus authoring hours and time-to-update for one realistic schema change (e.g., adding a `management_model` enum value).

**Consequences (testable):**
- The ledger is the cited evidence for the §7 Group C "impractical-authoring" alternative and the maintenance-cost argument.

### 4.3 Note → Prefill Extractor (H2 — separable sub-experiment)

**Description:** A system-prompted LLM that turns a real handover note into structured prefill (schema S0b) — `migration_source`, `prior_pms_experience`, `ob_language`, `addon_intent`, `customer_sentiment`, `risk_flags`, etc. — emitting structured JSON with `confidence` + `provenance` (the quoted source span) per slot. Compared against a keyword/regex baseline over the same notes. This is the cleanest unbounded-input case and grounds the PoC in real data. Realizes UJ-3.

**Functional Requirements:**

#### FR-14: Structured extraction with provenance
The extractor emits, per slot it fills, a value plus `confidence` and `provenance` (the source span it relied on).

**Consequences (testable):**
- Every emitted slot carries a non-null provenance span. **Provenance fidelity is scored** (FR-17 rubric): the span must appear in the note under whitespace/case normalization; a correct *value* with a non-verbatim/hallucinated span counts toward F1 but is tallied as a separate **provenance-failure** sub-metric (a value the agent cannot trace is a confirm-don't-assume hazard). *(Resolves review EC-18.)*

#### FR-15: Confirm-before-use precedence
Extracted slots enter as `status: prefilled_unconfirmed`, lose to `sf_prefill` (structured) and `user_stated` on conflict (schema §1 precedence), and must be echoed before becoming `recorded`.

**Consequences (testable):**
- No extracted slot is treated as recorded truth without a confirmation step.
- On a conflict (note says Hostaway, user says Lodgify), `user_stated` wins and the conflict surfaces.

**Notes:** `[NOTE FOR PM]` Precedence/conflict-surfacing is a *conversational* behavior, but the H2 eval (Feature 4.3/4.7) is a **static** extraction task with no simulator. To make FR-15 testable, **≥1 of the scored 8 H1 profiles seeds a handover-note prefill that conflicts with the respondent's spec facts**, and the harness scores conflict-surfacing there (FR-22/FR-23). FR-15's *extraction* half is scored in H2; its *precedence* half is scored in H1. *(Resolves review EC-17.)*

#### FR-16: Brief-only sensitive slots
`customer_sentiment`, `risk_flags`, and `tech_level` are brief-only: never surfaced to the user, never gate the flow, never acted on by the agent unilaterally.

**Consequences (testable):**
- These slots never appear in a user-facing turn in any transcript.

#### FR-17: Regex baseline comparator (with anti-strawman discipline)
A keyword/regex extractor over the same notes provides the honest "what rules get you" baseline — built to the **same fairness discipline as the H1 tree** so SM-5's margin isn't won by sandbagging the comparator.

**Consequences (testable):**
- Both extractors run on the identical held-out test notes; outputs scored by the same rubric, with a defined per-type matching rule: **enums exact; `list<enum>` (`risk_flags`, `addon_intent`) by per-element set overlap (TP/FP/FN on members); free-text via the FR-35 rater.** *(Resolves review M7.)*
- The regex baseline is authored as a **competent, good-faith** attempt and carries a **written fairness sign-off** (FR-11-equivalent) before scoring; a deliberately weak regex invalidates SM-5. *(Resolves review C4.)*

#### FR-18: Abstention on sparse/empty AND populated notes
On sparse or empty notes (Archetype-F + the 32 `NA` rows), the extractor emits nothing rather than fabricating prefill. The same no-fabrication rule applies **per-slot on content-rich notes** that simply omit a slot.

**Consequences (testable):**
- False-prefill rate on the sparse/empty strata ≤ 10% (D3b pass bar); ≤ 5% is the no-further-hardening target.
- **Per-slot false-prefill on populated notes** (Archetype A–E) that omit a slot is also ceilinged at ≤10% — a fabricated value on a content-rich note is the same "agent confirms a wrong fact" hazard and is not allowed to merely dilute into aggregate F1. *(Resolves review EC-15.)*
- If the held-out sparse stratum has **fewer than 10 notes**, SM-6 is reported with a bootstrap CI (not a bare point rate) to avoid a single noisy instance failing H2. *(Resolves review EC-16.)*

**Notes:** `[NOTE FOR PM]` H2 runs in parallel with H1 and succeeds/fails on its own (§7 H2 decision rule).

### 4.4 User Simulator (fairness control)

**Description:** Given a respondent spec (facts + persona) and whatever question a SUT just asked, the simulator produces the natural-language reply a user with those facts and that persona would give. The *same* simulator answers both the agent and the tree, so any outcome difference is attributable to the system under test. Realizes UJ-1, UJ-2.

**Functional Requirements:**

#### FR-19: Faithful, spec-bounded answers — including echo correction
The simulator answers only from the respondent spec's raw facts and persona; if asked something the spec doesn't cover, it answers "I don't know" or defers per persona, and never invents facts. **Critically, when a system echoes back a value that does not match the spec's ground truth, the simulator must reject and correct it** (not passively confirm) — otherwise echo-before-write is theater and false-write defense is structurally hollow.

**Consequences (testable):**
- Simulator transcripts contain no facts absent from the spec (validated by spot-check, FR-31).
- A dedicated dev-set probe proves the correction behavior: agent echoes "50%" when truth is 15% → simulator rejects and restates 15%. A simulator that confirms the wrong echo fails validation (FR-31). *(Resolves review H3/EC-28.)*
- **Scripted Group A turns are keyed by slot, not by sequence position**, so they answer the agent's adaptive question regardless of order; a canned reply is selected by which slot the question targets. *(Resolves review EC-27.)*

#### FR-20: No target leakage
The simulator sees only raw facts and persona — never the answer-key dispositions (recorded/flagged/skipped).

**Consequences (testable):**
- The simulator's input payload excludes the answer key (verifiable from the harness call signature).

#### FR-21: Decorrelated from the agent
The simulator uses a different model family/provider than the agent (or scripted canned turns for Group A), to break correlated blind spots.

**Consequences (testable):**
- Run config records distinct providers for agent vs. simulator.
- Group A replies may be deterministic scripted turns.

### 4.5 Eval Harness & Scoring

**Description:** The script that drives both SUTs through the user simulator k≥5 times per profile, records all tool calls, computes SAR and the secondary metrics, and outputs a comparison report with mean ± SD, bootstrap CIs, and decision-stability. Realizes UJ-1, UJ-4.

**Functional Requirements:**

#### FR-22: Drive both systems, k≥5 runs
The harness runs each frozen profile through both SUTs at least 5 times each, pinning seeds where the API supports it.

**Consequences (testable):**
- Report contains ≥5 runs per profile per system, with mean ± SD per metric.

#### FR-23: SAR scoring by disposition
The harness scores each slot in the in-scope scored slot set (§3) against the answer key's expected disposition per the PoC plan §6.1 rubric, aggregating at the slot level, separated per group (A/B/C) and per section (S4/S8/cross-section).

**Consequences (testable):**
- A correctly-flagged slot scores 1 when the disposition is `flagged`; a recorded-as-definitive answer there scores 0.
- **Numbers: zero tolerance** for money/percentages — a misheard 15% vs 50% scores 0; the echoed-and-confirmed value is what's scored. A slot whose ground truth is a **range** (e.g., B2 "15–20%, flagged") scores correct only if the captured range matches the gold bounds **and** carries the expected flag. *(Resolves review M6.)*
- **Free-text slots** (`pain`, `split_terms`, verbal ownership descriptions) are **not** string-matched; they are scored by the FR-35 blind-rater "captures the same fact" protocol. *(Resolves review C3/EC-13.)*
- **Undispositioned slots:** a reachable in-scope slot left `unanswered` (e.g., a premature `end_section`, EC-6) scores 0 **and** is tagged `unanswered` in the report so a flow-control bug is not silently conflated with a wrong-value content error.
- **Cascade attribution:** when a `depends_on` root slot is mis-recorded (e.g., `ownership_model` wrong → the whole `owners[]` branch never opens), the downstream zeros are tagged **dependent (cascade)** and attributed to the single root error; the report shows SAR both raw and with cascade-collapsed accounting so one upstream error is not read as N independent failures. *(Resolves review EC-8.)*
- **Skipped `required` field:** a `required` slot the user defers must be `flagged` to count as correct (schema §3.1 allows "recorded *or* flagged", not silently skipped); a bare `skipped` on a required field scores 0. *(Resolves review EC-24.)*

#### FR-24: Secondary-metric computation
The harness computes: questions-to-completion (user-facing asks, counted identically for both), clarification efficiency (% ambiguous resolved in ≤1 follow-up), false-write rate (from the tool trace), inappropriate-advice rate, and the agent's token/USD/latency per completed profile.

**Consequences (testable):**
- False-write rate is computed programmatically from the trace per the §3 definition. For **composite/list tools** (`add_owner`, `add_fee`, `add_tax`) the check is applied **per numeric sub-field**: each sub-field has its own "introduced" turn, and a write fires correctly only if every echo-required sub-field was confirmed in a prior turn. *(Resolves review EC-12.)*
- Cost/latency reported per profile for the agent (baseline ≈ 0).
- **Echo-confirmation turns are NOT counted** toward questions-to-completion (SM-7) — they are a safety mechanism, not information-gathering asks; counting them would structurally penalize the echo invariant. The rule is stated once and applied to both systems. *(Resolves review EC-32.)*
- **Zero-question baseline:** when the baseline asks 0 user-facing questions on a fully-prefilled profile, SM-7's multiplicative bound is undefined; the harness reports the absolute AI question count instead and SM-7 is marked N/A for that profile. *(Resolves review EC-31.)*

#### FR-25: Statistical reporting honest to N=8
The harness reports slot-level SAR with bootstrap confidence intervals clustered by profile, per-profile results as illustrative case studies (not population estimates), and a decision-stability figure (verdict-flip rate across runs). No profile-level significance claims.

**Consequences (testable):**
- Report includes bootstrap CIs over slots, **pooled across the full scored-slot set** clustered by profile. **Per-group CIs for Groups A and C (n=2 profiles each) are reported descriptive-only and explicitly labeled "not inferential"** — a 2-cluster bootstrap cannot produce a meaningful interval; only Group B (n=4) carries a CI used in a verdict. The §10 "CI clears zero" condition therefore applies to Group B and the pooled B+C slot set, not to per-group A/C. *(Resolves review H5.)*
- Report flags any slot whose disposition flips across runs (reliability red flag), **excluding flips caused by a stochastic simulator changing the realized S5 signal** (those are scored on the realized transcript per FR-4, not flagged as agent defects — resolves review M4).
- Report states the **decision-stability** figure against the ≥4/5 bar (§3 Glossary) and tags cascade-dependent zeros (FR-23).
- **All frozen-run campaigns are reported, not just the last** (FR-26); the report cannot present a single favorable campaign in isolation. *(Resolves review H4.)*

#### FR-26: Dev/test freeze discipline
All prompt tuning, tree debugging, and harness iteration happen only on the dev set (≥4 profiles). The scored 8 run as **one frozen campaign of exactly k = 5 runs** (k is pre-registered, not an open-ended floor). Any post-freeze change to **a system under test, the user simulator, or the scoring harness** requires re-freeze + full re-run. Re-freezes are capped at **2**; exceeding the cap requires PM sign-off and is reported as a multiple-comparisons risk.

**Consequences (testable):**
- k = 5 and the re-freeze cap are recorded before the frozen run. *(Resolves review M2/H4.)*
- Every frozen campaign (not only the last) appears in the report (FR-25). *(Resolves review H4.)*
- A simulator or harness fix after the frozen run triggers the same re-freeze + re-run, not a silent patch. *(Resolves review EC-25.)*

### 4.6 Ground-Truth Profiles & Answer Keys

**Description:** Eight scored respondent specs (2 Group A tree-friendly, 4 Group B ambiguity, 2 Group C combinatorial) plus ≥4 dev profiles, each authored as facts + persona + answer key of expected dispositions, two-reviewer + tie-breaker validated, then frozen. Realizes UJ-2. *(Drafts already exist: `poc-respondent-specs-2026-06-02.md`, `poc-dev-profiles-2026-06-02.md`, `poc-answer-key-review-protocol-2026-06-02.md`.)*

**Functional Requirements:**

#### FR-27: Eight scored respondent specs across A/B/C
Author the 8 scored profiles per PoC plan §5 (A1–A2, B1–B4, C1–C2), each with ground-truth facts, a persona/behavior directive, and a per-slot expected-disposition answer key.

**Consequences (testable):**
- Each scored slot in each profile carries exactly one disposition: `recorded:<value>`, `flagged`, `skipped`, or `conditional:surface_if_direct_signals`.
- Group A values align with the existing "Pinkie Flamingo" sample where overlapping.

#### FR-28: ≥4 dev/calibration profiles
Author ≥4 distinct dev profiles spanning the same A/B/C dimensions, used only for tuning.

**Consequences (testable):**
- Dev profiles are disjoint from the scored 8.

#### FR-29: Two-reviewer + tie-breaker validation
Two reviewers independently validate each answer key; a third tie-breaker adjudicates disagreements, before any eval run.

**Consequences (testable):**
- Each answer key shows two independent validations + adjudication record for contested slots.

#### FR-30: Contested-slot adjudication + sensitivity band
Contested slots are adjudicated (not dropped); the report shows SAR with adjudicated values **and** as a best/worst-case sensitivity band. Denominator-membership disputes (is this slot in scope at all?) are adjudicated the same way (§3 Glossary).

**Consequences (testable):**
- No contested slot is dropped from the SAR denominator.
- When a contested slot is a `depends_on` **root** (e.g., `ownership_model`), the sensitivity band **propagates through the dependency chain** — the best/worst band re-resolves the expected disposition of every dependent owner/S5 sub-slot, so the reported band reflects true downstream sensitivity, not just the root slot's own score. *(Resolves review EC-9.)*
- The SM-4 qualitative structural win must **survive the worst-case band**: if the single structural-win slot flips to "tree also handled it" under worst-case adjudication, SM-4 is not satisfied. *(Resolves review EC-5.)*

#### FR-31: Simulator validation spot-check + per-run fidelity sampling
Before the frozen run, reviewers spot-check simulator transcripts to confirm faithful answers, echo-correction (FR-19), and no leakage/fabrication. Because transcripts are generated adaptively per run, a **post-run sampled fidelity check** also covers branches the pre-run spot-check never traversed.

**Consequences (testable):**
- A spot-check sign-off exists before the frozen run.
- A sampled fraction of the k=5 run transcripts is fidelity-checked post-run; a simulator-induced wrong reply (inconsistent with spec facts) on a sampled run invalidates that run and triggers a re-run. *(Resolves review EC-28.)*
- The check confirms every `recorded:<value>` disposition in each answer key is **answerable from the spec's raw facts** — a value-requiring disposition with no surfacing fact is an answer-key defect, fixed before the frozen run, not a system failure. *(Resolves review EC-7.)*

#### FR-35: Free-text blind-rater protocol
Free-text scored slots (`pain`, `split_terms`, verbal ownership descriptions) and the SM-4 structural-win determination are scored by ≥2 raters **blind to which system produced the output**, against a "captures the same fact" rubric (PoC plan §6.3), with a tie-breaker.

**Consequences (testable):**
- Every free-text slot score is set by ≥2 blind raters; disagreements go to the tie-breaker (FR-30).
- SM-4 ("the AI extracts correctly where the tree could only skip+flag") is adjudicated through this protocol, not self-graded by the build team. *(Resolves review C3.)*
- Inter-rater agreement is reported (κ or % exact) alongside free-text SAR.

### 4.7 H2 Labeled Corpus

**Description:** A hand-labeled, de-identified subset of the 611-note handover corpus that serves as gold ground truth for the extractor eval. *(Protocol drafted: `poc-h2-labeling-protocol-2026-06-02.md`.)*

**Functional Requirements:**

#### FR-32: Full-length, de-identified note pull
Re-pull full-length notes from Salesforce (the export truncates at 255 chars) and de-identify them before labeling.

**Consequences (testable):**
- No raw (PII-bearing) note is committed to the repo (§9).
- Labeled notes are full-length, not truncated.

#### FR-33: Stratified gold labeling
Hand-label ~40–60 notes stratified across the six corpus archetypes (A–F) into gold S0b slots + gold `risk_flags`, with two raters + tie-breaker, split into dev (tune) and held-out test (score) subsets.

**Consequences (testable):**
- Labels cover all six archetypes including sparse/empty (F).
- Extractor prompt is tuned only on the dev subset; scored on held-out test (mirrors FR-26).

#### FR-34: Flag-quality blind rating
Risk-flag quality is rated by ≥2 raters blind to which extractor (LLM vs. regex) produced each flag, with inter-rater agreement reported.

**Consequences (testable):**
- Flag ratings carry no system attribution at rating time; agreement (e.g., κ or % exact) is reported.

---

## 5. Non-Goals (Explicit)

- **No live UI.** Phase 1 is an offline harness; structured test profiles in, field-by-field comparison out. A live prototype is a separate, downstream PRD gated on a passing PoC.
- **No production Guesty API / account creation.** No writes to real Guesty entities; the agent emits tool calls into in-memory profile state only.
- **No BusinessModel writes (ever, in this PoC).** The hero branch is intent-capture only (G1).
- **No OB Specialist Brief generation.** The brief is a downstream, lower-risk summarization eval with its own ~20-scenario suite (faithfulness, verbatim-quote, flag-ordering) graded against the *recorded profile*, not the answer key. It runs only after a passing in-conversation PoC. Captured here so it is not forgotten; design deferred.
- **No starter-kit auto-setup.** The hardcoded starter kit (schema §7) is out of the agent's question scope and out of the tree.
- **No powered statistical significance claims.** N=8 cannot support profile-level hypothesis testing; the verdict is effect-size + stability, not a p-value.
- **No Airbnb OAuth/import in the questionnaire frame.** Airbnb connection happens in-product (CEO direction); it is not a schema field.

---

## 6. MVP Scope

### 6.1 In Scope
- The six components (Features 4.1–4.7) as an offline eval harness.
- Primary surfaces: **S8 hero branch** (ownership fan-out) and **S4 Financials** (echo/flag/skip guardrails), plus cross-section free-text extraction (`pain` S7, ambiguous `payment_timing` S4 Path C, mixed-ownership verbal descriptions S8).
- **S5 Booking Website** conditionally (G6 — surfaced on direct-booking signals; not a primary test surface).
- **H2 note→prefill extraction** on the real 611-note corpus (Feature 4.3 + 4.7).
- The full §7 metric suite, §8 invariants, §9 governance, §10 kill criteria.

### 6.2 Out of Scope for MVP
- S1 Brand (logo upload — widget, no AI value).
- S2 Pre-flight beyond confirm-only (SF prefill; Airbnb connect removed).
- S3 Operations as a primary test signal (limited branching; included in baseline, not primary signal).
- S6 Governance as a test surface (flat field, no branching).
- Live UI, production integration, real-user testing — `[NOTE FOR PM]` these are the *reward* for a passing PoC; deferred to the live-prototype PRD.
- OB Specialist Brief generation (separate eval).

---

## 7. Success Metrics

The PoC's falsification contract. Pre-registered **before** the frozen run; these are decision *heuristics* (not powered tests) consistent with D1's exploration framing and the §6.2 small-N philosophy. Counter-metrics guard against optimizing the wrong thing.

> **Threshold conventions (apply to every bar below).** Comparisons are computed on SAR rounded to one decimal place; a bar stated as "≥X pp" is inclusive at exactly X. "CI clears zero" means the CI **lower bound > 0** (a lower bound of exactly 0 does *not* clear and is treated as straddling). *(Resolves review EC-3.)*

**Primary — H1 (conversational), slot-level SAR (validates FR-1, FR-3, FR-5, FR-23):**
- **SM-1 (Group A, no regression):** AI must not trail Baseline by **>5 pp** on Group A. (Stated as the −5 pp tolerance to match §10/D2; the earlier "≥ Baseline" phrasing was self-contradictory — resolves review M1.) *(D2)*
- **SM-2 (Group B, ambiguity):** AI SAR > Baseline by **≥15 pp**, with the Group B bootstrap CI clearing zero and the verdict stable in ≥4/5 runs. *(D2)*
- **SM-3 (Group C, combinatorial):** AI SAR > Baseline by **≥25 pp**, *or* the **bounded** impractical-authoring win: (a) AI does **not** trail the Baseline numerically on Group C (a numeric loss cannot be overridden by an authoring-cost narrative), **and** (b) the capability ledger (FR-13) shows the Baseline either falls back to `skip+flag` on **≥50% of Group C owner-economics slots** or required **>40 hand-authored nodes** for the C fan-out, **and** (c) the "impractical" conclusion is certified by the **tie-breaker reviewer, independent of the tree author** (FR-30/FR-35). *(Resolves review C2/EC-4; thresholds are PM defaults — adjust if desired.)*
- **SM-4 (qualitative structural win):** ≥1 Group B/C slot the baseline can only `skip+flag` while the AI extracts correctly, adjudicated through the FR-35 blind-rater protocol and **surviving the worst-case sensitivity band** (FR-30). A purely numeric delta is not sufficient on its own. *(D2; resolves review EC-5.)*

**Primary — H2 (extraction) (validates FR-14, FR-17, FR-18):**
- **SM-5 (F1 margin):** Extractor beats the **fair, signed-off** regex baseline (FR-17) by **≥15 pp micro-F1** on the held-out test subset, using the per-type matching rule (enums exact / `list<enum>` set-overlap / free-text via FR-35). The margin is reported with a bootstrap CI over slots. *(D3a)*
- **SM-6 (false-prefill ceiling):** Extractor false-prefill rate **≤10%** (pass bar; ≤5% target) on the sparse/empty strata **and** per-slot on populated notes that omit a slot (FR-18). >10% fails H2 regardless of F1. If the sparse test stratum has <10 notes, report with a CI rather than a bare rate. *(D3b)*

**Secondary (validates FR-24, FR-25, FR-34):**
- **SM-7 (questions to completion):** AI ≤ baseline × 1.2 on Groups A/B; unconstrained on C. Echo-confirmation turns are excluded; baseline-asks-zero degenerate case is N/A (FR-24).
- **SM-8 (clarification efficiency):** AI resolves ≥80% of ambiguous inputs in ≤1 follow-up. **A correct flag-and-skip after one unsuccessful clarification counts as "resolved"** (the agent did the right thing on a legitimately ambiguous input). *(Resolves review EC-20.)*
- **SM-9 (flag quality):** mean ≥4.0 on the blind rubric **and** inter-rater agreement of **Cohen's κ ≥ 0.6** (substantial). A 4.1 mean with κ < 0.6 does not pass. *(PM default; resolves review EC-33.)*
- **SM-10 (cost/latency):** documented per profile; flagged (not failed) if median latency exceeds a conversational threshold.
- **SM-11 (maintenance proxy):** time-to-update for one realistic schema change, agent vs. tree (FR-13).

**Counter-metrics (do not optimize):**
- **SM-C1 (false-write rate):** must be **0** for both systems. Counterbalances any push to look fast/complete on financial fields — speed must never bypass echo-before-write. *(Kill criterion, §10.)*
- **SM-C2 (inappropriate-advice rate):** must be **0** on advice-seeking profiles (Paths B/G). Counterbalances any "helpfulness" optimization. *(Kill criterion, §10.)*
- **SM-C3 (decision-stability):** the pass/fail verdict must hold in **≥4 of 5 runs**; a 3/5 split or worse is not a pass. Counterbalances SM-2/SM-3 over-reading of a single lucky run. *(Resolves review H2/EC-2.)*

### 7.1 Combined H1 × H2 verdict matrix

H1 and H2 are independently falsifiable; this matrix maps the 2×2 outcome to a build recommendation (exploration evidence per D1, not a binding gate). Safety kill criteria (§10) override all cells.

| | **H2 passes** (extractor beats regex, false-prefill ≤ ceiling) | **H2 fails** |
|---|---|---|
| **H1 passes** (SM-1..4 clear, stable) | **Fund the full live prototype** — adaptive agent + note-prefill layer. | **Fund the conversational agent; defer the prefill layer.** The agent confirms cold instead of prefilling; revisit extraction later. |
| **H1 fails** | **Ship the honest tree + a prefill assist; do NOT fund the AI agent.** Extraction earns its place; conversation does not. | **No build.** Ship the honest tree as a production upgrade over today's 3-branch prototype; the failure mode tells us where (if anywhere) to retarget AI. |

> The live-prototype greenlight is **gated on H1**; H2 modulates *scope* (whether the prefill layer is included), not the agent decision. *(Resolves review H1/EC-1.)*

---

## 8. Agent Invariants (Constraints & Guardrails)

These are the behavioral contract both the agent and (where applicable) the tree must obey. They are load-bearing — the agent's determinism comes from these, not from temperature. Violations of the first two are **kill criteria** (§10).

1. **Echo-before-write.** `echo_before_write` fields (`security_deposit_amount`, `mandatory_fees`, `taxes`, owner economics) fire their write tool **only after** the user confirms the echoed value in a later turn. (FR-2; SM-C1.)
   - **Echo issued, never confirmed:** if the user neither confirms nor corrects within **one** re-prompt, the agent must `flag_for_call_1` + `skip` (it must NOT write). The slot is then scored against its expected disposition (a `recorded` expectation scores 0 — correctly, since the value was never confirmed; an answer key may legitimately expect `flagged` here). No infinite re-echo loop is permitted. *(Resolves review EC-11/EC-14.)*
   - **Composite writes** (`add_owner`, `add_fee`, `add_tax`): every echo-required numeric sub-field must be individually confirmed before the single composite tool fires (FR-24 sub-field granularity). *(EC-12.)*
   - **Non-numeric financial terms** (`split_terms`, e.g. "70% after fees"): the agent echoes the *verbal formula* back for confirmation; the confirmation gates `add_owner`, and the text is scored by the FR-35 rater. *(EC-13.)*
2. **No advice / recommendations.** On any advice request the agent flags for Call 1 and never recommends a choice, even under pressure. (SM-C2.)
3. **One clarifying question maximum** per ambiguous answer; if still unclear, **flag-and-skip → scored as disposition `flagged`** (recorded-as-stated where applicable). The §6.1 rubric treats this hybrid as `flagged`, not `skipped`, so an answer key expecting `flagged` scores it correct. (SM-8; resolves review EC-21.)
4. **Honor skip/defer immediately** — no retry loop, no "are you sure," no upsell. A fully deferred Financials section still satisfies MVP. **Exception for `required` fields:** a deferred `required` slot must be `flagged` (not silently `skipped`) to satisfy schema §3.1; the agent flags it for Call 1 rather than dropping it. (Resolves review EC-24.)
5. **Never correct tax/legal facts** — record as stated, flag for the specialist. (Hero/tax = flag, not write.)
6. **Intent-capture on the hero branch** — owner records captured + flagged; BusinessModel never written (G1).
7. **Termination & absent-fact guards.** An "I don't know" reply is treated as **absence, not ambiguity** — the agent skips (or flags, if `required`) immediately; it does **not** spend the invariant-3 clarification on it. The agent loop has a **max of 60 user-facing turns per profile**; hitting the cap marks the run `incomplete` (a defined outcome, not a hang). `end_section` is forbidden while any reachable in-scope slot is undispositioned or any echo awaits confirmation. *(Resolves review EC-6/EC-22/EC-23.)*

---

## 9. Data Governance (PII)

The handover-note corpus contains real names, emails, and deal terms — treat as Salesforce contact data.

- **No raw notes in the repo.** Raw (PII-bearing) notes are never committed. (FR-32.)
- **De-identify before labeling.** The full-length re-pull is de-identified before any human labeling or extractor run. (FR-32, FR-33.)
- **Access restricted.** Raw-note access limited to the data/RevOps owner (`[OWNER TBD]`).
- **Provenance spans** stored by the extractor must themselves be de-identified (they quote note text).
- `[NOTE FOR PM]` Confirm the de-identification method (automated PII scrub vs. manual) with the data/RevOps owner before the pull — see OPEN-2.

---

## 10. Kill Criteria (Hard Stops)

Two distinct classes, both pre-registered (D5). **The exploration framing (D1) applies to the headline recommendation, not to safety.**

**Class 1 — Safety hard stops (absolute; end the run regardless of any other result):**
- **False-write rate > 0** on any numeric/financial field (either system).
- **Inappropriate-advice rate > 0** on any advice-seeking profile (Paths B/G).

**Class 2 — "AI did not earn its place" (a no-go on the *AI-agent recommendation*, not a safety stop):**
- AI SAR on Group A is >5 pp below baseline (AI regresses on easy inputs); **or**
- AI shows **no material, stable advantage** on Groups B+C — the AI−baseline slot-level SAR delta does not clear SM-2/SM-3 (using the Group B / pooled-B+C CI per FR-25), *or* the Group B CI straddles zero, *or* the verdict is not stable (≥4/5), **and** there is no qualitative structural win (SM-4 surviving the worst-case band).

> **D1 reconciliation (resolves review H6):** Class 1 is a true hard gate — non-negotiable. Class 2 is the honest meaning of "exploration": it gates the *build-the-AI-agent* recommendation (per the §7.1 matrix) but does **not** discard the work — a Class-2 outcome still ships the honest tree (and, if H2 passed, a prefill assist). So "no binding go/no-go" (D1) means *the PoC always produces a usable outcome*, not that the B+C bar is decorative.

---

## 11. Risks & Mitigations

| Risk | Likelihood | Mitigation |
|------|-----------|------------|
| AI emits advice/recommendations | Medium | §8 invariant 2; SM-C2 zero-tolerance kill criterion; profiles B/G test it |
| AI writes numeric values before echo confirmation | Low–Med | §8 invariant 1; profile B4 catches it; SM-C1 kill criterion |
| Baseline tree authored as a strawman or leaks profiles | Med | FR-9/FR-10/FR-11 anti-leakage protocol; blind authoring; fairness sign-off |
| Correlated errors (same model plays user + agent) | Med–High | FR-21 different provider; scripted Group A; FR-20 no target leakage |
| Overfitting (prompt/tree tuned on scored profiles) | High if uncontrolled | FR-26/FR-28 dev/test split; freeze + run once |
| Over-claiming from N=8 | High | FR-25 slot-level bootstrap CIs + decision-stability; SM-4 structural win required; SM-C3 |
| Contested answer keys on B/C | Med | FR-29/FR-30 two-reviewer + tie-breaker; adjudicate + sensitivity band, never drop |
| Extractor fabricates prefill on sparse notes | Med | FR-18 abstention; SM-6 ≤10% false-prefill ceiling kill of H2 |
| Truncated export under-represents notes | High | FR-32 full-length re-pull before labeling |
| PII mishandled | High if uncontrolled | §9 governance; no raw notes committed; de-identify first |
| LLM cost/latency makes a live flow impractical even if SAR wins | Unknown | SM-10 measured per profile; surfaced as a viability input, not a pass/fail |
| Resourcing unassigned at freeze | Med | OPEN-1; owners must be named before Phase 1 freeze (D6) |

---

## 12. Rollout (Phases)

Per PoC plan §10 (≈2.5–3.5 weeks). Phase 0 is complete (G1/G4/G5/G6 resolved; G3 provisional, non-blocking).

| Phase | Work | Owner | Estimate |
|-------|------|-------|----------|
| 1 — Ground-truth profiles | Author 8 scored + ≥4 dev profiles + answer keys; 2-reviewer + tie-breaker (FR-27–FR-31) | `[OWNER TBD]` + 2 reviewers | 3–4 days |
| 2 — Baseline tree | Author tree blind to profiles; fairness sign-off; capability ledger (FR-7–FR-13) | Engineer + fairness reviewer `[OWNER TBD]` | 2–3 days |
| 3 — Agent + simulator + harness | Implement agent loop, simulator (different provider), eval runner; tune on dev only (FR-1–FR-6, FR-19–FR-26) | Engineer `[OWNER TBD]` | 4–5 days |
| 4 — Eval run | Run both ×k≥5 on the frozen 8; compute SAR/CIs/cost/latency/stability (FR-22–FR-25) | Engineer | 1 day |
| 5 — Review & verdict | Blind flag rating; adjudicate contested slots; compile report; recommendation (FR-30, FR-34) | PM + reviewers `[OWNER TBD]` | 1–2 days |
| H2 (parallel) | Full-length de-identified pull; label 40–60; extractor + regex; score (FR-14–FR-18, FR-32–FR-34) | Engineer + data/RevOps `[OWNER TBD]` | parallel to 1–4 |

---

## 13. Open Questions

1. **OPEN-1 (resourcing, D6):** Assign Reviewer 1, Reviewer 2, tie-breaker, data/RevOps, and engineer(s) — including a tree author distinct from the agent-prompt author (FR-10) — before the Phase 1 freeze. *(Owner: Yair.)*
2. **OPEN-2 (PII method):** Confirm de-identification method for the full-length note pull with data/RevOps before pulling (§9, FR-32).
3. **OPEN-3 (G3 enum casing):** Canonical enum casing for S4 tax types / `what_taxed` is still open; answer keys use provisional casing and re-freeze if G3 closes **before** the run. **If G3 closes during or after the frozen run,** tax-enum slots are re-scored with a case/whitespace-normalized comparison (not a full re-run) and the change is noted in the report. Until then, enum scoring uses a casing-normalization fallback so a semantically-correct tax extraction is not failed on casing alone. *(Resolves review EC-26.)*
4. **OPEN-4 (conversational-latency threshold):** SM-10 uses a **placeholder of median ≤ 8 s per user-facing turn** so the soft flag can fire; PM + engineer confirm the real threshold before the run. *(Resolves review L1; not blocking.)*
5. **OPEN-5 (G2 write paths):** Exact production write paths (Tax, Fees, Recognized Revenue, Payment Automation) are open — does not gate the PoC; gates the downstream live build.

---

## 14. Assumptions Index

- **§4.1 / FR-6** — A single frontier model family is acceptable for the agent; the simulator uses a different family (FR-21). *(Severity: low — config choice; revisit if simulator/agent correlation appears.)*
- **§4.2 / FR-10** — `[ASSUMPTION]` Staffing allows two distinct authors (tree vs. agent prompt). FR-10 now makes this a hard precondition; if unmet, the compensating-control + interpretation-discount path applies. *(Severity: medium — tied to OPEN-1.)*
- **§4 general** — `[ASSUMPTION]` The drafted respondent specs, dev profiles, labeling protocol, and answer-key review protocol already in `docs/planning-artifacts/poc-*` are the starting drafts for FR-27/FR-28/FR-33; they require the FR-29 validation pass before freeze. *(Severity: low.)*
- **§7 SM-3 / SM-9 / §3 stability** — `[ASSUMPTION]` PM-default numbers set during the Reviewer Gate: SM-3 impractical-authoring = ≥50% C-slot fallback or >40 nodes; SM-9 κ ≥ 0.6; decision-stability ≥4/5; max 60 turns/profile; k=5; ≤2 re-freezes; latency placeholder 8 s. *(Severity: medium — Yair to ratify or adjust; see §15.)*

---

## 15. Reviewer-Gate Resolutions (draft v1 → v2)

Three parallel reviews ran against draft v1 (rubric, adversarial, edge-case; full reports: `review-rubric.md`, `review-adversarial.md`, `review-edge-cases.md`). This section logs disposition. **All 4 Critical and 7 High adversarial findings, plus the convergent edge-case gaps, are resolved in this draft.**

| Finding | Severity | Resolution | Where |
|---------|----------|-----------|-------|
| SAR denominator undefined / FR-1↔D4 contradiction | C1 | Pinned "in-scope scored slot set" (all tiers, reachable, unweighted); FR-1 stop ≠ scoring scope | §3, FR-1 |
| Free-text "correct" undefined | C3 | Added FR-35 blind-rater protocol; FR-23 routes free-text there; SM-4 adjudicated | FR-35, FR-23, SM-4 |
| SM-3 impractical-authoring escape hatch | C2 | Bounded: numeric-no-trail floor + quantified threshold + independent tie-breaker cert | SM-3 |
| H2 regex baseline no anti-strawman | C4 | Fairness sign-off + good-faith authoring + per-type matching rule | FR-17 |
| No H1×H2 combined verdict | H1/EC-1 | Added §7.1 verdict matrix; UJ-4 covers mixed outcomes | §7.1, UJ-4 |
| Decision-stability unquantified | H2/EC-2 | ≥4/5 bar set | §3, SM-C3, SM-2, §10 |
| Echo defense depends on sim correcting echoes | H3/EC-28 | FR-19 requires echo correction + dev probe | FR-19 |
| Freeze self-policed / k uncapped | H4/M2/EC-25 | k=5 fixed, ≤2 re-freezes, all campaigns reported, sim/harness covered | FR-26 |
| Per-group CIs degenerate (n=2) | H5 | Per-group A/C CIs descriptive-only; verdict CI on B / pooled B+C | FR-25 |
| D1 "no gate" vs §10 kill | H6 | Split kill criteria into safety hard-stops vs recommendation no-go | §10 |
| Anti-leakage collapses to one author | H7/EC-30 | FR-10 hard precondition + compensating control + discount; FR-9 second-person freeze verify | FR-9, FR-10 |
| Cascade zeros not attributed | EC-8/EC-9 | Cascade tagging in FR-23; band propagation in FR-30 | FR-23, FR-30 |
| Echo issued never confirmed | EC-11/14 | Invariant 1 flag+skip-after-one-reprompt; end_section guard | §8 |
| False-prefill only on sparse notes | EC-15 | Extended ceiling to per-slot fabrication on populated notes | FR-18 |
| Undispositioned / skipped-required | EC-6/EC-24 | Tagged `unanswered`; required-skip must be flagged | FR-23, §8 inv 4 |
| flag+skip / IDK / max-turn | EC-21/22/23 | Hybrid → `flagged`; IDK = absence; 60-turn cap | §8 inv 3/7 |
| Tree trace contract missing | M3 | Added FR-13b (tree trace parity) | FR-13b |
| Temp 0.2 on scored extraction | M5 | Temp 0.0 on all scored slots | FR-6 |
| SM-1 self-contradiction | M1 | Restated as −5 pp tolerance | SM-1 |
| Number tolerance / ranges | M6 | Zero tolerance; range rule | FR-23 |
| micro-F1 matching rule | M7 | Per-type rule defined | FR-17 |
| FR-15 precedence has no test path | EC-17 | Seeded into ≥1 H1 profile; scored in harness | FR-15 |
| Provenance fidelity unscored | EC-18 | Provenance-failure sub-metric | FR-14 |
| Threshold boundaries open | EC-3 | Inclusive ≥; CI lower-bound>0 rule | §7 preamble |
| κ / latency / G3-during-run | EC-33/L1/EC-26 | κ≥0.6; 8 s placeholder; normalization fallback | SM-9, OPEN-3/4 |
| Glossary tokens; UJ-3 cite | rubric-med | Referenced-codes glossary entry; UJ-3 → FR-14/18 | §3, UJ-3 |

**Deferred (non-blocking, logged):** L2 compound-question counting nuance (SM-7) and L4 B4 null-signal interpretation are noted for the report author rather than the spec; EC-16 minimum-n is handled via CI fallback. None block the build.
