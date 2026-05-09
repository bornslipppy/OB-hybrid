# Intake UX Design Plan

**Version:** 2.0  
**Date:** February 13, 2026 (Updated)  
**Based on:** Product Brief - Intake 2026-02-13 (Latest)  
**Purpose:** Comprehensive UX design strategy aligned with MVP scope and user needs

---

## Executive Summary

This UX design plan translates the updated Intake product brief into actionable design deliverables. **Intake is Product Reasoning Infrastructure**—the context layer between scattered signals and AI execution, validated by OpenAI's transformation where 95% of engineers now manage AI agents (not write code), achieving 70% more output.

**Primary Design Goal:** Create a PM-native interface that automates the proven "management loop" (Brief → Dialogue → Investigation → Critique → Production) collapsing 4-5 hours of manual work to 90 seconds.

**Core UX Challenges:**
1. **Visualizing context encoding (BMAD triangulation)**: SAY vs DO vs TECHNICAL vs BELIEVES
2. **Making say-vs-do contradictions actionable**: Flag when customers want features they won't use
3. **Showing the automated management loop**: Make 5-step automation visible and trustworthy
4. **Designing for future multi-agent workflows (V2)**: Layout supports parallel exploration
5. **Leveraging social proof**: 840+ enterprise PM engagement as trust signal

---

## Design Principles

### 1. Context Encoding Made Visible (The Core Moat)
**OpenAI Validation:** *"Most agent failures stem from lack of tribal knowledge. Solving this requires encoding knowledge into files the model can ingest."*

**Our Differentiator:** BMAD triangulation = Structured context encoding

**Our Approach:**
- **Visual 4-quadrant framework**: Show SAY (interviews), DO (behavior), TECHNICAL (codebase), BELIEVES (strategy)
- **Contradiction highlighting**: Red flags when customer SAY conflicts with customer DO
- **Evidence linking**: Each quadrant shows sources, counts, and strength
- **Completion indicators**: Visual progress (3/4 signals complete, TECHNICAL scanning...)
- **Auto-enrichment badges**: Purple "🤖 Auto-enriched" tags on TECHNICAL discoveries

**Design Litmus Test:** Does Sarah understand why Intake said "don't build this" when customers asked for it?

**Example Visualization:**
```
┌─────────────────────────────────────────────────────────┐
│  Context Encoding (BMAD)                    Confidence: 92%│
├────────────────────┬────────────────────┐                │
│  💬 SAY            │  📊 DO             │                │
│  "Need analytics"  │  80% never open    │ ⚠️ CONTRADICTION
│  15 interviews     │  3mo behavior data │                │
├────────────────────┼────────────────────┤                │
│  🤖 TECHNICAL      │  🎯 BELIEVES       │                │
│  AnalyticsService  │  "Reduce churn"    │ ✓ ALIGNED      
│  /src/analytics    │  Q1 goal           │                │
└────────────────────┴────────────────────┘                │
```

---

### 2. Automated Management Loop (Infrastructure, Not DIY Mastery)
**Problem:** Successful AI users manually execute a 4-5 hour workflow. Most PMs don't know this pattern exists.

**Our Approach:**
- **Show the 5 steps visually**: Brief → Dialogue → Investigation → Critique → Production
- **Progress indicators for each step**: ✓ Brief (loaded from BMAD), ⏳ Investigation (fetching evidence)...
- **Time savings prominent**: "Manual: 4-5 hours → Intake: 90 seconds"
- **Expandable detail**: Click any step to see what Intake automated
- **Educational tooltips**: Teach the pattern while executing it

**Design Litmus Test:** Does Sarah understand *how* Intake automated 4 hours of work?

**Example Visualization:**
```
┌─────────────────────────────────────────────────────────┐
│  Management Loop (Automated)                            │
│                                                         │
│  ✓ Brief         → Loaded from BMAD (0 seconds)        │
│  ✓ Dialogue      → Contradictions surfaced (15 sec)    │
│  ✓ Investigation → Evidence chains built (30 sec)      │
│  ✓ Critique      → Validation checks passed (20 sec)   │
│  ⏳ Production   → Generating spec... (25 sec)         │
│                                                         │
│  Total: 90 seconds (Manual approach: 4-5 hours)        │
└─────────────────────────────────────────────────────────┘
```

---

### 3. Say-vs-Do Contradictions as First-Class Feature
**Key Insight:** Customers claim to want features they won't use. This prevents wasted engineering effort.

**Our Approach:**
- **Contradiction cards**: Prominent red/yellow warning cards when SAY ≠ DO
- **Impact estimation**: "Building this would waste 2 weeks based on usage patterns"
- **Recommendation actions**: "Investigate further" or "Deprioritize" buttons
- **Historical accuracy**: Show success rate of contradiction detection over time
- **Learning system**: PM can mark false positives to improve detection

**Design Litmus Test:** Does Sarah trust Intake when it says "don't build this"?

**Example Contradiction Card:**
```
┌─────────────────────────────────────────────────────────┐
│  ⚠️ SAY-vs-DO Contradiction Detected                   │
│                                                         │
│  Customers SAY: "We need advanced filtering"            │
│  • 12/15 interviews mentioned this                     │
│  • Rated as "critical" priority                        │
│                                                         │
│  Customers DO: Use only 2 of 8 existing filters        │
│  • 92% use basic filters only                          │
│  • Advanced filters: 8% adoption                       │
│                                                         │
│  Recommendation: Don't over-build. Focus on improving   │
│  the 2 filters customers actually use.                  │
│                                                         │
│  Impact: Saves ~2 weeks engineering time                │
│                                                         │
│  [Investigate Further] [Deprioritize] [Override]       │
└─────────────────────────────────────────────────────────┘
```

---

### 4. Social Proof & Distribution Signal
**Strategic Asset:** 840+ enterprise PM comments (Microsoft, Meta, Amazon, NVIDIA, Gong)

**Our Approach:**
- **Trust indicators on marketing pages**: "Join 840+ PMs from Microsoft, Meta, Amazon..."
- **Activity feed shows real usage**: "23 PMs generated specs today"
- **Company logos (where permitted)**: Show recognizable brands using Intake
- **Community insights**: "Teams like yours prioritize X features" (anonymized)
- **Referral tracking visible**: "Sarah from Acme recommended you join"

**Design Litmus Test:** Does Sarah feel she's joining a movement, not buying a tool?

---

### 5. PM-Native, Not Developer-Native
**Problem:** Cursor excludes non-technical PMs with IDE interfaces, git concepts, terminal commands.

**Our Approach:**
- Visual, drag-and-drop interfaces for data upload
- Natural language everywhere (no git commands in UI)
- Hide technical complexity (OAuth flows, repo scanning, YAML generation behind scenes)
- Progressive disclosure (advanced features only when needed)
- Management framework language ("Brief, Dialogue, Investigation" not "RAG, embedding, vector store")

**Design Litmus Test:** Could Sarah (non-technical PM from UX background) use this without asking for help?

---

### 6. Speed as a Feature
**Goal:** 90 seconds from signals to spec, 5 minutes including review.

**Our Approach:**
- One-click actions ("Generate Spec", "Commit to Git")
- Batch uploads (drag 15 files at once)
- Smart defaults (auto-detect data types)
- Async processing with clear progress
- Instant feedback (stream results)
- **Time savings always visible**: "Saved: 4h 57min"

**Design Litmus Test:** Can Sarah generate her first spec in under 5 minutes on day one?

---

### 7. Git Integration Without Git Knowledge
**Problem:** Specs need to be git-versioned, but PMs don't use git.

**Our Approach:**
- One-click "Commit to Git" (no branch names, commit messages, push commands)
- Auto-generated commit messages (readable, semantic)
- Visual git history (timeline view, not command line)
- Shareability (copy link to spec in GitHub)

**Design Litmus Test:** Can Sarah commit a spec to git without knowing what a branch is?

---

### 8. Design for Multi-Agent Future (V2 Ready)
**OpenAI Pattern:** Engineers manage 10-20 parallel AI threads (70% more output)

**Our Approach (Foundation in MVP):**
- Layout supports side-by-side comparison (future: 5 parallel explorations)
- Status indicators accommodate multiple threads (today: 1 spec, V2: 5 specs in parallel)
- "Coordinator" language (today: single workflow, V2: coordinator + specialist agents)
- Expansion slots in UI (room for additional agent cards)

**Design Litmus Test:** Does the UI feel ready to scale to multi-agent workflows without major redesign?

**Note:** Multi-agent workflows NOT in MVP, but UX foundation laid today.

---

## BMAD Triangulation Visualization (Core Differentiator)

### Overview

**BMAD = The visual manifestation of our core moat: Context Encoding Infrastructure**

The BMAD framework visualizes how Intake triangulates 4 signal types to create machine-actionable specs. This is what separates Intake from generic AI tools and traditional PM software.

### The 4-Quadrant Model

```
┌─────────────────────────────────────────────────────────────┐
│  🔍 Discovery: Bank Connection Issues          92% Confidence│
│                                                             │
│  ┌────────────────────┬─────────────────────┐              │
│  │ 💬 SAY             │ 📊 DO               │              │
│  │ (Customer Voice)   │ (Behavior Data)     │              │
│  ├────────────────────┼─────────────────────┤              │
│  │ "Bank connection   │ 23% mobile users    │              │
│  │ fails constantly"  │ abandon at connect  │              │
│  │                    │ (vs 8% desktop)     │              │
│  │ 15 interviews      │ 3 months data       │              │
│  │ 45 Jira tickets    │ 2,847 drop-offs     │              │
│  │                    │                     │              │
│  │ [View Sources]     │ [View Funnel]       │              │
│  └────────────────────┴─────────────────────┘              │
│          │                      │                           │
│          └──────────┬───────────┘                           │
│                     ↓                                       │
│              ✓ ALIGNED                                      │
│        (SAY matches DO = Real problem)                      │
│                                                             │
│  ┌────────────────────┬─────────────────────┐              │
│  │ 🤖 TECHNICAL       │ 🎯 BELIEVES         │              │
│  │ (Codebase Context) │ (Strategic Goals)   │              │
│  ├────────────────────┼─────────────────────┤              │
│  │ ✓ Found:           │ Q1 Goal:            │              │
│  │ BankIntegration    │ "Reduce onboarding  │              │
│  │ Service            │ drop-off by 20%"    │              │
│  │ /src/services/bank │                     │              │
│  │                    │ Strategic Priority: │              │
│  │ Integrations:      │ HIGH                │              │
│  │ • Plaid (8% fail)  │                     │              │
│  │ • MX (3% fail) ✓   │ Budget: Available   │              │
│  │ • Yodlee (5%)      │                     │              │
│  │                    │                     │              │
│  │ Constraint:        │ Deadline: Q1 end    │              │
│  │ No schema changes  │                     │              │
│  │ (200+ tenant DBs)  │                     │              │
│  │                    │                     │              │
│  │ [View Code]        │ [Edit Goals]        │              │
│  └────────────────────┴─────────────────────┘              │
│                                                             │
│  [Generate Spec] ← Primary CTA                             │
└─────────────────────────────────────────────────────────────┘
```

### Interaction Patterns

#### 1. **Quadrant Expansion**
- Click any quadrant to expand full-screen
- Shows all sources, data points, and evidence
- Inline filtering and sorting

#### 2. **Contradiction Detection**
- Red warning icon when SAY ≠ DO
- Yellow caution when partial mismatch
- Green checkmark when aligned
- Hover for explanation

#### 3. **Auto-Enrichment Badges**
- Purple "🤖 Auto-enriched" badge on TECHNICAL discoveries
- Tooltip: "Found by scanning your codebase"
- Click to see scan details

#### 4. **Confidence Score**
- Percentage at top-right (92%)
- Color-coded: Green (>90%), Yellow (70-89%), Red (<70%)
- Breakdown on hover (SAY: 95%, DO: 88%, TECHNICAL: 95%, BELIEVES: 90%)

### States & Edge Cases

**1. Incomplete Context (3/4 Quadrants Complete)**
```
┌─────────────────────────────────────────────────────────────┐
│  ⏳ Building Context...                      3/4 Complete   │
│                                                             │
│  ┌────────────────────┬─────────────────────┐              │
│  │ 💬 SAY ✓           │ 📊 DO ✓             │              │
│  │ 15 interviews      │ 3 months data       │              │
│  └────────────────────┴─────────────────────┘              │
│                                                             │
│  ┌────────────────────┬─────────────────────┐              │
│  │ 🤖 TECHNICAL ⏳    │ 🎯 BELIEVES ✓       │              │
│  │ Scanning codebase  │ Q1 Goal loaded      │              │
│  │ 1,247 files...     │                     │              │
│  └────────────────────┴─────────────────────┘              │
│                                                             │
│  [Wait for completion] or [Generate Anyway] (lower confidence)
└─────────────────────────────────────────────────────────────┘
```

**2. Contradiction Alert**
```
┌─────────────────────────────────────────────────────────────┐
│  ⚠️ Contradiction Detected                  74% Confidence  │
│                                                             │
│  ┌────────────────────┬─────────────────────┐              │
│  │ 💬 SAY             │ 📊 DO               │              │
│  │ "Need analytics"   │ 80% never open      │ ⚠️ MISMATCH │
│  │ 12 interviews      │ existing analytics  │              │
│  └────────────────────┴─────────────────────┘              │
│          │                      │                           │
│          └──────────┬───────────┘                           │
│                     ↓                                       │
│         ⚠️ SAY-vs-DO CONTRADICTION                          │
│                                                             │
│  Recommendation: Customers SAY they want this, but behavior │
│  shows they don't use existing features. Investigate before │
│  building.                                                  │
│                                                             │
│  [Investigate Further] [Override] [Skip This Discovery]    │
└─────────────────────────────────────────────────────────────┘
```

**3. No Technical Constraints Found**
```
┌────────────────────┐
│ 🤖 TECHNICAL       │
│                    │
│ No constraints     │
│ detected           │
│                    │
│ ✓ Clean slate     │
│ Build as needed    │
│                    │
│ [Rescan Codebase]  │
└────────────────────┘
```

### Animation & Microinteractions

**Loading Sequence:**
1. SAY quadrant fills (15s - NLP analysis)
2. DO quadrant fills (10s - data processing)
3. TECHNICAL quadrant fills (30s - codebase scan)
4. BELIEVES quadrant fills (5s - goal extraction)
5. Contradiction check runs (5s)
6. Confidence score appears (fade in)

**Contradiction Pulse:**
- Red warning icon pulses when detected
- Draws eye to SAY-DO mismatch
- Stops pulsing when user acknowledges

---

## User Flows

### Primary Flow: Sarah's MVP Experience

**Goal:** From scattered signals to Cursor-ready spec in 5 minutes.

#### Flow Stages

**Stage 1: Upload Data (3 minutes)**

```
┌─────────────────────────────────────────────────────────────┐
│  Welcome to Intake                                          │
│                                                             │
│  "Upload your product signals to get started"              │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  📄 Customer Interviews                             │   │
│  │  Drag files or click to upload                      │   │
│  │  ✓ 15 files • Modjo transcripts                    │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  🎫 Jira Tickets                                    │   │
│  │  ✓ 87 tickets • Exported CSV                       │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  📊 Behavioral Data                                 │   │
│  │  ✓ 3 months • Datadog funnel export                │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  🔗 GitHub Repository                               │   │
│  │  [Connect Repository] ← OAuth                       │   │
│  │  ✓ Connected • FinFlow/accounting-platform          │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  🎯 Strategic Brief                                 │   │
│  │  "Q1 goal: Reduce onboarding drop-off by 20%"      │   │
│  │  (Edit in-app)                                      │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  [Start Discovery] ←─────────────────────────────── Primary CTA
└─────────────────────────────────────────────────────────────┘
```

**UX Notes:**
- Drag-and-drop for all file uploads (feels modern, fast)
- Smart detection (recognizes file types, suggests categories)
- Optional fields (Strategic Brief can be skipped if empty)
- GitHub OAuth in modal (don't leave the page)
- Progress saved (can come back later)

---

**Stage 2: Discovery Engine with BMAD Visualization (90 seconds - Automated)**

```
┌─────────────────────────────────────────────────────────────┐
│  Building Context (BMAD Triangulation)                     │
│                                                             │
│  Management Loop Progress:                                  │
│  ✓ Brief      → Loaded strategic goals                     │
│  ⏳ Dialogue  → Finding contradictions... (15 sec)         │
│  ⏳ Investigation → Building evidence chains... (30 sec)   │
│  ⏳ Critique  → Running validation checks... (queued)      │
│  ⏳ Production → Generating specs... (queued)              │
│                                                             │
│  ┌────────────────────┬─────────────────────┐              │
│  │ 💬 SAY ✓           │ 📊 DO ✓             │              │
│  │ Analyzing 15       │ Processing 3mo      │              │
│  │ interviews...      │ behavior data...    │              │
│  │ 45 patterns found  │ 2,847 drop-offs     │              │
│  └────────────────────┴─────────────────────┘              │
│          │                      │                           │
│          └──────────┬───────────┘                           │
│                     ↓                                       │
│              Checking alignment...                          │
│                                                             │
│  ┌────────────────────┬─────────────────────┐              │
│  │ 🤖 TECHNICAL ⏳    │ 🎯 BELIEVES ✓       │              │
│  │ Scanning codebase  │ Q1 Goal: Reduce     │              │
│  │ 1,247 files...     │ drop-off 20%        │              │
│  │ 47% complete       │ Loaded              │              │
│  └────────────────────┴─────────────────────┘              │
│                                                             │
│  [View Progress Details] ← Expandable                      │
└─────────────────────────────────────────────────────────────┘

⬇ After completion (90 seconds):

┌─────────────────────────────────────────────────────────────┐
│  🎉 Context Complete: 3 Opportunities Discovered  92% Confidence│
│                                                             │
│  Opportunity #1: Bank Connection Reliability                │
│  ┌────────────────────┬─────────────────────┐              │
│  │ 💬 SAY             │ 📊 DO               │              │
│  │ "Bank connection   │ 23% mobile abandon  │ ✓ ALIGNED   │
│  │ fails constantly"  │ at connection step  │              │
│  │ 15 interviews      │ (vs 8% desktop)     │              │
│  │ 45 Jira tickets    │ 2,847 drop-offs     │              │
│  └────────────────────┴─────────────────────┘              │
│  ┌────────────────────┬─────────────────────┐              │
│  │ 🤖 TECHNICAL ✓     │ 🎯 BELIEVES ✓       │              │
│  │ BankIntegration    │ Q1: Reduce drop-off │              │
│  │ Service exists     │ by 20% (HIGH)       │              │
│  │ /src/services/bank │                     │              │
│  │ MX: 3% fail rate ✓ │ Budget: Available   │              │
│  └────────────────────┴─────────────────────┘              │
│                                                             │
│  Impact: HIGH • Confidence: 92% • No contradictions         │
│  [Generate Spec] ← Primary action                          │
│                                                             │
│  Opportunity #2: Email Verification Flow                    │
│  ⚠️ SAY-DO Contradiction detected • View details           │
│                                                             │
│  Opportunity #3: Multi-Currency Support                     │
│  Lower priority • View details                              │
│                                                             │
│  Time saved: 4h 32min (vs manual synthesis)                │
└─────────────────────────────────────────────────────────────┘
```

**UX Notes:**
- **BMAD quadrants show progress** (builds anticipation, educational)
- **Management loop visible** (Brief → Dialogue → Investigation → Critique → Production)
- **Contradictions flagged early** (red warning on Opportunity #2)
- **Time savings prominent** (reinforces value)
- **Confidence score** (builds trust)
- **Auto-enrichment highlighted** (purple badges on TECHNICAL findings)
- **One-click to spec generation** (highest impact opportunity is default)

---

**Stage 3: Spec Generation (30 seconds - Automated)**

```
┌─────────────────────────────────────────────────────────────┐
│  ⏳ Generating spec: Bank connection reliability...         │
│                                                             │
│  ✓ Writing goal and success criteria                       │
│  ✓ Extracting constraints from codebase                    │
│  ✓ Linking evidence sources                                │
│  ✓ Formatting for Cursor                                   │
│                                                             │
│  [Spec Ready for Review] ← Animated transition             │
└─────────────────────────────────────────────────────────────┘
```

---

**Stage 4: Spec Review (2 minutes - PM Control)**

```
┌─────────────────────────────────────────────────────────────┐
│  ← Back to Insights      Bank Connection Reliability        │
│                          Confidence: 92% ✓                  │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  🎯 Goal                                            │   │
│  │  Reduce bank reconciliation abandonment by 20%     │   │
│  │  [Edit] ← Inline editing                           │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  ✓ Success Criteria                                 │   │
│  │  • Connection success rate > 95%                    │   │
│  │  • Time to first reconciliation < 2 min             │   │
│  │  • Zero data consistency errors                     │   │
│  │  [+ Add Criterion]                                  │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  🔒 Constraints (Auto-Enriched)                     │   │
│  │  • Use existing BankIntegrationService ← /src/services│ │
│  │  • No transaction table schema changes ← Migration cost│
│  │  • Maintain SOC 2 audit trail ← Compliance requirement│
│  │  [+ Add Constraint]                                 │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  🤖 Context (Auto-Enriched)                         │   │
│  │  • BankIntegrationService supports Plaid, Yodlee, MX│  │
│  │  • MX has 3% failure rate vs Plaid 8%              │   │
│  │  • Multi-tenant isolation at database level         │   │
│  │  [View Codebase Discoveries]                        │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  📎 Evidence (15 sources linked)                    │   │
│  │  • "Bank connection fails 30%" - CFO, Acme Corp     │   │
│  │  • 23% abandon at connection - Datadog funnel       │   │
│  │  • 45 Jira tickets - "bank connection failure"      │   │
│  │  [View Evidence Chain]                              │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  📄 Machine-Actionable Format (YAML)                │   │
│  │  ```yaml                                            │   │
│  │  goal: Reduce bank reconciliation abandonment...    │   │
│  │  success_criteria:                                  │   │
│  │    - Connection success rate > 95%                  │   │
│  │  ...                                                │   │
│  │  ```                                                │   │
│  │  [Copy YAML] [Download]                            │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  [Regenerate] [Edit Manually] [Commit to Git] ← Primary    │
└─────────────────────────────────────────────────────────────┘
```

**UX Notes:**
- Confidence score prominent (builds trust)
- Inline editing everywhere (click to edit, no separate edit mode)
- Auto-enriched items annotated (← where it came from)
- Evidence is summarized, expandable (don't overwhelm)
- YAML visible but not required knowledge (copy/paste works)
- Multiple action paths (regenerate if wrong, edit if close, commit if perfect)

---

**Stage 5: Commit to Git (10 seconds)**

```
┌─────────────────────────────────────────────────────────────┐
│  Commit to Git                                 [X] Close    │
│                                                             │
│  Repository: FinFlow/accounting-platform                    │
│  Branch: specs/bank-connection-optimization (auto-created) │
│  File: specs/bank-connection-optimization.yaml              │
│                                                             │
│  Commit message (auto-generated):                          │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Add spec: Reduce bank connection abandonment       │   │
│  │                                                     │   │
│  │ - Goal: 20% reduction in mobile drop-off           │   │
│  │ - Auto-enriched with BankIntegrationService context│   │
│  │ - Evidence: 15 sources (interviews, tickets, data) │   │
│  │ (Editable)                                          │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  [Cancel] [Commit & Push] ← Primary action                 │
└─────────────────────────────────────────────────────────────┘

⬇ After commit:

┌─────────────────────────────────────────────────────────────┐
│  ✓ Committed to Git!                                        │
│                                                             │
│  Your spec is now live at:                                 │
│  github.com/FinFlow/accounting-platform/specs/...           │
│                                                             │
│  Share with your team:                                      │
│  [Copy Link] [Share in Slack] [Download PDF]               │
│                                                             │
│  Next steps:                                                │
│  • Developer can open this spec in Cursor                  │
│  • Cursor will read the structured YAML                    │
│  • Implementation can start immediately                     │
│                                                             │
│  [Generate Another Spec] [Back to Dashboard]               │
└─────────────────────────────────────────────────────────────┘
```

**UX Notes:**
- Auto-generated commit message (PM can edit if desired)
- No git jargon in UI ("branch" explained in hover tooltip)
- Success state celebrates achievement
- Clear next steps for PM and developer
- Shareability built-in (link copying, Slack integration)

---

### Secondary Flows

#### Flow 2: Dashboard (Returning User)

Sarah returns day 2, already has 3 specs committed.

```
┌─────────────────────────────────────────────────────────────┐
│  Intake                [Search specs...]        [@Sarah ▼] │
│                                                             │
│  [+ New Spec] ← Primary CTA                                │
│                                                             │
│  Your Specs (3)                                            │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Bank Connection Reliability               ✓ Shipped│   │
│  │  Goal: Reduce abandonment by 20%                    │   │
│  │  • Committed 2 days ago                             │   │
│  │  • Referenced in PR #234                            │   │
│  │  [View Spec] [View PR]                              │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Email Verification Flow                  🔄 In Dev │   │
│  │  Goal: Improve verification completion               │   │
│  │  • Committed 1 day ago                              │   │
│  │  [View Spec]                                        │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Multi-Currency Support                   📝 Draft  │   │
│  │  Goal: Enable international transactions             │   │
│  │  • Last edited 3 hours ago                          │   │
│  │  [Continue Editing]                                 │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  Recent Activity                                            │
│  • PR #234 merged - Bank connection feature shipped 🎉     │
│  • Developer @mike commented on Email Verification spec    │
│  • New Jira tickets uploaded (12) - Run discovery?         │
└─────────────────────────────────────────────────────────────┘
```

**UX Notes:**
- Status badges (Shipped, In Dev, Draft) show progress
- Activity feed keeps PM informed
- Easy re-entry to editing or viewing
- Prompts to run discovery when new data arrives

---

#### Flow 3: Evidence Chain Visualization

PM clicks "View Evidence Chain" to understand reasoning.

```
┌─────────────────────────────────────────────────────────────┐
│  Evidence Chain: Bank Connection Reliability                │
│                                                             │
│  🎯 Goal: Reduce abandonment by 20%                         │
│      ↓                                                      │
│  📊 Data Signal: 23% mobile users abandon at connection     │
│      Source: Datadog funnel (Jan-Mar 2026)                 │
│      ↓                                                      │
│  💬 Customer Voice: "Bank connection fails constantly"      │
│      Source: CFO interview, Acme Corp (Feb 3)              │
│      Source: CFO interview, BrightBooks (Feb 8)            │
│      +10 more interviews                                    │
│      ↓                                                      │
│  🎫 Engineering Signals: 45 Jira tickets                    │
│      "Bank connection timeout"                             │
│      "Plaid integration failing"                           │
│      "Mobile reconciliation errors"                        │
│      ↓                                                      │
│  🤖 Codebase Discovery: BankIntegrationService exists       │
│      Location: /src/services/bank/BankIntegrationService.ts│
│      Integrations: Plaid (8% fail), MX (3% fail)           │
│      ↓                                                      │
│  ✓ Success Criterion: Connection success rate > 95%         │
│      Rationale: Current 77% (mobile) too low               │
│                                                             │
│  [Export Evidence Report] [Share]                          │
└─────────────────────────────────────────────────────────────┘
```

**UX Notes:**
- Visual tree/chain structure (shows causality)
- Each node expandable (click to see full transcript/ticket)
- Traceability = trust (engineering can audit)
- Exportable for compliance (fintech requirement)

---

#### Flow 4: Codebase Discoveries (The "Magic" Moment)

PM clicks "View Codebase Discoveries" to see what Intake found.

```
┌─────────────────────────────────────────────────────────────┐
│  Codebase Discoveries: FinFlow/accounting-platform          │
│                                                             │
│  ✓ Scanned 1,247 files in 12 seconds                       │
│                                                             │
│  🎉 Services Found (3)                                      │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  BankIntegrationService                             │   │
│  │  /src/services/bank/BankIntegrationService.ts      │   │
│  │  • Plaid, Yodlee, MX integrations                   │   │
│  │  • OAuth flow handling                              │   │
│  │  [View Code on GitHub]                              │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  ReconciliationService                              │   │
│  │  /src/services/reconciliation/                      │   │
│  │  • Transaction matching logic                       │   │
│  │  • Multi-tenant data isolation                      │   │
│  │  [View Code on GitHub]                              │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ⚠️ Constraints Detected (2)                                │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Large Table: transactions (3.2M rows)              │   │
│  │  Schema changes = expensive migration               │   │
│  │  Recommendation: Avoid altering this table          │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Multi-Tenant Architecture                          │   │
│  │  Database isolation at tenant level                 │   │
│  │  Recommendation: Test changes per-tenant            │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  📊 Technical Patterns (4)                                  │
│  • NestJS framework                                         │
│  • PostgreSQL database                                      │
│  • Microservices architecture                               │
│  • Event-driven communication                               │
│                                                             │
│  [Rescan Codebase] [View Full Report]                      │
└─────────────────────────────────────────────────────────────┘
```

**UX Notes:**
- Celebration tone ("Found X services!" not "Scan complete")
- Direct links to GitHub (verify AI findings)
- Constraints explained (why they matter)
- Patterns inform future specs (learning system)

---

## Screen Inventory

### MVP Screens (Priority Order)

#### 1. **Data Upload / Onboarding** (P0 - First-run experience)
- Welcome message with social proof ("Join 840+ PMs...")
- 5 upload zones (interviews, tickets, data, GitHub, brief)
- Progress persistence
- OAuth modal for GitHub
- **NEW:** Management loop preview ("We'll automate Brief → Dialogue → Investigation...")

**Success Metric:** 90% complete upload in < 5 minutes

---

#### 2. **BMAD Context Building** (P0 - NEW - Core differentiator)
- 4-quadrant BMAD visualization (SAY, DO, TECHNICAL, BELIEVES)
- Live progress per quadrant
- Management loop progress overlay
- Contradiction detection (real-time)
- Confidence score building
- Time savings counter ("Saved: 2h 15min so far...")

**Success Metric:** 
- 85% users watch progress (don't navigate away)
- 70% understand what BMAD means by end
- "Aha moment" when TECHNICAL quadrant fills with auto-discoveries

---

#### 2.1. **Opportunity Review** (P0 - NEW - Discovery results)
- 3-5 opportunities with BMAD context
- Each opportunity shows 4-quadrant summary
- Contradiction alerts (if detected)
- Impact ranking
- Confidence scores
- Primary CTA: "Generate Spec" for top opportunity

**Success Metric:**
- 80% users generate spec for #1 opportunity
- 40% explore multiple opportunities before choosing

---

#### 3. **Contradiction Deep Dive** (P1 - Key feature)
- SAY vs DO side-by-side comparison
- Evidence sources (expandable)
- Impact estimation ("Saves 2 weeks engineering")
- Recommendation explanation
- Override capability with reasoning capture
- Historical accuracy (how often contradictions were correct)

**Success Metric:**
- 60% users view at least one contradiction
- 80% follow recommendation (don't override)
- 5% false positive rate (user says contradiction was wrong)

---

#### 4. **Spec Review** (P0 - Core value delivery)
- Goal (editable)
- Success criteria (add/remove)
- Constraints (auto-enriched, annotated)
- Context (discoveries)
- Evidence (linked, expandable)
- YAML preview (copy/download)
- Actions: Regenerate, Edit, Commit

**Success Metric:** 80% specs committed without major edits

---

#### 4. **Git Commit Modal** (P0 - Seamless handoff)
- Repository info
- Auto-generated commit message
- Branch creation (auto)
- Success confirmation
- Share options

**Success Metric:** 95% successful commits (no errors)

---

#### 5. **Dashboard / Home** (P1 - Returning user entry point)
- Spec list (3 states: Draft, In Dev, Shipped)
- Activity feed
- "New Spec" CTA
- Search/filter

**Success Metric:** 70% returning users go directly to "+ New Spec"

---

#### 6. **Evidence Chain Viewer** (P1 - Trust building)
- Visual tree structure
- Source links (expandable)
- Export capability

**Success Metric:** 60% users view at least once (validates trust building)

---

#### 7. **Codebase Discoveries Viewer** (P1 - "Magic" showcase)
- Services found (with paths)
- Constraints detected (with reasoning)
- Patterns identified
- Rescan option

**Success Metric:** 90% users exclaim "How did it know that?!"

---

### Post-MVP Screens (v2.0+)

- **Settings:** Integrations, repos, preferences
- **Spec Diff Viewer:** Compare versions, see changes
- **Team Collaboration:** Comments, reviews, approvals
- **Analytics Dashboard:** Usage stats, velocity metrics
- **Integration Setup Wizard:** Connect Modjo, Jira, Datadog live

---

## Component Library

### Core Components (Design System)

#### 0. **BMAD Quadrant Card** (NEW - Core Differentiator)
- 4-quadrant layout with equal sizing
- Icons per quadrant (💬 SAY, 📊 DO, 🤖 TECHNICAL, 🎯 BELIEVES)
- Status indicators (✓ Complete, ⏳ Working, ⚠️ Contradiction)
- Expandable detail view
- Confidence score header
- Alignment indicator between SAY-DO quadrants

**Variants:**
- Loading state (progress indicators)
- Complete state (all quadrants filled)
- Contradiction state (red warning)
- Aligned state (green checkmark)
- Incomplete state (some quadrants empty)

**Subcomponents:**
- Quadrant header (icon + title + status)
- Evidence count badge (e.g., "15 interviews")
- Auto-enrichment badge (🤖 purple badge)
- Alignment indicator (between SAY-DO)
- Expansion button (per quadrant)

---

#### 0.1. **Contradiction Alert Card** (NEW - Key Feature)
- Warning header (⚠️ SAY-vs-DO Contradiction)
- Two-column SAY vs DO comparison
- Impact estimation ("Saves ~2 weeks")
- Recommendation text
- Action buttons (Investigate, Override, Deprioritize)
- Confidence degradation warning

**Variants:**
- Strong contradiction (red, high certainty)
- Weak contradiction (yellow, investigate further)
- False positive (green, user marked as incorrect)

**States:**
- Unreviewed (pulsing animation)
- Acknowledged (static)
- Resolved (collapsed with summary)

---

#### 0.2. **Management Loop Progress** (NEW - Educational)
- 5-step vertical timeline
- Step icons (Brief, Dialogue, Investigation, Critique, Production)
- Time per step (Brief: 0s, Dialogue: 15s, etc.)
- Total time vs manual comparison
- Expandable step details

**Variants:**
- Processing (show current step animated)
- Complete (all steps green checkmarks)
- With time savings callout ("Saved: 4h 32min")

---

#### 1. **Upload Zone**
- Large drag-drop target
- File count badge
- Status indicator (empty, uploading, complete)
- File type auto-detection
- Error states

**Variants:**
- Empty state
- Uploading (progress bar)
- Complete (checkmark, file count)
- Error (red border, error message)

---

#### 2. **Progress Stepper**
- 5-stage vertical timeline
- Icons per stage
- States: Queued, Working (animated), Complete
- Expandable details

**Variants:**
- Processing (show current stage)
- Complete (all green)

---

#### 3. **Spec Section Card**
- Section header (Goal, Criteria, Constraints, etc.)
- Content area (editable inline)
- Auto-enriched badge (when applicable)
- Actions (Edit, Add, Remove)

**Variants:**
- View mode
- Edit mode (inline)
- Empty state (+ Add first item)

---

#### 4. **Evidence Link**
- Source preview (quote or metric)
- Source attribution (person, date, tool)
- Hover: Full content
- Click: Expand in modal

**Types:**
- Customer quote
- Data metric
- Jira ticket
- Strategic goal

---

#### 5. **Codebase Discovery Badge**
- Icon (service, constraint, pattern)
- Title (service name)
- Path annotation (← /src/services/auth/)
- Link to GitHub

**Types:**
- Service found (green)
- Constraint detected (yellow)
- Pattern identified (blue)

---

#### 6. **Confidence Score**
- Percentage (92%)
- Visual indicator (progress circle)
- Tooltip (how it's calculated)

**Thresholds:**
- 90-100%: High (green)
- 70-89%: Medium (yellow)
- <70%: Low (red, suggest regenerate)

---

#### 7. **Status Badge**
- Text label (Draft, In Dev, Shipped)
- Icon (pencil, gear, checkmark)
- Color coding

**States:**
- Draft (gray)
- In Dev (blue)
- Shipped (green)

---

#### 8. **Code Block**
- YAML syntax highlighting
- Line numbers
- Copy button
- Download button
- Collapsible sections

---

### Interaction Patterns

#### Pattern 1: Inline Editing
**Trigger:** Click any editable field
**Behavior:**
- Field becomes input/textarea
- Save button appears
- ESC to cancel, Enter to save
- Auto-save on blur (optional)

---

#### Pattern 2: Progressive Disclosure
**Use Cases:**
- Evidence (show 3, "+ See 12 more")
- Codebase discoveries (show top 3 services)
- YAML preview (collapsed by default)

---

#### Pattern 3: Empty States
**Components:**
- Illustration or icon
- Helpful message ("No specs yet. Create your first one!")
- Primary CTA

---

#### Pattern 4: Loading States
**Types:**
- Skeleton screens (for content loading)
- Progress bars (for upload/processing)
- Spinners (for quick actions)
- Streaming text (for AI generation)

---

## Visual Design Direction

### Brand Personality

**Intake is:**
- **Professional** yet **approachable** (PM-friendly, not intimidating)
- **Intelligent** yet **transparent** (AI-powered, but explainable)
- **Fast** yet **thoughtful** (speed without sacrificing quality)
- **Technical** yet **accessible** (handles complexity, hides it from user)

**Avoid:**
- Overly playful (this is serious work)
- Overly technical (don't alienate non-technical PMs)
- Generic SaaS (we're different, show it)

---

### Color Strategy

**Primary Palette:**
- **Primary Blue (#3B82F6):** Trust, professionalism, technology
  - Use for: CTAs, links, focus states
  - Avoid overuse: Not for all buttons/badges

**Semantic Colors:**
- **Success Green (#10B981):** Completion, shipped features, SAY-DO alignment, correct data
- **Warning Yellow (#F59E0B):** Weak contradictions, low confidence, attention needed
- **Error Red (#EF4444):** Strong contradictions, errors, failures, critical issues

**Neutral Grays:**
- **900-700:** Primary text (headings, body)
- **500-300:** Secondary text, borders
- **100-50:** Backgrounds, subtle dividers

**Special Use (NEW - Core Differentiator):**
- **Purple (#8B5CF6):** AI/auto-enrichment, TECHNICAL discoveries, magic moments
  - Use for: 🤖 Auto-enriched badges, TECHNICAL quadrant highlights, codebase discoveries
  - Brand association: "Intake found this automatically"
  - Accent color for differentiation from competitors

**BMAD Quadrant Colors:**
- **SAY Quadrant:** Blue accent (#3B82F6) - customer voice
- **DO Quadrant:** Green accent (#10B981) - behavior data
- **TECHNICAL Quadrant:** Purple accent (#8B5CF6) - auto-enriched context
- **BELIEVES Quadrant:** Orange accent (#F59E0B) - strategic goals

**Contradiction Indicators:**
- **Aligned (SAY = DO):** Green checkmark with subtle green glow
- **Weak Contradiction:** Yellow warning icon
- **Strong Contradiction:** Red alert icon with pulse animation

---

### Typography

**Fonts:**
- **Inter:** UI text (clean, readable, professional)
- **Fira Code:** Code blocks, file paths, technical content

**Hierarchy:**
- **H1 (32px Bold):** Page titles
- **H2 (24px Bold):** Section headers
- **H3 (18px Bold):** Card titles
- **Body (14px Regular):** Primary content
- **Small (12px Regular):** Annotations, timestamps

**Emphasis:**
- Bold for key terms (not overuse)
- Italic for quotes
- Mono for code, paths

---

### Spacing & Layout

**Grid:**
- 12-column responsive grid
- 16px gutter
- Max content width: 1200px (comfortable reading)

**Spacing Scale:**
- XS: 4px (tight spacing)
- S: 8px (related items)
- M: 16px (standard gap)
- L: 24px (section spacing)
- XL: 32px (major sections)
- XXL: 48px (page sections)

**Component Padding:**
- Cards: 24px
- Modals: 32px
- Page: 48px (top/bottom), 64px (sides)

---

### Elevation & Depth

**Shadows:**
- **SM:** Buttons, badges (2px blur)
- **MD:** Cards, dropdowns (8px blur)
- **LG:** Modals, popovers (16px blur)

**Use Cases:**
- Hover states: Increase shadow
- Active/focus: Blue outline (accessibility)
- Disabled: Reduce opacity to 40%

---

### Iconography

**Style:** Outline icons (Heroicons or Lucide)
**Size:** 20px default, 16px for inline, 24px for headers

**Key Icons:**
- 📄 File/document
- 🎯 Goal/target
- ✓ Success/checkmark
- ⚠️ Warning
- 🔍 Search/discover
- 🤖 AI/automation
- 📊 Data/analytics
- ⚙️ Settings
- 🔗 Link/connection
- ← → Navigation

---

## Multi-Agent Workflow Design (V2 Foundation)

### Overview

**Not in MVP, but design foundation laid today.**

**OpenAI Pattern:** Engineers manage 10-20 parallel AI threads (70% more output). Intake V2 will enable PMs to do the same—exploring 5 feature approaches simultaneously.

### V2 Vision: Parallel Exploration

```
┌─────────────────────────────────────────────────────────────┐
│  Exploring: Onboarding Optimization (5 Approaches)          │
│                                                             │
│  🤖 Coordinator Agent                            Status: Active│
│  Managing 5 specialist agents across parallel explorations │
│                                                             │
│  ┌───────────┬───────────┬───────────┬───────────┬────────┐│
│  │ Agent 1   │ Agent 2   │ Agent 3   │ Agent 4   │ Agent 5││
│  │ Mobile    │ Email     │ Onboarding│ Fraud     │ Speed  ││
│  │ Focus     │ Verify    │ Steps     │ Checks    │ Optim. ││
│  │           │           │           │           │        ││
│  │ ⏳ Working│ ✓ Complete│ ⏳ Working│ ⏳ Queued │ ⏳ Queue││
│  │           │           │           │           │        ││
│  │ Found: 2  │ Found: 1  │ Finding...│ Waiting...│ Wait...││
│  │ contradict│ solution  │           │           │        ││
│  │           │           │           │           │        ││
│  │ [Review]  │ [Review]  │ [Steer]   │ [Steer]   │ [Steer]││
│  └───────────┴───────────┴───────────┴───────────┴────────┘│
│                                                             │
│  Latest Update (2 sec ago):                                 │
│  Agent 1 detected contradiction: Mobile users abandon at    │
│  email verification (not connection). Exploring alternative.│
│                                                             │
│  [Synthesize Best Insights] ← When ready                   │
└─────────────────────────────────────────────────────────────┘
```

### MVP Design Decisions that Enable V2

**1. Card-Based Layout:**
- Today: 1 discovery card (vertical)
- V2: 5 discovery cards (horizontal grid)
- Same component, different layout

**2. Status Indicators:**
- Today: Single progress indicator
- V2: Multiple parallel progress indicators
- Same component system, scales up

**3. "Coordinator" Language:**
- Today: Single workflow called "Management Loop"
- V2: Coordinator agent manages specialists
- Language consistent

**4. Expandable Detail:**
- Today: Expand single discovery
- V2: Expand any of 5 parallel explorations
- Same interaction pattern

**5. Review/Steer Actions:**
- Today: Review single spec
- V2: Steer multiple explorations, review in parallel
- Same action vocabulary

### V2 Features (Not in MVP)

- ❌ **Parallel thread management**: Launch 5 explorations simultaneously
- ❌ **Live updates**: Agents discover new evidence while working
- ❌ **Cross-thread synthesis**: Merge best insights from 5 explorations → 1 spec
- ❌ **PM steering**: Approve/reject/redirect individual threads
- ❌ **Thread comparison view**: Side-by-side comparison of approaches

**Timeline:** V2 ships 12 months post-MVP launch

**Why this matters for MVP design:** Layout must accommodate future expansion without major redesign.

---

## Social Proof & Distribution Signals

### Overview

**Strategic Asset:** 840+ enterprise PM engagement (Microsoft, Meta, Amazon, NVIDIA, Gong, CrowdStrike)

This isn't just marketing—it's a competitive moat. Design must leverage this social proof.

### Where to Surface Social Proof

**1. Marketing/Landing Pages:**
```
┌─────────────────────────────────────────────────────────────┐
│  Join 840+ PMs from leading companies                       │
│  [Microsoft] [Meta] [Amazon] [NVIDIA] [Gong] [CrowdStrike] │
│                                                             │
│  "Intake collapsed our PRD process from 3 days to 90 sec"  │
│  — Sarah Chen, PM at FinFlow                               │
└─────────────────────────────────────────────────────────────┘
```

**2. In-App Activity Feed:**
```
┌─────────────────────────────────────────────────────────────┐
│  Activity                                                   │
│  • 23 PMs generated specs today                            │
│  • Sarah from Acme just shipped a feature you'd like       │
│  • Teams like yours are prioritizing mobile optimization   │
└─────────────────────────────────────────────────────────────┘
```

**3. Referral Attribution:**
```
┌─────────────────────────────────────────────────────────────┐
│  Welcome to Intake!                                         │
│  Sarah Chen from FinFlow recommended you join.              │
│  [Thank Sarah] [See what Sarah built]                      │
└─────────────────────────────────────────────────────────────┘
```

**4. Network Insights (V3 - Platform Phase):**
```
┌─────────────────────────────────────────────────────────────┐
│  💡 Insight: Teams like yours prioritize                   │
│  mobile optimization (68% of fintech PMs)                  │
│                                                             │
│  Say-vs-Do Pattern: Analytics features have                │
│  low adoption in your vertical (15% avg usage)             │
└─────────────────────────────────────────────────────────────┘
```

### Design Principles for Social Proof

- **Authentic, not salesy**: Show real usage, not generic testimonials
- **Privacy-respecting**: Anonymize when needed ("A PM from Microsoft" vs full name)
- **Value-driven**: Social proof reinforces product value, doesn't replace it
- **Progressive**: MVP shows static logos, V2 shows activity, V3 shows insights

---

## Information Architecture

### Navigation Structure (MVP)

```
Intake
├── Dashboard (Home)
│   ├── Your Specs
│   │   ├── Draft
│   │   ├── In Development
│   │   └── Shipped
│   └── Activity Feed
│
├── New Spec [+ CTA]
│   ├── Upload Data
│   ├── Discovery Results
│   ├── Spec Review
│   └── Commit to Git
│
├── Settings
│   ├── Connected Repositories
│   ├── Data Sources
│   └── Profile
│
└── Help
    ├── Getting Started
    ├── Video Walkthrough
    └── Contact Support
```

---

### Content Hierarchy (Spec Review Screen)

**Priority 1 (Above fold):**
- Spec title
- Confidence score
- Goal
- Success criteria (top 3)
- Primary CTA: "Commit to Git"

**Priority 2 (Scroll):**
- Constraints (with annotations)
- Context (auto-enriched)
- Evidence summary (3 examples)

**Priority 3 (Expandable/Links):**
- Full evidence chain
- Complete YAML
- Codebase discoveries
- Secondary actions (Regenerate, Download)

---

## Accessibility (WCAG 2.1 AA)

### Requirements

**Color Contrast:**
- Text: 4.5:1 minimum
- Large text (18px+): 3:1 minimum
- Interactive elements: 3:1 minimum

**Keyboard Navigation:**
- All interactive elements focusable (Tab order logical)
- Focus indicators visible (blue outline)
- Shortcuts: Escape to close modals, Enter to submit

**Screen Readers:**
- Semantic HTML (headings, landmarks, lists)
- Alt text for all icons/images
- ARIA labels for custom components
- Status announcements (spec generated, commit success)

**Visual:**
- Text resizable to 200% without loss of functionality
- No reliance on color alone (use icons + text)
- Minimum touch target: 44x44px

---

## Responsive Design Strategy

### MVP: Desktop-First

**Why:** Target users (PMs) primarily work on desktops/laptops.

**Breakpoints:**
- Desktop: 1440px (primary design)
- Laptop: 1280px (minor adjustments)
- Tablet: 768px (not supported in MVP)
- Mobile: 375px (not supported in MVP)

**Post-MVP:** Add responsive tablet/mobile views for:
- Dashboard (check specs on-the-go)
- Evidence viewing (reference during meetings)
- Spec reading (review on mobile)

**Not Mobile-Optimized:**
- Data upload (too complex for mobile)
- Spec editing (needs keyboard/mouse)
- Codebase discoveries (too much detail)

---

## Animation & Microinteractions

### Purpose

**Animations Should:**
- Provide feedback (button pressed, file uploaded)
- Show progress (discovery running, spec generating)
- Celebrate success (spec committed, feature shipped)
- Guide attention (new insights, important warnings)

**Animations Should NOT:**
- Slow down the experience (speed is a feature)
- Distract from content
- Trigger accessibility issues (motion sensitivity)

---

### Key Animations

#### 1. **Upload Progress**
- File drag: Highlight drop zone (blue border)
- File drop: Checkmark animation
- Upload: Progress bar fill (smooth)

**Duration:** 300ms transition, 1-5s upload

---

#### 2. **Discovery Progress**
- Stage transition: Fade in next stage
- Working indicator: Subtle pulse (not spinning)
- Completion: Checkmark slide-in

**Duration:** 500ms transitions

---

#### 3. **Spec Generation**
- Text streaming: Type-writer effect (fast)
- Section reveal: Stagger (50ms delay each)
- Auto-enrichment badge: Bounce-in

**Duration:** 1-2s total

---

#### 4. **Success Moments**
- Commit success: Confetti (subtle) + modal fade-in
- Discovery complete: Gentle scale-up on insights
- High confidence: Green glow on score

**Duration:** 800ms

---

#### 5. **Hover States**
- Buttons: Scale to 1.05 (100ms)
- Cards: Lift shadow (200ms)
- Links: Underline slide-in (150ms)

---

### Motion Preferences

**Respect `prefers-reduced-motion`:**
- Disable decorative animations
- Keep functional animations (progress, feedback)
- Use fade transitions instead of slides/scales

---

## Error Handling & Edge Cases

### Error States

#### 1. **Upload Errors**
**Scenarios:**
- File too large (>50MB)
- Unsupported format
- Network timeout

**UX:**
- Inline error message (red text)
- Suggested action ("Try a smaller file" or "Export as CSV")
- Option to skip and continue

---

#### 2. **GitHub Connection Errors**
**Scenarios:**
- OAuth canceled
- Permission denied
- Repository not found

**UX:**
- Modal with clear error message
- Retry button
- Link to troubleshooting docs
- Option to proceed without GitHub (manual context entry)

---

#### 3. **Discovery Failures**
**Scenarios:**
- No patterns found
- Contradictory signals
- Insufficient data

**UX:**
- Explanation: "We found conflicting signals..."
- Show what we found (raw data)
- Option to manually prioritize
- Suggestion: "Upload more interviews or clarify strategic brief"

---

#### 4. **Spec Generation Low Confidence**
**Scenarios:**
- Confidence < 70%
- Missing critical data
- Ambiguous goals

**UX:**
- Warning badge on spec (yellow)
- Explanation of what's missing
- Suggested improvements
- Option to regenerate with more context or edit manually

---

#### 5. **Git Commit Failures**
**Scenarios:**
- Branch already exists
- Permission denied (read-only repo)
- Network error

**UX:**
- Modal with error details
- Retry button
- Fallback: Download YAML file manually
- Support link

---

### Empty States

#### 1. **No Specs Yet**
```
┌─────────────────────────────────────┐
│         📋                          │
│                                     │
│     No specs yet!                   │
│                                     │
│  Create your first machine-         │
│  actionable spec in 5 minutes.      │
│                                     │
│     [+ Create First Spec]           │
└─────────────────────────────────────┘
```

---

#### 2. **No Data Sources Connected**
```
┌─────────────────────────────────────┐
│         🔗                          │
│                                     │
│   Connect your first data source    │
│                                     │
│  Upload interviews, tickets, or     │
│  analytics to get started.          │
│                                     │
│     [Upload Data]                   │
└─────────────────────────────────────┘
```

---

#### 3. **No Activity Yet**
```
┌─────────────────────────────────────┐
│  Activity feed will show here once  │
│  specs are committed and developed. │
└─────────────────────────────────────┘
```

---

### Loading States

**Best Practices:**
- Show progress percentage when available
- Use skeleton screens for content loading (avoid blank screens)
- Provide time estimates for long operations
- Allow cancellation when appropriate

---

## User Testing Plan

### Phase 1: Prototype Testing (Week 1-2)

**Goals:**
- Validate Sarah's flow (upload → discovery → review → commit)
- Test PM-native UX (can non-technical users complete tasks?)
- Identify confusion points

**Method:**
- **5 PM users** (mix: technical, non-technical)
- **Tasks:**
  1. Upload sample data (provided)
  2. Review discovery insights
  3. Edit and commit a spec
- **Observe:** Time to completion, hesitation points, questions asked

**Success Criteria:**
- 80% complete all tasks without help
- Average time < 10 minutes
- 4/5 users say "I'd use this"

---

### Phase 2: MVP Beta Testing (Week 3-6)

**Goals:**
- Validate real-world usage (with users' actual data)
- Test auto-enrichment accuracy (codebase scanning)
- Measure "aha moment" timing

**Method:**
- **20 PM beta users** (early adopters from target ICP)
- **Tasks:**
  1. Connect real GitHub repo
  2. Upload real customer interviews
  3. Generate 3+ specs over 2 weeks
- **Track:**
  - Specs generated per week
  - Specs committed to git
  - Developer clarifying questions (survey engineering after)
  - Time to first spec

**Success Criteria:**
- 80% generate 3+ specs in first week
- 70% commit at least 1 spec to git
- 60% report "fewer clarifying questions from engineering"
- Average time to first spec < 5 minutes

---

### Phase 3: Post-Launch Iteration (Ongoing)

**Methods:**
- **Session recordings** (Hotjar or similar) - identify drop-off points
- **User interviews** (weekly) - qualitative feedback
- **Analytics** (Mixpanel or similar) - track feature usage, completion rates
- **NPS surveys** (monthly) - "How likely are you to recommend Intake?"

**Metrics:**
- Screen drop-off rates (where do users abandon?)
- Feature adoption (% using evidence chain, codebase discoveries)
- Time-to-value (signup to first committed spec)
- Retention (% active after 30, 60, 90 days)

---

## Implementation Priorities

### Phase 1: Core MVP (Weeks 1-10 - Extended for BMAD)

**Week 1-2: Design System & Core Components**
- [ ] Color palette with BMAD quadrant colors (blue, green, purple, orange accents)
- [ ] Typography, spacing, elevation
- [ ] Core components (buttons, cards, badges, inputs)
- [ ] Upload zone component
- [ ] **NEW:** BMAD quadrant card component (most complex)
- [ ] **NEW:** Contradiction alert card component
- [ ] **NEW:** Management loop progress component

**Week 3-4: BMAD Visualization (Core Differentiator)**
- [ ] **NEW:** BMAD context building screen (4-quadrant animation)
- [ ] **NEW:** Opportunity review screen with BMAD summaries
- [ ] **NEW:** Contradiction deep dive modal
- [ ] Live progress states (loading, complete, contradiction detected)
- [ ] Confidence score visualization
- [ ] Time savings counter

**Week 5-6: Primary Flow Screens**
- [ ] Data upload screen (with management loop preview)
- [ ] Spec review screen (updated with BMAD evidence links)
- [ ] Git commit modal

**Week 7-8: Secondary Screens**
- [ ] Dashboard / home (with activity feed, social proof)
- [ ] Evidence chain viewer
- [ ] Codebase discoveries viewer
- [ ] **NEW:** Management loop explainer (educational)

**Week 9-10: Polish, Prototype & V2 Foundation**
- [ ] Animations (BMAD quadrant fills, contradiction pulse, management loop progress)
- [ ] Microinteractions (hover states, transitions)
- [ ] Interactive prototype (Figma)
- [ ] **NEW:** V2 multi-agent layout mockups (non-functional, for validation)
- [ ] Accessibility audit (WCAG 2.1 AA)
- [ ] User testing round 1

**Deliverables:**
- Figma file with all MVP screens + V2 vision mockups
- Interactive prototype (MVP flow)
- Design system documentation with BMAD components
- Component specifications for developers
- V2 design direction document

---

### Phase 2: Beta Refinements (Weeks 9-12)

Based on user testing feedback:
- [ ] Iterate on confusing interactions
- [ ] Add missing error states
- [ ] Improve empty states
- [ ] Optimize for speed (reduce clicks)

**Deliverables:**
- Updated Figma designs
- UX improvement report
- Beta testing insights document

---

### Phase 3: Post-Launch (Weeks 13+)

**Feature Additions (based on roadmap):**
- Settings screen (integrations, preferences)
- Spec diff viewer (version comparison)
- Search and filters (dashboard)
- Batch operations (generate multiple specs)

**Continuous:**
- Analytics review (monthly)
- User interviews (weekly)
- A/B testing (key flows)
- Design system evolution

---

## Handoff to Development

### Design Deliverables

**1. Figma Files:**
- **Design System page:** All colors, typography, spacing, components
- **Screens page:** All screens (organized by flow)
- **Prototype:** Interactive flow (upload → discovery → review → commit)
- **Specs page:** Component specs (dimensions, states, behaviors)

**2. Documentation:**
- **Component Library Guide:** How to use each component, variants
- **Interaction Patterns:** Inline editing, progressive disclosure, etc.
- **Responsive Breakpoints:** (MVP: desktop only, but document future needs)
- **Accessibility Requirements:** WCAG checklist, keyboard nav, ARIA labels

**3. Assets:**
- **Icons:** Exported SVGs (20px, 24px)
- **Illustrations:** Empty states, success moments (if custom)
- **Logo variants:** Full logo, icon-only, light/dark modes

**4. Design Tokens (for developers):**
```json
{
  "colors": {
    "primary-500": "#3B82F6",
    "primary-600": "#2563EB",
    "success-500": "#10B981",
    ...
  },
  "spacing": {
    "xs": "4px",
    "s": "8px",
    "m": "16px",
    ...
  },
  "typography": {
    "h1": { "size": "32px", "weight": "700", "lineHeight": "40px" },
    ...
  }
}
```

**5. User Flow Diagrams:**
- Primary flow (Sarah's MVP experience)
- Secondary flows (dashboard, evidence, discoveries)
- Error/edge case flows

---

### Developer Collaboration

**During Implementation:**
- **Daily standups:** Designer attends to answer questions
- **Weekly design reviews:** Review implemented screens vs. designs
- **Component approval:** Designer approves each component before moving on
- **Feedback loops:** Developers flag technical constraints early

**Quality Gates:**
- [ ] Pixel-perfect match (or documented deviations)
- [ ] All states implemented (default, hover, active, disabled, error)
- [ ] Responsive behavior (even if MVP is desktop-only)
- [ ] Accessibility checklist complete
- [ ] Animations match specs (duration, easing)

---

## Success Criteria for Design

### How We'll Know the UX Design is Successful

**User Testing Metrics:**
- **90% task completion** rate without help (upload → commit flow)
- **< 5 minutes** average time to first committed spec
- **< 2 hesitation points** per user (moments of confusion)
- **4.5/5 stars** average usability rating

**Post-Launch Metrics:**
- **70% retention** at 30 days (users return after first experience)
- **80% specs committed** (users don't abandon at review step)
- **< 10% support tickets** related to UI confusion
- **4.5+ NPS** from PM users

**Engineering Validation:**
- **Developer approval:** "Specs from Intake require 0-1 clarifying questions" (vs. baseline 10+)
- **Integration success:** Cursor can parse YAML specs without reformatting

**Business Validation:**
- **Time collapse validated:** PM work goes from hours to minutes
- **"I can't go back" moment:** 80%+ users say this in interviews
- **Word-of-mouth growth:** 40%+ signups from PM friend referrals

---

## Strategic UX Considerations

### Model-Agnostic Architecture (Competitive Advantage)

**Strategic Insight:** *"Build for where models are going, not where they are today. Models will eat your scaffolding for breakfast."* — OpenAI

**What This Means for UX:**
- **Never mention specific AI models** (Claude, GPT-4) in user-facing UI
- **Generic "AI-powered" language**: "Intake analyzes..." not "Claude analyzes..."
- **Provider flexibility messaging**: "Works with any AI provider" (future marketing)
- **Update-proof design**: UI doesn't break when we swap underlying models

**UI Language Guidelines:**
```
✅ GOOD:
- "AI-powered discovery"
- "Automatic analysis"
- "Intake found..."
- "Context encoding"

❌ AVOID:
- "Claude is analyzing..."
- "GPT-4 discovered..."
- "Powered by Anthropic"
- References to specific providers
```

**Why This Matters:**
- Competitors locked to single providers face strategic risk
- We benefit from provider competition (models improve → we improve)
- Future-proof: Can switch providers without confusing users

---

### Distribution Moat (Social Proof Strategy)

**Strategic Asset:** 840+ enterprise PM engagement = primary competitive moat

**UX Implications:**
- **Social proof must be prominent**: Not buried in footer
- **Company logos where permitted**: Microsoft, Meta, Amazon (with permission)
- **Activity feeds**: Show real usage ("23 PMs generated specs today")
- **Referral attribution**: "Sarah from FinFlow recommended you"
- **Network insights (V3)**: "Teams like yours prioritize..."

**First-Mover Urgency:**
- Public engagement alerts competitors (ProductBoard watching)
- Design must help us move FAST (MVP in 6 months)
- Category ownership requires speed: Ship before competitors react

**UI Opportunities:**
- Landing page: "Join 840+ PMs from Microsoft, Meta, Amazon..."
- Onboarding: "You were invited by [Name]"
- Dashboard: Activity feed with real (anonymized) usage
- Empty states: "Sarah from Acme just shipped a feature like this"

---

### Category Definition (Own the Language)

**Goal:** Make "Product Reasoning Infrastructure" synonymous with Intake

**UX Language Strategy:**
- **Use the term consistently**: "Product Reasoning Infrastructure" in headers, taglines
- **Define it visually**: Show the flow (Signals → Context Encoding → Specs → Execution)
- **Contrast with old paradigm**: ProductBoard = "Roadmaps for humans", Intake = "Reasoning for machines"
- **Educational approach**: Teach PMs what product reasoning means

**UI Placements:**
- Hero header: "Intake: Product Reasoning Infrastructure"
- Footer: "The first Product Reasoning Infrastructure"
- About page: "What is Product Reasoning?"
- Documentation: "Product reasoning vs product management"

---

### Competitive Positioning in UI

**Key Messages to Convey Through Design:**

**1. vs ProductBoard/Aha (Traditional PM Tools):**
- **They:** Human-readable dashboards
- **We:** Machine-actionable specs
- **Show:** Side-by-side JIRA ticket vs Intake spec (visual proof)

**2. vs Cursor (Developer Tools):**
- **They:** Developer UX (IDEs, terminals, git)
- **We:** PM-native UX (visual, drag-drop, no code)
- **Show:** Same output (machine-actionable), different interface

**3. vs ChatGPT/Claude (AI Tools):**
- **They:** One-off document generation
- **We:** Infrastructure with context persistence
- **Show:** BMAD triangulation (structure), evidence chains (traceability)

**UI Elements:**
- Comparison page on website (spec.yaml vs JIRA)
- "Why Intake?" page with competitive positioning
- Explainer video showcasing PM-native UX

---

### Designing for Speed (6-Month MVP Timeline)

**Time Pressure:** First-mover window closing (competitors react in 6-9 months)

**Design Decisions to Optimize Speed:**
- **Desktop-first ONLY** (no mobile responsive for MVP)
- **Component library reuse** (Tailwind UI, Shadcn, or similar)
- **Fewer custom illustrations** (use Heroicons/Lucide)
- **MVP screens only** (defer v2 screens)
- **Figma templates** (don't design from scratch)

**What We Can't Cut (Core Value):**
- BMAD 4-quadrant visualization (the differentiator)
- Contradiction detection UI (key feature)
- Codebase discoveries (auto-enrichment showcase)
- Evidence chains (trust building)

**Speed vs Quality Tradeoffs:**
- ✅ Reuse design system components (speed)
- ✅ Simple animations (speed)
- ✅ Desktop-only (speed)
- ❌ Don't cut BMAD visualization (quality = differentiation)
- ❌ Don't cut contradiction detection (quality = moat)

---

## Open Questions & Decisions Needed

### Design Decisions Requiring Product Input

**1. Spec Editing Depth:**
- **Question:** How much manual editing should we support in MVP?
- **Options:**
  - A) Inline editing only (simple text changes)
  - B) Full structured editor (reorder, add sections)
  - C) Hybrid: Inline for quick edits + "Advanced Editor" link
- **Recommendation:** C (balances speed with flexibility)

---

**2. GitHub Integration Depth:**
- **Question:** Should users see git history/branches in Intake UI, or just "commit" and done?
- **Options:**
  - A) Minimal: One-click commit, no git UI
  - B) Moderate: Show recent commits, link to GitHub
  - C) Full: Embedded git UI (branches, diffs, history)
- **Recommendation:** A for MVP (least complexity), B in v2.0

---

**3. Discovery Customization:**
- **Question:** Can users steer the discovery process, or is it fully automated?
- **Options:**
  - A) Fully automated (no user input)
  - B) Guided (user sets priorities: "focus on mobile issues")
  - C) Manual override (user can reject insights, flag false positives)
- **Recommendation:** A for MVP (simplicity), B in v2.0

---

**4. Evidence Depth:**
- **Question:** How much of the raw data (full interviews, tickets) should be accessible in-app?
- **Options:**
  - A) Summaries only (quotes, snippets)
  - B) Full access (read entire transcripts in modal)
  - C) External links (link to Modjo, Jira, Datadog)
- **Recommendation:** C for MVP (avoid content duplication), B in v2.0

---

**5. Multiplayer (Future):**
- **Question:** When do we add team collaboration features?
- **Timing:**
  - MVP: Single-player (Sarah works alone)
  - v2.0: Async collaboration (PM comments, engineering responds)
  - v3.0: Real-time (GitHub-style for PMs)
- **Recommendation:** Validate single-player value first, defer multiplayer to Phase 3

---

## Appendix: Design References

### Inspiration (What We Admire)

**1. Cursor (Developer Tool):**
- **Admire:** Clean, focused UI. AI suggestions feel integrated, not intrusive.
- **Avoid:** Too technical for non-technical PMs. Terminal-centric.

**2. Linear (Project Management):**
- **Admire:** Fast, keyboard-driven. Minimalist design. Excellent empty states.
- **Avoid:** Assumes technical fluency (shortcuts, command palette).

**3. Notion (Knowledge Management):**
- **Admire:** Inline editing everywhere. Progressive disclosure. Familiar UX.
- **Avoid:** Can feel overwhelming with too many options.

**4. Figma (Design Tool):**
- **Admire:** Real-time collaboration. Version history. Component-driven.
- **Avoid:** Complexity curve too steep for casual users.

**5. Stripe Dashboard:**
- **Admire:** Data-dense but readable. Clear visual hierarchy. Trust-building design (security, precision).
- **Avoid:** Corporate aesthetic (we want to feel more approachable).

---

### Competitive Analysis (PM Tools)

**ProductBoard:**
- **UX Strengths:** Familiar roadmap visualizations, feedback boards
- **UX Weaknesses:** Cluttered UI, too many features, slow workflows
- **Our Advantage:** Speed (90 seconds vs. hours), machine-actionable output

**Aha!:**
- **UX Strengths:** Strategy-first approach, visual roadmaps
- **UX Weaknesses:** Expensive, complex setup, no codebase awareness
- **Our Advantage:** Auto-enrichment, developer-friendly specs

**ProdPad:**
- **UX Strengths:** Lightweight, simple feedback capture
- **UX Weaknesses:** Manual prioritization, no AI, generic outputs
- **Our Advantage:** AI discovery, structured reasoning, git integration

**Key Insight:** All competitors feel like "dashboards for humans." We need to feel like "infrastructure for machines" (but designed for humans to use).

---

## Next Steps

### Immediate Actions (This Week)

**For Designer:**
1. [ ] Review this UPDATED plan with product team (align on BMAD visualization priority)
2. [ ] Set up Figma file structure with V2 vision page
3. [ ] Build design system with BMAD quadrant colors (blue, green, purple, orange accents)
4. [ ] Start core components: **BMAD quadrant card (PRIORITY #1)**, contradiction alert, management loop progress
5. [ ] Prototype BMAD 4-quadrant animation (critical for "aha moment")

**For Product Team:**
1. [ ] Answer open questions (spec editing depth, GitHub integration, contradiction override)
2. [ ] **NEW:** Provide sample BMAD data (15 interview quotes, Jira tickets, Datadog metrics, strategic brief)
3. [ ] **NEW:** Define contradiction detection thresholds (how strong = red alert vs yellow caution?)
4. [ ] Prioritize screens if timeline is tight (10 weeks realistic? Or cut scope?)
5. [ ] Connect designer with early PM users (especially those who commented in 840+ engagement)

**For Engineering:**
1. [ ] Review technical constraints (BMAD visualization feasibility?)
2. [ ] Confirm real-time progress per quadrant (4 parallel processes)
3. [ ] Discuss BMAD data structure (how to pass SAY, DO, TECHNICAL, BELIEVES to frontend?)
4. [ ] **NEW:** Multi-agent architecture implications (V2 = 12 months, but discuss now)
5. [ ] Design handoff format (Figma inspect? Design tokens? React components?)

---

### Weekly Milestones (Next 10 Weeks - Updated)

**Week 1:**
- [ ] Design system complete with BMAD colors
- [ ] **NEW:** BMAD quadrant card component (all states: loading, complete, contradiction)
- [ ] **NEW:** Contradiction alert card component
- [ ] **NEW:** Management loop progress component

**Week 2:**
- [ ] Upload zone, progress indicators, code blocks (standard components)
- [ ] Data upload screen with management loop preview

**Week 3:**
- [ ] **NEW:** BMAD context building screen (4-quadrant live animation)
- [ ] Quadrant fill sequences, contradiction detection

**Week 4:**
- [ ] **NEW:** Opportunity review screen (3-5 opportunities with BMAD summaries)
- [ ] **NEW:** Contradiction deep dive modal

**Week 5:**
- [ ] Spec review screen (updated with BMAD evidence links)
- [ ] Evidence chain viewer

**Week 6:**
- [ ] Git commit modal
- [ ] Dashboard / home with activity feed
- [ ] Codebase discoveries viewer

**Week 7:**
- [ ] Error states, empty states, loading states
- [ ] Social proof elements (company logos, activity feeds)

**Week 8:**
- [ ] Animations (BMAD fills, contradiction pulse, management loop progress)
- [ ] Microinteractions (hover, transitions)

**Week 9:**
- [ ] Interactive prototype (MVP flow complete)
- [ ] **NEW:** V2 multi-agent mockups (vision, non-functional)
- [ ] Accessibility audit

**Week 10:**
- [ ] User testing with 5-10 PMs (focus on BMAD comprehension)
- [ ] Iterate based on feedback
- [ ] Developer handoff (Figma + comprehensive docs)

---

### Long-Term Roadmap (Post-MVP)

**Q2 2026 (v2.0):**
- Settings screen (integration management)
- Spec diff viewer (version comparison)
- Search and filters (dashboard improvements)
- Automated integrations (Modjo API, Jira webhooks, Datadog live)

**Q3 2026 (v2.5):**
- Multiplayer (comments, reviews, approvals)
- Advanced discovery (hypothesis testing, A/B test recommendations)
- Mobile-responsive design (tablet + phone)

**Q4 2026 (v3.0 - Platform):**
- Public API (third-party integrations)
- Plugin marketplace (custom reasoning frameworks)
- Network effects (cross-customer insights, benchmarks)

---

## Conclusion

This UPDATED UX design plan provides a comprehensive roadmap from product brief to implemented designs, aligned with the latest strategic direction. The focus is on:

### Core Design Priorities

1. **Context Encoding Visualization (BMAD)** - The differentiator that makes our moat visible
2. **Say-vs-Do Contradiction Detection** - Prevent wasted engineering effort  
3. **Automated Management Loop** - Show how we compress 4-5 hours to 90 seconds
4. **PM-native simplicity** - Non-technical users become AI managers
5. **Speed as a feature** - 90 seconds to spec, 5 minutes including review
6. **Trust through transparency** - Evidence chains, codebase discoveries
7. **Model-agnostic positioning** - Never lock to single AI provider
8. **Distribution moat leverage** - 840+ PM engagement as trust signal

### Strategic Advantages Reflected in UX

**OpenAI Validation:**
- Management skills > coding skills (we automate the management loop)
- Context encoding > better prompts (BMAD triangulation is the structure)
- 70% more output when managing AI agents (our V2 vision)

**Competitive Moats:**
- BMAD visualization (unique to Intake, hard to copy)
- Say-vs-Do detection (requires data integration + reasoning)
- Codebase auto-enrichment (parsing infrastructure takes months)
- Evidence traceability (compliance value, engineering trust)
- 840+ PM network (distribution advantage)

**Design for the Future:**
- V2 multi-agent foundation laid in MVP (layout scales)
- Model-agnostic language (works with any AI provider)
- Framework-agnostic specs (works with any tech stack)
- Platform-ready architecture (API ecosystem, network effects)

### The MVP Flow (Updated)

**Upload signals → BMAD context building → Detect contradictions → Review opportunities → Generate spec → Review with evidence → Commit to git → Engineering executes**

**New screens (vs original plan):**
- ✅ BMAD context building (4-quadrant visualization)
- ✅ Contradiction deep dive (SAY vs DO comparison)
- ✅ Opportunity review (with BMAD summaries)
- ✅ Management loop progress (educational overlay)

**Timeline:** 10 weeks (extended from 8 to accommodate BMAD visualization)

### Critical Success Factors

**For "Aha Moment":**
- BMAD visualization must feel magical (auto-enrichment is the hook)
- Contradictions must be trustworthy (80% follow recommendation)
- Time savings must be obvious ("Saved: 4h 32min")

**For Category Ownership:**
- "Product Reasoning Infrastructure" language everywhere
- Visual comparison (spec.yaml vs JIRA) on website
- Social proof prominent (840+ PMs, company logos)

**For First-Mover Speed:**
- Desktop-only MVP (no mobile)
- Component reuse (Tailwind UI, Shadcn)
- Ship in 6 months (before competitors react)

### Next Step

**Build the BMAD quadrant card component first.** This is the visual manifestation of our core moat. Everything else can wait.

**Week 1 Priority:**
1. Design system with BMAD colors
2. BMAD 4-quadrant card (all states)
3. Contradiction alert card
4. Management loop progress indicator

---

**Questions? Feedback? Changes?**  
This plan is a living document. Update as we learn from users, engineering constraints, and market validation.

**The first-mover window is closing. Let's ship fast.** 🚀

**Let's build Product Reasoning Infrastructure.** Not just a PM tool—infrastructure for the AI-native era.

---

**Document Version:** 2.0 (Updated 2026-02-13)  
**Based on:** Product Brief 2026-02-13 (Latest)  
**Changes:** Added BMAD visualization, say-vs-do contradictions, management loop automation, multi-agent V2 foundation, strategic positioning, distribution moat leverage
