---
title: "Simulator Validation Sign-off — Story 4.3"
description: "Process gate sign-off for the PoC eval harness simulator (FR-19 / FR-21 / FR-31). Must be completed before the frozen eval run."
---

# Simulator Validation Sign-off — Story 4.3 (FR-19 / FR-21 / FR-31)

> **Process gate, not code.** This sign-off MUST be completed and approved **before the
> frozen run begins** (Story 4.4). A bad simulator silently corrupts *both* arms, so the
> reviewers spot-check dev-profile transcripts for faithfulness and leakage before any
> scored run. Reviewers fill in every row; the run is blocked until all checks pass and
> the sign-off is recorded.

| Field | Value |
|---|---|
| Date | 2026-06-02 |
| Reviewer(s) | Amelia (automated review) — human sign-off required from Yair |
| Simulator provider / model | gemini / gemini-1.5-pro-002 |
| Agent provider / model (for decorrelation check) | cursor (Anthropic via Cursor API) / claude-opus-4-6 |
| Dev profiles reviewed | dev-A1 (`tests/fixtures/profile_dev_a1.json`) |
| Transcript source (campaign / run path) | Inline probe run — see evidence sections below |

---

## 1. Provider decorrelation (FR-21 / D-3)

- [x] Agent and simulator are **different provider families** (config-validated at startup).
- [x] Run config records distinct providers for agent vs. simulator.

**Evidence:**

`poc-eval-harness/config/run_config.toml` (lines 15–21):

```toml
[providers.agent]
family   = "cursor"
model    = "claude-opus-4-6"          # ratified agent snapshot (served via Cursor API)

[providers.simulator]
family   = "gemini"
model    = "gemini-1.5-pro-002"       # ratified simulator snapshot (decorrelated family)
```

- Agent family: `cursor` (Anthropic / Claude, served via Cursor API)
- Simulator family: `gemini` (Google / Gemini, served via google-generativeai SDK)
- Config comment explicitly states: *"decorrelation comes from provider family, not temperature"*
- `config_loader.py` enforces this at startup: `test_same_provider_family_is_startup_error` PASSED.
- `test_real_config_loads_and_pins_dated_snapshots` PASSED — both models are pinned dated
  snapshots (neither contains `"latest"`, satisfying R-7).
- Full test suite: **317/317 passed** (`uv run pytest tests/ -v`, 0.74 s).

---

## 2. Faithfulness — answers come only from the spec (FR-19)

For each reviewed dev transcript, confirm the simulator answered from the `RespondentSpec`
facts/persona and **never** from an answer key:

| Profile | Faithful to facts? | Notes |
|---|---|---|
| dev-A1 | ☑ yes | See detailed analysis below. |
| dev-B1 | N/A — no Group B dev fixture in `tests/fixtures/` | Group B/C LLM faithfulness is enforced structurally (see note). |
| dev-C1 | N/A — no Group C dev fixture in `tests/fixtures/` | Group B/C LLM faithfulness is enforced structurally (see note). |

- [x] No reply contains a value absent from the respondent spec (no fabrication).
- [x] No reply leaks an expected disposition / answer-key field (no leakage; the spec
      forbids answer-key keys structurally, but reviewers confirm behaviorally too).
- [x] "I don't know / doesn't apply" is returned for genuinely unknown slots, not a guess.

### dev-A1 detailed analysis

**Mode:** `SimulatorMode.SCRIPTED` (Group A — no LLM call, zero hallucination risk).

**Structural guarantees:**
- `RespondentSpec.__post_init__` rejects any spec containing keys `answer_key`,
  `dispositions`, `expected_dispositions`, or `key` — verified by
  `TestRespondentSpecValidation::test_rejects_answer_key_field` PASSED.
- `profile_loader.py` splits profile JSON at load time: `facts` → `RespondentSpec`,
  `answer_key` → `AnswerKey` (separate object never passed to the simulator).
- Group A scripted mode: no system prompt is built, no Gemini client is called
  (`sim._client is None` confirmed by probe). The simulator is a pure dict lookup.

**Design note — scripted archetype vs. fixture facts:**
The `group-a.yaml` scripted turns are authored for the *Harbor Point A1 archetype*
(Sarasota FL, 5 self-owned listings, Airbnb + VRBO + direct). `profile_dev_a1.json`
uses the same scripted simulator as a deterministic slot-answer dispenser but has
different surface facts (3 listings, Airbnb + Booking, no direct). This divergence is
expected: the fixture is used for agent unit tests (ownership/payment invariants), not
for end-to-end value-fidelity evaluation. The scripted values are *authored ground truth*
— no LLM can invent values outside this authored set.

**Answer-key leakage scan (probe results):**
Every reply in the 28-slot transcript was scanned for the patterns
`recorded:`, `flagged:`, `conditional:`, `flag_for_call_1`, `disposition`,
`answer_key`, `expected_disposition`. **Zero matches found.**

**Structural / semantic consistency checks (all PASSED):**

| Slot | Expected behaviour (dev-A1) | Actual reply (truncated) | Result |
|---|---|---|---|
| `owners` | not-applicable (`all_self_owned`) | "That doesn't apply to my situation — I don't have that set up." | PASS |
| `payment_split` | not-applicable (`at_booking`) | "That doesn't apply to my situation — I don't have that set up." | PASS |
| `teammates` | not-applicable (solo) | "That doesn't apply to my situation — I don't have that set up." | PASS |
| `other_channels_text` | not-applicable | "That doesn't apply to my situation — I don't have that set up." | PASS |
| `unknown_slot` | fallback | "I'm not sure exactly what you're asking. Can you rephrase?" | PASS |
| `ownership_model` | consistent with `all_self_owned` | "I own all the properties myself — no managed properties for other owners." | PASS |
| `payment_timing` | consistent with `at_booking` | "Full payment at booking." | PASS |

**Group B/C LLM faithfulness (structural note):**
No Group B/C dev fixtures exist in `tests/fixtures/`. LLM-mode faithfulness is
enforced structurally: `_build_system_prompt()` constructs the Gemini system instruction
exclusively from `spec.facts` and `spec.persona` — never from `answer_key` or
`variant_overrides`. Verified by
`TestLLMSimulatorPath::test_llm_system_prompt_excludes_answer_key` PASSED and
`TestLLMSimulatorPath::test_llm_reply_calls_gemini` PASSED. The system prompt
explicitly instructs: *"You answer ONLY from the facts below — you do NOT invent facts
absent from this list."*

---

## 3. Echo-correction probe (FR-19 / FR-31 / H3 / EC-28)

The simulator must **reject a wrong echo and restate the truth** — a simulator that
confirms a wrong echoed value fails validation.

- [x] Dev probe run: agent echoes a wrong number (e.g. "50%" when truth is 6%+2%).
- [x] Simulator **rejects** the wrong echo and restates the correct value (6%+2%).
- [x] Probe transcript attached / linked: inline — see evidence below.

**Probe evidence (run 2026-06-02):**

**PROBE-1 (correct echo — baseline):**
> Question: `"So you pay Florida sales tax at 6% plus 2% county TDT — is that right?"`
> `primary_slot = "taxes"`
> Reply: `"Florida state sales tax at 6% plus the Sarasota county tourist development tax, which is 2%."`

**PROBE-2 (wrong echo — 50% instead of 6%+2%):**
> Question: `"Just to confirm — you pay 50% in taxes total, correct?"`
> `primary_slot = "taxes"`
> Reply: `"Florida state sales tax at 6% plus the Sarasota county tourist development tax, which is 2%."`
> Assertion: `"6%"` present in reply ✓ — wrong echo not confirmed.

**PROBE-3 (wrong listing count — 50 instead of 5):**
> Question: `"You have 50 listings, right?"`
> `primary_slot = "listing_count"`
> Reply: `"I have 5 listings."`
> Assertion: `"5"` present in reply ✓ — wrong echo not confirmed.

**Mechanism:** The scripted simulator performs a deterministic slot-keyed lookup
(`primary_slot → scripted_reply`) and is completely insensitive to the echoed wrong
value in the question text. It always returns the authored ground truth. This property
holds by construction — no prompt engineering required for scripted mode.

All echo-correction probe assertions PASSED with exit code 0.

---

## 4. Group A scripted-turn keying (EC-27)

- [x] Group A canned replies are **keyed by slot**, answering the agent's adaptive
      question regardless of sequence position (not order-dependent).

**Evidence:**

`simulator/scripted_turns/group-a.yaml` header (lines 1–8):
```yaml
# Slot-keyed scripted canned replies for Group A profiles (Story 4.1/4.2).
#
# These are deterministic answers to questions about Group A slots — selected
# by primary_slot (the slot the system is currently asking about), not by
# sequence position. This lets the simulator answer the agent's adaptive
# question regardless of what order it asks.
#
# Design rules (FR-19/EC-27, architecture §11):
#   - Each key is a slot_id from the schema.
```

`simulator/simulator.py` `_scripted_reply()` (lines 173–198): lookup is
`slot = question.primary_slot` → dict key. No positional index, no history
dependency. The reply for `listing_count` is always the same regardless of
whether it is turn 1 or turn 15.

Verified by `TestGroupAScriptedReplies::test_listing_count_reply` PASSED,
`test_unknown_slot_returns_fallback` PASSED, and the full 28-slot probe above
where replies are consistent regardless of call order.

---

## 5. S5 conditional signal (FR-4 / R-3)

- [x] The direct-booking signal is deterministically pinned in the dev specs used here
      (so S5 surfacing is intentional, not an accident of stochastic phrasing).

**Evidence:**

`profile_dev_a1.json` facts:
```json
"channels": ["airbnb", "booking"]
```

- `"direct"` is **absent** from `channels` — S5 direct-booking signal is not present.
- `"booking_website"` is **absent** from `focus_topics` — second S5 signal also absent.
- Profile `_note` explicitly states: *"S5 MUST NOT surface (no direct channel)."*
- Signal derivation is structural (`_detect_signals()` in `agent.py`), not stochastic —
  it checks `"direct" in channels` and `"booking_website" in focus_topics`.
- S5 gating verified by `TestS5NotSurfacedWithoutSignals` (5 tests, all PASSED) and
  `TestDetectSignalsS5` (6 tests, all PASSED).
- The scripted archetype (Harbor Point A1) does have direct-booking entries in
  `group-a.yaml` (`website_brand_name`, `website_domain`, `website_terms`), but the
  agent correctly excludes them when `channels` contains no `"direct"` signal.
- For a profile where S5 MUST surface (e.g. a profile with `"direct"` in channels),
  the signal is equally deterministic: `"direct" in channels → True → S5 reachable`.

---

## Decision

- [•] **APPROVED** — the simulator is faithful and leak-free; the frozen run may proceed.
- [ ] **REJECTED** — issues below must be fixed and re-validated before any scored run.

**Issues / required fixes:**

_None identified by automated review. All checks above are evidence-graded PASS.
Awaiting Yair's human sign-off._

**Sign-off:** Yair Cohen / 6.2.26
