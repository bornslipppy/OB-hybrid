# Design Brief: Incident Command Center Hero Component
## High-Fidelity Mockup Specifications

**Project:** Security Incident Management Dashboard - Hero Component  
**Deliverable:** High-fidelity interactive mockups (Figma preferred)  
**Created:** February 13, 2026  
**Author:** Sally (UX Designer) + Yair Cohen  
**Based On:** Hero Component Detailed Design Analysis  

---

## 📋 Overview

Create high-fidelity mockups for an integrated "Incident Command Center" dashboard that combines three intelligent features: Queue Routing, Explainable Priority Scoring, and Adaptive Tables. This system helps security analysts triage incidents 3x faster while reducing burnout.

**Target Users:** SOC (Security Operations Center) analysts - Tier 1, 2, and 3  
**Use Context:** High-stress, time-sensitive incident management (24/7 operations)  
**Key Goal:** Reduce cognitive load, eliminate "queue fishing," build trust in AI recommendations

---

## 🎯 Design Priorities

1. **Clarity Over Beauty** - Users need to make split-second decisions under stress
2. **Information Hierarchy** - Most critical info must be immediately visible
3. **Scanability** - Dense data tables must be easily scannable
4. **Trust Building** - Transparent explanations for AI recommendations
5. **Accessibility** - WCAG 2.1 AA compliance minimum

---

## 📐 Views to Design

### **1. Main Dashboard View (Priority: CRITICAL)**
The landing page analysts see when starting their shift.

**Components Needed:**
- Queue Health Overview panel (bar charts showing capacity)
- "Next Best Incident" recommendation card (hero position)
- Active Incidents table (adaptive, context-aware)
- Alert notifications banner

**Key Interactions:**
- `[ASSIGN TO ME]` button - primary CTA
- `[SKIP]` button - secondary action
- `[VIEW FULL QUEUE]` link - tertiary navigation
- Expandable priority factor breakdown

### **2. Incident Investigation View (Priority: CRITICAL)**
Where analysts work on assigned incidents.

**Components Needed:**
- Incident header (status, priority, metadata)
- Quick Triage Info panel (adaptive based on incident type)
- Priority Breakdown visualization (horizontal bar chart)
- Recommended Actions checklist
- Investigation Notes field

**Key Interactions:**
- Expandable sections (`[▼ EXPAND FOR FULL CONTEXT]`)
- Action buttons (Isolate Host, Escalate, etc.)
- Status update dropdown
- Priority adjustment modal trigger

### **3. Full Queue View with Adaptive Table (Priority: HIGH)**
Browsing all available incidents with filters.

**Components Needed:**
- Filter bar (Type, Severity, Status dropdowns)
- Search field
- Adaptive data table with expandable rows
- Pagination controls
- Column customization menu

**Key Interactions:**
- Filter application (columns adapt automatically)
- Row expansion (▼ → ▲)
- Sorting by column headers
- Bulk actions (optional)

### **4. Priority Adjustment Modal (Priority: MEDIUM)**
Feedback interface for analysts to override AI scores.

**Components Needed:**
- Slider control (0-100 priority scale)
- Radio button list (feedback reasons)
- Text area (explanation field)
- Checkbox list (incorrect factors)
- Submit/Cancel buttons

---

## 🎨 Visual Design System

### **Color Palette**

**Primary Colors (Severity-Based):**
```
Critical Red:    #DC2626 (red-600)
High Orange:     #EA580C (orange-600)
Medium Yellow:   #CA8A04 (yellow-600)
Low Blue:        #2563EB (blue-600)
Info Gray:       #64748B (slate-500)
```

**Status Colors:**
```
Success Green:   #16A34A (green-600)
Warning Amber:   #F59E0B (amber-500)
Error Red:       #DC2626 (red-600)
```

**Background & Surfaces:**
```
Background:      #F8FAFC (slate-50)
Surface:         #FFFFFF (white)
Surface Alt:     #F1F5F9 (slate-100)
Border:          #E2E8F0 (slate-200)
```

**Text Colors:**
```
Primary:         #0F172A (slate-900)
Secondary:       #475569 (slate-600)
Tertiary:        #94A3B8 (slate-400)
Disabled:        #CBD5E1 (slate-300)
```

**⚠️ IMPORTANT:** Do NOT use these colors for decoration - only use them to signal severity, status, or meaning.

---

### **Typography**

**Font Family:**
- Primary: **Inter** (clean, highly readable)
- Monospace (for IDs, hashes): **JetBrains Mono** or **SF Mono**

**Type Scale:**
```
Heading 1:  32px / 40px line-height, Bold (700)
Heading 2:  24px / 32px line-height, Semibold (600)
Heading 3:  20px / 28px line-height, Semibold (600)
Heading 4:  16px / 24px line-height, Semibold (600)

Body Large: 16px / 24px line-height, Regular (400)
Body:       14px / 20px line-height, Regular (400)
Body Small: 12px / 16px line-height, Regular (400)

Label:      14px / 20px line-height, Medium (500)
Caption:    12px / 16px line-height, Regular (400)
```

**When to Use:**
- H1: Page title ("Incident Command Center")
- H2: Section headers ("Queue Health Overview")
- H3: Card titles ("Next Best Incident")
- Body: Standard content, table cells
- Body Small: Metadata, timestamps
- Label: Form labels, button text
- Caption: Helper text, footnotes

---

### **Spacing System**

Use 8px base grid:
```
xs:  4px
sm:  8px
md:  16px
lg:  24px
xl:  32px
2xl: 48px
3xl: 64px
```

**Component Padding:**
- Cards: `lg` (24px)
- Table cells: `md` (16px)
- Buttons: `sm` vertical, `lg` horizontal (8px / 24px)
- Modals: `xl` (32px)

**Component Margins:**
- Between sections: `2xl` (48px)
- Between cards: `lg` (24px)
- Between form fields: `md` (16px)

---

### **Border Radius**

```
None:   0px     (tables, alerts)
Small:  4px     (badges, tags)
Medium: 8px     (buttons, inputs, cards)
Large:  12px    (modals, panels)
Full:   9999px  (pills, avatars)
```

---

### **Shadows**

```
sm:  0 1px 2px rgba(0, 0, 0, 0.05)
md:  0 4px 6px -1px rgba(0, 0, 0, 0.1)
lg:  0 10px 15px -3px rgba(0, 0, 0, 0.1)
xl:  0 20px 25px -5px rgba(0, 0, 0, 0.1)
```

**When to Use:**
- Cards: `md` shadow
- Modals: `xl` shadow
- Dropdowns: `lg` shadow
- Buttons (hover): `sm` shadow

---

## 🧩 Component Specifications

### **1. Priority Score Badge**

**Visual:**
```
┌─────────────────────┐
│  92 🔴 CRITICAL    │  ← Border: 2px solid #DC2626
└─────────────────────┘     Background: #FEE2E2 (red-100)
                            Text: #DC2626 (red-600), Bold 16px
                            Padding: 8px 16px
                            Border radius: 8px
```

**Variants:**
- Critical: Red background (#FEE2E2), red border (#DC2626)
- High: Orange background (#FFEDD5), orange border (#EA580C)
- Medium: Yellow background (#FEF3C7), yellow border (#CA8A04)
- Low: Blue background (#DBEAFE), blue border (#2563EB)

**Accessibility:**
- Minimum contrast ratio: 4.5:1 (text to background)
- Include severity text, not just color
- Icon (🔴) provides additional visual cue

---

### **2. Factor Breakdown Bar Chart**

**Visual:**
```
████████████████████████████████ +35  Asset Criticality
Domain Controller (DC01) - Business Critical Tier 0 Asset

Bar height: 8px
Bar background: Severity color (e.g., #DC2626 for critical)
Bar corner radius: 4px
Number (+35): Bold, 14px, right-aligned, same color as bar
Label: Medium weight, 14px, slate-900
Subtext: Regular, 12px, slate-600
Spacing between bars: 12px vertical
Max bar width: Based on highest score (proportional)
```

**Interaction:**
- Hover: Show tooltip with detailed evidence
- Click: Expand to show full factor explanation

---

### **3. Queue Capacity Indicator**

**Visual:**
```
Critical Queue    ⬛⬛⬛⬛⬛⬛⬛⬛ 8 incidents
────────────────  Avg Wait: 12 min  |  SLA: 15 min
                  Status: ⚠️ SLA RISK

Blocks: 10px × 10px squares, 2px gap
Color: Matches severity (red for critical)
Text: Body (14px), slate-900
Metadata: Body Small (12px), slate-600
Status badge: Inline, padding 4px 8px, rounded corners
```

**Status Badge Colors:**
- ✅ OK: Green background (#D1FAE5), green text (#16A34A)
- ⚠️ WARNING: Yellow background (#FEF3C7), yellow text (#CA8A04)
- 🔴 CRITICAL: Red background (#FEE2E2), red text (#DC2626)

---

### **4. Adaptive Table**

**Visual:**
```
│ ID    │ Status  │ Priority │ Email Subject      │ Sender       │ Recipients │
├───────┼─────────┼──────────┼────────────────────┼──────────────┼────────────┤
│ 47301 │ New     │ 78 🟠   │ Urgent: Update...  │ evil@bad.com │ 127        │

Row height: 48px
Cell padding: 16px horizontal, 12px vertical
Border: 1px solid #E2E8F0 (slate-200)
Header: Bold 14px, slate-700, background #F8FAFC
Row hover: Background #F1F5F9 (slate-100), cursor pointer
Row selected: Background #E0E7FF (blue-100), 2px left border blue-600
```

**Column Widths (Phishing View):**
- ID: 80px (fixed, left-frozen)
- Status: 120px (fixed, left-frozen)
- Priority: 100px (fixed, left-frozen)
- Email Subject: Flexible (min 200px, grows to fill space)
- Sender: 180px
- Recipients: 120px
- Actions: 80px (fixed right, always visible)

**Frozen Columns:**
- First 3 columns (ID, Status, Priority) remain visible when scrolling horizontally
- Use subtle shadow on right edge to indicate frozen boundary

**Empty State:**
```
┌─────────────────────────────────────────────┐
│                                             │
│         🎉 No incidents in queue!           │
│                                             │
│    All caught up - great work!              │
│                                             │
└─────────────────────────────────────────────┘
```

---

### **5. Button Styles**

**Primary Button (e.g., "ASSIGN TO ME"):**
```
Background: #2563EB (blue-600)
Text: White, 14px, Medium weight (500)
Padding: 12px 24px
Border radius: 8px
Hover: Background #1D4ED8 (blue-700), shadow-sm, transform scale(1.02)
Active: Background #1E40AF (blue-800), transform scale(0.98)
Disabled: Background #CBD5E1, text #94A3B8, cursor not-allowed
Focus: 2px outline #3B82F6, 2px offset
```

**Secondary Button (e.g., "SKIP"):**
```
Background: White
Text: #475569 (slate-600), 14px, Medium (500)
Border: 1px solid #E2E8F0 (slate-200)
Padding: 12px 24px
Border radius: 8px
Hover: Background #F8FAFC, border #CBD5E1
Active: Background #F1F5F9
```

**Danger Button (e.g., "ISOLATE HOST"):**
```
Background: #DC2626 (red-600)
Text: White, 14px, Medium (500)
Padding: 12px 24px
Border radius: 8px
Hover: Background #B91C1C (red-700), shadow-sm
Active: Background #991B1B (red-800)
```

**Text Button (e.g., "View Full Queue"):**
```
Background: Transparent
Text: #2563EB (blue-600), 14px, Medium (500)
Padding: 8px 16px
Hover: Text #1D4ED8 (blue-700), underline
Active: Text #1E40AF (blue-800)
```

---

### **6. Expandable Row**

**Collapsed State:**
```
│ 47293 │ New │ 92 🔴 │ APT29 Match on DC │ [▼] │
```

**Expanded State:**
```
│ 47293 │ New │ 92 🔴 │ APT29 Match on DC │ [▲] │
├───────────────────────────────────────────────┤
│ Asset:          DC01.corp.local               │
│ Detection:      PowerShell accessing LSASS    │
│ File Hash:      a3f8b2c4... [🔍 SEARCH]       │
│ Threat Intel:   IOC matches APT29             │
│ Created:        18 min ago                    │
│                                               │
│ [ASSIGN TO ME] [VIEW FULL] [ESCALATE]        │
└───────────────────────────────────────────────┘

Expansion panel background: #F8FAFC (slate-50)
Padding: 16px
Border-top: 1px solid #E2E8F0
Animation: 200ms ease-out, height from 0 to auto
```

---

### **7. Modal/Overlay**

**Visual Structure:**
```
┌─────────────────────────────────────────────┐
│  Modal Title                          [X]   │
├─────────────────────────────────────────────┤
│                                             │
│  Modal content goes here...                 │
│                                             │
│                                             │
│  [PRIMARY ACTION]  [CANCEL]                 │
└─────────────────────────────────────────────┘

Width: 600px (default), max 90vw
Padding: 32px
Border radius: 12px
Shadow: xl (0 20px 25px rgba(0,0,0,0.1))
Backdrop: rgba(15, 23, 42, 0.75) - semi-transparent overlay
Animation: Fade in (200ms), scale from 0.95 to 1.0
```

---

## 🔄 Interaction States

### **All Interactive Elements Need:**

1. **Default State** - Normal appearance
2. **Hover State** - Cursor: pointer, visual feedback (background change)
3. **Active/Pressed State** - Slight scale or color change
4. **Focused State** - Blue outline (2px solid #3B82F6, 2px offset) for keyboard navigation
5. **Disabled State** - Grayed out (#CBD5E1), cursor: not-allowed
6. **Loading State** - Spinner or skeleton, where applicable

---

### **Specific Interactions to Design:**

**Row Expansion Animation:**
- Duration: 200ms ease-out
- Arrow rotates from ▼ (0deg) to ▲ (180deg)
- Row content slides down smoothly
- Height expands from 48px to auto
- Background color transition to #F8FAFC

**Filter Application & Column Adaptation:**
- Duration: 300ms ease-in-out
- Old columns fade out (opacity 1 → 0, 100ms)
- Old columns slide left (translateX 0 → -20px, 200ms)
- New columns slide in from right (translateX 20px → 0, 200ms)
- New columns fade in (opacity 0 → 1, 100ms, delay 150ms)
- Show toast notification: "Table adapted to Phishing view"

**Priority Adjustment Slider:**
- Thumb: 20px × 20px circle, white, shadow-md
- Track: 4px height, #E2E8F0 (gray) background
- Active track (left of thumb): #2563EB (blue)
- Inactive track (right of thumb): #E2E8F0 (gray)
- Show value tooltip above thumb on hover/drag
- Snap to nearest integer value

**Toast Notification:**
```
┌─────────────────────────────────────────┐
│  ℹ️ Table adapted to Phishing view      │
└─────────────────────────────────────────┘

Background: #0F172A (slate-900, 95% opacity)
Text: White, 14px
Padding: 12px 16px
Border radius: 8px
Position: Bottom center, 24px from bottom
Animation: Slide up + fade in (300ms), auto-hide after 3s
```

---

## 📱 Responsive Breakpoints

Design for these screen sizes:

1. **Desktop (Primary):** 1920px × 1080px
2. **Laptop:** 1440px × 900px
3. **Tablet:** 1024px × 768px (landscape)
4. **Mobile:** 375px × 812px (portrait) - OPTIONAL but nice to have

**Layout Rules:**
- **Desktop:** 2-column layout (optional sidebar + main content)
- **Laptop:** Same as desktop, slightly compressed
- **Tablet:** Single column, cards stack vertically, table scrolls horizontally
- **Mobile:** Simplified view, progressive disclosure mandatory, card-based layout

**Responsive Table Behavior:**
- Desktop: All columns visible
- Laptop: Hide less important columns (e.g., "Created" timestamp)
- Tablet: Horizontal scroll, frozen left columns
- Mobile: Convert to card view (no table), show 3-4 key fields per card

---

## 🎭 States to Design

For EACH view, create mockups showing:

### **Main Dashboard:**
1. ✅ **Default state** - Fresh shift, no active incidents, empty "Active Incidents" section
2. ✅ **With recommendation** - "Next Best" incident displayed with full factor breakdown
3. ✅ **With active incidents** - Analyst has 2-3 incidents in progress in table
4. ✅ **SLA alert state** - Critical queue approaching breach (red banner, urgent messaging)
5. ✅ **Empty queue state** - All incidents cleared (celebration message/illustration)

### **Incident Investigation:**
1. ✅ **Malware type** - Adaptive panel shows: file hash, affected hosts, detection source
2. ✅ **Phishing type** - Adaptive panel shows: email subject, sender, recipients, click rate
3. ✅ **Network type** - Adaptive panel shows: source/dest IP, ports, protocol
4. ✅ **Expanded context** - Timeline, full details, related incidents visible
5. ✅ **With notes** - Investigation notes field populated with analyst comments

### **Queue View:**
1. ✅ **No filters applied** - Default columns (ID, Status, Priority, Title, Created)
2. ✅ **Filtered by Phishing** - Columns: ID, Status, Priority, Email Subject, Sender, Recipients
3. ✅ **Filtered by Malware** - Columns: ID, Status, Priority, File Hash, Affected Hosts, Detection Source
4. ✅ **Expanded row** - One incident expanded showing inline details
5. ✅ **Empty results** - No incidents match filters (empty state message)

### **Priority Adjustment Modal:**
1. ✅ **Default state** - Modal open, slider at current priority value
2. ✅ **With feedback** - Radio button selected, text area filled with explanation
3. ✅ **Error state** - Validation error (e.g., "Explanation required when adjusting priority")

---

## 📊 Data to Use in Mockups

**Use realistic but anonymized data:**

### **Sample Incidents:**

**Incident #47293** (Critical Malware)
- Priority: 92 🔴 CRITICAL
- Type: Malware
- Title: APT29 Match on Domain Controller
- Asset: DC01.corp.local (Domain Controller)
- Detection: PowerShell accessing LSASS.exe
- File Hash: `a3f8b2c4d5e6f7a8b9c0d1e2f3a4b5c6`
- Detection Source: EDR (CrowdStrike)
- Affected Hosts: 1 (DC01)
- User: SYSTEM
- Process: powershell.exe (PID: 4892)
- Threat Intel: IOC matches APT29 (Cozy Bear) infrastructure, C2 IP: 198.51.100.23
- MITRE Tactic: T1003 - Credential Dumping
- Created: 18 min ago
- Status: New
- Assigned: Unassigned

**Factor Breakdown:**
- Asset Criticality: +35 (Domain Controller, Business Critical Tier 0)
- Threat Intelligence: +30 (APT29 infrastructure match)
- MITRE Tactic: +20 (Credential Dumping - LSASS access)
- Time Sensitivity: +7 (Active session, user still logged in)

---

**Incident #47301** (High Phishing)
- Priority: 78 🟠 HIGH
- Type: Phishing
- Title: Mass Phishing Campaign - Finance Department
- Email Subject: "Urgent: Update your password immediately"
- Sender: finance@totallylegit-payroll.biz
- Sender IP: 198.51.100.45 (Russia)
- SPF: FAIL
- DKIM: FAIL
- Recipients: 127 (entire Finance dept)
- Clicked Link: 23 users (18% click rate)
- Credentials Submitted: 5 users ⚠️ ACTIVE BREACH
- Domain Registered: 2 days ago
- Hosting: Bulletproof hosting (suspicious)
- Threat Intel: New campaign, no IOC matches yet
- Created: 12 min ago
- Status: New
- Assigned: Unassigned

**Factor Breakdown:**
- Blast Radius: +25 (127 users targeted, 5 credentials compromised)
- Threat Intelligence: +20 (New domain, suspicious hosting)
- Time Sensitivity: +18 (Credentials submitted 8 min ago, attacker may be active)
- Detection Confidence: +15 (High confidence phishing indicators)

---

**Incident #47298** (High Phishing)
- Priority: 72 🟠 HIGH
- Type: Phishing
- Email Subject: "Invoice #8472 - Payment Required"
- Sender: accounts@secure-payment-portal.net
- Recipients: 45
- Clicked Link: 12 users (27%)
- Credentials Submitted: 0
- Created: 25 min ago
- Status: New

---

**Incident #47289** (Medium Phishing)
- Priority: 68 🟡 MEDIUM
- Type: Phishing
- Email Subject: "Package delivery notification"
- Sender: fedex-notify@delivery-updates.biz
- Recipients: 1
- Clicked Link: 1 user (100%)
- Created: 35 min ago
- Status: New

---

**Incident #47285** (Medium Phishing)
- Priority: 64 🟡 MEDIUM
- Type: Phishing
- Email Subject: "Employee satisfaction survey"
- Sender: hr@corporate-survey.biz
- Recipients: 340 (company-wide)
- Clicked Link: 12 users (4%)
- Created: 48 min ago
- Status: In Progress
- Assigned: John Smith

---

**Incident #47280** (Medium Malware)
- Priority: 58 🟡 MEDIUM
- Type: Malware
- Title: Suspicious File Execution
- Asset: WS-Finance-42 (Workstation)
- Detection: Unsigned executable launched from temp folder
- File Hash: `b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9`
- Detection Source: Antivirus (Windows Defender)
- Affected Hosts: 1
- Threat Intel: No matches found
- Created: 1 hr ago
- Status: New

---

**Additional Incidents (for table population):**

Create 10-15 more incidents following this pattern with:
- Mix of types: Phishing (50%), Malware (30%), Network (15%), Other (5%)
- Mix of severities: Critical (5%), High (20%), Medium (50%), Low (25%)
- Mix of statuses: New (60%), In Progress (30%), Resolved (10%)
- Varied timestamps: From "2 min ago" to "4 hrs ago"
- Some assigned, some unassigned

---

## 🎨 Assets Needed

### **Icons** (Use Heroicons or similar consistent set):

**Status & Actions:**
- ⚠️ Alert/Warning (triangle-exclamation)
- ✅ Success/Complete (check-circle)
- ❌ Error/Failed (x-circle)
- ⏸️ Paused (pause-circle)
- 🔄 In Progress (arrow-path, animated)
- ℹ️ Information (information-circle)

**Severity Indicators:**
- 🔴 Critical (filled circle, red)
- 🟠 High (filled circle, orange)
- 🟡 Medium (filled circle, yellow)
- 🔵 Low (filled circle, blue)

**Navigation & UI:**
- ▼ Expand (chevron-down)
- ▲ Collapse (chevron-up)
- → Forward (chevron-right)
- ← Back (chevron-left)
- 🔍 Search (magnifying-glass)
- ⚙️ Settings (cog-6-tooth)
- 👤 User Profile (user-circle)
- ☰ Menu (bars-3)
- ✕ Close (x-mark)
- ⋮ More Options (ellipsis-vertical)

**Security & Incidents:**
- 🎯 Target/Recommendation (cursor-arrow-rays)
- 🔐 Security/Lock (lock-closed)
- 🚨 Urgent Alert (bell-alert)
- 📊 Chart/Metrics (chart-bar)
- 📝 Notes (document-text)
- 🔗 Link/Connection (link)
- 🌐 Network (globe-alt)
- 💻 Computer/Endpoint (computer-desktop)
- 📧 Email (envelope)
- 🛡️ Shield/Protection (shield-check)

**Icon Specifications:**
- Default size: 20px × 20px
- Small size: 16px × 16px (for inline use)
- Large size: 24px × 24px (for emphasis)
- Stroke width: 1.5px (Heroicons default)
- Style: Outline (primary), Solid (for emphasis/filled states)

### **Illustrations** (Optional but recommended):

**Empty States:**
- No active incidents (celebration - person with checkmark)
- No search results (magnifying glass with empty box)
- All caught up (relaxed person at desk)

**Error States:**
- Connection lost (broken wifi symbol)
- Permission denied (locked folder)
- Something went wrong (warning triangle with tools)

**Success States:**
- Shift completed (chart showing upward trend)
- Incident resolved (checkmark with sparkles)

**Illustration Style:**
- Simple, minimal line art
- Use brand color palette (blues, grays)
- Size: 200px × 200px maximum
- Format: SVG (scalable, crisp at any size)

---

## ✅ Deliverables Checklist

Please provide:

### **Figma File Structure:**
```
📁 Incident Command Center Design
  📄 00 - Cover Page
      - Project overview
      - Key stakeholders
      - Timeline
      - Last updated date
      
  📄 01 - Design System
      - Color palette (with hex codes)
      - Typography scale
      - Spacing system (8px grid)
      - Component library
      - Icon set
      
  📄 02 - Main Dashboard
      ├─ Default state (empty)
      ├─ With recommendation
      ├─ With active incidents
      ├─ SLA alert state
      └─ Empty queue (celebration)
      
  📄 03 - Incident Investigation
      ├─ Malware type (collapsed)
      ├─ Malware type (expanded)
      ├─ Phishing type
      ├─ Network type
      └─ With notes
      
  📄 04 - Queue View
      ├─ No filters (default columns)
      ├─ Filtered by Phishing
      ├─ Filtered by Malware
      ├─ Filtered by Network
      ├─ Expanded row
      └─ Empty results
      
  📄 05 - Modals & Overlays
      ├─ Priority adjustment modal (default)
      ├─ Priority adjustment modal (filled)
      ├─ Priority adjustment modal (error)
      └─ Toast notifications
      
  📄 06 - Responsive Views (Optional)
      ├─ Laptop (1440px)
      ├─ Tablet (1024px)
      └─ Mobile (375px)
      
  📄 07 - Component Library
      ├─ Buttons (all states)
      ├─ Form elements
      ├─ Tables
      ├─ Cards
      ├─ Badges
      └─ Icons
      
  📄 08 - Interaction Flows
      - Annotated flows showing key user paths
      - Animation specifications
```

### **Exports Required:**

**Images:**
- ✅ PNG exports (2x resolution @2x, 3x for Retina @3x) for each screen
- ✅ JPG exports for presentation deck (lower file size)
- ✅ SVG exports for all icons and illustrations

**Interactive:**
- ✅ Figma Prototype with clickable flows
- ✅ Key interactions demonstrated (expand, filter, modal)
- ✅ Annotated prototype (notes explaining interactions)

**Developer Handoff:**
- ✅ Figma file with "Inspect" mode enabled
- ✅ Design specs document (PDF or Notion page)
- ✅ Component usage guidelines
- ✅ Exported CSS/Tailwind tokens (if possible)

### **Documentation to Include:**

**Design Specs Document:**
- ✅ Color palette with accessibility notes (contrast ratios)
- ✅ Typography specifications (font sizes, weights, line heights)
- ✅ Spacing measurements (margins, padding, gaps)
- ✅ Component dimensions (button heights, input widths)
- ✅ Border radius values
- ✅ Shadow specifications

**Component Usage Guide:**
- ✅ When to use each component variant
- ✅ Do's and Don'ts for common patterns
- ✅ Examples of correct implementation

**Interaction Patterns:**
- ✅ Animation durations and easing functions
- ✅ Transition specifications (fade, slide, scale)
- ✅ Hover/focus/active state behaviors
- ✅ Loading states and skeleton screens

**Accessibility Notes:**
- ✅ Color contrast ratios for all text (WCAG 2.1 AA)
- ✅ Keyboard navigation patterns (tab order, shortcuts)
- ✅ Screen reader considerations (ARIA labels)
- ✅ Focus indicators (visible, 2px outline)

---

## 🎓 Design References & Inspiration

**Study these for inspiration** (style reference, not direct copying):

### **Excellent Data Visualization:**
- **Datadog Security Monitoring** - Clean metrics, clear status indicators
- **Grafana Dashboards** - Excellent use of color for signal vs. noise
- **Elastic Security** - Good table design with drill-down patterns

### **Excellent Information Hierarchy:**
- **Linear** - Clear priority systems, excellent keyboard shortcuts
- **Height** - Clean project management UI, great use of progressive disclosure
- **Notion** - Excellent expandable/collapsible patterns

### **Excellent Status Indicators:**
- **Stripe Dashboard** - Clear payment status, good use of color and icons
- **GitHub Actions** - Excellent run status visualization
- **Vercel Deployments** - Great status timeline and log viewing

### **Excellent Tables:**
- **Airtable** - Flexible column views, great filtering
- **Retool** - Dense data tables that remain readable
- **Basecamp** - Simple, scannable tables with clear actions

---

## 🚫 What to AVOID

**Design Anti-Patterns:**

❌ **Overly Playful Designs**
- This is high-stakes, stressful work environment
- Avoid excessive animations, playful illustrations, or casual language
- Serious ≠ Boring (aim for professional, confident, trustworthy)

❌ **Tiny Fonts**
- Analysts need to read quickly under stress
- Minimum body text: 14px (never go below 12px)
- Table text: 14px minimum

❌ **Excessive Animations**
- Every animation adds delay
- Only animate for purpose (signal change, provide feedback)
- Keep durations short: 100-300ms max

❌ **Ambiguous Icons**
- Every icon must be immediately recognizable
- Pair icons with text labels when space allows
- Test with users: "What does this icon mean?"

❌ **Poor Color Contrast**
- Never rely on color alone to convey information
- Always pair color with icon, text, or shape
- Check WCAG AA compliance (4.5:1 minimum for text)

❌ **Cluttered Interface**
- Resist urge to show everything at once
- Use progressive disclosure (show more on demand)
- White space is your friend

❌ **Inconsistent Patterns**
- Use same interaction pattern for similar actions
- Don't mix button styles arbitrarily
- Maintain consistent spacing throughout

---

## 🧪 User Testing Recommendations

Before finalizing designs, test with:

**Target Users:**
- 3-5 SOC analysts (Tier 1, 2, or 3)
- Mix of experience levels (junior to senior)
- Different shifts (day, night, weekend)

**Test Scenarios:**
1. **Cold Start:** "You just logged in for your shift. What do you do first?"
2. **Triage Task:** "Find and investigate the most critical incident."
3. **Queue Management:** "How would you filter to see only phishing incidents?"
4. **Override:** "The priority score seems wrong. How would you adjust it?"
5. **Navigation:** "Show me how you'd move between incidents."

**Key Questions to Ask:**
- "What do you notice first on this screen?"
- "What would you click next?"
- "Is anything confusing or unclear?"
- "What information are you looking for that you can't find?"
- "Does this match how you currently work?"

**Success Metrics:**
- ✅ Users can identify "next best" incident in <5 seconds
- ✅ Users understand priority factors without explanation
- ✅ Users can complete triage task without external help
- ✅ Users rate clarity as 4/5 or higher
- ✅ Users trust the AI recommendations

---

## 📞 Questions for Designer

Before starting, please confirm:

1. **Timeline:** 
   - When can you deliver the first draft? (Target: 1 week for Design System + Main Dashboard)
   - What's your availability for feedback cycles?

2. **Tools:** 
   - Will you use Figma? (Preferred for real-time collaboration)
   - Do you have access to Figma Professional? (Needed for advanced prototyping)

3. **Scope:** 
   - Should we start with all states or prioritize Main Dashboard first?
   - Do you need mobile responsive designs now or later?

4. **Design System:**
   - Can you use existing component libraries (e.g., Tailwind, Radix) or build custom?
   - Should we align with any existing brand guidelines?

5. **Questions:**
   - Any unclear requirements from this brief?
   - Do you need access to user research documents?
   - Would you like a kickoff meeting to walk through this brief?

6. **Collaboration:**
   - How should I provide feedback? (Figma comments preferred)
   - Should we schedule weekly check-ins or async updates?
   - Who else should be in the Figma file? (PM, developers, stakeholders)

7. **Handoff:**
   - Do you typically provide Zeplin/Figma specs for developers?
   - Can you export CSS/Tailwind tokens?
   - Will you be available during implementation for questions?

---

## 🚀 Project Timeline (Suggested)

### **Week 1: Foundation**
- **Day 1-2:** Designer reviews brief, asks questions, kickoff meeting
- **Day 3-5:** Design System created (colors, typography, components)
- **Day 5:** Review & feedback on Design System

### **Week 2: Core Screens**
- **Day 1-3:** Main Dashboard (all states)
- **Day 3:** Review & feedback on Dashboard
- **Day 4-5:** Incident Investigation View
- **Day 5:** Review & feedback on Investigation View

### **Week 3: Secondary Screens**
- **Day 1-2:** Queue View with Adaptive Tables
- **Day 2:** Review & feedback on Queue View
- **Day 3-4:** Modals, overlays, notifications
- **Day 4:** Review & feedback on Modals
- **Day 5:** Polish and refinements

### **Week 4: Finalization**
- **Day 1-2:** Responsive designs (if in scope)
- **Day 2-3:** Interactive prototype creation
- **Day 3-4:** Documentation and developer handoff prep
- **Day 5:** Final review & approval

**Total: 4 weeks for complete high-fidelity mockups with prototype**

---

## 📋 Feedback Process

**How we'll collaborate:**

### **Feedback Rounds:**
1. **Round 1:** Design System + Main Dashboard
   - Focus: Overall look & feel, color palette, typography
   - Timeline: 2-3 day turnaround for feedback

2. **Round 2:** Incident Investigation + Queue View
   - Focus: Data visualization, table design, interactions
   - Timeline: 2-3 day turnaround

3. **Round 3:** Modals + Complete Flow
   - Focus: Edge cases, error states, polish
   - Timeline: 1-2 day turnaround

### **Feedback Format:**
- Use Figma comments (preferred - directly on designs)
- Tag specific elements: "@Designer: Can we make this button larger?"
- Provide context: "Users might miss this because..."
- Be specific: "Change font size from 12px to 14px" (not "make bigger")
- Prioritize: Label as "Critical," "Important," or "Nice to have"

### **Approval Criteria:**
- ✅ Meets all requirements from this brief
- ✅ Passes accessibility checks (WCAG 2.1 AA)
- ✅ Positive user testing feedback (if conducted)
- ✅ Development team confirms feasibility
- ✅ Stakeholder sign-off

---

## 📚 Reference Documents

**Related documents in project:**
- `hero-component-detailed-design.md` - Full technical specification
- `hero-component-analysis.md` - Initial analysis and concept
- `market-security-incident-management-dashboards-research-2026-02-13.md` - Market research
- `ux-design-plan-intake.md` - UX strategy document
- `product-brief-intake-2026-02-12.md` - Product requirements

**Designer should review:**
1. Hero Component Detailed Design (understand the system logic)
2. Market Research (see competitor screenshots for context)
3. UX Design Plan (understand user needs and pain points)

---

## 🎨 Final Notes

**Design Philosophy:**
This interface serves analysts working under extreme stress, managing hundreds of security incidents daily. Every design decision should prioritize:

1. **Speed** - Analysts need to make decisions in seconds, not minutes
2. **Clarity** - No ambiguity allowed when dealing with security threats
3. **Trust** - Build confidence in AI recommendations through transparency
4. **Focus** - Eliminate visual noise that distracts from critical information
5. **Calm** - Despite urgency, avoid panic-inducing design (use color purposefully)

**Remember:**
- Less is more (progressive disclosure over showing everything)
- Color is signal (red = urgent action needed, not just decoration)
- Typography is hierarchy (size and weight guide the eye)
- White space is breathing room (especially important in high-stress environments)
- Consistency is predictability (analysts should never wonder "what does this do?")

**This system should feel like:**
- A trusted co-pilot, not a bossy robot
- A clean, organized workspace, not cluttered desk
- A calm, confident presence, not anxious alarm system
- A helpful guide, not cryptic puzzle

---

## ✅ Success Criteria

**This design will be successful when:**

1. ✅ Analysts can identify their "next best" incident in under 5 seconds
2. ✅ 90%+ of analysts understand priority scores without explanation
3. ✅ Triage time reduces from 15 seconds to 5 seconds per incident
4. ✅ No analyst asks "What does this mean?" or "Why is this critical?"
5. ✅ System achieves WCAG 2.1 AA accessibility compliance
6. ✅ Development team confirms all designs are feasible to implement
7. ✅ User testing shows 4/5 or higher satisfaction ratings
8. ✅ Stakeholders approve design for development

---

**Contact for Questions:**  
Yair Cohen  
[Your email]  
[Slack/Teams handle]

---

**Document Version:** 1.0  
**Last Updated:** February 13, 2026  
**Next Review:** Upon first draft completion

---

🎨 **From Sally:** This brief gives your designer everything they need to create a beautiful, functional system that analysts will actually trust and love to use. The key is balancing clarity (for stressed analysts) with polish (to build confidence). Can't wait to see the mockups! ✨
