# UX Design Plan Changelog

**Date:** February 13, 2026  
**Version:** 2.0  
**Reason:** Updated to reflect major product brief changes

---

## Summary of Changes

The UX design plan has been comprehensively updated to reflect the latest product brief (v2.0, dated 2026-02-13). This update shifts Intake's positioning from "AI-native PM tool" to **"Product Reasoning Infrastructure"** with validation from OpenAI's transformation.

---

## Major Changes

### 1. New Core Positioning

**OLD:** "First AI-native product management infrastructure for machine clients"

**NEW:** "Product Reasoning Infrastructure—the context layer between scattered signals and AI execution"

**Why:** OpenAI validation (95% engineers managing AI agents, 70% more output) proves the pattern. 840+ enterprise PMs engaged (Microsoft, Meta, Amazon).

---

### 2. BMAD Triangulation as Primary Differentiator

**Added:** Complete BMAD visualization system

**What It Is:** 4-quadrant framework visualizing context encoding:
- **SAY** (customer interviews) 
- **DO** (behavior data)
- **TECHNICAL** (codebase auto-enrichment)
- **BELIEVES** (strategic goals)

**Why It Matters:** This is the visual manifestation of our core moat (Context Encoding Infrastructure).

**UX Impact:**
- New screen: "BMAD Context Building" (replaces generic "Discovery Progress")
- New component: BMAD 4-quadrant card (most complex component)
- New color strategy: Blue (SAY), Green (DO), Purple (TECHNICAL), Orange (BELIEVES)
- Contradiction detection between SAY and DO (red alerts)

---

### 3. Say-vs-Do Contradiction Detection

**Added:** First-class feature for detecting when customers SAY they want features they won't USE

**Why It Matters:** Prevents wasted engineering effort (core value proposition)

**UX Impact:**
- New screen: "Contradiction Deep Dive"
- New component: Contradiction Alert Card
- Red/yellow warning indicators
- Impact estimation ("Saves 2 weeks engineering time")
- Override capability with reasoning capture

---

### 4. Automated Management Loop

**Added:** Visualization of 5-step management workflow automation

**What It Is:** 
1. Brief → Loaded from BMAD (0 sec)
2. Dialogue → Contradictions surfaced (15 sec)
3. Investigation → Evidence chains built (30 sec)
4. Critique → Validation checks (20 sec)
5. Production → Spec generated (25 sec)

**Why It Matters:** Shows HOW Intake automates 4-5 hours of manual work → 90 seconds

**UX Impact:**
- New component: Management Loop Progress overlay
- Time savings prominent ("Saved: 4h 32min")
- Educational tooltips

---

### 5. Multi-Agent Workflows (V2 Vision)

**Added:** Design foundation for parallel exploration (not in MVP, but layout ready)

**What It Is:** PM explores 5 feature approaches simultaneously (mirrors OpenAI's 10-20 parallel threads)

**Timeline:** V2 ships 12 months post-MVP

**UX Impact:**
- Card-based layout scales from 1 to 5 explorations
- "Coordinator" language introduced
- Status indicators support multiple parallel threads
- V2 mockups included in design deliverables (vision, non-functional)

---

### 6. Social Proof & Distribution Moat

**Added:** 840+ enterprise PM engagement as competitive advantage

**Why It Matters:** Distribution is the primary moat in AI-native era

**UX Impact:**
- Company logos on landing page (Microsoft, Meta, Amazon, NVIDIA, Gong)
- Activity feed ("23 PMs generated specs today")
- Referral attribution ("Sarah from FinFlow recommended you")
- Network insights (V3 future: "Teams like yours prioritize...")

---

### 7. Model-Agnostic Positioning

**Added:** Strategic language guidelines to avoid locking to AI providers

**Why It Matters:** Competitors locked to single providers face risk; we benefit from provider competition

**UX Impact:**
- Never mention "Claude," "GPT-4," or specific models in UI
- Use "AI-powered," "Automatic analysis," "Intake found..."
- Future-proof: Can swap underlying models without confusing users

---

### 8. Category Definition Strategy

**Added:** "Product Reasoning Infrastructure" as category term

**Why It Matters:** First to own the language = category leadership

**UX Impact:**
- Term used consistently across UI
- Comparison pages (vs ProductBoard/Aha/Cursor)
- Educational content ("What is product reasoning?")
- Visual flow diagrams (Signals → Context Encoding → Specs → Execution)

---

## Updated Design Principles

**Added 3 new principles:**
1. **Context Encoding Made Visible** (BMAD as core moat)
2. **Automated Management Loop** (infrastructure, not DIY mastery)
3. **Say-vs-Do Contradictions as First-Class Feature**

**Updated 3 existing principles:**
4. **Social Proof & Distribution Signal** (840+ PM engagement)
5. **Design for Multi-Agent Future** (V2 ready)
6. **Model-Agnostic Positioning**

**Kept (with minor updates):**
7. PM-Native, Not Developer-Native
8. Speed as a Feature
9. Git Integration Without Git Knowledge

---

## New Screens Added

**MVP Screens (10 weeks total, extended from 8):**
1. Data Upload (updated with management loop preview)
2. **NEW:** BMAD Context Building (4-quadrant live animation)
3. **NEW:** Opportunity Review (with BMAD summaries)
4. **NEW:** Contradiction Deep Dive (SAY vs DO comparison)
5. Spec Review (updated with BMAD evidence links)
6. Git Commit Modal
7. Dashboard (updated with activity feed, social proof)
8. Evidence Chain Viewer
9. Codebase Discoveries Viewer

**V2 Vision Mockups (non-functional):**
- Multi-agent parallel exploration layout
- Coordinator + specialist agent cards
- Cross-thread synthesis interface

---

## New Components Added

**Priority Components:**
1. **BMAD Quadrant Card** (most complex, core differentiator)
   - 4-quadrant layout
   - Live progress per quadrant
   - Contradiction detection
   - Confidence score
   - Auto-enrichment badges

2. **Contradiction Alert Card**
   - SAY vs DO comparison
   - Impact estimation
   - Recommendation explanation
   - Override capability

3. **Management Loop Progress**
   - 5-step timeline
   - Time per step
   - Total time vs manual comparison
   - Expandable details

---

## Updated Color Strategy

**Added BMAD Quadrant Colors:**
- **Blue (#3B82F6):** SAY quadrant (customer voice)
- **Green (#10B981):** DO quadrant (behavior data)
- **Purple (#8B5CF6):** TECHNICAL quadrant (auto-enriched, AI magic)
- **Orange (#F59E0B):** BELIEVES quadrant (strategic goals)

**Purple as Brand Differentiator:**
- 🤖 Auto-enriched badges
- TECHNICAL quadrant highlights
- Codebase discoveries
- "Intake found this automatically" moments

---

## Updated Timeline

**OLD:** 8 weeks (MVP)

**NEW:** 10 weeks (MVP) + V2 vision mockups

**Reason:** BMAD visualization is complex and critical (can't rush the core differentiator)

**Week 1-2:** Design system + BMAD components (extended)  
**Week 3-4:** BMAD visualization screens (new)  
**Week 5-6:** Primary flow screens  
**Week 7-8:** Secondary screens + social proof elements  
**Week 9-10:** Polish, prototype, V2 mockups, user testing

---

## Strategic Additions

**Added Sections:**
- BMAD Triangulation Visualization (detailed specs)
- Multi-Agent Workflow Design (V2 foundation)
- Social Proof & Distribution Signals
- Strategic UX Considerations (model-agnostic, category definition)
- Competitive Positioning in UI

**Updated Sections:**
- Executive Summary (OpenAI validation, 840+ PMs)
- Design Principles (BMAD, contradictions, management loop)
- User Flows (BMAD context building integrated)
- Component Library (3 new priority components)
- Screen Inventory (4 new screens)
- Implementation Priorities (10 weeks, reordered)
- Conclusion (strategic advantages, category ownership)

---

## Success Metrics Updates

**Added Metrics:**
- 70% understand what BMAD means by end of first session
- "Aha moment" when TECHNICAL quadrant fills with auto-discoveries
- 80% follow contradiction recommendations (don't override)
- 5% false positive rate on contradictions

**Updated Metrics:**
- 85% users watch BMAD progress (don't navigate away)
- 60% users view at least one contradiction
- 40% explore multiple opportunities before choosing

---

## Key Takeaways for Design Team

### Must-Haves (Can't Cut)
1. ✅ BMAD 4-quadrant visualization (the differentiator)
2. ✅ Contradiction detection UI (key feature, moat)
3. ✅ Codebase auto-enrichment showcase (purple badges)
4. ✅ Evidence chains (trust building)
5. ✅ Management loop progress (educational, shows value)

### Can Defer or Simplify
- ❌ Mobile responsive (desktop-only for MVP)
- ❌ Custom illustrations (use Heroicons/Lucide)
- ❌ V2 multi-agent (vision mockups only, non-functional)
- ❌ Rich animations (simple is fine)
- ❌ Advanced settings (defer to v2.0)

### Strategic Priorities
1. **Speed to market:** 6-month window before competitors react
2. **Category ownership:** "Product Reasoning Infrastructure" everywhere
3. **Social proof:** 840+ PM engagement visible
4. **Distribution moat:** Referral flows, activity feeds, community feel
5. **Future-proof:** Model-agnostic language, V2 foundation

---

## Next Actions

### Immediate (This Week)
1. Review updated design plan with product team
2. **BUILD BMAD QUADRANT CARD FIRST** (priority #1)
3. Set up Figma with BMAD color system
4. Prototype 4-quadrant fill animation
5. Get sample BMAD data from product team

### Week 1-2
1. Complete design system with BMAD colors
2. Build 3 new priority components (BMAD, contradiction, management loop)
3. Design BMAD context building screen
4. Create contradiction alert variations

### Week 3-4
1. Opportunity review screen
2. Contradiction deep dive modal
3. Complete primary flow with BMAD integration
4. User testing on BMAD comprehension

---

## Questions for Product Team

**Priority Questions (answer ASAP):**
1. What are contradiction detection thresholds? (Red alert vs yellow caution)
2. Can we show real company logos? (Microsoft, Meta, etc. - need permission)
3. What's the sample BMAD data we can use for realistic mockups?
4. Is 10-week timeline acceptable? (vs original 8 weeks)
5. Should we prototype multi-agent V2 now, or defer to later?

**Secondary Questions:**
1. How much can PMs override contradictions? (Full control or guided?)
2. What's the management loop educational strategy? (Tooltips? Video? Help docs?)
3. Do we show model names anywhere in UI? (Leaning NO per model-agnostic strategy)
4. What's the referral tracking mechanism? (How do we attribute "Sarah invited you"?)

---

## Document Changes Summary

- **Lines changed:** ~1,500 lines
- **New sections:** 5 major sections added
- **Updated sections:** 8 sections substantially revised
- **New components:** 3 priority components specified
- **New screens:** 4 MVP screens added
- **Timeline:** Extended from 8 to 10 weeks
- **Strategic additions:** Model-agnostic, distribution moat, category definition

---

**Status:** ✅ Design plan fully updated and aligned with product brief v2.0

**Next Step:** Review with product team, get approval on BMAD visualization approach, then start building.

**Urgency:** First-mover window closing in 6-9 months. Design + build in 6 months total.

**Let's ship.** 🚀
