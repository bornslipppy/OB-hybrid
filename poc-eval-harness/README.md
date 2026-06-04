# PoC Eval Harness

Offline, file-based eval harness for the AI Adaptive Onboarding PoC (H1 + H2).
See [architecture.md](../docs/planning-artifacts/architecture.md) and
[build guide](../docs/planning-artifacts/poc-eval-harness-build-guide.md).

## Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (`curl -LsSf https://astral.sh/uv/install.sh | sh`)

## Environment setup

API keys and local data paths live in a **gitignored** `.env` at the **repo root**
(`BMAD-METHOD/.env`), not inside this folder.

```bash
# From the repository root (BMAD-METHOD/)
cp .env.example .env
# Edit .env — add your keys only on your machine; never commit .env
```

| Variable | Required for | Notes |
|----------|----------------|-------|
| `GEMINI_API_KEY` | Agent (Gemini path), simulator | Used when `CURSOR_BASE_URL` points at `generativelanguage.googleapis.com` |
| `CURSOR_BASE_URL` | Agent (OpenAI-compat path) | Gemini demo: `https://generativelanguage.googleapis.com/v1beta/openai/` |
| `CURSOR_API_KEY` | Agent (Cursor/proxy path) | Alternative to Gemini; set `CURSOR_BASE_URL` to your bridge |
| `ANTHROPIC_API_KEY` | Agent (direct Anthropic) | Omit `CURSOR_BASE_URL` to use native Anthropic SDK |
| `SALES_NOTES_XLSX` | Streamlit demo (real accounts) | **PII** — absolute path to Tamar export; never commit the file |

**Handover notes (PII):** Private **ob-brain** includes `data/Notes-for-Tamar-2026-06-02.xlsx` (auto-detected by the demo). Do not make the repo public. Override with `SALES_NOTES_XLSX` if needed.

**Campaign outputs:** `poc-eval-harness/campaigns/` holds frozen eval manifests, run records, and traces (tracked on private **ob-brain**). Re-run `uv run python -m harness` to add new campaigns locally.

Install Python deps:

```bash
cd poc-eval-harness
uv sync
# Streamlit demo also needs:
uv sync --extra demo
```

## Interactive CLI

Play the customer in a live session (same loop as eval, no simulator LLM):

```bash
cd poc-eval-harness
uv run python -m harness.interactive --system agent --profile A1
uv run python -m harness.interactive --system tree --profile A1
```

## Stakeholder demo (Streamlit)

Real-account mode: load the Tamar Salesforce export and let the agent **confirm from the sales note** instead of cold questions.

```bash
cd poc-eval-harness
uv sync --extra demo
uv run streamlit run harness/demo_app.py
```

1. Sales notes load from `data/Notes-for-Tamar-2026-06-02.xlsx` when present (or set path in sidebar / `SALES_NOTES_XLSX`)
2. Search for an account (e.g. **City and Coastal**)
3. Expand **Handover note** to verify the export row
4. **Start session** — the agent opens with note-aware confirmations

Without a workbook path, the demo falls back to synthetic scored profiles (A1, B1, …).

## Batch eval (campaign runner)

```bash
cd poc-eval-harness
uv run python -m harness --dry-run    # validate freeze manifest, no API calls
uv run python -m harness              # agent + tree vs scored profiles
```

Requires agent + simulator keys per `.env.example`. See `config/run_config.toml` for models and `k` runs.

## Scored profiles

Frozen respondent specs and answer keys: `profiles/scored/A1.json` … `C2.json`.
Stakeholder-friendly overview: [schema stakeholder summary](../docs/planning-artifacts/guesty-pro-account-creation-schema-stakeholder-summary.md).
