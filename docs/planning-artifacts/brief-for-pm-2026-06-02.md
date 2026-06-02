---
title: "PM Brief — AI Adaptive Onboarding PoC: Decisions Needed"
for: "BMAD PM (John)"
from: "Mary (Business Analyst)"
date: 2026-06-02
purpose: "Self-contained handoff. Paste into a fresh PM agent window. The PM does not need the analyst chat — everything is here or in the linked artifacts."
---

# PM Brief — AI Adaptive Onboarding PoC

You are picking up a planning package from the analyst (Mary). The analyst track is complete and
self-contained. **I need product decisions from you, not more analysis.** This brief gives you the
context and the exact decisions to make.

---

## 1. What this is (30 seconds)

Guesty Pro has a rule-based onboarding questionnaire prototype. The CEO wants an **AI agent** that
holds a model of a "complete customer profile" and **adapts its questions** to prior answers
(e.g., "10 listings → who owns them → some managed → owner details → commission model → …"),
instead of a hand-authored question tree.

The analyst built a **falsifiable PoC** to test whether AI actually beats an honest decision tree —
not on "adaptivity" (research proved an optimal adaptive questionnaire *is* a tree), but on the
things a tree provably **cannot** do: free-text/ambiguous input, combinatorial owner fan-out, and
turning unstructured **sales handover notes** into structured prefill.

Two falsifiable claims:
- **H1 (conversational):** the AI agent fills a more complete/accurate profile than an honestly-built
  tree on free-text, ambiguous, and combinatorial inputs — without breaking determinism where it matters.
- **H2 (extraction):** an LLM extracts more correct prefill (and better risk flags) from real sales
  handover notes than a regex baseline, at acceptable precision. *(Grounded in 611 real notes.)*

---

## 2. What's already decided (don't reopen unless you disagree)

| Item | Resolution |
|------|-----------|
| Hero ownership branch: write vs. capture | **Intent-capture only** — agent records owner economics + flags for the human; never writes BusinessModel records. |
| Airbnb connection | Out of the questionnaire — happens in-product (CEO direction). |
| Booking Website (S5) | In scope **conditionally** — AI surfaces it only on direct-booking signals. |
| Non-refundable scope | Per-listing/per-rate-plan. |
| Experimental rigor | Adversarially reviewed: anti-leakage baseline, dev/test split, user simulator, repeated runs, blind rating, small-N stats (bootstrap CIs, no false significance claims on N=8). |

---

## 3. Decisions I need from you

### D1 — Greenlight & framing
Is this a **funded PoC** (≈2.5–3.5 weeks of engineering + reviewer time), and is the goal a
**go/no-go on building the AI agent**, or an exploration? If funded, you'll likely want this PoC
plan promoted into a **PRD** for the build phase.

### D2 — H1 success thresholds (ratify the pre-registered decision rules)
The plan pre-registers these as *decision rules* (not powered tests):
- AI must not trail the tree by **>5 pts SAR on easy (Group A)** profiles.
- AI must show a **material, stable advantage on ambiguous/complex (Groups B+C)** — proposed
  **≥15 pp** slot-level SAR lift (with a bootstrap CI clearing zero and verdict stable across runs),
  and a qualitative win the tree structurally can't achieve.
**Do you accept 15 pp, or set a different bar?**

### D3 — H2 margin + false-prefill ceiling (set the numbers)
The extractor must beat regex on micro-F1 **and** rarely fabricate prefill on sparse/empty notes
(a fabricating extractor is worse than none — it makes the agent confirm wrong facts).
**Set: (a) the minimum F1 margin over regex, and (b) the max acceptable false-prefill rate** on the
negative/sparse strata.

### D4 — MVP completeness line (G5)
The analyst's `required` / `recommended` / `optional` tiers define when an account is "complete
enough." **Ratify these tiers, or tell me which fields truly block account creation** so the SAR
denominator reflects the real MVP.

### D5 — Kill criteria
Confirm the plan's kill conditions are acceptable as written: any false numeric write, any
inappropriate advice, or no material+stable advantage on B+C → kill/redesign.

### D6 — Resourcing
Assign owners (names) for: **Reviewer 1 + Reviewer 2 + tie-breaker** (answer-key freeze),
**data/RevOps** (full-length de-identified note pull), and the **engineer** (eval harness + extractor).

---

## 4. Read order (linked artifacts)

1. `poc-plan-ai-adaptive-onboarding-2026-06-02.md` — the experiment (claims, baseline, metrics, gates, timeline). **Primary.**
2. `guesty-pro-account-creation-schema.md` (v0.3) — the profile the agent fills; the SAR ground truth.
3. `sales-handover-notes-corpus-analysis-2026-06-02.md` — the 611-note corpus behind H2.
4. Supporting: `poc-respondent-specs-2026-06-02.md` (scored profiles), `poc-dev-profiles-2026-06-02.md` (tuning), `poc-h2-labeling-protocol-2026-06-02.md`, `poc-answer-key-review-protocol-2026-06-02.md`, `research/ai-adaptive-questionnaire-onboarding-research-2026-06-02.md`.

---

## 5. Output I'd like from you
- Decisions D1–D6 recorded (a short decision log is fine).
- If greenlit: turn the PoC plan into a **PRD** for the build phase, or tell me to.
- Any scope you want cut or added before the answer-key freeze.

> ⚠️ The handover-note corpus contains **PII** — do not commit raw notes; de-identify before labeling.
