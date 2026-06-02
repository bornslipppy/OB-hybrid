---
title: "Welcome screen patch (S0)"
---

# Welcome screen patch (S0)

**Date:** 2026-05-27
**Author:** Sally (UX Designer)
**Audience:** Designer producing the Figma + agent building the prototype
**Applies to:** §3 (wizard structure overview) and §4 (Section 1) of [`ux-design-specification-v2-atlas-aligned-2026-05-27.md`](ux-design-specification-v2-atlas-aligned-2026-05-27.md). Adds a new Section 0 (S0) ahead of Q1.1.
**Voice & copy standards:** Atlas — sentence case, no exclamation marks, glossary-compliant terminology, plain-language voice.
**Tone:** *Keep it Light* (Atlas tone persona for welcome moments) layered on the standard Humble Expert voice.

---

## 0. Why this patch exists

The wizard currently opens cold on `How many active listings do you have?` — a question with no introduction, no context, and no signal of what's about to happen. Users arriving from the dashboard or a Salesforce hand-off email have no idea:

- How long this takes.
- That answers save automatically.
- That most of it is pre-filled from their sales call.
- Who their CSM is or what comes next.

A 30-second welcome screen fixes all four. It's not a marketing surface — it's an expectation-setting surface.

---

## 1. Summary

| # | Delta | Why |
|---|------|-----|
| **P-1** | Add a new **Section 0 (S0)** welcome screen as the wizard's entry point | Users need context before the first question |
| **P-2** | Single-panel, single-CTA layout — heading, two short paragraphs, a four-item "what to expect" list, optional CSM line, primary `Start setup` CTA | Simple, scannable, low-effort to read |
| **P-3** | Returning users skip S0 if they've already committed Q1.1 | Don't make a finished step re-introduce itself |
| **P-4** | Returning users who haven't started yet (saved state, no Q1.1 commit) see a `Welcome back` variant | Honors the resume-where-you-left-off pattern |
| **P-5** | Knock-on change: Q1.1's bot copy drops the `Welcome.` opener since the welcome now happens on S0 | Two welcomes in a row is awkward |

---

## 2. Where S0 fits in the wizard

```
Dashboard / SF hand-off email
        │
        ▼
  ┌────────────┐
  │ S0 Welcome │ ◄── new
  └─────┬──────┘
        │ Start setup
        ▼
  ┌────────────┐
  │ Q1.1 Active│
  │ listing    │
  │ count      │
  └─────┬──────┘
        │
        ▼
      … (rest of wizard unchanged)
```

S0 is **not counted in the section progress indicator** — Sections 1 through 8 stay as the user-facing progress count. S0 is the entry; Sections 9 and 10 are outcomes; the wizard's *configuration* is Sections 1–8.

---

## 3. Layout

Single-panel, no canvas. Centered or left-aligned within the wizard surface — match the alignment used by question screens for visual continuity. No section nav header on S0 (the user isn't in a section yet).

```
┌────────────────────────────────────────────────────────────┐
│                                                            │
│  Welcome, Yair.                                            │
│  ──────────────                                            │
│                                                            │
│  Let's set up Guesty to match how you run your business.   │
│  We'll move through eight short sections — most of it      │
│  pre-filled from your sales call, so you're mostly         │
│  confirming what we already know.                          │
│                                                            │
│  Takes about 15 minutes. Your answers save as you go —     │
│  leave and come back any time.                             │
│                                                            │
│                                                            │
│  Here's what we'll cover                                   │
│                                                            │
│   ✓ Connect your Airbnb account                            │
│   ✓ Confirm how you handle operations and finances         │
│   ✓ Set up your booking website and brand                  │
│   ✓ Pick what to focus on with your CSM                    │
│                                                            │
│                                                            │
│  Your first call: Maria Hernandez · June 3 at 2:00 PM EST  │
│                                                            │
│                                                            │
│  [ Start setup ]                                           │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### Typography

- **Heading:** large display — recommended `gst-text-4xl` (~36px), `gst-font-semibold`, `gst-leading-tight`. Bigger than the rest of the wizard's h2s — this is the front door.
- **Body paragraphs:** standard body size (~16px), generous line-height (`gst-leading-relaxed`), max-width ~`60ch` to keep line length readable.
- **List header:** small caps optional, or just a muted h3 (`gst-text-base`, `gst-font-medium`, muted color) — clearly subordinate to the welcome heading.
- **List items:** body size, parallel structure (each starts with a verb).
- **CSM line:** body size, muted foreground.
- **CTA:** Arc primary button, default size.

### Spacing

- `gst-mt-8` between heading and first paragraph.
- `gst-mt-4` between paragraphs.
- `gst-mt-12` between body paragraphs and the "what we'll cover" list.
- `gst-mt-8` between the list and the CSM line.
- `gst-mt-12` between the CSM line (or list, if no CSM) and the CTA.

The screen breathes — this is a moment, not a form.

---

## 4. Copy register

### 4.1 Heading

| Condition | Copy |
|---|---|
| First name available from Salesforce or Guesty account | `Welcome, {first_name}.` |
| First name not available | `Welcome to Guesty.` |

Period at the end is intentional — it's a complete sentence, not a label. No exclamation mark.

### 4.2 Body

| Element | Copy |
|---|---|
| Paragraph 1 — purpose | `Let's set up Guesty to match how you run your business. We'll move through eight short sections — most of it pre-filled from your sales call, so you're mostly confirming what we already know.` |
| Paragraph 1 fallback (no Salesforce data) | `Let's set up Guesty to match how you run your business. We'll move through eight short sections.` |
| Paragraph 2 — time + save | `Takes about 15 minutes. Your answers save as you go — leave and come back any time.` |

### 4.3 "What we'll cover" list

| Element | Copy |
|---|---|
| List header (small muted h3) | `Here's what we'll cover` |
| Item 1 | `Connect your Airbnb account` |
| Item 2 | `Confirm how you handle operations and finances` |
| Item 3 | `Set up your booking website and brand` |
| Item 4 | `Pick what to focus on with your CSM` |

Four items, parallel structure (each starts with a verb), each in sentence case. Bullet glyph: a small check or chevron, not a dot — signals "you'll do this," not "here's a list of things." Use `lucide-react`'s `Check` icon stroke-only, sized to match the body text x-height.

The list groups the wizard's 8 sections into 4 user-readable buckets (operations + finances paired, booking-website + governance + business paired, etc.). Don't try to enumerate all 8 — that's information overload before the user has done anything.

### 4.4 CSM line (conditional)

| Condition | Copy |
|---|---|
| CSM name AND first-call date both available | `Your first call: {csm_name} · {date} at {time} ({timezone})` |
| CSM name available, no call scheduled yet | `Your CSM: {csm_name} — they'll email you to schedule your first call.` |
| Neither available | (omit the line entirely) |

Date format: `Month DD` (e.g. `June 3`). Time format: `H:MM AM/PM` (e.g. `2:00 PM`). Timezone in parentheses, abbreviated (`EST`, `PST`, etc.) — Atlas style §dates.

### 4.5 CTA

| Element | Copy |
|---|---|
| Primary CTA | `Start setup` |
| Primary CTA — returning user with saved state but no Q1.1 commit | `Pick up where you left off` |

Verb + object, sentence case, no terminal punctuation. Atlas-compliant.

Considered and rejected:
- `Get started` — generic, doesn't say *what* gets started.
- `Let's go` — chummy, not specific.
- `Begin` — one word, no object.
- `Continue` — implies the user was already in the wizard; only true for the returning-user variant.

### 4.6 Returning-user variant — "Welcome back"

If a user has saved state but hasn't committed Q1.1 yet, the heading and body shift to a returning frame:

| Element | Copy |
|---|---|
| Heading | `Welcome back, {first_name}.` (or `Welcome back to Guesty.` if no name) |
| Paragraph 1 | `Your progress is saved. We'll drop you back in where you left off — most of it is already pre-filled from your sales call.` |
| Paragraph 2 | (omit — they already know the wizard saves) |
| "What we'll cover" list | (keep — they may need the reminder) |
| CSM line | (keep if data is available) |
| Primary CTA | `Pick up where you left off` |

If the user has already committed Q1.1, **S0 is skipped entirely** — the wizard opens on the question they last interacted with.

---

## 5. Behavior

| Trigger | Effect |
|---|---|
| First visit (no saved state) | Render S0 with the default copy from §4.1–§4.5. |
| Returning, saved state, no Q1.1 commit | Render S0 in the `Welcome back` variant per §4.6. |
| Returning, Q1.1 already committed | **Skip S0.** Open the wizard at the last-interacted question. |
| Click `Start setup` (or `Pick up where you left off`) | Advance to Q1.1 (or the last-interacted question on resume). Fire `wizard.started` event with `entry_source: 'welcome'` and `is_returning: true|false`. |
| Click browser back from Q1.1 | Returns to S0 — same state as before. Welcome is part of the navigable history. |
| Page refresh on S0 | Re-renders S0 in its current variant. No data loss — no answers were committed yet. |
| Salesforce data partial (e.g. first name yes, CSM no) | Render whichever conditional elements have data; omit the rest cleanly. No "Loading…" or "—" placeholders. |

---

## 6. Salesforce / data dependencies

S0 reads (but never blocks on) the following fields. If any are absent, the screen falls back gracefully per §4:

| Field | Used for | Fallback if missing |
|---|---|---|
| `user.first_name` | Heading personalization | Generic `Welcome to Guesty.` heading |
| `wizard_prefill.has_any_prefilled_data` (boolean) | Decides whether paragraph 1 mentions "pre-filled from your sales call" | Drop the second clause; keep `Let's set up Guesty to match how you run your business. We'll move through eight short sections.` |
| `csm.name` | CSM line | Omit CSM line |
| `csm.first_call_date` + `csm.first_call_time` + `csm.first_call_timezone` | "Your first call" variant of CSM line | Use the "they'll email you to schedule" variant if `csm.name` is available; otherwise omit |
| `wizard.last_committed_question_id` | Decides between first-visit, welcome-back, and skip-S0 paths | First-visit path |

S0 must render **without blocking** on these fields. If the data is still loading, render the generic-fallback variant immediately — never show a spinner on the welcome screen. A slow welcome screen is the worst first impression.

---

## 7. Knock-on change — Q1.1 bot copy

The v2 spec's Q1.1 anchor bot currently reads:

> `Welcome. We'll pull most of this in automatically — you'll just confirm what's right.`

With S0 owning the welcome moment, the `Welcome.` opener on Q1.1 becomes redundant and slightly off — the user just said hello on S0, now we say hello again? Update Q1.1's bot to drop the welcome and lead with the action:

| Where | Old copy | New copy |
|---|---|---|
| §4.2 Q1.1 anchor bot (v2 spec) | `Welcome. We'll pull most of this in automatically — you'll just confirm what's right.` | `We've pulled most of this in automatically — you'll just confirm what's right.` |

Tiny edit — one word dropped, tense shifted from future (`We'll pull`) to present-perfect (`We've pulled`). Reads cleaner now that the user is past the welcome and into the first question.

---

## 8. Accessibility

| Concern | Spec |
|---|---|
| Document title | `Welcome to Guesty — set up your account` (browser tab; uses generic heading even when personalized) |
| Heading hierarchy | S0 owns the only h1 on the wizard. Q1.1 onward use h2 for question headings. |
| Initial focus | On the primary CTA (`Start setup`). Keyboard users can press Enter immediately to begin. |
| Screen-reader announcement on render | The full heading + paragraph 1 reads aloud on page load (no special live-region needed — standard document landmark behavior). |
| CTA aria-label | None needed — the visible button text is descriptive. |
| List semantics | Use a real `<ul>` with `<li>` items so screen readers announce "list of 4 items." |
| Check icon on list items | `aria-hidden="true"` — decorative; the list semantics carry the meaning. |
| Reduced motion | No animations on S0. Pure layout. Nothing to scale back. |
| Contrast | All text uses the wizard's standard foreground tokens on the standard background — no new color decisions. |

---

## 9. States

| State | When | What renders |
|---|---|---|
| **Default (first visit)** | No saved wizard state | Full S0 with personalized heading (if available), both paragraphs, the list, the CSM line (if available), and `Start setup` CTA. |
| **Returning — not yet started** | Saved state but no Q1.1 commit | "Welcome back" variant per §4.6. |
| **Returning — in progress** | Q1.1 (or later) already committed | **S0 skipped.** Wizard opens on the last-interacted question. |
| **Data still loading** | Prefill API hasn't returned yet | Render the generic-fallback variant immediately. Do not show a spinner. |
| **No name, no CSM, no prefill** | New account with no enrichment data | `Welcome to Guesty.` + the no-prefill paragraph 1 + paragraph 2 + the list + the CTA. No CSM line. |

---

## 10. Acceptance criteria

A prototype build passes this patch when:

- [ ] S0 renders as the wizard's entry point — between dashboard/email arrival and Q1.1.
- [ ] S0 is **not** counted in the section progress indicator. Sections 1–8 remain the user-facing progress count.
- [ ] Heading reads `Welcome, {first_name}.` when first name is available, otherwise `Welcome to Guesty.` — period at the end, no exclamation mark.
- [ ] Paragraph 1 mentions "pre-filled from your sales call" when `wizard_prefill.has_any_prefilled_data` is true; drops that clause otherwise.
- [ ] Paragraph 2 reads `Takes about 15 minutes. Your answers save as you go — leave and come back any time.` exactly.
- [ ] The "what we'll cover" list renders four items in the order specified in §4.3, each prefixed with a `Check` icon and aria-hidden.
- [ ] CSM line renders only when at least `csm.name` is available; chooses the "first call" variant or the "they'll email you to schedule" variant based on whether call data is present.
- [ ] Primary CTA reads `Start setup` (first-visit) or `Pick up where you left off` (returning, no Q1.1 commit).
- [ ] Returning users with Q1.1 already committed **never see S0** — the wizard opens on the last-interacted question.
- [ ] Initial focus lands on the primary CTA.
- [ ] No spinner is shown on S0 — if data is loading, the generic fallback renders immediately.
- [ ] The browser back button from Q1.1 returns to S0 cleanly.
- [ ] Q1.1's anchor bot copy is updated to `We've pulled most of this in automatically — you'll just confirm what's right.` (dropping the `Welcome.` opener).
- [ ] `wizard.started` event fires on `Start setup` click with `entry_source: 'welcome'` and `is_returning: true|false`.
- [ ] No exclamation marks anywhere on the screen.
- [ ] Sentence case for every label, heading, button, and list item.
- [ ] All copy matches §4 verbatim.

---

## 11. Resolved decisions (locked 2026-05-27)

1. **S0 is the new wizard entry point.** A welcome screen sits between dashboard/email arrival and Q1.1.
2. **Single primary CTA.** `Start setup` (first-visit) or `Pick up where you left off` (returning). No secondary CTA — keep the screen focused.
3. **Personalization is graceful.** Heading personalizes with first name when available; falls back cleanly. CSM line is conditional; absent if no data.
4. **Returning-user behavior.** Saved state but no Q1.1 commit → "Welcome back" variant. Q1.1 already committed → skip S0 entirely.
5. **Not counted in section progress.** S0 is the entry; the configuration is Sections 1–8 (and the outcome screens are 9 and 10).
6. **No spinner.** S0 renders the generic fallback immediately if data isn't ready. A loading welcome is a bad welcome.
7. **Q1.1 bot copy updated.** Drops the `Welcome.` opener since S0 owns the welcome.
8. **No exclamation marks.** Welcome moments are excluded from Atlas's "max one per success state" allowance — the welcome screen is the front door of a long workflow, not a moment of triumph.

---

## 12. Open questions

1. **Visual treatment beyond typography.** A simple welcome screen reads as serious and professional. Should it have a subtle illustration (hero image, motif, brand graphic) to add warmth? Defer to product/brand — recommendation is to ship the type-only version first and add visuals only if user testing surfaces a "feels cold" finding.
2. **Estimated time accuracy.** `Takes about 15 minutes` is the v2 spec's target. If real-world data shows the median is consistently 12 or 18, update the copy here to match — don't let the welcome promise something the wizard doesn't deliver.
3. **CSM call data freshness.** If the `csm.first_call_date` is in the past at S0 render time (rescheduling lag, stale data), what do we show? Recommended: fall back to the "they'll email you to schedule" variant rather than display a stale date. Confirm with integration team.

---

## 13. Hand-off note

This patch lives alongside the Airbnb Connect, Fees, Educational Expansion, and Channels Prefill patches in `docs/planning-artifacts/`. Once the prototype agent picks it up:

- v2 spec §3 (wizard structure overview) should add a row for S0 before Section 1.
- v2 spec §4 should add a new §4.0 covering S0, then renumber the existing §4.1–§4.7 (or leave the question numbering and just prepend a §4.0 — whichever the spec sweep prefers).
- v2 spec §4.2 (Q1.1) should update the bot copy per §7 of this patch.
- The wizard's section-progress component should be configured to skip S0 from the visible count (still "Section 1 of 8" on Q1.1).

I'll fold all five patches into the next v2 spec sweep so the canonical doc stays accurate.
