---
title: "Airbnb Connect Step — UX Patch"
---

# Airbnb Connect Step — UX Patch

**Date:** 2026-05-27
**Audience:** Agent building the Guesty Pro Onboarding Wizard prototype
**Applies to:** `docs/planning-artifacts/airbnb-connect-implementation-reference.md` (sections 4, 5) and the merged Appendix A4–A8 inside `docs/planning-artifacts/ux-design-specification-2026-05-25.md`
**Source of truth for visuals:** Figma — [Untitled · node 1-577](https://www.figma.com/design/0BXmOvz9WvW25JmWLNHztU/Untitled?node-id=1-577) (Step 1) and [node 1-602](https://www.figma.com/design/0BXmOvz9WvW25JmWLNHztU/Untitled?node-id=1-602) (Step 2), plus production screenshots provided 2026-05-27.
**Background context:** Guesty help center — [Pilot: Pre-onboarding an Airbnb account to Guesty (view-only)](https://help.guesty.com/hc/en-gb/articles/34669189548957-Pilot-Pre-onboarding-an-Airbnb-account-to-Guesty-view-only) (auth-gated; for the prototype agent's reference if they have Guesty SSO).
**Embedded video asset:** [youtube.com/watch?v=LfFd_s2kz8Y](https://www.youtube.com/watch?v=LfFd_s2kz8Y) — the real explainer video to embed in the Step 1 video block (no longer a placeholder).

---

## 0. Why this patch exists

The pre-built `ConnectAbnb` and `ImportListingsContent` components from `abnb-distribution-page-master` are close to the target UX but **not exact**. The Figma + production screenshots provided on 2026-05-27 introduce five concrete deltas the prototype must honor. This patch is surgical: it does **not** revisit OAuth mocking, dummy data, or the embed pattern — those remain as specified in the implementation reference. Apply only the changes below on top of the prototype copies under `src/prototype/connect/`.

---

## 1. Patch summary (TL;DR)

| # | Where | Delta |
|---|-------|-------|
| **P-1** | Step 1 — `ConnectAbnb.tsx` (prototype copy) | Restructure into three vertical sections: **(a)** heading + view-only subtitle, **(b)** "Watch this video" block with a video placeholder, **(c)** "Start test-driving Guesty" block ending with the CTA. The current implementation has no video block and uses a different content order. |
| **P-2** | Step 1 — copy | Heading + subtitle copy and section headers locked. See §3. |
| **P-3** | Step 2 — `ImportListingsContent.tsx` (prototype copy) | Heading + subtitle copy locked. See §4. |
| **P-4** | Step 2 — filters toolbar | Replace the "Showing N listings" counter with an **"X/Y Filtered"** counter rendered inside the filters toolbar (between filter dropdowns and search). See §5. |
| **P-5** | Step 2 — `ListingItem.tsx` | Add **unit-type pill** ("Single Unit" / "Multi Unit") next to the listing name, and ensure the **co-host icon** renders before the name when `hostRole === 'co-host'`. Confirm the existing "Listed" / "Unlisted" status pill renders on the right edge of the row. See §6. |

---

## 2. Step 1 — Visual structure (P-1)

The current prototype `ConnectAbnb.tsx` (per Appendix A4 of the spec) renders:

```
Heading: Airbnb listings to be imported
Subtitle: A view-only connection will import data…
[bold] Start test-driving Guesty:
Paragraph 1
Paragraph 2
[Button] Pre-connect to Airbnb
```

Replace this layout with three distinct vertical sections, each separated by Arc spacing:

```
┌─ Section A — Header ───────────────────────────────┐
│ Heading (h2): Airbnb listings to be imported       │
│ Subtitle (muted): A view-only connection will…     │
└────────────────────────────────────────────────────┘

┌─ Section B — Video ────────────────────────────────┐
│ Label (bold): Watch this video to get more         │
│               information                           │
│ ┌──────────────────────────────────────────────┐   │
│ │                                              │   │
│ │   YouTube iframe — 16:9 — LfFd_s2kz8Y        │   │
│ │   (real explainer video, click to play)      │   │
│ │                                              │   │
│ └──────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────┘

┌─ Section C — Test-drive explainer ─────────────────┐
│ Label (bold): Start test-driving Guesty:           │
│ Paragraph 1 (muted): Test Guesty without…          │
│ Paragraph 2 (muted): We'll import real data…       │
│ [Primary Button] Pre-connect to Airbnb             │
└────────────────────────────────────────────────────┘
```

### Spacing & sizing tokens

- Use Arc `gst-mt-*` / `gst-mb-*` utility classes. Recommended rhythm: `gst-mt-2` between heading and subtitle, `gst-mt-14` between sections A→B and B→C, `gst-mt-6` between paragraphs inside section C, `gst-mt-16` between the last paragraph and the primary button.
- Section labels ("Watch this video to get more information", "Start test-driving Guesty:") are Arc `Text bold` at the default size, in the muted-foreground color used elsewhere in the step. Match the visual weight shown in the Figma — they are subheadings, not h3s.
- The video frame embeds the real explainer video at **16:9**. Implementation:
  - Render an Arc `AspectRatio` wrapper (or a `div` with `gst-aspect-video`) containing a YouTube `<iframe>`.
  - Source: `https://www.youtube.com/embed/LfFd_s2kz8Y` (the embed-form URL for [youtube.com/watch?v=LfFd_s2kz8Y](https://www.youtube.com/watch?v=LfFd_s2kz8Y)).
  - Iframe attributes: `title="Pre-connect to Airbnb — view-only explainer"`, `allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"`, `allowfullscreen`, `loading="lazy"`, `frameborder="0"`, width / height `100%`.
  - No custom thumbnail or overlay — let YouTube render its own poster + play affordance so the video card looks identical across browsers.
  - The card itself sits on the surface with no extra elevation, border, or shadow.
- Do **not** introduce new colors, shadows, or borders that aren't already used elsewhere in the onboarding step — the video card sits on the surface with no extra elevation.

### Behavior — unchanged

- The "Pre-connect to Airbnb" button still drives the mock `onPreconnectClick` from Appendix A4 (1.5 s loading → `goNext()` or `?mockError` Alert).
- The error Alert, when present, renders directly below the button as in the current Appendix A4 example. No change to the error states.
- The bot Alert (DD-5 anchor screen) remains the **wizard shell's** responsibility, mounted above section A.

---

## 3. Step 1 — Copy (P-2)

Use these strings verbatim. They override the strings in Appendix A4's example JSX wherever they differ.

| Element | Copy | Notes |
|---|------|------|
| Heading (h2) | `Airbnb listings to be imported` | unchanged from current |
| Subtitle | `A view-only connection will import data without making changes to your listings on Airbnb.` | unchanged from current |
| Section B label | `Watch this video to get more information` | **new** |
| Section C label | `Start test-driving Guesty:` | unchanged from current — colon included |
| Section C paragraph 1 | `Test Guesty without affecting your listings on Airbnb. The property management software you're using will still be connected to Airbnb until you decide to switch to Guesty.` | Render as a single flowing paragraph — drop the manual `<br />` line breaks present in the current Appendix A4 JSX. Let the paragraph wrap naturally to fit the panel width. |
| Section C paragraph 2 | `We'll import real data from Airbnb so you can explore Guesty. We won't sync changes in Guesty to Airbnb until you are ready to switch to Guesty and fully connect the Airbnb account.` | Same — single paragraph, no manual breaks. |
| Primary button | `Pre-connect to Airbnb` | unchanged |

Keep every copy string wrapped in the `t()` macro from `@guestyci/localize` as the original component does — translations matter.

---

## 4. Step 2 — Heading & subtitle (P-3)

Inside the prototype copy of `ImportListingsContent.tsx` (and/or its subheader, depending on where the title currently lives — verify against the source), confirm the heading and subtitle render as:

| Element | Copy |
|---|------|
| Heading (h2) | `Choose listings to import` |
| Subtitle | `Changes you make on Guesty won't sync to Airbnb until you fully connect the account and listings.` |

If the current `ImportListingsSubheader.tsx` from the source codebase ships with different copy, override it in the prototype copy. Do not edit the source repo.

---

## 5. Step 2 — Filters toolbar (P-4)

### Toolbar layout

Single horizontal row, left-aligned controls + right-aligned search:

```
[ ] Select all   [City: All ▾]   [Status: All ▾]   [Ownership: All ▾]   X/Y Filtered          [🔍 Search…]
```

- **Select all** — primary checkbox + label, as currently rendered by the source `ListingsFilter`. Default state per Appendix A5 (b) is **checked** (idSet seeded from all listings on mount). Toggling it bulk-selects or bulk-clears.
- **City / Status / Ownership** — Arc dropdowns. Each shows its label + current selection in the chip-style trigger shown in the Figma (e.g. `City   All`). Default value: `All`.
- **X/Y Filtered counter** — **new**, replaces the "Showing N listings" string referenced in §9 of the implementation reference and in Appendix A8. See sub-spec below.
- **Search** — right-aligned text input with a leading magnifier glyph. Existing behavior preserved (filters by listing name/nickname/address).

### "X/Y Filtered" counter — spec

- **Format:** `{filteredCount}/{totalCount} Filtered` where:
  - `totalCount` = total listings returned from the mock dataset (e.g. `DUMMY_LISTINGS_EIGHT.length`).
  - `filteredCount` = listings remaining after the City + Status + Ownership + Search filters are applied.
- **States:**
  - No filters active → `8/8 Filtered` (still rendered — provides at-a-glance dataset size).
  - One or more filters active → e.g. `5/8 Filtered`.
  - Zero matches → `0/8 Filtered`. The counter remains; the list area below shows the existing empty state.
- **Styling:** muted-foreground text, same size as filter labels. No badge / no pill — plain text inside the toolbar.
- **Position:** between the last filter dropdown ("Ownership") and the search input. On narrow widths, the counter wraps to a second row below the dropdowns rather than overlapping the search field.

### Helper-text under controls — discard

The Figma frame shows placeholder helper-text strings under each control (`This is a checkbox description.`, `This is an input description.`, `This is a select description.`). These are Figma component placeholders, not real copy. **Do not render them** in the prototype.

---

## 6. Step 2 — Listing item row (P-5)

### Row anatomy

```
┌────────────────────────────────────────────────────────────────────────────────┐
│ [ ] [thumb]  [👥]? Ultra Luxe Apartment   [Single Unit | Multi Unit]   [Listed]│
│              [Nickname] · [Property type]                                       │
│              [Address]                                                          │
└────────────────────────────────────────────────────────────────────────────────┘
```

### Required changes vs current `ListingItem.tsx`

1. **Unit-type pill** — Render an Arc `Badge` (or equivalent chip) immediately after the listing name. Values:
   - `Single Unit` — neutral / default badge variant.
   - `Multi Unit` — soft-blue badge variant (matches Figma — distinct from the green "Listed" pill).
   - The pill is required on every row.
2. **Co-host icon** — When `hostRole === 'co-host'`, render a small `Users` icon (from `lucide-react`) immediately **before** the listing name, in the same line as name + unit-type pill. Owner-role rows render with no icon. Icon size matches the name's cap-height (use `gst-size-4` or equivalent).
3. **Listed / Unlisted pill** — Right-aligned on the row. Already produced by the source component via `isListed`. Verify the green "Listed" / muted "Unlisted" variants match the Figma swatches; no change if they do.
4. **Nickname · Property type line** — Render as a single muted text line with a middle-dot separator (`·` or `•`) between the two values. If either is empty, omit that segment and the separator.
5. **Address line** — Muted text, single line, truncated with ellipsis on overflow. No change to existing truncation behavior.
6. **Thumbnail** — Continue using the `image` field with the component's built-in fallback. The Figma shows the same blurred-bedroom fallback for every row — that's the existing fallback rendering correctly. **Do not** invent CDN URLs to populate the dummy data.

### Data model addition

The `Listing` type currently does not carry a unit-type field. For the prototype, add a `unitType: 'single' | 'multi'` field to the **prototype's** dummy listings data (`src/prototype/dummyListings.ts`) and to the `Listing` shape consumed by the prototype copy of `ListingItem.tsx`. Do **not** modify the type in the source repo.

Suggested seed: in `DUMMY_LISTINGS_EIGHT`, mark listings 2 and 5 as `'multi'` and the remaining six as `'single'` so the demo shows both pill variants. Inactive- and empty-state datasets inherit the same field.

The unit-type pill copy:
- `'single'` → render `Single Unit`
- `'multi'` → render `Multi Unit`

---

## 7. Out of scope for this patch

The following stay exactly as the implementation reference specifies — this patch does **not** modify them:

- OAuth mock logic, 1.5 s loading delay, `?mockError` flag handling (Appendix A4).
- Dummy data structure beyond the `unitType` field added in §6 (Appendix A6).
- The `IdListProvider` + `useIdListContext` selection behavior (Appendix A7).
- Embed pattern in the onboarding wizard shell — `Wizard` steps, `disableStepNavigation`, `onConnected` callback contract (Appendix A7).
- Bot Alert above sub-step 1 — still owned by the wizard shell, not by this connect-step patch (Appendix A7, DD-5).
- The "Back" button on step 2, the primary "Select listings" button, and their disabled-when-empty behavior (Appendix A5 e).

---

## 8. Acceptance criteria

A prototype build passes this patch when:

- [ ] Step 1 renders three distinct vertical sections (header → video → test-drive explainer) matching §2.
- [ ] Step 1 copy matches §3 verbatim, with no manual `<br />` line breaks inside the test-drive paragraphs.
- [ ] Step 1 video block embeds the YouTube video at `https://www.youtube.com/embed/LfFd_s2kz8Y` in a 16:9 frame; clicking the YouTube poster plays the real video inline.
- [ ] Step 2 heading and subtitle match §4 verbatim.
- [ ] Step 2 filters toolbar shows: `Select all`, `City`, `Status`, `Ownership`, `X/Y Filtered` counter, `Search` — in that order, left-aligned + right-aligned as in §5.
- [ ] The counter updates live as filters and search change, in the `filtered/total Filtered` format.
- [ ] Placeholder helper-texts from the Figma (`This is a … description.`) are **not** rendered.
- [ ] Each listing row renders: checkbox · thumbnail · optional co-host icon · listing name · unit-type pill · `Nickname · Property type` line · address line · right-aligned `Listed`/`Unlisted` pill.
- [ ] Co-host icon appears on the row whose `hostRole === 'co-host'` and only on that row.
- [ ] Both `Single Unit` and `Multi Unit` pill variants are visible in the default dummy dataset (at least one of each).
- [ ] No edits exist in `abnb-distribution-page-master/` — every change is in the prototype copies under `src/prototype/connect/` and `src/prototype/dummyListings.ts`.
- [ ] Production guard from Appendix A0 Rule 2 still wraps every mock file.

---

## 9. Source alignment — Guesty help center article

The Guesty help center article *"Pilot: Pre-onboarding an Airbnb account to Guesty (view-only)"* describes the **existing production** pre-onboarding flow inside the main Guesty app (Marketing & Sales → Distribution → Airbnb). It is the canonical source for terminology, reassurance language, and downstream behavior. The new onboarding-wizard implementation in this patch shares the same underlying product behavior but **restyles the entry-point UX** to fit a first-run wizard context.

### Terminology — confirmed by the article

| Term in this patch | Confirmed by article? | Source quote |
|---|---|---|
| `Airbnb listings to be imported` (Step 1 heading) | ✅ aligned | *"Review which listings will be copied to Guesty…"* |
| `view-only connection` (subtitle + button context) | ✅ official term | *"Pre-onboarding…creates a view-only version of Airbnb data…"* |
| `Multi Unit` pill (P-5) | ✅ official term | *"Multi-unit structures and their associated sub-units are automatically detected and imported with the correct configuration."* |
| `Listed` / `Unlisted` right-aligned pill (P-5) | ✅ official term | *"The listing will be imported in the same listed status as in Airbnb… if it is listed (or unlisted) in Airbnb, it will be listed (or unlisted) in Guesty."* |
| `Nickname` line on the listing row (P-5) | ✅ official term | *"The listing's nickname is retrieved from Airbnb. If none is provided, Guesty generates one automatically."* |
| No-sync reassurance subtitle on Step 2 | ✅ aligned with article's behavior | *"Data doesn't sync between platforms during pre-onboarding."* and *"Changes made to a pre-onboarded listing in Guesty don't sync to Airbnb."* |

This gives the integration team firmer footing on the `unitType` field (Decision 3 below): Guesty already names the concept "Multi-unit / sub-units" in user-facing documentation, so introducing `unitType: 'single' | 'multi'` on the production `Listing` type aligns the data model with existing nomenclature.

### CTA wording — deliberate divergence from production

The production flow described in the article uses **"Set up a view-only connection"** as the primary button (appears twice in the article — at the integration page entry point and inside the modal). The new onboarding wizard's Figma renames this CTA to **"Pre-connect to Airbnb"**.

This patch follows the **Figma**, not the article. Rationale (inferred from the design intent, to be confirmed):

- *"Pre-connect to Airbnb"* is shorter, more action-oriented, and reads more naturally in a first-run onboarding context where the user has not yet learned Guesty's "view-only" vocabulary.
- The full phrase "Set up a view-only connection" is still present on Step 1 — embedded in the subtitle (*"A view-only connection will import data without…"*) and in the sub-step label inside the Arc wizard (per Appendix A's `WizardStepData.label: 'Set up a view-only connection'`). So the official term is **introduced** before being abbreviated on the button.

**Action for stakeholders:** confirm this divergence is intentional before the prototype is reviewed externally. If alignment is preferred, the cheapest change is button copy only — every other instance of the official term remains intact.

### Optional microcopy from the article (not currently in the patch)

The article carries a `Tip` callout: *"Select only the listings you want to explore in Guesty to maintain control during pre-onboarding."*

The current Step 2 subtitle (*"Changes you make on Guesty won't sync to Airbnb until you fully connect the account and listings."*) already conveys the underlying reassurance, so we did **not** add the Tip. If user testing suggests selection anxiety on Step 2 (e.g. users selecting nothing or selecting all without thought), consider adding a single-line helper above the listings list:

> *Tip: Select only the listings you want to explore — you can always import the rest later.*

This is a future iteration, not a P-1 to P-5 change.

---

## 10. Resolved decisions (locked 2026-05-27)

1. **Video asset.** Embed the real explainer at [youtube.com/watch?v=LfFd_s2kz8Y](https://www.youtube.com/watch?v=LfFd_s2kz8Y) via an iframe pointing at `https://www.youtube.com/embed/LfFd_s2kz8Y`. See §2 for the iframe attributes. No placeholder card.
2. **Counter copy across locales.** Keep `X/Y Filtered` literally in **all** builds (English and localized). Rationale: the `/` is a direction-neutral glyph that renders consistently in LTR and RTL; the format is compact enough to fit the toolbar without wrapping at every breakpoint; the Figma source uses this exact form. Only the literal word `Filtered` gets translated — the numeric pattern stays.
3. **Unit-type source field in production.** Production **needs a new field** on the `Listing` type — `unitType: 'single' | 'multi'` (or equivalent enum). It is **not** derivable from `propertyType` (an apartment can be either a single rental or a multi-unit building, and the existing field doesn't encode that). Action item for the integration / wizard-shell team: add the field upstream of where listings are imported from the Airbnb API; the prototype anticipates this shape so the contract carries through cleanly. The prototype copy of `Listing` (in `src/prototype/connect/`) already includes `unitType`; the source-repo type stays untouched.
