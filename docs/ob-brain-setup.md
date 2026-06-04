---
title: "ob-brain — Clone & Run"
description: "Quick setup for the private ob-brain repo: env, demo, optional batch eval."
---

# ob-brain — Clone & Run

Private repo: [github.com/bornslipppy/ob-brain](https://github.com/bornslipppy/ob-brain)

This bundle includes the PoC eval harness, frozen **campaigns/**, scored profiles, and the Tamar sales-notes workbook (PII — keep the repo private).

---

## 1. Clone

```bash
git clone https://github.com/bornslipppy/ob-brain.git
cd ob-brain
```

## 2. API keys (local only)

```bash
cp .env.example .env
```

Edit `.env` at the **repo root** and add your keys. **Never commit `.env`.**

| Variable | Demo (Streamlit) | Batch eval |
|----------|------------------|------------|
| `GEMINI_API_KEY` | ✅ (with Gemini `CURSOR_BASE_URL`) | ✅ agent + simulator |
| `CURSOR_BASE_URL` | ✅ see `.env.example` | optional |
| `CURSOR_API_KEY` | if using Cursor bridge | optional |
| `ANTHROPIC_API_KEY` | if using direct Anthropic | optional |

Details: `poc-eval-harness/README.md`.

## 3. Install & run the stakeholder demo

```bash
cd poc-eval-harness
uv sync --extra demo
uv run streamlit run harness/demo_app.py
```

Open the app at [http://localhost:8501](http://localhost:8501).

1. Sales notes load from `poc-eval-harness/data/Notes-for-Tamar-2026-06-02.xlsx` (included in this repo).
2. Search for an account (e.g. **City and Coastal**).
3. Click **Start session** — the agent reads Salesforce + the handover note and tailors opening copy and question order to that account (see `docs/planning-artifacts/guesty-pro-account-creation-schema-stakeholder-summary.md` § Tailored onboarding).

Optional override:

```bash
export SALES_NOTES_XLSX="$(pwd)/data/Notes-for-Tamar-2026-06-02.xlsx"
```

## 4. Interactive CLI (synthetic profile, no xlsx)

```bash
cd poc-eval-harness
uv sync
uv run python -m harness.interactive --system agent --profile A1
```

## 5. Batch eval (optional)

Uses existing **campaigns/** for reference; new runs need API keys and spend:

```bash
cd poc-eval-harness
uv run python -m harness --dry-run
uv run python -m harness
```

## Security reminders

- **Do not** make this repo public — it contains real Salesforce handover notes (PII).
- **Do not** commit `.env` or paste keys into issues/PRs.
- Rotate keys if they were ever exposed outside your machine.

## More context

- **Agent handoff (for other AIs):** [agent-handoff.md](agent-handoff.md)
- **Gap report:** [ob-brain-gap-report.md](ob-brain-gap-report.md)
- PoC build guide: `docs/planning-artifacts/poc-eval-harness-build-guide.md`
- Schema stakeholder summary: `docs/planning-artifacts/guesty-pro-account-creation-schema-stakeholder-summary.md`
