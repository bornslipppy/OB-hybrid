---
title: "Brief for Amelia — Epic 0: Shared Kernel & Scaffold"
---

# Brief for Amelia — Epic 0: Shared Kernel & Scaffold

**Date:** 2026-06-02  
**From:** Mary (analyst)  
**For:** Amelia (dev)  
**Epic:** Epic 0 — Shared Kernel & Scaffold  
**Status:** ✅ Epic 1 (answer keys) frozen. Epic 0 is the critical-path unblock for Epics 2 and 3.

---

## What you are building

An **offline evaluation harness** that tests two falsifiable claims about AI-driven onboarding:

- **H1:** An AI adaptive agent fills a more accurate Guesty Pro onboarding profile than a deterministic decision tree.
- **H2:** An LLM extracts better prefill from unstructured sales handover notes than a regex baseline.

Epic 0 is the **neutral shared foundation** — the kernel both the AI agent (Epic 3) and the baseline decision tree (Epic 2) are built on top of. It must be frozen before Epics 2 and 3 begin acceptance.

**There is no UI.** This is a pure offline eval harness.

---

## Read these first (in order)

1. `docs/planning-artifacts/prds/prd-AI-Adaptive-Onboarding-PoC-2026-06-02/prd.md` — full PRD
2. `docs/planning-artifacts/epics.md` — Epic 0 stories (§ "Epic 0: Shared Kernel & Scaffold")
3. `docs/planning-artifacts/guesty-pro-account-creation-schema.md` — the schema (v0.3) the tools must match
4. `docs/planning-artifacts/poc-respondent-specs-2026-06-02.md` — frozen answer keys (DO NOT share with the tree author)

---

## Epic 0 deliverables (two stories)

### Story 0.1 — Shared neutral kernel

Build and export:

1. **7-tool contract** — exact function signatures for: `record_answer`, `add_fee`, `add_tax`, `add_owner`, `skip_question`, `flag_for_call_1`, `end_section`. Schema-validated argument shapes (no extra or missing fields).
2. **`ProfileState` reducer** — pure; all state transitions go through the kernel; no direct field mutation anywhere.
3. **Trace event schema** — each event emits: `tool`, `slot`, `value_introduced`, `echo_issued`, `user_confirmed`. Must be machine-readable (JSON per turn).
4. **`System` protocol** — per-turn input/output shapes for both the agent and the tree client (they share the same interface).
5. **Dual-provider LLM client** — two call modes only:
   - `scored_completion` → temperature **locked to 0.0** (all tool-call-emitting turns)
   - `glue_completion` → temperature **0.2** (conversational transitions only)
   - Temperature enforcement is structural — no call site can override it. A wrong temperature is a startup error.

### Story 0.2 — Project scaffold

1. **Directory layout:** `kernel/`, `profiles/`, `runs/`, `reports/`
2. **Pinned lockfile** — all dependency versions pinned; lockfile is part of the freeze manifest.
3. **`run-config.toml`** — specifies: agent provider/model, simulator provider/model, temperature policy, `k` (number of runs, default 5), seed strategy, freeze-manifest path. Validated on load — wrong temperature on any scored-slot path = startup error.
4. **CI PII commit-guard** — blocks any commit touching `profiles/raw/` or matching a configurable PII filename pattern. Must be active before any note-pull work begins.

---

## Runtime / API key

- **SDK:** Cursor SDK (Python: `cursor-sdk` or TypeScript: `@cursor/sdk`)
- **Key:** `CURSOR_API_KEY` — stored in `.env` at repo root (already gitignored). Load with `python-dotenv` or `dotenv`.
- **Model:** `composer-2.5` or `auto` — do not hardcode unusual model IDs.
- **No separate Anthropic/OpenAI key needed** — Cursor subscription covers the underlying models.

```python
import os
from dotenv import load_dotenv
from cursor_sdk import Agent, AgentOptions, LocalAgentOptions

load_dotenv()
api_key = os.environ["CURSOR_API_KEY"]
```

---

## Key constraints

- The kernel is authored by you (neutral harness engineer) — **not** the Epic 2 tree author or the Epic 3 agent-prompt author (FR-10). Keep these roles separate.
- The `ProfileState` reducer must enforce echo-before-write structurally (PRD §8, NFR-2) — no call site can record a value without first issuing an echo.
- PII guard must block `profiles/raw/` before any handover-note work starts (NFR-3).
- Freeze the kernel (version-tag + freeze manifest entry) before Epic 2 or Epic 3 acceptance begins (NFR-4).

---

## Definition of done

- [ ] 7 tools exported with schema-validated argument shapes
- [ ] `ProfileState` pure reducer, no direct mutation
- [ ] Trace events emit `value_introduced`, `echo_issued`, `user_confirmed`
- [ ] `System` protocol defines per-turn I/O for both agent and tree
- [ ] `scored_completion` (0.0) and `glue_completion` (0.2) enforced structurally
- [ ] Scaffold directories created
- [ ] Lockfile pinned
- [ ] `run-config.toml` validated on load
- [ ] CI PII guard blocks `profiles/raw/`
- [ ] Kernel version-tagged in freeze manifest

---

## Companion documents

| Document | Purpose |
|----------|---------|
| `epics.md` | Full story acceptance criteria |
| `prd.md` | PRD — §3 (tool surface), §4 (LLM client), §8 (invariants), §9 (PII) |
| `guesty-pro-account-creation-schema.md` | Schema v0.3 — tool argument shapes must match |
| `poc-respondent-specs-2026-06-02.md` | Frozen answer keys — kernel must support these dispositions |
