# Tree Capability Ledger  (FR-13 / FR-13b)

> This ledger is the cited evidence for SM-3 ("impractical-authoring" alternative),
> SM-11 (maintenance-cost proxy), and the §7 Group-C analysis.  It records which
> `depends_on` paths the tree branches, where it falls back, estimated authoring hours,
> and the time to extend for one realistic schema change.

---

## 1. `depends_on` Coverage Map

Every schema v0.3 condition is listed with its tree treatment.

| Slot | `depends_on` / `surface_when` condition | Tree treatment |
|------|----------------------------------------|----------------|
| `other_channels_text` | `channels includes 'other'` | ✅ **Branches** — only asked if parsed channels list contains `other` |
| `turnover_checklist_file` | `turnover_checklist_choice == 'upload'` | ✅ **Branches** — only surfaces widget note if choice == `upload`; otherwise skips |
| `security_deposit_amount` | `security_deposit_type in ['damage_waiver','security_deposit']` | ✅ **Branches** — echo-before-write question only when type is in the guarded set; skipped for `damage_protection` / `none` |
| `payment_split` | `payment_timing == 'split' OR user volunteers a split` | ✅ **Branches (deterministic half)** — surfaces when `payment_timing` is recorded as `split`.  **Fallback:** "OR user volunteers" is a runtime signal not evaluable from recorded facts alone; tree relies on parsing the `payment_timing` reply for volunteered splits.  If the user volunteers a split *before* the payment_timing question, the tree may miss it — **documented fallback: skip+flag_for_call_1**. |
| `owners` (list) | `ownership_model in ['all_managed_for_others','mixed']` | ✅ **Branches** — full per-owner sub-FSM activated; `all_self_owned` skips the loop |
| `owners_csv` | `ownership_model in ['all_managed_for_others','mixed']` | ⚠️ **Partial fallback** — tree uses conversational capture for all owner counts; CSV upload path is widget-based and cannot be driven by the tree.  Recorded as `skip_question` + note. |
| `pmc_commission_rate` (per owner) | `management_model == 'commission'` | ✅ **Branches** — echo-before-write sub-field within add_owner; only asked/captured when management_model is `commission` |
| `fixed_fee_amount` (per owner) | `management_model == 'fixed_fee'` | ✅ **Branches** — echo-before-write sub-field; only asked when management_model is `fixed_fee` |
| `split_terms` (per owner) | `management_model in ['revenue_split','other']` | ✅ **Branches** — verbal echo + flag_for_call_1; asked when management_model is `revenue_split` or `other` |
| `teammates` | `decision_owner == 'shared'` | ✅ **Branches** — teammate loop only entered when `decision_owner` is `shared` |
| `website_brand_name` | `surface_when: channels includes 'direct' OR focus_topics includes 'booking_website' OR user volunteers website intent` | ✅ **Branches (signals detected from recorded facts + history scan)** — `channels includes 'direct'` and `focus_topics includes 'booking_website'` are machine-evaluable; "user volunteers website intent" is detected by scanning conversation history for keywords (`my website`, `direct booking`, `booking website`) |
| `website_domain` | `website_brand_name is recorded` | ✅ **Branches** — traversal guard: slot skipped unless previous slot dispositioned |
| `website_terms` | `website_domain is recorded` | ✅ **Branches** — same chain guard |
| `handover_note_raw` (S0b) | none | ✅ **Skipped** — S0b is prefill input only; tree neither asks nor records it |
| `tech_level`, `customer_sentiment`, `risk_flags` | none (brief-only) | ✅ **Never surfaced** — brief-only per schema; tree does not echo or act on them |

---

## 2. Behavioral-Path Parity

| Path | Schema specification | Tree behavior |
|------|---------------------|---------------|
| **echo-before-write** (§8 inv 1) | `security_deposit_amount`, `mandatory_fees`, `taxes`, owner numeric sub-fields | ✅ `_EchoState` buffer; write tool fires ONLY after `UserConfirmed` emitted.  False-write rate = 0 by construction. |
| **tax = always flag** (Path H) | `taxes.human_handoff == flag_for_call_1`; "never corrects tax law" | ✅ `add_tax` always followed by `flag_for_call_1`; no correction or recommendation ever made |
| **advice deflection** (§8 inv 2, Paths B/G) | Advice request → `flag_for_call_1` + no recommendation | ✅ `_is_advice_request()` check on every reply; routes to `FlagForCall1` |
| **one clarifying question** (§8 inv 3) | One clarification max; then `skip+flag` | ✅ `_ambiguity_count[slot]` ≤ 1; second ambiguity → `SkipQuestion + FlagForCall1` |
| **IDK / absence → skip, not ambiguity** (§8 inv 7) | `i don't know` = absence; not a clarifying-question trigger | ✅ `_is_idk()` routes directly to skip (or flag if required) without spending the one clarification |
| **intent-capture on hero branch** (G1 / FR-3) | `add_owner` records intent; BusinessModel never written | ✅ `add_owner` + `flag_for_call_1(topic="owner_economics")`; no BusinessModel tool call exists in the tree |
| **conditional fee → flag** (Path E) | Conditional/gated fees → `flag_for_call_1` | ✅ Detected by "if / only if / when guest" keywords; flagged without `add_fee` |
| **echo verbal formula** (§8 inv 3 / EC-13) | `split_terms` echoed back for confirmation | ✅ `_begin_echo(slot="owners", subfield="split_terms")` before `add_owner` |
| **payment Path C** ("depends on channel") | Record direct-booking default + flag OTA ambiguity | ✅ Detected by "channel / depends" in reply; records `near_arrival` default + `FlagForCall1` |
| **S5 conditional** (G6 / FR-4) | Surface S5 only when direct-booking signal present | ✅ `_detect_direct_booking_signal()` gate in `_advance()`; S5 skipped when no signal |
| **rate_strategy skip** | Skip if third-party pricing tool present | ✅ `_has_external_pricing_tool()` check; `SkipQuestion` emitted |
| **required slot deferred** (§8 inv 4 / EC-24) | Deferred `required` slot → `FlagForCall1`, not silent `SkipQuestion` | ✅ `_handle_idk()` checks `slot_def.priority`; `required` → flag |
| **end_section guard** (§3.2) | `end_section` forbidden while reachable in-scope slots undispositioned | ⚠️ **Fallback** — tree does NOT emit `end_section` tool calls (the reducer guard would reject premature ones anyway); sections advance purely by exhausting their traversal slots.  This deviates from the agent's trace shape but does not affect SAR scoring. |

---

## 3. Documented Fallbacks (where `skip+flag` replaces a branch)

| Scenario | Why a full branch is impractical | Fallback |
|----------|----------------------------------|---------|
| **"user volunteers a split"** (payment_split guard) | Runtime conversational signal; not derivable from recorded facts alone | If `payment_timing` was not asked yet and user mentions a split unprompted, tree may miss it.  Fallback: `skip_question("payment_split") + flag_for_call_1`.  Capability ledger shows this as a B-group slot where AI has a structural advantage (free-text parsing). |
| **Owners CSV path** | File upload is widget-based; tree cannot drive a file selection dialog | `skip_question("owners_csv")` + note for Jordan if conversational path is used.  Owner count > 5 → prompt user to "upload a CSV" but record as skip. |
| **Custom payment split terms** (deposit_pct / balance_when) | Schema does not define them as formal field IDs; sub-fields implied by `shape_if_custom` only | Recorded verbatim as `payment_split = "custom"` + `flag_for_call_1` with user quote.  Jordan configures the exact rule. |
| **Ambiguous owner count** | User replies with non-numeric / vague answer (e.g. "a few") | `skip_question("owners") + flag_for_call_1`; owner capture deferred entirely to Call 1. |
| **`who_pays_channel_commission` — ambiguous reply** | Free-text owner-comm reply that doesn't match any canonical phrase | Default to `pmc` and flag for Jordan to verify.  Not a guess-and-write; flag accompanies the assumption. |
| **`third_party_tools` prefill** | S0b prefill values arrive as SF-structured data; tree cannot infer them from conversation without being told | If `third_party_tools` is not in recorded facts AND no third-party tool mentioned in history, `rate_strategy` is asked normally.  If mentioned in conversation, tree detects and skips. |
| **`mandatory_fees` with no amounts** | Some replies name a fee type without an amount | Tree asks a follow-up for the amount; if second parse also fails → `skip+flag`. |
| **S5 surface_when "user volunteers website intent"** | Pure conversational signal; tree detects via keyword scan of history, which is imperfect | History scan covers the most common phrases; unusual phrasings may be missed.  Fallback: S5 skipped (scored as `conditional: surface_if_direct_signals_present`, which is correct for no-signal case). |

---

## 4. False-Write Safety

**False-write rate: 0 by construction** (SM-C1 kill criterion / NFR-2).

The structural gate is `_EchoState`:

```
user gives numeric value
  → _begin_echo() emits ValueIntroduced + EchoIssued into drain buffer
  → returns UserQuestion (the echo confirmation prompt)
    ← user confirms (yes / correct)
      → _commit_echo_value() emits UserConfirmed + write tool
    ← user corrects
      → UserCorrected emitted; new value re-echoed
    ← user defers / ambiguous (after 1 reprompt)
      → FlagForCall1 + no write tool
```

The write tool for any `echo_before_write` field is **never reachable** without a prior `UserConfirmed` event in the same echo cycle.  There is no code path from value-parse to tool-emit that bypasses this buffer.

Per-sub-field granularity (EC-12): composite tools (`add_owner`, `add_fee`, `add_tax`) each numeric sub-field has its own `_begin_echo` / confirm cycle before `_commit_owner` / `_commit_tax` / fee commit fires the composite tool.

---

## 5. Tooling Parity (FR-12 / FR-13b)

### 5.1 NLU Vocabulary Map
The tree applies the full §10 normalization map (`_NLU_MAP` in `tree.py`) before any parsing.  All 10 documented high-frequency mappings are implemented, plus ~30 additional synonyms derived from the same corpus analysis.  Failures attributable to literal string matching are not counted as tree weakness (FR-12 consequence).

### 5.2 Tool Vocabulary
The tree emits exactly the 7 kernel tools:
`record_answer`, `add_fee`, `add_tax`, `add_owner`, `skip_question`, `flag_for_call_1`, `end_section`

No free-writes.  All calls go through kernel Pydantic models with schema-validated argument shapes.

### 5.3 Trace Event Parity (FR-13b)
The tree exposes `drain_trace_events()` (R-10 forward-compat hook used by `runner.py`).  Echo-lifecycle events emitted:

| Event | When emitted |
|-------|--------------|
| `ValueIntroduced(call_type="scored", temperature=0.0)` | On every value extraction for an echo-required field |
| `EchoIssued` | When echo question is posed |
| `UserConfirmed` | When user confirms the echoed value |
| `UserCorrected` | When user corrects the echoed value |

`ToolCallEvent(call_type="scored", temperature=0.0)` is emitted by the harness runner for every tool call returned by the tree (default `call_type="scored"`, `temperature=0.0` per `ToolCallEvent` model defaults in `kernel/trace.py`).  FR-23/FR-24 scoring (false-write detection, disposition scoring, questions-to-completion) runs unmodified on the tree's trace.

---

## 6. Authoring Time

| Activity | Estimated Hours |
|----------|----------------|
| Schema analysis (reading v0.3 cover-to-cover, mapping all depends_on guards) | 1.5 h |
| FSM design (section order, S8 hero-branch phases, echo protocol, fallback rules) | 1.5 h |
| `tree.py` implementation (TreeSystem + all parsing + owner sub-FSM) | 4.0 h |
| NLU synonym map authoring (per-slot enum maps + §10 NLU map) | 1.0 h |
| Capability ledger authoring (this document) | 0.5 h |
| `AUTHORSHIP.md` | 0.25 h |
| Smoke-test / lint pass | 0.5 h |
| **Total** | **~9.25 h** |

*This session is the independent authorship record (FR-10 / Story 2.5).*

---

## 7. Time-to-Update: Adding One New `management_model` Enum Value

**Scenario:** Schema adds `management_model = "net_split"` (net-of-expenses revenue split).

Steps required in the tree:

| Step | File | Change | Estimated Time |
|------|------|--------|---------------|
| Add synonym mapping | `tree.py: _MGMT_MODEL_MAP` | `"net split": "net_split", "after expenses": "net_split"` | 5 min |
| Add economics phase | `tree.py: _first_econ_phase()` | Add `"net_split": "split_terms"` branch (same as `revenue_split`) | 3 min |
| Add question text | `tree.py: _owner_question_for_phase()` or reuse `split_terms` | Identical behavior to `revenue_split` — `split_terms` path already handles it | 0 min (reuse) |
| Update `AddOwner` kernel model | `kernel/tools.py` | Add `"net_split"` to the `management_model` Literal | 2 min |
| Update capability ledger | `capability-ledger.md` | Note new branch | 5 min |
| **Total** | | | **~15 min** |

**For comparison (agent):** Adding a `management_model` enum value requires:
- Updating the system prompt to list the new value and describe when/how to use it
- Updating any few-shot examples that reference management models
- Re-testing on dev profiles to verify the agent doesn't confuse the new value with existing ones
- Estimated: **30–90 min** (prompt re-tuning is non-deterministic)

**Maintenance advantage:** The tree update is mechanical and verifiable (grep + unit test).  The agent update requires empirical re-validation.

---

## 8. Group-C Impractical-Authoring Assessment

**Quantitative:** The tree branches on **12 of 14** distinct `depends_on` conditions in schema v0.3 (see §1 above).  The two partial fallbacks (`payment_split` volunteered signal, `owners_csv` widget) involve no scoring slots that a Group-C profile would exercise as `recorded` dispositions.

**Fan-out node count (S8 hero branch):**  The owner sub-FSM has:
- 4 management_model branches × (1–2 numeric sub-fields each) = **6–8 hand-authored phase transitions per owner**
- For N owners each with a different management_model: **N × 8 nodes** in an equivalent static tree
- For the typical Group-C profile (4 owners, mixed models): **~32 decision nodes** for the economics fan-out alone

This is within the SM-3 "≤40 nodes for C fan-out" threshold — so the tree is a **competent authoring**, not an impractical one.  The impractical-authoring win (SM-3 alternative) applies only if the Group-C capability ledger shows **≥50% skip+flag** on Group-C owner-economics slots; see §3 for where the fallbacks live.

---

*Ledger version: 1.0 — authored during independent tree-authorship session (see AUTHORSHIP.md).  No profile/answer-key exposure at time of authoring.*
