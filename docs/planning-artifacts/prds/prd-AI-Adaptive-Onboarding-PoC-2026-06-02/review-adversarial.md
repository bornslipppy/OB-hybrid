---
title: "Adversarial Review — AI Adaptive Onboarding PoC PRD (Eval-Harness Build Spec)"
reviewer: "Cynical Reviewer (adversarial pass)"
target: "prd.md (this folder) + .decision-log.md"
context_read:
  - poc-plan-ai-adaptive-onboarding-2026-06-02.md (v1.2 — source of truth)
  - guesty-pro-account-creation-schema.md (v0.3)
  - brief-for-pm-2026-06-02.md (D1–D6)
date: 2026-06-02
method: bmad-review-adversarial-general
scope_note: "Experiment design is out of scope (already adversarially reviewed). This pass attacks the PRD's testability, metric/kill-criteria loopholes, and fidelity to the decision log + source plan + schema."
---

# Adversarial Review — AI Adaptive Onboarding PoC PRD

**Verdict:** The PRD is well-structured and mostly faithful to the source plan, but it is **not yet build-ready or game-proof**: the SAR denominator is undefined and contradicts D4/schema in a way that can gut or inflate the headline metric, free-text "correct" is left unspecified, Group C and H2 each carry an unguarded escape hatch, and there is no rule for how the H1+H2 verdict aggregates. A motivated builder can "pass" this PoC without the AI actually earning its place.

Findings are ordered by severity. Each cites the FR/§/decision it attacks.

---

## CRITICAL

### C1 — The SAR denominator is undefined, and the only definitions on offer contradict each other and gut the test
SAR is `correct_slot_decisions / total_scored_slots` (§3 glossary, FR-23), and §7 makes per-group SAR the primary verdict. **But the PRD never states which slots enter `total_scored_slots`.** The two candidate definitions diverge sharply:
- FR-1's stop condition and the glossary cite **schema §3.1 (the MVP-completeness line)**. Schema §3.1 is **`required` fields only**.
- D4 (`.decision-log.md`) ratifies "the schema's `required`/`recommended`/`optional` tiers (schema §3)" as "the MVP-completeness line **and** the SAR denominator" — i.e. the §3 weighted `completion_pct` over **all three tiers**.

These are not the same set. Per schema v0.3, virtually every slot where AI is supposed to win is **not `required`**: all S4 financial echo fields (`security_deposit_amount`, `payment_split`, `taxes` → `recommended`/`optional`), and the entire S0b extraction layer (`migration_source`, `ob_language`, `addon_intent` → `recommended`/`optional`). If the denominator is "required-only" (FR-1's §3.1), the AI-advantage slots barely count and SAR is dominated by easy structured `required` fields the tree also gets right — **washing out exactly the signal the PoC exists to detect**, and biasing toward the null. If the denominator is the weighted §3 formula, that must be stated (with the weights) because it changes every threshold in §7. This single ambiguity is load-bearing for SM-1/2/3 and the §10 kill criterion. **The PRD must pin the scored slot set explicitly and reconcile FR-1 with D4.**

### C2 — Group C's "OR impractical-authoring" branch (SM-3) is an unbounded, self-judged escape hatch
SM-3 lets the AI pass Group C either by `≥25 pp` SAR **or** by the capability ledger (FR-13) "documenting that the baseline requires an impractical number of hand-authored branches." There is **no threshold for "impractical"** (10 branches? 100?), and the ledger is **authored by the tree builder themselves** (FR-13) with **no independent adjudication** of the "impractical" conclusion — FR-11's fairness sign-off only certifies the tree is competent, not that any failure to branch was unavoidable. With only **2 Group C profiles**, the numeric `≥25 pp` bar is already fragile, so the qualitative escape hatch will carry the verdict in practice. This is precisely the spot where D1's "exploration" framing can be used to dodge rigor: a team whose AI does **not** beat the tree on C can simply assert "the tree would have needed too many branches" and claim the win. **Require a pre-registered, independently-reviewed definition of "impractical" (e.g., branch-count or time-to-author ceiling) before the ledger can satisfy SM-3.**

### C3 — "Correct" is undefined for free-text slots — the exact slots SM-4 and C2 hinge on
FR-23's scoring rubric only specifies disposition matching and **"Numbers are scored exact."** It is silent on free-text slots. The source plan (PoC §6.1) routes free-text (`pain`, `split_terms`) to the **§6.3 blind human raters** under a "captures the same fact" rubric — **but the PRD never carries this forward.** Yet SM-4 (the mandatory qualitative structural win) and profile C2 (`revenue_split` + `split_terms`, "70% of whatever comes in after fees") are *exactly* free-text extraction cases. As written, "the AI extracts correctly" (SM-4, UJ-2) has **no defined scorer, rubric, blinding, or tolerance** in the build spec. This is both un-buildable (the engineer can't implement the scorer) and gameable (free-text wins can be graded generously by the same team). **Add an FR that imports the §6.3 blind-rater "captures the same fact" protocol for every free-text scored slot, and route SM-4 through it.**

### C4 — The H2 regex baseline has none of the anti-strawman protections H1's tree has
H1 spends four FRs (FR-9 blind authoring, FR-10 independent author, FR-11 written fairness sign-off, plus FR-13 ledger) ensuring the tree is not a strawman — because "a rigged baseline invalidates the whole PoC" (PoC §4.1). **The H2 regex baseline (FR-17) gets none of this:** no blind authoring, no independent author, no "competent, good-faith" certification, no fairness reviewer. So SM-5's `≥15 pp micro-F1` margin is trivially achievable against a deliberately or carelessly weak regex, and nobody is accountable for that weakness. This is an unguarded asymmetry that lets H2 "pass" by sandbagging its comparator. **Apply FR-9/FR-11-equivalent fairness discipline (good-faith authoring + written sign-off) to the regex baseline.**

---

## HIGH

### H1 — No rule for how the verdict aggregates H1 + H2
The PRD repeatedly states H1 and H2 are "independently falsifiable" and "both outcomes are valuable" (§1, FR-18 note, §4.3), but **never defines the combined verdict.** What is the recommendation if H1 passes and H2 fails? If H2 passes and H1 fails? §7 lists H1 and H2 metrics in parallel; §10 kill criteria mention H2 only via "fails H2 regardless of F1" (false-prefill) but never say a failed H2 affects the overall fund/no-fund recommendation. UJ-4 (the decision-maker's journey) reads **only** H1 results and recommends "fund the live prototype" — H2 is absent from the verdict it models. "Both valuable" is a sentiment, not a decision rule. **Add a verdict matrix (H1×H2 → recommendation) and state which claim, if either, gates the live-prototype greenlight.**

### H2 — Decision-stability is required everywhere but quantified nowhere
SM-C3, §10, and FR-25 all hinge on the verdict being "stable across k≥5 runs," and SM-2 requires "a verdict stable across k≥5 runs." **No finding defines "stable."** 5/5? 4/5? 3/5? FR-25 reports a "verdict-flip rate" but sets no pass line on it. Since stability is the counter-metric guarding against a lucky run (SM-C3) and is a hard kill condition (§10), leaving it unquantified lets a builder declare a 3/5 result "stable." **Pre-register the stability threshold (e.g., verdict holds in ≥k−1 of k runs).**

### H3 — Echo-before-write protection silently depends on the simulator correcting wrong echoes — which FR-19 never requires
§8.1 and SM-C1 make echo-before-write the determinism guarantee and a zero-tolerance kill criterion. But "echo-before-write" only catches a *wrong* number if the user simulator, on hearing the agent echo a wrong value, **disagrees and corrects it.** FR-19 only requires the simulator to "answer from the spec's raw facts" and "never invent facts" — it does **not** require the simulator to detect and reject an incorrect echoed-back value. If the simulator simply confirms whatever it is asked to confirm (a common LLM-as-user failure mode), echo-before-write and the entire false-write defense are theater, and false-write rate is structurally 0 for reasons unrelated to safety. **Add an FR requiring the simulator to correct mismatched echoes, and a dev-set test that proves it does (e.g., agent echoes 50% when truth is 15% → simulator must reject).**

### H4 — Freeze discipline (FR-26) is self-policed and leaves the garden of forking paths open
FR-26: "Any post-freeze change to a system requires re-freeze + re-run, noted in the report." There is **no pre-registered cap on the number of re-freezes**, and **no requirement to report all prior frozen runs** — only to "note" each. A team that gets a disappointing frozen result can tweak the prompt, re-freeze, re-run, and report only the favorable latest campaign while technically "noting" the re-freeze. Combined with the "run once" language (see M2), this is the classic multiple-comparisons loophole. **Require pre-registration of k and a maximum re-freeze count, and mandate that every frozen-run result (not just the last) appears in the report.**

### H5 — Per-group bootstrap CIs are statistically degenerate for Groups A and C (n=2 each)
FR-25/SM-2/SM-3 lean on "bootstrap confidence intervals clustered by profile" and "CI clearing zero." Group A and Group C each have **only 2 profiles** (FR-27). A bootstrap **clustered by profile** with **2 clusters** cannot produce a meaningful CI — it resamples among two units. So the "CI clears zero" condition in SM-2 is only arguably defensible for Group B (4 profiles), and is essentially undefined for the per-group A/C verdicts the kill criterion (§10) relies on. The PRD correctly disclaims profile-level significance (§5, SM line) but does **not** acknowledge that its chosen CI method is inapplicable at the per-group granularity it reports. **Either pool the CI across the full scored-slot set or explicitly downgrade per-group A/C CIs to descriptive-only and state it.**

### H6 — D1 "no go/no-go gate" contradicts §10, which reinstates a hard gate
D1 and the §0 framing insist the §7 thresholds are "decision heuristics, not a binding go/no-go gate." But §10 makes "AI shows no material, stable advantage on Groups B+C — delta does not clear SM-2/SM-3, *or* CI straddles zero, *or* not stable — and no qualitative win" a **hard kill**. That is a go/no-go gate on the headline result, expressed as a kill criterion. The same "CI clears zero" condition is therefore simultaneously a soft heuristic (§7/SM-2) and a hard stop (§10). The "exploration, not a gate" framing is partly illusory — and the contradiction will surface the moment a borderline result lands. **Reconcile: state plainly that the B+C advantage *is* effectively gated by §10, or remove it from §10 and keep it heuristic.**

### H7 — The anti-leakage backbone can collapse to one self-attesting author under D1/D6
FR-9 anti-leakage rests on "a written attestation" **by the tree author** — self-attested, with no independent verification of non-exposure. FR-10 (independent authorship) is itself an `[ASSUMPTION]` that "staffing allows two distinct authors; if not, flagged as a fairness caveat," and D6/OPEN-1 leaves **all** owners as `[OWNER TBD]`. So the load-bearing fairness controls (blind, independent, signed-off) may, in practice, reduce to a single person authoring both the tree and the agent prompt, self-attesting blindness, and the whole thing proceeding under a "documented caveat" — which D1's exploration framing makes easy to wave through. **Make distinct tree/agent-prompt authors a hard precondition (not an assumption), and have a second person verify the freeze, not just the author attest it.**

---

## MEDIUM

### M1 — SM-1 contradicts itself on the Group A bar
SM-1 reads "AI SAR ≥ Baseline SAR on Group A; AI must not trail by >5 pp." The first clause demands parity-or-better (trail by 0); the second permits trailing by up to 5 pp. §10's kill criterion uses the −5 pp line. The headline clause is therefore wrong/misleading. **Drop "AI SAR ≥ Baseline SAR" or restate it as the −5 pp tolerance to match §10/D2.** (Inherited from PoC §6, but the PRD should fix it, not propagate it.)

### M2 — "Run once" (FR-26) vs "k≥5 runs" (FR-22), and k is an uncapped floor
FR-26 says the scored 8 are "frozen and run once"; FR-22 says each is run "at least 5 times." The intent is presumably "one frozen campaign of k≥5 runs," but the wording is a latent contradiction a builder can exploit either direction. Worse, `k≥5` is an unbounded floor with no pre-registered value, so a team can keep adding runs until stability/CI looks favorable (interacts with H4). **Fix k to a pre-registered number before the frozen run and rephrase FR-26 as "one frozen campaign."**

### M3 — The tree's tool-call trace contract is never specified, yet FR-24 scores it from the trace
FR-2 mandates the 7-tool vocabulary and machine-readable trace **for the agent only**. FR-7–FR-13 (the tree) never require the tree to emit the same tool vocabulary or trace format. But FR-24 computes false-write rate "from the tool trace" for **both** systems and FR-8 asserts "the tree's false-write rate is 0." Without an FR mandating an equivalent tree trace, false-write detection on the tree is unimplementable as specified. **Add a tree-side FR requiring the same tool surface / trace schema as FR-2.**

### M4 — S5 conditional disposition can flip with stochastic simulator phrasing against a frozen key (FR-4, FR-25)
FR-4 scores S5 as correct-skipped on no-signal profiles and correct-surfaced on signal profiles, but whether a "direct-booking signal" actually appears depends on what the **stochastic simulator** says in a given run. Across k runs the simulator may or may not volunteer "my website," flipping the *correct* disposition while the answer key is frozen — which FR-25 will then flag as a "reliability red flag" that is actually a harness artifact, not an agent defect. **Pin the S5 signal in each profile's spec/persona deterministically, or score S5 conditional on the realized transcript, not the frozen key.** Also: FR-4/glossary write the disposition `conditional:surface_if_direct_signals` while schema v0.3 §S5 writes `conditional: surface_if_direct_signals_present` — a literal-string mismatch a strict scorer would miss.

### M5 — Temperature 0.2 on "structured extraction" injects variance into the very Group B slots SM-2 measures
FR-6 sets temp 0.2 for structured extraction (only numeric/financial writes get 0.0). The ambiguous Group B extraction slots driving the headline SM-2 lift are run at 0.2, so the `≥15 pp` advantage carries avoidable run-to-run variance — in tension with the determinism narrative (§8) and with the small-N stability concern. **Justify 0.2 on extraction or drop to 0.0 for scored extraction slots.**

### M6 — Number scoring: "exact" vs "within tolerance," and no rule for ranges
FR-23 says numbers are "scored exact," but the glossary's `recorded:<value>` and FR-23's own "recorded within tolerance" imply a tolerance band — which is it, and what is the band? Separately, profile B2's expected disposition is a **range** ("15–20%, flagged"), and FR-23's exact-number rule gives no scoring rule for a correctly-captured range. **State the numeric tolerance (likely zero) unambiguously and add a range-capture scoring rule.**

### M7 — SM-5 micro-F1 has no defined matching rule across heterogeneous slot types
H2 slots span enums (`migration_source`), set-valued fields (`risk_flags`, `addon_intent` = `list<enum>`), and fuzzy text. Micro-F1 requires a per-type TP/FP/FN matching rule (exact for enums? set-overlap for lists? rubric for text?), none of which FR-14/FR-17/SM-5 specify. Without it, the `≥15 pp` margin is not reproducible. **Define the matching rule per slot type.**

---

## LOW

### L1 — SM-10's latency threshold is TBD (OPEN-4), so the metric is currently inert
SM-10 flags (not fails) median latency above "a conversational threshold," but OPEN-4 leaves that threshold undefined. A known live-viability risk (cost/latency, §11) therefore cannot trigger even its soft flag until OPEN-4 closes. Acceptable under exploration framing, but should be acknowledged the metric is presently non-operative. **Set a placeholder threshold so the flag can fire.**

### L2 — "Questions to completion" (SM-7) compound-question ambiguity
The rule counts "distinct asks requiring a user reply," but a tree asking one compound question vs an agent asking two atomic ones are scored differently for the same information gained, partially undermining the `≤ baseline × 1.2` comparison. **Define how compound/batched questions are counted.**

### L3 — Contested-slot machinery (FR-29/FR-30) handles value disputes, not scope disputes
The tie-breaker + sensitivity band covers reviewers disagreeing on a slot's *disposition/value*. It does not cover reviewers disagreeing on whether a slot is **in the scored set at all** — which directly moves the SAR denominator (see C1). **Extend adjudication to denominator membership.**

### L4 — B4's fully-deferred section contributes mostly null-signal slots
B4 defers the entire Financials section; per the rubric, `skipped`-disposition slots score correct for **both** systems, inflating both SARs and contributing little discriminating signal. Not a defect, but worth noting B4 mostly tests "honor skip" invariants, not extraction advantage — so it should not be read as evidence for or against H1's core claim. **No change required; interpret B4 accordingly in the report.**

---

## Summary of required fixes before this PRD is build-ready
1. **Pin the SAR denominator** and reconcile FR-1 (schema §3.1, required-only) with D4 (weighted §3). *(C1)*
2. **Define free-text scoring** via the §6.3 blind-rater protocol and route SM-4 through it. *(C3)*
3. **Bound the SM-3 "impractical-authoring" escape hatch** with a pre-registered, independently-reviewed threshold. *(C2)*
4. **Give the H2 regex baseline the same anti-strawman discipline** as the tree. *(C4)*
5. **Add an H1×H2 verdict matrix.** *(H1)*
6. **Quantify decision-stability** and the re-freeze/k pre-registration. *(H2, H4, M2)*
7. **Require the simulator to correct wrong echoes** (or echo-before-write is theater). *(H3)*
8. Fix the per-group CI method (H5), the D1↔§10 gate contradiction (H6), the anti-leakage staffing precondition (H7), and the SM-1 wording (M1).
