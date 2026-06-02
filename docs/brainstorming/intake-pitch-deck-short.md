---
title: "Intake: Product Reasoning Infrastructure"
---

# Intake: Product Reasoning Infrastructure
**From Scattered Signals to Executable Specs in 90 Seconds**

---

## Slide 1: The Pattern Is Proven

### At OpenAI: Engineers → Managers of AI Agents

- **95%** of engineers use Codex to manage AI fleets
- **70% more PRs** opened by shifting from coding to context + steering
- **10-20 parallel threads** managed simultaneously
- **100% AI-written codebases** maintained through better context

> *"Engineers are becoming tech leads... It literally feels like we're wizards casting spells."*
> — Sherwin Woo, Head of Engineering, OpenAI API Platform

**Key Insight:** Success requires **management skills, not coding skills.** The primary lever is **context.**

---

## Slide 2: PMs Are Next (And They're Ready)

### 840+ Enterprise PMs Engaged

**Microsoft • Meta • Amazon • NVIDIA • Gong • CyberArk • Palo Alto**

**Three Behaviors We're Seeing:**

1. **Technical PMs building "Product OS"**
   - Custom Cursor commands, shipped products in 2 weeks
   - Pattern matches OpenAI: Context + steering → 10x output

2. **Non-technical PMs mastering "management loop"**
   - Brief → Dialogue → Investigation → Critique → Production
   - Works brilliantly, but takes **4-5 hours per artifact**

3. **Most PMs stuck**
   - "Started Claude, hasn't improved workflow"
   - Missing: Management framework + context encoding

**The Gap:** No infrastructure automating what successful users do manually.

---

## Slide 3: The Problem

### Current Tools Don't Encode Context

| Tool | What's Missing |
|------|----------------|
| **ProductBoard/Aha** | Human dashboards, no context encoding |
| **ChatGPT/Claude** | No context persistence or evidence chains |
| **Cursor DIY** | Works if technical, no PM reasoning framework |

> *"Most agent failures stem from underspecification or lack of tribal knowledge."*
> — OpenAI Head of Engineering

**What Works:** PMs manually encoding context through management loops (4-5 hours per artifact)

**The Opportunity:** Make context encoding **infrastructure, not a task.**

---

## Slide 4: The Solution

### Intake = Automated Product Reasoning

```
Scattered Signals → Context Encoding → AI Reasoning → Executable Specs → Ship
                    (BMAD Framework)    (Management Loop)  (90 seconds)
```

**Three Core Capabilities:**

1. **Context Encoding (BMAD Triangulation)**
   - Automatically triangulates: Customer SAY vs. DO vs. Technical POSSIBLE vs. Strategic BELIEVES
   - Detects contradictions: "Say advanced filters, use only 2" → Don't over-build

2. **Automated Management Loop**
   - Brief → Dialogue → Investigation → Critique → Production
   - **Manual: 4-5 hours | Intake: 90 seconds**

3. **Machine-Actionable Specs**
   - Not human PRDs, executable YAML for AI agents
   - Includes evidence chains: Every decision linked to source

---

## Slide 5: How It Works (Example)

**Customer Say:** "We need advanced filtering"  
**Customer Do:** 80% use only 2 filters (Datadog)  
**Technical:** FilterService.ts supports 12 filters (GitHub)  
**Strategic:** Q2 goal = reduce time-to-value

**Intake Output (90 seconds):**
```yaml
goal: Reduce time-to-value (Q2 OKR)

recommendation: Simple filter UI + "Advanced" toggle
  - Default: 2 most-used filters (visible)
  - Toggle: Expand to show all 12 filters
  - Don't rebuild FilterService (already supports it)

evidence:
  customer_say: "Advanced filtering" (Modjo #47)
  customer_do: 80% use ≤2 filters (Datadog query)
  technical: FilterService.ts line 234 (GitHub)
  strategic: Q2 goal = reduce TTL by 15% (Jira OKR-23)
```

**Result:** Cursor reads this → Implements correctly → Ships fast.

---

## Slide 6: Market Traction

### Distribution Advantage: 840+ Enterprise PM Comments

**Quality Over Quantity:**
- **Enterprise:** Microsoft, Meta, Amazon, Intel, NVIDIA
- **B2B SaaS (ICP):** Gong, Guesty, monday.com, Wix, JFrog
- **Cybersecurity:** CyberArk, Palo Alto, CrowdStrike, Checkmarx

**Conversion Math:**
- 840 comments → **8K-42K PMs** saw post
- 1% conversion → **80-420 customers** from ONE post
- At $69/month → **$66K-$350K ARR** potential

**Market Size:**
- TAM: **$6.9B-$21.2B** PM software market
- SAM: **100K-250K PMs** globally (B2B SaaS focus)
- Early adopters: Cybersecurity (compliance) + B2B SaaS (speed)

---

## Slide 7: Why We Win

### Three Unfair Advantages

**1. Context Encoding Infrastructure**
- BMAD triangulation (SAY vs. DO vs. POSSIBLE vs. BELIEVES)
- Automatic contradiction detection
- Integration layer: Modjo, Datadog, GitHub, Jira

**2. Evidence Traceability**
- Every decision → Verifiable source
- Compliance value (cybersecurity cares)
- Engineering trust ("Show me the data" → Already embedded)

**3. Automated Management Loop**
- What RevOps leaders do manually → Built-in
- Non-technical users get expert results
- Management skills > Technical skills

**Bonus: Future-Proof Architecture**
- **Model agnostic:** Works with Claude, GPT-4, Gemini, future models
- **Framework agnostic:** Supports any tech stack
- **Multi-agent ready:** V2 = 10x exploration speed (OpenAI pattern)

---

## Slide 8: Competition

| Who | Advantage | Gap | Time to Compete |
|-----|-----------|-----|-----------------|
| **ProductBoard/Aha** | Established market | No machine-actionable output | 18-24 months |
| **Cursor** | Developer love | PM reasoning framework missing | Unlikely (not their focus) |
| **ChatGPT/Claude** | Used by all PMs | No infrastructure | 12-18 months (new product) |
| **New Startups** | None | None | 6-12 months |

**Our Moat:** Distribution (840 PMs) + Context Encoding + Evidence Traceability

**First-Mover Window:** **6-9 months** before incumbents react.

---

## Slide 9: Business Model

### Pricing: $39-$99/PM/month

- **Starter:** $39/month (individual, basic integrations)
- **Pro:** $69/month (teams, advanced integrations)
- **Enterprise:** $99+/month (compliance, SSO, audit logs)

**Revenue Targets:**
- **Year 1:** 500 customers → **$830K ARR**
- **Year 2:** 2,000 customers → **$3.3M ARR**
- **Year 3:** 5,000 customers → **$12.4M ARR**

**GTM Strategy:**
- **Bottom-up:** Technical PM "tiger teams" (840 commenters)
- **Top-down:** Executive pitch (productivity + compliance)
- **Content-led:** "How [Company] ships 10x faster" case studies

---

## Slide 10: The Ask

### Seeking [Amount] to Own the Category

**Use of Funds:**
- **60% Product:** Ship MVP in 6 months
  - Context encoding engine (BMAD)
  - Core integrations (Modjo, Jira, GitHub, Datadog)
  - Management loop automation
  - Model/framework agnostic architecture
  
- **30% GTM:** Leverage distribution (840+ PMs)
  - Content marketing & case studies
  - Technical PM early adopter program
  - Cybersecurity vertical pilot
  
- **10% Team:** Key hires (PM, Engineer, GTM lead)

**Success Metrics (12 Months):**
- ✅ 500 paying customers ($830K ARR)
- ✅ 10+ enterprise pilots
- ✅ Category leadership: "Product Reasoning Infrastructure"
- ✅ Competitor response (validates market)

---

## The Transformation Is Happening

**At OpenAI:** Engineers → Managers of AI Agents (70% more output)

**In Product Management:** PMs → Managers of AI Reasoning (10x faster specs)

**Intake is the infrastructure that makes it possible.**

---

**Contact:** [Your Info]  
**Demo:** [Link]

*Built on validated pattern: Management > Technical. Context > Prompts. Infrastructure > Tools.*
