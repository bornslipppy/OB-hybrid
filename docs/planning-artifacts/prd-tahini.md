---
title: "Product Requirements Document - Tahini"

stepsCompleted: ['step-01-init', 'step-02-discovery', 'step-02b-vision', 'step-02c-executive-summary', 'step-03-success', 'step-04-journeys', 'step-05-domain-skipped', 'step-06-innovation', 'step-07-project-type', 'step-08-scoping', 'step-09-functional', 'step-10-nonfunctional', 'step-11-polish']
inputDocuments: ['Polaris Product Brief v5.1.md']
workflowType: 'prd'
classification:
  projectType: 'SaaS B2B (MVP: API-first with thin web surface)'
  domain: 'Design Tooling / DesignOps'
  complexity: 'medium'
  projectContext: 'greenfield'
---

# Product Requirements Document - Tahini

**Author:** Yair
**Date:** 2026-04-09

## Executive Summary

Tahini is a structured-context engine built exclusively for product design teams. Not for meetings. Not for sales calls. Not for engineering. For design — where intent lives in spatial hierarchies, component relationships, and layout decisions that no horizontal tool knows how to read.

The landscape is crowded with generic context and knowledge management tools. None of them understand that design context is fundamentally different from text. A meeting can be transcribed. A sales call is sequential audio. Design intent lives partly in words and partly in *geometry* — Figma layer trees, auto-layout decisions, component variants, design system usage, comments anchored to canvas positions. Capturing the geometric half is a deeper problem than text transcription, and no horizontal tool is attempting it. Tahini exists because design needs its own context engine, purpose-built for its own substrate.

The problem is two-sided. Design intent at scale is fragmented and ungoverned: scattered across Figma comments, Slack threads, and senior designers' heads, never written down in a form anyone can query. Simultaneously, AI agents now doing real design work (Figma Make, Cursor, custom copilots) produce generic output because they lack team-specific context. These are the same problem viewed from two angles. Solving one solves the other.

Tahini runs as a cloud-hosted agent on Anthropic's platform. When a designer reaches a moment where context is useful — a review, a handoff, a decision — Tahini ingests the relevant Figma file content, joins it with the team's structured knowledge layer (principles, domain definitions, personas, prior decisions, design system rules), and synthesizes a structured intent artifact. That artifact is stored in a queryable corpus and exposed via API/MCP to downstream agents and human reviewers.

The MVP is built for one customer: Guesty, a $150M ARR property management platform with 30 designers, a mature design system, and an existing structured knowledge layer of ~70 files already built by the founder in his role as Principal of Design. This is not a cold start — half the product already exists. The MVP builds the signal extraction layer on top of it and validates the end-to-end loop: real design problem, real extraction, real artifact, real downstream improvement.

Tahini is API-first for the MVP with a thin web surface that makes the before/after magic visible — a designer triggers extraction, a structured intent artifact comes back, and the Guesty UX Copilot grounded in that artifact produces output visibly preferred over its ungrounded baseline. The long-term trajectory is SaaS B2B as the customer base grows; multi-tenancy, RBAC, and workspace management are explicitly deferred to post-POC phases.

### What Makes This Special

**Vertical specialization is the strategy, not a limitation.** Every horizontal context tool — Notion, Confluence, Granola, generic RAG pipelines — treats all content as text. Design is not text. Design is spatial, hierarchical, and multi-modal. The principles a team follows, the components they chose and why, the layout constraints they respected, the prior decisions they referenced — these live in the canvas, not in a document. Tahini is the only product that reads this substrate natively. The vertical is the wedge, not the ceiling.

**Structure is the moat, not smarts.** Tahini does not claim to reason better than a frontier model. Reasoning is commodity. The value is turning loose, fragmented, between-the-cracks design context into structured, queryable, citable artifacts with a specific shape — a shape that encodes 15 years of product design leadership practice. The schema looks simple until you try to replicate it, at which point you discover that every field exists because a senior design leader learned the hard way that you need it.

**Founder-market fit is the second moat.** The founder is not a technologist who identified a design problem. He is the exact buyer persona — a design executive who has spent a decade scaling UX orgs at Guesty, Culture Trip, Alike, and Designit, and who built the knowledge layer at Guesty by hand because no product existed to do it. The schema requirements are not speculative; they are extracted from a working system the founder already operates manually.

**The accumulating corpus is the third moat.** Every intent artifact Tahini produces makes the corpus more valuable. After 12 months, the corpus is useful. After 24 months, it is structurally irreplaceable. Switching means losing the team's accumulated design memory.

## Project Classification

| Attribute | Value |
|-----------|-------|
| **Project Type** | SaaS B2B (MVP phase: API-first with thin web surface) |
| **Domain** | Design Tooling / DesignOps |
| **Complexity** | Medium — no regulatory constraints; domain complexity in schema design and extraction quality |
| **Project Context** | Greenfield |
| **MVP Timeline** | 4–6 weeks from kickoff |
| **POC Customer** | Guesty (30 designers, mature design system, existing knowledge layer) |

## Success Criteria

### User Success

The product succeeds for users when a senior Guesty designer, reviewing a downstream agent's output grounded in a Tahini artifact, recognizes their team's principles and prior decisions in the output — without being told Tahini was involved. The "aha" moment is not "this is a nice summary." It is "this agent knows how we think."

Specific user success indicators:
- A senior designer can scan a Tahini artifact and confirm it correctly identifies the domain, persona, and applicable principles for the design problem — in under 2 minutes
- The artifact surfaces prior decisions and cross-domain considerations the designer would have raised in review but hadn't yet documented
- The Guesty UX Copilot produces output the designer would be willing to hand back to the original designer without rewriting

### Business Success

Tahini's MVP success is measured at Guesty only. There is no external design partner target for the MVP. Tahini earns its existence if it demonstrably improves the quality of agent-assisted design work at one real company.

- **Primary metric:** Blind paired comparison win rate of grounded vs ungrounded agent output, evaluated by senior Guesty designers on 10–15 real design tasks. Target: 70%+ win rate with reasons that explicitly cite Guesty-specific context (a principle, a prior decision, a domain consideration, a persona need)
- **Quality of wins:** At least 60% of winning reasons must be tagged as Guesty-specific context, not generic improvement. This separates "Tahini makes output better" from "Tahini makes output longer"
- **Evaluation protocol:** Blind paired comparison. Two outputs per task (grounded vs ungrounded), randomized order, stripped of markers. Senior Guesty designers — not the founder — rate with forced binary choice, structured reason tagging, and a "would you ship this" yes/no. The founder is excluded as a rater

### Technical Success

Technical success criteria are scoped to what a solo non-technical founder can measure and act on. Traditional infrastructure SLAs (uptime, throughput, concurrency) are not measured at MVP scale — they require infrastructure the founder doesn't control and can't fix.

Four measurable, actionable metrics:

| # | Metric | Target | What it proves |
|---|--------|--------|----------------|
| 1 | End-to-end loop completion on real Guesty Figma files | 10+ files without manual intervention | Tahini works reliably |
| 2 | Schema-valid artifacts on first attempt | 95%+ | Downstream consumers can read the output |
| 3 | Time from invocation to artifact | Under 3 minutes | Demo-viable, not embarrassing in a pitch |
| 4 | Founder quality rating against hand-authored benchmark | 80%+ rated "acceptable" on field-by-field rubric | Extraction quality clears the bar |

### Measurable Outcomes

The MVP is done when all of the following are true:
- The end-to-end loop runs on 10+ real Guesty Figma files and produces schema-valid artifacts
- A hand-authored benchmark suite exists and extracted artifacts match it on the founder's field-by-field rubric
- The blind paired comparison has been run on 10–15 real tasks with senior Guesty designers as raters
- The win rate is 70%+ with Guesty-specific reasons

If any of these fail, the specific failure is diagnosed before iterating. If the win rate is below 70%, the question is whether the problem is extraction quality (fixable) or schema design (harder). Each failure has a named next step.

## User Journeys

> **Architectural note:** Artifacts are scoped to Figma files, not to invokers. An artifact about a junior designer's invoice flow exists in the corpus regardless of who triggered its creation, and is queryable by any user or agent with corpus access. The corpus is the shared substrate that all journeys read from. Extraction is triggered only by explicit human invocation — no ambient capture, no background extraction, no agent-triggered extraction in the MVP.

### Journey 1: Self-Check (Primary MVP Journey)

**Persona:** Noa, a mid-level product designer at Guesty, 2 years on the team. She works on the Reservations domain and knows her area well, but she's less confident about how her decisions interact with adjacent domains (Payments, Guest Communication) and whether she's applying the team's principles the way a senior would.

**Opening Scene:** Noa has been working on a redesign of the reservation cancellation flow for three days. She's reached the point where she thinks it's ready for review, but she has a nagging feeling she's missed something. Last time she submitted work for review, her lead flagged that she'd ignored a prior decision about how cancellation policies map to the Payments domain. She doesn't want to repeat that. She also knows that when she runs the team's Cursor agent to generate implementation specs, the output is generic — it doesn't reference Guesty's component patterns or naming conventions.

**Rising Action:** Noa opens the Tahini web surface, pastes the Figma file link for her cancellation flow, and clicks "Run." She waits approximately 1–3 minutes (target latency, to be validated during the spike). Tahini ingests her file — the layer structure, the components she used, the auto-layout decisions, the comments she left for herself — and joins it with Guesty's knowledge layer: the Reservations domain definition, the cancellation policy principles, the Payments cross-domain seam documentation, the Arc design system rules.

**Climax:** The structured artifact comes back. Noa scans it in under two minutes. The context resolution section correctly identifies this as a Reservations domain problem with a Payments cross-domain seam. The findings section flags two things: (1) her flow doesn't account for partial refund states, which is covered by a prior decision from Q3 2025 she hadn't seen, and (2) her use of the modal component for the confirmation step conflicts with a principle about wizard patterns for multi-step destructive actions. Both findings cite the specific Guesty principle or decision, with a severity tag. The open questions section asks whether the cancellation flow should surface guest communication status — a cross-domain consideration Noa hadn't thought of.

**Resolution:** Noa addresses the partial refund gap and swaps the modal for a wizard pattern before submitting for review. When her lead reviews the file, there are no surprises. When Noa runs the Cursor agent with the Tahini artifact as context, the generated specs reference the correct Arc components and follow the wizard pattern. Noa's review cycle dropped from two rounds to one. Across Guesty's mid-level designers, this pattern — catching principle violations and cross-domain gaps before review — eliminates an estimated 8–12 unnecessary review cycles per week, returning 4–6 hours of senior designer review time that was previously spent on issues Tahini now catches upstream.

**Note:** During the MVP, this journey operates in *evaluation mode* — Noa is assessing whether the artifact is accurate and useful. In steady-state, the same journey operates in *use mode* — Noa trusts the artifact and acts on it directly. The surface should support both without conflict: side-by-side comparison views for evaluation, efficient single-artifact views for use.

### Journey 2: Pre-Review (Secondary MVP Journey)

**Persona:** Amit, a senior designer and domain lead for Guesty's Financial Products area. He reviews 4–6 design files per week from three designers on his squad. Review is the most time-consuming part of his week — each file takes 30–45 minutes to review thoroughly because he has to mentally reconstruct the context: which domain is this, what principles apply, what prior decisions are relevant, are there cross-domain implications.

**Opening Scene:** Amit has three files in his review queue for the afternoon. He has two hours. The first is a junior designer's first attempt at an invoice generation flow, and Amit knows from experience that junior designers on Financial Products consistently miss the auditability principle and the regulatory display requirements.

**Rising Action:** Before opening the Figma file, Amit opens the Tahini web surface, pastes the file link, and runs extraction. The artifact comes back in 1–3 minutes. Amit reads the artifact first, not the file. The context resolution tells him this is a Financial Products problem involving the Invoice entity with a Guest Communication cross-domain seam. The findings flag exactly what he expected — the auditability principle isn't addressed — plus something he hadn't anticipated: the flow uses a date picker component that doesn't support the locale-specific formatting required by Guesty's internationalization rules.

**Climax:** Amit opens the Figma file with a focused review agenda instead of a cold read. He spends 10 minutes confirming the artifact's findings against the actual design, adds two comments of his own that the artifact missed (a business logic nuance about tax calculation sequencing), and completes the review. Total time: 15 minutes instead of 40.

**Resolution:** Amit reviews all three files in his two-hour window with time to spare. The quality of his feedback is higher because he's not spending cognitive energy reconstructing context — Tahini did that for him. His feedback cites specific principles and prior decisions, which teaches the junior designers what to check next time.

**Variant:** In the *reviewer-initiated* case, the original designer never interacted with Tahini. Amit invoked it himself as an analytical aid. The journey works identically — the distinction is who triggers the extraction, not what happens after. The resulting artifact is scoped to the file (the junior designer's invoice flow), not to Amit as the invoker, and is queryable by anyone with corpus access.

**Note:** During the MVP, Amit is in *evaluation mode* — reading the artifact carefully to determine whether it's worth trusting as a review aid. In steady-state, Amit is in *use mode* — scanning the artifact quickly to focus his review on what matters, trusting it enough to skip the full cold read. The cognitive load is different in each mode. The surface should support both: detailed views with source citations for evaluation, and scannable summary views for efficient use.

### Journey 3: Agent Grounding (Technical Integration Journey)

**Prerequisite:** An artifact for the relevant file or domain must already exist in the corpus, generated by a prior self-check or pre-review invocation. The agent grounding journey depends on the human invocation journeys having happened first. The agent does not trigger extraction. If no relevant artifact exists, the query returns no Tahini context and the agent operates ungrounded — the same as today.

**Persona:** The Guesty UX Copilot — an existing AI agent that Guesty designers use via Cursor to generate implementation specs, review UX copy, and suggest component patterns. The copilot currently has no access to Guesty's team-specific context.

**Opening Scene:** A Guesty designer asks the copilot to generate a component spec for a new notification banner in the Guest Communication domain. Without Tahini, the copilot produces a generic notification component spec — reasonable structure, standard patterns, but no awareness of Guesty's Arc design system, no reference to the existing notification hierarchy principle, no knowledge of the domain-specific rules about guest-facing vs host-facing messaging.

**Rising Action:** With the Tahini integration active, the copilot's workflow includes a step: before generating output, query Tahini's corpus via MCP for context relevant to the current design task. The query includes the domain (Guest Communication), the component type (notification banner), and the design problem (new notification for booking confirmation). Tahini returns the relevant structured artifacts — the Guest Communication domain definition, the notification hierarchy principle, the Arc component guidelines for banners, and a prior decision about tone differentiation between guest-facing and host-facing messages.

**Climax:** The copilot generates a component spec that references the correct Arc banner variant, follows the notification hierarchy (informational, not actionable), uses the correct tone for guest-facing messaging, and cites the specific Guesty principles that informed each choice.

**Resolution:** The designer receives output that sounds like it was written by someone who knows how Guesty works. The spec is reviewable without rewriting. The before/after difference — generic output vs grounded output — is the core evidence for the blind paired comparison evaluation.

**Demo implication:** The demo must sequence the full loop: first, a human invokes extraction on a real Figma file (Journey 1 or 2), producing an artifact in the corpus. Then, the agent queries the corpus and produces grounded output. The two halves are connected by the corpus, and the connection is what makes the loop coherent.

**Integration requirements:** MCP or API endpoint accepting structured queries (domain, component type, design problem). Response format: array of relevant structured artifacts. Latency target: under 5 seconds for query/response (retrieval only, no extraction in the query path). Authentication: MVP-level API key, not user-level auth.

### Journey 4: Founder as Admin (Operational, Temporary)

**Persona:** Yair, the founder. At MVP scale, he is the only person who manages Tahini's backend: the knowledge layer, the benchmark artifacts, the evaluation protocol, and extraction quality monitoring.

**Flow:**
- **Knowledge layer management:** Maintains the ~70 structured files. When a Guesty principle changes or a new domain decision is made, Yair updates the relevant file. No UI — direct file editing.
- **Benchmark authoring:** Hand-writes 3–5 reference artifacts as the quality bar. These are produced from real Guesty Figma files using the founder's own design leadership judgment.
- **Quality monitoring:** Reviews extracted artifacts against benchmarks using a field-by-field rubric. Flags extraction failures and adjusts agent prompts or schema when quality dips.
- **Evaluation protocol:** Prepares the blind paired comparison materials, coordinates with senior Guesty designers as raters, collects and analyzes results.

**Exit criteria for this journey:** This operational role is retired when Tahini matures enough to have automated quality monitoring, a knowledge layer management interface, and evaluation tooling. All of these are post-MVP.

### Journey 5: Design Leader Corpus Query (Deferred, Post-MVP)

**Persona:** The Head of Design at a Tahini customer. They want org-level visibility: patterns across the design team's work, principle adherence trends, cross-domain gap identification, quality drift detection.

**Deferred because:** Requires corpus volume (months of accumulated artifacts), a different surface (dashboard or chat interface, not per-file invocation), and query capabilities beyond single-artifact retrieval. Named here so the architecture supports corpus-level querying from day one, even though no surface is built for it in the MVP.

**Example queries this journey would support:**
- "How often are we citing the auditability principle in Financial Products flows?"
- "Which domains have the most unresolved open questions in their reviews?"
- "Are new designers applying the wizard pattern correctly, or are we seeing repeated modal misuse?"

### Journey Requirements Summary

| Journey | Key Capabilities Required |
|---------|--------------------------|
| **Self-check** | Figma file ingestion, knowledge layer join, artifact generation, thin web surface for invocation and artifact viewing |
| **Pre-review** | Same pipeline as self-check (different user intent, identical requirements) |
| **Agent grounding** | MCP/API endpoint, structured query interface, artifact retrieval by relevance, sub-5s query latency. Depends on prior human invocation |
| **Founder admin** | File-based knowledge layer management, benchmark comparison tooling, evaluation protocol materials |
| **Design leader (deferred)** | Corpus-level querying, aggregation across artifacts, pattern detection — architecture supports, surface deferred |

## Innovation & Novel Patterns

### Detected Innovation Areas

**Meta-agent architecture.** Tahini does not compete with design AI agents — it grounds them. This is a layer-below play: rather than building a better agent, Tahini builds the context substrate that makes all agents better. This is structurally uncommon in the design tooling space, where every product is racing to be the agent that produces output.

**Spatial-substrate context extraction.** Existing context engines operate on text (meeting transcripts, documents, chat logs). Design intent is not text — it is spatial, hierarchical, and multi-modal (Figma layer trees, auto-layout, component variants, canvas-anchored comments). Extracting structured intent from geometry is a novel technical problem with no direct precedent in the context-engine space.

**Structure-over-smarts thesis.** The prevailing industry assumption is that better models produce better output. Tahini's contrarian bet: the bottleneck is context quality, not reasoning quality. A structured artifact grounding a standard model will outperform an ungrounded frontier model. This thesis is directly testable in the MVP's blind paired comparison.

**Schema as encoded expertise.** The artifact schema is not a data format — it is 15 years of design leadership practice encoded into a queryable structure. Treating domain expertise as a *data shape* rather than as prompts or training data is a novel approach to knowledge engineering that is harder to replicate than any prompt library.

### Validation Approach

Each innovation area is validated through the MVP's existing success criteria — no separate innovation validation is needed:
- Meta-agent architecture is validated when the Guesty UX Copilot's grounded output wins the blind comparison
- Spatial-substrate extraction is validated when artifacts from real Figma files are schema-conforming and quality-passing
- Structure-over-smarts is validated when grounded output is preferred over ungrounded, regardless of model
- Schema-as-expertise is validated when senior Guesty designers recognize their team's voice in the artifact structure

### Risk Mitigation

Innovation-specific risks are consolidated in the risk table under Product Scope & Phased Development (see Consolidated Risk Mitigation). Key fallback: if spatial extraction proves too noisy, Tahini falls back to comment-and-metadata extraction only — the schema and grounding loop still work with shallower input.

## Technical Architecture

Tahini is classified as SaaS B2B with an API-first MVP trajectory. Standard SaaS B2B requirements — multi-tenancy, RBAC, subscription tiers — are explicitly deferred to post-MVP. The MVP operates as a single-tenant cloud agent with API exposure and a thin web surface, optimized for one customer (Guesty) and one goal (proving the end-to-end loop).

### Architecture Decisions

**Cloud Agent Runtime.** Tahini runs as a hosted agent on Anthropic's platform. The agent has tool access to: Figma API, knowledge layer (structured files), and artifact storage. The agent's prompts, tool definitions, and extraction logic are the core IP. Infrastructure is minimal and deliberately not differentiated.

**Figma API Integration.** Single Guesty-provisioned personal access token, stored in a secure secret store. No OAuth, no per-user authentication. All Figma API calls use the Guesty token regardless of which designer triggered extraction. The token access is wrapped in a replaceable function to support per-tenant lookup when multi-tenancy is added later. Designers never authenticate to Tahini directly.

**Knowledge Layer Access (Two-Stage).** Stage 1 (spike): all ~70 structured files bundled into the agent's context on every invocation. This validates extraction quality without tool design complexity — the spike has one job, and separating "can the agent extract well" from "are the tools well-designed" is the right discipline. Stage 2 (MVP build): selective tool-based retrieval via structured query tools (`get_domain_definition`, `get_principles_for_domain`, `get_prior_decisions`, etc.). The tool set is informed by what the spike reveals about the agent's actual retrieval needs. Vector DB / RAG is not needed at MVP scale and is explicitly excluded.

**Artifact Storage.** Each artifact is a JSON file with a stable ID (derived from Figma file URL + extraction timestamp), stored in cloud object storage (S3 or equivalent). A SQLite index maps file IDs to metadata: Figma file URL, domain, principles cited, entities referenced, severity levels, extraction timestamp, agent version. Artifacts are immutable and versioned — re-extraction produces a new version, never overwrites. This supports the deferred Design Leader corpus query journey and quality drift detection without additional infrastructure.

**MCP/API Exposure.** Three query endpoints shaped around actual consumer needs, plus a separate ops endpoint:

| # | Endpoint | Purpose | Consumer |
|---|----------|---------|----------|
| 1 | `get_relevant_context(domain, entity_type, design_problem)` | Returns artifacts whose metadata matches the query, ranked by recency within matching results | Downstream agents (Journey 3) |
| 2 | `get_artifact_by_file(figma_file_url)` | Returns the latest artifact for a specific file | Web surface after extraction |
| 3 | `get_artifacts_by_domain(domain)` | Returns artifacts filtered by domain | Debugging, future Design Leader journey |
| 4 | Health / status | Ops endpoint, separate from query interface | Monitoring |

**MVP query tradeoff:** Relevance ranking in endpoint 1 uses metadata filtering only — domain match plus explicitly-referenced entities, with recency as tiebreaker. No embeddings, no semantic search, no scoring model. **Named limitation:** if the copilot works on a cross-domain problem or the relevant artifact is in a domain the copilot didn't explicitly reference, metadata filtering will miss it. This is acceptable at MVP scale and is the first thing to improve when query quality becomes a problem post-MVP.

Single API key for authentication. No pagination needed at MVP scale.

### Thin Web Surface

Two views, no authentication, internal-only at Guesty:

**Extraction view.** One input field (Figma file URL), one button ("Run"). Progress indicator during extraction with stage visibility ("Reading Figma file," "Joining knowledge layer," "Synthesizing artifact") — necessary because extraction time is not yet verified. Renders the structured artifact in scannable format: headings, sections, severity-tagged findings, collapsible open questions. Export as JSON and/or markdown.

> **Note:** The ~90-second extraction time referenced in the user journeys is a target, not a verified measurement. Performance targets and timeout behavior are specified in NFR1-2. Actual extraction latency on real Guesty Figma files is one of the spike's explicit exit measurements.

**Comparison view.** Side-by-side columns: "Without Tahini" (left) and "With Tahini" (right). Same Guesty UX Copilot task, same design problem, two outputs rendered live. No explanation text — the viewer's eyes do the comparison. This is the demo surface for YC and design partner conversations.

### Gating Blocker: Programmatic Access to Downstream Agent

The comparison view requires Tahini's backend to programmatically call the Guesty UX Copilot with and without Tahini context. **This is a gating blocker, not a "verify and adapt" item.** A live comparison is visceral — the viewer sees it happen and trusts they could repeat it. A static screenshot comparison is slides — the viewer sees a claim, not a demonstration. For a demo-dependent product in a demo-dependent phase, the difference is significant.

Programmatic access to the Guesty UX Copilot is confirmed (see Pre-Kickoff Gating Milestones). If access had not been available, the fallback demo strategy would be a fundamentally different narrative ("here's a structured artifact, here's a senior designer confirming it captures their team's voice") — weaker but honest.

### Implementation Considerations

**What is built vs what is configured:**
- **Built:** MCP server, web surface, artifact storage/index, agent tool definitions
- **Configured:** Figma API token, knowledge layer files (already exist), agent prompts
- **Not built:** database, auth system, user management, admin panel, CI/CD pipeline

**Estimated non-agent infrastructure effort:** 3–4 days for storage, MCP server, and web surface combined. The majority of MVP time is spent on the agent itself — prompts, tool design, extraction quality iteration, and schema refinement.

**Architecture constraints for future-proofing (not built, just not precluded):**
- Token access wrapped in a replaceable function (supports per-tenant lookup later)
- Artifact metadata stored consistently in index (supports corpus querying later)
- Immutable versioned artifacts (supports quality drift detection later)
- MCP server endpoint structure (supports additional query types and semantic search later)

## Product Scope & Phased Development

### Product Vision

Tahini starts as a single-customer validation at Guesty — proving that structured, schema-governed context extraction measurably improves AI agent output for design teams. It evolves through signal source expansion and first external customer onboarding into a SaaS B2B platform: the canonical structured-context layer for product design. The trajectory is from proving the loop at one company to becoming the infrastructure layer that every design team's agents query for context.

### MVP Strategy & Philosophy

**MVP type: Validation MVP.** The goal is not to launch a product for adoption. The goal is to prove one loop works at one company — extraction quality is real, artifacts are usable, grounded agent output is visibly preferred. Everything in the MVP serves that single validation. If the loop works, the product exists. If it doesn't, no amount of infrastructure saves it.

**The Guesty advantage shapes the scope.** The knowledge layer (~70 structured files) already exists. This eliminates what would normally be 40-60% of the build for a new customer. The MVP builds only the signal extraction layer on top of it — you're not building the whole product, you're building the half that's missing. This is why a 4-6 week timeline is credible for a solo founder.

**Resource model:** Solo founder, full stack. Domain expertise (schema, knowledge layer, extraction quality) is the founder's direct contribution. Infrastructure (MCP server, web surface, storage, agent glue code) is handled by the founder.

### MVP Scope

**In scope:** Everything that serves the end-to-end validation loop at Guesty.
- Cloud agent on Anthropic platform with Figma API and knowledge layer tool access
- Extraction pipeline: Figma file → knowledge layer join → structured intent artifact
- Integration with the Guesty knowledge layer (~70 structured files, reused as-is)
- Artifact schema with automated validation
- Artifact storage (JSON + SQLite index, immutable, versioned)
- MCP server with three query endpoints (relevance, file, domain)
- Thin web surface: extraction view + comparison view
- Hand-authored benchmark suite (3–5 artifacts) as the quality bar
- Blind paired comparison evaluation protocol and materials
- End-to-end validation on 10–15 real Guesty design tasks

**Out of scope:** Explicitly excluded from MVP, confirmed across prior steps.
- Multi-tenancy, RBAC, subscription tiers, user accounts
- OAuth / per-user Figma authentication
- Multiple signal sources, ambient capture, autonomous actions
- Human contribution interfaces (no authoring UI, no manual tagging, no approval flows)
- Artifact generation of design work itself (Tahini analyzes designs, it doesn't create them)
- Semantic search / embedding-based retrieval
- Design Leader corpus query surface

### Pre-Spike Thesis Validation

Before the spike begins, validate the structure-over-smarts thesis with zero automation:

1. Take one hand-authored benchmark artifact (principle-grounded, structured, Guesty-specific)
2. Feed it to the Guesty UX Copilot as context alongside a real design task
3. Run the same task without the artifact
4. Compare the two outputs

If grounded output is visibly better — cites Guesty principles, references the right components, matches team voice — the thesis is directionally validated and the spike proceeds with confidence. If grounded output is not visibly better, the thesis is wrong at the foundation and the product needs to be reconsidered before any further investment.

This test costs 2-3 hours. It answers the most load-bearing question in the product. A solo founder cannot afford to discover at week 6 that the core thesis is wrong. Discovering it on day 1 is bad but survivable.

### Pre-Kickoff Gating Milestones

| # | Milestone | Status |
|---|-----------|--------|
| 1 | Programmatic access to the Guesty UX Copilot | **Confirmed** |
| 2 | Figma API token with team-level access | **Confirmed** |
| 3 | Anthropic hosted agent platform capabilities verified against architecture needs | Not started |
| 4 | Hand-authored benchmark artifact produced (at least 1, target 3-5) | Not started |

### Core Journeys Supported

- Self-check (primary) — designer invokes extraction, reads artifact, acts on findings
- Pre-review (secondary) — reviewer invokes extraction on another designer's work, uses artifact to focus review
- Agent grounding — the Guesty UX Copilot queries the corpus, produces grounded output
- Founder admin (temporary) — knowledge layer management, quality monitoring

### Spike Plan Summary

**Duration:** 1-2 weeks, before full MVP build.
**Purpose:** Validate the single most load-bearing technical assumption — can the extraction pipeline produce artifacts comparable to hand-authored benchmarks from real Guesty Figma files?

**Spike exit criteria:**
1. 5+ real Guesty Figma files processed end-to-end without manual intervention
2. Artifacts are schema-valid
3. Founder rates artifacts as "comparable" to hand-authored benchmarks on field-by-field rubric
4. Actual extraction latency measured and documented
5. Knowledge layer access pattern validated (Option A bundling sufficient or needs refinement)
6. At least one senior Guesty designer (not the founder) has read 2-3 extracted artifacts and independently rated them as credible — either "this reads like our team's voice" or "this is wrong for Guesty in ways I can name." Not a formal evaluation — 30 minutes of a designer's time. This catches the founder's-blind-spot failure mode. If no senior designer is available, that itself signals insufficient Guesty engagement for a real POC.

**If spike passes:** Full MVP build proceeds with confidence (remaining 3-4 weeks).
**If spike fails:** Gap diagnosed (extraction logic, schema design, or Figma API limitations) and addressed before committing remaining timeline.

### Post-MVP Features

**Phase 2 — Two priorities, infrastructure in support:**

**Priority 1: Second signal source.** Add Slack threads or design review meeting transcripts as an extraction input alongside Figma. This is the biggest validation of the vertical schema hypothesis — if Tahini can extract structured intent from text-based signals as well as spatial ones, the thesis is broadly true and the product has legs. If it can't, the thesis is Figma-specific and the product is smaller than assumed.

**Priority 2: First external customer.** Onboard one design team outside Guesty, with their own knowledge layer bootstrapped from scratch using Tahini's methodology. This validates moat #2 (onboarding methodology). Infrastructure required to support this customer:
- Basic multi-tenancy (workspace isolation)
- Authentication for external access (simple invite/password initially)
- API rate limiting and usage tracking

**Secondary Phase 2 items** (built as needed to support the two priorities):
- Knowledge layer tool-based retrieval (if spike used Option A bundling)
- Additional downstream agent integrations
- Corpus browser for human reviewers

**Phase 3 — SaaS B2B platform:**
- Full multi-tenancy with workspace management, RBAC, and admin controls
- Subscription tiers and self-serve onboarding
- Cross-tool distribution (Figma plugin, Cursor MCP, IDE integrations)
- Cross-domain insight surfacing within a customer's corpus
- Onboarding methodology productized (knowledge layer bootstrapping as guided workflow)
- Semantic search across corpus
- Enterprise features (SSO, SCIM, audit trails)

### Consolidated Risk Mitigation

| Risk | Severity | Mitigation | When diagnosed |
|------|----------|------------|----------------|
| **Extraction quality insufficient** | Critical — product fails | Spike validates against benchmark. If fails, diagnose extraction vs schema | Spike (week 1-2) |
| **Structure-over-smarts thesis wrong** | Critical — no fallback | Pre-spike thesis validation with hand-authored artifact. If grounded output not preferred, product needs rethinking | Pre-spike (day 1) |
| **Spatial extraction too noisy** | Medium — degrades quality | Fall back to comment-and-metadata extraction only (text-based subset); schema and grounding loop still work with shallower input | Spike |
| **Figma API constraints** | Medium — shapes extraction | Rate limits and data access verified during spike | Spike |
| **Anthropic platform dependency** | Medium — strategic risk | Conscious tradeoff accepted. Alternative is building custom infrastructure that does not differentiate Tahini. Platform bet is analogous to Granola's bet on frontier model APIs. If Anthropic changes terms significantly, migration to equivalent platforms (AWS Bedrock agents, self-hosted agent runtime) is possible with manageable rework — the moat is in schema and corpus, not the runtime | Ongoing |
| **Schema too Guesty-specific** | Medium — affects expansion | Onboarding methodology adapts per customer | Phase 2 |
| **Extraction latency exceeds 3-minute target** | Medium — affects surface and demo viability | Actual latency measured as spike exit criterion; timeout behavior defined in NFR2 | Spike |

### Founder Time & Delegation

**Assumption:** The founder can execute the full 4-6 week build alone, handling both domain work and infrastructure work. Feasible but leaves no slack.

**If engineering help becomes available**, the first two items to delegate:
1. **MCP server** — well-specified, standard engineering, no domain expertise required
2. **Web surface** — two views, no auth, clear requirements, buildable from the architecture spec

The founder's time is better spent on schema design, agent prompts, extraction pipeline iteration, benchmark authoring, and Guesty stakeholder relationships — the things where domain expertise compounds.

**Rough weekly shape:**
- Weeks 1-2 (spike): Pre-spike thesis validation on day 1. Agent pipeline + schema iteration. Founder heads-down.
- Weeks 3-4 (build): Extraction refinement, MCP server, web surface, benchmarks authored. Most delegatable phase.
- Weeks 5-6 (validation): Blind paired comparison runs, results documented, demo polished. Founder time shifts from building to evaluating.

## Functional Requirements

### Design Signal Extraction

- **FR1:** Designer can submit a Figma file URL to initiate context extraction
- **FR2:** System can ingest content from a Figma file including layer structure, component usage, auto-layout decisions, and canvas-anchored comments
- **FR3:** System can identify the design domain from ingested Figma content with sufficient confidence to ground the extraction
- **FR4:** When domain identification is ambiguous, system produces an artifact flagged as "domain uncertain" or accepts designer-provided domain context as override
- **FR5:** System can join Figma file signals with the team's structured knowledge layer during extraction
- **FR6:** System can produce a structured intent artifact containing domain identification, applicable principles, findings with severity tags, cross-domain considerations, and open questions
- **FR7:** Each artifact finding cites specific knowledge layer sources — principles, prior decisions, or domain definitions — that informed it

### Knowledge Layer Integration

- **FR8:** System can access the team's structured knowledge files as extraction context
- **FR9:** System can retrieve domain definitions, principles, prior decisions, and design system rules relevant to the identified design problem
- **FR10:** System can identify cross-domain seams and surface considerations from adjacent domains referenced or implied by the design
- **FR11:** Founder can update knowledge layer content; subsequent extractions reflect updated content; existing artifacts remain unchanged and reflect the knowledge layer state at the time of their original extraction; re-extraction on the same file produces a new artifact version reflecting current knowledge layer state. Note: knowledge layer changes do not invalidate existing artifacts; schema changes are signaled via schema_version in the API payload (see NFR11); consumers should handle both cases explicitly

### Artifact Schema & Storage

- **FR12:** System validates each extracted artifact against a defined schema before storage
- **FR13:** System stores artifacts as immutable, versioned records with stable identifiers
- **FR14:** System indexes artifact metadata including source file URL, domain, principles cited, entities referenced, severity levels, and extraction timestamp
- **FR15:** Re-extraction of the same Figma file produces a new artifact version without overwriting previous versions

### Context Delivery

- **FR16:** Downstream agent can query the corpus for relevant artifacts by domain and entity type; the query accepts additional context (design problem description) which is stored but does not affect MVP retrieval — MVP filtering uses metadata matching only
- **FR17:** Consumer can retrieve the latest artifact for a specific Figma file URL
- **FR18:** Consumer can retrieve artifacts filtered by domain
- **FR19:** System ranks query results by relevance using metadata matching and recency
- **FR20:** System authenticates corpus API access via API key
- **FR21:** System exposes a health and status endpoint

### Invocation & Viewing Surface

- **FR22:** Designer can enter a Figma file URL and trigger extraction through a web interface
- **FR23:** Designer can observe extraction progress with stage-based indicators during processing
- **FR24:** Designer can view the completed artifact in a scannable format with headings, severity-tagged findings, and collapsible sections
- **FR25:** Designer can view artifacts in both detailed evaluation mode (full source citations, field-by-field inspection) and efficient scanning mode (summary-first with expandable detail)
- **FR26:** Designer can export an artifact as JSON or markdown
- **FR27:** Viewer can see side-by-side comparison of Guesty UX Copilot output produced with and without Tahini context for the same design task
- **FR28:** Comparison view produces both grounded and ungrounded outputs live by invoking the Guesty UX Copilot programmatically

### Quality Evaluation

- **FR29:** Founder can author hand-written benchmark artifacts as quality reference standards
- **FR30:** Founder can compare extracted artifacts against benchmarks using a field-by-field rubric
- **FR31:** System can produce blind paired comparison materials with randomized output order and stripped identifying markers
- **FR32:** Evaluator can rate paired outputs using forced binary choice with structured reason tagging and a "would you ship this" assessment
- **FR33:** Founder can track artifact quality over time by comparing new extractions against established benchmarks

### Error Handling & Resilience

- **FR34:** System reports specific, actionable error messages when extraction cannot proceed (inaccessible file, invalid URL, API failure, timeout)
- **FR35:** System flags artifacts with "limited knowledge layer coverage" when the identified domain has insufficient knowledge layer context for grounded extraction
- **FR36:** System retries or fails visibly when an extracted artifact fails schema validation, rather than storing invalid artifacts
- **FR37:** System enforces a maximum extraction time and reports timeout clearly to the designer

### Critical-Path Assessment

Not all FRs carry equal weight for thesis validation. If the builder runs out of time in week 5, they need to know what's load-bearing for proving the core thesis vs what's supporting infrastructure.

**Critical path — thesis fails without these:**
- FR1-7 (extraction pipeline — the core product capability)
- FR12-15 (schema and storage — artifacts must be valid and retrievable)
- FR16 (agent grounding query — needed for the blind comparison)
- FR27-28 (comparison view — the demo surface that makes the magic visible)
- FR29-32 (evaluation protocol — the measurement that proves the thesis)

**Supporting — necessary but thesis validates without polish:**
- FR8-10 (knowledge layer access — required for extraction to work, but what's validated is extraction quality, not retrieval sophistication)
- FR11 (knowledge layer updates — operational, not on the validation path)
- FR17-21 (context delivery extras — needed for function but the core thesis validates on FR16 alone)
- FR22-26 (viewing surface — needed for usability but the thesis validates even with a rough surface)
- FR33 (quality tracking over time — post-validation utility)
- FR34-37 (error handling — important for reliability but thesis validates on happy path first)

**Cut-last signal:** If time pressure forces a choice, FR26 (markdown export), FR21 (health endpoint), FR33 (quality tracking over time), and FR25 (dual-mode views) are the first candidates to defer without weakening the validation.

### Functional Requirements Coverage Validation

- All four MVP journeys covered: Self-Check (FR1-7, FR22-26), Pre-Review (same pipeline, different user intent), Agent Grounding (FR16-21), Founder Admin (FR11, FR29-33)
- Evaluation/use mode surface flexibility from Journeys 1 and 2 covered by FR25
- Deferred Design Leader journey has no FRs — architecture supports it via FR14/FR18 but no surface is built
- Every must-have capability from scoping maps to at least one FR
- Every out-of-scope item has no FR
- Error handling and failure modes named as contractual product behaviors (FR34-37)
- FR16 explicitly aligned with architecture document's metadata-only filtering commitment
- FR4 names domain identification fallback behavior, preventing silent failures in the pipeline's first step
- FR11 explicitly commits to option 1 (existing artifacts immutable, new extractions reflect updates), removing ambiguity about knowledge layer change propagation

## Non-Functional Requirements

### Performance

- **NFR1:** Extraction completes within 3 minutes for Guesty Figma files of typical complexity (validated during spike). 3 minutes is the threshold below which the demo remains viable, not an arbitrary number.
- **NFR2:** Extraction times out at 5 minutes with a clear failure message if the file exceeds complexity or processing bounds. Timeout is preferable to indefinite hang. Actual timeout threshold informed by spike measurements.
- **NFR3:** Corpus query responses return within 5 seconds under single-user load. Retrieval only — no extraction in the query path.
- **NFR4:** Web surface renders artifact content within 2 seconds of receiving it from the backend.

### Security

- **NFR5:** Figma API token stored in a secure secret store, never logged, never included in API responses or client-side code.
- **NFR6:** All corpus API queries require a valid API key. Requests without a valid key receive a 401 response with no data leakage.
- **NFR7:** Knowledge layer content and artifact data are not accessible through any unauthenticated endpoint.
- **NFR8:** Knowledge layer files and artifact storage are accessible only through the agent's authorized tool calls. Direct storage access (bucket URLs, file paths) is not exposed to any unauthenticated party, and storage credentials are managed in the same secret store as the Figma token.

### Integration

- **NFR9:** System handles Figma API rate limits gracefully — retries with backoff rather than failing silently or producing incomplete artifacts.
- **NFR10:** If the Figma API is unavailable or returns errors, the system reports the specific failure to the designer rather than proceeding with partial data.
- **NFR11:** API responses include an explicit schema version field in the payload. Consumers can detect schema changes and fail visibly on unrecognized versions. Formal multi-version API support is deferred to post-MVP.

### Data Integrity

- **NFR12:** 100% of stored artifacts pass schema validation. No invalid artifacts persist in the corpus.
- **NFR13:** Artifacts are never overwritten or deleted through normal system operation. Data loss requires explicit manual intervention.
- **NFR14:** The artifact index remains consistent with stored artifacts — every stored artifact has an index entry, every index entry points to an existing artifact.

### Reliability

- **NFR15:** System maintains a demo mode that can replay a previously-successful extraction end-to-end without calling the live Anthropic agent or Figma API. Demo mode exists as a fallback for external demos when upstream dependencies are unavailable.

### NFR Scope Notes

**Categories explicitly skipped:**
- **Scalability** — Single customer, handful of users. No growth scenarios at MVP.
- **Accessibility** — Internal-only surface, small known user group. No regulatory requirement.

**Categories considered and explicitly excluded:**
- **Extraction determinism** — LLM agents are non-deterministic by nature. Consistency is covered by schema validation (FR12) and quality benchmarking (FR29-31). Specifying determinism would force temperature reduction or caching, both of which hurt the product more than they help.
