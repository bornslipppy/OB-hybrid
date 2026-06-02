---
title: "PRD Quality Review — AI Adaptive Onboarding PoC (Eval-Harness Build Spec)"
---

# PRD Quality Review — AI Adaptive Onboarding PoC (Eval-Harness Build Spec)

## Overall verdict

This is an unusually disciplined PRD: it knows exactly what it is — an offline falsification experiment, not a product — and almost everything in it is load-bearing. The thesis ("adaptivity alone doesn't justify AI; AI earns its place only where a tree provably cannot keep up") is stated, bet on, and wired straight through to the success metrics, counter-metrics, and kill criteria. FRs carry testable consequences, the glossary is tight, traceability FR↔SM↔kill-criteria mostly resolves, and the anti-bias protocol (blind authoring, two-reviewer + tie-breaker, dev/test freeze) is encoded in the UJs rather than asserted. It is decision-ready as a *spec*.

What's at risk is a single but consequential asymmetry: the PRD holds H1 to a high statistical-honesty standard (bootstrap CIs clustered by profile, decision-stability across k≥5 runs, "no significance claims") while H2 — an equally primary claim — is left with bare point thresholds (SM-5 ≥15 pp micro-F1, SM-6 ≤10% false-prefill) on a labeled test subset of only ~40–60 notes split into dev/test, with no uncertainty band and no run-to-run stability guard on a stochastic LLM extractor. The PRD's own rigor about N=8 makes this gap conspicuous. Secondary issues are mechanical (one mis-cited UJ→FR link, a cluster of undefined `G#`/`Path`/`Archetype` tokens that live only in source docs, an Assumptions-Index roundtrip miss). Net: strong, with one high-severity gap to close before the verdict carries equal weight on both claims.

## Decision-readiness — strong

A decision-maker can act on this. The six PM decisions (D1–D6) are stated as decisions and ratified in `.decision-log.md`, not buried as "considerations." Trade-offs are named with what was given up: D1 chooses exploration framing *over* a binding go/no-go gate and says so; §1 concedes "adaptivity alone does not justify AI" — the PRD argues *against* its own headline feature where the evidence (Tree-CAT equivalence, Grade A) demands it. The Open Questions (OPEN-1…5) are genuinely open — resourcing, PII method, enum casing, latency threshold, production write paths — not rhetorical setups. `[NOTE FOR PM]` callouts sit at real tensions (FR-6: "Real determinism comes from echo-before-write, not temperature"; §9: confirm de-identification method), not safe checkpoints.

The one soft spot is the **combined H1+H2 recommendation rule**. The PRD treats the two claims as separable (correctly) and gives the decision-maker two independent verdict paths (UJ-4 for H1; the FR-18 note for H2), and §1 sketches the four corner outcomes ("a validated claim greenlights… a falsified claim still ships the honest tree"). But it never states the synthesis the Decision-Maker persona (§2.1) actually consumes: what is the build recommendation when H1 passes and H2 fails, or vice-versa? It is inferable, not stated.

### Findings
- **medium** Combined H1/H2 recommendation framework is implicit (§1, §7, UJ-4) — the decision-maker gets two independent verdicts but no stated rule for the four pass/fail combinations. *Fix:* add a short decision matrix (H1×H2 → recommendation) to §7 or §13, even if it's "H1 and H2 are reported and funded independently."
- **low** D2 thresholds (≥15 pp / ≥25 pp) are ratified as "PM default accepted; no objection raised" with only light magnitude justification (D3 calls 15 pp "clear, defensible… consistent with the H1 Group B bar"). Acceptable under exploration framing, but a skeptic asking "why 15 and not 10 or 20?" finds little. *Fix:* one sentence on why the magnitude is the smallest effect worth acting on.

## Substance over theater — strong

Almost no furniture. The three personas (§2.1) each drive concrete content: the Eval Engineer demands the fixed tool surface and deterministic rubric (FR-2, FR-23); the Answer-Key Reviewers exist because blind, adjudicated ground truth is the experiment's integrity (FR-29, FR-30, FR-34); the Decision-Maker's needs shape FR-25's "honest to N=8" reporting. The four UJs each realize named FRs and carry a real edge case (UJ-2's "never silently dropped — dropping it would bias toward the null on exactly the cases that test AI's advantage" is the opposite of theater). The Vision (§1) is specific to this experiment and could not be pasted into another PRD. §9 PII governance is product-specific (real Salesforce notes, provenance spans must themselves be de-identified), not boilerplate "must be secure." NFR usage is sparse and earned (FR-6's machine-readable tool-call trace exists to enable false-write detection). No innovation theater — the PRD actively deflates the novelty claim.

### Findings
- None material.

## Strategic coherence — strong

The PRD reads as a single bet, not a backlog. The thesis is explicit and every feature serves it: Features 4.1–4.2 are the head-to-head SUTs, 4.4–4.6 are the fairness rig that makes the comparison attributable, 4.3/4.7 are the separable H2 case. Prioritization follows the thesis, not ease — the "hero branch" (S8 combinatorial fan-out) is named the primary surface precisely because it is the case the thesis predicts a tree cannot keep up with (FR-3, FR-7, SM-3). Success Metrics validate the thesis rather than measuring activity: SAR deltas are demanded on exactly the input classes (ambiguous, combinatorial) where AI is theorized to win, and SM-4 forbids a "purely numeric delta" without a structural win. Counter-metrics are present and pointed (SM-C1 false-write, SM-C2 advice, SM-C3 stability), each tied to a kill criterion. MVP scope kind is coherently "problem-solving / experiment," and §6 scope logic matches.

### Findings
- None material.

## Done-ness clarity — strong (with one cross-cutting gap)

This is where the PRD is strongest structurally and where its one real weakness lives. Every FR carries a **Consequences (testable)** block, and most are genuinely verifiable: FR-1 ("question order diverges… never asks a slot whose `depends_on` guard is unmet"), FR-23 ("numbers scored exact… 15% vs 50% scores 0"), FR-24 (false-write "computed programmatically from the trace"), FR-9 (written attestation of freeze). Vague adjectives are rare and mostly bounded (FR-12's "reasonable synonym mapping" is constrained by parity with the agent and "not crippled to literal string matching").

The gap is **H2's done-ness as a *trustworthy* verdict, not its testability per se.** SM-5/SM-6 are testable, but the PRD applies its small-N honesty machinery (FR-25: bootstrap CIs clustered by profile, decision-stability, "no significance claims") only to H1. H2's held-out test set is a subset of ~40–60 labeled notes (FR-33), split dev/test — so the scored set may be ~20–30 notes, and the SM-6 false-prefill denominator (sparse/empty strata only) could be a handful of notes where one fabrication = 20%+. Nothing requires the stochastic extractor to be run k≥5 times (FR-22's k≥5 applies to "SUTs," and the glossary defines SUT as Agent or Tree — the extractor is neither), so there is no run-to-run stability guard and no uncertainty band on the F1 margin. A "≥15 pp micro-F1" point estimate on a small test set is exactly the kind of single-run over-read the PRD is otherwise scrupulous about.

### Findings
- **high** H2 metrics lack the small-N rigor the PRD demands of H1 (§7 SM-5, SM-6; FR-33; FR-22/FR-25) — point thresholds with no CI, no clustered uncertainty, and no repeated-run stability on a stochastic extractor over a ~20–30-note test set. *Fix:* extend FR-25's discipline to H2 — report the F1 margin with a bootstrap CI, run the extractor k times for a false-prefill stability figure, and state the sparse/empty test-stratum count so SM-6's resolution is honest.
- **low** "Acceptable inter-rater agreement" (SM-9) and "conversational threshold" (SM-10) are unbounded adjectives. SM-10 is explicitly deferred to OPEN-4 (fine); SM-9 is not. *Fix:* give SM-9 a numeric floor (e.g., κ ≥ 0.6) or point it at an open item.

## Scope honesty — strong

Omissions are explicit, not inferred. §5 Non-Goals does real work and draws bright lines (no live UI, no production Guesty API, **no BusinessModel writes ever in this PoC**, no powered significance claims, no Airbnb OAuth in the frame). `[ASSUMPTION: …]` tags sit on the two real inferences (FR-6 model family; FR-10 two distinct authors) and both are indexed in §14. `[NOTE FOR PM]` callouts mark deferred decisions honestly (§6.2 "these are the *reward* for a passing PoC"). De-scoping is proposed, not done silently — the OB Specialist Brief is named, scoped at a high level, and explicitly deferred so it is "not forgotten."

Open-items density is high for a green-light-to-build document — five Open Questions, three indexed assumptions, multiple `[NOTE FOR PM]`, and six `[OWNER TBD]` placeholders — but the stakes justify it: this is funded *exploration*, and every open item is acknowledged rather than hidden (OPEN-1 + D6 + a Risks-table row all flag that resourcing must be assigned before the Phase 1 freeze). The honest read is "build-ready as a spec, execution-blocked on resourcing," and the PRD says exactly that. That is scope honesty working, not failing.

### Findings
- **low** `[OWNER TBD]` appears in six places (§2.1, §9, §12 ×4, §13) and is a hard prerequisite to starting Phase 1. Honestly flagged, but worth stating once at the top that the spec is execution-gated on OPEN-1. *Fix:* a one-line banner under §0/§12 that no Phase begins until OPEN-1 closes.

## Downstream usability — adequate

This PRD is explicitly chain-top: it feeds a downstream live-prototype PRD and is the build spec for engineers. The internals support that well — FR/UJ/SM IDs are contiguous (FR-1…34, no gaps or duplicates), unique, and most cross-references resolve; the glossary anchors the domain nouns; each FR reads coherently pulled out alone. Where it loses points is **standalone readability against its source docs**: the PRD leans on tokens defined only in the PoC plan and schema — `G1`–`G6` ("G1 resolution," "G6 resolution," "G3 provisional"), `Path B/G/C`, and `Archetype A–F` — none of which appear in the §3 Glossary. A build engineer reading `prd.md` alone hits "intent-capture only (G1 resolution)" with no in-document referent. The PRD does declare it references sources "by section ID," so this is partly by design, but the most-used of these tokens deserve a glossary line. There is also one broken FR cross-reference and a minor schema-section typo (below).

### Findings
- **medium** Undefined domain tokens used throughout (`G1`–`G6` in FR-3/FR-4/§12/OPEN-3; `Path B/G/C` in §8/§10/SM-C2; `Archetype A–F` in FR-18/FR-33/UJ-3) — defined only in source docs, absent from §3 Glossary. *Fix:* add the high-frequency ones (at minimum G1, G6, and "Archetype-F / Paths") to the Glossary or a one-line "gate resolutions" note.
- **medium** UJ-3 cites the wrong FR — "Realizes FR-18, FR-20." FR-20 is *User Simulator: No target leakage* (H1), unrelated to the extractor's abstention scenario. *Fix:* change to FR-18 (+ FR-14 provenance) and drop FR-20.
- **low** UJs reference personas by paraphrase ("the engineer," "a reviewer," "the decision-maker") rather than the exact §2.1 labels ("The Eval Engineer," etc.). Resolvable, but not exact-label linkage. *Fix:* align to the defined labels.

## Shape fit — strong

The PRD resists two opposite failure modes. It does not over-formalize: although the "user" is the internal eval team (correctly stated in §2), the UJ density is *justified* because process integrity — blind authoring, contested-slot adjudication, dev/test freeze, abstention — is the entire substance of a falsification experiment, so the UJs encode the protocol rather than decorate it. And it does not under-formalize: the capability-spec elements (fixed tool surface FR-2, agent invariants §8, machine-readable traces) coexist with the experiment-protocol elements without either crowding out the other. SMs are appropriately operational/experimental rather than user-facing engagement metrics. The hybrid "capability spec + experiment protocol" shape matches what an offline eval harness actually is.

### Findings
- None material.

## Mechanical notes

- **Glossary drift:** Minor — "Echo-before-write" (glossary/§8 heading) vs. the field tag `echo_before_write` (FR-2, §8.1, FR-8). Same concept, acceptable. No synonym/plural drift detected on the core nouns (Slot, Disposition, SAR, SUT used identically throughout).
- **ID continuity:** FR-1…FR-34 contiguous, unique, no gaps. SM-1…SM-11 + SM-C1…SM-C3 contiguous. UJ-1…UJ-4 contiguous. Feature numbering 4.1–4.7 contiguous.
- **Cross-references:** One broken — UJ-3 → FR-20 (should be FR-18/FR-14), flagged above. One likely typo — FR-1 cites "§3.1 of schema" for the MVP-completeness line while D4 ratifies "schema §3" tiers; reconcile §3 vs §3.1.
- **Assumptions Index roundtrip:** Two inline `[ASSUMPTION]` tags (FR-6, FR-10) — both indexed in §14. The third §14 entry ("§4 general — drafted respondent specs… are the starting drafts") has **no** corresponding inline `[ASSUMPTION:]` tag at FR-27/FR-28/FR-33 (the feature text says "Drafts already exist" untagged). *Fix:* either add the inline tag or move that note out of the Assumptions Index.
- **UJ persona linkage:** Each UJ maps to a §2.1 persona, but by paraphrase rather than exact label (flagged under Downstream usability).
- **Required sections:** All present for an internal experiment / build-spec shape — Vision, Target User, Glossary, Features+FRs, Non-Goals, MVP Scope, Success Metrics, Invariants, Data Governance, Kill Criteria, Risks, Rollout, Open Questions, Assumptions Index.
