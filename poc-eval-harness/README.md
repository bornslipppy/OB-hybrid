# PoC Eval Harness

Offline, file-based eval harness for the AI Adaptive Onboarding PoC (H1 + H2).
See ../docs/planning-artifacts/architecture.md.

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
# Add to .env (file is gitignored — do NOT commit the xlsx; it contains PII):
# SALES_NOTES_XLSX=/path/to/Notes for Tamar-2026-06-02-13-51-50 (1).xlsx

uv sync --extra demo
uv run streamlit run harness/demo_app.py
```

1. Search for an account (e.g. **City and Coastal**)
2. Expand **Handover note** to verify the export row
3. **Start session** — the agent opens with note-aware confirmations

Without `SALES_NOTES_XLSX`, the demo falls back to synthetic profiles (A1, B1, …).

Uses the same `.env` API keys as batch runs (`GEMINI_API_KEY`, OpenAI-compat `CURSOR_BASE_URL`).
