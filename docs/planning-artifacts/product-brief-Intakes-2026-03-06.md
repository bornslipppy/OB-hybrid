---

title: "Product Brief: Intakes"

date: '2026-03-06'

lastUpdated: 2026-03-06
---

# Product Brief: Intakes

## Core Vision

### Problem Statement

Teams know what to build. They can't encode it in a form coding agents can act on.

The 56-page PRD is the wrong artifact for an AI-native world. It's too long, too prose-heavy, scattered across Figma, Slack, Google Docs, and Google Sheets, and stale within days of being published. Critical sections are TBD. Open questions go unresolved. The developer column is empty. Decisions live in three channels simultaneously — a Figma comment, a Slack thread, a verbal agreement in a meeting — and nobody knows which one is current.

This isn't a failure of effort. It's the wrong format for how work happens now.

The Augment research makes the cost empirical: 33,000+ agent PRs studied. #1 rejection reason: missing context. 80% require human fixes. Agents aren't failing because they can't code. They're failing because the spec they're working from was written for a human to interpret, not a machine to execute.

**The real gap isn't discovery. It's encoding.**

Getting from "we need to unify our financial configuration" to "here is a file Cursor can execute on without hallucinating the gaps" requires a structured process that doesn't exist yet. Product teams either skip it — and the agent drifts — or spend months producing a 56-page document that the agent still can't parse.

### The Shift: The Plan Becomes the Product

As the Augment Code article puts it: *"At that point, the plan becomes the product. The code is simply the result of executing it."*

This changes everything about what the primary artifact of product work is. It's not the PRD. It's not the Figma file. It's the machine-executable plan — short, structured, explicit — that sits in git as the living source of truth and feeds directly into the coding agent.

```yaml
initiative: Business Models for All
goal: Unify financial configuration across all user types

signals:
  - GPro users constrained by Revenue Share Formulas that don't scale
  - Accounting users duplicate entire models for small variations

constraints:
  - NRI logic takes precedence over all components ("NRI is King")
  - Locked accounting periods block activation and reprocessing

hypotheses:
  - 5-step wizard reduces setup time by 50%
  - Component architecture eliminates model duplication

tasks:
  - [ ] Unified navigation for all user types
  - [ ] 5-step wizard: NRI → Commission → Fees → Assign → Review
  - [ ] Version history and audit log

open_questions:
  - Migration: automatic or phased?
  - Permissions: who can create/edit business models?
```

50 lines. Not 56 pages. A coding agent can read this. It won't go stale — you edit one field, not a prose paragraph buried on page 23.

### Proposed Solution

Intakes is a guided product intent encoding tool for non-technical product builders. You bring your signals — customer interviews, PFRs, usage data, Slack threads, existing specs. Intakes runs a structured synthesis and produces a machine-executable plan: short, explicit, structured, living in git as the primary artifact.

The output isn't a recommendation. It's a plan — with goals, signals, constraints, hypotheses, tasks, and open questions made explicit. The kind of file a coding agent reads and executes without hallucinating the gaps.

### Why Existing Tools Don't Solve This

**Traditional PM tools (Google Docs, Notion, Confluence):**
Written for humans to read, not machines to parse. No structure, no validation, no git integration. Gets stale and scattered across too many tools the moment a decision changes.

**AI chat (ChatGPT, Claude):**
Produces fluffy recommendations, not structured plans. No persistent memory across sessions. No connection to the codebase or existing signals. Resets every conversation.

**Cursor:**
Extraordinarily powerful — once the spec exists. It's a blank canvas that assumes intent has already been encoded. No guided workflow for product discovery. No signal ingestion. Produces developer artifacts, not PM-readable plans.

**Babysitter and execution-layer tools:**
Handle quality gates *during* agent execution. Assume the spec is already good. Intakes produces the spec that these tools then execute on. Complementary, not competitive.

**The gap:** No tool sits at the product intent layer — taking scattered human signals and encoding them into a machine-executable plan before a single line of code is written.

---

## Target Users

### Primary Persona: Eliana — Senior Product Manager at a Mid-Size B2B SaaS

Eliana is the PM who wrote a 56-page PRD for a single feature. She's been in the role for two years, owns two product areas, and is good at her job. She's not the problem. The format is.

**Who she works with:**
Principal Designer, Design Lead, Director of Design, Director of PM, CEO, and a development team that has opinions — all with competing priorities and limited availability.

**Where her signals live:**
Customer interviews in Modjo. PFRs in a spreadsheet. Usage data in a dashboard. Competitive analysis in a Google Doc. CEO input in a Slack thread from last Tuesday. Design notes in Figma comments. No single source of truth.

**What she does with them:**
Reads everything, synthesizes manually, writes a Google Doc, gets conflicting feedback from five stakeholders, rewrites it, schedules alignment meetings, rewrites again, and eventually publishes a 56-page PRD — with two TBD sections, unresolved open questions, and external links to three supporting documents — that will be stale within a week.

**Time from signal to developer handoff:** One to four months for complex features.

**Where the process breaks — every time:**

- The CEO overrides a data-driven direction after a single customer conversation
- A developer not involved early enough pushes back at handoff, requiring spec rework while the next feature is already due
- Decisions get made in three channels simultaneously — Figma comments, Slack threads, verbal agreements — with no canonical version
- A stakeholder gives feedback in week six that should have been given in week two
- The PRD is published but already stale — a decision changed last week and nobody updated the document

**What a good week looks like:** Stakeholders aligned early, decisions in one place, the spec moves forward without doubling back. Eliana estimates this happens about 30% of the time.

**How Intakes changes her week:**

Eliana brings her signals. Intakes runs a structured synthesis and produces a 50-line machine-executable spec: goals, constraints, hypotheses, tasks, open questions — all explicit, all in one place, all in git.

When a decision changes, she edits one field. Not a prose paragraph on page 23.

When the coding agent runs, it executes on her intent — right constraints respected, right scope, no hallucinated assumptions. She reviews a working result, not a clarification thread.

**The "aha" moment:**

When she pushes the spec and the coding agent proposes an implementation that matches her intent exactly — nothing hallucinated, nothing misinterpreted, nothing missing. She realizes: *she's not a spec writer anymore. She's a plan author. And the plan is the product.*

---

### Secondary Persona: Yair — Principal Designer navigating the same process

Yair doesn't write the PRD. He lives with it. He translates it into Figma, fields questions from developers about design decisions that weren't in the spec, and spends half his time in alignment meetings that exist because the source of truth is scattered.

For him, Intakes is the thing that finally makes direction stable enough to design against at speed. When the spec is live, current, and machine-readable, the designer and the developer can move in parallel instead of sequentially. The back-and-forth that sends projects "one step forward, two steps back" collapses.
