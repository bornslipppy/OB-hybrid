---
title: "OB-V2 × Brain — Feasibility Report"
author: "Winston (System Architect)"
date: 2026-06-04
audience: "Yair Cohen"
status: draft
related:
  - docs/planning-artifacts/ob-v2-brain-merge-architecture-report-2026-06-04.md
  - docs/agent-handoff.md
  - docs/planning-artifacts/research/ai-adaptive-questionnaire-onboarding-research-2026-06-02.md
---

# OB-V2 × Brain — Feasibility Report

**Question:** Can we deliver the same rule-based questionnaire experience, plugged into a schema and LLM, with adaptive flow, a personal intro, and personalized UX copy per account — while keeping hard technical inputs (e.g. tax percentages) fixed?

**Answer:** **Yes — feasible**, with a hybrid architecture and phased scope. This report maps expectations to implementation and validates the three cases where AI earns its place over a decision tree.

---

## 1. Executive summary

You are not asking for a different product. You are asking for:

**OB-V2 wizard UX + schema-backed brain as orchestration**, with AI only where the tree breaks.

| Expectation | Feasible? | How |
|-------------|-----------|-----|
| Same rule-based questionnaire UX (screens, Continue, canvas, review) | **Yes** | Keep OB-V2 shell; do not replace with chat |
| Plugged into a schema | **Yes** | Schema = contract for what must be collected; wizard uses `answers` at runtime; map screen IDs ↔ schema field IDs |
| LLM in the loop | **Yes, hybrid** | LLM for policy, copy, normalization — not for tax % widgets or silent production writes |
| Adaptive flow | **Yes, layered** | `showIf` = hard branches; planner = soft order + capture path selection |
| Personal intro + personalized copy per account | **Yes** | Context engine (SF + note) + template/LLM copy on welcome and screen headers |
| Hard inputs stay fixed (tax %, fee amounts, splits) | **Yes — should** | Structured widgets + echo-before-write (PoC invariants) |
| Flexibility around the questionnaire | **Yes** | Order, intro, copy, defer sections, free-text capture → structured `answers` |

**Scope risk:** Expecting AI to replace fixed financial widgets or invent new UI without authored templates. Keeping hard inputs fixed while flexing intro, order, copy, and NL capture paths is the viable product.

---

## 2. What “adaptive” means (tree vs AI)

A well-built decision tree already adapts which questions appear (`showIf` in OB-V2). That is **not uniquely AI**.

**What a tree cannot do well** (and why AI earns its place):

1. **Free text → structure** — e.g. “we split it after Airbnb takes their cut” without forcing a dropdown first.
2. **Fan-out without pre-authoring every branch** — e.g. four owners with four different deal structures.
3. **Sales handover note → quiet prefill** — e.g. “nervous about financials, wants locks, coming off Hostaway” → confirm instead of cold-ask.

The PoC validates these three before building for production. The wizard merge implements them **inside** the same screen-based UX, not as a separate chat product.

---

## 3. Feasibility — the three AI cases

### 3.1 Free text → structured

**Verdict: Feasible** (high value, medium risk)

| Layer | Approach |
|-------|----------|
| UX | One screen at a time; **capture** step (textarea) where dropdowns feel wrong; **confirm** chip before commit |
| Logic | LLM or rules + LLM fallback **normalize** to schema enums / `answers` keys |
| Guardrail | Low confidence → route to existing structured screen, do not guess |

PoC pattern: tools + `record_answer`. Wizard pattern: `answers` + review panel. Same idea, different write API.

---

### 3.2 Multi-owner fan-out (4 owners, 4 deal structures)

**Verdict: Feasible within bounded UI** (not infinite dynamic screens)

| Limit | Reality |
|-------|---------|
| Tree | Requires pre-authored screen templates (owner card, split type, mixed split) — OB-V2 already has owner/split branching |
| AI role | How many owners, which template per owner, order of owner screens, parse messy text into owner-shaped data |
| v1 | Cap at N owners with **repeat pattern**; LLM fills slots inside that pattern |

**Not feasible as stated if interpreted as:** “zero authored UI, AI invents every branch.”  
**Feasible as:** “AI orchestrates repeat templates and normalizes messy owner economics.”

---

### 3.3 Sales handover note → prefill + confirm

**Verdict: Feasible — easiest win**

| Step | Implementation |
|------|----------------|
| Extract | Deterministic keywords (`account_context.py`) for v1; optional LLM for messy notes (PoC H2) |
| Wizard | Seed `answers`, `SourceChip`, welcome/handover recap; first screens = “Looks right?” |
| AI depth | Does **not** require full conversational AI — needs **context at init** + copy/planner |

Matches **personal intro** and **personalized UX copy** expectations directly.

---

## 4. Target architecture

```text
┌─────────────────────────────────────────────────────────┐
│  Schema (what “complete profile” means)                 │
│  - field ids, enums, depends_on, echo_before_write      │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│  Planner (LLM + rules)                                  │
│  - next eligible screen / capture mode                  │
│  - personalized copy                                    │
│  - defer_section, priority                              │
└────────────────────┬────────────────────────────────────┘
                     │ only eligible screens
┌────────────────────▼────────────────────────────────────┐
│  OB-V2 wizard (fixed widgets for hard fields)           │
│  showIf ∩ planner order ∩ copy overrides                │
└─────────────────────────────────────────────────────────┘
```

| Component | Role |
|-----------|------|
| **Schema** | Source of truth for completeness and evaluation |
| **LLM** | Planner + normalizer + copy — **not** tax percentage input |
| **Questionnaire** | What the user sees; `answers` = runtime state |

**Invariant:** `showIf` stays the safety gate. Planner never bypasses compliance or OAuth/financial branch rules.

---

## 5. PoC vs production

| PoC validates | Production still needs |
|---------------|------------------------|
| Note → prefill + confirm beats cold-ask | Real Salesforce + notes API at wizard init |
| NL → slot on conversational paths | Capture + confirm UI on wizard (not chat-only) |
| Owner/complex branch policy vs tree (SAR) | Repeatable owner UI + normalizer into `answers` |
| Same schema, two policies (agent vs tree) | Screen registry + planner service |
| Financial echo / no unsafe writes | Keep fixed tax/fee builders unchanged |

The PoC is **sufficient to justify building** the hybrid for real, scoped as **wizard UX + schema-backed planner**, not “replace every dropdown with chat.”

---

## 6. Recommended v1 scope

| Phase | Deliverable |
|-------|-------------|
| **P0** | Note + SF context → personal intro, seeded answers, confirm-first screens |
| **P1** | Rule-based (+ optional LLM) screen priority among `showIf`-eligible steps; defer financials when note signals anxiety |
| **P2** | Personalized `title` / `help` / BotAlert lines per account |
| **P3** | 3–5 capture screens (payment description, pain, handover correction) → normalize → confirm → `answers` |
| **P4** | Owner fan-out assist inside existing owner UI patterns |

**Explicitly out of v1:**

- LLM editing tax % fields directly
- Skipping structured financial widgets
- Unbounded dynamic screens without templates

---

## 7. Conclusion

| Statement | Assessment |
|-----------|------------|
| Same rule-based questionnaire + schema + LLM | **Feasible** |
| Adaptive flow + personal intro + personalized copy | **Feasible** |
| Hard technical inputs stay fixed | **Required for safety and UX** |
| Three AI differentiators (free text, owner fan-out, sales notes) | **Feasible** with hybrid planner + bounded UI |
| Tree handles branching; AI handles wording, order, NL, note seeding | **Correct product split** |

Implementation shape: **planner on top, wizard underneath** (see merge architecture report).

---

## 8. Related documents

- [OB-V2 × Brain Merge — Architecture Report](./ob-v2-brain-merge-architecture-report-2026-06-04.md)
- [Agent handoff — ob-brain](../agent-handoff.md)
- [AI adaptive questionnaire research](./research/ai-adaptive-questionnaire-onboarding-research-2026-06-02.md)

---

*Generated 2026-06-04 — architecture feasibility session.*
