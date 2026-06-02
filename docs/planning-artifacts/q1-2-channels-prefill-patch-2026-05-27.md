---
title: "Q1.2 + Q1.3 — Salesforce channel prefill patch"
---

# Q1.2 + Q1.3 — Salesforce channel prefill patch

**Date:** 2026-05-27
**Author:** Sally (UX Designer)
**Audience:** Designer producing the Figma + agent building the prototype
**Applies to:** §4.3 and §4.3a of [`ux-design-specification-v2-atlas-aligned-2026-05-27.md`](ux-design-specification-v2-atlas-aligned-2026-05-27.md) — Q1.2 ("Airbnb-only check") and Q1.3 ("Channel confirmation").
**Pattern source:** Salesforce-prefill chip pattern, already defined in v2 §15.3 and used at Q1.1.
**Voice & copy standards:** Atlas — sentence case, no exclamation marks, glossary-compliant terminology, plain-language voice.

---

## 0. Why this patch exists

Q1.2 asks the user a question Guesty already knows the answer to. By the time the user reaches the wizard, the sales call has populated Salesforce with the channels the user manages — the wizard shouldn't ask, it should **verify**.

This patch flips Q1.2 (and the downstream Q1.3 if it renders) from *blank multi-select* to *prefilled-confirm*. Same pattern Q1.1 already uses for listing count. Goal: shorter wizard for known accounts, no information loss, full editability for the small number of cases where Salesforce is wrong or out of date.

> **⚙️ Safety net — read this first.** If Salesforce returns no data, empty data, or anomalous data, **the wizard falls back to today's behavior exactly** (the v2 spec §4.3 and §4.3a baselines — blank multi-select on Q1.2, Airbnb-locked-checked on Q1.3, no chip, no attribution line, no error message to the user). The prefill pattern is purely additive. An account with no Salesforce data sees the same wizard it would see today. See §3.5 and §4.3 for the exact fallback contract.

---

## 1. Summary

| # | Delta | Why |
|---|------|-----|
| **P-1** | Q1.2 renders a prefilled chip showing the **specific channel list** (e.g. `Airbnb, Booking.com, and Vrbo`) — not a vague binary — with `Looks right` and `Change` actions | Verify-don't-ask reduces friction; showing the actual channels lets the user verify in one glance |
| **P-2** | **Q1.3 is skipped entirely in the prefilled path** — the Q1.2 pill already shows the exact channel list, so re-asking is redundant. Q1.3 only renders when Q1.2 fell back to the baseline binary state | Don't ask twice for data we already have; collapse the two screens into one when we can |
| **P-3** | **If Salesforce data is missing, empty, or anomalous, both Q1.2 and Q1.3 fall back to today's exact behavior** (v2 spec §4.3 and §4.3a baselines). No error, no degraded state — the wizard behaves as it does for accounts without sales-call data. | The prefill pattern must never break the wizard for users we don't have data on |
| **P-4** | `Change` on Q1.2 expands the question into the full multi-select (with the prefilled value pre-selected, not erased) — user adjusts and confirms | Treating "change" as "edit" not "restart" preserves the user's existing intent |
| **P-5** | Confirmed answer commits and advances. `Looks right` and an explicit `Continue` from the edit state both trigger branch-lock per master spec FR-11.2 | Salesforce prefill is treated as a *user commit* once confirmed — same write semantics as a typed answer |
| **P-6** | When the user checks `Other` (in Q1.2's edit state OR in the fallback Q1.3), an inline text field reveals below it to capture which channel(s) — lightweight progressive disclosure, not a full follow-up screen | Captures specific channel names while the user is engaged, without slowing down the wizard with another screen |
| **P-7** | Attribution line shows the sales-call date only when older than 30 days — fresh prefills get a clean attribution, stale ones get an explicit "anything changed since?" prompt | Builds trust on recent data; flags potentially-stale data to the user honestly |

---

## 2. Data model — what Salesforce gives us

Confirm the actual contract with the integration team. This patch assumes the following minimum shape; flag in §11 if the real fields differ.

```ts
type SalesforceWizardPrefill = {
  // Q1.2 inputs
  channels: Array<'airbnb' | 'booking_com' | 'vrbo' | 'expedia' | 'other'>;
  // Optional — if present, used to render Q1.3 "Other" follow-up
  other_channel_names?: string[];
  // Provenance for the chip copy
  source_call_date?: string; // ISO date of the sales call this came from
};
```

### Derived state for Q1.2

The prefilled pill shows the **specific channel list**, not a binary "Airbnb only / plus others" framing. Saying `Airbnb plus other channels` when we already know the others is wasteful — the chip's whole job is to surface what we know.

| Salesforce input | Q1.2 prefilled pill |
|---|---|
| `channels: ['airbnb']` | `Airbnb` |
| `channels: ['airbnb', 'booking_com']` | `Airbnb and Booking.com` |
| `channels: ['airbnb', 'booking_com', 'vrbo']` | `Airbnb, Booking.com, and Vrbo` |
| `channels: ['airbnb', 'booking_com', 'vrbo', 'expedia']` | `Airbnb, Booking.com, Vrbo, and Expedia` |
| `channels: ['airbnb', 'other']` + `other_channel_names: ['Hostfully']` | `Airbnb and Hostfully` |
| `channels: ['airbnb', 'booking_com', 'other']` + `other_channel_names: ['Hostfully', 'Lodgify']` | `Airbnb, Booking.com, Hostfully, and Lodgify` |
| `channels: ['airbnb', 'other']` + no `other_channel_names` | `Airbnb and one other channel` |
| `channels: ['airbnb', 'booking_com', 'other']` + no `other_channel_names` | `Airbnb, Booking.com, and one other channel` |
| `channels` is empty, null, or undefined | **Missing — fall back to v2 baseline (Q1.2 binary multi-select, then Q1.3 if needed)** |
| `channels` doesn't include `airbnb` at all | **Data anomaly — fall back to v2 baseline and log a soft error to ops** (the wizard's Q1.2 hypothesizes Airbnb is at least present; an account with no Airbnb shouldn't be in this wizard at all) |

### List formatting rules (locked)

- **1 channel:** the channel name alone (e.g. `Airbnb`).
- **2 channels:** `{a} and {b}` (no commas).
- **3+ channels:** `{a}, {b}, and {c}` — **Oxford comma required** per Atlas §style.
- **`Other` with captured names:** unfold each name as if it were a regular channel — they appear in line with the rest. The literal word "other" never appears.
- **`Other` without captured names:** append `one other channel` (singular) at the end. If the integration team ever surfaces a count of unnamed others, switch to `{n} other channels`.
- **No truncation cap.** Even with 6 channels, list them all. Accuracy beats brevity in a verification pill.

### Structural implication — Q1.3 in the prefilled path

Once the Q1.2 pill lists the specific channels, **Q1.3 (the channel-confirmation question) becomes redundant in the prefilled path** — the user already verified the channel set when they clicked `Looks right`. Q1.3 only renders in the fallback path.

| Path | Q1.2 | Q1.3 | Notes |
|---|---|---|---|
| Salesforce prefill present + user confirms | Prefilled pill state | **Skipped** | Advance directly to Q1.4. The pill already verified the channel list. |
| Salesforce prefill present + user edits | Prefilled pill → edit state (channel checkboxes) | **Skipped** | The edit state already shows the channel checkboxes — same UI as Q1.3 would have been. No reason to re-ask. |
| Salesforce prefill absent (fallback) | v2 baseline binary multi-select | Renders if Q1.2 = "Airbnb plus other channels" | Today's exact behavior. |

---

## 3. Q1.2 — Prefilled state (primary)

### 3.1 Layout

Single-panel question, same chrome as today. The change is the body — instead of two option buttons, render the prefill chip pattern with the **specific channel list**.

```
┌────────────────────────────────────────────────────────────────────┐
│                                                                    │
│  Your listings are on these channels                              │
│                                                                    │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │ Pre-filled from your sales call. Looks right?              │   │
│  │                                                            │   │
│  │   ✓ Airbnb, Booking.com, and Vrbo                          │   │
│  │                                                            │   │
│  │   [ Looks right ]   [ Change ]                             │   │
│  └────────────────────────────────────────────────────────────┘   │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

The heading shifts from the original binary framing (`Are your listings on Airbnb only, or other channels too?`) to the more direct `Your listings are on these channels` because the pill is now answering specifically. The original binary heading still appears in the **fallback state** (§3.5) — it makes sense when the user is filling in a blank multi-select from scratch.

### 3.2 Copy register

| Element | Copy |
|---|---|
| Heading (h2) | `Your listings are on these channels` |
| Attribution line — **fresh** (`source_call_date` ≤ 30 days old, or missing) | `Pre-filled from your sales call. Looks right?` |
| Attribution line — **stale** (`source_call_date` > 30 days old) | `Pre-filled from your sales call on {date}. Anything changed since?` |
| Date format in stale attribution | `Month DD, YYYY` (e.g. `April 14, 2026`) — Atlas style §dates |
| Prefilled value pill | The formatted channel list per §2 (e.g. `Airbnb`, `Airbnb and Booking.com`, `Airbnb, Booking.com, and Vrbo`, `Airbnb and Hostfully`, `Airbnb, Booking.com, and one other channel`) |
| Primary CTA | `Looks right` |
| Secondary CTA | `Change` |

### 3.3 Behavior

| Trigger | Effect |
|---|---|
| Click `Looks right` | Commits the full channel list (verbatim from Salesforce). **Q1.3 is skipped** — advance directly to Q1.4. The pill already verified what Q1.3 would have asked. Triggers `wizard.answer_committed` with `source: 'salesforce_prefill'`. |
| Click `Change` | Q1.2 swaps into the **edit state** (§3.4) — the full channel checkbox list, pre-checked from Salesforce. **Q1.3 is also skipped** in this path (the edit state already shows the same checkboxes). |
| Salesforce data missing or anomalous | Render Q1.2 in the **fallback state** (§3.5) — no chip, no attribution line, blank multi-select per v2 spec §4.3 baseline. **This is the safety net — fully identical to today's wizard behavior.** |
| Click `Looks right` keyboard | `Enter` triggers `Looks right` when focus is anywhere inside the chip card. `Space` works on the focused button. |
| Click `Change` keyboard | `Tab` from `Looks right` reaches `Change`. `Enter` or `Space` activates. |
| `source_call_date` present and ≤ 30 days old | Use the **fresh** attribution: `Pre-filled from your sales call. Looks right?` |
| `source_call_date` present and > 30 days old | Use the **stale** attribution: `Pre-filled from your sales call on {date}. Anything changed since?` |
| `source_call_date` missing entirely | Use the fresh attribution (no date to render). Hide the trailing `. Looks right?` is optional — keep it for consistency with Q1.1. |

### 3.4 Edit state (user clicked `Change`)

The chip card transforms into the **full channel checkbox list** — what Q1.3 would have shown — with the prefilled channels already checked and any captured `other_channel_names` already populated in the `Other` field. The user's job is to refine, not redo.

| Element | Copy / behavior |
|---|---|
| Attribution line | Replaced with: `Update what's changed since your sales call.` |
| Checkbox — Airbnb | `Airbnb` — **locked checked**, disabled. Tooltip: `Airbnb is your starting channel — we'll connect it on the next screen.` |
| Checkbox — Booking.com | `Booking.com` — pre-checked if `channels` includes `booking_com` |
| Checkbox — Vrbo | `Vrbo` — pre-checked if `channels` includes `vrbo` |
| Checkbox — Expedia | `Expedia` — pre-checked if `channels` includes `expedia` |
| Checkbox — Other | `Other` — pre-checked if `channels` includes `other`. Reveals the inline text field below when checked, prefilled with `other_channel_names.join(', ')`. Field is optional. (Behavior identical to Q1.3 fallback path §4.) |
| Helper text (below checkboxes, muted) | `Airbnb first because it gives us the richest data — we'll connect the others later.` |
| Primary CTA | `Continue` — commits the full channel list. Q1.3 is skipped; advance directly to Q1.4. |
| Cancel link (below primary CTA) | `Cancel edit — keep the original answer` |

### 3.5 Fallback state (no Salesforce data) — the safety net

**This is today's exact Q1.2 behavior, unchanged.** Identical to v2 spec §4.3 baseline — no chip, no attribution line, blank multi-select with helper text. The user sees no indication that prefill was attempted; the wizard simply renders as it does for accounts without Salesforce data.

| Element | Copy |
|---|---|
| Heading | `Are your listings on Airbnb only, or other channels too?` |
| Option A | `Airbnb only` |
| Option B | `Airbnb plus other channels` |
| Helper text | `We'll connect the other channels later. Airbnb first because it gives us the richest data.` |
| Primary CTA (auto-advance on selection per master spec form patterns) | (none — single-tap option commits and advances) |

**When fallback fires:**
- Salesforce returned no payload.
- Salesforce returned an empty `channels` array.
- Salesforce returned `channels` that omit `airbnb` entirely (data anomaly — the wizard's Q1.2 hypothesizes Airbnb is at least present).
- Salesforce returned malformed data (network error, schema mismatch, etc.).

In any of these cases, render the baseline — no user-facing error, no spinner, no "we couldn't load your sales call data" message. The fallback is invisible to the user.

---

## 4. Q1.3 — Channel confirmation (fallback path only)

**Q1.3 only renders when Q1.2 fell back to the baseline binary state** (no Salesforce data) and the user picked `Airbnb plus other channels`. In the prefilled path, Q1.3 is absorbed into Q1.2's edit state per §3.4 and never renders as a separate screen.

When Q1.3 does render, it's today's v2 §4.3a baseline — Airbnb locked-checked, all other channels unchecked, plus the `Other` inline reveal pattern below. No attribution line (there's no Salesforce data to attribute), no pre-checked channels.

### 4.1 Layout — fallback Q1.3

Identical to v2 spec §4.3a baseline — Airbnb locked-checked, every other channel unchecked, helper text intact, plus the `Other` inline-field reveal pattern from §3.4 (which is the same component, reused).

| Element | Copy / behavior |
|---|---|
| Heading | `Which channels are your listings on today?` |
| Subtitle | `Airbnb stays selected — we'll connect it on the next screen.` |
| Checkbox — Airbnb | `Airbnb` — **locked checked**, disabled. Tooltip on the disabled control: `Airbnb is your starting channel — we'll connect it on the next screen.` |
| Checkbox — Booking.com | `Booking.com` |
| Checkbox — Vrbo | `Vrbo` |
| Checkbox — Expedia | `Expedia` |
| Checkbox — Other | `Other` |
| Inline reveal under `Other` (only when checked) | A single-line text field with: label `Which channels?`, placeholder `e.g. Hostfully, Lodgify`, helper `Separate multiple channels with commas.`. Starts empty. Optional — empty submissions allowed. |
| Inline field commit | Commits on blur or `Enter`. Value persists to backend on `Continue`. |
| Inline field aria-label | `Which other channels are your listings on?` |
| `Other` unchecked → inline field collapses | Captured value preserved in component state — re-checking restores it. |
| Primary CTA | `Continue` |

### 4.2 Behavior — fallback Q1.3

| Trigger | Effect |
|---|---|
| User toggles a non-Airbnb checkbox | Selection registered. `Continue` stays enabled. |
| User unchecks every non-Airbnb channel | Soft inline prompt below the checkbox group: `Looks like you're only on Airbnb after all. Go back to update your previous answer?` with a link `Update previous answer` that returns to Q1.2 in its fallback state. Doesn't block continue. |
| User tries to uncheck Airbnb | Cannot — checkbox is locked. Tooltip explains. |
| `Continue` | Commits and advances to Q1.4. Triggers `wizard.answer_committed` with `source: 'user_input'`. |

---

## 5. Visual treatment — the prefill chip card

The chip card on Q1.2 default state is a visual pattern reused from Q1.1 and other prefilled questions. Spec for consistency:

| Element | Spec |
|---|---|
| Container | Arc surface card. Soft border (`gst-border` + `gst-border-muted`), padded `gst-p-6`, radius matches Arc default. |
| Background | Default surface (`gst-bg-card`) — not a special accent color. The chip pattern is informational, not promotional. |
| Attribution line typography | Muted foreground, body text size. Italic optional — match Arc's existing prefill chip use at Q1.1 for consistency. |
| Prefilled value display | Arc `Badge` (or pill) with a check icon to the left. Size: larger than the standard inline badge — needs to read as the answer, not a status tag. |
| Action row | Primary `Looks right` button + tertiary text-link `Change`. Side-by-side, left-aligned. |
| Animation on `Change` click | The badge fades out, the multi-select fades in. 200ms cross-fade. No layout shift if possible — the card height can stay constant. Reduced motion: instant swap. |
| Animation on `Cancel edit` click | Reverse — multi-select fades out, badge fades back in. |

---

## 6. State machine — Q1.2 with prefill

```
                  ┌─────────────────────┐
   Salesforce ──→ │  Prefill resolved?  │ ──No──→ Fallback Q1.2 (binary)
   data load      └──────────┬──────────┘                │
                             │ Yes                       │ Picks "Airbnb plus others"
                             ▼                           ▼
                  ┌─────────────────────┐       ┌─────────────────────┐
                  │   Default state     │       │  Fallback Q1.3      │
                  │   (specific list    │       │  (channel checkboxes,
                  │    pill + actions)  │       │   Airbnb locked)    │
                  └──────────┬──────────┘       └──────────┬──────────┘
                             │                             │ Continue
              Looks right ───┤                             │
                             │                             ▼
                             ▼                          Q1.4
                             ▼
                  ┌─────────────────────┐
                  │     Edit state      │ ──Continue──→ Q1.4 (Q1.3 skipped)
                  │  (channel checkbox  │
                  │   list, pre-checked)│
                  └──────────┬──────────┘
                             │ Cancel edit
                             ▼
                  ┌─────────────────────┐
                  │   Default state     │
                  │  (specific list     │
                  │   pill + actions)   │
                  └─────────────────────┘
```

**Key paths:**
- **Prefilled + confirmed** (the happy path for known accounts): chip → `Looks right` → Q1.4. Q1.3 never renders.
- **Prefilled + edited:** chip → `Change` → edit state with channel checkboxes pre-checked → `Continue` → Q1.4. Q1.3 still doesn't render — the edit state already captured what Q1.3 would have asked.
- **Fallback:** baseline Q1.2 binary → (optional) Q1.3 channel multi-select → Q1.4. Today's exact behavior, unchanged.

`Commit` is the same write semantic as a typed answer. Triggers:
- Branch lock per master spec FR-11.2.
- `wizard.answer_committed` event with `source: 'salesforce_prefill' | 'user_edit' | 'user_input'`.
- Auto-save per master spec form patterns.

---

## 7. Events and analytics

Add (or extend) the following events to the master spec's Event Taxonomy. Confirm exact field names against §Event Taxonomy before instrumenting.

| Event | When | Payload |
|---|---|---|
| `wizard.prefill_rendered` | Q1.2 (or Q1.3) renders in prefilled state | `{ question_id, prefilled_value, source: 'salesforce', source_call_date }` |
| `wizard.prefill_confirmed` | User clicks `Looks right` (Q1.2) or `Continue` without edits (Q1.3) | `{ question_id, prefilled_value, source_call_date }` |
| `wizard.prefill_edited` | User clicks `Change` then `Continue` with any edit, OR toggles any checkbox in Q1.3 | `{ question_id, prefilled_value, final_value, fields_changed }` |
| `wizard.prefill_cancelled` | User clicks `Change` then `Cancel edit` without changing anything | `{ question_id, prefilled_value }` |
| `wizard.prefill_fallback` | Prefill data was unavailable or anomalous; question rendered in baseline state | `{ question_id, reason: 'missing' \| 'anomalous' }` |

Why this matters: the `prefill_edited` rate tells us how often Salesforce is wrong. If it's high, the sales-team data hygiene is a problem — that's a finding worth surfacing.

---

## 8. Accessibility

| Concern | Spec |
|---|---|
| Focus on prefill render | Default focus lands on the `Looks right` primary CTA — keyboard users can confirm with `Enter` immediately. |
| Focus on `Change` click | After the cross-fade animation, focus moves to the multi-select option that matches the prefilled value. Polite live region announces: `Edit mode. Update your channels.` |
| Focus on `Cancel edit` click | After the cross-fade, focus returns to the `Looks right` button. Polite live region announces: `Original answer restored.` |
| Reduced motion | Cross-fade collapses to instant swap. No content changes. |
| Screen reader on prefill render | Polite live region announces: `Pre-filled from your sales call. Your channels: {prefilled value}. Confirm or change.` Fires once on initial render. |
| Disabled Airbnb checkbox at Q1.3 | Visible disabled style + tooltip per §4.1. Aria attribute: `aria-disabled="true"` and `aria-describedby` pointing to the tooltip text so screen readers announce why. |
| Contrast | All chip-card colors inherit from existing Arc tokens — no new color decisions needed. |

---

## 9. Copy register (consolidated)

| Where | Copy |
|---|---|
| Q1.2 heading (prefilled state) | `Your listings are on these channels` |
| Q1.2 heading (fallback state) | `Are your listings on Airbnb only, or other channels too?` |
| Q1.2 attribution — fresh (≤ 30 days or no date) | `Pre-filled from your sales call. Looks right?` |
| Q1.2 attribution — stale (> 30 days) | `Pre-filled from your sales call on {date}. Anything changed since?` |
| Q1.2 prefilled pill — 1 channel | `{channel}` (e.g. `Airbnb`) |
| Q1.2 prefilled pill — 2 channels | `{a} and {b}` (e.g. `Airbnb and Booking.com`) |
| Q1.2 prefilled pill — 3+ channels | `{a}, {b}, and {c}` — Oxford comma (e.g. `Airbnb, Booking.com, and Vrbo`) |
| Q1.2 prefilled pill — Other without captured names | `…, and one other channel` |
| Q1.2 primary CTA (default state) | `Looks right` |
| Q1.2 secondary CTA (default state) | `Change` |
| Q1.2 attribution (edit state) | `Update what's changed since your sales call.` |
| Q1.2 edit-state checkbox labels | `Airbnb` (locked), `Booking.com`, `Vrbo`, `Expedia`, `Other` |
| Q1.2 edit-state Airbnb disabled tooltip | `Airbnb is your starting channel — we'll connect it on the next screen.` |
| Q1.2 edit-state helper | `Airbnb first because it gives us the richest data — we'll connect the others later.` |
| Q1.2 edit-state primary CTA | `Continue` |
| Q1.2 edit-state cancel link | `Cancel edit — keep the original answer` |
| Q1.3 heading (fallback path only) | `Which channels are your listings on today?` |
| Q1.3 subtitle (fallback) | `Airbnb stays selected — we'll connect it on the next screen.` |
| Q1.3 Airbnb checkbox label | `Airbnb` |
| Q1.3 Airbnb disabled tooltip | `Airbnb is your starting channel — we'll connect it on the next screen.` |
| Q1.3 other channel labels | `Booking.com`, `Vrbo`, `Expedia`, `Other` |
| `Other` inline field label (Q1.2 edit state + Q1.3 fallback) | `Which channels?` |
| `Other` inline field placeholder | `e.g. Hostfully, Lodgify` |
| `Other` inline field helper | `Separate multiple channels with commas.` |
| `Other` inline field aria-label | `Which other channels are your listings on?` |
| Q1.3 only-Airbnb-left soft prompt | `Looks like you're only on Airbnb after all. Go back to update your previous answer?` |
| Q1.3 update-prev link | `Update previous answer` |
| Q1.3 primary CTA | `Continue` |
| Success toast on channel edit (any path) | `Channels updated` |
| Live region — prefill rendered | `Pre-filled from your sales call. Your channels: {prefilled value}. Confirm or change.` |
| Live region — entered edit mode | `Edit mode. Update your channels.` |
| Live region — cancelled edit | `Original answer restored.` |

---

## 10. Acceptance criteria

A prototype build passes this patch when:

- [ ] Q1.2 reads Salesforce prefill data on mount. If present and well-formed (non-empty `channels` array that includes `airbnb`), renders the prefilled chip card per §3.1.
- [ ] The prefilled heading reads `Your listings are on these channels` — NOT the original binary question.
- [ ] The pill shows the **specific channel list** formatted per §2:
  - 1 channel → channel name alone (`Airbnb`)
  - 2 channels → `{a} and {b}` (`Airbnb and Booking.com`)
  - 3+ channels → Oxford comma form (`Airbnb, Booking.com, and Vrbo`)
  - `Other` with captured names → unfold each name in line (`Airbnb, Booking.com, and Hostfully`)
  - `Other` without captured names → append `one other channel` (`Airbnb, Booking.com, and one other channel`)
- [ ] Clicking `Looks right` commits the full channel list and advances **directly to Q1.4**. Q1.3 is skipped.
- [ ] Clicking `Change` cross-fades the card into edit state (200ms; instant under reduced motion) — showing the **full channel checkbox list** with `airbnb` locked-checked and every Salesforce-supplied channel pre-checked.
- [ ] Edit state shows `Update what's changed since your sales call.` as the attribution and includes the `Cancel edit — keep the original answer` link.
- [ ] Clicking `Continue` from the edit state commits the channel selection and advances **directly to Q1.4** — Q1.3 is also skipped in this path.
- [ ] Clicking `Cancel edit` cross-fades back to the default chip state with the original prefill restored.
- [ ] **Fallback path (no Salesforce data):** Q1.2 renders today's baseline binary question with the original heading `Are your listings on Airbnb only, or other channels too?`. If the user picks `Airbnb plus other channels`, Q1.3 renders normally per v2 §4.3a baseline.
- [ ] Q1.3 (when rendered — fallback path only) shows Airbnb locked-checked with the disabled tooltip per §4.1; no other checkboxes pre-checked; no attribution line.
- [ ] Checking the `Other` checkbox (in Q1.2's edit state OR in fallback Q1.3) reveals an inline text field with label `Which channels?`, placeholder `e.g. Hostfully, Lodgify`, and helper `Separate multiple channels with commas.` In Q1.2's edit state the field is prefilled with `other_channel_names.join(', ')` if captured; in fallback Q1.3 the field starts empty.
- [ ] Unchecking `Other` collapses the inline field but preserves its value in component state — re-checking restores the value.
- [ ] The `Other` inline field is optional — `Continue` is enabled with or without a value entered.
- [ ] If the user unchecks every non-Airbnb channel at Q1.3 (fallback only), the soft prompt appears with an `Update previous answer` link routing back to Q1.2's fallback binary state.
- [ ] Toast `Channels updated` fires on advance from the edit state OR the fallback Q1.3 if and only if the user changed at least one checkbox or edited the `Other` field.
- [ ] Attribution line on Q1.2 uses the **fresh** copy when `source_call_date` is ≤ 30 days old or missing; uses the **stale** copy (with the date formatted as `Month DD, YYYY`) when older than 30 days.
- [ ] **Fallback (safety net):** when Salesforce returns no data, empty data, or anomalous data (missing `channels`, missing `airbnb` in `channels`, malformed payload), Q1.2 (and downstream Q1.3) render today's baseline behavior with **no user-facing error message** — no chip, no attribution line, no "couldn't load" text. The wizard behaves exactly as it does today for accounts without sales-call data.
- [ ] The five `wizard.prefill_*` events fire per §7 with the documented payloads.
- [ ] Focus management and polite live region announcements match §8.
- [ ] No exclamation marks anywhere.
- [ ] Sentence case for every label, heading, button, link, and tooltip.
- [ ] All copy matches §9 verbatim.

---

## 11. Resolved decisions (locked 2026-05-27)

1. **Data source.** Salesforce, via the existing wizard prefill payload. Field shape assumed in §2 — confirm with integration team before final hand-off.
2. **Affordances on the chip.** `Looks right` (primary) + `Change` (secondary). Matches the Q1.1 pattern already in v2 §15.3.
3. **`Change` semantics.** Reveals the multi-select with the prefilled value **pre-selected**, not erased. Treats the action as "edit," not "restart."
4. **Q1.3 coverage.** **Q1.3 is collapsed into Q1.2's edit state in the prefilled path** — it would have asked exactly what the Q1.2 pill already shows. Q1.3 only renders in the fallback path (no Salesforce data). When it does render, it's today's exact v2 §4.3a baseline plus the `Other` inline-field pattern.
5. **Fallback behavior — the safety net.** Missing, empty, or anomalous Salesforce data → render the v2 baseline blank state. **No error message, no spinner, no "we couldn't load" text.** The wizard behaves exactly as it does today for accounts without sales-call data. The prefill pattern is purely additive — it can never break the wizard.
6. **Commit semantics.** `Looks right` is a commit. Triggers branch lock per FR-11.2 and the same auto-save behavior as a typed answer.
7. **Edit-state copy.** `Update what's changed since your sales call.` — frames the action positively (refining what's known) rather than negatively (correcting what's wrong).
8. **Source-call date in attribution.** Show the date only when `source_call_date` is older than 30 days; use the **stale** attribution `Pre-filled from your sales call on {date}. Anything changed since?`. Fresh prefills (≤ 30 days) and prefills without a date use the cleaner `Pre-filled from your sales call. Looks right?`. Builds trust on recent data, honestly flags stale data.
9. **`Other` channel follow-up.** Inline reveal under the `Other` checkbox on Q1.3 — a single text field for the user to name which other channel(s), prefilled from `other_channel_names` if Salesforce captured them. **Not** a separate follow-up screen. Field is optional; empty submissions are allowed. Lightweight progressive disclosure rather than another full step.
10. **Salesforce confidence threshold.** **Trust all non-empty `channels` arrays.** No confidence-score gating, no rendering thresholds — if Salesforce returned channels, the chip renders. If sales-team data quality is a problem in practice, the `prefill_edited` event in §7 will surface it for ops review.
11. **Pill specificity.** The prefilled pill lists the **actual channels**, not a binary "Airbnb only / plus others" framing. List-formatting rules locked in §2: 1 channel = bare name, 2 = `{a} and {b}`, 3+ = Oxford-comma form, `Other` with captured names unfolds them inline, `Other` without names appends `one other channel`. The wasteful binary framing existed in earlier drafts; this revision retires it.

---

## 12. Remaining open questions

All four original open questions are now resolved (folded into §11 decisions 8–10 and the patch body). One residual deferral remains for product to revisit later:

1. **Multi-account Salesforce records.** **Deferred — not relevant for current scope.** When a single Salesforce contact owns multiple Guesty accounts with different channels, this patch assumes the integration layer resolves the right record before the wizard ever runs. If this becomes a real production scenario, revisit and add the rule (likely: account-id-matched record always wins; fall back to most-recently-updated).

---

## 13. Hand-off note

This patch lives alongside the Airbnb Connect, Fees, and Educational Expansion patches in `docs/planning-artifacts/`. Once the prototype agent picks it up:

- v2 spec §4.3 (Q1.2) and §4.3a (Q1.3) should be updated to point here as the canonical layouts.
- The §15.3 Salesforce-prefill chip pattern is unchanged — this patch instantiates that pattern; it doesn't redefine it.
- The Event Taxonomy section of the master spec should add the five `wizard.prefill_*` events from §7.
- The §18 audit table should note the Q1.2 layout change.

I'll fold all four patches into the next v2 spec sweep to keep the canonical doc accurate.
