---
title: "PoC Plan — AI-Driven Adaptive Onboarding Questionnaire"
author: "Mary (Business Analyst)"
date: 2026-06-02
version: 1.2
status: draft — adversarially reviewed; + handover-note corpus; ready for PM + architect review
decision_required_by: "—"
related:
  - docs/planning-artifacts/guesty-pro-account-creation-schema.md (v0.3)
  - docs/planning-artifacts/sales-handover-notes-corpus-analysis-2026-06-02.md
  - docs/planning-artifacts/research/ai-adaptive-questionnaire-onboarding-research-2026-06-02.md
  - OB V2 prototype (ob-v2-pearl.vercel.app)
  - conversation_script_financials.md
  - ob_specialist_brief.md
---

# PoC Plan — AI-Driven Adaptive Onboarding Questionnaire

---

## 1. The claim we are testing

> **An AI-driven adaptive flow collects a more complete and accurate customer profile than
> a hand-authored decision tree, specifically on inputs a tree cannot handle — free-text,
> ambiguous, and combinatorially-branching answers — without sacrificing reliability on
> the structured fields where determinism is required.**

This is a **falsifiable, head-to-head claim**, not a vibe. The PoC either validates it (with numbers) or kills it cleanly. Both outcomes are valuable.

### Why this framing matters
The research established that adaptive-testing science *proves* an optimal adaptive questionnaire is mathematically equivalent to a decision tree (Tree-CAT equivalence, Grade A). "Adaptivity" alone does not justify AI. The specific, testable advantages AI can demonstrate are:

1. Extracting structured slot values from free-text / ambiguous input a tree can't anticipate
2. Collapsing a combinatorial branch space the CEO doesn't want to hand-author
3. One-shot ambiguity resolution that matches the "one clarifying question" contract
4. Post-collection brief synthesis

This PoC tests claims 1–3 against an honestly-built baseline. Claim 4 (the brief) is lower-risk and a separate, constrained eval.

### Claim H2 — note → prefill extraction (added 2026-06-02)

> **Given a real sales→onboarding handover note, an LLM extractor fills more correct prefill
> slots — and flags more legitimate risks — than a rules/regex baseline, at acceptable
> precision.**

This is advantage #1 (free-text → structured slots) applied to a **new and entirely real
surface**: the 611 handover notes in the `Notes for Tamar` Salesforce export (see
`sales-handover-notes-corpus-analysis-2026-06-02.md`). It matters for three reasons:

1. **It is the cleanest unbounded-input case.** A tree/regex cannot turn *"both owner and manager,
   starting with 6 of 18 listings, still fuzzy on payments"* into `ownership_model: mixed` +
   `payment: flag_for_call_1`. This is precisely what the research says a tree *provably cannot* do.
2. **It grounds the whole PoC in real data.** Until now the experiment was synthetic-only. The
   corpus lets us anchor respondent profiles to real archetypes and score extraction on real notes.
3. **It directly serves the CEO's "prefill the starter kit" ask** — extracted slots let the agent
   *confirm* instead of *ask*, lowering "questions to completion" (a §6 secondary metric).

H2 is evaluated by **Component 6** (§7) and is independently falsifiable from claims 1–3.

---

## 2. What the CEO asked for (translated into testable scope)

| CEO direction | PoC translation |
|---------------|----------------|
| "Prepare the agent with an understanding of what a complete customer profile looks like, then let it determine which questions to ask" | Agent reasons toward the account-creation schema (v0.2); does not follow an authored question list |
| "10 listings → who owns them → some managed → owner details → commission or other → keep going" | Hero scenario: the S8 ownership branch — the primary test surface |
| "Each question adapts based on answers that came before" | AI-generated next question vs. tree-branched next question, on identical profiles |
| "Airbnb connection happens inside the product" | Airbnb OAuth/import removed from the questionnaire frame entirely |
| "Widgets inside Guesty afterward" | Post-questionnaire auto-setup (starter kit) — **out of PoC scope**; already defined in hardcoded starter-kit |

---

## 3. Scope

### In scope
- **S8 hero branch** (ownership → management model → commission detail) — the primary PoC surface. Richest, most combinatorial, completely absent from the current prototype.
- **S4 Financials branch** — the existing conversation scripts make this the best-documented section; also covers the most important "AI can't handle this" guardrail (tax/numeric echo-before-write).
- **Cross-section free-text extraction** — `pain` (S7), ambiguous `payment_timing` (S4 Path C), and mixed-ownership verbal descriptions (S8).
- **Sales handover-note → prefill extraction (S0b)** — Claim H2; evaluated on the real 611-note corpus via Component 6.

### Out of scope for this PoC
- S1 Brand (logo upload — widget, no AI value)
- S2 Pre-flight — channels and listing count (SF prefill, confirm-only; Airbnb connect removed)
- S3 Operations (cleaning system — limited branching; included in baseline but not primary test signal)
- S5 Booking Website — **now in scope conditionally** (G6 resolved: AI surfaces it on direct-booking signals); not a primary test surface
- S6 Governance (simple flat field; no branching)
- Post-questionnaire auto-setup / starter kit
- OB Specialist Brief generation (separate eval, lower risk)
- Full Guesty integration / production account creation

### Tech boundary
The PoC runs as an **offline evaluation harness** — not a live UI, not wired to a Guesty production API. Inputs are structured test profiles; outputs are compared field-by-field against a ground-truth answer key. This is the fastest, cheapest way to generate a credible signal. A live-UI prototype comes only if the offline eval validates the claim.

---

## 4. The baseline (what AI must beat)

The baseline is an **honestly-built decision tree** over the same schema — not the current prototype (which has only 3 `showIf` branches). An honest baseline:

- Branches on every `depends_on` condition in the schema
- Handles the full ownership × management-model × per-owner fan-out in S8
- Applies echo-before-write for all numeric fields
- Applies flag-for-call-1 for tax, advice, and out-of-scope inputs
- Gracefully routes ambiguous inputs to a `skip + flag` fallback (as the scripts specify)

If a tree authored against the **schema** (not against the test profiles — see §4.1) can still cover the inputs the profiles introduce, that is evidence the AI is redundant. If the tree requires impractical combinatorial authoring, or falls back to `skip + flag` on inputs the AI extracts correctly — that is the signal.

### 4.1 Baseline fairness / anti-strawman protocol

A rigged baseline invalidates the whole PoC. Two failure modes must be controlled:

1. **Strawman risk** — a deliberately weak tree makes the AI look good.
2. **Data-leakage / overfitting risk** — a tree authored *against the 8 known profiles* trivially "passes" them, which both inflates the tree on Group A and understates its real-world capability on B/C.

Controls (all mandatory before any eval run):

- **Author from the schema, blind to the test profiles.** The tree is built to cover the schema's `depends_on` graph and the documented behavioral paths (echo, flag, skip) — **not** reverse-engineered from the 8 answer keys. The engineer authoring the tree does **not** see the profiles or answer keys until authoring is frozen.
- **Tooling parity.** The tree gets the *same* NLU vocabulary-normalization map the agent gets (schema §10) and the *same* canonical enums. The baseline is allowed reasonable synonym mapping (e.g., "portals" → `channels`); it is not crippled to literal string matching.
- **Independent authorship.** The tree is authored by a different person than the one who writes/tunes the agent system prompt, so neither artifact is optimized to make the other look bad.
- **Fairness sign-off.** Before scoring, a second reviewer certifies in writing that the tree is a *competent, good-faith* attempt a real team would ship — not a knock-down.
- **Capability ledger.** Document explicitly what the tree **can** and **cannot** do (which `depends_on` paths it branches, where it falls back to `skip + flag`). This ledger — not a post-hoc narrative — is the evidence for the authoring-cost argument.

> **Interpretation caveat.** Because the tree is authored from the schema and not from the profiles, expect it to handle Group A cleanly and to fall back on genuinely unbounded inputs. The "AI must match the tree on Group A" bar is therefore a check that AI does not *regress* on easy structured fields — not a strong claim, by design.

---

## 5. Test profiles

Eight synthetic respondent profiles, designed to stress-test the specific dimensions where AI vs. tree diverges. Grouped by expected difficulty.

### Group A — Tree-friendly (baseline should handle cleanly)
AI must match or beat the tree here; failure is a red flag.

| # | Profile name | Listing count | Ownership | Payment | Notable characteristic |
|---|-------------|---------------|-----------|---------|----------------------|
| A1 | Clear-cut self-owner | 5 | All self-owned | At booking, full | All structured answers; no free text |
| A2 | Simple managed | 8 | All managed (2 owners, flat fee) | Split 50/50 | Clean CSV-style owner data |

### Group B — Ambiguity tests (AI's primary advantage)
The tree falls back to `skip + flag`; AI should extract the correct slot value.

| # | Profile name | Ambiguous input | Expected correct extraction |
|---|-------------|----------------|----------------------------|
| B1 | Channel-dependent payer | "Depends — Airbnb collects, I take 50% for direct" | `payment_timing=at_booking`, `payment_split=50_50`, note re: OTA |
| B2 | Vague commission | "I take a cut — usually around 15–20% depending on the property" | `management_model=commission`, `pmc_commission_rate` flagged as range + flag_for_call_1 |
| B3 | User vocabulary mismatch | Uses "prices," "portals," "payout," "cleaning fee" throughout | All slots correctly normalized to canonical terms (research §10) |
| B4 | Skip + stress | Defers entire financials section; pushes back on 3 questions | All skips honored; no retry loops; 3 flags with vibe notes |

### Group C — Combinatorial fan-out tests (CEO's stated value)
The hero branch at scale. The tree either requires exhaustive pre-authoring or falls to fallback.

| # | Profile name | Listing count | Ownership | Commission complexity |
|---|-------------|---------------|-----------|----------------------|
| C1 | Mixed portfolio, diverse models | 12 | 4 owners: 2×commission, 1×fixed fee, 1×revenue split | All 4 models in one session |
| C2 | Large managed, verbal description | 20 | "Some are mine, some belong to a family I work with — they get 70% of whatever comes in after fees" | No enum match; must extract `revenue_split` + `split_terms` + echo-back |

### Profile construction rules
- Each profile is authored as a **respondent spec**, not a flat utterance list: (a) the **ground-truth facts** about the business, (b) a **persona/behavior directive** (e.g., "defers all financials," "pushes back on 3 questions," "uses Airbnb vocabulary"), and (c) a **ground-truth answer key** giving, for every in-scope slot, the *expected disposition* — `recorded:<value>`, `flagged`, or `skipped` (see scoring rubric §6.1). Splitting facts from disposition is what lets the same spec drive both systems and lets a slot the agent *correctly flags* score as correct.
- The natural-language messiness is produced at run time by the **user simulator** (§7, Component 3) from the respondent spec — not pre-baked, so the simulator can answer whatever question either system actually asks.
- Profiles A1–A2 ground-truth values align exactly with the existing "Pinkie Flamingo" sample answers where overlapping.

> **Gate dependency — updated 2026-06-02.** G1 resolved (intent-capture): hero-branch dispositions = `recorded + flag_for_call_1`. G5 resolved: SAR denominator = analyst's priority tiers. G6 resolved: S5 included conditionally. G3 still open: S4 enum casing is provisional — answer keys marked accordingly and frozen on first run; re-freeze if G3 closes before the eval run. Phase 1 is unblocked and starts immediately.

### 5.1 Dev/test split & anti-overfit
Tuning the agent prompt — or debugging the tree — against the same 8 profiles you score on is overfitting, and inflates both systems. Therefore:

- Author **≥4 additional dev/calibration profiles**, distinct from the scored 8, spanning the same A/B/C dimensions.
- **All** prompt tuning, tree debugging, and harness iteration happen **only** on the dev set.
- The scored 8 are **frozen** and run **once** for the reported result (a held-out test set). Any change to a system after the frozen run requires re-freezing and a re-run noted in the report.

---

## 6. Success metrics

These are the PoC's **falsification conditions** — the numbers that either validate or kill the claim.

### Primary metric: Slot Accuracy Rate (SAR)
```
SAR = correct_slot_decisions / total_scored_slots_in_profile
```
A slot decision is scored against the answer key's **expected disposition**, not just a value match (see rubric §6.1). Evaluated separately per group (A/B/C) and per section (S4/S8/cross-section free-text), and aggregated at the **slot level** (not the profile level) for interpretation — see §6.2.

**Decision thresholds to validate the claim** (pre-registered before the frozen run; these are decision heuristics, not powered statistical tests — see §6.2):
- AI SAR ≥ Baseline SAR on Group A (AI must not regress on easy, structured cases)
- AI SAR > Baseline SAR by ≥ 15 percentage points on Group B (ambiguity)
- AI SAR > Baseline SAR by ≥ 25 percentage points on Group C (combinatorial) — or demonstrate baseline requires hand-authoring an impractical number of branches (per the §4.1 capability ledger)
- **AND** at least one *qualitative* win the tree structurally cannot achieve (a Group B/C slot the baseline can only `skip + flag` while the AI extracts correctly). A purely numeric delta on an overfit-prone small sample is not sufficient on its own.

### 6.1 Scoring rubric for SAR (including skip/flag handling)

SAR is undefined unless we say what "correct" means when a field is legitimately skipped or flagged (the scripts *require* this — e.g., taxes are always flagged, a deferred Financials section is valid per schema §3.1). Each scored slot in the answer key carries an **expected disposition**:

| Answer-key disposition | Agent action that scores **correct (1)** | Scores **wrong (0)** |
|------------------------|------------------------------------------|----------------------|
| `recorded:<value>` | Slot recorded with value matching ground truth (within tolerance below) | Missing, skipped, flagged, or wrong value |
| `flagged` (e.g. taxes, advice, conditional fees) | Slot flagged `for_call_1`, recorded-as-stated where applicable, no correction/advice | Recorded as a definitive answer, or silently dropped |
| `skipped` (user deferred) | Slot marked `skipped`, honored immediately, no retry | Re-asked, recorded anyway, or upsold |

**Value-match tolerance:**
- Enums: exact match on canonical casing (depends on G3).
- Numbers: exact for money/percentages (a misheard 15% vs 50% is a failure — research §7); the echoed value is what's scored.
- Free-text (`pain`, `split_terms`): scored by the human raters of §6.3 against a "captures the same fact" rubric, not string equality.

**Contested slots.** Slots where reviewers cannot agree on the ground-truth disposition (mostly Group B/C ambiguity) are **adjudicated by a third tie-breaker reviewer**, not dropped. Dropping them would silently remove exactly the cases that test AI's advantage and bias the result toward the null. The report shows SAR both *with adjudicated values* and as a *sensitivity band* (best/worst-case for the contested slots).

### 6.2 Statistical interpretation with small N

**Eight profiles (2/4/2 across A/B/C) cannot support profile-level hypothesis testing.** Any "statistically significant" claim at the profile level is false precision. Therefore:

- **Unit of analysis is the slot, not the profile.** Each group contributes dozens of scored slot decisions; report SAR with **bootstrap confidence intervals over slots**, clustered by profile to avoid over-counting correlated slots within one profile.
- **Per-profile results are reported as illustrative case studies**, not population estimates. The narrative ("on C2 the tree fell back on 4 of 6 owner-economics slots; the AI extracted 5/6") is the deliverable, alongside the aggregate.
- The 15pp / 25pp thresholds are **pre-registered decision rules**, not powered tests. No formal power analysis is claimed; if a sponsor needs inferential confidence, that requires a larger, separately-scoped profile set (out of this PoC).
- Because results are non-deterministic (§7, Component 4), report **mean ± SD across k≥5 runs** per profile and a **decision-stability** figure (how often the pass/fail verdict flips across runs).

### Secondary metrics
| Metric | How measured | Target |
|--------|-------------|--------|
| **Questions to completion** (efficiency) | Count of **user-facing questions posed** (distinct asks requiring a user reply), counted identically for AI and tree. Raw "turns"/messages are *not* comparable across interaction models, so we count questions, not turns. | AI ≤ baseline × 1.2 on Groups A/B; unconstrained on C |
| **Clarification efficiency** | % of ambiguous inputs resolved in ≤1 follow-up (Path C contract) | AI ≥ 80% |
| **False-write rate** | A write tool (`record_answer`/`add_fee`/`add_tax`) fired on an `echo_before_write` field **in the same turn the value was first introduced, with no intervening user-confirmation turn**. Detected programmatically from the tool-call trace. | Must be 0 for both AI and baseline |
| **Inappropriate advice rate** | % of advice-seeking turns where agent gave a recommendation | Must be 0 (Paths B/G) |
| **Flag quality** | ≥2 raters per §6.3 rubric, blind to which system produced the flag | Mean ≥ 4.0 **and** acceptable inter-rater agreement |
| **LLM cost / latency** | Tokens, USD cost, and wall-clock latency per completed profile for the AI agent (baseline ≈ 0). Reported, not pass/fail — a production-viability input. | Documented; flagged if median latency > a conversational threshold |
| **Authoring & maintenance cost** | (a) Hours to author the tree from the schema (§4.1); (b) **time-to-update**: hours to extend the tree vs. the agent for one realistic schema change (e.g., add a `management_model` enum value). (b) is the truer maintenance proxy — authoring once for 8 profiles is not. | Document both; (b) is the core "maintenance" argument |

### 6.3 Flag-quality rating protocol
Single-rater 1–5 scoring is subjective and gameable. Instead:
- **≥2 independent raters**, **blind** to whether a flag came from the AI or the tree.
- Score each flag on a short rubric: (1) correct topic/section, (2) includes the user's verbatim quote where required, (3) actionable — Jordan could act on it without re-interviewing, (4) no fabricated facts.
- Report **inter-rater agreement** (e.g., Cohen's κ or % exact agreement); the ≥4.0 mean target only counts if agreement is acceptable. Disagreements adjudicated as in §6.1.

### Kill criteria
The PoC is **killed or redesigned** if any of these are true:
- AI SAR on Group A is more than 5 points below the baseline (AI introduces errors on easy inputs)
- False-write rate > 0 on any numeric/financial field
- Inappropriate advice rate > 0 on any advice-seeking profile (Paths B/G)
- AI shows **no material, stable advantage** on Groups B+C — i.e., the AI−baseline slot-level SAR delta does not clear the §6.1 thresholds, *or* its bootstrap CI (§6.2) straddles zero, *or* the verdict is not stable across the k runs, *and* there is no qualitative win the tree structurally cannot achieve. (Phrased as effect-size + stability, not a profile-level significance test, which N=8 cannot support.)

---

## 7. Minimum viable implementation

Six components, buildable largely in parallel. Components 1–2 are the *systems under test* (conversational claims 1–3); components 3–5 are the *evaluation rig*; **Component 6 is a separable sub-experiment for Claim H2** (note → prefill extraction) that needs neither the simulator nor the baseline tree. No live Guesty API required.

### Component 1 — The agent (AI adaptive flow)

**What it is:** A system-prompted LLM that holds the account-creation schema as its context and conducts a structured conversation to fill it. Not a UI — a message-passing loop.

**Minimal system prompt structure:**
```
ROLE: You are a Guesty Pro onboarding assistant. Your job is to fill the
account-creation profile below through conversation. You do not follow a
fixed question list — you decide which unanswered field to ask about next
based on what you already know.

PROFILE TARGET: [schema JSON, fields with status=unanswered]

INVARIANTS (never break these):
1. Echo every number back before recording it. Do not fire record_answer
   on a numeric field until the user confirms.
2. When the user asks for advice or a recommendation, say
   "Good question for [specialist name] — I'll flag it for Call 1."
   Do not recommend a choice under any circumstances.
3. One clarifying question maximum per ambiguous answer. If still unclear,
   flag and skip.
4. When the user skips or defers, accept immediately. No retry.
5. Never correct the user on tax or legal facts. Record what they said,
   flag for the specialist.

TOOLS: record_answer, add_fee, add_tax, add_owner, skip_question,
       flag_for_call_1, end_section

CURRENT PROFILE STATE: [runtime field values]
```

**Model choice:** Start with a frontier model at temperature 0.2 for structured extraction, temperature 0.0 on any numeric-echo or financial write. (Determinism on the fields that require it, as the research specifies. Note temp 0 is *not* a hard determinism guarantee over an API — see Component 4.)

**Implementation:** A Python/Node script that runs a message loop: get next agent question + tool calls → pass the question to the **user simulator** (Component 3) → feed its reply back → apply tool calls to profile state → repeat. No UI.

### Component 2 — The baseline (honest decision tree)

**What it is:** A deterministic branching script that covers the same schema, **authored from the schema and blind to the 8 test profiles** (the anti-leakage / anti-strawman protocol in §4.1).

**Scope of authoring (to be measured):**
- Every `depends_on` condition → a branch
- S4 echo-before-write → explicit confirm step
- S8 ownership × management-model fan-out → explicit nodes for each path
- Ambiguous inputs the schema implies → `skip + flag` fallback nodes (authored from the schema's behavioral paths, not from inspecting the profiles)

Authoring effort is a data point, but **authoring a tree once for a fixed scenario set is a weak proxy for real maintenance cost.** The stronger measure is **time-to-update** for a realistic schema change (§6 secondary metrics) — that is what the CEO's "I don't want to author every question" complaint is actually about.

**Implementation:** A finite-state machine or simple decision-table JSON that the eval harness drives via the **same** user simulator (Component 3) the AI faces.

### Component 3 — User simulator (and fairness controls)

**Why it's needed:** The AI asks *adaptive* questions; a flat, pre-written list of user utterances cannot answer a question the author didn't anticipate, and the AI and tree will ask different questions in different orders. Without a simulator, the comparison is not apples-to-apples and free-text follow-ups have no responder.

**What it is:** A component that, given a profile's **respondent spec** (facts + persona directive from §5) and whatever question a system just asked, produces the natural-language reply a user with those facts and that persona would give.

**Fairness & integrity controls:**
- **Same simulator for both systems.** The identical user simulator answers the AI agent and the baseline tree, so any difference in outcome is attributable to the system under test, not to different user behavior.
- **Decorrelate from the agent.** Use a **different model family/provider** for the simulator than for the agent. LLM-as-user + LLM-as-agent from the same model share blind spots (e.g., both normalize "portals"→channels the same wrong way), producing correlated errors that flatter the AI. A different provider (or a rules-based simulator for Group A) breaks that correlation.
- **No target leakage.** The simulator sees only the **raw facts and persona**, never the answer-key dispositions (recorded/flagged/skipped). It must not invent facts beyond the spec; if asked something the spec doesn't cover, it answers "I don't know" or defers, per persona.
- **Group A can be fully scripted.** For the all-structured profiles, user replies can be deterministic canned turns (no LLM needed), eliminating simulator variance on the cases where it matters least.
- **Simulator validation.** Before the frozen run, reviewers spot-check simulator transcripts to confirm it answers faithfully and doesn't leak or fabricate — a bad simulator silently corrupts both arms.

### Component 4 — Determinism & repeated runs

LLM outputs vary run-to-run even at temperature 0. To keep the result honest:
- Run each profile **k ≥ 5 times** through both systems (pin seeds where the API supports it).
- Report **mean ± SD** of SAR and the **decision-stability** rate (how often the pass/fail verdict per §6 flips across runs).
- Track **slot-disposition flips** — any slot whose recorded/flagged/skipped outcome changes across runs is itself a reliability red flag, independent of correctness.
- Real determinism guarantees come from the **echo-before-write gate**, not from temperature; this component measures residual variance so we don't over-trust a single lucky run.

### Component 5 — Eval harness

**What it is:** A script that:
1. Drives both systems through the **user simulator** (Component 3), k times each per profile
2. Records all tool calls emitted by both
3. Computes SAR (per the §6.1 rubric), questions-to-completion, false-write rate, advice rate per profile, plus cost/latency for the agent
4. Outputs a comparison report with mean ± SD and bootstrap CIs (§6.2)

**Ground-truth answer keys** are the single source of truth for SAR scoring. **Two reviewers independently validate each answer key, with a third tie-breaker for disagreements (§6.1), before any eval runs.**

### Component 6 — Note → prefill extraction eval (Claim H2)

**What it is:** A self-contained sub-experiment that scores how well an LLM extractor turns a
real handover note into structured prefill (schema S0b), versus a rules/regex baseline.

**Inputs:** The 611-note corpus (`Notes for Tamar`). Re-pull **full-length** notes from
Salesforce (the export truncates at 255 chars) and **de-identify** before labeling (§ governance).

**Labeled set:**
- Hand-label a **stratified sample of ~40–60 notes** spanning the six archetypes (A–F) in the
  corpus analysis doc, into gold S0b slots (`migration_source`, `ob_language`, `addon_intent`,
  `ownership_model` hint, `prior_pms_experience`, …) + gold `risk_flags`.
- **Dev/test split:** tune the extractor prompt on a dev subset; freeze and score on a held-out
  test subset (no leakage; mirrors §5.1).
- **Two-rater labeling** with a tie-breaker (reuse the §6.3 raters).

**Systems under test:**
- **Extractor:** system-prompted LLM emitting structured JSON with `confidence` + `provenance`
  (the quoted source span) per slot.
- **Baseline:** a keyword/regex extractor over the same notes (the honest "what rules get you").

**Metrics:**
- **Slot precision / recall / F1** per field and micro-averaged.
- **Risk-flag quality** — blind multi-rater rating (precision of flags raised; recall vs. gold).
- **Abstention behavior** — on sparse/empty notes (Archetype F, plus the 32 `NA` rows), does the
  extractor correctly emit nothing rather than hallucinate? (False-prefill rate.)
- **Confidence calibration** — are high-confidence slots actually more correct? (Reliability curve.)

**Decision rule (pre-registered):** H2 is supported if the extractor beats the regex baseline on
micro-F1 by a clear margin **and** keeps false-prefill rate low on sparse/empty notes (a noisy
extractor that fabricates prefill is worse than no prefill, because it makes the agent confirm
wrong things). Exact margin to be set with the PM, consistent with the §6.2 small-N philosophy.

**Why it's separable:** Component 6 does not need the user simulator or the baseline tree — it is a
static extraction task on real text. It can run in parallel with the conversational eval and fails
or succeeds on its own.

---

## 8. Pre-build gates (unresolved SME questions)

Most of these do not block PoC planning or the harness *build*, and all must be resolved before any production build. **But three of them gate the eval itself** because SAR scoring depends on them — see the sequencing note below. Assign an owner to each.

| # | Question | Status | Resolution |
|---|----------|--------|-----------|
| G1 | Does the agent **create** BusinessModel records during onboarding, or **capture intent** for Jordan to configure? | ✅ **Resolved 2026-06-02** | **Intent-capture only.** Agent records owner name/email/listings/share/economics conversationally; Jordan configures BusinessModel on Call 1. Expected disposition for owner-economics slots = `recorded:<value>` + `flag_for_call_1`. Write scope = zero for hero branch. See schema §S8. |
| G2 | Exact write paths for Tax Configuration, Additional Fees, Recognized Revenue, Payment Automation | ⚠️ Open | Needed before any production API calls. Does not gate PoC SAR scoring. |
| G3 | Canonical enum casing for tax types and `what_taxed` line items | ⚠️ Open | Needed for exact SAR scoring on S4 profiles — use provisional enums in answer keys; re-freeze if resolved before eval run. |
| G4 | Is non-refundable a global toggle or per-listing / per-rate-plan? | ✅ **Resolved 2026-06-02** | Per-listing / per-rate-plan (maps to `RatePlan.cancellationPolicy`). Schema already reflects this. |
| G5 | MVP-completeness line ratification — which fields truly block account creation | ✅ **Resolved 2026-06-02** | Use analyst's judgment (schema `required`/`recommended`/`optional` tiers) as the MVP line for the PoC. Onboarding team to ratify before production. |
| G6 | Is Booking Website (S5) in the questionnaire, or fully in-product? | ✅ **Resolved 2026-06-02** | **AI-judgment conditional.** S5 is in scope; agent surfaces it only when direct-booking signals are present in the conversation. Expected disposition in answer keys = `conditional: surface_if_direct_signals`. See schema §S5. |

**Phase 0 is complete.** G1, G5, and G6 are resolved. G4 was resolved in the same session. G2 and G3 remain open but do not block profile authoring — proceed with Phase 1 immediately using provisional enum values for G3; re-freeze answer keys if G3 closes before the eval run.

**Eval-gating sequencing — updated.** G1 resolved: hero-branch dispositions are now `recorded:<value>` + `flag_for_call_1` (not `write`). G5 resolved: SAR denominator uses analyst's priority tiers. G3 still open: answer keys for S4 use provisional enum casing, flagged for potential re-freeze.

---

## 9. What a passing PoC unlocks

If the eval validates the claim (§6 metrics pass, kill criteria clean):

1. **Go signal** for a thin live prototype wiring the AI agent into the existing OB V2 shell — replacing the static question screens in S8 and S4 with the adaptive conversational surface
2. **Brief generator build** — the post-hoc low-temperature LLM call that synthesizes the recorded profile into the OB Specialist Brief (separate, lower-risk, already specced in `ob_specialist_brief.md`)
3. **PM handoff** — the PoC results become the primary evidence input for the PRD (John's territory), quantifying the value claim that drives roadmap prioritisation

> **Brief eval is out of scope for *this* PoC's scoring** and must not be conflated with SAR. The brief is a downstream summarization task with its own ~20-scenario eval suite (research §4.4; `ob_specialist_brief.md`) measuring faithfulness (no invented facts), verbatim-quote correctness, and flag-ordering — graded against the *recorded profile*, not the ground-truth answer key. It runs only after a passing in-conversation PoC, on the profiles this PoC produces. Pointer captured here so it is not forgotten; design is deferred.

If the eval does **not** validate:
- The baseline tree is already built and can be shipped as a production improvement over the current 3-branch prototype — not wasted work
- The specific failure mode tells us *where* to target AI, rather than a general "AI didn't work" finding

---

## 10. Timeline estimate (eval-harness PoC only)

| Phase | Work | Owner | Estimate |
|-------|------|-------|----------|
| 0 — Pre-build gates | ~~Resolve **G1, G3, G5**~~ **✅ COMPLETE (2026-06-02)** — G1/G4/G5/G6 resolved; G3 provisional (does not block). | Product SME + Mary | Complete |
| 1 — Ground-truth profiles | Author 8 scored + ≥4 dev profiles (§5.1) + answer keys w/ expected dispositions; 2-reviewer + tie-breaker validation | Mary + 2 domain reviewers | 3–4 days |
| 2 — Baseline tree | Author decision tree **from the schema, blind to profiles** (§4.1); fairness sign-off; record authoring time | Engineer + fairness reviewer | 2–3 days |
| 3 — AI agent + user simulator | Implement agent loop, **user simulator (different provider)**, eval runner; tune prompt **on dev set only** | Engineer | 4–5 days |
| 4 — Eval run | Run both ×k≥5 on the frozen 8; compute SAR/CIs/cost/latency/stability | Engineer | 1 day |
| 5 — Review | Blind flag-quality rating (≥2 raters); adjudicate contested slots; compile report; greenlight decision | Mary + PM + raters | 1–2 days |
| **Total** | | | **≈ 2.5–3.5 weeks** |

This is a **tight, bounded experiment** — no UI, no production integration, no user testing in phase 1. It answers the core question with engineering-hours, not months. The added rigor (user simulator, dev/test split, repeated runs, blind rating) is what makes the resulting numbers *defensible* rather than suggestive.

---

## 11. Risks

| Risk | Likelihood | Mitigation |
|------|-----------|------------|
| AI emits advice / recommendations (invariant failure) | Medium | System prompt hardening; kill criterion enforces zero tolerance |
| AI writes numeric values before echo confirmation | Low–Medium | Explicit prompt invariant + test case B4 catches this |
| Baseline tree authoring takes longer than estimated, biasing the authoring-cost argument | Medium | Track authoring hours honestly; document scope precisely; report time-to-update as the truer maintenance proxy (§6) |
| Ground-truth answer keys have inter-rater disagreement on ambiguous profiles (B/C) | Medium | Two-reviewer + **third tie-breaker** validation (§6.1); contested slots **adjudicated and reported as a sensitivity band, not dropped** (dropping them would bias toward the null) |
| LLM generates plausible but wrong slot values (hallucination) | Low on structured fields; Medium on free-text extraction | Echo-before-write catches financials; SAR catches the rest; temperature 0 on numeric writes |
| **Correlated errors — same model plays user and agent** | Medium–High | User simulator uses a **different provider/family** (or scripted turns for Group A); simulator sees only raw facts, never answer-key dispositions (§7 Component 3) |
| **Overfitting — prompt/tree tuned on the scored profiles** | High if uncontrolled | **Dev/test split (§5.1)**: tune only on dev profiles; freeze and run the scored 8 once; baseline authored blind to profiles (§4.1) |
| **Over-claiming from N=8** — a numeric delta read as proof | High | Slot-level aggregation + bootstrap CIs + decision-stability across k runs; require a qualitative structural win; no profile-level significance claims (§6.2) |
| **LLM cost/latency makes a live flow impractical** even if SAR wins | Unknown | Measure tokens/$/latency per profile (§6); surface as a viability input to the PM handoff |
| G1 answered "agent creates BusinessModel records" → higher blast radius | ✅ Resolved | G1 = intent-capture only; hero branch is pure conversational capture. Production write is a Phase 2 decision. |
| **PII in the handover-note corpus** (real names, emails, deal terms) | High if mishandled | Do **not** commit raw notes; de-identify before labeling; restrict access; treat as Salesforce contact data (Component 6 governance) |
| **Note extractor fabricates prefill** on sparse/empty notes → agent confirms wrong facts | Medium | False-prefill rate is a pre-registered H2 metric; abstention on Archetype-F/`NA` notes is required; extracted slots are confirm-don't-assume (schema S0b precedence) |
| **Truncated export (255 chars)** under-represents note content | High (in this file) | Re-pull full-length notes from Salesforce before labeling/extraction; current frequencies are explicit lower bounds |

---

## 12. Companion documents

| Document | Role |
|----------|------|
| `guesty-pro-account-creation-schema.md` v0.3 | The frame the agent reasons toward; the ground truth for SAR scoring; S0b adds the note-extraction prefill layer |
| `sales-handover-notes-corpus-analysis-2026-06-02.md` | The 611-note corpus analysis: signal taxonomy, archetypes, extraction design — the basis for Claim H2 / Component 6 |
| `research/ai-adaptive-questionnaire-onboarding-research-2026-06-02.md` | Evidence base; source of the CAT/slot-filling theory and completion-rate data |
| `conversation_script_financials.md` | Behavioral contract for S4 (echo, advice-deflect, skip) — informs system prompt invariants |
| `ob_specialist_brief.md` | Downstream deliverable; brief generator is a separate, lower-risk build |
| `Inputs from Salesforce.md` | Prefill contract for S0; seeded into every test profile |
| OB V2 prototype (`wizard.jsx`, `screens.jsx`) | Deterministic baseline reference; existing `showIf` branches are a floor, not a ceiling |

---

## 13. Changelog

- **v1.2 (2026-06-02) — sales handover-note corpus integration.** Added **Claim H2** (note → prefill extraction) to §1 as an independently falsifiable, real-data claim; added **Component 6** (§7) — a separable extraction sub-experiment scored on the 611-note `Notes for Tamar` corpus (slot P/R/F1, risk-flag quality, false-prefill/abstention, confidence calibration) against a regex baseline, with dev/test split and 2-rater labeling; brought **S0b** and **S5 (G6-conditional)** into scope; added **PII, false-prefill, and truncation risks** (§11); pointed companions at schema v0.3 + the new corpus analysis doc. (Conversational claims 1–3 and the §4.1/§5.1/§6 rigor are unchanged.)
- **v1.1 (2026-06-02) — adversarial review pass.** Hardened the experimental design against the failure modes that would make the result indefensible:
  - **§4.1 Baseline fairness / anti-strawman protocol** — tree now authored *from the schema, blind to the profiles* (kills data leakage), with tooling parity, independent authorship, a fairness sign-off, and a capability ledger.
  - **§5 / §5.1** — profiles reframed as *respondent specs* (facts + persona + expected disposition); added a **dev/test split** so prompt/tree tuning never touches the frozen scored 8; made profile authoring explicitly depend on gates G1/G3/G5.
  - **§6.1 SAR scoring rubric** — defines "correct" for `recorded`/`flagged`/`skipped` dispositions and value tolerances; contested slots are **adjudicated (third reviewer) and reported as a sensitivity band, not dropped**.
  - **§6.2 Statistical interpretation with small N** — shifts the unit of analysis to slots with bootstrap CIs, reframes 15pp/25pp as pre-registered decision rules (not powered tests), and requires a qualitative structural win.
  - **§6.3 Flag-quality protocol** — ≥2 blind raters + inter-rater agreement, replacing single subjective scoring.
  - **§6 secondary metrics + kill criteria** — comparable "questions to completion" unit, operational false-write detection, **LLM cost/latency**, and **time-to-update** as the real maintenance proxy; kill criterion restated as effect-size + stability instead of an impossible profile-level significance test.
  - **§7 Components 3–5** — added a **user simulator** (different provider, no target leakage, scripted Group A) to enable a fair adaptive comparison, plus a **determinism / repeated-runs** component (k≥5, mean±SD, stability).
  - **§8 / §10** — eval-gating sequencing (G1/G3/G5 close in Phase 0) and timeline updated for the added rigor.
  - **§9** — explicit **brief-eval pointer** (separate suite; not conflated with SAR).
  - **§11** — added risks for correlated user/agent errors, overfitting, over-claiming from N=8, and cost/latency.
- **v1.0 (2026-06-02)** — Initial PoC plan: falsifiable head-to-head claim, scope, honest-tree baseline, 8 profiles, SAR + secondary metrics, MVP implementation, gates, timeline, risks.
