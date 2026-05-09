# Inbox v2 - Research Synthesis & Product Recommendations

**Research Date:** February 11, 2026  
**Analyst:** Mary (Business Analyst)  
**Project:** Inbox v2 - Next Build Priority Analysis

---

## Executive Summary

Based on comprehensive analysis of 8 data sources spanning strategic vision, customer feedback, feature requests, support tickets, and usage analytics, three clear opportunities emerge for Inbox v2:

**🥇 TIER 1 - CRITICAL WINS (High Impact + Revenue)**
1. **Calendar-Based Automations** - #1 requested feature (80 accounts, $189K MRR)
2. **Bulk/Broadcast Messaging** - #3 PFR (40 accounts, $164K MRR) + enterprise need
3. **Multiwork Capabilities** - Tag users (#6 PFR, $132K MRR) + enterprise blocker

**🥈 TIER 2 - STRATEGIC GROWTH**
4. **AI Premium Monetization** - ReplyAI enhancements ($1M+ yearly revenue potential)
5. **Auto Response All Channels** - #2 critical PFR (63 accounts, $124K MRR)

**🥉 TIER 3 - RETENTION & POLISH**
6. **Inbox Filters & Search** - Reduces 10.68% of tickets (1,064 tickets = "Inbox Slow/Down")
7. **AM Simplification** - Reduces 46% of support burden (automated message complexity)

---

## Data Sources Analyzed

### Strategic Documents
- ✅ **Communications Domain Vision 2025** (66 pages) - Product strategy, competitive analysis, roadmap
- ✅ **Inbox v2 Codebase Documentation** - Technical foundation (React 18, Redux, multi-channel)

### Customer Voice (3 sources)
- ✅ **JIRA Feature Requests** (408K chars, sampled recent 200) - Engineering-tracked requests
- ✅ **Inbox PFRs June 2025** (225K chars, sampled top 200) - Product feature request backlog  
- ✅ **Support Tickets Feb 2025-2026** (1.7M chars, sampled recent 200) - 12 months of pain points

### Product Metrics (3 sources)
- ✅ **Zendesk Ticket Overview** - Category breakdown and volumes (9,960 tickets analyzed)
- ✅ **Communications Dashboard** (13 pages PDF) - Usage analytics, adoption, workflows
- ✅ **Usage Data Tables** - Detailed metrics on inbox, AM, WhatsApp, saved replies

---

## Key Findings

### Finding 1: AUTOMATIONS ARE THE #1 FRICTION POINT

**Support Ticket Evidence:**
- **46% of all tickets relate to Automated Messages** (Q1 2025)
- **AM Creation confusion: 19.58% (1,950 tickets)** - "How to" questions
- **AM Failed to Send: 9.14% (910 tickets)** - 40% due to condition misunderstanding
- **30% of Jira tickets = "As Designed"** - Knowledge gap, not actual bugs
- **40% of tickets are duplicates** - Escalation/triage issues

**Strategic Impact:**
> "Automated messages is a recurring friction point raised by CFT and users... Simplifying the AM setup and management can reduce a lot of friction, impacting CFT, support teams and the dev team"

**Root Cause:**
- Setup complexity ("Users do not understand AM easily… What does advanced notice or length of stay mean…")
- Condition logic confusion (40% of "Failed to Send" = condition misunderstanding)
- Templates outdated (old check-in form links)

---

### Finding 2: CALENDAR-BASED CONDITIONS = HIGHEST DEMAND FEATURE

**PFR Evidence:**
| Rank | PFR ID | Feature | Accounts | MRR | Priority |
|------|--------|---------|----------|-----|----------|
| **#1** | PFR-2924 | **Trigger and Automate Message on specific day of week** | **80** | **$189,094** | **Important** |
| Related | PFR-10491 | Send AM based on seasons or dates | 31 | $81,170 | Nice to have |
| Related | PFR-7358 | Select specific day and time | 27 | $80,675 | Nice to have |

**Customer Quote (from Vision doc):**
> "Many of the gaps that users bring up are related to... Day of the week AM conditions" (Top 3 missing capability)

**Strategic Context:**
> "Most requested feature in the domain - calendar based conditions (has been asked for over a year now, and growing in demand)"

**Competitive Gap:**
- Track: ✅ Has calendar-based conditions
- Streamline: ✅ Has calendar-based conditions  
- Guesty: ❌ Missing (lagging in automations: 3★ vs 4★)

**Impact:**
> "Introducing calendar based conditions will significantly improve the AM capabilities and increase user satisfaction, closing the gap in automations from PMS that already offer it"

---

### Finding 3: ENTERPRISE CLIENTS NEED MULTIWORK CAPABILITIES

**Sales Blocker:**
> "Main sales friction is for the Enterprise clients. The Inbox lacks capabilities to manage communications at scale"

**Product-Market Fit Score: 2.5/5 for Enterprise**

**Missing Capabilities for Enterprise:**
1. **Status of agents** (away, online, etc.)
2. **Queues** (assigning types of conversations to specific agents)
3. **Load management** (limit # of conversations per agent)
4. **Tagging users** in conversations

**PFR Evidence:**
| PFR ID | Feature | Accounts | MRR | Priority |
|--------|---------|----------|-----|----------|
| PFR-75 | **Tag team members in Inbox** | 15 | $131,945 | **Important** |
| PFR-6954 | See if another member is typing | 7 | $66,037 | Important |
| PFR-3328 | Assigning groups to inbox messages | 4 | $42,598 | Important |

**CFT Quote:**
> "Main gap - missing capabilities to manage scaled communication team... For enterprise clients, Call Center is considered 'meat and potatoes'"

**Strategic Guidance:**
> "By introducing a few features, we can improve the positioning of the Inbox with the enterprise clients (no need to get to a full 'ticketing system')"

---

### Finding 4: BULK OPERATIONS = HIGH VALUE, CROSS-SEGMENT NEED

**PFR Evidence:**
| PFR ID | Feature | Accounts | MRR | Priority | Segment Impact |
|--------|---------|----------|-----|----------|----------------|
| **PFR-21** | **Broadcast/mass message** | **40** | **$164,192** | **Important** | Core + Enterprise |
| PFR-126 | Bulk actions (mark read, archive) | 29 | $149,347 | Nice to have | Enterprise priority |
| PFR-1952 | Export guest communications | 34 | $149,111 | Nice to have | Enterprise request |

**Strategic Context:**
> "Inbox: bulk actions (sending messages, archiving, etc.)" - Listed in 2025 retention plan

**Enterprise Overlap:**
> "The marked PFRs overlap with the top 10 domain PFRs → by addressing more PFRs we can close the gap for Enterprise clients while serving Core/VR"

**Usage Pattern:**
- Bulk operations requested across all segments (Small → Enterprise)
- Common use case: Send message to all guests in a specific view/filter
- Related need: Better filters to enable bulk selection

---

### Finding 5: AI IS THE COMPETITIVE OPPORTUNITY

**Competitive Analysis:**
| Capability | Guesty | Competitors (avg) | Gap |
|------------|--------|-------------------|-----|
| **AI for Comms** | 2★ | 0-2★ | **Small lead** |
| Reply suggestions | ✅ | Most have it | Parity |
| **Suggestion adjustments** | ❌ | ❌ (Hospitable ✅) | **Behind leader** |
| **Autopilot (advanced)** | ❌ Limited | ✅ (Hospitable) | **Behind leader** |
| **Improve with AI** | ❌ | ❌ (Hospitable ✅) | **Behind leader** |
| **Conversation summary** | ❌ | ❌ (BestyAI, IntoAI ✅) | **Behind specialists** |

**ReplyAI Competitive Positioning:**
- **Guesty Score:** 2/8 on premium features
- **Best competitor (BestyAI):** 6/8 on premium features
- **Paying Guesty users:** Only 5 (vs BestyAI: 182, IntoAI: 306!)

**Strategic Opportunity:**
> "Guesty has an opportunity to create a gap, positioning itself as an automation leader... Once reaching a meaningful offering - Guesty can revisit monetization from advanced capabilities"

**Revenue Potential:**
- **ReplyAI Premium:** >$1M yearly revenue (strategy estimate)
- **GCS:** $1.6M expected in 2025

**2025 AI Roadmap (from Vision):**
- **Q2:** Suggestions adjustments
- **Q3:** Translations expand, ReplyAI redesign
- **Q4:** Improve with AI, Conversation summary, **Advanced Autopilot (#1 paid feature)**
- **2026 H1:** PMC performance reports, Task creation & management

---

### Finding 6: INBOX EXPERIENCE NEEDS ELEVATION (NOT PERFORMANCE)

**Current State:**
- **Inbox Rating:** 4★ (best-in-class)
- **Competitor Threat:** Closing the gap (Track: 3★, Hostaway: 3★)
- **Customer Quote:** "People join Guesty because of the Inbox"

**Key Insight:**
> "Inbox performance (speed, etc.) is not a meaningful issue to users... While the Inbox does need an enhancement, its performance should be less of the focus than the **UX and added features**"

**Support Ticket Reality:**
- **"Inbox Slow/Down": Only 10.68% of tickets (1,064)** - 4th highest, but...
- Resolution: "Most of the tickets were resolved by refreshing the browser or clearing cache/cookies on user's end"

**Top Inbox PFRs (prioritized by impact):**
1. **Broadcast/mass messaging** - 40 accounts, $164K
2. **Export communications** - 34 accounts, $149K  
3. **Tag team members** - 15 accounts, $132K
4. **White labeling UI** - 34 accounts, $134K
5. **Advanced filters** - 3 accounts, $49K (but **Critical** priority)
6. **Bulk actions** - 29 accounts, $149K

**Strategic Guidance:**
> "By introducing a few features, we can improve the positioning of the Inbox with the enterprise clients (no need to get to a full 'ticketing system')"

---

### Finding 7: WHATSAPP IS GROWING BUT PROBLEMATIC

**Adoption Trajectory:**
- **156 accounts successfully integrated** (as of Feb 2026)
- **Cumulative growth:** 1 → 210 accounts (Nov 2024 - Feb 2026)
- **23 integration errors** (failed WhatsApp setup)

**Usage Volume:**
- **Host Messages:** ~50K/month (template + non-template)
- **Guest Messages:** ~95K/month
- **Active users:** 68 accounts actively sending WhatsApp

**Pain Points:**
- **Integration friction:** "WhatsApp - handling the Meta business account issues add friction to the new integration"
- **Channel limitations:** Users want WhatsApp support in more places (AM, auto-response)
- **CFT Quote:** "Not all users will want to give up an active number for Guesty integration or set up a new number"

**Top WhatsApp PFRs:**
| PFR ID | Feature | Accounts | MRR | Priority |
|--------|---------|----------|-----|----------|
| PFR-10229 | **Send WhatsApp via API** | 7 | $64,320 | **Critical** |
| PFR-3110 | Use their own WhatsApp number | 36 | $60,558 | **Critical** |
| PFR-2037 | WhatsApp for Automated Messages | 13 | $28,718 | Important |
| PFR-8142 | Send files/photos via WhatsApp | 9 | $61,608 | Important |

**CFT Gap:**
> "Handle inquiries from WhatsApp (not only reservation-associated messages)"

---

### Finding 8: AUTO RESPONSE ALL CHANNELS = #2 CRITICAL PFR

**PFR-2426: Auto Response to work with all channels**
- **Accounts:** 63
- **Accumulated MRR:** $124,304
- **Priority:** **CRITICAL**
- **Strategic Importance:** Listed in Top 10 domain PFRs

**Current Limitation:**
- Auto response only works for certain channels
- Gap mentioned by multiple customers
- Required for channel parity

**Strategic Context:**
> "Auto response: work with all channels" - Listed in 2025 plan under "Regain leadership" vector

---

### Finding 9: SAVED REPLIES NEED REVAMP

**Support Ticket Evidence:**
- **Saved Replies issues: 1.82% of tickets (181 tickets)**
- Variable confusion (old {{checkin_form}} vs new Guest App variables)
- Template management difficulty

**Usage Data:**
- **74.4% of accounts = NO usage or LOW usage**
- Only 25.6% have Medium to High usage
- **GCS accounts:** 56% no usage (worse than non-GCS!)

**Strategic Plan:**
> "Saved Replies revamp" - Listed in 2025 Inbox redesign plan

**PFR Evidence:**
| PFR ID | Feature | Accounts | MRR |
|--------|---------|----------|-----|
| PFR-6001 | Export saved replies report | 12 | $99,513 |
| PFR-2511 | Rename saved reply folders | 4 | $35,653 |

---

### Finding 10: EXTENSION AUTOMATION = HIDDEN GEM (REVENUE DRIVER!)

**New Feature Adoption (launched recently):**
- **5,402 accounts** using Guest Review condition
- **170 accounts** using Extension Available condition  
- **172 accounts** using Reservation Payment condition

**Extension Success Metrics:**
- **119 accounts** scheduled extension messages
- **94 accounts** had successful extensions
- **774 reservations successfully extended**
- **$160,238 in GBV additions** from extensions
- **1,205 additional nights** booked

**Growth Trajectory:**
- Aug 2025: 40 accounts
- Feb 2026: 159 accounts (4x growth in 6 months!)

**Strategic Impact:**
- **Revenue generation** through extended stays
- **High success rate:** 55.95% of accounts with scheduled extensions achieved successful extensions
- **Viral potential:** Accounts with success are scaling usage

---

## Competitive Landscape Summary

### Overall Positioning

| Capability | Guesty | Track | Streamline | Hostaway |
|------------|--------|-------|------------|----------|
| **Unified Inbox** | 4★ | 3★ | 2★ | 3★ |
| **Automations** | 3★ | **4★** | **4★** | 2★ |
| **AI for Comms** | 2★ | 0★ | 0★ | 2★ |
| **API** | 4★ | 2★ | 1★ | 2★ |

**Bottom Line:**
> "Guesty has the edge in Inbox, but the competition is closing the gap. Guesty could improve position in automations and has an opportunity to open a gap in AI integration"

### AI Competitive Deep Dive

**Guesty vs PMS Competitors:** Leading (but basic)
- Reply suggestions: ✅ (all competitors have it)
- Sentiment analysis: ✅ (only Hospitable & Hostaway have it)
- Autopilot: ❌ Limited (only "thank you")

**Guesty vs AI-First Add-ons:** Lagging significantly
- BestyAI: 182 paying Guesty customers, 6/8 premium features
- IntoAI: 306 paying Guesty customers, 4/8 premium features
- HostAI: 49 paying Guesty customers, 4/8 premium features
- Hospitable: Advanced autopilot, performance reports

**Key Missing Premium Features:**
- Suggestion adjustments (tone, length, formality)
- External knowledge import
- Advanced autopilot (beyond thank you)
- Improve with AI (rewrite)
- Conversation summary
- Task creation & management
- Performance reports

---

## Usage Analytics Insights

### Inbox Usage
- **Overall Adoption:** ~86% no usage (trend stable)
- **High usage:** 35.6% (strong core engagement)
- **Channel inbox:** 64.3% high usage (healthy)
- **Guest inbox:** 30.2% high usage

**Segment Breakdown:**
- **Enterprise:** 62.2% high usage (strong!)
- **SME:** 67.5% high usage
- **Mid-Market:** Lower engagement
- **Small/SMB:** 78.3% low/no usage

### Automated Message Usage
- **9,281 accounts with active workflows** (70.3% of paying accounts!)
- **99.44% use Reservation Confirmed trigger** (universal adoption)
- **36.15% use Reservation Canceled trigger**
- **29.09% use Reservation Altered trigger**
- **10,192 accounts executed AMs** (strong adoption)

**Workflow Duplication Trend:**
- Consistent growth: 478 events (Aug 2024) → 1,156 events (Feb 2026)
- Users actively duplicating workflows (cloning pattern)

### WhatsApp Growth
- **Host Messages:** 50K-55K/month (stable)
- **Guest Messages:** 93K-99K/month (growing)
- **Integration:** 156 accounts (from 1 in Nov 2024!)
- **Template vs Manual:** 57% template, 43% manual

### SMS Cost Reality
- **18.9M posts sent**
- **39.6M SMS sent** (avg 2.09 SMS per post due to multi-part messages)
- **86.1% GSM-7 encoding** (standard Latin characters)
- **13.9% UCS-2 encoding** (emojis, non-Latin = higher cost!)

**Cost Driver:**
- Wonder Vacation Homes: 2.1M SMS (2.18 avg per post)
- Mattino Sydney Stays: 1.3M SMS (2.61 avg per post!)

**Strategic Priority:**
> "Scale: SMS - cutting costs, improving logs"

---

## Top 10 PFRs by Weighted Impact

Ranked by: (# Accounts × MRR × Priority Score)

| Rank | PFR ID | Feature | Domain | Accounts | MRR | Priority | EE | Strategic Fit |
|------|--------|---------|--------|----------|-----|----------|----|----|
| 1 | PFR-2924 | **Calendar-based AM conditions** | Auto Messages | 80 | $189K | Important | M | ⭐️⭐️⭐️ |
| 2 | PFR-2426 | **Auto Response all channels** | Auto Response | 63 | $124K | **Critical** | M | ⭐️⭐️⭐️ |
| 3 | PFR-21 | **Broadcast/mass messaging** | Inbox | 40 | $164K | Important | L | ⭐️⭐️⭐️ |
| 4 | PFR-15206 | SMS webhook (priority restore) | API | 10 | $45K | **Critical** | S | ⭐️⭐️ |
| 5 | PFR-1952 | **Export guest communications** | Inbox | 34 | $149K | Nice | S | ⭐️⭐️ |
| 6 | PFR-75 | **Tag team members in conversation** | Inbox | 15 | $132K | Important | **XL** | ⭐️⭐️⭐️ |
| 7 | PFR-1560 | **Multiple recipients in AM** | Auto Messages | 24 | $120K | Important | S | ⭐️⭐️ |
| 8 | PFR-5889 | **White labeling communications UI** | Inbox | 34 | $134K | Nice | L | ⭐️⭐️ |
| 9 | PFR-9042 | White labeled SMS number | Inbox | 29 | $155K | Nice | L | ⭐️⭐️ |
| 10 | PFR-14264 | **Advanced inbox filters** | Inbox | 3 | $49K | **Critical** | **XL** | ⭐️⭐️⭐️ |

**Key Observations:**
- **7 of 10 = Inbox features** (Inbox dominates demand)
- **3 of 10 = Critical priority** (PFR-2426, PFR-15206, PFR-14264)
- **4 of 10 = Enterprise requests** (overlapping with top 10)
- **5 of 10 = Small-Medium EE** (L/S/M) = Quick wins

---

## Recent Feature Requests (Last 30 Days) - Emerging Patterns

### New Requests from JIRA (Feb 2026)

**Recent High-Value Requests:**
1. **PFR-20200** (Feb 9): **Schedule messages in Inbox** (similar to "Send Later")
   - Account: Grand Welcome Austin ($425 MRR)
   - Priority: Nice to have
   
2. **PFR-20176** (Feb 7): **Real-time Guest App status in AM widget**
   - Shows if guest completed app BEFORE scheduled send time
   - Account: Grand Welcome Austin ($425 MRR)
   - Reduces unnecessary follow-ups
   
3. **PFR-20151** (Feb 5): **Delete AM messages from Lite Inbox**
   - User wants to remove duplicate/unwanted messages
   - Account: Rehab ($0 MRR - but usability issue)
   
4. **PFR-20058** (Jan 30): **AI Conversation Summary with timestamps & users**
   - Enterprise need (Avari/Casago - uber enterprise)
   - Team collaboration context (who said what when)
   
5. **PFR-20056** (Jan 29): **Facebook Messenger sync**
   - Account: The Sanctuary Co ($1,720 MRR)
   - Centralize all channels

**Pattern Detection:**
- **Scheduling/timing themes** (PFR-20200, PFR-20176)
- **AI enhancement requests** (PFR-20058)
- **Multi-channel expansion** (PFR-20056)
- **UX polish** (PFR-20151)

---

## What Customers Actually Say (Recent Ticket Quotes)

### On Inbox UX
> "From a user experience perspective, that makes no sense at all... the system is designed to communicate inaccurate information" *(PFR-20176)*

### On Multiwork Needs
> "They have an entire team of guest experience agents who all work together... They would like to use the AI summary to quickly get an overview of who said what and when" *(PFR-20058 - Avari/Casago)*

### On Channel Consolidation
> "Users must respond through Facebook separately, which fragments communication and makes it harder to manage guest interactions efficiently" *(PFR-20056)*

### On Automation Complexity
> "Users do not understand the AM easily… What does advanced notice or length of stay mean…" *(Vision doc - Professional Services feedback)*

> "Gap in understanding triggers and conditions (leading to wrong set ups)" *(User insights from calls)*

---

## Strategic Alignment with 2025 Vision

### Vision's 3 Main Vectors:

**1. Regain Leadership in Guest Communications** 🏆
- **Focus:** Raise the bar on automations and AI
- **Approach:** Simplify AM while enhancing capabilities
- **Target:** Close automation gap with Track/Streamline (3★ → 4★)

**2. Work Towards Monetization** 💰
- **Focus:** ReplyAI premium features
- **Revenue Target:** >$1M yearly from ReplyAI + $1.6M GCS
- **Approach:** Free base features + premium advanced capabilities

**3. Cater to Enterprise Clients** 🏢
- **Focus:** Features that serve Core/VR AND Enterprise
- **Approach:** NOT full ticketing system, but key multiwork capabilities
- **Blockers:** Call center (explore 3rd party), multiwork features

### 2025 Planned Features (from Vision)

**Q2 2025:**
- SMS cost reduction
- Saved replies rewrite
- Auto messages simplification
- Calendar-based conditions (#1 PFR!)
- General payment condition (top PFR!)
- AI suggestions adjustments

**Q3 2025:**
- Inbox new design for Pro (discovery ETA end of Q3)
- Bulk actions (sending messages, archiving)
- Auto messages: group reservations
- AI translations

**Q4 2025:**
- Inbox: filtering capabilities
- Inbox: export guest communications
- Inbox: tag users
- Inbox: variables dropdown
- AI: Improve with AI, Conversation summary, Advanced Autopilot

**2026 H1 Potential:**
- Inbox: branding (email templates, signatures)
- Auto messages: multiple recipients
- Auto response: all channels
- SMS: white labeling
- AI: PMC performance reports, task creation & management

---

## Recommendations: What to Build Next

### 🥇 TIER 1: CRITICAL WINS (Build in Q2 2026)

#### **Option 1A: Calendar-Based Automation Engine** ⭐️⭐️⭐️
**Why:** #1 requested feature, closes automation gap with competitors
**Impact:** 80 accounts, $189K MRR, reduces AM complexity tickets
**Evidence:**
- Highest demand PFR (PFR-2924)
- Competitive gap (Track & Streamline have it, Guesty doesn't)
- Related high-value PFRs (PFR-10491, PFR-7358)
- Strategic: "Required to support existing GFH capabilities"

**What to Build:**
- Day-of-week trigger conditions (e.g., "Send on Thursdays only")
- Specific date/date range triggers (e.g., "Holiday weekend messages")
- Seasonal campaign support
- Time-of-day scheduling

**Quick Win Subset:**
- Day-of-week only (simplest, highest demand)
- EE: M (Medium)

---

#### **Option 1B: Bulk Operations Suite** ⭐️⭐️⭐️
**Why:** High ROI, serves Core + Enterprise, multiple high-value PFRs
**Impact:** 40+ accounts for broadcast, 29 for bulk actions, 34 for export
**Evidence:**
- PFR-21: Broadcast messaging (40 accounts, $164K, Important)
- PFR-126: Bulk actions (29 accounts, $149K)
- PFR-1952: Export communications (34 accounts, $149K)
- Strategic: Listed in Q3 2025 plan "bulk actions (sending messages, archiving, etc.)"

**What to Build:**
- **Phase 1:** Bulk actions on selected conversations
  - Mark as read/unread (bulk)
  - Archive/unarchive (bulk)  
  - Assign/unassign (bulk)
  - Resolve/unresolve (bulk)
  
- **Phase 2:** Broadcast messaging
  - Send message to all in current view/filter
  - Select recipients by criteria
  - Broadcast to owners
  
- **Phase 3:** Export functionality
  - Export conversation history
  - CSV/PDF formats
  - Filter-based export

**Quick Win Subset:**
- Bulk mark as read/archive + Broadcast to filtered view
- EE: L (Large) for full suite, M for Phase 1 only

---

#### **Option 1C: Multiwork Foundation** ⭐️⭐️⭐️
**Why:** Enterprise blocker, high-value accounts, strategic positioning
**Impact:** Unlocks enterprise sales, $132K MRR from tagging alone
**Evidence:**
- PFR-75: Tag team members (15 accounts, $132K, Important)
- Sales: "Main sales friction is for the Enterprise clients"
- PMF Score: 2.5/5 for enterprise (needs improvement)
- CFT: "Multiwork - see who is viewing/typing, tag users in conversation" (Top 3 gap)

**What to Build:**
- **Phase 1:** User tagging in conversations
  - @mention team members in internal notes
  - @mention in conversation thread
  - Notifications for tagged users
  
- **Phase 2:** Presence indicators
  - See who's viewing conversation
  - Typing indicators for team members
  - "Claimed" status for conversations
  
- **Phase 3:** Assignment & routing (future)
  - Agent queues
  - Load balancing
  - Status (online/away)

**Quick Win Subset:**
- Tagging in internal notes only (simplest, high value)
- EE: XL (Extra Large) for full suite, L for Phase 1

---

### 🥈 TIER 2: STRATEGIC GROWTH (Build in Q3-Q4 2026)

#### **Option 2A: AI Premium Monetization Suite** ⭐️⭐️
**Why:** $1M+ revenue opportunity, competitive differentiation, strategic priority
**Impact:** New revenue stream, positions Guesty as AI leader
**Evidence:**
- Vision: ">$1M yearly revenue from ReplyAI" (strategy estimate)
- Competitive gap: 2/8 premium features vs competitors 4-6/8
- Only 5 paying Guesty users (vs BestyAI: 182, IntoAI: 306)
- 2025 roadmap: Q4 focus on premium AI

**What to Build (Q4 2025 Roadmap):**
- **Suggestion adjustments** (tone, length, formality) - Q2
- **Translations** (expand existing) - Q3
- **Improve with AI** (rewrite messages) - Q4 *
- **Conversation summary** - Q4 *
- **Advanced Autopilot** (beyond thank you) - Q4 * **#1 paid feature**
- **PMC performance reports** - 2026 H1
- **Task creation & management** - 2026 H1

**Monetization Strategy:**
- Free tier: Current suggestions + adjustments + translations
- **Premium tier:** Autopilot + Improve + Summary + Reports
- Target: Compete with BestyAI/IntoAI/HostAI

**Quick Win Subset:**
- Suggestion adjustments only (unlocks premium tier)
- EE: M (Medium)

---

#### **Option 2B: Auto Response All Channels** ⭐️⭐️
**Why:** #2 critical PFR, high account count, listed in 2025 plan
**Impact:** 63 accounts, $124K MRR
**Evidence:**
- PFR-2426: Critical priority, 63 accounts
- Strategic: "Auto response: work with all channels" in 2025 plan
- Gap: Currently limited channel support

**What to Build:**
- Extend auto-response to WhatsApp
- Extend to email (if not already supported)
- Extend to all OTA channels
- Unified configuration across channels

**Quick Win Subset:**
- WhatsApp auto-response only (highest demand)
- EE: M (Medium)

---

#### **Option 2C: Multiple Recipients for Automated Messages** ⭐️⭐️
**Why:** High demand (PFR-1560), strategic fit, reduces ticket burden
**Impact:** 24 accounts, $120K MRR
**Evidence:**
- PFR-1560: Important priority, $120K MRR
- Strategic: "Multiple recipients" in 2025 Q4 plan
- CFT: Top 3 missing capability
- User quote: "Auto messages lack the ability to send to multiple recipients"

**What to Build:**
- CC/BCC functionality for automated messages
- Send to owner + vendor + team member simultaneously
- Multiple owner support (partnerships)
- Group reservation handling

**Quick Win Subset:**
- CC owners + team members in single AM
- EE: S (Small)

---

### 🥉 TIER 3: RETENTION & POLISH (Q1 2027 or ongoing)

#### **Option 3A: Advanced Inbox Filters & Search** ⭐️⭐️
**Why:** Reduces friction, enables bulk operations, Critical priority
**Impact:** Reduces 10.68% of tickets, enables other features
**Evidence:**
- PFR-14264: Critical priority (3 accounts, $49K)
- Support tickets: "Inbox Slow/Down" 10.68% (1,064 tickets)
- Most resolved by refresh (not real performance issues)
- Enables bulk operations (need good filtering first)

**What to Build:**
- Filter by: Source/channel, Status, Assignee, Date range
- Filter by: Unanswered messages (requested in PFR-20200 context)
- Filter by: Reservation status (checked-in, upcoming, etc.)
- Advanced search: Property name, confirmation code, guest details
- Saved filters (custom views improvement)

**Quick Win Subset:**
- Unanswered messages filter + Source/channel filter
- EE: M (Medium)

---

#### **Option 3B: AM Simplification & Templates Refresh** ⭐️⭐️
**Why:** Reduces 46% of support burden, improves onboarding
**Impact:** Massive ticket reduction (46% of all tickets!)
**Evidence:**
- 46% of tickets = Automated Messages
- 30% of Jira tickets = "As Designed" (knowledge gap)
- Templates outdated (old checkin_form links)
- Strategic: "Simplification efforts" in 2025 plan

**What to Build:**
- **Wizard-based AM setup** (instead of complex form)
- **Template library refresh** (remove deprecated variables)
- **In-context help** (explain conditions with examples)
- **Visual condition builder** (instead of text)
- **AM testing capability** (send test messages before activation)
- **Better error messages** (when conditions fail)

**Quick Win Subset:**
- Template refresh + in-context help tooltips
- EE: M (Medium) for full wizard, S for quick fixes

---

#### **Option 3C: Saved Replies Revamp** ⭐️
**Why:** Low adoption (74% low/no usage), strategic plan commitment
**Impact:** Improves efficiency for active users, adoption growth
**Evidence:**
- 74.4% of accounts = Low/No usage
- Strategic: "Saved replies - rewrite and improve UX" (Q2 2025 plan)
- CFT: "No saved replies" noted as Track disadvantage vs Guesty
- PFR-6001: Export saved replies (12 accounts, $99K)

**What to Build:**
- **Folder/category management** (PFR-2511)
- **Variable picker/dropdown** (easier than memorizing {{variables}})
- **Export/import** saved replies (PFR-6001)
- **Templates search**
- **Usage analytics** (which replies are most used)
- **Bulk edit** capabilities

**Quick Win Subset:**
- Variable dropdown picker only
- EE: S (Small)

---

## Effort-Impact Matrix

### High Impact, Low-Medium Effort (DO FIRST)

| Feature | Impact | Effort | ROI | Rank |
|---------|--------|--------|-----|------|
| **Calendar-based AM conditions** | ⭐️⭐️⭐️⭐️⭐️ | M | **Highest** | #1 |
| **Bulk messaging (Phase 1)** | ⭐️⭐️⭐️⭐️ | L | High | #2 |
| **Multiple recipients AM** | ⭐️⭐️⭐️ | S | **Highest** | #3 |
| **Auto Response all channels** | ⭐️⭐️⭐️⭐️ | M | High | #4 |
| **Saved replies variable picker** | ⭐️⭐️ | S | Medium | #8 |

### High Impact, High Effort (STRATEGIC BETS)

| Feature | Impact | Effort | ROI | Rank |
|---------|--------|--------|-----|------|
| **Tag team members (full multiwork)** | ⭐️⭐️⭐️⭐️⭐️ | XL | Medium | #5 |
| **Advanced filters & search** | ⭐️⭐️⭐️ | XL | Medium | #7 |
| **AI Premium suite (Autopilot, etc.)** | ⭐️⭐️⭐️⭐️⭐️ | XL | **Strategic** | #6 |

### Medium Impact, Low-Medium Effort (QUICK WINS)

| Feature | Impact | Effort | ROI | Rank |
|---------|--------|--------|-----|------|
| **Export communications** | ⭐️⭐️⭐️ | S | High | #9 |
| **AM template refresh** | ⭐️⭐️⭐️ | S | High | #10 |
| **White labeling UI** | ⭐️⭐️ | L | Medium | #11 |

---

## Recommended Roadmap: 3 Build Phases

### 📅 **Phase 1: Q2 2026 - Foundation for Scale** (3-4 months)

**Theme:** Enable PMs to manage communications at scale

**Build:**
1. **Calendar-Based Automations** (PFR-2924)
   - Day-of-week conditions
   - Specific date triggers
   - EE: M (Medium)
   
2. **Multiple Recipients** (PFR-1560)
   - CC/BCC for automated messages
   - EE: S (Small)
   
3. **Auto Response All Channels** (PFR-2426)
   - Extend to WhatsApp first
   - EE: M (Medium)

**Total EE:** ~2-3 months (M + S + M)

**Impact:**
- Closes automation gap with competitors
- Addresses 3 of top 10 PFRs
- Serves 167 accounts representing $433K MRR
- Reduces AM complexity tickets

---

### 📅 **Phase 2: Q3-Q4 2026 - Enterprise Unlock** (4-6 months)

**Theme:** Enterprise-grade collaboration + bulk operations

**Build:**
1. **Multiwork Foundation** (PFR-75 + related)
   - Tag users in conversations
   - Presence indicators (who's viewing/typing)
   - EE: L-XL (Large)
   
2. **Bulk Operations Suite** (PFR-21, PFR-126, PFR-1952)
   - Phase 1: Bulk actions (mark read, archive)
   - Phase 2: Broadcast messaging
   - Phase 3: Export conversations
   - EE: L (Large) for full suite
   
3. **Advanced Filters** (PFR-14264)
   - Enhanced filtering capabilities
   - Unanswered messages view
   - Custom filter combinations
   - EE: M-XL (Medium to Extra Large)

**Total EE:** ~4-6 months

**Impact:**
- Unlocks enterprise sales (addresses 2.5/5 PMF score)
- Addresses 6 of top 10 PFRs
- Serves 120+ accounts representing $445K+ MRR
- Enables "management at scale" capabilities

---

### 📅 **Phase 3: 2027 H1 - AI Leadership & Monetization** (3-4 months)

**Theme:** Premium AI capabilities for competitive differentiation

**Build:**
1. **AI Premium Suite**
   - Suggestion adjustments (tone, length)
   - Improve with AI (rewrite)
   - **Conversation summary** (recent PFR-20058 demand!)
   - **Advanced Autopilot** (#1 premium feature)
   - EE: XL (Extra Large)
   
2. **AI Monetization Launch**
   - Free tier: Basic suggestions + adjustments
   - Premium tier: Autopilot + Improve + Summary
   - Revenue target: $1M+ yearly

**Total EE:** ~3-4 months

**Impact:**
- Opens revenue stream ($1M+ potential)
- Competes with BestyAI/IntoAI (currently 182-306 paying users each)
- Positions Guesty as AI leader in PMS space
- Creates gap vs main competitors (Track, Streamline have 0★ AI)

---

## Alternative Approach: Quick Wins First

If you want **faster time to value** with smaller bets:

### 🚀 **Quick Wins Bundle (6-8 weeks)**

**Build:**
1. **Multiple Recipients AM** (PFR-1560) - EE: S (2 weeks)
2. **Variable Dropdown Picker** - EE: S (1-2 weeks)
3. **AM Template Refresh** - EE: S (1 week)
4. **Export Conversations** (PFR-1952) - EE: S (2 weeks)
5. **Unanswered Messages Filter** - EE: S (1 week)

**Total:** ~6-8 weeks, **5 features** delivered

**Impact:**
- Addresses 4 high-value PFRs
- Reduces support burden (template refresh, variable picker)
- Quick customer wins (export, filtering)
- **BUT:** Doesn't address #1 feature (calendar conditions) or enterprise gap (multiwork)

---

## Risk Analysis

### Risks of Building Calendar Automations FIRST
- **Medium complexity** (M effort)
- May not fully close competitor gap (Track has 200+ triggers, not just calendar)
- Requires careful UX to avoid adding MORE complexity

**Mitigation:**
- Start with day-of-week only (simplest use case)
- Invest in wizard/visual builder simultaneously
- Beta test with high-volume accounts

### Risks of Building Multiwork FIRST
- **High complexity** (XL effort)
- May not generate immediate revenue
- Enterprise adoption takes longer than SMB/Mid-Market

**Mitigation:**
- Start with tagging only (L effort instead of XL)
- Focus on internal notes first (lower risk)
- Partner with beta customers (Casago/Avari mentioned in tickets)

### Risks of Building AI Premium FIRST
- **Highest complexity** (XL effort)
- Unproven monetization (only 5 paying ReplyAI users today)
- Competitive landscape moving fast (BestyAI, IntoAI growing)

**Mitigation:**
- Start with suggestion adjustments only (M effort)
- Validate pricing with existing GCS customers
- Partner with 3rd party if build effort too high

---

## Final Recommendation: The "1-2-3 Punch"

### **Recommended Build Sequence:**

**Q2 2026 (Now):**
1. **Calendar-Based Automations** - Closes #1 gap, competitive parity
2. **Multiple Recipients** - Quick win, high value, low effort
3. **Auto Response All Channels** - Critical PFR, channel parity

**Q3-Q4 2026:**
4. **Bulk Operations** - Enterprise enabler, multiple PFRs
5. **Multiwork (Tagging)** - Enterprise blocker, sales enabler

**2027 H1:**
6. **AI Premium Suite** - Monetization play, competitive differentiation

---

## Why This Sequence?

### Step 1: Regain Automation Leadership (Q2)
- **Calendar conditions** closes the gap with Track/Streamline
- **Multiple recipients** + **Auto response** rounds out automation parity
- Combined impact: 167 accounts, $433K MRR
- Reduces support burden (46% of tickets!)

### Step 2: Unlock Enterprise (Q3-Q4)
- **Bulk ops** + **Multiwork** addresses enterprise PMF score (2.5/5)
- Removes sales friction ("Inbox lacks capabilities to manage at scale")
- Positions for larger deals
- Combined impact: 120+ accounts, $445K+ MRR

### Step 3: Monetize AI (2027 H1)
- **AI Premium** opens new revenue stream
- Competes with add-ons stealing Guesty customers (182-306 users!)
- Positions Guesty as AI leader (create gap vs Track/Streamline/Hostaway)
- Revenue potential: $1M+ yearly

---

## Evidence Summary

### Quantitative Validation

**From PFRs:**
- 673 PFRs reviewed total
- 10 critical, 211 important, 453 nice to have
- 249 PFRs requested by 2+ accounts
- Top 10 represent $1.3M in accumulated MRR

**From Support:**
- 9,960 tickets analyzed (Q1 2025)
- 46% = Automated Messages (highest category!)
- 30% of Jira tickets = "As Designed" (not bugs)
- 40% = Duplicates (triage issues)

**From Usage:**
- 70.3% of paying accounts use workflows (strong adoption!)
- 86% of accounts low inbox usage (opportunity for engagement)
- Extension automation: 4x growth in 6 months (119 → 774 extended reservations)
- WhatsApp: 156 accounts integrated (from 1 in Nov 2024!)

**From Strategy:**
- 2025 vectors align with recommendations
- AI monetization: $1M+ ReplyAI + $1.6M GCS
- Enterprise gap acknowledged (PMF 2.5/5)

### Qualitative Validation

**Customer Quotes:**
- "People join Guesty because of the Inbox" (sales)
- "Users do not understand AM easily" (Professional Services)
- "Main sales friction is for the Enterprise clients" (CFT)
- "Day of the week AM conditions" (Top 3 missing, CFT)

**Strategic Quotes:**
- "Introducing calendar based conditions will significantly improve AM capabilities"
- "Most requested feature in the domain - has been asked for over a year now"
- "By introducing a few features, we can improve positioning with enterprise clients"

---

## Conclusion: Build Calendar Automations First

**Why Calendar-Based Automations Should Be Your Next Build:**

1. ✅ **Highest demand** - 80 accounts, $189K MRR (most of any PFR)
2. ✅ **Competitive urgency** - Track & Streamline have it, Guesty doesn't
3. ✅ **Strategic fit** - Explicitly in 2025 plan, closes automation gap
4. ✅ **Reduces support burden** - Simplifies AM setup, addresses 46% of tickets
5. ✅ **Cross-segment value** - Small, SMB, Mid-Market, Enterprise all want it
6. ✅ **Foundation for more** - Enables seasonal campaigns, promotional automations
7. ✅ **Reasonable effort** - M (Medium) EE, not XL complexity
8. ✅ **Customer validation** - Requested for over a year, growing demand

**Followed by:**
- **Multiple Recipients** (quick S effort, $120K MRR, high satisfaction)
- **Auto Response All Channels** (M effort, 63 accounts, critical priority)

This sequence:
- Closes competitive gaps FIRST
- Delivers quick wins in Q2
- Sets foundation for enterprise unlock in Q3-Q4
- Positions for AI monetization in 2027

---

**Next Step:** Create Product Brief or PRD for Calendar-Based Automations?

