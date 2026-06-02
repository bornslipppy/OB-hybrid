---
title: "Answer-Key Review & Freeze Protocol — Scored Respondent Profiles"
author: "Mary (Business Analyst)"
date: 2026-06-02
version: 1.0
status: draft — ready to assign reviewers
purpose: "Coordinate independent validation of the 8 scored answer keys, adjudicate disagreements, and freeze them before any eval run — so SAR is well-defined and defensible (PoC plan §6.1)."
companions:
  - "poc-respondent-specs-2026-06-02.md v1.1 (the keys under review)"
  - "poc-plan-ai-adaptive-onboarding-2026-06-02.md §6.1 / §6.2"
  - "guesty-pro-account-creation-schema.md v0.3"
---

# Answer-Key Review & Freeze Protocol

The 8 scored answer keys are the **single source of truth** for SAR. If they're wrong or contested,
every downstream number is meaningless. This protocol makes the keys **independently validated,
adjudicated, and frozen** before the eval runs.

---

## 1. Roles

| Role | Who | Responsibility |
|------|-----|----------------|
| **Author** | Mary (analyst) | Wrote the keys; **does not** get a validation vote (avoids self-confirmation) |
| **Reviewer 1** | Onboarding SME (knows real OB behavior) | Independent pass |
| **Reviewer 2** | Product/data-model SME (knows the schema/entities) | Independent pass |
| **Tie-breaker** | Senior onboarding lead or PM | Adjudicates only the disagreements |
| **Freeze owner** | Mary | Locks the version + records the checksum |

> Reviewers 1 and 2 must be **different people from the author** and should review **independently**
> (no shared doc-commenting until both submit) to keep their judgments uncorrelated.

---

## 2. What each reviewer checks (per slot)

For every slot disposition in each profile, confirm it is correct **given the profile's facts +
persona + the schema rules**. Use this checklist:

1. **Disposition type is right** — `recorded` / `flag_for_call_1` / `flagged` / `skipped` /
   `conditional` matches what the schema + resolved gates require.
2. **G1 (intent-capture)** — owner *identity* fields = `recorded`; owner *economics* =
   `recorded + flag_for_call_1`; no expectation that the agent writes a BusinessModel.
3. **G6 (S5 conditional)** — S5 slots are `surface` **iff** a direct-booking signal exists in the
   profile/persona; otherwise `conditional → not surfaced`.
4. **Echo-before-write** — every numeric/financial `recorded` value implies a confirm step (the key
   shouldn't expect a silent write).
5. **Tax always flagged** — every tax line is `flagged: confirm_filing` even when the rate is recorded.
6. **Skip handling** — deferrals are `skipped` with **no** expectation of retry; partial vs.
   whole-section deferral is correctly scoped (cf. B4 whole-section vs. D-style per-field).
7. **One-clarifying-question cases** (B1, B2, C2) — the key expects exactly one targeted question,
   not zero (assumed) or many (interrogation).
8. **SAR denominator** — `required + recommended` slots with disposition ≠ `skipped`; provisional-G3
   slots flagged as such.
9. **Value tolerances** — approximate values (B2 "~18%") are allowed per the §6.1 tolerance rule.

Reviewers mark each slot: **✓ agree** · **✗ disagree (propose X)** · **? unclear (needs author note)**.

---

## 3. Process & timeline

```
Day 1   Author distributes: scored specs v1.1 + this checklist + schema v0.3 + plan §6.1.
Day 1–2 Reviewer 1 and Reviewer 2 label every slot INDEPENDENTLY (✓/✗/?). Submit to freeze owner.
Day 3   Freeze owner computes agreement, builds the CONTESTED-SLOT LOG (every ✗ or ? from either).
Day 3   Tie-breaker adjudicates ONLY the contested slots (with author present to answer "?", not to vote).
Day 4   Apply adjudicated changes → specs v1.1-frozen. Mark surviving-ambiguous slots as a
        SENSITIVITY BAND (scored both ways; reported as a range, not dropped — plan §6.1/§6.2).
Day 4   Freeze: tag the file version, record a content checksum, set status = FROZEN.
```

Estimated **3–4 days**, overlapping PoC plan Phase 1.

---

## 4. Agreement & adjudication rules

- **Per-slot agreement** between Reviewer 1 and Reviewer 2 is reported (target ≥ 90% pre-adjudication;
  lower means the schema rules need clarifying before scoring).
- A slot is **contested** if *either* reviewer marks ✗ or ?.
- The tie-breaker's adjudicated disposition is final for scoring.
- A slot that remains **genuinely ambiguous after adjudication** is **not deleted**. It is scored
  under **both** plausible dispositions and reported as a **sensitivity band** (e.g., "SAR 0.82–0.86
  depending on slot X") — dropping it would bias toward whichever arm the analyst prefers.

---

## 5. Contested-slot log (template)

| Profile | Slot | Author key | R1 | R2 | Reason for dispute | Tie-breaker decision | Sensitivity-band? |
|---------|------|-----------|----|----|--------------------|----------------------|-------------------|
| C1 | `owners[0].who_pays_channel_commission` | recorded: owner | ✗ → split? | ? | gross-vs-net basis unclear | record `owner` + flag basis | no |
| … | | | | | | | |

---

## 6. Freeze record (fill at freeze time)

| Field | Value |
|-------|-------|
| Frozen file | `poc-respondent-specs-2026-06-02.md` |
| Version | v1.1-frozen |
| Freeze date | — |
| Content checksum (sha256) | — |
| Reviewers | R1: — · R2: — · Tie-breaker: — |
| Pre-adjudication agreement | — % |
| Contested slots | n = — (m as sensitivity band) |
| Provisional-G3 slots | listed (re-freeze trigger if G3 resolves before run) |

> **Re-freeze triggers:** any change to the schema's resolved gates, G3 enum casing closing, or a
> defect found mid-run. A re-freeze **invalidates prior runs** — the scored 8 must be run again,
> once, post-freeze (plan §5.1).

---

## 7. Definition of done
- [ ] R1 + R2 independent passes submitted
- [ ] Contested-slot log complete and adjudicated
- [ ] Sensitivity-band slots identified and dual-scored in the harness
- [ ] Version tagged, checksum recorded, status = FROZEN
- [ ] Greenlight to run Phase 4 eval
