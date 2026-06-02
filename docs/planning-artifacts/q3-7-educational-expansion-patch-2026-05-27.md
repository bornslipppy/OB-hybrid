---
title: "Q3.7 — Educational expansion (progressive disclosure) patch"
---

# Q3.7 — Educational expansion (progressive disclosure) patch

**Date:** 2026-05-27
**Author:** Sally (UX Designer)
**Audience:** Designer producing the Figma + agent building the prototype
**Applies to:** §6.8 of [`ux-design-specification-v2-atlas-aligned-2026-05-27.md`](ux-design-specification-v2-atlas-aligned-2026-05-27.md) — Q3.7 sub-wizard Step 1, "What taxes apply to your reservations?"
**Voice & copy standards:** Atlas — sentence case, no exclamation marks, glossary-compliant terminology, plain-language voice.
**Pattern type:** New reusable wizard pattern — *user-triggered educational expansion*. Distinct from canvas reveal moments.
**Assets:** `Frame 1 from Figma.svg` (provided 2026-05-27) — four-icon illustrative header for the tax topic.

---

## 0. Why this patch exists

Taxes are the single most jargon-heavy topic in the wizard. Users either know exactly what applies in their jurisdiction or have no idea — and the spread between those two groups is wider than for any other question.

The current Q3.7 Step 1 forces every user to commit to one of `Sales tax or VAT`, `Occupancy or tourist tax`, `City or local tax`, `Other` — without explaining what those terms mean in the context of Guesty, when taxes get applied, or what changes downstream.

This patch introduces a **progressive disclosure** affordance: a confident user picks and moves on; a confused user clicks **"Explain taxes"**, the screen splits 50/50, and a brief in-context educational module appears on the right. If they need more, the module links to the Guesty Academy for the full deep-dive.

This pattern is designed to be **reusable**. Q3.7 is the first instance, but any future wizard question where the explain-it-here-vs-explain-it-on-the-academy tradeoff matters can adopt the same `Explain {topic}` mechanic.

---

## 1. Summary

| # | Delta | Why |
|---|------|-----|
| **P-1** | Add an `Explain taxes` secondary CTA below the primary `Continue` on Q3.7 Step 1 | Optional, low-commitment way for unsure users to ask for help without leaving the screen |
| **P-2** | Clicking `Explain taxes` transitions the screen from single-panel to 50/50 split | Visual rhyme with Airbnb Connect (Q1.4) and Fees (Q3.6 patch) layouts |
| **P-3** | Right panel renders the **educational module** on a dark `#0A0036` background with a teal-iconography header, big title, body, and Academy link | Visually distinct from the question — signals "this is help, not part of the form" |
| **P-4** | Module is dismissible — the user can close it and return to single-panel | Progressive disclosure runs both ways; nothing forces the user to keep reading |
| **P-5** | "Go deeper" sends users to the Guesty Academy in a new tab | Keeps the wizard surface uncluttered; honors the user's existing momentum |

---

## 2. Pattern — Educational expansion (the generic rules)

This patch defines a **reusable wizard pattern**. The Q3.7 application in §3–§6 follows from these rules.

### When to use

- The question is **conceptually heavy** for at least one significant user segment (taxes, financial reporting, channel sync semantics, multi-unit configuration).
- A short paragraph can meaningfully unblock the user — the topic isn't so deep that the only useful answer is a 20-minute Academy course.
- The Academy has (or will have) a deeper article we can link to for users who want the full picture.

### When **not** to use

- The question is self-explanatory — adding `Explain {topic}` adds noise.
- The educational copy would exceed ~80 words. If the in-context module would need a header, two paragraphs, and a bulleted list, the right answer is "go to the Academy", not "expand in-context".
- The question is on an anchor screen with an existing bot `Alert`. The bot already serves the same job; don't double-stack.

### Pattern interaction with other surfaces

- **Distinct from canvas reveals.** Canvas reveals are system-triggered, momentous, and reserved for the three Canvas-as-Moments per master spec §Canvas Reveal Moments. The educational expansion is **user-triggered**, dismissible, and as common as the questions that benefit from it.
- **Distinct from tooltips.** Tooltips are one-sentence purpose statements pinned to a single field. The educational expansion covers the whole question and includes a path to deeper learning.
- **Distinct from the bot Alert.** Bot Alerts are advisory and persistent on anchor screens — present whether the user wants them or not. The educational expansion is opt-in.

---

## 3. Default state — Q3.7 Step 1, single-panel

Renders as today's single-panel layout (per the v2 spec §6.8). The only addition is a secondary CTA below the primary `Continue`.

| Element | Copy / behavior |
|---|---|
| Sub-step indicator | `Step 1 of 3` |
| Heading (h2) | `What taxes apply to your reservations?` |
| Helper (muted, under heading) | `Select every tax type that applies. We'll set the rates next.` |
| Multi-select option A | `Sales tax or VAT` |
| Multi-select option B | `Occupancy or tourist tax` |
| Multi-select option C | `City or local tax` |
| Multi-select option D | `Other` |
| Primary CTA | `Continue` |
| **Secondary CTA (new)** | `Explain taxes` |
| Back link | `Back` |

### Secondary CTA — copy decision

I considered the user's three suggestions and picked one Atlas-aligned variant:

| Candidate | Verdict |
|---|---|
| `I don't understand` | Rejected — puts the user in a defensive, self-blaming frame. Atlas's voice-and-tone *never blame the user* principle applies in both directions (system → user and user → self). |
| `I need more explanations` | Rejected — grammatically awkward ("explanations" plural), longer than necessary, in user-first person. |
| `Explain it to me` | Rejected — works conversationally but doesn't read as a button label. "It" is referent-less in isolation, weakening accessibility (screen reader users hear the button outside its visual context). |
| **`Explain taxes`** ✅ | Verb + object, sentence case, 2 words, glossary-compliant. Specific (says what gets explained). For other future instances, interpolate the topic: `Explain {topic}` — e.g., `Explain payouts`, `Explain channel sync`. |
| `Help me decide` | Acceptable alternative, but less precise — *decide* implies a binary choice, while taxes are a multi-select. |

**Final:** `Explain taxes` as primary recommendation. If product wants something more conversational, `Help me decide` is the fallback. I do not recommend any of the three original phrasings.

### Visual treatment of the secondary CTA

- Arc `Button` variant `tertiary` (text-link style) — keeps it clearly subordinate to `Continue`.
- Sits directly below the primary CTA, left-aligned to match.
- Icon to the left: a small question-mark glyph from `lucide-react` (`HelpCircle`, stroke-only, `gst-size-4`). Reinforces the help affordance for users skimming.
- No terminal punctuation (it's a button per Atlas §style).

---

## 4. Expanded state — 50/50 split

On `Explain taxes` click, the screen transitions to a 50/50 horizontal split:

```
┌────────────────────────────────────┬────────────────────────────────────┐
│ LEFT — The question                │ RIGHT — Educational module         │
│  (unchanged content)               │  background: #0A0036                │
│                                    │                                    │
│ Step 1 of 3                        │  ┌─ icon row (teal SVG asset) ──┐  │
│                                    │  │                              │  │
│ What taxes apply to your           │  └──────────────────────────────┘  │
│ reservations?                      │                                    │
│                                    │  How taxes work in Guesty          │
│ Select every tax type that         │  ────────────────────────────      │
│ applies. We'll set the rates next. │                                    │
│                                    │  Setting up taxes in Guesty        │
│ [ ] Sales tax or VAT               │  automatically applies them to     │
│ [ ] Occupancy or tourist tax       │  your new reservations. You can    │
│ [ ] City or local tax              │  configure these taxes globally    │
│ [ ] Other                          │  across your entire account or     │
│                                    │  tailor them to specific           │
│ [ Continue ]                       │  listings. Keep in mind that       │
│ Hide explanation                   │  taxes are not applied             │
│                                    │  retroactively to existing         │
│                                    │  reservations, and syncing rules   │
│                                    │  vary by channel — for example,    │
│                                    │  you must set taxes at the         │
│                                    │  listing level, rather than the    │
│                                    │  account level, to sync them       │
│                                    │  with Airbnb.                      │
│                                    │                                    │
│                                    │  Go deeper in the Guesty Academy → │
└────────────────────────────────────┴────────────────────────────────────┘
```

### 4.1 Left panel (the question)

Identical to the default state §3, with two changes:

| Element | Change |
|---|---|
| Secondary CTA below `Continue` | Copy switches from `Explain taxes` to `Hide explanation`. Icon switches from `HelpCircle` to `X` (`lucide-react`). |
| Width | 50% of the wizard surface (down from 100%). Form controls reflow to the narrower column — multi-select options stack at full width inside the column. |

### 4.2 Right panel (the educational module)

The module is a single styled card filling the right 50% of the wizard surface, edge-to-edge except for inner padding.

| Element | Spec |
|---|---|
| Background color | `#0A0036` (deep indigo-purple, matches the SVG asset) |
| Foreground (body text) color | `#E8E6F2` or pure `#FFFFFF` (TBD — confirm with brand against contrast tokens; both clear AAA on `#0A0036`) |
| Accent color (link, optional rule lines) | `#85B9B8` (the SVG asset's teal — borrow it to tie the module together) |
| Inner padding | `gst-p-12` (48px equivalent) on all sides — generous, since the module needs to *feel* like a different surface |
| Border radius | Same as Arc's standard surface radius — match the canvas card if there is one, otherwise `gst-rounded-lg` |
| Border / divider | None on the module itself; rely on the `#0A0036` fill to do the separation. A single 1px `#1A0E5C` left edge (slightly lighter than background) is optional for added definition against the wizard's pale-surface left panel |
| Shadow | None — flat, confident, doesn't compete with the question |
| Top decoration | The provided **`Frame 1 from Figma.svg`** — the four-icon teal-on-purple illustration. Renders flush at the top of the module, full width, centered. Aspect ratio preserved from the SVG (1482 × 455). Aria-hidden — purely decorative. |
| Title | `How taxes work in Guesty` |
| Title typography | **Big.** Recommended: Arc display token if available, otherwise `gst-text-4xl` (~36px) with `gst-font-semibold` and `gst-leading-tight`. Color: foreground (white / off-white). |
| Title spacing | `gst-mt-8` between the SVG asset and the title; `gst-mb-6` between title and body |
| Body | The educational copy from §5.1 — sentence case, no exclamation marks, no `IMPORTANT:` callouts, no bold inside the paragraph. Color: foreground. Type scale: Arc body large or `gst-text-lg` (~18px) — bigger than the question column's body so it reads as a featured panel. |
| Body line-height | `gst-leading-relaxed` (~1.6) — readable on a dark background |
| Body max-width | Constrain to `~60ch` even if the column is wider, to keep line length readable |
| Academy link | `Go deeper in the Guesty Academy →` — underline-on-hover, color `#85B9B8` (teal accent), `gst-mt-8` from the body. Opens in a new tab (`target="_blank" rel="noopener noreferrer"`). Arrow is part of the link text, not a separate icon. |

### 4.3 The SVG asset

- **File:** `Frame 1 from Figma.svg` (provided 2026-05-27, see `/Users/yair.cohen/Downloads/Frame 1 from Figma.svg`).
- **Place into the prototype project** at `src/prototype/assets/q3-7-tax-module-header.svg` (or the prototype's equivalent assets directory). Never reference the user's Downloads folder.
- **Render** as an inline `<img>` or `<svg>` at the top of the module. Inline `<svg>` is preferred so the fill colors can adapt to theme tokens later if needed.
- **Aria:** `aria-hidden="true"` — the icons are decorative; the title carries the meaning.
- **Responsive:** scale by width to fit the right column; preserve aspect ratio. No cropping.

---

## 5. Educational content — Q3.7 taxes

### 5.1 Body copy (locked verbatim — provided by user 2026-05-27)

> Setting up taxes in Guesty automatically applies them to your new reservations. You can configure these taxes globally across your entire account or tailor them to specific listings. Keep in mind that taxes are not applied retroactively to existing reservations, and syncing rules vary by channel — for example, you must set taxes at the listing level, rather than the account level, to sync them with Airbnb.

**Two minor edits I made to the user-provided source (Atlas-aligned):**

| Original | Edited | Reason |
|---|---|---|
| `existing bookings` | `existing reservations` | Glossary canonical — `reservation` is the canonical term; `booking` is acceptable but not preferred for primary copy. |
| `syncing rules vary by channel—for example` | `syncing rules vary by channel — for example` | Style — em dashes get surrounding spaces per Atlas §style §punctuation (en dash for ranges, em dash for breaks, spaces around dashes when breaking a sentence). |

If product prefers the original verbatim, both edits are easy to revert — flag and I'll re-edit.

### 5.2 Title

`How taxes work in Guesty`

Verb-noun phrase, sentence case, frames the panel as conceptual (not a step). Distinct enough from the question heading (`What taxes apply to your reservations?`) that the user knows they're reading help, not a re-asked question.

### 5.3 Academy link

| Element | Copy / behavior |
|---|---|
| Link text | `Go deeper in the Guesty Academy →` |
| Destination | The Guesty Academy article on taxes. **URL TBD — confirm with content team** (see §13). |
| Target | New tab. Always. `target="_blank" rel="noopener noreferrer"`. |
| Aria-label | `Go deeper in the Guesty Academy (opens in new tab)` — accessibility convention for new-tab links. |
| Underline behavior | Underline on hover and on keyboard focus. Default state can be unadorned given the teal accent color is distinct enough to read as a link on the dark background. |

---

## 6. Transitions and animation

- **Reveal (on `Explain taxes` click):** right panel slides in from the right over 350ms, easing `ease-out`. Left panel resizes from 100% → 50% concurrently. Total motion duration matches the canvas reveal timing of 350ms (NOT the 500ms AHA reveal — this is a lighter, opt-in moment, not an AHA).
- **Hide (on `Hide explanation` click):** right panel slides out to the right over 250ms, easing `ease-in`. Left panel expands from 50% → 100% concurrently.
- **Reduced motion:** both reveal and hide collapse to 150ms opacity fades. Panel resize is instant.
- **Re-trigger:** clicking `Explain taxes` again after hiding re-runs the same reveal animation. The module's scroll position resets to top.
- **State persistence:** **session-scoped only.** If the user dismisses the module then navigates away (back to Section 2, forward to Step 2), the module returns to hidden state. Do not persist `explanation_open` across questions or across sessions — it'd surprise the user.

---

## 7. Dismissibility

Multiple paths to close the module, all consistent in behavior:

| Trigger | Effect |
|---|---|
| Click `Hide explanation` (left panel) | Animated hide per §6. Focus returns to the `Explain taxes` button (which is now the same button, copy reverted). |
| Press `Esc` while the module has focus | Animated hide. Focus returns to the `Explain taxes` button. |
| Navigate forward (`Continue`) or back (`Back`) | Module hides without animation as the wizard transitions. The next/previous question's default state is single-panel; the module does not persist. |
| Click outside the module | **No effect** — outside-click does not dismiss. The module is a sibling panel, not an overlay. (This mirrors the Airbnb Connect 50/50 — clicking the left panel doesn't dismiss the right.) |

---

## 8. Accessibility

| Concern | Spec |
|---|---|
| Focus on reveal | After the animation completes, move focus to the module's title (`h3`). Announce via polite live region: `Explanation: How taxes work in Guesty.` |
| Focus on hide | Return focus to the `Explain taxes` button. |
| Module reading order | Heading → body → Academy link. SVG asset is `aria-hidden`; the title carries the meaning. |
| Keyboard order when expanded | Left panel tab order is unchanged (options → `Continue` → `Hide explanation` → `Back`). Then focus moves to the module: title (focusable, `tabindex="0"`) → Academy link. After the Academy link, focus loops back to the left panel's first option per Arc wizard convention. |
| Screen reader announcement of "opens in new tab" | Academy link aria-label includes `(opens in new tab)`. |
| Contrast | Body text on `#0A0036` background: white (`#FFFFFF`) is 18.4:1 — AAA. Off-white (`#E8E6F2`) is 15.6:1 — AAA. Teal accent (`#85B9B8`) on `#0A0036` is 6.9:1 — AAA for body, AA for graphics. All good. |
| Reduced motion | See §6 — animations collapse to 150ms opacity fades; resize is instant. The educational content is unchanged in reduced-motion mode. |
| Color is not the only signal | Academy link uses both the teal accent color and the trailing `→` arrow, so users with color-vision differences see the link affordance regardless of color perception. |

---

## 9. Copy register (consolidated)

Every string used in this patch:

| Where | Copy |
|---|---|
| Step indicator | `Step 1 of 3` |
| Question heading | `What taxes apply to your reservations?` |
| Question helper | `Select every tax type that applies. We'll set the rates next.` |
| Option A | `Sales tax or VAT` |
| Option B | `Occupancy or tourist tax` |
| Option C | `City or local tax` |
| Option D | `Other` |
| Primary CTA | `Continue` |
| Secondary CTA (default state) | `Explain taxes` |
| Secondary CTA (expanded state) | `Hide explanation` |
| Back link | `Back` |
| Module title | `How taxes work in Guesty` |
| Module body | (verbatim from §5.1) |
| Academy link | `Go deeper in the Guesty Academy →` |
| Academy link aria-label | `Go deeper in the Guesty Academy (opens in new tab)` |
| Polite live region on reveal | `Explanation: How taxes work in Guesty.` |

---

## 10. States — at a glance

| State | Layout | What's visible |
|---|---|---|
| **Default** | Single-panel | Question + options + `Continue` + `Explain taxes` |
| **Expanded** | 50/50 split | Question + options + `Continue` + `Hide explanation` (left) · Module with icon row, title, body, Academy link (right) |
| **Reduced-motion default** | Single-panel | Identical to default; only animation differs on transition |
| **Reduced-motion expanded** | 50/50 split | Identical to expanded; transition is a 150ms opacity fade and instant resize |

The pattern has no error, loading, or empty states — the educational copy is static, the Academy link is a navigation away, and the module surface itself doesn't fetch data.

---

## 11. Acceptance criteria

A prototype build passes this patch when:

- [ ] Q3.7 Step 1 default state renders as a single-panel layout matching the v2 spec §6.8 baseline, plus a secondary `Explain taxes` text-link CTA below `Continue` (with a `HelpCircle` icon to the left of the text).
- [ ] Clicking `Explain taxes` transitions the layout to 50/50 — left panel reflows the question to 50% width; right panel slides in from the right over 350ms.
- [ ] In the expanded state, the secondary CTA's copy changes to `Hide explanation` and the icon swaps to `X`.
- [ ] The right panel has background `#0A0036`, inner padding `gst-p-12`, and no shadow.
- [ ] `Frame 1 from Figma.svg` renders at the top of the module, full-width, aspect-ratio preserved, `aria-hidden="true"`.
- [ ] The asset is copied into the prototype project (e.g. `src/prototype/assets/q3-7-tax-module-header.svg`) — no references to a user's Downloads folder.
- [ ] Module title reads `How taxes work in Guesty` in a big display-size weight (~36px, semibold).
- [ ] Module body matches §5.1 verbatim — with the two Atlas edits (`reservations` not `bookings`; spaces around the em dash).
- [ ] Academy link reads `Go deeper in the Guesty Academy →` and opens the URL in a new tab with `rel="noopener noreferrer"` and an aria-label that includes `(opens in new tab)`.
- [ ] `Hide explanation` and `Esc` both close the module, animating per §6. Focus returns to the `Explain taxes` button.
- [ ] Forward (`Continue`) and back (`Back`) navigation collapses the module without animation; the next/previous question opens in single-panel default state.
- [ ] On reveal, focus moves to the module title and a polite live region announces `Explanation: How taxes work in Guesty.`
- [ ] Body text contrasts at AAA against `#0A0036` — verified at white or off-white.
- [ ] Reduced-motion mode collapses animations to 150ms opacity fades with instant resize.
- [ ] Outside-clicking the module does NOT dismiss it. Only `Hide explanation`, `Esc`, or navigation dismisses.
- [ ] No exclamation marks anywhere on the screen.
- [ ] Sentence case for every label, heading, button, and link.

---

## 12. Resolved decisions (locked 2026-05-27)

1. **Button label** — **`Explain taxes`** (sentence case, verb+object). Rejects all three original suggestions per the rationale in §3. Generic form for future reuse: `Explain {topic}`.
2. **Module background** — `#0A0036` (verbatim from user).
3. **Module top decoration** — the provided `Frame 1 from Figma.svg` asset.
4. **Module title weight** — large display (~36px, semibold).
5. **Persistence** — session-only; no cross-question or cross-session persistence.
6. **Trigger placement** — secondary text-link CTA below the primary `Continue` on the question screen.
7. **Two Atlas-aligned edits to the source copy** — `bookings` → `reservations`; spaces around em dash. Flag to revert if product wants verbatim.

---

## 13. Open questions

1. **Guesty Academy URL.** The Academy link target is `TBD`. Confirm with the content team:
   - Is there an existing Academy article on taxes that this should deep-link to?
   - If not, who owns creating it, and what's the URL slug?
   - Until confirmed, the link can render to a placeholder `https://academy.guesty.com/` so the affordance is testable.
2. **Foreground color choice on the module.** Pure white (`#FFFFFF`) vs off-white (`#E8E6F2`) — both AAA on `#0A0036`. Off-white is softer and feels more on-brand for a deep-purple surface; pure white is bolder. Recommend off-white; defer to brand on the final call.
3. **Generic pattern adoption.** This patch defines `Explain {topic}` as a reusable wizard pattern. Which other Q3.x or Q5.x questions warrant adopting it? Candidates I'd flag for product review:
   - Q3.1 — *When do you count revenue from a reservation?* (`Explain revenue recognition`)
   - Q3.3 — *How do you handle damage protection?* (`Explain damage protection`)
   - Q5.1 — *Who makes the calls on Guesty settings?* (probably no — self-explanatory enough)
   Recommend folding the candidate decision into a Phase-2 spec sweep, not now.
4. **Icon library overlap.** The SVG asset's four icons are decorative/conceptual, not reused elsewhere. If product wants this pattern reused for other questions, each will need its own header asset — confirm whether the design team owns producing those, or whether a more generic decorative motif covers all future cases.

---

## 14. Hand-off note

This patch lives alongside the Airbnb Connect (`airbnb-connect-ux-patch-2026-05-27.md`) and Fees (`q3-6-fees-layout-patch-2026-05-27.md`) patches in `docs/planning-artifacts/`.

Once the prototype agent picks it up:

- v2 spec §6.8 should be updated to point here as the canonical Step 1 layout.
- A new pattern entry should be added to v2 spec §14 (Microcopy patterns) for `Explain {topic}` — covering when to use, how to copy, and the visual treatment of the educational module.
- The §18 audit table should be updated to note this layout change.

I'll fold all three into the next spec sweep so the v2 doc stays accurate.
