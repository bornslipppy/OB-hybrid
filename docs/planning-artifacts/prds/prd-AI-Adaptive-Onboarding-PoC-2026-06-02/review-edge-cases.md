---
title: "Edge-Case Hunter Review — AI Adaptive Onboarding PoC PRD"
---

# Edge-Case Hunter Review — AI Adaptive Onboarding PoC PRD

**Target:** `prd-AI-Adaptive-Onboarding-PoC-2026-06-02/prd.md`
**Method:** Exhaustive path enumeration over FRs, §7 metrics, §8 invariants, §10 kill criteria, against the PoC plan (v1.2) and schema (v0.3). Reports **only unhandled** branching paths, boundary conditions, and state transitions. Not a quality assessment.
**Date:** 2026-06-02

Each finding: **path/condition** → **why unhandled** → **where in the PRD to address**.

---

## A. Verdict logic — outcome combinations with no rule

### EC-1. H1 and H2 disagree (pass/fail cross-product) — no combined verdict
- **Path/condition:** H1 passes (SM-1..4 clear) but H2 fails (SM-5/SM-6 fail), or the reverse. The PRD repeatedly states H1 and H2 are "independently falsifiable" (§1, FR-18 Notes, §7).
- **Why unhandled:** No verdict rule maps the 2×2 outcome matrix to a recommendation. UJ-4 only narrates the all-pass case. If H1 passes but extraction is no better than regex, is the live prototype funded *without* prefill? If H2 passes but the conversational agent fails H1, is anything shipped? The decision-maker (persona §2.1) has no stated decision for three of four quadrants.
- **Where to address:** §7 (add a verdict matrix) and §10; UJ-4 should cover the mixed outcomes.

### EC-2. Decision-stability (SM-C3) has no quantitative pass threshold
- **Path/condition:** Across k≥5 runs the per-profile pass/fail verdict flips — e.g., 3/5 pass, 2/5 fail right at the SM-2 15pp line.
- **Why unhandled:** SM-C3 and the §10 kill criterion say the verdict "must hold"/"is not stable" but never define "stable" numerically. FR-25 reports the verdict-flip rate but sets no acceptance bar (unanimous? ≥80%? majority?). At a threshold boundary, run noise decides the verdict with no rule.
- **Where to address:** SM-C3 and FR-25 — define the stability bar (e.g., verdict must hold in ≥k−1 runs).

### EC-3. Threshold boundaries are not closed (SM-1/2/3 and CI)
- **Path/condition:** Delta lands exactly on a bar: AI trails Group A by exactly 5.00 pp (SM-1 / §10 "must not trail by >5pp" vs kill ">5pp below"); Group B delta exactly 15.0 pp; Group C exactly 25.0 pp; bootstrap CI lower bound exactly 0 ("clears zero" vs §10 "straddles zero").
- **Why unhandled:** Inclusive/exclusive handling, rounding precision, and the pre-/post-rounding computation point are unspecified. A CI lower bound of exactly 0 neither clearly "clears" nor "straddles."
- **Where to address:** §7 (state ≥/> and rounding rules per metric) and §10 (define the exactly-0 CI case).

### EC-4. SM-3 OR-branch lets the AI lose Group C numerically yet still "pass"
- **Path/condition:** AI SAR < Baseline on Group C, but the capability ledger (FR-13) argues the tree needs "impractical" authoring → SM-3's OR is satisfied.
- **Why unhandled:** SM-3 is an OR with no guard preventing a numeric *loss* on C from being overridden by an authoring-cost narrative. "Impractical" branch count is undefined (no number). A tree that scored fine on the 8 profiles cannot simultaneously be "impractical" without a defined yardstick.
- **Where to address:** SM-3 — define "impractical" quantitatively and add a floor (AI must not trail on C numerically to use the ledger branch).

### EC-5. SM-4's single structural win is not robust to adjudication
- **Path/condition:** The one Group B/C slot satisfying SM-4 (tree can only skip+flag, AI extracts) is itself a contested slot whose worst-case sensitivity band (FR-30) flips to "tree also handled it."
- **Why unhandled:** SM-4 requires "≥1" structural win but never requires it to survive the worst-case band of FR-30. The minimum win could evaporate under adjudication sensitivity, yet §10 still treats it as present.
- **Where to address:** SM-4 — require the structural-win slot to hold under the worst-case sensitivity band.

---

## B. SAR scoring — undispositioned, unscoreable, and cascade slots

### EC-6. Agent ends a section with required slots still `unanswered` (undispositioned)
- **Path/condition:** Agent calls `end_section` (FR-2) leaving a required slot in `unanswered` — neither recorded, skipped, flagged, nor conditional.
- **Why unhandled:** §6.1 rubric only defines correct/wrong for `recorded`/`flagged`/`skipped`/`conditional`. An `unanswered` slot just scores 0, conflating a flow-control bug ("agent forgot") with a content error ("recorded wrong value"). FR-1's consequence ("stops when MVP satisfied OR all reachable slots dispositioned") has no enforcing guard — nothing catches a premature `end_section`.
- **Where to address:** FR-2/FR-23 — forbid `end_section` with undispositioned reachable slots, or score/report `unanswered` distinctly.

### EC-7. Simulator says "I don't know" to a slot whose answer-key disposition is `recorded:<value>`
- **Path/condition:** A scored slot's disposition requires a value, but the respondent spec's raw facts don't contain it; FR-19 makes the simulator answer "I don't know."
- **Why unhandled:** The slot becomes unfillable, so both systems score 0 — an artifact of *spec/answer-key incompleteness*, not system capability. FR-31's spot-check covers fabrication/leakage but **not** the invariant "every `recorded:<value>` disposition has a surfacing fact in the spec." No FR ties answer-key dispositions to spec fact coverage.
- **Where to address:** FR-27/FR-29/FR-31 — add a consistency check that each `recorded` disposition is answerable from the spec facts.

### EC-8. Cascade — an upstream slot error zeroes many downstream slots
- **Path/condition:** A system mis-records a root slot (e.g., `ownership_model = all_self_owned` when truth is `mixed`), so it never reaches the `owners[]` branch (depends_on guard); all owner slots (disposition `recorded`) score 0. Symmetrically, a wrong `mixed` surfaces owner questions that should be `skipped`.
- **Why unhandled:** §6.1 scores each slot independently and never attributes downstream zeros to a single upstream cause. One root error inflates/deflates the AI−baseline delta by a multiplier depending on *which* system erred. FR-25 reports per-profile case studies but no FR requires separating cascade failures from independent failures.
- **Where to address:** FR-23/FR-25 — require cascade-root attribution in scoring/reporting (e.g., mark downstream zeros as dependent).

### EC-9. A contested slot that is also a cascade root — sensitivity band doesn't propagate
- **Path/condition:** The contested slot adjudicated in FR-30 is `ownership_model` (or another depends_on guard). The best/worst band must then flip the disposition of every dependent owner/S5 slot.
- **Why unhandled:** FR-30's sensitivity band contemplates only the contested slot's own score, not the downstream slots whose expected disposition changes with the adjudication. The reported band understates true sensitivity.
- **Where to address:** FR-30 — specify band propagation through depends_on chains.

### EC-10. Agent stops at MVP line while recommended/optional slots remain — SAR penalty
- **Path/condition:** FR-1 allows stopping when "the MVP-completeness line is satisfied." MVP (§3.1 schema) is required-only, but G5 sets the **SAR denominator to all priority tiers** (required + recommended + optional).
- **Why unhandled:** A legitimate MVP stop leaves recommended/optional slots `unanswered`, scoring 0 against the broader denominator — a stop-policy artifact, not capability. The tree presumably traverses all branches. The two stop conditions in FR-1 and the SAR denominator (G5) are in tension and never reconciled.
- **Where to address:** FR-1 / FR-23 — align the agent stop policy with the SAR denominator, or score MVP-stop slots separately.

---

## C. Echo-before-write / write-tool state transitions

### EC-11. Echo issued, user never confirms (abandons mid-echo)
- **Path/condition:** Agent echoes a number (invariant 1 / FR-2) but the next simulator reply neither confirms nor denies (subject change, "I don't know," defer that isn't a clean skip).
- **Why unhandled:** The write never fires (correct — no false-write), so the slot stays unconfirmed and scores 0 against a `recorded` disposition; the agent is penalized for the simulator's non-confirmation. No FR defines a disposition for "echoed, no confirmation," no confirmation-retry cap (invariant 3 covers *clarifying* questions, not echo confirmations), and no rule preventing an infinite re-echo loop.
- **Where to address:** §8 invariant 1 / FR-2 — define behavior and scoring when an echo is never confirmed.

### EC-12. False-write detection on composite/list tools (`add_owner`, `add_fee`, `add_tax`)
- **Path/condition:** `add_owner` writes a whole owner object containing multiple numerics (`ownership_share`, `pmc_commission_rate`, `fixed_fee_amount`). Some are echoed, some not, before the single tool call fires.
- **Why unhandled:** False-write is defined (§3) per "the value … introduced … in the same turn." For a composite write, *which* sub-field's introduction turn is the reference is undefined. Partial-echo composite writes can pass or fail detection arbitrarily.
- **Where to address:** §3 false-write definition + FR-24 — specify sub-field granularity for composite/list tools.

### EC-13. Echo mechanics for non-numeric financial terms (`split_terms`)
- **Path/condition:** C2's "70% of whatever comes in after fees" maps to `management_model=revenue_split` + free-text `split_terms`. `owners[]` is `echo_before_write:true`.
- **Why unhandled:** Echo-before-write and the false-write rule are defined for *numbers*; `split_terms` is text scored by human raters (§6.1). What must be echoed, and how confirmation of a verbal formula is scored, is unspecified.
- **Where to address:** §8 invariant 1 / FR-3 — define echo/confirmation for non-numeric financial terms.

### EC-14. `end_section` with pending (unconfirmed) echoes
- **Path/condition:** Agent introduces a number, echoes it, then calls `end_section` before the confirming turn.
- **Why unhandled:** No guard forbids closing a section with outstanding echoes; the slot is left unconfirmed → scores 0 (see EC-11). Distinct from EC-6 because the slot was *engaged*, not skipped.
- **Where to address:** FR-2 — prohibit `end_section` while echoes await confirmation, or define the resulting disposition.

---

## D. H2 extractor — sparse vs populated, conflict, small strata

### EC-15. False-prefill on a NON-sparse note is not ceilinged
- **Path/condition:** A content-rich note (Archetype A–E) that simply doesn't mention `migration_source`; the extractor fabricates `hostaway` anyway. Gold = "nothing."
- **Why unhandled:** SM-6 / FR-18 cap false-prefill **only** on the sparse/empty strata (Archetype-F + 32 NA rows). A fabrication on a populated note is the exact "agent confirms a wrong fact" hazard (§3 false-prefill rationale) yet is merely diluted into aggregate micro-F1, with no per-slot or non-sparse ceiling.
- **Where to address:** SM-6 / FR-18 — extend the false-prefill ceiling to per-slot fabrications on populated notes.

### EC-16. SM-6's hard 10% ceiling on a tiny held-out sparse stratum
- **Path/condition:** FR-33 labels ~40–60 notes across six archetypes split into dev/test. The held-out sparse/empty stratum may contain only 3–4 notes; one fabrication = 25–33% > 10%.
- **Why unhandled:** The §6.2 small-N philosophy (CIs, no false precision) is applied to H1 SAR but **not** to SM-6, which is stated as a hard 10% with no minimum-n or confidence interval. H2 can fail on a single noisy instance.
- **Where to address:** SM-6 / FR-33 — set a minimum test-n for the sparse stratum or report the ceiling with a CI.

### EC-17. FR-15 precedence/conflict-surfacing has no test path
- **Path/condition:** "note says Hostaway, user says Lodgify → `user_stated` wins, conflict surfaces" (FR-15) requires the *conversational* flow to reconcile note-prefill against user answers. But the H2 eval (Feature 4.3/4.7) is a **static** task with no user simulator (PoC §7 Component 6).
- **Why unhandled:** FR-15 lives under the extractor feature, but precedence/conflict resolution is only exercisable in the H1 harness — and no FR wires handover-note prefill into the scored 8 profiles, and no metric scores conflict-surfacing. The requirement falls between the static H2 eval and the H1 harness.
- **Where to address:** FR-15 / FR-22 — specify which harness exercises precedence and add a scored conflict-surfacing case, or move FR-15 out of the offline-extractor scope.

### EC-18. Provenance correctness is required to exist but not scored for fidelity
- **Path/condition:** FR-14 requires a "non-null provenance span quotable from the note." Extractor returns a correct value but a paraphrased/non-verbatim (or hallucinated) span.
- **Why unhandled:** "Quotable" is asserted but there is no scoring rule for provenance that doesn't literally appear in the note, and no statement of whether bad provenance with a right value scores as correct.
- **Where to address:** FR-14 / FR-17 rubric — define provenance-fidelity scoring (verbatim match tolerance).

---

## E. Conditional surfacing (S5) and ambiguity contract

### EC-19. S5 `conditional:surface_if_direct_signals` — fuzzy trigger and undefined scoring of sub-slots
- **Path/condition:** FR-4 surfaces S5 on "non-OTA-exclusive operation" among other signals. Most non-100%-OTA hosts qualify, making the trigger near-always-true; the answer key must pre-resolve surface/skip on a fuzzy judgment.
- **Why unhandled:** (a) The "non-OTA-exclusive" signal is so broad it conflicts with "silently skip when no signal," and borderline profiles become contested. (b) Scoring of the *resolved* conditional is underspecified: if surfaced, the three chained sub-slots (`website_brand_name`→`website_domain`→`website_terms`, each depends_on the prior) — how many count, and does surfacing-then-user-defer score as correct skip? FR-4 only addresses surface-vs-skip of the section, not the sub-slot chain.
- **Where to address:** FR-4 + schema §S5 — tighten the signal definition and specify sub-slot scoring under the conditional disposition.

### EC-20. SM-8 "resolved in ≤1 follow-up" vs invariant 3 "one clarify then flag+skip"
- **Path/condition:** An ambiguous input the agent correctly flags after one unsuccessful clarification (invariant 3).
- **Why unhandled:** SM-8 measures "% of ambiguous inputs resolved in ≤1 follow-up." A correct flag-and-skip is *dispositioned* but not *resolved to a value*. Whether a correct flag counts as "resolved" for SM-8 is undefined; if it counts as unresolved, the agent can fail SM-8 by doing exactly the right thing on legitimately-ambiguous inputs.
- **Where to address:** SM-8 — define whether a correct flag-after-one-clarify counts as resolved.

### EC-21. Invariant 3 "flag and skip" maps to two mutually exclusive dispositions
- **Path/condition:** After one failed clarification the agent does "flag and skip" (invariant 3). The §6.1 rubric defines `flagged` and `skipped` as **separate** rows with different correctness conditions.
- **Why unhandled:** A combined flag+skip is not a defined disposition. If the answer key expected `flagged`, does flag+skip score correct? If it expected `skipped`? The hybrid has no rubric mapping.
- **Where to address:** §8 invariant 3 + §6.1 rubric — define the disposition produced by "flag and skip."

---

## F. Flow control, loops, and freeze discipline

### EC-22. No max-turn / non-termination guard on the agent loop
- **Path/condition:** The agent is a message-passing loop (FR-1, §4.1). The user simulator repeatedly answers "I don't know" (FR-19), or the agent never reaches a stop condition.
- **Why unhandled:** No FR caps turns, sets a timeout, or bounds the loop. SM-10 *measures* cost/latency but never *caps* it. A runaway conversation has no terminating guard or defined failure outcome.
- **Where to address:** FR-1 / FR-22 — add a max-turn / timeout guard and a defined outcome on hitting it.

### EC-23. "I don't know" treated as ambiguity vs absence — re-ask loop
- **Path/condition:** Simulator returns "I don't know" (fact absent from spec). The agent may rephrase and re-ask.
- **Why unhandled:** Invariant 3 caps *clarifying* questions per *ambiguous* answer, but an IDK is absence, not ambiguity. Whether IDK triggers the one-clarify cap, an immediate skip, or unbounded re-asks is unspecified — feeds EC-22.
- **Where to address:** §8 — add an invariant for handling absent-fact ("I don't know") replies.

### EC-24. Skipping a *required* slot (e.g., `ownership_model`) — invariant 4 vs MVP
- **Path/condition:** A "defers everything" profile (B4) skips `ownership_model` (required). Invariant 4 honors skip immediately, setting status `skipped`.
- **Why unhandled:** §3.1 schema requires required fields "recorded **or explicitly flagged**" — a `skipped` status is neither. Invariant 4 (honor skip) and the MVP definition conflict for required fields, and the answer-key disposition for a skipped required field is not defined. The hero branch also never opens, cascading to all owner slots (see EC-8).
- **Where to address:** §8 invariant 4 + schema §3.1 — define handling/disposition when a *required* field is skipped.

### EC-25. Re-freeze scope excludes simulator/harness changes
- **Path/condition:** After the frozen run, a bug is found in the **user simulator** or the **scoring harness** (not a SUT) and fixed.
- **Why unhandled:** FR-26 requires re-freeze + re-run only for "post-freeze change to **a system**" (SUT = agent/tree). A simulator or scoring fix mid-analysis is not covered, yet it changes results just as much.
- **Where to address:** FR-26 — extend re-freeze discipline to the simulator and harness.

### EC-26. G3 enum casing closes *during/after* the frozen run
- **Path/condition:** OPEN-3 re-freezes "if G3 closes **before** the eval run." G3 instead closes mid-k-runs or after.
- **Why unhandled:** Tax-enum slots are scored on provisional casing with "exact match on canonical casing" tolerance and no casing-normalization fallback. A semantically-correct tax extraction scores 0 on a casing mismatch, and the re-freeze rule has no branch for closure during/after the run.
- **Where to address:** OPEN-3 / §6.1 tolerance — add a during/after-run branch and a casing-normalization fallback for enums.

---

## G. Fairness-control failure branches

### EC-27. Scripted Group A simulator vs adaptive agent question order
- **Path/condition:** FR-21 permits "deterministic scripted turns" for Group A. FR-1 makes the agent ask adaptive, order-varying questions.
- **Why unhandled:** A canned turn list presupposes a question order; if the agent asks Group A slots out of the scripted order, canned replies may not match the asked question. The scripted-simulator/adaptive-agent mismatch has no reconciliation rule.
- **Where to address:** FR-21 — specify how scripted Group A turns map to out-of-order adaptive questions (keyed by slot, not sequence).

### EC-28. Per-run simulator fidelity on un-spot-checked adaptive branches
- **Path/condition:** FR-31 spot-checks simulator transcripts *before* the frozen run. Transcripts are generated per-run (k≥5) and adaptively, so each run can traverse branches never spot-checked. A runtime simulator error (reply inconsistent with spec facts) corrupts that run's input for both systems.
- **Why unhandled:** The answer key scores against the *true* spec fact, so a simulator-induced wrong reply scores both systems 0 on a non-capability error. No per-run or post-hoc simulator-fidelity check exists.
- **Where to address:** FR-31 — add a per-run (or sampled post-run) simulator-fidelity check.

### EC-29. Fairness sign-off (FR-11) refused — no rejection branch
- **Path/condition:** The reviewer declines to certify the tree as good-faith (judges it a strawman or, conversely, profile-leaked).
- **Why unhandled:** FR-11 specifies only the success path ("a signed certification exists"). There is no defined branch for a refused sign-off — re-author, re-freeze impact, schedule effect (Phase 2).
- **Where to address:** FR-11 — define the rejected-certification path.

### EC-30. Single-author fallback (FR-10) — caveat with no compensating control
- **Path/condition:** §14 assumption: if staffing can't supply two authors, it's "flagged as a fairness caveat."
- **Why unhandled:** With one author for both tree and agent prompt, the FR-9 anti-leakage guarantee weakens (the author has seen the agent's design), yet the only mitigation is a documented caveat — no FR adjusts verdict weight or adds a compensating control, so a passing result under single authorship is interpreted identically to a clean one.
- **Where to address:** FR-9/FR-10 / §14 — specify a compensating control or interpretation discount for single-author runs.

---

## H. Secondary-metric boundaries

### EC-31. SM-7 with a zero-question baseline (division boundary)
- **Path/condition:** A fully prefilled Group A profile where the baseline confirms everything silently and asks 0 user-facing questions. SM-7 = "AI ≤ baseline × 1.2" → 0; any AI question fails SM-7.
- **Why unhandled:** No floor or handling for baseline = 0 user-facing questions; the multiplicative bound degenerates.
- **Where to address:** SM-7 / FR-24 — define behavior when baseline question count is 0.

### EC-32. SM-7 — do echo-confirmation turns count as "questions"?
- **Path/condition:** Echo-before-write requires a user-facing confirmation turn requiring a reply. FR-24 counts "user-facing asks."
- **Why unhandled:** Whether an echo-confirmation turn is a counted "question" is undefined. If counted, the echo invariant structurally inflates question counts; if not, the rule must say so. Affects SM-7 comparability.
- **Where to address:** FR-24 / §3 — define whether echo-confirmation turns count toward questions-to-completion.

### EC-33. SM-9 "acceptable inter-rater agreement" and SM-6/SM-C3 thresholds are undefined
- **Path/condition:** SM-9 passes only if mean ≥4.0 **and** κ is "acceptable," but no κ value is given (same undefined-threshold class as SM-C3 stability).
- **Why unhandled:** "Acceptable" is unquantified; a 4.1 mean with low κ has no defined verdict.
- **Where to address:** SM-9 / FR-34 — set the κ (or % exact agreement) threshold.

---

## Coverage note

Walked: every FR (FR-1..FR-34) consequence; §7 SM-1..SM-11 + SM-C1..C3 boundaries; §8 invariants 1–6 state transitions; §10 kill criteria; schema depends_on guards (S4, S5 chain, S8 hero fan-out), echo_before_write fields, source-precedence; PoC-plan §4.1/§5.1/§6.1/§6.2 scoring and freeze rules. Handled paths discarded silently. Findings above are paths with **no explicit guard, disposition, or threshold** in the spec.
