---
title: "Intake Figma Content Library"
---

# Intake Figma Content Library

**Copy-paste realistic content for your mockup screens**

---

## 🏠 Home Dashboard Content

### Space Card 1: Investigating State
```
Title: Notification Preferences
Icon: 🔍
Status Badge: ⏳ In Progress
Progress: 3/4 (SAY, DO, TECHNICAL complete)
Metadata: Started 12 min ago
Alert: ⚠️ Contradiction detected
Button: Enter →
```

### Space Card 2: Ready State
```
Title: Dashboard Performance
Icon: 🎨
Status Badge: ✓ Complete
Progress: 4/4 (All complete)
Metadata: Ready for review • 92% confidence
Button: Review →
```

### Space Card 3: Synthesizing State
```
Title: SSO Integration
Icon: 🔐
Status Badge: ⏳ In Progress
Progress: 2/4 (SAY, BELIEVES complete)
Metadata: Coordinator: Synthesizing insights...
Button: Enter →
```

### Collapsed Sections
```
📦 Ready for Review (2) [Expand ▼]
🎯 Shipped to Cursor (12) [View →]
```

---

## 🎯 Space Detail Content

### Intent Section
```
Heading: 🎯 Intent

Intent text:
"Add notification preferences so users can control 
email vs Slack notifications independently"

Button: [Edit Intent]
```

### Agent Status Cards

#### SAY Agent (Complete)
```
Type: SAY
Badge: ✓ Complete

Metric:
12 interviews analyzed

Key findings:
• "Turn off email but keep Slack" (3 quotes)
• "Too many pings" (8 quotes)  
• "Need more control" (2 quotes)

Link: [View All →]
```

#### DO Agent (Working)
```
Type: DO
Badge: ⏳ Working

Metric:
Analyzing usage patterns...

Patterns found:
• 23% disable ALL notifications
• 67% never customize defaults
• 10% change settings weekly

Link: [View All →]
```

#### TECHNICAL Agent (Queued)
```
Type: TECHNICAL
Badge: ⏸️ Queued

Status:
Waiting for DO results

Next steps:
• Scan NotificationService.ts
• Check routing capabilities
• Verify channel support

Link: [View All →]
```

#### BELIEVES Agent (Complete)
```
Type: BELIEVES
Badge: ✓ Complete

Documents analyzed:
3 strategy docs
1 OKR document

Aligned with:
• Q2 Goal: Reduce churn by 15%
• Initiative: Improve user control

Link: [View All →]
```

### Coordinator Insight Card
```
Heading: 🤖 Coordinator Agent Insight

Insight:
"Users SAY they want granular control, but DO shows 
binary behavior (all on/off). This suggests granularity 
is desired but not discoverable in current UI."

Recommendation:
Add per-channel notification toggles with better UX 
education (tooltips, onboarding flow, clear labels).

Confidence: 87%
```

### Action Buttons
```
[Steer Investigation]  [Review Draft Spec →]
```

---

## 📄 Spec Review Content

### Evidence Chain
```
Decision: Add per-channel notification toggles

Evidence tree:
└─┬─ SAY: "Turn off email but keep Slack" (Modjo #47, #51, #62)
  ├─ DO: 23% disable ALL notifications (Datadog Analytics)
  ├─ TECHNICAL: NotificationService.ts supports channel routing
  └─ BELIEVES: Q2 churn reduction goal (OKR-2024-Q2-03)

[View Full Evidence Trail →]
```

### Implementation Plan (Accordion Sections)

#### UI/UX Changes (3)
```
UI/UX Changes (3) [Expand ▼]

When expanded:
├─ Add NotificationSettings component
│  └─ New React component with per-channel toggles
├─ Update UserPreferences modal  
│  └─ Add notification preferences tab
└─ Add tooltip education layer
   └─ Contextual help for new granular controls
```

#### Data Model Updates (2)
```
Data Model Updates (2) [Expand ▼]

When expanded:
├─ Add notification_preferences table
│  └─ Columns: user_id, channel, enabled, updated_at
└─ Migration: Split notification column
   └─ Migrate binary flag to granular preferences
```

#### Business Logic (1)
```
Business Logic (1) [Expand ▼]

When expanded:
└─ Update NotificationService routing logic
   └─ Check per-channel preferences before sending
```

#### Acceptance Criteria (4)
```
Acceptance Criteria (4) [Expand ▼]

When expanded:
├─ User can toggle email notifications independently
├─ User can toggle Slack notifications independently  
├─ Tooltips explain granular control options
└─ Existing users migrated to new schema (email=on, Slack=on)
```

### Code Block
```yaml
feature: notification_preferences
priority: high
confidence: 92%

files:
  - path: src/components/NotificationSettings.tsx
    action: create
    description: Per-channel toggle component
  
  - path: src/services/NotificationService.ts
    action: modify
    description: Update routing to check channel preferences
  
  - path: database/migrations/2024_02_add_notification_prefs.sql
    action: create
    description: New table + migration logic

ui_changes:
  - component: NotificationSettings
    type: new_component
    location: UserPreferences modal
    
  - component: UserPreferences
    type: modify
    changes: Add notifications tab

data_model:
  - table: notification_preferences
    columns:
      - user_id: uuid (FK to users)
      - channel: enum['email', 'slack', 'in_app']
      - enabled: boolean
      - updated_at: timestamp

business_logic:
  - service: NotificationService
    method: sendNotification
    changes: Check channel preference before routing

acceptance_criteria:
  - Independent email toggle works
  - Independent Slack toggle works  
  - Tooltips show on hover
  - Migration preserves existing behavior

evidence:
  customer_say: "Turn off email but keep Slack" (Modjo #47)
  customer_do: 23% disable ALL notifications (Datadog)
  technical: NotificationService.ts supports routing
  strategic: Q2 churn goal (OKR-2024-Q2-03)
```

### Action Buttons
```
[Edit Spec]  [Investigate More]  [Ship to Cursor →]
```

---

## 🚀 Onboarding Content

### Step 1: Welcome
```
Heading: Welcome to Intake
Subheading: "Cursor for Product Managers"

Body text:
Transform scattered signals into machine-executable 
specs in 90 seconds — not 4-5 days.

Illustration caption:
SAY → DO → TECHNICAL → BELIEVES → Spec

Buttons:
[Get Started →]  [Watch Demo (2 min)]
```

### Step 2: Connect Integrations
```
Heading: Step 1 of 3: Connect Your Data Sources
Progress bar: 33% filled (step 1 of 3)

Intro text:
Intake investigates 4 signals automatically:

SAY Section:
Heading: SAY — What customers tell you
Buttons: [Connect Modjo] [Connect Gong] [Upload CSVs]

DO Section:
Heading: DO — What customers actually do
Buttons: [Connect Datadog] [Connect Mixpanel] [Upload]

TECHNICAL Section:
Heading: TECHNICAL — What's possible in your codebase
Buttons: [Connect GitHub] [Connect GitLab]

BELIEVES Section:
Heading: BELIEVES — What your strategy says
Buttons: [Connect Notion] [Connect Confluence] [Upload]

Footer buttons:
[Skip for Now]                        [Continue →]
```

### Step 3: First Decision
```
Heading: Step 2 of 3: Create Your First Decision
Progress bar: 66% filled (step 2 of 3)

Intro text:
What product decision do you need help with?

Example callout:
💡 Example: "Should we add granular notification 
preferences or keep it simple?"

Input label:
Your turn:

Placeholder text:
Describe your product decision or question...

Buttons:
[Use Example]                   [Start BMAD →]
```

### Step 4: Watch BMAD
```
Heading: Step 3 of 3: Watch BMAD Investigate
Progress bar: 100% filled (step 3 of 3)

Decision echo:
Your decision: "Should we add granular notification 
preferences or keep it simple?"

Status:
🔍 BMAD agents are investigating...

Live updates (show 2-3):
[SAY Agent] ████████ Analyzing 12 interviews...
            ↳ Found: "Turn off email but keep Slack" (3x)

[DO Agent]  ████░░░░ Checking Datadog...
            ↳ Found: 23% disable ALL notifications

Tooltip/callout:
"This takes 90 seconds. Grab a coffee ☕"

Buttons:
[Watch Live]  [Skip to Results →]
```

---

## 📊 Data Examples

### Customer Quotes (SAY)
```
1. "I want to turn off email notifications but keep Slack"
   Source: Modjo Interview #47, Customer: Acme Corp PM

2. "Getting too many pings throughout the day"
   Source: Modjo Interview #51, Customer: TechStart PM

3. "Wish I had more control over which notifications I get"
   Source: Modjo Interview #62, Customer: Growth Co PM

4. "Email notifications are overwhelming, but I need Slack"
   Source: Modjo Interview #18, Customer: SaaS Inc PM

5. "Can't focus with constant email interruptions"
   Source: Modjo Interview #23, Customer: Product Labs
```

### Behavioral Data (DO)
```
Datadog Analytics — Notification Settings Usage:
├─ 23% of users disable ALL notifications
├─ 67% of users never change default settings
├─ 10% of users change settings weekly
├─ Average time in settings: 12 seconds
└─ 45% abandon settings page without changes

Mixpanel — Feature Engagement:
├─ Notification settings page: 3.2% MAU
├─ Settings changed: 1.1% MAU  
├─ Settings reverted within 7 days: 34%
└─ Support tickets about notifications: 142/month
```

### Technical Evidence (TECHNICAL)
```
Codebase scan results:
├─ NotificationService.ts exists ✓
├─ Supports channel routing ✓
├─ Current channels: email, slack, in_app
├─ Refactor effort: Medium (2-3 days)
└─ Dependencies: UserPreferences model, Queue service

Architecture notes:
├─ Notification routing uses channel enum
├─ Preferences stored in user_settings JSONB
├─ Migration path: Add new table, backfill, switch
└─ Risk: Low (backwards compatible)
```

### Strategy Docs (BELIEVES)
```
Q2 2024 OKRs — OKR-2024-Q2-03:
Objective: Reduce user churn by 15%
Key Results:
├─ KR1: Improve notification satisfaction (NPS +10)
├─ KR2: Reduce "too many notifications" complaints by 40%
└─ KR3: Increase settings engagement by 25%

Product Strategy Doc — 2024-Product-Strategy.md:
"Focus on giving users more control over their 
experience. Hypothesis: Users churn when they feel 
overwhelmed or unable to customize the product to 
their workflow."

Roadmap Priority:
├─ Priority: P0 (Top 3 Q2 initiatives)
├─ Target: Ship by end of Q2
└─ Success metric: Churn reduction + NPS improvement
```

---

## 🎨 Microcopy Library

### Button Labels
```
Primary CTAs:
├─ Get Started →
├─ Continue →
├─ Start BMAD →
├─ Review Draft Spec →
├─ Ship to Cursor →
└─ Enter →

Secondary:
├─ Edit Intent
├─ Steer Investigation
├─ Watch Demo (2 min)
├─ Investigate More
├─ Edit Spec
└─ View All →

Tertiary:
├─ Skip for Now
├─ Use Example
├─ View Full Evidence Trail →
├─ Copy to Clipboard
└─ Download YAML
```

### Status Messages
```
In Progress:
├─ "Analyzing usage patterns..."
├─ "Coordinator: Synthesizing insights..."
├─ "BMAD agents are investigating..."
└─ "Checking Datadog..."

Complete:
├─ "Ready for review"
├─ "Investigation complete"
├─ "92% confidence"
└─ "✓ All signals analyzed"

Queued:
├─ "Waiting for DO results"
├─ "Queued for investigation"
└─ "Next in line"
```

### Empty States
```
No decisions yet:
"No product decisions yet. Create your first one to 
see BMAD in action!"

No integrations:
"Connect your data sources to enable automated 
investigation of SAY, DO, TECHNICAL, and BELIEVES 
signals."

Investigation failed:
"Unable to complete investigation. Check your data 
source connections and try again."
```

### Tooltips
```
BMAD Framework:
"BMAD triangulates 4 signals: What customers SAY, 
what they DO, what's TECHNICALLY possible, and what 
your strategy BELIEVES."

Confidence Score:
"Confidence is based on signal strength, evidence 
quality, and alignment across all 4 sources."

Contradiction:
"When SAY and DO signals diverge, it reveals hidden 
insights about user behavior vs. stated preferences."

Machine-Executable Spec:
"A structured format that Cursor can parse and 
execute, with clear file paths, components, and 
acceptance criteria."
```

---

## 🔢 Metrics & Numbers

### Progress Indicators
```
├─ 3/4 signals complete
├─ 2/4 signals complete  
├─ 4/4 signals complete
├─ 92% confidence
├─ 87% confidence
└─ 95% confidence
```

### Time Estimates
```
├─ Started 12 min ago
├─ Started 3 min ago
├─ Completed 5 min ago
├─ Takes 90 seconds
└─ Est. completion: 30s
```

### Evidence Counts
```
├─ 12 interviews analyzed
├─ 3 strategy docs
├─ 23% disable ALL notifications
├─ 67% never customize
├─ 142 support tickets/month
└─ 840+ PM comments (LinkedIn)
```

---

## 📝 Realistic PM Decision Examples

Use these for additional Space Cards:

```
1. "Dashboard Performance"
   Icon: 🎨
   Problem: Dashboard loads slowly (>3s)
   Stage: Ready for review

2. "SSO Integration"  
   Icon: 🔐
   Problem: Should we support SAML or just OAuth?
   Stage: Investigating

3. "Bulk Edit Features"
   Icon: ✏️
   Problem: Users requesting multi-select + bulk actions
   Stage: Investigating

4. "Advanced Filters"
   Icon: 🔍
   Problem: Add more filter options vs. keep UI simple
   Stage: Synthesizing

5. "Mobile App Priority"
   Icon: 📱
   Problem: Build native mobile app or improve responsive?
   Stage: Ready for review
```

---

**Pro tip:** Use Cmd+F (Mac) or Ctrl+F (Windows) to quickly find the content you need while building in Figma!
