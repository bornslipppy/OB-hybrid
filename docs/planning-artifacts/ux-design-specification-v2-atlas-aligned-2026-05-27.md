---
title: "Guesty Pro Onboarding Wizard — UX Copy Specification v2 (Atlas-aligned)"
---

# Guesty Pro Onboarding Wizard — UX Copy Specification v2 (Atlas-aligned)

**Date:** 2026-05-27
**Author:** Sally (UX Designer)
**Status:** Companion specification to the master UX design spec.
**Master spec:** [docs/planning-artifacts/ux-design-specification-2026-05-25.md](ux-design-specification-2026-05-25.md)
**Airbnb Connect implementation:** [docs/planning-artifacts/airbnb-connect-implementation-reference.md](airbnb-connect-implementation-reference.md) + [docs/planning-artifacts/airbnb-connect-ux-patch-2026-05-27.md](airbnb-connect-ux-patch-2026-05-27.md)
**Atlas source standards:** `atlas-design-copilot-master/standards/{voice-and-tone,style,glossary.json,canonical-copy,content-principles,legal-safety}.md` and `knowledge/ux-writing/checks.md`.

---

## 0. Reading order

This document is the **single source of truth for every user-facing string** in the onboarding wizard. The master UX spec keeps owning architecture, flow, state machines, and component contracts; this file replaces every copy decision inside it.

If a string here disagrees with the master spec or with the Airbnb implementation reference, **this file wins**. Open a follow-up to align the older docs.

Read top to bottom on first pass. After that, jump directly to the section you need — every screen has its own table.

---

## 1. Scope and what changed

### In scope

- Every heading, subtitle, label, button, helper text, placeholder, validation message, empty state, success toast, error message, and bot utterance in the 10-section wizard.
- The full Airbnb Connect sub-flow (Q1.4 Step 1 + Step 2), incorporating the locked decisions from the 2026-05-27 patch.
- Glossary alignment for wizard-specific concepts that didn't yet have canonical terms.
- Microcopy patterns (errors, empty states, success, loading, validation, tooltips, confirmations).

### Out of scope

- Visual design tokens, animation timings, component anatomy — owned by the master spec's Visual Design Foundation and Component Strategy sections.
- State machines (DC-3, DC-8, DC-9, DC-10') — owned by the master spec's Cross-Cutting State Machines section.
- Event taxonomy — owned by master spec §Event Taxonomy.

### What changed vs. the master spec

A full delta table lives in §18. The high-level summary:

- **Sentence case applied everywhere** — many headings in the master spec used Title Case ("Choose Listings to Import", "Setup in Progress"). All flattened.
- **All exclamation marks removed.** "You're halfway through!" → "You're halfway through."
- **Bot voice strings rewritten** to match the Humble Expert tone — no "Great!", no "Awesome!", no "Don't worry."
- **Loading copy made specific** — "Loading…" → "Loading your listings…", "Connecting to Airbnb…", "Saving changes…".
- **CTAs verbed and concrete** — "Continue" stays only where the action genuinely is "continue to next step"; everywhere else it becomes "Confirm and continue", "Select listings", "Send invitations", etc.
- **Glossary compliance** — "OTA" → "channel" in user-facing copy, "popup" → "dialog", "type" → "enter", "remove" reserved for non-destructive removal, "delete" for permanent.
- **Airbnb Connect Q1.4** — adopts the full Step 1 / Step 2 restructure from the 2026-05-27 patch (see §4.4 + §4.5).

---

## 2. Foundation — voice, principles, and standards

### 2.1 Voice (constant across every surface)

| Attribute | What it means here | This, not that |
|---|---|---|
| **Clear** | Plain words, one idea per sentence, max ~25 words. | "Set up a view-only connection so your existing tools keep running" — not "Establish a non-disruptive read-only integration." |
| **Confident** | We know property management. We guide without hedging. | "You'll see your listings here once Airbnb is connected." — not "You should hopefully be able to see your listings…" |
| **Warm** | We write like a colleague, not a corporation. We use "you" and contractions. | "We'll keep your data view-only until you're ready." — not "The system will maintain read-only mode pending user authorization." |
| **Honest** | We don't over-promise, soften bad news, or hide consequences. | "This can't be undone." — not "Just a heads-up, this is permanent." |

**Hard prohibitions (binary — no exceptions):**

- Never playful during errors. No "Oops!"
- Never celebratory during destructive confirmations. No "Great! Property deleted."
- Never blame the user. "Enter a valid email address." — not "You entered an invalid email."
- Never use softening language for serious consequences. No "just", "simply", "easy".
- Never expose technical internals (error codes, stack traces, system names).
- Never use exclamation marks. Confidence comes from clarity.
- Never use emojis in product UI.

### 2.2 Style (mechanical rules)

- **Sentence case everywhere** — headings, labels, buttons, menu items, tabs, column headers. Only the first word and proper nouns capitalize. Product names always capitalize: Guesty PMS, GuestyPay, Channel Manager, Booking Engine.
- **No terminal punctuation on** headings, labels, buttons, tab names, column headers, incomplete-sentence list items.
- **Terminal punctuation required on** complete sentences in body copy, tooltips, error messages, alert / banner text.
- **Oxford comma** required in all lists.
- **En dash (–)** for ranges, **em dash (—)** for breaks (no surrounding spaces).
- **Numbers:** spell zero–nine, numerals for 10+. Always numerals with units (3 listings, 8 cities, 24 hours).
- **Contractions** used naturally (you'll, we're, it's).
- **American English** (color, cancelation, dialog).
- **Acronyms:** spell out on first use, then abbreviate. PMS spelled out once per major surface.

### 2.3 Glossary (canonical terms used in this spec)

| Concept | Use | Don't use |
|---|---|---|
| A guest's stay | **reservation** (canonical), *booking* and *stay* acceptable | "appointment" |
| Person staying at a property | **guest** | "tenant", "customer", "client", "renter" |
| Property manager using Guesty | **host** | "landlord" |
| Digital representation on a channel | **listing** | "property page", "rental page" |
| Physical asset | **property** | "unit", "rental" |
| Booking site (Airbnb, Booking.com, Vrbo) | **channel** | "OTA", "platform" |
| Connection to a third-party service | **integration** | "third-party connection", "plugin", "add-on" |
| User's Guesty account | **account** | "profile" |
| Authentication action | **sign in** | "log in", "login" |
| Choose from a list or dropdown | **select** | "choose", "pick" |
| Type text into a field | **enter** | "type", "input", "key in" |
| Move to another screen | **go to** | "navigate to", "visit" |
| Permanent data removal | **delete** | "remove", "erase" |
| Non-destructive removal from a view | **remove** | "delete", "take out" |
| Making something new | **create** | "make", "add new", "generate" |
| Changing existing content | **edit** | "modify", "change", "update" |
| Persisting changes | **save** | "store", "keep", "commit" |
| Overlay requiring response | **dialog** | "modal", "popup", "overlay" |
| Expandable selection list | **dropdown** | "drop-down", "select box" |
| Single-line entry | **text field** | "text box", "input field" |

**Wizard-specific terms** (proposed additions to `glossary.json` — see §17):

| Concept | Canonical | Notes |
|---|---|---|
| The pre-onboarding flow | **pre-connect** (verb), **pre-connection** (noun) | Replaces inconsistent "view-only setup", "pilot connection" |
| The Airbnb data import preview | **view-only connection** | Per Guesty help center wording |
| The mid-funnel celebratory canvas | **milestone** | Not "celebration", not "achievement" |
| The post-OAuth canvas reveal | **AHA reveal** internally; **your account preview** user-facing | Never use "AHA" in user-facing copy |
| Owner who receives payouts | **owner** within Owner's Portal context; **host** elsewhere | Scoped glossary exception |
| The 10-section configuration flow | **onboarding wizard** | Not "setup wizard", "configuration tool" |

**Words to avoid (general):** Click here, Kindly, Please (overuse), Simply / Just, Utilize, Due to the fact that, In order to, Very / Really / Totally, internal CS slang.

### 2.4 Content principles (precedence order)

When two voice rules conflict, principles decide. They are ranked — higher rules win.

1. **Clarity over cleverness.** Add words if cutting them would confuse.
2. **Accuracy over optimism.** A warm lie is worse than a direct truth.
3. **Helpfulness over brevity.** A short dead-end is worse than a longer path forward.
4. **Contextual over generic.** If the system knows the listing name, count, or amount — use it.
5. **User perspective over system perspective.** "You couldn't save your changes." — not "The system failed to persist the entity."
6. **Consistency over local optimization.** Same word for the same thing across the wizard.
7. **Empathy over efficiency.** In moments of frustration, acknowledge before instructing.

---

## 3. Wizard structure overview

10 sections, ~25–30 questions depending on branching. Three canvas reveal moments: Q1.4 (AHA, holds through Q1.5), Section 3 entry (4.5s milestone), Section 8 (entire section).

| # | Section | Anchor bot? | Canvas reveal? |
|---|---|---|---|
| 1 | Pre-flight | Yes | Yes — at Q1.4, holds through Q1.5 |
| 2 | Operations | Inline only | No |
| 3 | Financials | Yes | Yes — 4.5s milestone at section entry |
| 4 | Booking Website | Yes | No |
| 5 | Governance | Inline only | No |
| 6 | Focus Topics | Inline only | No |
| 7 | Business | Inline only | No |
| 8 | Review and confirm | Yes | Yes — entire section |
| 9 | Setup in progress | None (loader) | No |
| 10 | Done | None (dashboard) | No |

---

## 4. Section 1 — Pre-flight

Anchor bot present on every question. Canvas hidden through Q1.3, reveals at Q1.4 on OAuth success, holds through Q1.5.

### 4.1 Section header (persistent)

| Element | Copy |
|---|---|
| Section nav label | `Pre-flight` |
| Section progress | `Section 1 of 8` (Sections 9 and 10 not counted in user-facing progress — they're outcomes, not configuration) |

### 4.2 Q1.1 — Listing count confirm

| Element | Copy |
|---|---|
| Bot (anchor) | `Welcome. We'll pull most of this in automatically — you'll just confirm what's right.` |
| Heading | `How many active listings do you have?` |
| Subtitle (only if Salesforce prefilled) | `We pulled this from your sales call. Confirm or update it before we connect Airbnb.` |
| Prefilled value chip | `{count} active listings` (e.g. `8 active listings`) |
| Primary CTA (prefilled) | `Looks right` |
| Secondary CTA (prefilled) | `Update count` |
| Numeric input label (no prefill) | `Active listings` |
| Numeric input placeholder | `e.g. 8` |
| Validation — empty | `Enter your number of active listings.` |
| Validation — non-numeric | `Enter a whole number.` |
| Validation — outlier soft | `That's higher than most accounts. Looks right?` |

### 4.3 Q1.2 — Airbnb-only check

| Element | Copy |
|---|---|
| Heading | `Are your listings on Airbnb only, or other channels too?` |
| Option A | `Airbnb only` |
| Option B | `Airbnb plus other channels` |
| Helper (below options) | `We'll connect the other channels later. Airbnb first because it gives us the richest data.` |

### 4.3a Q1.3 — Channel confirmation (shown only if Q1.2 = "Airbnb plus other channels")

| Element | Copy |
|---|---|
| Heading | `Which channels are your listings on today?` |
| Subtitle | `Airbnb stays selected — we'll connect it on the next screen.` |
| Checkbox group label | `Channels` |
| Checkbox — Airbnb (locked checked) | `Airbnb` |
| Checkbox — Booking.com | `Booking.com` |
| Checkbox — Vrbo | `Vrbo` |
| Checkbox — Expedia | `Expedia` |
| Checkbox — Other | `Other (we'll ask which)` |
| Primary CTA | `Continue` |

### 4.4 Q1.4 — Airbnb Connect, Step 1 of 2 (Pre-connect)

> This screen is built by reusing `ConnectAbnb.tsx` from `abnb-distribution-page-master`, with the structure from the 2026-05-27 patch. The copy below is locked.

**Layout:** three vertical sections — header → video → test-drive explainer + CTA. See [airbnb-connect-ux-patch-2026-05-27.md §2](airbnb-connect-ux-patch-2026-05-27.md).

| Element | Copy |
|---|---|
| Arc wizard sub-step label | `Set up a view-only connection` |
| Anchor bot (above section A) | `We only request view-only access — Guesty reads your listings but never changes them, messages guests, or accepts reservations on Airbnb's side.` |
| Section A — heading (h2) | `Airbnb listings to be imported` |
| Section A — subtitle | `A view-only connection will import data without making changes to your listings on Airbnb.` |
| Section B — section label | `Watch this video to get more information` |
| Section B — video iframe `title` attribute | `Pre-connect to Airbnb — view-only explainer` |
| Section C — section label | `Start test-driving Guesty:` |
| Section C — paragraph 1 | `Test Guesty without affecting your listings on Airbnb. The property management software you're using will still be connected to Airbnb until you decide to switch to Guesty.` |
| Section C — paragraph 2 | `We'll import real data from Airbnb so you can explore Guesty. We won't sync changes in Guesty to Airbnb until you are ready to switch and fully connect the Airbnb account.` |
| Primary CTA | `Pre-connect to Airbnb` |
| Loading state (button) | `Connecting to Airbnb…` |
| Error — OAuth token expired (Alert critical) | `Your Airbnb session may have expired. Sign in to Airbnb again to continue.` |
| Error — scope rejected (Alert critical) | `Looks like permission wasn't granted. We only need view-only access — try again to grant it.` |
| Error — network (Alert critical) | `Airbnb didn't respond. Check your connection and try again.` |
| Error — retry CTA | `Try again` |

**Why "Pre-connect to Airbnb" not "Set up a view-only connection" on the button:** the official term *view-only connection* is introduced in the subtitle and in the Arc wizard sub-step label, so the abbreviated CTA is grounded in context. The patch's source-alignment rationale carries forward (§9 of the patch).

### 4.5 Q1.4 — Airbnb Connect, Step 2 of 2 (Choose listings)

> Built by reusing `ImportListingsContent.tsx`, with the toolbar and row changes from the 2026-05-27 patch.

| Element | Copy |
|---|---|
| Arc wizard sub-step label | `Import listings` |
| Anchor bot | `Pick the listings you want to test Guesty with. You can always import the rest later.` |
| Heading (h2) | `Choose listings to import` |
| Subtitle | `Changes you make in Guesty won't sync to Airbnb until you fully connect the account and listings.` |

**Filters toolbar (left to right):**

| Element | Copy | Notes |
|---|---|---|
| Bulk-select checkbox label | `Select all` | Default state: checked (idSet seeded from all listings on mount per patch §6). |
| Filter dropdown — City | `City` | Trigger displays selected value beside the label, e.g. `City: All`. Default: `All`. |
| Filter dropdown — Status | `Status` | Default: `All`. Options: `All`, `Listed`, `Unlisted`. |
| Filter dropdown — Ownership | `Ownership` | Default: `All`. Options: `All`, `Owner`, `Co-host`. |
| Filter dropdown options — All | `All` | Used as the default selection across all three filters. |
| Filtered counter | `{filtered}/{total} Filtered` | Live-updates with filters and search. See patch §5. Localizable word: `Filtered`. |
| Search field placeholder | `Search…` | |
| Search field aria-label | `Search listings by name, nickname, or address` | |

**Helper-text placeholders from Figma** (`This is a checkbox description.`, etc.) are **discarded** — they're Figma component stubs.

**Listing row anatomy:**

| Element | Copy / behavior |
|---|---|
| Row checkbox aria-label | `Select listing {listing name}` |
| Listing name | `{listing.name}` — rendered from data |
| Co-host indicator | `Users` icon from lucide-react, rendered before name when `hostRole === 'co-host'`. Tooltip: `You co-host this listing on Airbnb.` |
| Unit-type pill — single | `Single Unit` |
| Unit-type pill — multi | `Multi Unit` |
| Secondary line | `{nickname} · {propertyType}` — middle-dot separator, omit a segment if missing |
| Tertiary line | `{address}` — single line, truncated with ellipsis on overflow |
| Status pill — listed | `Listed` |
| Status pill — unlisted | `Unlisted` |

**Action row (bottom of step 2):**

| Element | Copy |
|---|---|
| Primary CTA | `Select listings` |
| Primary CTA disabled tooltip | `Select at least one listing to continue.` |
| Secondary CTA | `Back` |
| Per-row status (when in-flight in prototype) | Not used — selection is instant. |

**Empty-state branches** (DC-9):

| Branch | Heading | Body | CTA |
|---|---|---|---|
| B1 — zero listings on Airbnb | `No listings on this Airbnb account` | `This account doesn't have any listings yet. You can keep exploring Guesty without importing — your sales contact will help you set up listings on your call.` | `Continue without importing` |
| B2 — all listings inactive on Airbnb | `Every listing is unlisted on Airbnb` | `We can still import them. Once you fully connect, you can list them from Guesty.` | `Import {count} unlisted listings` |
| B4 — partial data only | `We imported what we could` | `Some listing fields didn't make it across. You can fill the gaps later in Guesty.` | `Continue` |

### 4.6 Q1.5 — Going-live timeline (canvas held visible)

| Element | Copy |
|---|---|
| Anchor bot | `Your Airbnb data is in. Now we'll set up Guesty to match how you work.` |
| Heading | `When do you want to go live with Guesty?` |
| Helper (above options) | `This sets the pace for your onboarding calls — you can change it later.` |
| Option A | `Within 2 weeks` |
| Option B | `In 2 to 4 weeks` |
| Option C | `In 1 to 2 months` |
| Option D | `Not sure yet` |
| Primary CTA | `Continue` |

### 4.7 Canvas — AHA reveal copy (Q1.4 → Q1.5)

| Element | Copy |
|---|---|
| Canvas header | `Your Airbnb account` |
| Listings counter line | `{count} listings imported` |
| Reservations counter line | `{count} reservations synced` |
| Messages counter line | `{count} guest messages` |
| Footer reassurance | `View-only — nothing in Airbnb has changed.` |
| Screen-reader live-region announcement on reveal | `Your Airbnb account is connected. {count} listings, {count} reservations, and {count} guest messages imported in view-only mode.` |

### 4.8 Canvas — degraded mode (UJ-7 OAuth fallback)

| Element | Copy |
|---|---|
| Overlay heading | `We'll connect this on your call` |
| Overlay body | `Airbnb didn't connect on this attempt. {csm_name} will finish it with you on your kickoff call — your wizard answers are saved.` |
| Primary CTA | `Continue without Airbnb` |
| Secondary CTA | `Try connecting again` |

---

## 5. Section 2 — Operations

Body section. Inline italic bot voice only — no anchor `Alert`.

### 5.1 Q2.1 — Cleaning system

| Element | Copy |
|---|---|
| Heading | `How do you manage cleaning today?` |
| Inline italic helper | `We'll match the rest of Guesty's settings to whatever you tell us here.` |
| Option A | `In-house team` |
| Option B | `External cleaning service` |
| Option C | `Mix of both` |
| Option D | `I handle it myself` |
| Salesforce-prefill chip (when present) | `Pre-filled from your sales call. Looks right?` |
| Confirm CTA | `Looks right` |
| Edit CTA | `Change` |

### 5.2 Q2.2 — Cleaning timing (skipped if Q2.1 = "External cleaning service")

| Element | Copy |
|---|---|
| Heading | `When does cleaning usually happen?` |
| Option A | `Same day as check-out` |
| Option B | `Day after check-out` |
| Option C | `Day before check-in` |
| Option D | `It varies` |

### 5.3 Q2.3 — Inspection requirement

| Element | Copy |
|---|---|
| Heading | `Do you inspect properties between guests?` |
| Option A | `Always` |
| Option B | `Sometimes` |
| Option C | `Never` |

### 5.4 Q2.4 — Turnover checklist with upload option

| Element | Copy |
|---|---|
| Heading | `Do you have a turnover checklist your cleaners follow?` |
| Option A | `Yes — I'll upload it` |
| Option B | `Use Guesty's standard template` |
| Option C | `Skip for now` |
| Empty file picker | `Drag a file here, or select from your computer.` |
| File picker — selected file | `{filename} · {size}` |
| File picker — replace link | `Replace` |
| File picker — remove link | `Remove` |
| Upload progress | `Uploading {filename}…` |
| Upload success toast | `Turnover checklist uploaded` |
| Upload error — wrong file type | `That file type isn't supported. Use PDF, DOC, or DOCX.` |
| Upload error — too large | `Files must be under 10 MB. Yours is {size}.` |
| Upload error — generic | `Upload didn't go through. Try again or check your connection.` |
| Retry CTA | `Try again` |

### 5.5 Q2.5 — Check-in method

| Element | Copy |
|---|---|
| Heading | `How do guests check in?` |
| Option A | `Smart lock or keypad` |
| Option B | `Lockbox` |
| Option C | `In-person hand-off` |
| Option D | `Mix of methods` |

### 5.6 Q2.6 — Smart lock provider (only if Q2.5 = "Smart lock or keypad" or "Mix")

| Element | Copy |
|---|---|
| Heading | `Which smart lock do you use?` |
| Combobox label | `Smart lock brand` |
| Combobox placeholder | `Search brands…` |
| Combobox empty result | `No matches. Select "Other" to enter a brand name.` |
| Other option | `Other` |
| Free-text label when Other selected | `Brand name` |
| Free-text placeholder | `e.g. August, Schlage Encode` |

---

## 6. Section 3 — Financials

Anchor bot present. Canvas reveals at section entry for 4.5 seconds (milestone), then hides for the rest of the section.

### 6.1 Mid-funnel milestone canvas (4.5s hold on first entry)

| Element | Copy |
|---|---|
| Canvas heading | `You're halfway through.` |
| Canvas body | `Listings and operations are set. Financials next, then a few short sections after that.` |
| Countdown indicator (aria-live polite) | `Continuing in {seconds} seconds.` |
| Optional skip-ahead CTA | `Continue now` |

### 6.2 Q3.1 — Revenue recognition

| Element | Copy |
|---|---|
| Anchor bot | `These choices shape how Guesty reports your earnings. Pick what matches your accountant's books.` |
| Heading | `When do you count revenue from a reservation?` |
| Option A | `When the guest checks in` |
| Option B | `When the reservation is booked` |
| Option C | `When the payment is received` |
| Option D | `Spread across the stay` |
| Tooltip on each option | One-sentence explanation of the accounting treatment — see §14.8 for tooltip pattern. |

### 6.3 Q3.2 — Non-refundable rates

| Element | Copy |
|---|---|
| Heading | `Do you offer non-refundable rates?` |
| Option A | `Yes, on all listings` |
| Option B | `Yes, on some listings` |
| Option C | `No` |

### 6.4 Q3.3 — Security deposit or damage waiver

| Element | Copy |
|---|---|
| Heading | `How do you handle damage protection?` |
| Option A | `Security deposit (held and released)` |
| Option B | `Damage waiver (non-refundable fee)` |
| Option C | `Both, depending on the listing` |
| Option D | `Neither` |

### 6.5 Q3.4 — Payment timing

| Element | Copy |
|---|---|
| Heading | `When are guests charged?` |
| Option A | `Full amount at booking` |
| Option B | `Deposit at booking, balance before check-in` |
| Option C | `Full amount before check-in` |
| Option D | `Custom schedule` |

### 6.6 Q3.5 — Payment split

| Element | Copy |
|---|---|
| Heading (if Q3.4 = "Deposit at booking, balance before check-in") | `What's the deposit amount?` |
| Option A | `25% of the total` |
| Option B | `50% of the total` |
| Option C | `A flat amount` |
| Flat amount label | `Deposit amount` |
| Flat amount placeholder | `e.g. 250` |
| Currency hint | `In {accountCurrency}` |

### 6.7 Q3.6 — Mandatory fees (Fee Builder)

| Element | Copy |
|---|---|
| Heading | `What fees do you charge guests, on top of the nightly rate?` |
| Subtitle | `Add every fee that applies to most reservations. You can edit per-listing later.` |
| Row — fee type label | `Fee type` |
| Row — fee type placeholder | `e.g. Cleaning fee, City tax` |
| Row — amount label | `Amount` |
| Row — amount placeholder | `0.00` |
| Row — unit dropdown label | `Charged` |
| Row — unit option A | `Per reservation` |
| Row — unit option B | `Per night` |
| Row — unit option C | `Per guest, per night` |
| Add-row CTA | `Add another fee` |
| Remove-row link | `Remove` |
| Inline soft validation | `That's higher than most accounts. Looks right?` |
| Inline blocking validation | `Enter an amount.` |
| Primary CTA | `Continue` |
| Skip link | `I don't charge mandatory fees` |

### 6.8 Q3.7 — Taxes (3-step sub-wizard)

| Element | Copy |
|---|---|
| Sub-step indicator | `Step {n} of 3` |
| Step 1 heading | `What taxes apply to your reservations?` |
| Step 1 helper | `Select every tax type that applies. We'll set the rates next.` |
| Step 1 option — Sales/VAT | `Sales tax or VAT` |
| Step 1 option — Occupancy | `Occupancy or tourist tax` |
| Step 1 option — City | `City or local tax` |
| Step 1 option — Other | `Other` |
| Step 2 heading | `What rates apply?` |
| Step 2 row label — Tax name | `Tax name` |
| Step 2 row label — Rate | `Rate` |
| Step 2 row label — Base | `Calculated on` |
| Step 2 base option A | `Pre-tax subtotal` |
| Step 2 base option B | `Total with other taxes` |
| Step 3 heading | `Anything seasonal or per-location?` |
| Step 3 option A | `Rates are the same year-round, every location` |
| Step 3 option B | `Rates change by season or location` |
| Step 3 — seasonal flow (if B) | `We'll handle that with your CSM after the wizard. We've noted it for your kickoff call.` |
| Primary CTA on each step | `Continue` |
| Back link | `Back` |

---

## 7. Section 4 — Booking Website

Anchor bot present. No canvas.

### 7.1 Q4.1 — Business profile (Salesforce-prefilled)

| Element | Copy |
|---|---|
| Anchor bot | `These details show up on your booking website and on guest emails. We've pre-filled what we have from your sales call.` |
| Heading | `Your business profile` |
| Business name label | `Business name` |
| Business name helper | `Appears in the website header and email signatures.` |
| Email label | `Contact email` |
| Email placeholder | `e.g. hello@yourbusiness.com` |
| Email validation — empty | `Enter a contact email.` |
| Email validation — invalid | `Enter a valid email address.` |
| Domain label | `Website domain (optional)` |
| Domain placeholder | `e.g. yourbusiness.com` |
| Domain helper | `If you don't have one yet, leave it blank — Guesty will host you on a guesty.com subdomain.` |
| Primary CTA | `Continue` |

### 7.2 Q4.2 — Terms and conditions

| Element | Copy |
|---|---|
| Heading | `Terms and conditions for your booking website` |
| Subtitle | `Required by most jurisdictions before you can take reservations.` |
| Option A | `Use Guesty's standard terms (you can edit later)` |
| Option B | `Upload my own (PDF or DOC)` |
| Helper under option A | `Drafted by Guesty's legal team to cover common short-term rental scenarios. You're responsible for confirming they fit your jurisdiction.` |
| Upload empty state | `Drag your terms file here, or select from your computer.` |

### 7.3 Q4.3 — Cookie policy

Same pattern as Q4.2 — substitute `Cookie policy` for `Terms and conditions`. No additional copy.

---

## 8. Section 5 — Governance

Body section. Inline italic bot voice only.

### 8.1 Q5.1 — Decision owners

| Element | Copy |
|---|---|
| Heading | `Who makes the calls on Guesty settings?` |
| Inline italic helper | `Just you, or a few people splitting different areas?` |
| Option A | `Just me` |
| Option B | `Me plus a few teammates` |
| Option C | `A different person for each area` |

### 8.2 Q5.2 — Invite teammates (skippable)

| Element | Copy |
|---|---|
| Heading | `Invite anyone to help you set Guesty up?` |
| Subtitle | `They'll get a link to join your account and pick up where you left off.` |
| Row — Email label | `Email` |
| Row — Email placeholder | `name@example.com` |
| Row — Role dropdown label | `Role` |
| Role option — Account owner | `Account owner — full access` |
| Role option — Admin | `Admin — most settings, no billing` |
| Role option — Operator | `Operator — day-to-day operations only` |
| Add row CTA | `Add another teammate` |
| Send CTA | `Send invitations` |
| Skip link | `Skip for now` |
| Success toast (per invitation) | `Invitation sent to {email}` |
| Error — invalid email | `Enter a valid email address.` |
| Error — duplicate | `You've already added this email.` |

---

## 9. Section 6 — Focus Topics

Body section. Inline italic bot voice.

### 9.1 Q6.1 — Call 1 focus topics

| Element | Copy |
|---|---|
| Heading | `What do you want to dig into on your first onboarding call?` |
| Inline italic helper | `Pick up to three. Your CSM will lead with these.` |
| Multi-select checkboxes (examples — full list comes from product) | `Pricing strategy`, `Channel mix`, `Guest messaging`, `Cleaner workflows`, `Accounting setup`, `Owner reporting`, `Booking website`, `Reviews and reputation` |
| Max-selected message | `You've picked 3 topics — that's the limit. Remove one to add another.` |
| Primary CTA | `Continue` |

### 9.2 Q6.2 — Biggest pain (free text)

| Element | Copy |
|---|---|
| Heading | `In one sentence, what's the biggest thing slowing you down right now?` |
| Subtitle | `Your CSM reads this before your call. The more specific, the better.` |
| Textarea placeholder | `e.g. I'm losing hours every week chasing cleaners after late check-outs.` |
| Character counter | `{remaining} characters left` (soft limit 280) |
| Over-limit message | `Try to keep it under 280 characters — your CSM will dig in on the call.` |
| Primary CTA | `Continue` |

---

## 10. Section 7 — Business

Body section. Inline italic bot voice. Several sub-screens are optional and clearly skippable.

### 10.1 Q7.1 — Brand logo upload

| Element | Copy |
|---|---|
| Heading | `Upload your logo` |
| Subtitle | `Appears on your booking website and in guest emails. PNG or SVG, square works best.` |
| Empty state | `Drag your logo file here, or select from your computer.` |
| Skip link | `I'll add this later` |
| Replace link | `Replace logo` |
| Remove link | `Remove logo` |
| Remove confirmation — dialog title | `Remove your logo?` |
| Remove confirmation — dialog body | `Your logo will be removed from this account. You can upload it again any time.` |
| Remove confirmation — confirm | `Remove` |
| Remove confirmation — cancel | `Cancel` |
| Upload error — wrong type | `Logos must be PNG, JPG, or SVG.` |
| Upload error — too large | `Logos must be under 5 MB. Yours is {size}.` |

### 10.2 Q7.2 — Owner records CSV

| Element | Copy |
|---|---|
| Heading | `Upload your owner records` |
| Subtitle | `A CSV with each owner's name, email, and the listings they own. We'll match them up next.` |
| CSV template link | `Download CSV template` |
| Empty file picker | `Drag a CSV file here, or select from your computer.` |
| Validating state | `Checking your CSV…` |
| Validation success | `{count} owners loaded` |
| Validation error — wrong type | `Owner records must be a CSV file.` |
| Validation error — missing columns | `Your CSV is missing required columns: {column_names}. Use the template if you're not sure.` |
| Validation error — empty file | `That CSV doesn't have any rows. Add owner records and try again.` |
| Skip link | `I don't manage on behalf of owners` |

### 10.3 Q7.2a — Owner-to-listing matcher (only if Q7.2 uploaded AND Airbnb connected)

| Element | Copy |
|---|---|
| Heading | `Match owners to listings` |
| Subtitle | `Drag each owner from the left onto the listings they own on the right. Anything left over goes on your Call 1 punch list.` |
| Left column header | `Owners ({count})` |
| Right column header | `Listings ({count})` |
| Filter — unmatched only | `Show unmatched only` |
| Listing card — matched chip | `Matched to {owner_name}` |
| Listing card — unmatched chip | `No owner assigned` |
| Auto-match suggestion banner | `We found {count} likely matches by name. Review and accept the ones that look right.` |
| Auto-match accept-all CTA | `Accept all matches` |
| Auto-match dismiss link | `Dismiss suggestions` |
| Primary CTA | `Continue` |
| Skip link | `Match the rest on my call` |

### 10.4 Q7.3 — Rate strategy (skipped if dynamic-pricing tool detected)

| Element | Copy |
|---|---|
| Heading | `How does your pricing change over the year?` |
| Toggle — same year-round | `Pricing is the same year-round` |
| Date range — high season label | `High season` |
| Date range — low season label | `Low season` |
| Add date range CTA | `Add another date range` |
| Helper | `We'll use these to set up your rate strategies. You can refine them in Guesty's pricing tool later.` |

---

## 11. Section 8 — Review and confirm

Anchor bot. Canvas visible for the entire section — full summary with edit links.

### 11.1 Left panel

| Element | Copy |
|---|---|
| Anchor bot | `Last step before we set everything up. Look it over — anything off, click "Edit" to fix it.` |
| Heading | `Review your answers` |
| Subtitle | `Once you confirm, we'll set up your Guesty account with these choices. You can change anything later in settings.` |
| Primary CTA | `Confirm and continue` |
| Secondary CTA | `Go back to edit` |
| Skip-warning chip (per skipped item) | `{count} items will go to your Call 1 punch list — your CSM will help you finish them.` |
| Skip-warning expand link | `See punch list` |

### 11.2 Canvas — Review summary (Accordion)

| Element | Copy |
|---|---|
| Section header — Pre-flight | `Pre-flight` |
| Section header — Operations | `Operations` |
| Section header — Financials | `Financials` |
| Section header — Booking website | `Booking website` |
| Section header — Governance | `Governance` |
| Section header — Focus topics | `Focus topics` |
| Section header — Business | `Business` |
| Edit link (per row) | `Edit` |
| Edit link aria-label | `Edit {question_name}` |
| Skipped row chip | `Skipped — added to punch list` |
| Empty section header (nothing answered) | `Nothing to review here.` |

### 11.3 Confirmation dialog (on "Confirm and continue" — destructive-ish)

| Element | Copy |
|---|---|
| Title | `Confirm your setup?` |
| Body | `We'll start setting up your account with these answers. You can change settings later, but you can't reopen this wizard.` |
| Confirm | `Confirm setup` |
| Cancel | `Keep reviewing` |

---

## 12. Section 9 — Setup in progress

Full-viewport loader. No bot, no canvas.

### 12.1 Per-item progress

| Element | Copy |
|---|---|
| Heading | `Setting up your Guesty account` |
| Subtitle | `This usually takes under a minute. You can leave this tab open — we'll let you know when it's done.` |
| Item in progress (per row) | `{Item}…` (e.g. `Importing reservations…`, `Connecting Booking.com…`, `Setting up fees…`) |
| Item done (per row) | `{Item} ✓` (e.g. `Reservations imported ✓`) — checkmark via icon, not literal text |
| Item skipped (recoverable) | `{Item} — we'll finish this on your call` |
| Item failed (partial) | `{Item} — couldn't complete. Your CSM will fix it.` |
| Overall progress | `{done} of {total} steps complete` |
| Estimated time remaining (after first item) | `About {seconds} seconds left` |

### 12.2 Failure / partial outcome (rare)

| Element | Copy |
|---|---|
| Heading | `Setup couldn't finish completely` |
| Body | `Most of your setup is done. A few items need your CSM — they'll wrap them up on your kickoff call.` |
| Primary CTA | `Go to your dashboard` |
| Secondary CTA | `See what's pending` |

---

## 13. Section 10 — Done dashboard

Dashboard surface, not wizard. Includes Call 1 punch list and focus-topic widgets.

### 13.1 Welcome state (first arrival)

| Element | Copy |
|---|---|
| Heading | `You're set up, {first_name}.` |
| Subtitle | `Your Guesty account is ready. Your next onboarding call is on {date} at {time} ({timezone}) — {csm_name} will lead it.` |
| Primary CTA | `Go to your dashboard` |
| Secondary CTA | `See your punch list` |

### 13.2 Next session widget

| Element | Copy |
|---|---|
| Widget title | `Your next onboarding call` |
| Widget body | `{call_name} with {csm_name} · {date} at {time} ({timezone})` |
| Add to calendar link | `Add to calendar` |
| Reschedule link | `Reschedule` |
| Empty state (no call scheduled) | `Your CSM will email you to schedule your first call within 24 hours.` |

### 13.3 Punch list widget

| Element | Copy |
|---|---|
| Widget title | `Call 1 punch list` |
| Widget body (with items) | `{count} items to wrap up with {csm_name} on your call.` |
| Widget body (zero items) | `Nothing pending — you finished every section.` |
| Item row label | `{item_name}` |
| Item row context | `Skipped in {section_name}` |
| Mark-as-done link | `Mark done` |

### 13.4 Focus topic widget

| Element | Copy |
|---|---|
| Widget title (per topic) | `{focus_topic}` |
| Widget body | One-sentence preview of what the user said in Q6.2, plus a "Learn more" link to the relevant Guesty docs. |
| Learn more link | `Learn more about {focus_topic}` |

### 13.5 Recap widget

| Element | Copy |
|---|---|
| Widget title | `Your setup in 30 seconds` |
| Counter — listings | `{count} listings imported` |
| Counter — reservations | `{count} reservations synced` |
| Counter — messages | `{count} guest messages` |
| Counter — teammates | `{count} teammates invited` (omit if zero) |

---

## 14. Microcopy patterns

These patterns apply across every section. Always reach for these before writing one-off copy.

### 14.1 Buttons

| Pattern | Copy | Notes |
|---|---|---|
| Primary advance | `Continue` | Use only when the action genuinely is "continue to the next step". Replace with verb+object wherever possible (`Select listings`, `Send invitations`, `Confirm setup`). |
| Confirm a configuration | `Confirm {object}` | e.g. `Confirm setup`, `Confirm changes` |
| Back navigation | `Back` | Never `< Back` — chevron handled visually by the component. |
| Cancel an action | `Cancel` | Pairs with destructive confirms; never `Abort`, `Stop`. |
| Skip optional section | `Skip for now` | Implies returnability — only use when the user can come back. |
| Skip permanent | `Skip this step` | Use when the action is one-shot and won't be re-asked. |
| Retry after error | `Try again` | Never `Retry` alone. |
| Upload | `Upload {file_type}` | e.g. `Upload terms`, `Upload logo` |

Buttons are sentence case, 1–3 words for primary, no terminal punctuation. Never `OK`, `Submit`, `Done` as a primary CTA — they don't say what happens.

### 14.2 Errors (Inform → Explain → Guide → Reassure → Shortcut)

Every blocking error follows this five-beat structure. Beats can collapse for inline validation; in full-page errors, all five are present.

| Beat | Purpose | Example |
|---|---|---|
| **Inform** | Name what happened in user terms. | `We couldn't connect to Airbnb.` |
| **Explain** | Why, in one sentence if knowable. | `Airbnb didn't respond — they might be having an outage.` |
| **Guide** | What to do next. | `Wait a moment and try again, or skip this step for now.` |
| **Reassure** | What's safe. | `Your wizard answers are saved.` |
| **Shortcut** | The fastest recovery. | `Try again` / `Skip for now` |

**Inline (field-level) validation** collapses to Inform + Guide:

- `Enter a valid email address.`
- `Enter a whole number.`
- `Pick at least one listing to continue.`

**Form-level validation** collapses to Inform + Guide + Shortcut:

- `Some fields need attention. Fix the highlighted items before you continue.` + scroll-to-first-error link.

### 14.3 Empty states

Pattern: explain why empty → suggest the next useful action → CTA.

| Surface | Heading | Body | CTA |
|---|---|---|---|
| Step 2 listings — zero listings (DC-9 B1) | `No listings on this Airbnb account` | `This account doesn't have any listings yet. You can keep exploring Guesty without importing — your sales contact will help you set up listings on your call.` | `Continue without importing` |
| Owner CSV — before upload (Q7.2) | `Upload a CSV with your owners` | `We'll match each owner to their listings in the next step. Use Guesty's template if you're not sure of the format.` | `Download CSV template` |
| File upload (Q2.4, Q4.2, Q4.3) | `Use Guesty's standard {document}` | `You can upload your own version later in settings.` | `Use Guesty's {document}` |
| Owner-listing matcher — no matches yet (Q7.2a) | `Drag owners onto listings to match them` | `Anything left unmatched goes on your Call 1 punch list — your CSM will help finish it.` | (no CTA — the work is in the drag interaction) |
| Section nav — locked | (tooltip only) | `Complete the previous section to continue here.` | — |
| Search — no results (filter toolbar, Q1.4 Step 2) | `No listings match "{query}"` | `Check your spelling or try a broader search.` | — |
| Filter — no results (Q1.4 Step 2) | `No listings match these filters` | `Try removing a filter or adjusting your criteria.` | — |
| Punch list — zero items (Section 10) | `Nothing pending` | `You finished every section. Your CSM will use your call time to dive deeper.` | — |

### 14.4 Success toasts

Brief, no exclamation marks, no celebration.

| Pattern | Copy |
|---|---|
| Item created | `{Item} created` |
| Item updated | `Changes saved` |
| Item deleted | `{Item} deleted` |
| Item uploaded | `{Item} uploaded` |
| Connection established | `{Channel} connected` |
| Invitation sent | `Invitation sent to {email}` |
| Settings saved | `Settings saved` |

Display duration: 8s default, 12s if `prefers-reduced-motion`. Pause on focus. Maximum one visible at a time.

### 14.5 Loading states

Always specific. Never `Loading…` alone.

| Pattern | Copy |
|---|---|
| Generic data retrieval | `Loading {items}…` (e.g. `Loading your listings…`) |
| Specific action in progress | `{Verb}ing {object}…` (e.g. `Saving changes…`, `Sending invitations…`) |
| First-load setup | `Setting up your {feature}…` |
| OAuth round-trip | `Connecting to Airbnb…` |
| File upload | `Uploading {filename}…` |
| Validation in flight | `Checking your CSV…` |

### 14.6 Inline validation

Field-level, soft, and blocking validations are visually distinct (per §3056 of the master spec). Copy patterns:

- **Inline (informational)** — muted text, no icon. `Appears on your booking website and in guest emails.`
- **Soft (confirmation needed)** — warning color + icon, `Looks right?` pattern. `That's higher than most accounts. Looks right?` + `Confirm` link.
- **Blocking (must fix)** — destructive color + icon, advance disabled. `Enter a valid email address.`

Validation triggers:
- **On blur or submit** for completeness checks.
- **Live** only for format checks (email shape, currency symbols).
- **Never on every keystroke** for anything else.

### 14.7 Save status (WriteStatusIndicator — field-scoped)

| State | Visual | aria-live announcement |
|---|---|---|
| Idle | (none) | — |
| Pending | Amber edge + spinner | (silent) |
| Acked | Green check, fades 1.5s | `Saved` (once, polite) |
| Failed | Amber edge + inline chip | `Saving failed. Press Tab to review.` (polite) |

Never use a global "Saving…" banner. Save status is always field-scoped.

### 14.8 Tooltips

- Concise single sentences.
- Explain purpose, not mechanics.
- Don't restate the label.
- If a tooltip is needed to explain a label, the label is wrong — rewrite the label.

Example (Q3.1 revenue recognition options):

| Label | Tooltip |
|---|---|
| `When the guest checks in` | `Revenue counts on the check-in date — the most common method for short-term rentals.` |
| `When the reservation is booked` | `Revenue counts the day the guest books, even if the stay is months later.` |
| `When the payment is received` | `Revenue counts whenever each payment lands.` |
| `Spread across the stay` | `Revenue is split across each night of the reservation.` |

### 14.9 Confirmation dialogs

Use Atlas canonical patterns. Sentence case, no exclamation marks, no softening language.

**Delete (irreversible):**
```
Title: Delete {item}?
Body: This will permanently delete {item}. This can't be undone.
Confirm: Delete {item}
Cancel: Cancel
```

**Disconnect integration:**
```
Title: Disconnect {channel}?
Body: {Channel} will stop syncing with Guesty. Existing data won't be affected.
Confirm: Disconnect
Cancel: Cancel
```

**Remove teammate:**
```
Title: Remove {name}?
Body: {Name} will lose access to this account immediately.
Confirm: Remove
Cancel: Cancel
```

**Unsaved changes:**
```
Title: Unsaved changes
Body: You have unsaved changes. Leave without saving?
Primary: Leave without saving
Secondary: Keep editing
```

---

## 15. Bot voice — anchor screens and body

### 15.1 Anchor sections (1, 3, 4, 8)

The bot speaks in plain language, advisory tone — Atlas's *Humble Expert* persona.

- Max 3 sentences per utterance.
- No "Great!", "Awesome!", "Don't worry!".
- Uses contractions naturally.
- Explains *why*, not *what*. (The question heading says what; the bot says why it matters.)

| Section | Bot utterance |
|---|---|
| Section 1 entry (Q1.1) | `Welcome. We'll pull most of this in automatically — you'll just confirm what's right.` |
| Q1.4 — Pre-connect (Step 1) | `We only request view-only access — Guesty reads your listings but never changes them, messages guests, or accepts reservations on Airbnb's side.` |
| Q1.4 — Choose listings (Step 2) | `Pick the listings you want to test Guesty with. You can always import the rest later.` |
| Q1.5 — Going-live timeline | `Your Airbnb data is in. Now we'll set up Guesty to match how you work.` |
| Section 3 entry (Q3.1) | `These choices shape how Guesty reports your earnings. Pick what matches your accountant's books.` |
| Section 4 entry (Q4.1) | `These details show up on your booking website and on guest emails. We've pre-filled what we have from your sales call.` |
| Section 8 entry | `Last step before we set everything up. Look it over — anything off, click "Edit" to fix it.` |

### 15.2 Body sections (2, 5, 6, 7)

Inline italic — no `Alert` chrome, no bot avatar. Embedded directly under the question heading.

- Max 1 sentence.
- Adds context the question alone can't carry.
- Removed entirely if the question is fully self-explanatory.

Examples (already in §5–§10 above):

- Q2.1: *We'll match the rest of Guesty's settings to whatever you tell us here.*
- Q5.1: *Just you, or a few people splitting different areas?*
- Q6.1: *Pick up to three. Your CSM will lead with these.*

### 15.3 Salesforce-prefill chip pattern

When data came from the sales call, surface it with a single-line attribution chip and a quick-confirm pattern.

| Element | Copy |
|---|---|
| Chip text | `Pre-filled from your sales call. Looks right?` |
| Confirm CTA | `Looks right` |
| Edit CTA | `Change` |

---

## 16. Section navigation

The persistent header shows section progress and state.

| State | Icon | Tooltip / accessible label |
|---|---|---|
| Done | ✓ | `{Section name} — done` |
| Current | ● | `{Section name} — current section` |
| Unlocked | ○ | `{Section name} — go to this section` |
| Locked | 🔒 | `Complete the previous section to continue here.` |
| Skipped | ⊘ | `{Section name} — added to your Call 1 punch list` |

Section names match the table in §3. Always sentence case.

---

## 17. Glossary alignment for wizard-specific terms

These concepts didn't have canonical terms in Atlas's `glossary.json`. Proposed additions, with the rationale required by Atlas's terminology-research rubric.

| Concept | Canonical | Prohibited synonyms | Rationale |
|---|---|---|---|
| The pre-onboarding view-only flow | **pre-connect** (verb), **pre-connection** (noun) | "pilot connection", "trial connection", "view-only setup" | Grounded in Guesty help center wording. Verb form fits CTAs ("Pre-connect to Airbnb"); noun form fits documentation. |
| The Airbnb data preview that follows pre-connect | **view-only connection** | "read-only mode", "preview mode" | Used verbatim in Guesty's help center. Adds clarity about scope (read, not write). |
| The mid-funnel celebratory canvas | **milestone** | "celebration", "achievement", "checkpoint" | Neutral, professional, doesn't over-promise. Matches Atlas's *Humble Expert* persona. |
| The post-OAuth canvas reveal | **AHA reveal** (internal); **your account preview** (user-facing) | "WOW moment", "magic moment" | Never use "AHA" in user-facing copy — it's an internal team shorthand. |
| The 10-section configuration flow | **onboarding wizard** | "setup wizard", "configuration tool", "intake form" | Already used in product. Add to glossary so other surfaces don't drift. |
| The list of skipped items deferred to the kickoff call | **Call 1 punch list** | "to-do list", "pending items", "deferred tasks" | Connects two domain concepts (onboarding calls + remaining work) into one named artifact. |
| The kickoff onboarding session | **onboarding call** (generic), **Call 1** / **Call 2** (specific instance) | "kickoff meeting", "sync" | Aligns with how the CSM team already names these sessions. |
| Listing unit type | **unit type** — values `Single Unit` / `Multi Unit` | "property type" (separate concept), "structure type" | Production needs this as a new field on `Listing` (confirmed in Airbnb patch §9). Distinct from `propertyType` (apartment vs. villa), which is orthogonal. |

**Conflicts flagged for Atlas team review:**

- The master spec uses `OTA` in places (e.g. UJ-3); `glossary.json` prohibits this in user-facing copy. This spec uses **channel** throughout. Master spec needs a sweep.
- Master spec uses both `delete` and `remove` interchangeably. This spec restricts `delete` to permanent destruction and `remove` to reversible removal-from-view, per glossary.

---

## 18. Copy audit — deltas from prior spec

The Atlas-grade audit of the master spec's user-facing copy. Severity levels per Atlas:

- **Critical** — wrong terminology, contradicts standards, misleading.
- **Warning** — style inconsistency, suboptimal but not wrong.
- **Info** — optimization opportunity.

### 18.1 Critical

| # | Location (master spec) | Current copy | New copy (this spec) | Standard |
|---|---|---|---|---|
| C1 | §UJ-1 mermaid label, Section 3 milestone | `You're halfway through.` (with exclamation in some renders) | `You're halfway through.` (no exclamation, period only) | `style.md` — no exclamation marks |
| C2 | §UJ-1 mermaid label, Section 3 milestone | `Listings + Operations set.` | `Listings and operations are set.` | `style.md` — sentence case; `style.md` — spell out, avoid `+` in copy |
| C3 | §Q1.5 area (master spec implicit) | `WOW step` (used in flow labels, but leaks into some titles) | `Connect Airbnb` (label); internal-only `AHA reveal` allowed | `voice-and-tone.md` — Humble Expert; never expose internal shorthand |
| C4 | §Empty State Copy — Section nav locked tooltip | `Complete the previous section to continue here.` | (unchanged — passes audit) | — |
| C5 | §A4 (Appendix A) — paragraphs with manual `<br />` | Two-paragraph block with manual line breaks | Single flowing paragraphs (per Airbnb patch §3) | `style.md` — let text wrap naturally |
| C6 | §Q3.1 / §Bot specification | Various places use `Great!` / `Awesome!` as bot openers in examples | Removed in every utterance in §15 | `voice-and-tone.md` — never celebratory in onboarding |

### 18.2 Warning

| # | Location | Current | New | Standard |
|---|---|---|---|---|
| W1 | §Master spec section headings | `Choose Listings to Import` (Title Case in some renders) | `Choose listings to import` | `style.md` — sentence case |
| W2 | §Master spec — "Setup in Progress" | `Setup in Progress` | `Setup in progress` | `style.md` — sentence case |
| W3 | §Q3.6 fee builder | `Continue` everywhere | Specific verb where action is concrete (e.g. `Add another fee`); `Continue` only between sections | `checks.md` 1.1 — buttons are verb+object |
| W4 | §A5 button | `Select listings` | (unchanged — passes audit) | — |
| W5 | §Master spec — "Showing N listings" in toolbar | `Showing 8 listings` | `8/8 Filtered` (per Airbnb patch §5) | Consistency with Figma, direction-neutral for RTL |
| W6 | Bot Component Specification — "Anchor screens use Alert" | Doesn't specify max-sentence count | Bot max 3 sentences; body inline max 1 sentence (codified §15) | `voice-and-tone.md` Layer 3 |
| W7 | §UJ-7 OAuth fallback canvas overlay | `Coming on your call` | `We'll connect this on your call` | `voice-and-tone.md` — user perspective, not system fragment |
| W8 | §Loading-state rules | `Loading…` referenced as acceptable generic | Always specify: `Loading your listings…`, `Connecting to Airbnb…`, `Saving changes…` | `checks.md` 1.17 — informative & specific |
| W9 | §Q5.2 invite teammates | `Invite team members` (some places) | `Invite teammates` everywhere | Consistency — pick one and stick to it |
| W10 | §Section names | Mix of `Booking Site` and `Booking Website` | `Booking website` everywhere | Glossary consistency |

### 18.3 Info

| # | Location | Change | Standard |
|---|---|---|---|
| I1 | Q1.4 Step 2 row format | Add `Single Unit` / `Multi Unit` pill explicitly per Airbnb patch §6 | `glossary.json` proposed addition |
| I2 | Q1.4 Step 2 toolbar | Drop the placeholder helper texts (`This is a checkbox description.`) | Figma stubs, not real copy |
| I3 | §Section 10 dashboard | Tighten "Your setup in 30 seconds" recap copy | `content-principles.md` — contextual over generic |
| I4 | §Section 8 confirmation dialog | Use canonical "Unsaved changes" pattern from `canonical-copy.md` | Consistency |

### 18.4 Cross-cutting patterns identified

| Pattern | Affected elements | Recommendation |
|---|---|---|
| Mixed sentence/Title case across section headings | Section nav labels, screen headings | Sweep master spec to sentence case throughout |
| Generic "Continue" CTA overused | Q1.5, Q3.x, Q4.x, Q7.x | Replace with verb+object wherever the action is concrete; keep `Continue` only when the action genuinely is "continue to next step" |
| Internal shorthand (AHA, WOW) leaks into user-facing labels | Mermaid flow labels, occasional headings | Reserve internal vocabulary for engineering docs; user-facing copy never uses these terms |
| `Loading…` used as filler | Various inline states | Always specify what's loading |
| Inconsistent terminology — `delete` vs `remove` | Q7.1 logo, Q5.2 teammate, master spec misc. | Use glossary: `delete` = permanent, `remove` = reversible from view |

### 18.5 Score

Per Atlas's audit scoring criteria (0 Critical, 0–2 Warning = pass):

- **Critical findings:** 6 — addressed in this spec.
- **Warning findings:** 10 — addressed in this spec.
- **Info findings:** 4 — addressed in this spec.

**Score:** the master spec as-is would have been **needs-work** under Atlas. This spec brings it to **pass** for every screen catalogued above.

---

## 19. Acceptance criteria for this spec

A new screen, error, or microcopy element passes this spec when:

- [ ] Sentence case used for the heading, subtitle, buttons, labels, and tab names.
- [ ] No exclamation marks anywhere.
- [ ] No `Click here`, `Just`, `Simply`, `Kindly`, `Utilize`.
- [ ] Glossary-compliant terminology — `reservation`, `guest`, `host`, `listing`, `property`, `channel`, `integration`, `select`, `enter`, `delete` (permanent), `remove` (reversible), `dialog` (not modal/popup).
- [ ] Buttons are verb+object, 1–3 words, no terminal punctuation. Never `OK`, `Submit`, generic `Done`.
- [ ] Errors follow Inform → Explain → Guide → Reassure → Shortcut (or the collapsed inline form).
- [ ] Loading states are specific — never bare `Loading…`.
- [ ] Empty states explain why + what's next + a CTA where helpful.
- [ ] Bot utterances ≤ 3 sentences (anchor) or ≤ 1 sentence (inline italic).
- [ ] Numbers: zero–nine spelled out, 10+ as numerals. Always numerals with units.
- [ ] Oxford comma in lists.
- [ ] American English spelling.
- [ ] No emojis in product UI.
- [ ] No exposed technical internals (error codes, stack traces, system names).
- [ ] All user-facing copy uses `you` for the user, `we` only when Guesty acts on the user's behalf.
- [ ] Destructive actions state irreversibility (`This can't be undone.`).
- [ ] Every field with constraints has helper text or a placeholder that previews the format.

---

## 20. Open questions

1. **Salesforce-prefill chip permanence.** Should the `Pre-filled from your sales call. Looks right?` chip dismiss after confirmation, or persist as a source-attribution badge? Atlas's `voice-and-tone.md` argues for persistent attribution; current implementation dismisses. Defaulting to dismiss for now.
2. **Punch list naming.** `Call 1 punch list` is grounded in CSM-team vocabulary but unfamiliar to users on day one. Worth user-testing alongside `To finish on your call` as an alternative. Recommendation lives in §17.
3. **Bot avatar character.** The master spec specifies an `Avatar` slot in the `Alert` but doesn't name the bot or its persona. Atlas leans Humble Expert; if the bot gets a name, the voice loosens slightly. Out of scope for this copy spec — flag for branding.

---

## 21. Maintenance

- Each section's copy register lives in one place — this file. Master spec links here for copy.
- When adding a new screen, add its row(s) to the relevant section table here, then update the master spec's flow diagrams if structure changes.
- Quarterly: re-run the audit in §18 against the live product to catch drift.
- Whenever Atlas's `glossary.json` adds a term, sweep this spec for prior synonyms.

---

**End of UX Copy Specification v2 (Atlas-aligned, 2026-05-27).** 🎨
