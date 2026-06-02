---
title: "Wizard surface — dialog presentation patch"
---

# Wizard surface — dialog presentation patch

**Date:** 2026-05-29
**Author:** Sally (UX Designer)
**Audience:** Designer producing the Figma + agent building the prototype
**Applies to:** Global presentation of the onboarding wizard described in [`ux-design-specification-v2-atlas-aligned-2026-05-27.md`](ux-design-specification-v2-atlas-aligned-2026-05-27.md). Affects every wizard surface — S0 welcome, every question section (Sections 1–8), every canvas reveal (Q1.4 AHA, Section 3 milestone, Section 8 summary), the Section 9 loader, and the Section 10 dashboard hand-off animation.
**Voice & copy standards:** Atlas — sentence case, glossary-compliant. Per glossary, the user-facing term for an overlay-requiring-response is **dialog** (not "modal", "popup", or "overlay"). This spec uses *dialog surface* throughout.
**Scope:** **Visual presentation only.** No question content, no flow, no anchor bot behavior, no canvas behavior, no copy changes.

---

## 0. Why this patch exists

The current wizard occupies the full viewport edge-to-edge. That presentation choice tells the user, implicitly:

- *"You have left the platform."*
- *"This is a heavy, separate process."*
- *"You are not in Guesty yet — you are in onboarding."*

Both of those messages work against the activation goal. The wizard is supposed to feel like the user is **already inside Guesty**, just tuning a few defaults before Call 1. A full-screen takeover is the wrong metaphor for that intent.

Reframing the wizard as a large dialog surface over a blurred Guesty platform shifts the message:

1. **Continuity with the platform.** The dashboard is visible (blurred) behind the dialog, so the wizard reads as *configuration happening inside Guesty*, not as a separate destination. The user never loses sight of where they are.
2. **Reduced perceived effort.** A bounded surface — even a very large one — implies *"this finishes and you step through into the platform"*. A full-bleed surface implies *"this is the application for now"*. The dialog framing trims the psychological weight of the task without removing any of its substance.
3. **A visible destination.** The blurred dashboard is a soft promise. The user can see, peripherally, what they are setting up *toward*. That sustains motivation through the mid-funnel and pays off the AHA / milestone / summary canvases more strongly when they appear.

This is a presentation change, not a functional one. Every question, every branch, every canvas, every copy line is preserved exactly as specified in v2.

---

## 1. Summary

| # | Delta | Why |
|---|------|-----|
| **P-1** | Replace the full-viewport wizard surface with a centered **dialog surface** sized to ~88% of the viewport | Reframes the wizard as configuration *within* Guesty, not a separate destination |
| **P-2** | Render the prototype's own **`DonePanel` Guesty homepage**, blurred, as the backdrop behind the dialog surface | Anchors the user inside the platform; the backdrop is literally the homepage they'll land on at completion |
| **P-3** | Internal layout of the dialog (anchor bot rail, question column, canvas) is **unchanged** — same proportions, same grid, same components | This is presentation, not structure |
| **P-4** | Add **entry, exit, and reveal transitions** that use the blurred backdrop as a storytelling device (focus resolves on completion) | Turns the surface metaphor into a narrative payoff at Section 10 |
| **P-5** | Define **small-viewport fallback**: below a minimum width/height, the dialog surface goes edge-to-edge (current behavior) | The metaphor only works when there is visible breathing room around the dialog |
| **P-6** | Define **canvas reveal behavior** inside the dialog (AHA at Q1.4, milestone at Section 3, summary at Section 8) — the canvas still expands inside the dialog, not outside it | The dialog is the wizard's world; canvases live inside it |

---

## 2. Surface model

```
┌──────────────────────────────────────────────────────────────────┐
│  ░░░░░░░░░░░░░░░░░░░░░░░░░ blurred Guesty homepage (DonePanel) ░░░░░░░░░░░░ │
│  ░░░░  ┌────────────────────────────────────────────────┐   ░░░░ │
│  ░░░░  │                                                │   ░░░░ │
│  ░░░░  │   Anchor bot rail │ Question column │ Canvas   │   ░░░░ │
│  ░░░░  │                   │                 │          │   ░░░░ │
│  ░░░░  │                                                │   ░░░░ │
│  ░░░░  │             dialog surface                     │   ░░░░ │
│  ░░░░  └────────────────────────────────────────────────┘   ░░░░ │
│  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │
└──────────────────────────────────────────────────────────────────┘
        ▲                                ▲                    ▲
  Backdrop margin            Dialog surface            Backdrop margin
  (blurred dashboard         (the wizard, as           (blurred dashboard
   peeks through)             specified in v2)          peeks through)
```

Three layers, back-to-front:

1. **Backdrop layer** — blurred Guesty homepage (DonePanel) (see §4).
2. **Scrim layer** — a subtle dark tint that improves dialog/background contrast (see §4.3).
3. **Dialog surface** — the wizard's existing v2 layout, unchanged internally (see §3).

---

## 3. Dialog surface specification

### 3.1 Size

| Property | Value | Notes |
|---|---|---|
| Width | `88vw`, **max 1440px** | Caps on ultra-wide so the wizard doesn't stretch past its v2 max content width |
| Height | `88vh`, **max 920px** | Caps on tall monitors so it doesn't elongate beyond comfortable reading distance |
| Min width | `1024px` | Below this, fall back to full-bleed (see §6) |
| Min height | `680px` | Below this, fall back to full-bleed (see §6) |
| Aspect | Free — width and height clamp independently | The internal v2 grid handles the variation |

**Why 88%, not 95% or 75%:**
- *95%* — too close to full-bleed; the metaphor disappears, the user just sees a thin border and reads it as a window chrome artifact.
- *75%* — too small; the wizard's three-column layout (bot rail + question + canvas) gets compressed and the canvas reveals lose impact.
- *88%* — leaves a visible band of blurred platform on all four edges (~6% of viewport each side) that reads unambiguously as *"Guesty is behind this"* while preserving the v2 internal proportions.

### 3.2 Position

- Centered both axes.
- Fixed position relative to viewport (does not scroll with backdrop — the backdrop is also fixed, see §4).

### 3.3 Surface chrome

| Property | Value | Notes |
|---|---|---|
| Background | Solid surface token (`color/surface/elevated` or equivalent) | No transparency — the dialog itself is opaque so the wizard inside reads at full contrast |
| Corner radius | `16px` | Matches Guesty platform dialog radius |
| Elevation | Dialog-level shadow token (e.g. `shadow/dialog`) | Heavier than card, lighter than full-screen |
| Border | None | Shadow alone separates from backdrop |

### 3.4 Internal layout — UNCHANGED

Every internal element of the wizard — the anchor bot rail, the question column, the canvas, all section headers, progress indicator, transitions between Q-screens, save-as-you-go affordances — renders **exactly as specified in v2**. Treat the dialog surface as a new viewport boundary for the existing layout. No tokens, no grids, no spacings inside the dialog change.

---

## 4. Backdrop layer

### 4.1 Source content

The backdrop is the **Guesty homepage already built inside the prototype** — the `DonePanel` component rendered at the end of the wizard (Section 10 "done" state). In the current prototype this lives in `wizard.jsx:758` (`DonePanel` → `home-shell`), composed of:

- `HomeHeader` — the teal 56px top bar: hamburger, Guesty logo (`assets/guesty-home-logo.svg`), the `/`-to-search field, and the utility cluster (Guesty AI, bookmarks, create, apps, notifications, help, avatar).
- `HomeSidebar` — the left nav: Home (selected), Inbox (badge 24), Calendar, Listings, Marketing & Sales, Financials, Guest payments, Accounting, Integrations, Settings.
- `HomeGreeting` — the `Welcome to Guesty, {firstName}` banner with the Customize button.
- The content stack: `NextCallSection`, `TopicsSection`, `DailyOverviewSection`, `TrendsOverviewSection`, `RevenueSection`.

This is the **same homepage the user lands on at completion** — which is exactly why it's the right backdrop (see §7.4 for the narrative reasoning).

Rendering requirements:

- It is **not interactive** while it is the backdrop. Pointer events do not pass through the scrim.
- It is **visually stable** for the duration of the wizard — it does not animate, re-render its widgets, or shift while the user works. (Implementation note in §11-Q1: render it once and freeze it, e.g. mount `DonePanel` in a non-interactive container, or snapshot it to an image. Don't run a second live instance that could drift from the foreground state.)
- It **must remain recognizable as Guesty** through the blur. The teal header bar, the Guesty logo, and the sidebar shape are the load-bearing recognition cues — verify they still read at `24px` blur. If the backdrop reads as generic grey noise, the entire metaphor fails.

### 4.2 Blur

| Property | Value | Notes |
|---|---|---|
| Blur radius | `24px` (Gaussian) | Heavy enough to remove text legibility; light enough that shapes and color remain recognizable |
| Saturation | `0.9` | Slight desaturation so the backdrop doesn't compete with the dialog's brand color |
| Brightness | `0.95` | Subtle darken so foreground dialog "lifts" |

### 4.3 Scrim

A thin dark scrim sits between backdrop and dialog:

| Property | Value | Notes |
|---|---|---|
| Color | `rgba(0, 0, 0, 0.32)` | Tunable; goal is dialog separation without dimming the brand color of the backdrop below recognition |
| Coverage | Full viewport | Sits between backdrop and dialog |
| Pointer events | Captured by scrim — clicks on the scrim do **not** close the dialog | The wizard is committed work; an accidental backdrop click must not dismiss it (see §7.3) |

### 4.4 Fixed positioning

Backdrop and scrim are both viewport-fixed. They do not scroll. The dialog also does not move. Only content *inside* the dialog scrolls (as it does in v2 today).

---

## 5. Transitions and motion

The dialog framing turns into a narrative device when paired with motion. Three key moments:

### 5.1 Entry (wizard mount)

| Phase | Duration | What happens |
|---|---|---|
| 0ms | — | Backdrop renders sharp (un-blurred `DonePanel` homepage visible for ~120ms) |
| 0–280ms | 280ms | Blur ramps from `0px → 24px`, scrim fades from `0 → 0.32` |
| 120–400ms | 280ms | Dialog surface fades in (`opacity 0 → 1`) and rises (`translateY: 12px → 0`) |
| 400ms | — | S0 welcome content fades in over 200ms |

**Why pre-show the sharp backdrop briefly:** the unblurred-then-blurred sequence is what *names* the backdrop as Guesty. If the user sees only the blurred state from the first frame, the backdrop reads as decorative texture. The 120ms of sharp homepage — teal header, Guesty logo, the `Welcome to Guesty` greeting — is what makes the user think *"that's my Guesty"* before it recedes.

### 5.2 Canvas reveals (Q1.4 AHA, Section 3 milestone, Section 8 summary)

Canvas reveals happen *inside* the dialog. The dialog itself does not change size, position, or chrome during a canvas reveal. The internal v2 canvas-reveal motion is preserved exactly. The backdrop and scrim do not animate during canvas moments — the focus stays inside the dialog.

### 5.3 Exit (Section 10 dashboard hand-off)

This is the payoff moment. Reverse of entry, with one extra beat:

| Phase | Duration | What happens |
|---|---|---|
| 0ms | — | Section 10 "you're ready" state visible inside dialog |
| 0–240ms | 240ms | Dialog surface fades out (`opacity 1 → 0`) and falls (`translateY: 0 → 8px`) |
| 120–520ms | 400ms | Blur ramps from `24px → 0px`, scrim fades from `0.32 → 0`; backdrop swaps from the prefill-default `DonePanel` to the **personalized** `DonePanel` (real first name, imported count, focus topics) |
| 520ms | — | User is now on the real, interactive `DonePanel` homepage |

The user literally watches the platform come into focus as the wizard recedes — and it's the *same homepage* that was blurred behind them the whole time, now sharpened and personalized. This is the moment the surface metaphor pays off.

**Implementation note:** because the foreground wizard *is* what produces the `DonePanel`, the cleanest build is to render the live `DonePanel` as the exit target and simply remove the dialog + blur over it, rather than cross-fading two separate renders.

---

## 6. Small-viewport fallback

The dialog metaphor only works when there is visible blurred platform around the dialog. Below a minimum viewport, the metaphor collapses and the wizard should revert to its pre-patch full-bleed presentation.

| Condition | Presentation |
|---|---|
| `viewport width ≥ 1024px AND viewport height ≥ 680px` | Dialog presentation (this patch) |
| Either dimension below threshold | Full-bleed presentation (current v2 behavior) — no dialog, no backdrop, no scrim |

The threshold is set at the smallest viewport where the v2 three-column layout still has enough room for ~6% backdrop margin on all sides. Below that, squeezing the dialog further harms the wizard interior more than the dialog metaphor adds.

Transition between modes happens on viewport resize. No animation — just a clean swap. (Resizing across the threshold is an edge case; users almost never do it mid-wizard.)

---

## 7. Behavior details

### 7.1 Scroll containment

Scroll inside the dialog scrolls only the dialog interior, as in v2. The backdrop never scrolls. The page (`<body>`) is scroll-locked while the wizard is mounted.

### 7.2 Focus management

- On entry, focus moves to the dialog's first focusable element (S0 `Start setup` CTA, or the resume-from element).
- A focus trap is active for the duration of the wizard — Tab and Shift+Tab cycle within the dialog only.
- The dialog has `role="dialog"` and `aria-modal="true"` with a labelled accessible name ("Guesty onboarding").

### 7.3 Dismissal

- **The backdrop is non-dismissive.** Clicks on the scrim do not close the wizard. The wizard is committed work; accidental dismissal would destroy state and trust.
- **`Esc` is non-dismissive.** Same reasoning.
- The only way out of the wizard is the existing v2 exit affordances (save and leave, complete to dashboard, etc.).
- This is **deliberately different** from standard dialog patterns. The wizard is dialog-*shaped* but is not a "popup" — it's a configuration surface that happens to use dialog presentation. Document this clearly for engineering review.

### 7.4 Backdrop content choice

The backdrop is the prototype's own **`DonePanel` homepage** (§4.1) — the same homepage the user lands on at completion. This makes the entry/exit narrative coherent: the user sees the homepage → it blurs → they configure → it sharpens back into the *same* homepage they glimpsed at the start, now interactive. The destination doesn't change; the user becomes ready to use it.

Do **not** use a generic Guesty marketing screen, a logged-out state, or a fabricated dashboard. Use the real `DonePanel` / `home-shell` already in the prototype.

One consequence worth naming: `DonePanel` is partly **personalized** (`HomeGreeting` shows the first name; `importedCount` and focus topics derive from answers). As a backdrop at *entry*, those answers don't exist yet. For v1, render the backdrop with the same prefill/defaults `DonePanel` already falls back to (`SF_PREFILL.first_name`, `MOCK_LISTINGS`, default focus topics) so it's stable from the first frame. See §11-Q2 for the personalized-backdrop fast-follow.

---

## 8. Accessibility

| Concern | Treatment |
|---|---|
| Reduced motion (`prefers-reduced-motion: reduce`) | Entry, exit, and blur ramps collapse to instant state changes. Backdrop is shown directly in its blurred state; no sharp-to-blurred reveal. No fade or translate on the dialog. |
| Screen reader | Dialog has `aria-modal="true"`, accessible name "Guesty onboarding". Backdrop content has `aria-hidden="true"` and is not in the tab order or accessibility tree. |
| Contrast | Scrim opacity tuned so the dialog surface meets AA contrast against the blurred backdrop in both light and dark themes. Verify with token combinations before ship. |
| Keyboard | Focus trap active; all wizard interactions reachable via keyboard; the non-dismissive backdrop does not introduce any keyboard trap risk because exit affordances live inside the dialog. |
| Pointer | Backdrop and scrim do not receive pointer events that affect wizard state. Hover on the scrim shows no affordance (no pointer cursor change). |

---

## 9. Visual reference — three states

### State A: Entry, 0ms (backdrop sharp — the `DonePanel` homepage, dialog not yet visible)

```
┌──────────────────────────────────────────────────────────────────┐
│ ▟▙ Guesty   /  to search        ✦ AI  ⌘ ⊞ 🔔 ? (Y)   ← home-header│
│ ┌─────────┐  Welcome to Guesty, Yair          [ Customize ]       │
│ │ ▸ Home  │  ┌── Next call ──┐  ┌── Focus topics ──┐              │
│ │   Inbox │  └───────────────┘  └──────────────────┘              │
│ │   Calend│  ┌── Daily overview ──────────────────┐                │
│ │   Listin│  │  ◔ ◔ ◔   trends                    │                │
│ │   Market│  └────────────────────────────────────┘                │
│ │   Financ│  ┌── Revenue ─────────────────────────┐                │
│ │   …     │  └────────────────────────────────────┘                │
│ └─────────┘                                                        │
└──────────────────────────────────────────────────────────────────┘
   home-sidebar          home-main (DonePanel content stack)
```

### State B: Entry, 400ms (backdrop blurred, dialog faded in)

```
┌──────────────────────────────────────────────────────────────────┐
│  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │
│  ░░░░  ┌────────────────────────────────────────────────┐   ░░░░ │
│  ░░░░  │                                                │   ░░░░ │
│  ░░░░  │              S0 — Welcome, Yair                │   ░░░░ │
│  ░░░░  │                                                │   ░░░░ │
│  ░░░░  │       Let's set up Guesty to match how         │   ░░░░ │
│  ░░░░  │       you run your business.                   │   ░░░░ │
│  ░░░░  │                                                │   ░░░░ │
│  ░░░░  │                  [ Start setup ]               │   ░░░░ │
│  ░░░░  │                                                │   ░░░░ │
│  ░░░░  └────────────────────────────────────────────────┘   ░░░░ │
│  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │
└──────────────────────────────────────────────────────────────────┘
```

### State C: Exit, 520ms (backdrop sharp again — same `DonePanel` homepage, now interactive)

```
┌──────────────────────────────────────────────────────────────────┐
│ ▟▙ Guesty   /  to search        ✦ AI  ⌘ ⊞ 🔔 ? (Y)   ← interactive│
│ ┌─────────┐  Welcome to Guesty, Yair          [ Customize ]       │
│ │ ▸ Home  │  ┌── Next call ──┐  ┌── Focus topics ──┐              │
│ │   Inbox │  └───────────────┘  └──────────────────┘              │
│ │   Calend│  ┌── Daily overview ──────────────────┐                │
│ │   Listin│  └────────────────────────────────────┘                │
│ │   …     │  ┌── Revenue ─────────────────────────┐                │
│ └─────────┘  └────────────────────────────────────┘                │
└──────────────────────────────────────────────────────────────────┘
  Same homepage as State A — now personalized with real answers,
  blur removed, pointer events live. The wizard has receded into it.
```

---

## 10. What is explicitly NOT changing

To prevent scope creep on this patch:

- **No copy changes.** Every word in the wizard is as specified in v2 and v2 patches.
- **No flow changes.** Section count, branching, save-as-you-go, returning-user behavior, S0 skip logic, Section 10 hand-off — all unchanged.
- **No anchor bot changes.** Position, presence rules, voice — unchanged.
- **No canvas-reveal content changes.** AHA, milestone, summary content all unchanged.
- **No token changes outside this patch's scope.** Only the dialog/backdrop/scrim tokens introduced here are new.
- **No new homepage build.** We reuse the prototype's existing `DonePanel` homepage as the backdrop — we do not design or build a separate dashboard for this.
- **No analytics changes.** Existing wizard events fire identically. (Optionally add one event: `wizard.surface.fallback_to_fullbleed` if the small-viewport fallback triggers — see §11.)

---

## 11. Decisions (locked)

These were open during exploration; they are now decided. Each carries the rationale so a reviewer can reopen one with cause rather than by default.

1. **Backdrop source — DECIDED: inert live `DonePanel` instance.** Render the prototype's own `DonePanel` (§4.1) as the backdrop by mounting it in an inert (`aria-hidden`, `pointer-events: none`) container — not a static image snapshot. **Why:** `DonePanel` already exists in the bundle, so a live instance can't drift from the real homepage the way a separate exported image would, and it makes the §5.3 exit trivial (lift the dialog off the same render rather than cross-fading two). **Revisit only if:** the live instance creates a measurable mount-cost or visual-instability problem, in which case fall back to a one-time snapshot image.
2. **Backdrop personalization — DECIDED: prefill defaults for v1, progressive personalization as a fast-follow.** v1 renders the backdrop with `DonePanel`'s existing prefill defaults (`SF_PREFILL.first_name`, `MOCK_LISTINGS`, default topics) so it's stable from the first frame. The fast-follow re-renders the backdrop with the user's real data as answers accumulate (post-Q1.4), so the blurred homepage quietly fills in behind them. **Why:** ships the metaphor now without blocking on per-answer backdrop reactivity; the personalization is a strict enhancement layered on later. **Revisit only if:** the fast-follow proves cheap enough to fold into v1 during build.
3. **Non-dismissive backdrop — DECIDED: yes, deliberately non-dismissive.** Scrim click and `Esc` do **not** close the wizard (§7.3). **Why:** destroying committed wizard state on a stray click is a far worse failure than momentary "how do I exit" confusion; the wizard is configuration work, not a transient popup. This is an intentional departure from standard dialog convention — engineering should treat the §7.3 behavior as a hard requirement, with an explicit code comment marking it intentional.
4. **Brand-color preservation through blur — DECIDED: §4.2 values are the build target; one tuning pass scheduled.** Build to `blur 24px / saturation 0.9 / brightness 0.95 / scrim 0.32`, then hold one ~30-minute visual review with the designer on the first rendered prototype to fine-tune so Guesty stays recognizable but not loud. **Why:** these values are sound defaults but blur/contrast interaction is only judgeable on a real render. The tuning pass is a calibration step, not a reopening of the decision.
5. **Reduced-motion default — DECIDED: keep the sharp-then-blur reveal as the standard-motion default.** Users without `prefers-reduced-motion` get the §5.1 sharp-then-blur entry; users with it get the §8 instant blurred state. **Why:** the 120ms sharp pre-show is the moment the backdrop is *named* as Guesty — dropping it for everyone would cost the metaphor its strongest beat. Reduced-motion users still get full recognition via copy, teal header, and logo through the blur.
6. **Small-viewport threshold — DECIDED: `1024 × 680` for v1, pending one confirmation against the supported-viewport list.** Use `width ≥ 1024px AND height ≥ 680px` for dialog presentation, full-bleed below (§6). **Why:** this is the smallest viewport where the v2 three-column interior keeps its proportions *and* leaves a readable backdrop margin. **One action before ship:** confirm against Guesty's official supported-viewport / min-resolution list and adjust if their floor differs.

**Net for build:** nothing here blocks Figma production or prototype work. Items 4 and 6 carry a single lightweight confirmation each (a tuning pass, a viewport-list check) that happen *during* build, not before it.

---

## 12. Hand-off checklist

For the Figma producer:

- [ ] Build the three states (A, B, C in §9) as separate frames at canonical desktop (1440 × 900) and at threshold (1024 × 680).
- [ ] Use the prototype's `DonePanel` homepage as the backdrop reference (teal header, sidebar, `Welcome to Guesty` greeting, content stack); export sharp and blurred variants.
- [ ] Define dialog surface, scrim, and backdrop as separate component layers so engineering can wire them independently.
- [ ] Add tokens: `surface/dialog/wizard`, `shadow/dialog/wizard`, `scrim/wizard`, `radius/dialog/wizard` (or reuse platform equivalents if they exist).
- [ ] Mark all v2 internal wizard frames as **child of dialog surface** — do not redraw any internal layout.

For the prototype agent:

- [ ] Wrap the existing wizard root component in a dialog surface with the §3 spec.
- [ ] Render the `DonePanel` homepage as a fixed-position, full-viewport, inert (`aria-hidden`, `pointer-events: none`) layer behind the scrim, using prefill defaults for v1.
- [ ] Implement entry, canvas-reveal, and exit motion per §5, gated on `prefers-reduced-motion` per §8.
- [ ] Implement the small-viewport fallback per §6 — same component tree, dialog/backdrop/scrim layers conditionally rendered.
- [ ] Wire the non-dismissive backdrop per §7.3 — explicit comment in the code that this is intentional.
- [ ] Verify focus trap, `aria-modal`, accessible name, `aria-hidden` on backdrop per §8.
- [ ] No changes to wizard interior — confirm by visual diff against pre-patch v2 build.

---

*End of patch.*
