---
stepsCompleted: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
inputDocuments:
  - /Users/yair.cohen/Documents/GitHub/BMAD-METHOD/docs/inbox-v2-documentation/product-brief-calendar-automations-2026-02-11.md
  - /Users/yair.cohen/Documents/GitHub/BMAD-METHOD/docs/inbox-v2-documentation/research-synthesis-2026-02-11.md
  - /Users/yair.cohen/Documents/GitHub/BMAD-METHOD/docs/inbox-v2-documentation/project-overview.md
  - /Users/yair.cohen/Documents/GitHub/BMAD-METHOD/docs/inbox-v2-documentation/index.md
  - /Users/yair.cohen/Downloads/Communications Domain Vision 2025 (2).pdf
briefCount: 1
researchCount: 1
projectDocsCount: 2
workflowType: 'prd'
classification:
  projectType: 'web_app'
  domain: 'general'
  complexity: 'medium'
  projectContext: 'brownfield'
  scopeNotes: 'Automated Messages only, internal scheduling, real-time triggers'
---

# Product Requirements Document - Calendar-Based Automations for Inbox v2

**Author:** Yair Cohen  
**Date:** 2026-02-11

## Executive Summary

**Product Vision:**  
Calendar-Based Automations is an automation scheduling engine that enables property managers to trigger operational messages based on calendar patterns (day-of-week, time-of-day, date ranges) rather than reservation events. This closes a critical competitive gap with Track and Streamline while eliminating 400+ hours of manual weekly work across the customer base.

**Target Users:**  
80 mid-market accounts ($189K MRR) managing 50-200 properties who currently spend 2+ hours weekly manually activating/deactivating recurring operational messages (trash reminders, pool service, lawn care alerts) because existing Automated Messages require reservations to trigger.

**Core Problem:**  
Property managers are trapped in unsustainable manual workflows at scale. They log in weekly to activate "Trash Day Reminder" on Wednesday, deactivate it Thursday, repeat indefinitely. At 70+ properties this operational overhead becomes untenable. Support receives 2,860+ automation complexity tickets annually, with 40% caused by customers fighting reservation-based conditions when they simply need "every Thursday at 8am."

**Core Solution:**  
Calendar-Based Automation Engine enables "set it and forget it" scheduling:
- **Day-of-week triggers:** "Send every Thursday" or "Weekdays only"
- **Time-of-day scheduling:** "8:00 AM property local time"
- **Date range activation:** "June 1 - August 31 annually" for seasonal operations
- **Combine with reservations:** Calendar AND reservation conditions (additive, not replacement)
- **Real-time execution:** Trigger evaluation every 60 seconds, <60s fire latency

**Success Threshold:**  
50% adoption (40 of 80 accounts) within 3 months, 99.9% trigger firing accuracy, 400+ hours saved weekly, 40% reduction in "AM Failed to Send" support tickets, zero disruption to existing workflows. MVP timeline: 6-8 weeks.

**Strategic Impact:**  
Restores competitive parity with Track/Streamline (who already offer this), prevents $189K MRR churn, reduces support burden significantly, and unlocks mid-market growth by removing operational scalability ceiling.

---

## Success Criteria

### User Success

**Primary Success Indicator:**
- **90% of mid-market accounts (50-200 properties) create at least one calendar-based workflow within 60 days of launch**
- **Target users:** 80 accounts representing $189K MRR (the ones who requested this)

**Behavioral Change:**
- **400+ hours saved weekly across customer base** (eliminating manual activate/deactivate cycles)
- **Average 2 hours/week saved per property manager** with 70 properties
- **"Aha!" moment:** First Thursday morning when trash reminder auto-sends without PM intervention

**Adoption Pattern:**
- **Primary use case:** Day-of-week operational messages (trash, pool, lawn reminders)
- **Success threshold:** Users creating 3+ recurring workflows (indicates replacing manual patterns)
- **Workflow cleanliness:** Reduction in duplicate message creation (no more 7-message hacks for weekday logic)

### Business Success

**3-Month Post-Launch:**
- **50% adoption rate** among the 80 requesting accounts (40 accounts actively using calendar automations)
- **20% reduction in AM complexity tickets** (from 2,860 annually → 2,288)
- **Competitive positioning:** Feature parity announcement closes Track/Streamline gap

**12-Month Post-Launch:**
- **80% adoption rate** among target accounts (64 of 80 accounts)
- **40% reduction in "AM Failed to Send" tickets** (from 910 → 546 annually) - condition confusion eliminated
- **MRR retention:** $189K MRR retained (zero churn from the 80 requesting accounts)
- **Expansion:** Feature becomes standard selling point for mid-market prospects

**Revenue Impact:**
- **Churn prevention:** Retain $189K MRR from accounts waiting for this
- **Support cost reduction:** 1,142 fewer tickets annually (2,860 × 40%) = significant support hour savings
- **Competitive win:** Removes "missing feature" objection in mid-market sales cycles

### Technical Success

**Trigger Accuracy:**
- **99.9% of scheduled messages fire within 60 seconds of target time**
- **Zero false triggers** (messages don't fire on wrong days/times)
- **Timezone handling:** Correct local property time (not guest timezone)

**Performance Under Load:**
- **Support 10,000 concurrent calendar-based workflows** (assuming 80 accounts × 50 properties × 2-3 operational messages)
- **Real-time processing:** Trigger evaluation every 60 seconds maximum
- **Peak handling:** Monday morning surge (weekend → weekday transitions)

**Backward Compatibility:**
- **100% of existing automated message workflows continue functioning**
- **Zero disruption** to current reservation-based triggers
- **Seamless integration** with existing Redux AM state management

**System Reliability:**
- **99.95% uptime** for calendar trigger service
- **Graceful degradation:** If calendar service fails, reservation-based triggers still work
- **Audit trail:** All calendar triggers logged for debugging

### Measurable Outcomes

**By End of Month 1:**
- 20+ accounts have created calendar workflows (early adopters)
- First success stories captured ("saved me 2 hours this week!")
- Support team sees first reduction in "AM Failed to Send" tickets

**By End of Month 3:**
- 40 accounts actively using (50% of target)
- 15-20% reduction in AM complexity tickets observed
- Product marketing announces competitive parity

**By End of Month 6:**
- 50+ accounts using (62% of target)
- 30% reduction in AM-related support burden
- Feature becomes standard demo for mid-market prospects

**By End of Month 12:**
- 64+ accounts using (80% of target)
- 40% reduction in "AM Failed to Send" tickets achieved
- $189K MRR fully retained, expansion deals cite this as key feature

## Product Scope

**Strategic Overview:**

This feature targets 80 mid-market accounts ($189K MRR) requesting calendar-based scheduling for operational messaging (trash, pool, lawn reminders). MVP eliminates manual activate/deactivate cycles and closes competitive gap with Track/Streamline.

**Development Phases:**

- **MVP (Phase 1):** Day-of-week + time-of-day + date ranges + real-time triggers. Target: 50% adoption (40 accounts) within 3 months. Timeline: 6-8 weeks.
- **Growth (Phase 2):** Multiple send times, holiday awareness, advanced combinations, template library. Target: 80% adoption (64 accounts) by month 12.
- **Vision (Phase 3):** External calendar integration, AI-powered scheduling, conditional logic, broadcast + calendar.

Detailed MVP capabilities, Phase 2/3 features, and resource requirements documented in "Project Scoping & Phased Development" section below.

## User Journeys

### Journey 1: Sarah - The Overwhelmed Mid-Market PM

**Meet Sarah:**
- **Role:** Property Manager at "Coastal Rentals" (72 vacation properties across 3 beach towns)
- **Situation:** Managing operational messaging for 72 properties is consuming her life
- **Current Reality:** Every Sunday evening, she sets 15-minute phone alarms for Monday-Friday to manually activate "trash day" messages, pool service reminders, lawn care notices

**Opening Scene - Sunday Night, 9:47 PM:**

Sarah sits at her kitchen table, laptop open, mentally preparing for another week of message management. She has a spreadsheet tracking which properties get trash pickup on which days (Thursday for beachfront, Tuesday for inland). She's about to spend 30 minutes creating tomorrow's "Monday checklist":

- 6:00 AM: Activate "Trash reminder - Thursday properties" workflow
- 8:00 AM: Activate "Pool service - Wednesday properties" workflow  
- 9:00 AM: Remember to deactivate Friday's messages from last week

She thinks: *"There HAS to be a better way. This can't scale."*

**Rising Action - Monday Morning at Guesty HQ:**

Sarah receives an email: *"New Feature: Calendar-Based Automations - Set it and forget it!"*

She clicks through skeptically (she's seen "automation" promises before). The tutorial shows:
- "Send trash reminders every Thursday at 8am"
- "Pool service notifications every Wednesday at 7am"  
- "Weekend-only check-in prep messages"

She thinks: *"Wait... EVERY Thursday? Without me doing anything?"*

**The Critical Moment - Tuesday Afternoon:**

Sarah opens her Automated Messages. She sees a new "Calendar Scheduling" section. Her hands are shaking slightly as she:

1. Selects "Trash Day Reminder" workflow
2. Clicks "Add Calendar Trigger"
3. Checks "Thursday"
4. Sets time: "8:00 AM"
5. Clicks "Save"

A confirmation appears: *"This message will now send automatically every Thursday at 8:00 AM (property local time). You'll never need to activate it manually again."*

She stares at the screen. Creates 6 more calendar-based workflows in 20 minutes:
- Thursday trash (beachfront properties)
- Tuesday trash (inland properties)
- Wednesday pool service
- Monday lawn care
- Friday weekend prep
- Saturday arrival reminders

**Resolution - Three Weeks Later:**

Sarah's Sunday night routine has changed. No spreadsheet. No phone alarms. No manual activations.

She checks her Automated Messages dashboard:
- ✅ 156 calendar-based messages sent this month
- ✅ Zero manual interventions needed
- ✅ 6 hours saved

She texts her business partner: *"Remember when I spent 2 hours every week managing operational messages? That's gone. This actually works."*

Three months later, Coastal Rentals expands from 72 to 95 properties. Sarah doesn't change her workflow. The messages just work.

**Requirements from Sarah's Journey:**
- Calendar UI in AM creation flow
- Day-of-week selector
- Time picker
- "Set and forget" confirmation messaging
- Dashboard showing calendar-based message history
- Zero manual intervention after setup

---

### Journey 2: Marcus - The Burned-Out Support Engineer

**Meet Marcus:**
- **Role:** Senior Support Engineer at Guesty (3 years on the Communications team)
- **Situation:** Drowning in "AM Failed to Send" tickets - 910 annually, 40% due to condition confusion
- **Current Reality:** Explaining "advanced notice" vs "days before" vs "length of stay" conditions to frustrated customers 15 times a week

**Opening Scene - Tuesday Morning, 10:23 AM:**

Marcus opens ticket #1847291: *"My trash reminder didn't send on Thursday. It worked last week!"*

He sighs. He knows what happened. The customer set up a reservation-based trigger ("3 days after check-in") but their property had no check-in on Monday, so Thursday's message never fired. The customer was manually activating it weekly as a workaround.

He drafts his 47th explanation this month about how automated messages work. He thinks: *"They just want 'Send every Thursday.' Why is this so complicated?"*

**Rising Action - Feature Launch Day:**

Marcus attends the internal demo for Calendar-Based Automations. The PM shows:
- "Send on specific days of the week"
- "No reservation required"
- "Set it once, runs forever"

Marcus leans forward. He pulls up his saved "template responses" folder - 23 different explanations for why messages didn't send. He realizes most of them become obsolete.

**The Critical Moment - First Week Post-Launch:**

Marcus monitors his ticket queue:

**Week Before Launch:**
- Mon-Fri: 18 "AM Failed to Send" tickets
- Primary cause: Condition misunderstanding

**Week After Launch:**
- Mon-Fri: 11 "AM Failed to Send" tickets
- 7 resolved with: "Have you tried Calendar-Based Automations instead?"

He creates a new saved reply:
*"It sounds like you want operational messaging (trash, pool, etc.) rather than guest-journey messaging. Try our new Calendar-Based Automations - just select the day of the week! Here's a quick guide..."*

**Resolution - Three Months Later:**

Marcus reviews his quarterly metrics:
- **"AM Failed to Send" tickets: DOWN 38%** (from 227 to 141)
- **"AM Creation confusion" tickets: DOWN 22%** (from 488 to 381)
- **Average resolution time: DOWN 15 minutes per ticket**

His manager asks: *"What changed?"*

Marcus replies: *"Calendar automations gave customers the obvious answer. They stop fighting with reservation conditions when they just want 'every Thursday.'"*

He closes his laptop at 5pm on Friday. First time in months he's not finishing lingering "condition logic" explanations.

**Requirements from Marcus's Journey:**
- Clear separation in UI between "Reservation-based" and "Calendar-based" triggers
- Help documentation that's easy for support to link
- Error messages that suggest calendar automations when appropriate
- Support dashboard showing adoption rates (so they can proactively suggest it)

---

### Journey 3: Tom - The Comparison-Shopping Small Business Owner

**Meet Tom:**
- **Role:** Owner of "Mountain View Escapes" (23 cabins in Asheville, NC)
- **Situation:** Currently using Track PMS, evaluating Guesty for potential switch
- **Current Reality:** Track has calendar-based scheduling - he uses it for trash day reminders every Tuesday

**Opening Scene - Thursday, Sales Call with Guesty:**

Tom is on a demo call with Guesty's sales rep. He's impressed with the Inbox (multi-channel, AI replies), but he has a deal-breaker question:

*"I have trash pickup every Tuesday morning. I send a reminder Monday night at 8pm. Can Guesty do that automatically? Because Track does, and I'm not giving that up."*

The sales rep (who attended the product training last week) smiles:

*"Absolutely. Let me show you our Calendar-Based Automations..."*

**Rising Action - The Demo:**

The rep shows Tom:
1. Create new Automated Message
2. Add "Calendar Trigger"
3. Select "Monday"
4. Set time: "8:00 PM"
5. Done

Tom: *"Wait, that's it? No 'if reservation exists' conditions?"*

Rep: *"Right. This is for operational messaging. It just runs every Monday at 8pm, regardless of reservations. Perfect for trash, pool service, lawn care - anything on a schedule."*

Tom: *"And I can combine it with reservation triggers?"*

Rep: *"Yes. Same message can have both. Monday night trash reminder PLUS 'day before check-in' for guests."*

**The Critical Moment - Decision Time:**

Tom creates his switching pros/cons list:

**Stay with Track:**
- ✅ Has calendar scheduling (but that's not unique anymore)
- ❌ Weaker multi-channel inbox
- ❌ No AI reply suggestions
- ❌ Limited WhatsApp support

**Switch to Guesty:**
- ✅ Now has calendar scheduling (competitive parity)
- ✅ Superior inbox features
- ✅ AI-powered replies
- ✅ Better WhatsApp integration

He signs the Guesty contract that afternoon. Calendar automations removed his primary objection.

**Resolution - Two Months After Migration:**

Tom logs into Guesty on Tuesday morning. He checks his inbox.

12 calendar-based messages sent automatically last night:
- Monday 8pm trash reminders (all 23 properties)
- Zero manual work from him

He texts the Guesty sales rep: *"You were right. This is better than Track. The calendar stuff works exactly how it should."*

**Requirements from Tom's Journey:**
- Feature parity with competitors (Track, Streamline)
- Clear positioning in marketing materials: "Calendar-Based Automations"
- Sales enablement: Competitive comparison sheets
- Migration support: Import Track workflows → Guesty calendar triggers

---

### Journey 4: Lisa - The Enterprise Ops Manager (Scaling Beyond Breaking Point)

**Meet Lisa:**
- **Role:** Director of Operations at "Horizon Hospitality Group" (340 properties, 15-person ops team)
- **Situation:** Her team manually manages 1,200+ operational messages weekly across the portfolio
- **Current Reality:** Three junior ops coordinators spend 4 hours EACH per day managing recurring messages

**Opening Scene - Monthly Operations Review:**

Lisa presents to the executive team:

*"Operational messaging overhead: 60 hours per week across the team. This doesn't scale. If we acquire another 100 properties (Q3 target), we need to hire 2 more coordinators just for message management. Cost: $120K annually."*

CFO: *"Can't we automate this?"*

Lisa: *"Not with current Guesty capabilities. Automated Messages need reservations. We need operational messages on a schedule - trash Tuesdays, pool Wednesdays, regardless of bookings."*

**Rising Action - The Feature Request Response:**

Lisa's Customer Success Manager calls:

*"Lisa, remember that feature request you submitted 8 months ago (PFR-2924 - Calendar-Based Automations)? It's launching next month. You're invited to the beta."*

Lisa immediately schedules time with her team.

**The Critical Moment - Beta Implementation:**

Lisa and her ops team spend 2 days converting their manual workflows to calendar-based automations:

**Created:**
- 47 calendar-based workflows
- Covering: Trash (3 different days), Pool service (2x weekly), Lawn care (weekly), HVAC filter reminders (monthly), Seasonal property prep (date ranges)

**Before:**
- 3 coordinators × 4 hours/day = 60 hours/week
- Manual activate/deactivate cycles
- Frequent missed messages (human error)

**After:**
- 3 coordinators × 1 hour/day = 15 hours/week (monitoring only)
- **45 hours saved weekly**
- Zero missed messages (automated)

**Resolution - Quarterly Review, Three Months Later:**

Lisa updates her operations dashboard:

**Operational Messaging Metrics:**
- **Time spent: DOWN 75%** (60 hrs/week → 15 hrs/week)
- **Missed messages: DOWN 92%** (human error eliminated)
- **Coordinator reallocation:** Team now focuses on guest experience, not message logistics
- **Scalability unlocked:** Can handle 500+ properties with current headcount

CFO: *"So we DON'T need those 2 additional hires?"*

Lisa: *"Correct. Calendar automations bought us 18 months of growth runway."*

**Requirements from Lisa's Journey:**
- Bulk workflow creation (template library for common patterns)
- Portfolio-wide deployment (apply same workflow to 100+ properties)
- Monitoring dashboard (ops team can see ALL calendar-based workflows across portfolio)
- Audit trail (who created what, when)
- Permission model (only senior ops can edit production workflows)

---

### Journey 5: Sarah (Edge Case) - When Things Go Wrong

**Same Sarah from Journey 1, but now...**

**Opening Scene - Wednesday, 2pm:**

Sarah realizes she made a mistake. Her "Trash Day Reminder" workflow is set for **Thursday 8am**, but the trash company just changed pickup to **Tuesday 7am** starting next week.

She needs to:
1. Change the day (Thursday → Tuesday)
2. Change the time (8am → 7am)
3. Make sure Thursday's old messages don't send anymore

She thinks: *"What if I break something?"*

**Rising Action - The Edit Experience:**

Sarah opens the "Trash Day Reminder" workflow. She sees:

**Calendar Trigger Active:**
- Currently: Thursday, 8:00 AM
- Next scheduled send: Thursday, May 18 at 8:00 AM
- Messages sent: 24 (last 3 months)

She clicks "Edit Calendar Trigger":
- Warning appears: *"Changing the schedule will affect future sends. Past messages will not be affected."*
- She changes: Thursday → Tuesday
- She changes: 8:00 AM → 7:00 AM
- She clicks "Save"

Confirmation: *"Schedule updated. Next send: Tuesday, May 16 at 7:00 AM. No Thursday messages will be sent."*

**The Critical Moment - Verification:**

Sarah double-checks:
- ✅ Tuesday 7am is now in the schedule
- ✅ Thursday 8am shows "No upcoming sends"
- ✅ Old Thursday messages still visible in history (not deleted)

She breathes a sigh of relief. It worked exactly how she hoped.

**Resolution - Tuesday 7:15am:**

Sarah checks her phone. Notification:

*"24 automated messages sent: Trash Day Reminder (Tuesday 7:00 AM)"*

She smiles. The change worked. No manual intervention. No broken workflows.

**Requirements from Sarah's Edge Case:**
- Clear edit UI with warnings about schedule changes
- "Next scheduled send" visibility
- History preservation (don't delete past messages when editing)
- Confirmation messaging that's reassuring
- Rollback capability (undo recent edits)

---

### Journey Requirements Summary

These journeys revealed the following capability areas:

**Core Workflow Management:**
- Calendar trigger creation (day-of-week, time-of-day, date ranges)
- Edit/update existing triggers with safeguards
- Delete/disable triggers
- Combine calendar + reservation triggers

**User Interface:**
- Clear separation: "Reservation-based" vs "Calendar-based"
- Calendar selector UI (day picker, time picker)
- "Next scheduled send" visibility
- Confirmation messaging ("set and forget")
- Warning messages on edits

**Monitoring & Visibility:**
- Dashboard: Messages sent via calendar triggers
- Calendar-based workflow list (all active schedules)
- History/audit trail (what fired when)
- Error notifications (if trigger fails)

**Support & Documentation:**
- Help docs: When to use calendar vs reservation triggers
- Migration guide: Convert manual workflows → calendar automations
- Troubleshooting: Why didn't my message send?
- Support dashboard: Adoption metrics

**Enterprise Features:**
- Bulk workflow creation
- Portfolio-wide deployment
- Team permissions (who can edit production workflows)
- Audit trail (change history)

**Migration & Onboarding:**
- Feature discovery (email, in-app notification)
- Guided setup wizard
- Template library (common operational messages)
- Competitive import (Track → Guesty)

## Web App Specific Requirements

### Project-Type Overview

**Application Type:** React 18 Single Page Application (SPA)
- Authenticated admin feature within existing Inbox v2 platform
- Desktop-first workflow (property managers working from office/home computers)
- Integration with existing Redux state management and @guestyci component ecosystem

**User Context:**
- Power users (property managers) managing operational workflows
- Desktop environment (not mobile-optimized)
- Multi-tab usage common (Inbox + Calendar + Reservations)

### Technical Architecture Considerations

**Browser Matrix:**
- **Supported Browsers (Desktop Only):**
  - Chrome 90+ (evergreen)
  - Edge 90+ (Chromium-based)
  - Safari 14+ (macOS)
  - Firefox 88+
  
- **Explicitly NOT Supported:**
  - Internet Explorer 11
  - Mobile browsers (iOS Safari, Chrome Mobile)
  - Legacy/non-evergreen browsers
  - Tablet devices

**Responsive Design:**
- **Desktop-first:** Optimized for 1280px+ viewports
- **No mobile responsive requirements** for calendar automation UI
- Focus on large-screen workflows (multi-property management requires screen real estate)

**Performance Targets:**
- **Initial page load:** < 2 seconds (within existing Inbox v2 performance budget)
- **Calendar UI render:** < 500ms
- **Trigger creation/edit save:** < 1 second response time
- **Dashboard updates:** Real-time (< 5 seconds latency)
- **Trigger evaluation cycle:** Every 60 seconds (backend)

**SEO Strategy:**
- **Not applicable** - Feature is behind authentication
- No public-facing pages to optimize
- No sitemap or meta tags needed for calendar automations

**Accessibility Level:**
- **WCAG 2.1 Level AA compliance** (enterprise standard)
- **Keyboard navigation:** Full keyboard access for calendar picker (arrow keys for day selection, Tab navigation, Enter to confirm)
- **Screen reader support:** ARIA labels for all calendar controls, trigger status announcements, live regions for real-time updates
- **Focus management:** Clear visual focus indicators, logical tab order through workflow creation
- **Color contrast:** 4.5:1 minimum for text, 3:1 for UI components
- **Testing:** Automated accessibility testing in Cypress suite (axe-core integration)

### Real-Time Architecture

**Live Dashboard Updates (Option A Selected):**
- **Requirement:** Users see trigger fire events within 5 seconds without manual refresh
- **Implementation:** WebSocket connection with polling fallback

**WebSocket Strategy (Primary):**
- Subscribe to calendar trigger events when dashboard is active
- Push updates to connected clients in real-time
- Handle reconnection gracefully (exponential backoff)
- Fallback to polling if WebSocket connection fails

**Polling Fallback (Secondary):**
- Poll trigger status every 30 seconds when dashboard is visible
- Stop polling when tab is inactive (Page Visibility API)
- Resume polling when tab becomes active again
- Reduce server load with conditional requests (If-Modified-Since)

**Real-Time Use Cases:**
- Dashboard shows "24 messages sent" immediately after Thursday 8am trigger fires (< 5 seconds)
- "Next scheduled send" countdown updates live
- Error notifications appear instantly if trigger fails (< 5 seconds)
- Workflow status changes (enabled → sending → completed) update without refresh
- Live notification badge: "3 calendar triggers fired in the last hour"

**State Management:**
- Extend existing Redux architecture with `calendarTriggers` slice
- Real-time events update Redux store via WebSocket middleware
- Components react to store changes automatically (React-Redux subscriptions)
- Optimistic updates for trigger creation/edits (immediate UI feedback, confirmed via WebSocket)

### Integration with Existing Inbox v2 Architecture

**Redux State Management:**
- **New reducer:** `calendarTriggersReducer.js` (following existing pattern)
- **Actions:** `calendarTriggersActions.js`
  - `createTrigger`, `updateTrigger`, `deleteTrigger`
  - `fetchTriggerStatus`, `fetchTriggerHistory`
  - `subscribeToTriggerEvents` (WebSocket)
- **Selectors:** `calendarTriggersSelectors.js`
  - `selectActiveTriggers`, `selectNextScheduledSend`, `selectTriggerHistory`
  - `selectTriggersByWorkflow`, `selectTriggersByDay`

**Component Library:**
- Use existing `@guestyci/arc` components (0.38.1) for UI consistency
- Style with `@guestyci/arc-styles` (0.30.2)
- Follow existing Styled Components patterns (6.1.8)
- Reuse existing date/time picker components if available

**Feature Flags:**
- Use `@guestyci/feature-toggle-fe` (2.1.5) for gradual rollout
- **Flags:**
  - `calendar_based_automations_enabled` (master switch)
  - `calendar_automations_beta` (beta user access)
  - `calendar_real_time_updates` (enable/disable WebSocket)
  - `calendar_date_ranges` (enable seasonal date ranges)

**Date/Time Handling:**
- Leverage existing Moment.js (2.29.4 + timezone 0.5.45)
- Property timezone handling (already exists in Inbox v2)
- Display times in **property local time** (not user timezone or guest timezone)
- Handle daylight saving time transitions gracefully

### UI/UX Implementation Considerations

**Calendar Selector Component:**
- **Day-of-week picker:** Checkbox grid (Mon-Sun) with "Weekdays"/"Weekends" shortcuts
- **Time picker:** Time input with dropdown (format based on locale)
- **Date range picker:** Date selector for seasonal activation (start/end dates)
- **Visual feedback:** Selected days highlighted, time displayed in property timezone with timezone label

**Integration Points in Existing UI:**
- Add "Calendar Trigger" tab/section to existing Automated Message creation/edit flow
- Show calendar icon badge on workflow list items that have calendar triggers
- Dashboard widget: "Calendar-Based Workflows" summary card in main Inbox dashboard
- Side panel: "Upcoming Triggers" widget showing next 5 scheduled sends

**Component States to Handle:**
- **Creating:** New calendar trigger being configured (form validation active)
- **Active:** Trigger is running, show next scheduled send with countdown
- **Paused:** User temporarily disabled trigger (visual indicator)
- **Editing:** Warning modal about schedule changes affecting future sends
- **Error:** Trigger failed to fire, show error message with retry option
- **Loading:** Async operations (saving, fetching status)

**User Feedback Messaging:**
- **Confirmation:** "This message will now send automatically every Thursday at 8:00 AM (property local time). You'll never need to activate it manually again."
- **Next scheduled:** "Next send: Thursday, May 18 at 8:00 AM EDT"
- **Success:** "✓ 24 messages sent via calendar trigger (Thursday, May 18 at 8:00 AM)"
- **Error:** "⚠ Trigger failed: [reason]. Click to retry or contact support."
- **Edit warning:** "Changing the schedule will affect future sends. Past messages will not be affected. Continue?"

### Testing Requirements

**E2E Testing (Cypress):**
- Test suite location: `cypress/e2e/calendar-automations/`
- **Critical paths:**
  - Create calendar trigger flow (day selection → time selection → save → confirmation)
  - Edit existing trigger (warning → change → save → verification)
  - Delete/disable trigger (confirmation → removal)
  - Dashboard real-time updates (mock WebSocket events)
  - Timezone display accuracy
  - Combined calendar + reservation triggers

**Component Testing (React Testing Library):**
- `CalendarSelectorComponent.test.js` - Day picker interactions
- `TimePickerComponent.test.js` - Time selection validation
- `TriggerDashboard.test.js` - Dashboard rendering and updates
- `calendarTriggersReducer.test.js` - Redux state management
- `calendarTriggersSelectors.test.js` - Selector logic

**Accessibility Testing:**
- Automated: Axe-core via @cypress/axe
- Keyboard navigation: Tab order, arrow key navigation, Enter/Space actions
- Screen reader: ARIA label verification, live region announcements

**Performance Testing:**
- Load 100+ calendar workflows in dashboard (< 2 seconds)
- WebSocket message handling at scale (1,000 concurrent users)
- Calendar UI render time (< 500ms)

### Implementation Considerations

**Backward Compatibility:**
- **100% of existing automated message workflows must continue functioning**
- Calendar triggers are additive (don't break existing reservation-based triggers)
- Database schema changes must be backward compatible (add columns, don't modify existing)
- API versioning if calendar triggers introduce new endpoints

**Migration Path:**
- No automatic migration of existing workflows (user opt-in)
- Provide migration guide: "Convert manual workflows → calendar automations"
- Support can assist enterprise accounts with bulk migration

**Rollout Strategy:**
- **Phase 1:** Beta users only (feature flag: `calendar_automations_beta`)
- **Phase 2:** Gradual rollout to mid-market accounts (50-200 properties)
- **Phase 3:** General availability (all accounts)
- **Monitoring:** Track adoption, errors, support tickets during each phase

## Project Scoping & Phased Development

### MVP Strategy & Philosophy

**MVP Approach:** Problem-Solving MVP with Competitive Parity Focus

**Strategic Rationale:**
- **Primary goal:** Eliminate manual activate/deactivate pain for 80 accounts ($189K MRR)
- **Secondary goal:** Close competitive gap with Track & Streamline (restore automation parity)
- **Validation target:** Prove calendar concept works for mid-market segment (50-200 properties)

**Why This MVP Scope:**
1. **Day-of-week + time-of-day = 90% of use cases** (operational messaging: trash, pool, lawn)
2. **Date ranges = critical for seasonal operators** (ski resorts, beach rentals have seasonal patterns)
3. **Real-time triggers = table stakes** (competitors have this, can't launch without it)
4. **Combined triggers = power user need** (calendar AND reservation conditions together)

**Resource Requirements:**
- **Frontend team:** 1-2 React developers (calendar UI, Redux integration, real-time updates)
- **Backend team:** 1-2 backend developers (trigger engine, WebSocket service, database schema)
- **QA:** 1 QA engineer (E2E testing, real-time validation)
- **Timeline:** 6-8 weeks (Medium effort estimate from research)

### MVP Feature Set (Phase 1) - Detailed

**Core User Journeys Supported:**
1. ✅ **Sarah's Happy Path** - Create "Thursday trash reminder" in < 5 minutes
2. ✅ **Sarah's Edge Case** - Edit existing trigger with confidence
3. ✅ **Marcus's Support Path** - Clear documentation to reduce tickets
4. ✅ **Tom's Competitive Path** - Feature parity demo closes Track objection

**Must-Have Capabilities:**

**1. Day-of-Week Scheduling:**
- Multi-select day picker (Mon, Tue, Wed, Thu, Fri, Sat, Sun)
- "Weekdays" shortcut (Mon-Fri)
- "Weekends" shortcut (Sat-Sun)
- Visual feedback for selected days
- Combine with existing reservation conditions

**2. Time-of-Day Scheduling:**
- Time input field (12-hour or 24-hour based on locale)
- Property timezone display (e.g., "8:00 AM EDT")
- Single send time per workflow (MVP limitation)
- Validation: Prevent invalid times (e.g., 25:00)

**3. Date Range Activation:**
- Start date + End date picker
- "Active from [date] to [date]" semantics
- Annual recurrence option (e.g., "June 1 - August 31 every year")
- Validation: End date must be after start date

**4. Trigger Combination Logic:**
- Calendar triggers work independently (no reservation required)
- Calendar + Reservation triggers can combine (AND logic)
- Clear UI separation between "Reservation-based" and "Calendar-based" sections

**5. Real-Time Trigger Engine (Backend):**
- Evaluation cycle: Every 60 seconds
- Fire latency: < 60 seconds from target time
- Multi-channel support: Email, WhatsApp, Direct Messages
- Timezone-aware execution (property local time)
- Graceful degradation if trigger service fails

**6. Calendar Selector UI (Frontend):**
- Embedded in Automated Message creation/edit flow
- Calendar icon badge on workflow list items
- "Next scheduled send" countdown display
- Edit warnings: "Changing schedule affects future sends"
- Confirmation messaging: "Set it and forget it"

**7. Dashboard & Monitoring:**
- "Calendar-Based Workflows" summary widget
- List view: All active calendar triggers with status
- History view: Messages sent via calendar triggers (last 30 days)
- Real-time updates via WebSocket (< 5 second latency)
- Error notifications for failed triggers

**8. Core Integrations:**
- Redux state management: `calendarTriggersReducer`, actions, selectors
- Existing AM database schema (add calendar trigger tables)
- @guestyci/arc component library for UI consistency
- Feature flags: `calendar_automations_enabled`, `calendar_automations_beta`
- Moment.js timezone library for date/time handling

**MVP Success Threshold:**
- ✅ Mid-market PM sets up operational workflow in < 5 minutes
- ✅ Trigger fires accurately every week (99.9% accuracy)
- ✅ Zero disruption to existing AM workflows (backward compatibility)
- ✅ 20+ beta accounts using within 30 days (early adoption proof)

**MVP Out-of-Scope (Explicitly NOT in Phase 1):**
- ❌ Multiple send times per workflow (Phase 2)
- ❌ Holiday calendar awareness (Phase 2)
- ❌ Advanced day combinations ("every other Tuesday") (Phase 2)
- ❌ External calendar integrations (Phase 3)
- ❌ AI-suggested scheduling (Phase 3)
- ❌ Mobile web optimization (not needed for PM workflow)
- ❌ Bulk workflow creation UI (Phase 2 - enterprise feature)

### Post-MVP Features

**Phase 2 (Growth) - 3-6 Months After Launch:**

**Target:** Scale adoption from 40 → 64 accounts, add convenience features

**Features:**
1. **Multiple Send Times** - Same workflow, multiple daily sends
2. **Holiday Awareness** - Skip holidays automatically, custom holiday calendars
3. **Specific Date Triggers** - Annual recurring dates (July 4th, Memorial Day)
4. **Advanced Combinations** - "Every other Tuesday", "First Monday of month"
5. **Workflow Template Library** - Pre-built operational message templates
6. **Analytics Dashboard** - Success rates, usage patterns, adoption metrics

**Phase 2 Success Metrics:**
- 80% adoption among target accounts (64 of 80)
- 35% reduction in AM complexity tickets
- Template library used by 50% of accounts

---

**Phase 3 (Expansion) - 12+ Months After Launch:**

**Target:** Strategic differentiation, enterprise features, monetization potential

**Features:**
1. **External Calendar Integration** - Google Calendar, Outlook sync
2. **AI-Powered Scheduling** - Optimal send time suggestions, auto-adjust based on behavior
3. **Conditional Calendar Logic** - "If vacant, send maintenance reminders"
4. **Broadcast + Calendar** - Scheduled bulk/broadcast messaging
5. **Portfolio Coordination** - Cross-property operational scheduling
6. **Timezone Intelligence** - Auto-detect, DST handling

**Phase 3 Success Metrics:**
- Premium monetization tier (calendar + AI scheduling)
- Enterprise adoption (500+ property accounts)
- $1M+ ARR from advanced calendar features

### Risk Mitigation Strategy

**Technical Risks:**

**Risk 1:** Real-time trigger engine performance degrades under load (10,000 workflows)
- **Mitigation:** Load testing during beta phase, horizontal scaling architecture, database indexing optimization
- **Fallback:** Reduce evaluation frequency to 2 minutes if 60 seconds proves unsustainable
- **Monitoring:** Track trigger latency, fire success rate, system resource usage

**Risk 2:** WebSocket connection instability causes missed dashboard updates
- **Mitigation:** Polling fallback mechanism, automatic reconnection with exponential backoff, connection health monitoring
- **Fallback:** Pure polling approach (30-second intervals)
- **Monitoring:** WebSocket connection success rate, fallback usage frequency

**Risk 3:** Timezone handling errors cause messages to fire at wrong times
- **Mitigation:** Comprehensive timezone testing, leverage existing Moment.js timezone library, QA focus on DST transitions
- **Fallback:** Document timezone limitations clearly, provide manual timezone override option
- **Monitoring:** Track "wrong time" support tickets, audit trigger fire accuracy by timezone

**Market Risks:**

**Risk 1:** Adoption lower than expected (< 50% of 80 accounts in 3 months)
- **Mitigation:** Beta program with 20 high-value accounts, gather feedback early, iterate on UX based on beta insights
- **Validation:** If < 70% of beta users create 2+ workflows within 2 weeks, reassess UI complexity and onboarding
- **Contingency:** Enhanced onboarding wizard, video tutorials, dedicated CSM support for target accounts

**Risk 2:** Feature doesn't reduce support tickets as predicted (< 20% reduction)
- **Mitigation:** Monitor support tickets weekly post-launch, categorize remaining AM tickets, improve documentation and error messages
- **Learning:** If tickets remain high, investigate whether condition logic (not calendar) is the real root cause
- **Adjustment:** Invest in AM simplification (wizard-based setup) in Phase 2 if calendar alone doesn't solve complexity

**Risk 3:** Competitive response - Track/Streamline add features that leapfrog Guesty
- **Mitigation:** Ship Phase 2 quickly (3-6 months after MVP), differentiate with AI scheduling in Phase 3
- **Monitoring:** Quarterly competitive analysis, customer win/loss interviews, feature parity tracking
- **Strategy:** Focus on Guesty's strengths (superior Inbox, AI capabilities) to maintain overall advantage

**Resource Risks:**

**Risk 1:** Development takes longer than 6-8 weeks (scope creep, technical complexity)
- **Mitigation:** Weekly scope reviews, strict adherence to MVP boundaries, prioritize day-of-week over date ranges if timeline slips
- **Contingency:** Ultra-lean MVP (day-of-week ONLY), ship in 4 weeks, add date ranges in Phase 1.5
- **Escalation:** If > 10 weeks, reassess technical approach (consider third-party scheduling service)

**Risk 2:** Smaller team than planned (1 frontend, 1 backend only)
- **Mitigation:** Reduce MVP to day-of-week + time only (defer date ranges to Phase 2), simplify real-time updates (polling only, no WebSocket in MVP)
- **Timeline adjustment:** 8-10 weeks with smaller team
- **Scope trade-off:** Maintain trigger accuracy, sacrifice dashboard real-time updates if needed

**Risk 3:** Backend infrastructure limitations (trigger engine can't scale to 10K workflows)
- **Mitigation:** Architecture review before development starts, consider managed cron service (AWS EventBridge, Google Cloud Scheduler)
- **Fallback:** Start with 1,000 workflow limit (sufficient for 80 accounts), scale infrastructure in Phase 2 as adoption grows
- **Monitoring:** Track workflow count, trigger queue depth, system resource usage

## Functional Requirements

### Calendar Trigger Configuration

- **FR1:** Property managers can specify one or more days of the week (Monday-Sunday) when a workflow should activate
- **FR2:** Property managers can specify a time of day (hours and minutes) when a workflow should send messages
- **FR3:** Property managers can specify a date range (start date and end date) during which a workflow is active
- **FR4:** Property managers can configure date ranges to recur annually (e.g., "June 1 - August 31 every year")
- **FR5:** Property managers can use preset shortcuts for common day patterns (Weekdays, Weekends)
- **FR6:** Property managers can combine calendar triggers with existing reservation-based conditions (AND logic)
- **FR7:** Property managers can create calendar-only workflows that fire without any reservation required
- **FR8:** Property managers can view the property's timezone when configuring trigger times

### Workflow Management

- **FR9:** Property managers can create a new automated message workflow with calendar-based triggers
- **FR10:** Property managers can edit calendar trigger settings for existing workflows
- **FR11:** Property managers can delete calendar triggers from workflows
- **FR12:** Property managers can view a list of all workflows that use calendar-based triggers
- **FR13:** Property managers can activate or deactivate calendar-based workflows
- **FR14:** Property managers can duplicate existing calendar-based workflows to create new ones
- **FR15:** Property managers can see visual indicators that distinguish calendar-based workflows from reservation-based workflows

### Message Scheduling & Delivery

- **FR16:** The system can evaluate calendar triggers every 60 seconds to determine if messages should be sent
- **FR17:** The system can fire messages within 60 seconds of the configured trigger time
- **FR18:** The system can execute calendar triggers in the property's local timezone
- **FR19:** The system can send messages via multiple channels (Email, WhatsApp, Direct Messages)
- **FR20:** The system can handle daylight saving time transitions correctly
- **FR21:** The system can prevent duplicate message sends for the same trigger occurrence
- **FR22:** The system can continue firing calendar triggers even if reservation-based conditions fail

### Monitoring & Visibility

- **FR23:** Property managers can view the next scheduled send time for each calendar-based workflow
- **FR24:** Property managers can see a dashboard widget summarizing all calendar-based workflows
- **FR25:** Property managers can view a list of all active calendar triggers with their current status
- **FR26:** Property managers can view a history of messages sent via calendar triggers (last 30 days)
- **FR27:** Property managers can see real-time updates when calendar triggers fire or workflow status changes
- **FR28:** Property managers can receive error notifications when calendar triggers fail to fire
- **FR29:** Property managers can see a countdown timer showing time until next scheduled send

### Integration & Compatibility

- **FR30:** The system can maintain backward compatibility with all existing automated message workflows
- **FR31:** The system can integrate calendar trigger data into the existing Redux state management architecture
- **FR32:** The system can respect feature flags to enable/disable calendar automations for specific accounts
- **FR33:** The system can store calendar trigger configurations in the existing Automated Messages database
- **FR34:** The system can support calendar automations across all account types (SMB, mid-market, enterprise)
- **FR35:** The system can render calendar trigger UI using the existing @guestyci/arc component library

### User Support & Documentation

- **FR36:** Support agents can access documentation explaining how calendar-based automations work
- **FR37:** Property managers can see clear error messages when calendar trigger configuration is invalid (e.g., end date before start date)
- **FR38:** Property managers can see confirmation messages when workflows are successfully scheduled
- **FR39:** Property managers can see warning messages when editing a workflow will affect future scheduled sends
- **FR40:** Support agents can view a customer's calendar trigger configurations to troubleshoot issues

## Non-Functional Requirements

### Performance

**NFR-P1:** Calendar trigger evaluation cycle completes within 60 seconds
- **Measurement:** System checks all active calendar triggers and fires eligible workflows within one 60-second evaluation cycle

**NFR-P2:** Message firing occurs within 60 seconds of configured trigger time
- **Measurement:** 95th percentile latency from scheduled time to actual message send is ≤ 60 seconds

**NFR-P3:** Dashboard loads and displays calendar workflow list within 2 seconds
- **Measurement:** Time from page load to full calendar workflow list render ≤ 2 seconds (desktop, broadband)

**NFR-P4:** Real-time dashboard updates arrive within 5 seconds of trigger event
- **Measurement:** WebSocket message delivery latency from backend event to frontend UI update ≤ 5 seconds (95th percentile)

**NFR-P5:** Workflow creation/edit form interactions respond within 300ms
- **Measurement:** Calendar selector UI (day picker, time input, date range) interactions provide visual feedback within 300ms

### Security

**NFR-S1:** User access to calendar workflows is restricted by account permissions
- **Measurement:** Property managers can only view/edit workflows for properties they have access to

**NFR-S2:** Calendar trigger configurations are stored with encryption at rest
- **Measurement:** Database fields containing trigger configuration data use AES-256 encryption

**NFR-S3:** All API requests for calendar workflow operations require authenticated sessions
- **Measurement:** 100% of calendar workflow create/read/update/delete operations validate user authentication tokens

**NFR-S4:** WebSocket connections authenticate users before allowing real-time updates
- **Measurement:** WebSocket handshake validates session token before establishing connection

### Scalability

**NFR-SC1:** System supports concurrent evaluation of 10,000 calendar triggers per evaluation cycle
- **Measurement:** Trigger engine processes 10,000 active workflows within 60-second evaluation cycle without performance degradation

**NFR-SC2:** Dashboard UI supports displaying up to 500 calendar workflows per account without performance degradation
- **Measurement:** Workflow list rendering and filtering remains responsive (<2s load time) with 500 workflows

**NFR-SC3:** WebSocket service supports 1,000 concurrent real-time connections
- **Measurement:** System maintains stable WebSocket connections for 1,000 simultaneous users without dropped connections or increased latency

**NFR-SC4:** System scales horizontally to handle 10x user growth with <10% performance degradation
- **Measurement:** Adding horizontal capacity (additional backend instances) maintains NFR-P1 and NFR-P2 thresholds

### Accessibility

**NFR-A1:** Calendar trigger UI meets WCAG 2.1 Level AA compliance
- **Measurement:** Automated accessibility testing (axe-core) reports zero Level A or AA violations in calendar selector components

**NFR-A2:** All calendar workflow interactions are keyboard-navigable
- **Measurement:** Users can create, edit, and manage calendar workflows using keyboard only (no mouse required)

**NFR-A3:** Screen readers can announce calendar trigger status and next scheduled send times
- **Measurement:** NVDA/JAWS screen readers correctly announce workflow status, day selections, time inputs, and countdown timers

**NFR-A4:** Color-coded workflow indicators provide non-color alternative cues
- **Measurement:** Calendar workflow status uses both color and icons/text labels (e.g., "Active" badge, not just green color)

### Integration

**NFR-I1:** Calendar trigger data integrates seamlessly with existing Redux state management
- **Measurement:** Calendar workflows use standard Redux actions/reducers, no separate state management layer

**NFR-I2:** Calendar UI components use @guestyci/arc component library for consistency
- **Measurement:** 100% of calendar trigger UI elements use arc components (Button, Input, DatePicker, etc.)

**NFR-I3:** Feature flags control calendar automation availability per account
- **Measurement:** `calendar_automations_enabled` and `calendar_automations_beta` flags correctly enable/disable UI and backend features

**NFR-I4:** Calendar trigger storage uses existing Automated Messages database schema
- **Measurement:** Calendar trigger data stored in AM database with backward-compatible schema changes (no data migration required for existing workflows)

**NFR-I5:** Multi-channel message sending (Email, WhatsApp, Direct Messages) works identically for calendar triggers
- **Measurement:** Calendar-triggered messages send via all supported channels with same reliability as reservation-triggered messages

### Reliability

**NFR-R1:** Calendar trigger firing accuracy is 99.9% or higher
- **Measurement:** Percentage of calendar triggers that fire successfully at scheduled time: ≥ 99.9% (excluding external service failures)

**NFR-R2:** System continues operating if WebSocket service fails
- **Measurement:** Dashboard automatically falls back to 30-second polling if WebSocket connection drops, no user-facing errors

**NFR-R3:** Failed trigger sends generate error notifications to property managers
- **Measurement:** If message send fails after trigger fires, system creates notification visible in dashboard within 60 seconds

**NFR-R4:** System maintains backward compatibility with all existing automated message workflows
- **Measurement:** Zero existing workflows are disrupted or require manual updates after calendar automations launch

**NFR-R5:** Trigger evaluation service restarts automatically after failures
- **Measurement:** If trigger evaluation service crashes, system auto-restarts within 30 seconds and resumes evaluation cycle
