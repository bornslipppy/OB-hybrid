---
stepsCompleted: [1, 2, 3, 4, 5]
inputDocuments:
  - 'docs/brainstorming/brainstorming-session-2026-02-11.md'
  - 'docs/brainstorming/intake-pitch-deck-refined-2026-02-13.md'
  - 'docs/research/market-pm-tools-competitive-landscape-2026-02-12.md'
date: '2026-02-13'
author: 'Yair Cohen'
lastUpdated: '2026-02-13'
---

# Product Brief: Intake

## Executive Summary

**Intake is Product Reasoning Infrastructure—the context layer between scattered signals and AI execution.**

### The Transformation Is Proven (At OpenAI)

At OpenAI, 95% of engineers now use Codex to manage fleets of AI agents, resulting in 70% more PRs. The key insight: **success requires management skills, not coding skills.** Engineers shifted from writing code to providing context and steering agents across 10-20 parallel threads.

**Head of Engineering, OpenAI:** *"Engineers are becoming tech leads. They're managing fleets of agents... It literally feels like we're wizards casting spells."*

The primary lever isn't better prompts—it's **better context encoding.**

### PMs Are Next (And Already Building DIY Solutions)

840+ enterprise PMs from Microsoft, Meta, Amazon, NVIDIA, and Gong are actively engaged. Technical PMs are building "Product OS" systems in Cursor, shipping products in 2 weeks. Non-technical PMs are mastering "management loops" (Brief → Dialogue → Investigation → Critique → Production) but spending hours per artifact.

**The pattern is proven. The infrastructure doesn't exist.**

### What Intake Builds

Intake automates what successful AI users do manually:

```
Scattered Signals → Context Encoding (BMAD) → AI Reasoning → Machine-Actionable Specs → Multi-Agent Execution
                    ↑                                          ↑
                    Infrastructure                             Infrastructure
```

**Context encoding infrastructure** (BMAD triangulation) combines human judgment with system context:
- Customer SAY (interviews) vs. customer DO (behavior data)
- Technical POSSIBLE (codebase scan) vs. Strategic BELIEVES (PM goals)
- Automatic contradiction detection prevents building unwanted features

**Machine-actionable specs** coordinate multiple AI agents without clarifying questions:
- Measurable goals, testable criteria, explicit constraints
- Auto-enriched with codebase context (services, models, technical feasibility)
- Evidence-linked for compliance and engineering trust
- 90 seconds from signals to executable spec (vs. 4-5 hours manual)

**Architecture built for the future:**
- **Model agnostic:** Works with Claude, GPT-4, Gemini, future models (not locked to single provider)
- **Framework agnostic:** Supports any tech stack (React, Vue, Django, backend frameworks)
- **Multi-agent ready:** V2 enables parallel exploration workflows (10x speed, mirrors OpenAI pattern)

**The result:** PMs become managers of AI reasoning. Engineering trusts specs because they're precise, traceable, and codebase-aware. Product reasoning becomes living infrastructure versioned in git, not stale documents in Confluence.

**Traditional PM tools** (ProductBoard, Aha!) output human-readable dashboards. **Developer tools** (Cursor) require technical expertise. **Intake is purpose-built infrastructure** for the paradigm OpenAI proved: management > coding, context > prompts.

---

## Core Vision

### Problem Statement

**The transformation from "doer" to "manager of AI agents" is proven at OpenAI. PMs are next—but lack the infrastructure.**

### The Pattern That Works (Validated at Scale)

At OpenAI, 95% of engineers use Codex to manage fleets of AI agents, achieving 70% more output. The shift:
- **Old:** Engineers write every line of code
- **New:** Engineers provide context and steer 10-20 parallel AI threads
- **Key insight:** Management skills > Coding skills. Context encoding > Better prompts.

**OpenAI Head of Engineering:** *"Most agent failures stem from underspecification or lack of tribal knowledge. Solving this requires encoding knowledge into files the model can ingest."*

### PMs Face the Same Transformation (But Without Infrastructure)

**840+ enterprise PMs engaged** (Microsoft, Meta, Amazon, NVIDIA, Gong) are navigating this shift:

**1. Technical PMs building DIY "Product OS" systems:**
- Custom `/create`, `/verify`, `/dev` commands in Cursor
- Built working products in 2 weeks (pattern matches OpenAI)
- Writing "Process.md" guides (too complex to scale)
- **Gap:** No PM-specific reasoning framework, no context encoding infrastructure

**2. Non-technical PMs mastering "management loop" manually:**
- RevOps leader: *"We struggle with GenAI because we treat it like a search engine. The key isn't better code—it's better delegation."*
- Management loop: Brief → Dialogue → Investigation → Critique → Production
- Works brilliantly, but takes **4-5 hours per artifact**
- **Gap:** No automation of this proven workflow

**3. Most PMs experimenting but not improving:**
- "Started Claude product skills, hasn't significantly improved workflow"
- Missing: Management framework + context encoding
- **Gap:** No infrastructure bridging product reasoning and AI execution

### Why Existing Solutions Fail

**Traditional PM tools** (ProductBoard, Aha!, ProdPad):
- ❌ Human-readable dashboards, not machine-actionable output
- ❌ No context encoding or evidence chains
- ❌ No codebase awareness
- **Built for human clients, not AI agents**

**Developer tools** (Cursor):
- ❌ Developer UX excludes non-technical PMs
- ❌ No product discovery framework
- ❌ No built-in reasoning structure
- **Built for execution, not product reasoning**

**AI document generators** (ChatGPT, Claude, Notion AI):
- ❌ No context persistence or continuity
- ❌ Generic outputs lacking codebase awareness
- ❌ No data integration or evidence chains
- **One-off generation, not infrastructure**

**The Market Gap:** No tool provides the infrastructure layer for **context encoding + management automation + machine-actionable output** that successful AI users prove works.

### Problem Impact

**For Non-Technical PMs:**
- Excluded from the AI revolution (Cursor too technical, traditional tools not machine-actionable)
- Weeks spent manually synthesizing scattered signals with no structured framework
- Engineering doesn't trust vague specs, causing friction and rework: *"Where did this requirement come from?"*
- Burnout from heavy pressure, tighter timelines, fear of failure

**For Engineering Teams:**
- Waiting for PM specs while AI agents could be executing
- Endless "show me the data" debates because decisions lack traceability
- 10+ clarifying questions per feature before coding can start
- Rework from ambiguous requirements, missing edge cases, unclear constraints

**For Startups & Product Teams:**
- Product discovery cycles can't keep pace with AI-powered development speed
- Building features customers claim to want but won't use (say-vs-do disconnect)
- 4-5 days from idea to coding start; competitors ship while you're still writing PRDs
- Competitive disadvantage as faster teams iterate while you're stuck in spec review

### Why Existing Solutions Fall Short

**Traditional PM Tools (ProductBoard, Aha!, ProdPad):**
- Built for human consumption: roadmaps, feedback boards, static PDF documents
- No machine-actionable output—Cursor/Claude Code can't parse their PRDs without reformatting
- Manual evidence linking (time-consuming, incomplete, often skipped)
- No codebase awareness—can't tell PMs what's technically possible
- Expensive per-user pricing ($25-90/user/month) limits collaboration
- **Core Issue:** Built for the old paradigm (human client), not machine clients

**DIY Approach (PM + Cursor Directly):**
- Developer UX excludes non-technical PMs (IDE interface, git workflows, command-line concepts)
- No product discovery framework (execution-focused, not discovery-focused)
- No built-in reasoning structure—PMs start from blank canvas
- No codebase context synthesis—PMs must manually understand what exists
- Steep learning curve: repo management, branch strategies, merge conflicts
- **Core Issue:** Right output format, wrong interface for PMs

**AI Document Generators (ChatGPT, Claude, Notion AI):**
- No continuity or context persistence across sessions
- Generic outputs lacking codebase awareness (doesn't know your AuthService exists)
- No data integration—requires manual copy-paste from Modjo, Jira, Datadog
- One-off documents, not living source of truth
- No traceability to evidence (customer quotes, usage metrics, business goals)
- **Core Issue:** Tools for one-time generation, not infrastructure for ongoing product work

**The Market Gap:** No tool bridges product discovery (figuring out what to build) with machine-actionable specifications for AI-native development.

### Proposed Solution

**Intake = AI-Native Product Management Infrastructure for Discovery**

Intake closes the product discovery loop with a machines-first approach, answering the fundamental PM question: **"What should we build next?"**

**The Complete Flow:**
1. **PM uploads scattered signals** (customer interview transcripts, Jira tickets, Datadog/Looker analytics, GitHub repo access)
2. **Intake discovers problems** (open-ended discovery: analyzes patterns, surfaces contradictions, identifies high-impact opportunities)
3. **Intake generates machine-actionable specs** (90 seconds → structured YAML + markdown Cursor can parse)
4. **Developer + Cursor execute** (agent proposes implementation with full context, developer reviews)
5. **Feature ships** (10x faster than manual process)

**What Intake Generates: Machine-Actionable "WHAT" (Not "HOW")**

Intake outputs structured direction on **what** needs to be fixed, built, or updated—not implementation details:

```yaml
goal: Reduce onboarding drop-off by 20%

success_criteria:
  - Time to first action < 60s
  - No errors in signup flow
  - Mobile parity with desktop

constraints:
  - Use existing auth service
  - No changes to data model

context: auto-enriched ✓
```

**Auto-Enriched Context = The Differentiator:**
- **Codebase scan:** "Found AuthService at `/src/auth/`, no need to rebuild"
- **Pattern recognition:** "Data model changes are expensive in your architecture, avoiding them"
- **Technical feasibility:** "Mobile rendering already exists in component library"

**What Intake Does NOT Generate:**
- Not: UI designs or code implementations
- Not: Technical architecture decisions (developer + AI agent decide **HOW**)
- Not: Fully automated—PM reviews outputs before shipping to engineering

**Why "Machine-Actionable" vs "Machine-Executable":**

Traditional PRDs are human-readable prose. Intake specs are **machine-actionable**:
- **Structured:** YAML + markdown format Cursor/Claude Code parse directly
- **Specific:** Measurable goals, testable success criteria, explicit constraints
- **Contextual:** WHY decisions made (traced to customer evidence + usage data)
- **Codebase-aware:** References actual files, services, components via auto-enrichment
- **Git-versioned:** Single source of truth from discovery through execution

Cursor doesn't need a human to "translate" the spec—it reads the structure and acts. Developer reviews and approves the proposed implementation.

**Git-Versioned Living Artifacts:**

Specs aren't static documents that go stale:
- PM creates spec → commits to git branch
- Developer implements → references spec commit SHA in PR
- Spec evolves → new commits → clear audit trail
- Traceability: "Why did we build this?" → Git history shows reasoning + evidence

New data creates conflicts? Intake flags for PM review (not auto-update in MVP).

### Key Differentiators

**1. Context Encoding Infrastructure (The Core Moat)**

**OpenAI validation:** *"Most agent failures stem from lack of tribal knowledge. Solving this requires encoding knowledge into files the model can ingest."*

**BMAD triangulation = Structured context encoding:**
```yaml
Automatically encodes 4 signals:
  customer_say: Interview transcripts (qualitative evidence)
  customer_do: Behavioral data (quantitative validation)
  technical_possible: Codebase scan (constraints + feasibility)
  strategic_believes: PM goals (business direction)
```

**Unique capability:**
- **Say-vs-do contradiction detection:** Prevents building features customers claim to want but won't use
- **Example:** Customers SAY "advanced filtering" but DO use only 2 filters → Don't over-build

**Why hard to replicate:**
- Requires encoding PM expertise (not generic AI)
- Integration layer (Modjo, Datadog, GitHub) takes months to build
- Network effects: More data → Better pattern recognition

**2. Automated Management Loop (Infrastructure, Not DIY Mastery)**

**What successful AI users do manually:**
1. **Brief** → Write context (30 mins)
2. **Dialogue** → Ask clarifying questions (45 mins)
3. **Investigation** → Fetch data from sources (1-2 hours)
4. **Critique** → Red pen output, iterate (1 hour)
5. **Production** → Finalize artifact (30 mins)
- **Total: 4-5 hours per artifact**

**What Intake automates:**
1. **Brief** → Pre-loaded from BMAD triangulation (automatic)
2. **Dialogue** → AI surfaces contradictions (say vs. do) automatically
3. **Investigation** → Evidence chains pre-loaded from integrations
4. **Critique** → Built-in validation checks (completeness, testability)
5. **Production** → 90 seconds
- **Total: 90 seconds**

**RevOps Leader validation:** *"The key isn't better code—it's better delegation."* Management skills unlock AI leverage. Intake automates the management workflow.

**3. Machine-Actionable Specs for Multi-Agent Coordination**

**Augment Intent pattern:** Living specs coordinate multiple AI agents working in parallel.

**Compare the handoff:**

| Traditional JIRA Ticket | Intake Machine-Actionable Spec |
|-------------------------|--------------------------------|
| "Improve onboarding flow" (ambiguous) | `goal: Reduce onboarding drop-off by 20%` (measurable) |
| "Make it better. Users are dropping off." | `success_criteria: Time to first action < 60s` (testable) |
| Assignee: @agent | `constraints: Use existing auth service` (explicit) |
| **Dev questions: 10+** | `context: auto-enriched ✓` (codebase-aware) |
| **Time to start coding: 2-3 PM meetings** | **Dev questions: 0-1, Time to coding: Immediate** |

**Augment manifesto:** *"The spec becomes the coordination layer. Agents don't share intuition—they act on what's made explicit."*

**4. Auto-Enriched Codebase Context (Technical Feasibility)**

No other PM tool tells you what's technically possible in YOUR codebase:

**Traditional PM Tools:**
- "Use authentication" → Engineering asks: "Which auth system? Build new or use existing?"

**Intake:**
- `constraints: Use existing auth service` → Auto-discovered via codebase scan
- `context: AuthService found at /src/auth/, supports OAuth + SAML`

**Pattern Recognition:**
- "Data model changes are expensive in your microservices architecture" → Suggests no-schema-change solutions
- "Mobile components already exist in design system" → Points to reusable patterns

**Technical Approach (MVP-Tractable):**
- **Parsing-first:** Static analysis finds services, models, APIs (ship in months)
- **Semantic understanding later:** ML-powered "what's possible" analysis (future versions)

**5. Architecture Built for 12-24 Months Out**

**OpenAI strategic warning:** *"Build for where models are going, not where they are today. Models will eat your scaffolding for breakfast."*

**What survives (Structure):**
- ✅ **Model agnostic:** Works with Claude, GPT-4, Gemini, future models (not locked to single provider)
- ✅ **Framework agnostic:** Supports any tech stack (React, Vue, Django, Rails, etc.)
- ✅ **Multi-agent ready:** V2 enables parallel exploration workflows (10x speed, mirrors OpenAI pattern)
- ✅ **Context encoding:** BMAD triangulation (durable reasoning structure)
- ✅ **Evidence chains:** Traceability survives model improvements

**What dies (Scaffolding):**
- ❌ Complex RAG pipelines
- ❌ Over-engineered vector stores
- ❌ Workarounds for model limitations

**Competitive advantage:** Competitors locked to single AI providers face strategic risk. Intake benefits from provider competition.

**6. Discovery Engine for "What to Build Next"**

Unlike validation tools that test hypotheses, Intake is an **open-ended discovery engine**:

**The PM doesn't start with answers.** They start with:
- 10 customer interview transcripts
- 3 months of behavioral data
- 200 Jira tickets
- A vague sense that "onboarding needs work"

**Intake discovers:**
- **Patterns:** "23% of mobile users abandon at email verification (vs 8% desktop)"
- **Contradictions:** "Customers say they want analytics dashboard, but usage shows 80% never open it"
- **High-impact opportunities:** "Reducing time-to-first-action by 30s could save 15% drop-off based on funnel analysis"

**Outputs prioritized, evidence-linked specs.** PM reviews and approves before shipping to engineering.

**7. PM-Native UX for Non-Technical Users**

Bridges the gap Cursor left open:

- **Visual, Discovery-Oriented Interface:** Not a developer IDE
- **No Technical Expertise Required:** Non-technical PMs get machine-actionable power
- **Built-In Discovery Workflows:** Structured frameworks guide signal synthesis
- **Minutes to Execution:** From "What should we build?" to Cursor executing in 5 minutes

**Timeline Collapse:**

**Traditional Approach:**
- PM: 2-3 days writing PRD manually
- Engineering: 2 days clarifying ambiguous requirements
- Total: **4-5 days before coding starts**

**Intake Approach:**
- Intake: 90 seconds generating machine-actionable spec
- PM: 30 minutes reviewing + refining output
- Cursor: Executes immediately with developer oversight
- Total: **Same day from idea to working code**

Even with human-in-the-loop review, you've collapsed the timeline by **10x**.

---

## Target Users

### Primary Users

**Ideal Customer Profile:**

Intake is built for **non-technical Product Managers at B2B SaaS companies** navigating complex product domains while their engineering teams accelerate with AI agents.

**Company Profile:**
- B2B SaaS companies (fintech, healthcare, enterprise tools)
- Seed to Series B stage (10-100 employees)
- Using or planning to adopt AI-native development (Cursor, Claude Code)
- High feature velocity requirements
- Complex domain requirements (compliance, multi-tenant, data integrity)

**Geographic Focus:**
- Primary: US market (SF Bay Area, NYC, Austin, Seattle)
- Secondary: EU market (London, Berlin, Amsterdam)

---

**Primary Persona: Sarah Chen**

**Role:** Product Manager at FinFlow, a Series A fintech SaaS company (60 employees)  
**Product:** Multi-tenant accounting reconciliation platform for mid-market finance teams  
**Background:** 4 years PM experience, came from UX design background (non-technical)

**Sarah's Reality:**

Sarah has **3 hours of daily hands-on time** (rest is meetings) to answer the question that defines her job: **"What should we build next?"**

This question comes constantly:
- **Small decisions:** "Fix bank reconciliation bug or improve audit trail export?" (5x daily)
- **Big decisions:** "Q2 priority: multi-currency support or automated journal entries?" (weekly)

**The Complexity She Faces:**

Working on accounting software adds layers most PMs don't experience:

- **Domain complexity:** GAAP compliance, SOC 2 requirements, multi-tenant data isolation
- **Technical constraints:** Can't break reconciliation logic; schema changes require migrating 200+ customer databases
- **Regulatory traceability:** Every decision needs audit trail—"Why did we build this?" must be answerable

**Her Current Pain:**

Sarah is drowning in scattered signals:
- 15 CFO interviews in Modjo: "We need faster reconciliation"
- 87 Jira tickets: Half are duplicates phrased differently
- Datadog: 23% users abandon at "bank connection" step
- GitHub codebase: `ReconciliationService`, `BankIntegrationService`, `AuditTrailService`—but she doesn't know what's safe to change

**Synthesizing this manually takes her entire 3-hour block for ONE spec:**
1. Read interviews (1 hour) → Identify pattern
2. Cross-reference Jira (45 min) → Which pain matters most?
3. Engineering sync (30 min) → "Can we change the data model?" → "No, 3-month migration"
4. Write PRD (45 min) → Ship Friday

Monday: Engineering returns with 10 clarifying questions:
- "Which bank integration should we use?"
- "Can we modify transaction table?"
- "What if reconciliation is in progress?"

Result: **Full week from idea to code start.**

Meanwhile, engineering ships features in *hours* with Cursor... when they have clear specs.

**How Intake Transforms Sarah's Work:**

**Monday 1:00 PM:** Upload to Intake:
- 15 customer interviews
- 87 Jira tickets
- 3 months Datadog data
- GitHub repo access

**Monday 1:05 PM:** Intake generates auto-enriched spec:

```yaml
goal: Reduce bank reconciliation abandonment by 20%

success_criteria:
  - Connection success rate > 95%
  - Time to first reconciliation < 2 min
  - Zero data consistency errors

constraints:
  - Use existing BankIntegrationService (/src/services/bank/)
  - No transaction table schema changes (migration cost)
  - Maintain SOC 2 audit trail

context: auto-enriched ✓
  - BankIntegrationService supports Plaid, Yodlee, MX
  - MX has 3% failure rate vs Plaid 8%
  - Multi-tenant isolation at database level

evidence:
  - "Bank connection fails 30%" (CFO interview, Acme)
  - 23% abandon at connection (Datadog)
```

**Monday 1:30 PM:** Sarah reviews—Intake already found:
- Existing BankIntegrationService (no engineering sync needed)
- Data model constraint (saved 3-month migration discussion)
- Best integration option (MX lower failure rate)
- Compliance maintained (SOC 2)

**Monday 2:00 PM:** Commits spec to git. Engineering starts with Cursor.

**Tuesday:** Feature ships. Developer: *"Zero clarifying questions—spec knew everything. 🚀"*

**Sarah's "I Can't Go Back" Moment:**

That spec took **90 seconds to generate**. It used to take **3 hours plus engineering sync** to understand what's technically possible.

The developer asked *zero questions*—because Intake auto-enriched the spec with codebase context she'd never find herself.

She opens Intake for spec #2. She knows what she has: **A tool that understands her accounting platform better than she does.**

**Sarah's Success Metrics:**

- **Speed:** 3 hours + sync → 5 minutes (generate + review)
- **Quality:** 10 clarifying questions → 0-1
- **Domain confidence:** "I don't know what's possible" → "Intake tells me what exists"
- **Velocity:** 2 specs/week → 10+ specs/week
- **Compliance:** Every decision traced to evidence (audit-ready)

---

**Additional Primary User Characteristics:**

**Pain Points They Experience:**
1. Time wasted manually synthesizing scattered signals
2. Engineering doesn't trust specs (lack of evidence + codebase awareness)
3. Can't keep pace with AI-augmented engineering velocity
4. Traditional PM tools too expensive or don't output machine-actionable specs
5. Cursor too technical (developer IDE, git workflows, command-line)

**What Makes Them Choose Intake:**
- Hear about it from PM friends/coworkers in similar roles
- See the spec.yaml vs JIRA comparison on website
- Realize they need "Cursor for PMs"—machine-actionable output without developer skills
- Trial the product after seeing auto-enriched codebase context demo

---

### Secondary Users

**At MVP Launch:** No secondary user segments targeted.

**Future Consideration:**
- Technical Product Managers (looking to move faster with existing Cursor skills)
- Solo technical founders (wearing PM hat, need structured discovery)
- Product Ops teams at scaling companies (50-500 employees)
- Engineering leads (who review and approve specs)

**Rationale for MVP Focus:**
The non-technical PM segment represents the largest underserved market and highest pain point. Solving for this ICP first establishes product-market fit before expanding to adjacent user types.

---

### User Journey

**Sarah's Path from Discovery to Daily User**

**Week 1: Discovery**
- **How she hears about Intake:** PM friend at another fintech mentions it: "It auto-enriches specs with your codebase—you need to see this"
- **First website visit:** Sees spec.yaml vs JIRA comparison—"Wait, it knows what services exist in my code?"
- **Decision to try:** Signs up for trial (no credit card required)

**Week 1, Day 2: First Use**
- Uploads customer interviews, Jira tickets, Datadog data
- Connects GitHub repo (read-only access)
- Intake generates first spec in 90 seconds
- **Skepticism:** "Let me verify it actually found BankIntegrationService..."
- Opens GitHub → `/src/services/bank/BankIntegrationService.ts` *exists*
- **Mind blown**

**Week 2: Aha Moment**
- Developer reviews first Intake-generated spec: "This is gold—zero clarifying questions"
- Sarah generates 3 more specs in 15 minutes (used to take 9 hours)
- Engineering ships 2 features that week (used to be 1 feature every 2 weeks)
- **Realization:** "I can't go back to manual PRDs"

**Week 3+: Daily User**
- Sarah uses Intake in every discovery session
- Commits 2-3 specs per day to git
- Engineering velocity doubles
- Her precious 3-hour block now covers 6-8 discovery questions instead of 1
- Becomes internal champion: "Every PM on our team needs Intake"

**Key Moments in Journey:**

1. **Discovery Hook:** Friend recommendation + codebase-aware positioning
2. **First Impression:** Website's spec.yaml vs JIRA comparison
3. **Trial Conversion:** Seeing auto-enriched context in action (90 seconds)
4. **Aha Moment:** Developer says "zero clarifying questions"
5. **Daily Habit:** Engineering velocity proves the value
6. **Expansion:** Recommends to PM network

**Adoption Triggers:**
- ✅ Friend/coworker validation (word-of-mouth)
- ✅ Clear visual proof (spec comparison)
- ✅ Fast time-to-value (90 seconds to first spec)
- ✅ Engineering validation ("This is way better than before")
- ✅ Velocity improvement (measurable impact)

**Retention Drivers:**
- Can't return to 3-hour manual synthesis
- Engineering trust in specs increases team velocity
- Audit trail for compliance (fintech requirement)
- Git-versioned specs become source of truth
- "What to build next" answered in minutes, not days

---

## Success Metrics

Success for Intake is measured across three dimensions: **user value creation** (does it solve Sarah's problem?), **business viability** (can we build a sustainable company?), and **market impact** (are we defining a new category?).

### User Success Metrics

**Primary Success Indicator: The "I Can't Go Back" Moment**

When users say "I can't go back to writing PRDs manually"—we've succeeded. This happens when:

**Time Collapse (Leading Indicator):**
- **Spec generation time:** < 2 minutes per spec (baseline: 3+ hours)
- **Time to developer execution:** Same day from idea to code (baseline: 4-5 days)
- **Weekly capacity increase:** 5-10x more discovery questions answered (2 specs/week → 10+ specs/week)

**Quality & Trust (Core Value Metric):**
- **Zero clarifying questions:** 80%+ of specs shippable without developer questions (baseline: 10+ questions per spec)
- **Engineering approval rate:** 90%+ of specs accepted without rework
- **Codebase context accuracy:** 95%+ of auto-enriched constraints are technically correct

**Adoption & Retention (Behavioral Indicators):**
- **Time to first spec:** < 5 minutes from signup
- **Time to "aha moment":** Within first 3 specs generated (< 10 minutes total)
- **Daily active usage:** 3+ times per week (discovery happens daily)
- **Retention:** 90%+ monthly active users still active after 90 days

**User Impact Validation (The Proof):**
- 4 out of 5 specs shippable without clarifying questions (Amelia's test)
- Engineering velocity doubles within 2 weeks of adoption
- PMs recover 10+ hours per week from manual synthesis work

---

### Business Objectives

**Phase 1: MVP Validation (Months 1-6)**

**Objective:** Prove product-market fit with early adopters

**Success Criteria:**
- **50-500 paying customers** (validated early adopters, target: 500)
- **$39-99/PM/month pricing** validated (mid-market positioning between ProdPad and ProductBoard)
- **Word-of-mouth growth:** 40%+ of new users from PM friend referrals
- **YC validation:** Featured in YC portfolio as "Cursor for PMs" solution
- **Category positioning:** "Product Reasoning Infrastructure" language adopted by 10+ VCs/analysts

**Revenue Target:**
- 500 customers × $69/month average × 2 PMs per company = **$830K ARR**

**Phase 2: Scale & Category Leadership (Months 7-18)**

**Objective:** Establish category leadership and expand to enterprise

**Success Criteria:**
- **5,000+ customers** (category leader positioning)
- **5-10x customer growth** from MVP phase
- **Enterprise readiness:** Multiplayer features, SSO, compliance certifications
- **Partner ecosystem:** Official integrations with Cursor, Anthropic, major data sources
- **Market recognition:** Top 3 PM tool in AI-native category (G2, Product Hunt rankings)

**Revenue Target:**
- 5,000 customers × $69/month × 3 PMs average = **$12.4M ARR**

**Phase 3: Platform Vision (Months 19+)**

**Objective:** Become the operating system for product development

**Success Criteria:**
- **Multiplayer product work:** GitHub-style collaboration for PMs
- **API ecosystem:** 50+ third-party integrations and agent orchestration
- **Network effects:** Data insights improve with scale (anonymized patterns)
- **Category ownership:** "Product reasoning infrastructure" is Intake's category

---

### Key Performance Indicators

**Acquisition (Growth Engine)**

**Primary KPIs:**
- **Trial signups:** 500/month by Month 6 (target: 3,000/month by Month 12)
- **Trial → Paid conversion:** 20%+ (best-in-class SaaS benchmark)
- **Viral coefficient:** 1.5+ (each user brings 1.5 new users via referrals)
- **CAC Payback:** < 6 months

**Leading Indicators:**
- Website visitors who see spec.yaml vs JIRA comparison: 60%+ convert to trial
- Friend/coworker referral rate: 40%+ of signups from word-of-mouth
- PM community mentions: 50+ organic mentions per month (Lenny's Newsletter, Product Hunt, Twitter)

---

**Engagement (Product Value)**

**Primary KPIs:**
- **Weekly Active Users (WAU):** 70%+ of total users (discovery is daily work)
- **Specs generated per user:** 8-12 per week (2x baseline of 2-4 PRDs)
- **Specs committed to git:** 90%+ (proving they're used)
- **Features shipped from specs:** 80%+ (proving engineering trusts them)

**Leading Indicators:**
- Time from signup to first spec: < 5 minutes (95%+ of users)
- "Aha moment" trigger rate: 85%+ users generate 3+ specs in first session
- Multi-spec sessions: 60%+ of sessions generate 2+ specs (batch discovery work)

---

**Quality & Trust (Engineering Validation)**

**Primary KPIs:**
- **Developer clarifying questions:** < 1 per spec (target: 0.5 average)
- **Spec rework rate:** < 10% (specs requiring PM revision after review)
- **Codebase context errors:** < 5% (auto-enriched constraints are wrong)
- **Engineering NPS:** 50+ (developers love receiving Intake specs)

**Leading Indicators:**
- First-spec approval rate: 70%+ (even first-time users generate good specs)
- Auto-enrichment success: 95%+ of codebases successfully scanned
- Constraint accuracy: 98%+ of "use existing service" recommendations are valid

---

**Retention (Long-Term Value)**

**Primary KPIs:**
- **Monthly retention:** 95%+ (can't go back to manual PRDs)
- **90-day retention:** 90%+ (sticky product, daily habit)
- **Churn rate:** < 2% monthly (industry-leading for SaaS)
- **Expansion:** 30%+ of customers add more PM seats within 6 months

**Leading Indicators:**
- Daily active usage: 60%+ of users active 3+ times per week
- Spec velocity increase: Users generate 2x more specs in Month 3 vs Month 1
- Internal advocacy: 50%+ of customers recommend to other teams

---

**Financial (Business Health)**

**Primary KPIs:**
- **Monthly Recurring Revenue (MRR) Growth:** 20%+ month-over-month (MVP phase)
- **Annual Recurring Revenue (ARR):** $830K (Year 1), $12.4M (Year 3)
- **Customer Acquisition Cost (CAC):** < $500 (target: $300 via word-of-mouth)
- **Lifetime Value (LTV):** > $5,000 per customer (target: $8,000)
- **LTV:CAC Ratio:** > 3:1 (healthy SaaS unit economics)
- **Gross Margin:** > 80% (software-first business model)

**Leading Indicators:**
- Average Revenue Per Account (ARPA): $138/month (2 PMs per company @ $69 each)
- Net Revenue Retention: 110%+ (expansion from adding PM seats)
- Sales efficiency: < 3 months to closed deal (product-led growth)

---

**Market Impact (Category Leadership)**

**Primary KPIs:**
- **Category awareness:** "Product reasoning infrastructure" term used by 50+ companies/analysts
- **Market share:** Top 3 in AI-native PM tools by user count
- **Partnership validation:** Official partnerships with Cursor, Anthropic, or Jira/Modjo/Datadog
- **Thought leadership:** Featured in 20+ PM podcasts, conferences, major publications
- **Distribution moat:** 40%+ of signups from word-of-mouth (organic growth engine)

**Leading Indicators:**
- G2 reviews: 4.5+ rating with 50+ reviews by Month 12
- Product Hunt launch: Top 5 product of the week
- YC showcase: Featured as portfolio success story
- Competitive mentions: "Intake vs ProductBoard" searches growing 30%+ monthly
- Content-led growth: 50+ organic mentions per month (Lenny's Newsletter, Product Hunt, Twitter)
- 840+ PM engagement converted: 80-420 customers from initial engagement pool

**Distribution Moat (Strategic Advantage):**

**OpenAI insight:** *"As software becomes easier to create, distribution and audience become the primary differentiator."*

**Our distribution asset: 840+ enterprise PM comments**
- Not random users—PMs from Microsoft, Meta, Amazon, NVIDIA, Gong, CrowdStrike
- High buyer intent: Companies with budgets, proven willingness to pay
- Content marketing validated: 840 comments prove organic reach works
- ICP quality: B2B SaaS, cybersecurity, enterprise (our exact targets)

**Why this is a moat:**
- Competitors don't have this audience (ProductBoard/Aha have existing customers, not engaged early adopters)
- First-mover window closing: Public engagement alerts competitors (6-9 months to act)
- Network effects compound: Early users become advocates, refer peers
- Category definition: We're setting the language ("product reasoning infrastructure")

**Metrics:**
- 40%+ signups from referrals (word-of-mouth growth engine)
- Conversion from 840 pool: 1% = 80-420 customers from ONE post
- Content engagement: 50+ organic mentions per month
- Viral coefficient: 1.5+ (each user brings 1.5 new users)

---

### Success Metric Hierarchy

**North Star Metric:** 
**Specs shipped per week per user** (measures user value + product quality + engineering trust)

**Why this metric:**
- Combines time savings (more specs generated)
- Quality (specs actually ship, not rejected)
- Trust (engineering executes on them)
- Business growth (more specs = more value = retention)

**Supporting Metrics (in priority order):**

1. **Developer clarifying questions per spec** (< 1) → Proves machine-actionable quality
2. **Weekly active usage** (70%+) → Proves daily habit formation
3. **90-day retention** (90%+) → Proves "can't go back" stickiness
4. **CAC payback** (< 6 months) → Proves business viability
5. **Viral coefficient** (1.5+) → Proves word-of-mouth growth engine

---

### Metric Tracking & Validation

**MVP Launch (First 100 Users):**

Focus on **user success validation**:
- Are 80%+ of specs shippable without clarifying questions?
- Do users generate 8-12 specs per week?
- Is 90-day retention above 90%?

**If yes:** Product-market fit validated, scale go-to-market  
**If no:** Iterate on core value (auto-enrichment, spec quality, PM UX)

**Scale Phase (100-5,000 Users):**

Focus on **growth efficiency**:
- Is CAC under $500 with LTV > $5,000?
- Is word-of-mouth driving 40%+ of signups?
- Is enterprise expansion (multiplayer, SSO) opening larger deals?

**Platform Phase (5,000+ Users):**

Focus on **category ownership**:
- Are we defining the "product reasoning infrastructure" category?
- Are partners integrating with Intake APIs?
- Do anonymized insights improve spec quality across customers?

---

## MVP Scope

### Core Features

The Intake MVP focuses on proving the core hypothesis: **Can we convert scattered product signals into machine-actionable specs that eliminate developer clarifying questions and collapse PM-to-code timelines from days to minutes?**

**MVP Feature Set (Tier 1 - Must Have):**

#### **1. Data Ingestion (Manual Upload for MVP)**

**What:** Simple upload interface for scattered product signals

**Capabilities:**
- Upload customer interview transcripts (text files, Modjo CSV exports)
- Upload Jira ticket exports (CSV or JSON format)
- Upload behavioral data (Datadog/Looker CSV exports)
- Connect GitHub repository (read-only OAuth access)
- Write strategic brief in-app (simple text form with structured prompts)

**Why Manual for MVP:** Proves value without complex integration engineering. Users tolerate manual upload if output delivers 10x value.

---

#### **2. Discovery Engine (The Magic)**

**What:** AI-powered open-ended discovery that answers "What should we build next?"

**Capabilities:**
- **Pattern Detection:** Analyze interview transcripts via NLP to identify repeated themes, pain points, feature requests
- **Say-vs-Do Contradiction Flagging:** Surface mismatches between customer statements and usage behavior (e.g., "we need analytics" but 80% never use existing analytics)
- **High-Impact Opportunity Identification:** Prioritize problems based on evidence strength (frequency + severity + business impact)
- **Problem Synthesis:** Group scattered signals into coherent, actionable problems with supporting evidence

**Output:** Prioritized list of 3-5 problems with evidence links, ready for spec generation.

**Why This Is The Moat:** No other PM tool does open-ended discovery with automatic triangulation across qualitative + quantitative + technical + strategic signals.

---

#### **3. Codebase Context Auto-Enrichment (Parsing-First Approach)**

**What:** Automatic discovery of technical constraints and possibilities from user's codebase

**Capabilities:**
- **Service Discovery:** Parse GitHub repo to identify services (e.g., `AuthService`, `BankIntegrationService`, `ReconciliationService`)
- **Data Model Identification:** Detect database schemas, tables, models, migration patterns
- **Constraint Assessment:** Flag technical constraints (e.g., "Data model changes require 3-month migration across 200+ customer DBs")
- **Technical Feasibility Signals:** Identify what exists vs. what needs building (basic: "service found at /src/services/auth/" vs. "no existing service")

**Technical Approach (MVP-Tractable):**
- Static code analysis via AST parsing (TypeScript, JavaScript, Python, Java)
- File structure pattern recognition (common frameworks: NestJS, Express, Django, Spring)
- Simple heuristics for constraint detection (large table = expensive migration)

**Not in MVP:** Semantic understanding ("what's technically possible?") via ML - that's v2+

**Why This Is The Differentiator:** Traditional PM tools can't tell you what exists in YOUR codebase. This is why engineering stops asking clarifying questions.

---

#### **4. Machine-Actionable Spec Generation**

**What:** Structured YAML + markdown specs Cursor/Claude Code can parse and act on

**Output Format:**
```yaml
goal: [Measurable business outcome]

success_criteria:
  - [Testable criterion 1]
  - [Testable criterion 2]
  - [Testable criterion 3]

constraints:
  - [Explicit constraint from codebase scan]
  - [Explicit constraint from data model analysis]
  - [Explicit constraint from domain/compliance]

context: auto-enriched ✓
  - [Service found: path, capabilities]
  - [Technical feasibility note]
  - [Pattern recognition insight]

evidence:
  - [Customer quote with source]
  - [Usage metric with data source]
  - [Business goal with strategic brief link]
```

**Required Elements:**
- **Measurable Goal:** Quantifiable business outcome (not vague "improve onboarding")
- **Testable Success Criteria:** Developer can write assertions (`expect(timeToFirstAction).toBeLessThan(60000)`)
- **Explicit Constraints:** Clear boundaries ("use existing AuthService", "no data model changes")
- **Auto-Enriched Context:** Codebase discoveries annotated automatically
- **Evidence Links:** Every decision traced to customer voice + data + strategy

**Why Machine-Actionable:** Cursor reads structure → proposes implementation → developer reviews. No translation layer, no reformatting, no clarifying questions.

---

#### **5. Git Integration (Version-Controlled Living Artifacts)**

**What:** Specs as first-class git artifacts (not documents buried in Confluence)

**Capabilities:**
- **Commit to Git:** Push generated specs to user's GitHub repo via API
- **Branch Strategy:** Create feature branches for specs (e.g., `specs/onboarding-optimization`)
- **Version History:** Track spec evolution over time (git log shows reasoning changes)
- **Traceability:** Developer references spec commit SHA in implementation PR

**Why Git-Based:**
- Single source of truth from discovery → execution
- Audit trail for compliance (fintech, healthcare requirements)
- Developer workflow alignment (specs live where code lives)
- Natural version control without building custom system

**Not in MVP:** Rich git UI, diff visualization, merge conflict resolution - basic commit/push only for MVP.

---

### MVP User Flow (End-to-End)

**Sarah's MVP Experience:**

1. **Upload Data (5 minutes):**
   - Drags 15 interview transcripts into upload zone
   - Exports Jira tickets to CSV, uploads
   - Exports Datadog funnel data, uploads
   - Connects GitHub repo (OAuth, read-only)
   - Writes strategic brief: "Q1 goal: Reduce onboarding drop-off by 20%"

2. **Intake Discovers Problems (90 seconds):**
   - Analyzes transcripts: "23% abandon at bank connection step"
   - Cross-refs Jira: 45 tickets mention "bank connection failure"
   - Checks behavior: Desktop 8% abandon, mobile 23% abandon
   - Flags contradiction: None (say and do align - real problem)
   - Outputs: "Bank connection reliability (mobile focus)" as #1 priority

3. **Intake Generates Spec (30 seconds):**
   - Scans codebase: Found `BankIntegrationService` at `/src/services/bank/`
   - Identifies integrations: Plaid (8% failure), MX (3% failure), Yodlee (5% failure)
   - Constraint: "No transaction table changes" (detected: large table, multi-tenant)
   - Generates spec with auto-enriched context

4. **Sarah Reviews (2 minutes):**
   - Reads spec: "Goal: Reduce bank abandonment 20%, Success: 95% connection success"
   - Validates constraints: "Use existing BankIntegrationService" ✓ correct
   - Checks evidence: Customer quotes + usage data linked ✓
   - Approves spec

5. **Commit to Git (10 seconds):**
   - Intake pushes to GitHub: `specs/bank-connection-optimization.yaml`
   - Branch created: `specs/bank-connection-optimization`
   - Sarah shares link in Slack: "New spec ready for implementation"

6. **Developer + Cursor Execute (same day):**
   - Developer opens spec in Cursor
   - Cursor reads: Goal, success criteria, constraints, context
   - Cursor proposes: Switch primary integration to MX (lower failure rate)
   - Developer reviews, approves, ships

**Total Time: Idea → Shipping Code = 8 minutes PM work + same-day development**

---

### Out of Scope for MVP

**The following features are intentionally deferred to validate core value first:**

#### **Automated Integrations (v2.0+)**
- ❌ Live Modjo API integration (manual CSV upload for MVP)
- ❌ Jira webhook syncing (manual export for MVP)
- ❌ Datadog/Looker live connections (CSV upload for MVP)
- ❌ Zendesk integration (not in MVP scope)
- ❌ Slack/email notifications (commit to git is sufficient for MVP)

**Rationale:** Manual upload proves value without complex integration engineering. If users love the output, they'll tolerate manual upload. If output doesn't deliver value, integrations won't save it.

---

#### **Multi-Agent Workflows (V2 - 12 months post-launch)**

**OpenAI pattern:** Engineers manage 10-20 parallel AI threads, achieving 70% productivity gain.

**Intake V2 will enable:**
- ❌ **Parallel exploration workflows:** PM explores 5 feature approaches simultaneously
- ❌ **Live spec updates:** Agents discover contradictions/evidence while working
- ❌ **Coordinator + specialist agents:** One coordinator manages multiple specialist reasoners
- ❌ **PM steering across threads:** Review/approve multiple explorations in parallel
- ❌ **Cross-thread synthesis:** Best insights from 5 explorations → 1 final spec

**Why V2, not MVP:**
- Requires extended coherence (models improving in 2026)
- Complex orchestration UX (needs MVP validation first)
- Builds on proven single-spec generation workflow

**Timeline:** 12 months post-launch (once MVP validates core value)

**Expected impact:** 10x exploration speed (mirrors OpenAI's 70% productivity gain)

---

#### **Advanced Discovery Features (v2.0+)**
- ❌ Semantic codebase understanding (ML-powered "what's possible" analysis)
- ❌ Auto-update specs when new data ingested (flag conflicts for PM review only)
- ❌ Predictive recommendations ("you should build this next based on patterns")
- ❌ Multi-language support (English only for MVP)
- ❌ Custom reasoning frameworks (BMAD only for MVP)

**Rationale:** Parsing-first approach is MVP-tractable and delivers 80% of value. Semantic understanding is research-heavy—defer until core value proven.

---

#### **Multiplayer Features (Platform Phase - 18+ months)**
- ❌ Real-time collaboration (GitHub-style for PMs)
- ❌ Commenting and review workflows
- ❌ Team permissions and roles
- ❌ Shared knowledge graphs across PM teams
- ❌ Change request workflows

**Rationale:** Single-player experience validates individual PM value. Multiplayer features matter for scale (500+ customers), not MVP (first 100).

---

#### **Platform & Ecosystem (Platform Phase - 18+ months)**
- ❌ Public API for third-party integrations
- ❌ Agent orchestration hub (beyond internal multi-agent)
- ❌ Anonymized cross-customer insights (say-vs-do benchmarks)
- ❌ Marketplace for reasoning plugins
- ❌ White-label/on-premise deployment

**Rationale:** Platform features are valuable once category leadership established. Focus MVP on core product-market fit.

---

#### **Advanced UX & Visualization (v2.0+)**
- ❌ Rich evidence visualization (interactive graphs, timeline views)
- ❌ Interactive codebase exploration (click-through service maps)
- ❌ Visual workflow builders (drag-drop discovery flows)
- ❌ AI chat interface for spec refinement
- ❌ Mobile app (web-only for MVP)

**Rationale:** Simple upload → generate → review workflow is sufficient if output quality is excellent. Polish UX after core value proven.

---

### MVP Success Criteria

**How we'll know the MVP validates our hypothesis:**

#### **User Validation (First 50-100 Users)**

**Primary Success Gate:**
- **80%+ of generated specs shippable without developer clarifying questions**
  - Measures: Machine-actionable quality, auto-enrichment accuracy, PM value
  - Target: 80% (stretches to 90% as system learns)
  - Failure threshold: < 60% indicates core value unproven

**Adoption Metrics:**
- **Users generate 5+ specs in first week:** Proves speed value (baseline: 2-4 PRDs)
- **Time to first spec < 5 minutes:** Proves ease of use
- **"Aha moment" within 3 specs:** 85%+ users generate 3+ specs in first session

**Retention Metrics:**
- **70%+ retention at 30 days:** Proves "can't go back" stickiness
- **90%+ retention at 90 days:** Confirms daily habit formation
- **Users generate 8-12 specs/week:** Proves sustained velocity (vs. 2-4 baseline)

---

#### **Quality Validation (Engineering Approval)**

**Primary Success Gate:**
- **Auto-enriched codebase context 90%+ accurate**
  - Measures: Service discovery precision, constraint correctness
  - Test: Does "use existing BankIntegrationService" match reality?
  - Failure threshold: < 80% accuracy breaks engineering trust

**Developer Experience:**
- **Clarifying questions < 2 per spec:** Target < 1 average (baseline: 10+)
- **Engineering approval 85%+ of specs without rework:** Proves quality
- **Engineering NPS 50+:** Developers love receiving Intake specs

---

#### **Business Validation (Go-to-Market Proof)**

**Primary Success Gate:**
- **50+ paying customers within 6 months**
  - Measures: Product-market fit, willingness to pay
  - Stretch target: 500 customers = category validation
  - Minimum: 50 = MVP validated, proceed to scale

**Growth Validation:**
- **Word-of-mouth drives 30%+ of signups:** Proves viral potential
- **Users pay $39-99/PM/month:** Mid-market pricing validated
- **CAC < $500:** Growth efficiency validated
- **Trial → Paid conversion 15%+:** Product value clear

---

#### **MVP Decision Gates**

**If Success Criteria Met (80%+ spec quality, 70%+ retention, 50+ customers):**
→ **Scale Go-to-Market:** Invest in automated integrations, enterprise features, multiplayer  
→ **Raise Funding:** MVP validates $5-10M Series A opportunity  
→ **Category Leadership:** Position as "product reasoning infrastructure" leader

**If Partial Success (spec quality good, but low adoption/retention):**
→ **Iterate on Discovery UX:** Core value proven, onboarding/workflow needs improvement  
→ **Pricing Adjustment:** Value clear, but pricing/packaging needs refinement  
→ **ICP Refinement:** Product works, but for different segment than expected

**If Core Value Unproven (< 60% spec quality, high churn, low willingness to pay):**
→ **Pivot Discovery Approach:** Open-ended discovery too ambitious? Try validation mode  
→ **Rethink Auto-Enrichment:** Parsing insufficient? Need semantic understanding sooner  
→ **Reassess Problem:** Is PM bottleneck real or are we solving wrong problem?

---

### Future Vision

**If Intake MVP succeeds, here's the path from product to platform:**

#### **Phase 2: Multi-Agent Workflows + Automation (Months 7-18)**

**Goal:** Enable parallel exploration (OpenAI's 10-20 threads pattern) and eliminate manual work

**Key Features:**

**Multi-Agent Workflows (V2 - The Game Changer):**
- **Parallel exploration:** PM launches 5 different feature approaches simultaneously
- **Coordinator + specialists:** One coordinator agent manages multiple specialist reasoning agents
- **Live updates:** Agents discover new evidence/contradictions while exploring
- **PM steering:** Review and approve across multiple threads in parallel
- **Cross-thread synthesis:** Best insights from 5 explorations → 1 final spec
- **Expected impact:** 10x exploration speed (mirrors OpenAI's 70% productivity gain)

**Automated Data Ingestion:**
- Live Modjo API integration (real-time interview sync)
- Jira webhook syncing (tickets flow automatically)
- Datadog/Looker live dashboards (no CSV exports)
- Zendesk integration (support ticket signals)
- Slack integration (notifications, quick spec sharing)

**Semantic Codebase Understanding:**
- ML-powered "what's technically possible" analysis
- Architectural pattern recognition (microservices, monolith, serverless)
- Performance impact prediction ("this change affects 200+ customer DBs")
- Security/compliance constraint detection (PII handling, GDPR implications)

**Auto-Update Specs:**
- New data triggers spec update suggestions
- PM reviews and approves changes (not fully automated)
- Diff visualization shows what changed and why
- Git merge workflow for conflicting updates

**Enterprise Features:**
- SSO (Okta, Azure AD)
- Compliance certifications (SOC 2, GDPR)
- Advanced audit logs (regulatory requirements)
- Custom retention policies
- On-premise deployment option

**Success Indicator:** 5,000+ customers, $12.4M ARR, Top 3 AI-native PM tool, multi-agent workflows proven at scale

---

#### **Phase 3: Platform & Multiplayer (Months 19-36)**

**Goal:** Become the operating system for product development

**Key Features:**
- **Multiplayer Product Work (GitHub for PMs):**
  - Real-time collaboration on specs
  - Commenting, review workflows, approvals
  - Shared knowledge graphs across PM teams
  - Product history and decision archaeology
  - Cross-team pattern sharing

- **API Ecosystem:**
  - Public API for third-party integrations
  - Agent orchestration hub (coordinate external AI agents)
  - Webhook system for custom workflows
  - Plugin marketplace (custom reasoning frameworks)
  - White-label API for partner integrations
  - MCP-style community integrations (like Cursor)

- **Network Effects & Insights:**
  - Anonymized cross-customer insights (industry benchmarks)
  - "Teams like yours prioritize X features"
  - Say-vs-do pattern libraries by vertical (fintech, healthcare, SaaS)
  - ML model improves with aggregated data
  - Predictive recommendations ("you should explore this problem next")

- **Advanced Discovery:**
  - Hypothesis testing mode (validate ideas before building)
  - A/B test recommendation (which variant to test)
  - Impact forecasting (predict feature adoption, usage)
  - Competitive intelligence (track competitor feature launches)
  - Market trend detection (emerging patterns across verticals)

**Success Indicator:** Category ownership, "product reasoning infrastructure" is Intake's category, 50+ third-party integrations, community-built reasoning plugins

---

#### **Platform Vision: The Operating System for Product**

**Long-Term (3+ years):**

Intake becomes the foundational layer for product work—like Git for code, Figma for design:

**The Primitives:**
- `ingest` — Signals flow continuously from all sources
- `reason` — AI triangulates evidence, surfaces insights
- `generate` — Machine-actionable specs created on-demand
- `trace` — Every decision auditable, every insight sourceable
- `collaborate` — Teams work together on product knowledge
- `orchestrate` — AI agents coordinate around Intake specs

**The Ecosystem:**
- Cursor/Claude Code: Official partners for "spec → code" execution
- Modjo/Gong: Official partners for "customer voice → insights"
- Jira/Linear: Official partners for "spec → task management"
- Datadog/Amplitude: Official partners for "behavior → insights"
- Community: 100+ integrations, plugins, custom reasoning frameworks

**The Network Effect:**
- More users → Better insights (anonymized patterns)
- More data → Smarter reasoning (ML improves)
- More integrations → Stronger moat (ecosystem lock-in)
- Category definition → Market leadership (Intake = product reasoning)

**The Outcome:**
- PMs answer "What to build next?" in seconds, not weeks
- Engineering trusts specs implicitly (zero clarifying questions is standard)
- Product decisions are auditable, traceable, evidence-based
- AI agents coordinate seamlessly around machine-actionable specs
- Product work scales without proportional PM headcount

**This is the vision. The MVP is step one.**

---

## Strategic Positioning & Competitive Advantage

### Building for 12-24 Months Out (Not Today's Limitations)

**OpenAI strategic warning:** *"Build for where models are going, not where they are today. Models will eat your scaffolding for breakfast."*

**What dies (Scaffolding that models will obsolete):**
- ❌ Complex RAG pipelines (models getting better context windows)
- ❌ Over-engineered vector stores (embeddings improving)
- ❌ Workarounds for model limitations (capabilities expanding rapidly)

**What survives (Durable infrastructure):**
- ✅ **Context encoding structure** (BMAD triangulation)
- ✅ **Evidence traceability** (compliance + trust)
- ✅ **Integration layer** (Modjo, Jira, GitHub, Datadog)
- ✅ **PM-native UX** (management frameworks, not technical)
- ✅ **Model agnosticism** (works with any provider)
- ✅ **Framework agnosticism** (works with any tech stack)

### Architecture Advantages (Durable Moats)

**1. Model Agnostic = Strategic Flexibility**
- Works with Claude, GPT-4, Gemini, Llama, future models
- Not locked to single AI provider (competitive advantage)
- As models improve → Intake capabilities improve automatically
- Competitors locked to providers face strategic risk

**2. Framework Agnostic = Broad Market Appeal**
- Supports any development framework (React, Vue, Angular, Django, Rails, etc.)
- Machine-actionable specs describe "what," not "how"
- Engineering chooses implementation approach
- PMs don't need framework-specific knowledge

**3. Multi-Agent Ready = 10x Future Potential**
- V2 enables parallel exploration workflows (mirrors OpenAI's 10-20 threads)
- PM explores 5 feature approaches simultaneously
- Live updates as agents discover contradictions/evidence
- Expected impact: 10x exploration speed (validated by OpenAI's 70% productivity gain)

**Why competitors struggle:**
- ProductBoard/Aha built on legacy architecture (18-24 months to retrofit)
- Locked to single AI providers (strategic inflexibility)
- Can't support multi-agent workflows without ground-up rebuild
- **Intake built with this flexibility from day 1**

### Distribution as Primary Moat

**OpenAI prediction:** *"As software becomes easier to create, distribution and audience become the primary differentiator."*

**Our distribution advantage: 840+ enterprise PM engagement**
- Not just quantity—QUALITY: Microsoft, Meta, Amazon, NVIDIA, Gong, CrowdStrike
- High buyer intent: Companies with budgets, proven willingness to pay for PM tools
- Content-led GTM validated: 840 comments prove organic reach works
- ICP quality: B2B SaaS, cybersecurity, enterprise (our exact targets)

**First-mover urgency:**
- Public engagement alerts competitors (ProductBoard watching)
- Window to own category: 6-9 months before incumbents react
- Distribution moat compounds with early users (network effects, referrals)
- Category definition: First to own "Product Reasoning Infrastructure" language

### Competitive Timeline (Why Speed Matters)

| Competitor | Time to Build | Likelihood | Our Action |
|------------|---------------|------------|------------|
| ProductBoard/Aha | 18–24 months | MEDIUM | Own category before they ship |
| Cursor | Unlikely | LOW | Focus on developers, not PMs |
| ChatGPT/Claude | 12–18 months | MEDIUM | Requires new product, not feature |
| New Startups | 6–12 months | HIGH | Distribution moat (840 PMs) critical |

**Critical factor:** Public engagement (840 comments) alerts competitors. First-mover advantage requires **shipping MVP in 6 months, category ownership in 12 months.**

### Why Intake Wins (Summary)

**Pattern Validated:**
- ✅ OpenAI: 95% engineer adoption, 70% more output through management (not coding)
- ✅ RevOps leader: Management loop > technical skills, delegation > mastery
- ✅ Technical PMs: DIY builders shipped products in 2 weeks (approach validated)
- ✅ Market screaming: 840+ enterprise PMs engaged, high-quality ICP active NOW

**Gap Clear:**
- ❌ Current AI tools: No infrastructure, no context encoding, no management automation
- ❌ Traditional PM tools: Human-readable, no machine-actionable output, no codebase awareness
- ❌ DIY approach: Works but requires expertise, no built-in reasoning framework

**Moats Durable:**
- 🏰 Context encoding (BMAD): Proprietary framework, say-vs-do detection, integration complexity
- 🏰 Evidence traceability: Compliance value, audit trails, engineering trust
- 🏰 Automated management loop: Workflow expertise, accessible to non-technical users
- 🏰 Model & framework agnostic: Future-proof architecture, not locked to providers
- 🏰 Multi-agent orchestration (V2): 10x exploration speed, live updates across parallel workflows
- 🏰 Distribution advantage: 840+ PMs, content-led GTM proven, category leadership

**Window Closing:**
- ⏰ First-mover advantage: 6-9 months before incumbents react
- ⏰ Public engagement: 840 comments alert competitors (ProductBoard watching)
- ⏰ Market timing: Golden age of bespoke B2B SaaS (we enable it)
- ⏰ Build for future: 12-24 month model capabilities (extended coherence incoming)

---
