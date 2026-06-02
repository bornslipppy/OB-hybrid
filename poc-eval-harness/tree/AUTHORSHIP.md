# AUTHORSHIP.md — Honest Baseline Tree (Epic 2)

## Purpose

This file is the **independent authorship record** for `tree/tree.py`, required by
Story 2.5 / FR-10.  It establishes a verifiable record that the tree was authored
without access to the test profiles.

---

## Authoring Session

| Field | Value |
|-------|-------|
| Session | Cursor agent session — transcript at `/agent-transcripts/471303f8-700a-4286-a2b1-0afea8e9518a` |
| Author (AI) | Amelia (BMAD `bmad-agent-dev` persona, Senior Software Engineer) |
| Human collaborator | Yair Cohen (product owner — provided schema, architecture, PRD, and epics only) |
| Date | 2026-06-02 |
| Kernel version | `kernel-v1` (frozen) |
| Schema version | `guesty-pro-account-creation-schema.md` v0.3 (file as-of session start) |

---

## Blind-Authoring Attestation (FR-10 / Story 2.5)

The author attests:

1. **No profile exposure.**  `profiles/scored/` was never read, listed, or referenced
   during this session.  The constraint "it does not exist as far as you are concerned"
   was acknowledged at the start of the Epic 2 prompt and honoured throughout.

2. **Sources used.**  The tree was authored exclusively from:
   - `docs/planning-artifacts/guesty-pro-account-creation-schema.md` — all branching
     logic, `depends_on` guards, `echo_before_write` flags, `human_handoff` rules
   - `docs/planning-artifacts/architecture.md` — kernel contract, 7-tool vocabulary,
     `System` protocol, trace event schema
   - `docs/planning-artifacts/prds/prd-AI-Adaptive-Onboarding-PoC-2026-06-02/prd.md`
     — functional requirements, kill criteria, invariants
   - `docs/planning-artifacts/epics.md` — Story acceptance criteria (FRs 7–13b)
   - `poc-eval-harness/kernel/` module source — tools, state, trace, schema, protocol

3. **NLU vocabulary.** The synonym maps in `tree.py` were authored by reading
   `guesty-pro-account-creation-schema.md §10` and applying standard property-management
   industry vocabulary.  No corpus of test-profile utterances was consulted.

4. **No reverse-engineering of scoring rubric.**  The capability ledger (§1–§3) lists
   structural properties of the tree; no inference about which test profiles would
   "hit" which branches was made.

---

## What This Enables (FR-10)

This session record satisfies the PoC's **anti-leakage guard**:

> *"The tree must be authored blind to test profiles so the comparison between agent
> and tree isolates AI adaptive capability rather than test-set memorization."*
>                                         — Architecture §3.2 / Epic 2 preamble

An independent reviewer can verify blind authorship by inspecting the session
transcript (above) and confirming no `profiles/scored/` file was read.

---

## Files Produced in This Session

| File | Description |
|------|-------------|
| `tree/tree.py` | `TreeSystem(System)` — the full deterministic policy |
| `tree/__init__.py` | Package export for `TreeSystem` |
| `tree/capability-ledger.md` | Coverage map, fallbacks, authoring time, maintenance cost |
| `tree/AUTHORSHIP.md` | This document |

---

## Anti-Leakage Co-Sign (FR-9 / Story 2.5)

| Field | Value |
|-------|-------|
| Reviewer | Yair Cohen |
| Date | 2026-06-02 |
| Transcript reviewed | agent-transcripts/471303f8-700a-4286-a2b1-0afea8e9518a |
| Git check 1 | `git log --all --oneline -- "poc-eval-harness/profiles/scored/"` → empty |
| Git check 2 | `git log --all --oneline -- "poc-eval-harness/profiles/"` → empty |
| Tree commit audited | 5244548f (4 files: tree.py, __init__.py, AUTHORSHIP.md, capability-ledger.md) |

I independently verified: (1) `git log --all` shows zero commits touching
`profiles/scored/` or `profiles/` at any point in history; (2) the Epic 2 tree
commit (5244548f) introduced only the four tree artifacts and no profile or
answer-key files; (3) the authoring-session transcript shows no `Read`, `Glob`,
`Shell`, or `Grep` tool call on any path under `profiles/` — the single occurrence
of the string "profiles/scored/" in the transcript is the constraint instruction in
the user prompt, not an agent file access. The blind-authoring attestation recorded
above is corroborated. I co-sign that the tree was authored blind to the test
profiles.

— Yair Cohen (product owner / human collaborator)

---

## Fairness Sign-Off (FR-11 / Story 2.5)

| Field | Value |
|-------|-------|
| Reviewer | Yair Cohen |
| Date | 2026-06-02 |
| Files reviewed | `tree/tree.py`, `tree/capability-ledger.md` |
| Review basis | Code Review adversarial findings report (2026-06-02); patches applied for F-001, F-002, F-003, F-005 |

I have read the tree implementation and capability ledger in full. In my assessment
the tree is a competent, good-faith baseline: it branches on every machine-evaluable
`depends_on` condition in schema v0.3, implements echo-before-write as a structural
gate (write tools are unreachable without a prior UserConfirmed event), and honors the
§8 invariants (advice deflection, one-clarification-max, IDK→skip, tax→always-flag,
intent-only owner capture). The documented fallbacks (volunteered payment-split signal,
owners-CSV widget) are genuine limitations of a deterministic system, disclosed in the
ledger rather than concealed. Four issues identified by adversarial review (F-001 NLU
collision, F-002 sub-loop advice deflection, F-003 teammate IDK guard, F-005 ledger
wording) were patched before this sign-off. I find no evidence of sandbagging. I
certify this tree as a fair comparator for the frozen run.

— Yair Cohen (product owner)
