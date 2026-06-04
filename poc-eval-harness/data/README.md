# Sales handover notes (Tamar export)

**PII:** This workbook contains real Salesforce contact and deal data. It is stored in the **private** `ob-brain` repository for demo reproducibility only. Do not fork publicly or share outside Guesty.

| File | Purpose |
|------|---------|
| `Notes-for-Tamar-2026-06-02.xlsx` | Salesforce “Notes for Tamar” export (~611 accounts) |

The Streamlit demo and `harness/sales_notes.py` auto-detect this path when present. Override with:

```bash
export SALES_NOTES_XLSX="$(pwd)/data/Notes-for-Tamar-2026-06-02.xlsx"
```
