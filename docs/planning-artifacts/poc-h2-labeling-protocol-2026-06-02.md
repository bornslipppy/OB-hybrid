---
title: "H2 Labeling Protocol — Sales Handover Note → Prefill Extraction"
author: "Mary (Business Analyst)"
date: 2026-06-02
version: 1.0
status: draft — ready for data + labeling owners
purpose: "Procedure to (a) pull full-length, de-identified handover notes from Salesforce, (b) build a stratified gold-labeled set, and (c) score the LLM extractor vs. a regex baseline for PoC Claim H2 / Component 6."
companions:
  - "poc-plan-ai-adaptive-onboarding-2026-06-02.md §7 Component 6"
  - "sales-handover-notes-corpus-analysis-2026-06-02.md"
  - "guesty-pro-account-creation-schema.md v0.3 §S0b"
---

# H2 Labeling Protocol — Note → Prefill Extraction

Claim H2: *an LLM extractor fills more correct prefill slots — and flags more legitimate risks —
than a rules/regex baseline, at acceptable precision.* This protocol produces the gold set and the
scoring procedure that make that claim falsifiable.

---

## Phase 0 — Full-length, de-identified data pull

> **Why.** The `Notes for Tamar` export truncates the Notes field at **255 chars**. Labeling and
> extraction must run on **full** note text, or we measure the truncation artifact, not the model.

### 0.1 Pull (data/RevOps owner)
- Source: the same Salesforce report (Closed-Won · current FQ · Onboarding preference), but export
  the **long-text Notes field untruncated**. Options, in order of preference:
  1. **Report → export with the full rich-text field** (remove any 255-char preview formatting), or
  2. **Reports/Analytics API** or **SOQL** on the Opportunity/Account object pulling the note field
     directly (`SELECT Account.Name, Number_of_Listings__c, Notes__c FROM Opportunity WHERE …`).
- Capture columns: `account_id` (opaque), `note_full`, `listing_count`, `close_date`. Drop rep name
  unless needed (it is not a label input).
- Expected: ~643 rows, ~611 substantive (matches the truncated export's row count as a sanity check).

### 0.2 De-identify (before anyone labels)
Apply a deterministic scrub and store the mapping **separately, access-controlled**:

| PII | Action |
|-----|--------|
| Person names | Replace with `[PERSON_n]` (stable per note) |
| Emails | Replace with `[EMAIL_n]` |
| Phone numbers | `[PHONE_n]` |
| URLs / domains | `[URL_n]` (keep TLD if it signals a direct site, e.g. `[URL_n:.com]`) |
| Company names | `[ORG_n]` only if a person's surname; keep generic brand words |
| Hard $ deal terms | Keep amounts (signal), drop contract IDs |

- Scrubbing is **automated + spot-checked** (10% manual review) before distribution.
- **Governance:** the un-scrubbed pull never leaves the controlled store; only the scrubbed set is
  labeled. Do **not** commit either to the repo (PoC plan §11 risk row).

### 0.3 Output
`notes_deid.jsonl` — one row per note: `{ "id", "note_deid", "listing_count", "len" }`.

---

## Phase 1 — Stratified sampling

Target **50 notes** (within the §6 "40–60" band), stratified to guarantee archetype + difficulty
coverage rather than a random draw dominated by short/common notes.

| Stratum (corpus archetype) | Target n | Selection rule |
|----------------------------|----------|----------------|
| A — migration + add-on | 10 | notes naming a prior PMS + an add-on |
| B — managed-for-owners | 9 | ownership/management/conciergerie signal |
| C — sentiment / risk | 7 | sentiment cue present (worried, mandatory, opt-out…) |
| D — language / pacing | 6 | non-English OB or pacing/guidance signal |
| E — payment / term fuzziness | 6 | payment-processing or fuzzy-economics signal |
| F — sparse | 6 | length < 60 chars but non-empty |
| **Negative** — `NA`/blank | 6 | from the 32 `NA` rows (abstention test) |

- Sample **within** each stratum at random (seeded) for reproducibility.
- **Dev/test split (anti-leakage, mirrors plan §5.1):** 20 notes → **dev** (prompt tuning), 30 →
  **test** (frozen, scored once). Stratify the split so each archetype appears in both. The
  extractor prompt is **never** iterated against the test 30.

---

## Phase 2 — Gold label schema

Label each note into the S0b target. A slot is labeled **only if the note states or strongly implies
it**; otherwise it is `absent` (critical for the abstention/false-prefill metric).

```jsonc
{
  "id": "note_0173",
  "split": "test",
  "labels": {
    "migration_source":      { "value": "hostaway", "provenance": "coming off hostaway" },
    "prior_pms_experience":  { "value": "experienced", "provenance": "..." },
    "ob_language":           { "value": "fr", "provenance": "OB en français" },
    "tech_level":            { "value": "absent" },
    "addon_intent":          { "value": ["accounting","locks"], "provenance": "..." },
    "ownership_model_hint":  { "value": "managed", "provenance": "manages for owners" },
    "channels":              { "value": ["airbnb","booking"], "provenance": "..." },
    "direct_website_signal": { "value": true, "provenance": "own site" },
    "customer_sentiment":    { "value": "anxious", "provenance": "very worried about OB" },
    "risk_flags":            { "value": ["mandatory_dp"], "provenance": "DP mandatory on all res" }
  }
}
```

### Per-slot labeling rules (the contentious ones)
- **`migration_source`** — label the *named* prior system; `none` only if note says first-time/manual; `absent` if unmentioned.
- **`ownership_model_hint`** — `managed`/`mixed`/`self_owned` only on explicit signal ("on behalf of," "own units," "co-owner of managed"); otherwise `absent`. (This is a *hint* for the hero branch, not the final value.)
- **`addon_intent`** — multi-label; include only add-ons named or clearly bundled. "Mandatory DP" → both `damage_protection` here **and** `mandatory_dp` in `risk_flags`.
- **`customer_sentiment`** / **`risk_flags`** — label conservatively; require a textual cue. These are brief-only signals, so **precision matters more than recall** (a false "at_risk" misleads Jordan).
- **`tech_level`** — only on explicit cue ("tech savvy," "not technical"); else `absent`.
- **Negatives** — `NA`/blank notes: every slot is `absent`. Any predicted value here is a false-prefill.

### Provenance
Every non-absent label carries the **quoted span** that justifies it. This doubles as the rubric for
the extractor's required `provenance` output and as evidence during adjudication.

---

## Phase 3 — Two-rater labeling + adjudication

- **Two raters** label all 50 independently (reuse the answer-key raters where possible for consistency).
- **Inter-rater reliability:** report **Cohen's κ per slot** (treat multi-label slots as set agreement / Jaccard). Flag any slot with κ < 0.6 for guideline refinement before scoring.
- **Tie-breaker:** a third rater adjudicates disagreements; the adjudicated label is gold.
- **Contested labels** that survive adjudication as genuinely ambiguous are marked and reported as a
  **sensitivity band** (consistent with PoC plan §6.1) — not silently dropped.

---

## Phase 4 — Systems under test

- **Extractor (AI):** system-prompted LLM emitting the Phase-2 JSON with `confidence ∈ [0,1]` +
  `provenance` per slot. Prompt tuned **only on the dev 20**. Run on the test 30 (k≥3 for variance).
- **Baseline (regex):** the honest keyword/regex extractor used to build the corpus frequencies
  (signal taxonomy in the corpus-analysis doc). It is the "what rules get you" floor.

---

## Phase 5 — Metrics (pre-registered)

| Metric | Definition | Why |
|--------|-----------|-----|
| **Micro-F1** | Over all slot-label decisions, extractor vs. regex | Headline H2 comparison |
| **Per-slot P/R/F1** | Each S0b field | Shows *where* AI wins (free-text vs. keyworded) |
| **Risk-flag quality** | Precision (raised flags that are gold) + recall vs. gold; blind multi-rater on disputed | Flags drive Jordan's prep; precision-weighted |
| **False-prefill rate** | Predicted non-absent on a gold-`absent` slot (esp. negatives/sparse) | A fabricating extractor is **worse than none** |
| **Confidence calibration** | Reliability curve: do high-confidence slots have higher accuracy? | Justifies the confirm-don't-assume threshold |
| **Coverage lift** | (extractor correct slots − regex correct slots) / total gold | The practical "how much more does AI prefill" |

### Decision rule (pre-registered, set the margin with PM)
> H2 is **supported** if the extractor beats regex on **micro-F1 by a clear margin** *and* keeps
> **false-prefill rate** at or below a low pre-set ceiling on the negative/sparse strata. A high-F1
> extractor that fabricates prefill on sparse notes **fails** H2 — confirming wrong facts is a
> regression, not a feature. Margin/ceiling phrased as decision rules, not powered tests (plan §6.2).

---

## Phase 6 — Outputs
- `h2_gold.jsonl` (adjudicated labels, test split frozen)
- `h2_report.md` — the metric table above, per-slot breakdown, calibration curve, contested band,
  and a qualitative "what regex structurally missed" section (the core H2 evidence).

---

## Owners & open items
| Item | Owner |
|------|-------|
| Full-length pull + de-identification | Data / RevOps |
| Sampling + split freeze | Mary |
| Labeling guidelines + κ + adjudication | Mary + 2 raters + tie-breaker |
| Extractor + regex build, scoring harness | Engineer (Component 6) |
| Margin / false-prefill ceiling sign-off | PM |
