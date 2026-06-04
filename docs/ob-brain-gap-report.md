---
title: "ob-brain — What’s in the repo vs what’s missing"
description: "Gap analysis for private ob-brain clones: demo, H1 eval, H2, and out-of-scope items."
date: 2026-06-04
repo: https://github.com/bornslipppy/ob-brain
related:
  - docs/ob-brain-setup.md
  - docs/planning-artifacts/poc-eval-harness-build-guide.md
---

# ob-brain — Repository gap report

This report lists what **is** bundled in the private [ob-brain](https://github.com/bornslipppy/ob-brain) repository and what is **still missing** on a fresh clone — aside from API keys (`.env`), which are intentionally never committed.

For setup steps, see [ob-brain-setup.md](ob-brain-setup.md).

---

## Executive summary

| Goal | Ready after clone? | Main gaps |
|------|------------------|-----------|
| **Stakeholder demo** (Streamlit + Tamar) | Almost — add keys + `uv` | `.env`, local toolchain |
| **Full H1 eval** (agent vs tree, SAR, verdict) | Partial | Incomplete agent campaigns, no H1 report, no human rater files |
| **H2** (note extraction eval) | No | H2 is a stub; no gold corpus or runs |
| **Production Guesty onboarding** | No | Out of PoC scope |

---

## What is already in ob-brain

| Asset | Location | Purpose |
|-------|----------|---------|
| PoC harness (agent, tree, kernel, scoring) | `poc-eval-harness/` | Conversation loop, tools, SAR |
| Eight frozen scored profiles | `poc-eval-harness/profiles/scored/A1.json` … `C2.json` | Synthetic respondents + answer keys |
| Tamar sales-notes export | `poc-eval-harness/data/Notes-for-Tamar-2026-06-02.xlsx` | Real-account demo (PII — private repo only) |
| Campaign run artifacts | `poc-eval-harness/campaigns/` | Manifests, run records, traces (partial agent coverage) |
| Env template | `.env.example` | Key names and provider options |
| Planning docs | `docs/planning-artifacts/` | Schema, build guide, stakeholder summary |
| Setup guide | `docs/ob-brain-setup.md` | Clone → env → demo |

---

## 1. Stakeholder demo (Streamlit + Tamar accounts)

### Missing

| Item | Notes |
|------|--------|
| **`.env` with real keys** | Copy from `.env.example`; never in git |
| **`uv` + Python 3.12** | Install on the machine |
| **Local `.venv`** | Created by `uv sync --extra demo` |

### Already sufficient

- Harness code, demo app, sales-notes loader
- Tamar workbook under `data/`
- Scored profiles for synthetic fallback (A1, B1, …)

### Minimum path

```bash
git clone https://github.com/bornslipppy/ob-brain.git
cd ob-brain
cp .env.example .env   # add keys
cd poc-eval-harness && uv sync --extra demo
uv run streamlit run harness/demo_app.py
```

---

## 2. Full H1 eval (agent vs tree, SAR, verdict)

### Missing

| Item | Notes |
|------|--------|
| **API keys** | Agent + simulator (Gemini family per `poc-eval-harness/config/run_config.toml`) |
| **Complete agent campaigns** | Stored campaigns skew **tree-heavy** (~566 tree-related artifacts vs ~113 agent-related). Agent head-to-head is **not** fully frozen in git |
| **H1 verdict report** | `poc-eval-harness/reports/` is empty — no generated markdown verdict checked in |
| **Human rater artifacts** | No `rater_tasks.jsonl` / `rater_ratings.jsonl` — free-text slots (`pain`, verbal ownership, etc.) need blind ratings for final SAR (FR-35) |
| **Dev tuning profiles** | `profiles/dev_dir` is configured but **no `profiles/dev/*.json`** files exist |
| **New eval runs** | Re-running `uv run python -m harness` requires keys, time, and API spend |

### Already sufficient

- Schema, 8 scored profiles + answer keys, tree + agent code, scoring engine
- Partial campaign history for analysis or resume
- Freeze discipline code (`harness/freeze.py`, manifest hashing)

### Implication

You can **inspect** tree-heavy frozen runs and **re-run** evals with keys, but you **cannot** reproduce a complete, signed-off H1 verdict from the repo alone.

---

## 3. H2 (sales-note extraction eval)

### Missing (almost everything)

| Item | Notes |
|------|--------|
| **H2 implementation** | `poc-eval-harness/h2/` is a stub (`__init__.py` + guarded `data/`) |
| **De-identified gold corpus** | `h2/data/raw/`, labels, dev/test split — blocked for PII (NFR-3) |
| **Extractor vs regex baseline runs** | Not bundled like H1 `campaigns/` |

### Note on Tamar xlsx in repo

The **full** Tamar export in `data/` supports the **stakeholder demo** (confirm-from-note UX). It is **not** the de-identified, labeled set required for the H2 precision/recall eval.

---

## 4. Production / live product (out of scope)

These were never part of the PoC bundle:

- Live Guesty or Salesforce API integration
- Post-questionnaire starter-kit auto-setup in the product
- Hosted, shareable demo URL with auth
- Locked executive sign-off tied to a final `reports/` artifact

---

## 5. Optional / hygiene (not blockers)

| Item | Notes |
|------|--------|
| **Repo shape** | ob-brain contains the full **BMAD-METHOD** tree (skills, website, etc.), not a minimal onboarding-only package |
| **Upstream sync** | ob-brain may diverge from `bmad-code-org/BMAD-METHOD` on `origin` |
| **Cursor CLI** | Only required if using the Cursor API bridge instead of Gemini `CURSOR_BASE_URL` |

---

## Post-clone checklist

```text
IN REPO
  ✅  docs/ob-brain-setup.md
  ✅  docs/ob-brain-gap-report.md (this file)
  ✅  .env.example
  ✅  poc-eval-harness/ (code + schema)
  ✅  profiles/scored/A1–C2.json
  ✅  data/Notes-for-Tamar-2026-06-02.xlsx
  ✅  campaigns/ (partial eval history)

YOU PROVIDE
  ❌  .env with API keys
  ❌  uv + Python 3.12
  ❌  (For full H1) complete agent runs + human ratings + generated report
  ❌  (For H2) corpus, labels, and H2 pipeline — not in repo
```

---

## Recommendations

1. **Demo handoff** — Share ob-brain access + `.env.example`; each user adds keys locally. Point to `docs/ob-brain-setup.md`.
2. **Eval handoff** — Document which campaign hash is the “canonical” freeze and finish agent `k=5` runs before claiming H1 numbers.
3. **Verdict** — Run the scoring/report pipeline and commit or attach the H1 markdown under `reports/` (or store in a private artifact store).
4. **H2** — Treat as a separate deliverable; do not assume ob-brain includes it.
5. **PII** — Keep the repo **private**; do not fork publicly while Tamar xlsx is tracked.

---

## Related documents

- Setup: [ob-brain-setup.md](ob-brain-setup.md)
- How the harness works: `docs/planning-artifacts/poc-eval-harness-build-guide.md`
- Profile topics (plain language): `docs/planning-artifacts/guesty-pro-account-creation-schema-stakeholder-summary.md`
- PoC claims and metrics: `docs/planning-artifacts/poc-plan-ai-adaptive-onboarding-2026-06-02.md`
