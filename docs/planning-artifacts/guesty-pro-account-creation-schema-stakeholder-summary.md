---
title: "Guesty Pro Account Profile — Stakeholder Summary"
description: "Plain-language overview of what the account-creation schema contains. Companion to guesty-pro-account-creation-schema.md v0.3."
audience: "Non-technical stakeholders — PM, ops, onboarding, exec read-throughs"
date: 2026-06-03
companion: "guesty-pro-account-creation-schema.md"
---

# Guesty Pro Account Profile — Stakeholder Summary

> **Full technical spec:** [guesty-pro-account-creation-schema.md](guesty-pro-account-creation-schema.md) (v0.3)  
> **Example of a filled profile:** `poc-eval-harness/profiles/scored/A1.json`

---

## What is this?

A **complete customer profile** is everything Guesty needs to know about a new Pro customer **before the account is created and the first onboarding call (Call 1) is productive**.

The AI onboarding agent’s job is to **fill this profile through conversation** — not to read a fixed questionnaire word-for-word. The same profile is what the baseline decision tree branches over and what the onboarding specialist brief is built from.

This document explains **what topics the profile covers**, in plain language. It does not define field IDs, enums, or tool behavior.

---

## How “complete” is defined

| Level | What it means |
|-------|----------------|
| **Minimum** | Account can be created and Call 1 can be scheduled |
| **Target** | Call 1 is productive; meaningful auto-setup is possible |
| **Enriched** | Optional extras that reduce setup time on Call 1 — never required to proceed |

**Minimum viable profile** (must be recorded or explicitly flagged for a human):

- Company name, country, listing count, booking channels
- **Ownership model** — do they own their listings, manage for others, or both?
- **Go-live timing** — how soon they want to be live
- At least one **focus topic** or **pain point** — so Call 1 has a clear purpose

Financial and tax topics can be **deferred** (flagged for the human specialist) and the profile still meets the minimum bar.

---

## What the profile contains (10 topic areas)

| Area | Name | What we learn |
|------|------|----------------|
| **S0a** | Salesforce basics | Company name, country, listing count, channels, logo, third-party tools, assigned onboarding specialist — mostly **confirm**, not re-type |
| **S0b** | Sales handover note | AI reads the rep’s free-text note and extracts **hints to confirm** — e.g. prior PMS (Hostaway, Lodgify), language, add-ons, sentiment/risk flags for the specialist |
| **S1** | Brand | Logo for guest-facing surfaces (booking site, emails) |
| **S2** | Properties & channels | Listing count, which channels they use (Airbnb, Booking, VRBO, direct, etc.), **when they want to go live** |
| **S3** | Operations | Cleaning approach, turnover checklists, smart locks |
| **S4** | Financials | Revenue recognition, cancellation policy, security deposits, when guests pay, optional fees — **sensitive**; amounts are read back for confirmation; **taxes always go to a human** |
| **S5** | Booking website | Only if they care about direct bookings — site name, domain, terms |
| **S6** | Team & governance | Solo operator vs shared team; who gets which role on which listings |
| **S7** | Goals & pain | Top priorities for Call 1 (pick up to 3) plus “biggest blocker” in the customer’s own words |
| **S8** | Ownership & pricing | **Main adaptive branch** — self-owned vs property manager vs mixed; owner details and how they get paid; pricing approach |

---

## Three ideas to remember

### 1. Prefill, then confirm

Salesforce and the sales handover note provide starting answers. The AI **checks them with the customer** instead of asking cold questions.

Example: *“Sales noted you’re coming from Hostaway — is that still right?”*

### 2. Not everyone sees every question

The conversation adapts to context:

- **Booking website (S5)** — only if they use direct booking or mention a website
- **Owner details (S8)** — only if they manage properties for other owners
- **Payment split** — only if they don’t collect everything at booking

### 3. Some topics stay with the human specialist

The AI **captures intent** and **flags** the onboarding specialist (Jordan) when setup is high-risk or needs judgment:

- **Tax configuration** — always flagged; the agent never acts as tax advisor
- **Complex owner economics** — captured in plain language; specialist configures Business Models on Call 1
- **Risk/sentiment from sales notes** — surfaced on the brief only; not shown to the customer

---

## The main branching story (S8)

After we know **how many listings** they have, the conversation asks **who owns them**:

```
How many listings?
        │
        ▼
Who owns them?
   ├── All mine          → skip owner records → pricing / tools
   ├── All for others    → capture owner(s) + how PM gets paid
   └── Mixed             → capture owner(s) for managed listings
```

This is the **hero adaptive branch** — the part that changes most between customers and is hardest to capture in a fixed wizard.

---

## Concrete example — profile A1

| Topic | Value |
|-------|-------|
| Business | Harbor Point Rentals, Sarasota FL |
| Listings | 5 |
| Channels | Airbnb, VRBO, direct |
| Ownership | All self-owned |
| Financials | Pay at booking; damage waiver $50; taxes **flagged for specialist** |
| Website | Harbor Point Stays (Guesty subdomain) |
| Call 1 focus | Pricing strategy, guest messaging |
| Pain | *“Manual pricing takes too much time — adjusting rates by hand every morning.”* |

See the full machine-readable profile: `poc-eval-harness/profiles/scored/A1.json`.

---

## What to use in a stakeholder session

| Question | Where to look |
|----------|----------------|
| What topics does the AI cover? | This document — table in § “What the profile contains” |
| What’s the minimum to proceed? | § “How complete is defined” |
| What does a filled customer look like? | `poc-eval-harness/profiles/scored/A1.json` |
| How does the AI behave live? | Streamlit demo — `poc-eval-harness` interactive UI, profile **A1** |
| Full field definitions & rules | [guesty-pro-account-creation-schema.md](guesty-pro-account-creation-schema.md) |

---

## Scope notes (PoC)

- Field names and enums are **synthetic** — reconstructed for the PoC; production validation still required.
- **Airbnb connection** happens inside the product, not in this pre-call questionnaire.
- The harness runtime copy of the schema lives at `poc-eval-harness/schema/guesty-pro-account-creation-schema.md` (same content as the planning doc).
