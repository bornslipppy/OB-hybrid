---
title: "Q3.6 — Mandatory fees: 50/50 layout patch"
---

# Q3.6 — Mandatory fees: 50/50 layout patch

**Date:** 2026-05-27
**Author:** Sally (UX Designer)
**Audience:** Designer producing the Figma + agent building the prototype
**Applies to:** §6.7 of [`ux-design-specification-v2-atlas-aligned-2026-05-27.md`](ux-design-specification-v2-atlas-aligned-2026-05-27.md) — the single-panel `FeeBuilder` row pattern is replaced by the 50/50 layout below.
**Pattern sources:** *Filter / onboarding selector* (Udemy, Upwork, Apollo, Pinterest) as the primary interaction; *inline chip field* (Substack, Fireflies, Contra) as the input mechanic.
**Voice & copy standards:** Atlas — sentence case, no exclamation marks, glossary-compliant terminology, plain-language voice.

---

## 0. Why this patch exists

The current single-panel Fee Builder asks the user to name a fee, set an amount, and pick a unit all on one row. For users with five or six fees, that's a lot of small decisions stacked vertically. Splitting Q3.6 into **select-first, configure-second** reduces cognitive load and gives each panel a clear job:

- **Left panel** — discover and add the fee.
- **Right panel** — confirm what's in, then tune the numbers.

It also rhymes spatially with the Q1.4 Airbnb Connect 50/50 layout the user just saw in Section 1, reinforcing the wizard's visual rhythm.

---

## 1. Summary

| # | Delta | Why |
|---|------|-----|
| **P-1** | Replace the single-panel Fee Builder with a 50/50 split — left panel selects fees, right panel configures them | Reduces per-row cognitive load; matches Airbnb Connect's spatial rhythm |
| **P-2** | Left panel = autocomplete text field + suggestion chips below | Combines power-user typing with first-timer browsing |
| **P-3** | Right panel = card per fee, with `$` / `%` amount, charged-unit dropdown, and `×` to remove | Each fee is one card, not one row — easier to scan |
| **P-4** | Backspace on empty input removes the most recently added fee | Power-user shortcut; the `×` on each card stays as the always-visible affordance |
| **P-5** | Dictionary fees have non-editable names; custom-typed fees have editable names | Preserves taxonomy on the standard set; gives the user freedom on what they invent |

---

## 2. Layout

Single 50/50 horizontal split. **No canvas reveal** — this is a question surface, not a moment. Each panel scrolls independently when content exceeds viewport height. Below the wizard's lower viewport breakpoint, the panels stack vertically (left panel first, right panel below).

```
┌────────────────────────────────────┬────────────────────────────────────┐
│ LEFT — Pick fees                   │ RIGHT — Your fees                  │
│                                    │                                    │
│ Heading                            │ Heading + counter                  │
│ ──────────────                     │ ──────────────                     │
│ [ Search or add a fee…          ]  │  (empty)                           │
│                                    │  No fees added yet                 │
│ Suggestions                        │  Pick a fee on the left to start.  │
│ [ Cleaning fee ] [ Pet fee ]       │  I don't charge mandatory fees     │
│ [ Early check-in ] [ Resort fee ]  │                                    │
│ [ Late check-out ] [ Extra guest ] │  — or, when populated —            │
│ [ Linen fee ] [ +12 more ]         │                                    │
│                                    │  ┌─ Cleaning fee — × ───────────┐ │
│                                    │  │ Amount  [        ] ( $ | % ) │ │
│                                    │  │ Charged [ Per reservation  ▾]│ │
│                                    │  └──────────────────────────────┘ │
│                                    │                                    │
│                                    │  [ Continue ]                     │
└────────────────────────────────────┴────────────────────────────────────┘
```

---

## 3. Left panel — Pick fees

### 3.1 Heading

| Element | Copy |
|---|---|
| Heading (h2) | `What fees do you charge guests, on top of the nightly rate?` |
| Subtitle (muted, below heading) | `Pick from the list, or add your own. You can edit each fee on the right.` |

### 3.2 Search / add-your-own input field

A single text field that doubles as **search** (over the suggestion list and Guesty's autocomplete dictionary) and **add-your-own** (when the user types something not in the list and presses `Enter`).

| Element | Copy / behavior |
|---|---|
| Field label (visible, above the field) | `Your additional fees` |
| Placeholder | `Search or add a fee…` |
| Helper text (below field, muted) | `Start typing to see matches, or pick a suggestion below.` |
| Autocomplete source | **A flat list of fee names** provided by product. No defaults, no metadata — just strings. Dropdown matches by substring, case-insensitive. |
| Autocomplete dropdown — open trigger | Opens on focus and stays open while typing. Closes on blur, `Esc`, or selection. |
| Autocomplete dropdown — max visible | 8 rows visible at once; scrollable beyond. |
| Selection from dropdown | Click or `Enter` adds the fee to the right panel, clears the input, returns focus to the input for the next pick. |
| Free-text custom add | If the typed string doesn't match any dictionary entry, the last row of the dropdown reads `Add "{typed text}" as a custom fee`. Clicking it or pressing `Enter` adds the fee as a **custom entry** (see §5 — editable name). |
| Empty input + `Backspace` | Removes the most recently added fee from the right panel. If it came from the dictionary, the chip restores to the suggestions row in its original position. |
| Empty dropdown state (typed query has no matches) | `No matches. Press Enter to add "{query}" as a custom fee.` |
| Max-length soft validation | Soft limit 40 characters per fee name. Over: `Fee names work best under 40 characters.` (warning, doesn't block). |
| Loading state (only if autocomplete latency > 200 ms) | Top row of dropdown shows `Searching…` until results return. |

### 3.3 Suggestion chips (below the field)

Pre-populated set of common short-term-rental fees, acting as the *filter / onboarding selector* pattern — the user can pick without typing.

| Element | Copy / behavior |
|---|---|
| Section label (above chips, muted) | `Suggestions` |
| Default chips (initial order — confirm final list with product) | `Cleaning fee`, `Pet fee`, `Early check-in fee`, `Late check-out fee`, `Resort fee`, `Linen fee`, `Extra guest fee`, `Parking fee`, `Damage protection`, `City tax`, `Tourist tax`, `VAT` |
| Chip click | Adds that fee to the right panel; chip disappears from the suggestions row. |
| Chip keyboard | `Tab` to focus, `Space` or `Enter` to add. Visible focus ring matches Arc's `--gst-focus` token. |
| Overflow | If more than 8 suggestions remain, show 8 plus a `Show all` chip that expands the row inline (no dialog). |
| All suggestions selected | Hide the `Suggestions` section heading and the chip row entirely. The field stays. Field helper text becomes `Add another fee, or continue when you're done.` |
| Chip restore on remove | When a dictionary fee is removed from the right panel (via `×` or `Backspace`), its chip restores to the suggestions row in its original position. Custom fees don't restore — they vanish on removal. |

---

## 4. Right panel — Your fees

### 4.1 Heading

| Element | Copy |
|---|---|
| Heading (h3, paired with left panel's h2) | `Your fees` |
| Counter (right-aligned, muted, populated state only) | `{count} added` |

### 4.2 Empty state

| Element | Copy |
|---|---|
| Heading | `No fees added yet` |
| Body | `Pick a fee on the left to start. We'll let you set the amount and how it's charged.` |
| Secondary action (below body) | `I don't charge mandatory fees` — flat skip; advances to Q3.7. Records zero fees, no punch-list entry (skipping "I don't charge fees" is a real answer, not a deferral). |

The skip link is **only** visible in the empty state. Once any fee is added, it disappears and the `Continue` CTA appears at the bottom of the right panel.

### 4.3 Populated state — fee row anatomy

Each added fee renders as a card.

```
┌─ Cleaning fee                                              × ─┐
│                                                                │
│   Amount    [          ]   ( $ | % )                           │
│             In USD                                             │
│                                                                │
│   Charged   [ Per reservation                              ▾ ] │
└────────────────────────────────────────────────────────────────┘
```

| Element | Copy / behavior |
|---|---|
| Card heading — **dictionary fee** | The fee name. **Non-editable.** Rendered as plain text. |
| Card heading — **custom fee** | The fee name. **Editable inline.** Click the heading to enter edit mode (text becomes a single-line input). `Enter` or blur commits; `Esc` reverts. Pencil icon appears on hover/focus to signal affordance. Aria-label on the heading in display mode: `Edit fee name`. |
| Remove affordance | `×` in the top-right corner of the card. Accessible label: `Remove {fee name}.` On click: dictionary fees restore as suggestion chips on the left; custom fees vanish entirely. |
| Amount label | `Amount` |
| Amount input — placeholder | (empty — no placeholder value) |
| Amount input — default value | **Empty.** The user enters every amount. |
| Amount/unit toggle | Segmented control to the right of the amount field, two buttons: `$` and `%`. Defaults to `$`. Aria-labels: `Amount in {accountCurrency}` and `Amount as percentage of subtotal`. |
| Currency hint (below amount, when `$` selected, muted) | `In {accountCurrency}` |
| Percentage hint (below amount, when `%` selected, muted) | `Of the pre-tax subtotal` |
| Charged dropdown label | `Charged` |
| Charged dropdown default | **`Per reservation`** |
| Charged dropdown options | `Per reservation` · `Per night` · `Per guest, per night` |

### 4.4 Validation

| Trigger | Copy | Severity |
|---|---|---|
| Amount empty on blur | `Enter an amount.` | Blocking — disables `Continue`, marks the row with a destructive left edge. |
| Amount zero or negative | `Amount must be greater than zero.` | Blocking |
| Percentage above 100 | `Percentages must be 100 or less.` | Blocking |
| Outlier soft check — `$` over 200 per night | `That's higher than most accounts. Looks right?` + inline `Confirm` link | Soft — warning left edge, doesn't block |
| Outlier soft check — `$` over 500 per reservation | (same copy) | Soft |
| Outlier soft check — `%` over 50 | (same copy) | Soft |
| Custom fee name empty on commit | Revert to the previous name; no error message (user pressed Enter on an empty edit). | — |
| Custom fee name over 40 chars | `Fee names work best under 40 characters.` | Warning — doesn't block; lives below the heading while in edit mode |

### 4.5 Action row (bottom of right panel)

| Element | Copy |
|---|---|
| Primary CTA | `Continue` |
| Disabled tooltip (when any row has a blocking validation error) | `Fix the highlighted fees before you continue.` |

---

## 5. Editable name behavior — dictionary vs custom

This is the only place the two fee kinds diverge. Everything else (amount, unit, removal) behaves identically.

| Behavior | Dictionary fee | Custom fee |
|---|---|---|
| Source | Selected from suggestion chip or autocomplete match | Typed by the user via `Add "{query}" as a custom fee` |
| Card heading | Non-editable plain text | Editable inline — click to edit, `Enter` or blur to commit |
| Pencil affordance | Not shown | Visible on hover/focus next to the heading |
| On removal | Restores as a suggestion chip on the left panel | Vanishes entirely |
| Visual marker (subtle, optional) | None | Muted `Custom` chip next to the name, distinguishes them at a glance |

**Why:** dictionary names are part of Guesty's fee taxonomy — renaming "Cleaning fee" to "cleaning costs" breaks reporting downstream. Custom fees are the user's own naming — they should be able to refine the wording without re-adding the fee.

---

## 6. Cross-panel interactions

| Trigger | Effect |
|---|---|
| Click a suggestion chip | Chip animates into the right panel as a new card. Chip is removed from the suggestions row. Focus stays on the search field. |
| `Enter` on a dropdown autocomplete match | Same as suggestion-chip click. Input clears, focus stays. |
| `Enter` on the `Add "{query}" as a custom fee` row | New custom card appears on the right with the typed name. No chip is removed. Input clears, focus stays. |
| `Backspace` on empty input | Removes the most recently added fee. Dictionary fees restore to suggestions; custom fees vanish. |
| Click `×` on a card | Same as Backspace, but for that specific card. |
| `Tab` from the search field | Moves focus to the first suggestion chip. Then through chips left to right, then into the right-panel cards top to bottom. |
| `Tab` through a card | Order: (heading edit, custom only) → Amount field → `$` / `%` toggle → Charged dropdown → `×` remove → next card. |
| Screen reader — on add | Polite live region: `{Fee name} added. {count} fees total.` |
| Screen reader — on remove | Polite live region: `{Fee name} removed. {count} fees total.` |
| Screen reader — on outlier soft-check appearance | Polite live region: `{Fee name}: that's higher than most accounts. Confirm to keep it.` |

---

## 7. States — at a glance

| State | Where | Behavior |
|---|---|---|
| **Empty (no fees added)** | Right panel | Empty-state copy. Skip link visible. `Continue` CTA hidden. |
| **Loading suggestions** (rare) | Left panel | Skeleton chip row, three shimmer chips. No text label. |
| **Autocomplete loading** (only if > 200 ms) | Dropdown | Top row `Searching…` until results return. |
| **Populated, all valid** | Right panel | Cards stack vertically. `Continue` enabled. |
| **Populated, blocking validation on at least one card** | Right panel | Card(s) with errors get destructive left edge + inline messages. `Continue` disabled with tooltip. |
| **Populated, soft check on at least one card** | Right panel | Card(s) get warning left edge + `Looks right?` confirm link. `Continue` stays enabled. |
| **All suggestions selected** | Left panel | Suggestions section hides. Helper text updates to `Add another fee, or continue when you're done.` |
| **Custom fee in name-edit mode** | Right panel | Card heading becomes a single-line input. Pencil affordance hides while editing. Other card controls remain interactive. |
| **No fees, skip clicked** | Whole screen | Flat advance to Q3.7. Records zero fees. No punch-list entry. |

---

## 8. Copy register (consolidated, Atlas-compliant)

Every string in §3–§7 follows the UX Copy Specification v2's §2 standards: sentence case, no exclamation marks, no `Just / Simply / Kindly / Utilize`, glossary-compliant terminology (`guest`, `reservation`, `select`, `enter`, `remove` for reversible removal, `delete` reserved for permanent destruction).

Two copy strings that are easy to get wrong — pin these exactly:

- ❌ `Press Enter to add "{query}" as a new fee` → ✅ `Press Enter to add "{query}" as a custom fee` (matches the internal taxonomy term)
- ❌ `Fix the errors before continuing` → ✅ `Fix the highlighted fees before you continue.` (specific, user-perspective, terminal period because it's a complete sentence in a tooltip)

---

## 9. Acceptance criteria

A prototype build passes this patch when:

- [ ] Q3.6 renders as a 50/50 horizontal split — left panel for selection, right panel for configuration.
- [ ] Below the wizard's lower viewport breakpoint, the panels stack vertically (left first).
- [ ] Left panel shows the heading, subtitle, `Your additional fees` input field with `Search or add a fee…` placeholder, helper text, and a `Suggestions` chip row.
- [ ] Typing in the input opens an autocomplete dropdown showing substring matches from the flat fee-names list provided by product.
- [ ] If the typed string has no matches, the dropdown's last row reads `Add "{query}" as a custom fee` and pressing Enter adds it as a custom entry.
- [ ] Clicking a suggestion chip adds the fee to the right panel and removes the chip from the row.
- [ ] Backspace in an empty input removes the most recently added fee. Dictionary fees restore to suggestions; custom fees vanish.
- [ ] When all suggestions are selected, the `Suggestions` row hides and the field's helper text updates to `Add another fee, or continue when you're done.`
- [ ] Right panel empty state shows the empty-state heading + body + `I don't charge mandatory fees` skip link. `Continue` CTA is hidden.
- [ ] Each added fee renders as a card with a non-editable heading (dictionary) or editable heading (custom), an Amount field (empty default), a `$` / `%` segmented toggle (defaulting to `$`), and a `Charged` dropdown defaulting to `Per reservation`.
- [ ] Currency hint reads `In {accountCurrency}` when `$` is selected; percentage hint reads `Of the pre-tax subtotal` when `%` is selected.
- [ ] Custom fee headings are inline-editable — click to enter edit mode, `Enter` or blur commits, `Esc` reverts. Pencil icon shows on hover/focus.
- [ ] Each card has a `×` in the top-right corner labeled `Remove {fee name}`. Removing a dictionary fee restores its chip to the left; removing a custom fee vanishes it.
- [ ] Amount-empty-on-blur, amount-zero-or-negative, and percentage-over-100 trigger blocking validation with the copy from §4.4 and disable `Continue` with the tooltip `Fix the highlighted fees before you continue.`
- [ ] Outlier amounts trigger soft check `That's higher than most accounts. Looks right?` with a `Confirm` link inline; `Continue` stays enabled.
- [ ] Adding and removing fees announce via a polite live region using the copy from §6.
- [ ] Tab order: search field → suggestion chips (left-to-right) → right-panel cards top-to-bottom → fields within each card in the order specified in §6.
- [ ] Every string matches the Atlas-aligned copy in §3–§5 verbatim.
- [ ] No exclamation marks anywhere on the screen.
- [ ] Sentence case for every label, heading, button, and chip.

---

## 10. Resolved decisions (locked 2026-05-27)

1. **Autocomplete source.** A flat list of fee names is provided by product. No metadata, no pre-populated amounts or units.
2. **Default amount.** Empty. The user enters every amount themselves — no opinionated defaults.
3. **Default unit.** `Per reservation`.
4. **Fee name editability.** Dictionary fees (selected from chips or autocomplete) are **non-editable**. Custom fees (typed via `Add "{query}" as a custom fee`) are **inline-editable** in the card heading.
5. **Per-listing override reassurance.** **Not included** on this screen. The master spec covers per-listing overrides downstream; adding a reassurance line here would dilute the one-idea-per-screen principle.

---

## 11. Hand-off note

This patch lives alongside the Airbnb Connect patch in `docs/planning-artifacts/`. Once the prototype agent picks it up, the UX Copy Specification v2's §6.7 should be updated to point here as the canonical layout for Q3.6. I'll fold the layout change into v2's audit table (§18) as part of the next spec sweep so the audit stays accurate.
