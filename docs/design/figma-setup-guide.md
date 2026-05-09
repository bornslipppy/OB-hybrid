# Intake Figma Setup Guide

**Version:** 1.0  
**Date:** February 13, 2026  
**Purpose:** Step-by-step guide to set up Intake mockup in Figma

---

## 📁 File Structure Setup

### Step 1: Create New Figma File
1. Create new design file: **"Intake - Product OS for PMs"**
2. Set canvas to **1440px width** (desktop first)
3. Create these pages (in order):

```
Pages:
├── 📄 Cover
├── 🎨 Design System
├── 🧩 Components
├── 🖼️ Screens
└── 🔄 Prototype
```

---

## 🎨 Design System Page

### Canvas Organization
Create 5 frames on this page, left to right:

#### Frame 1: Color Palette (400 x 800)
**Name:** "Colors"

**Create color styles:**

**Primary Colors:**
- `Primary/500` — #3B82F6 (Main blue)
- `Primary/600` — #2563EB (Hover state)
- `Primary/400` — #60A5FA (Light variant)

**Semantic Colors:**
- `Success/500` — #10B981 (Complete, success)
- `Warning/500` — #F59E0B (Contradictions, alerts)
- `Error/500` — #EF4444 (Errors)

**Neutral Colors:**
- `Neutral/900` — #111827 (Headings)
- `Neutral/700` — #374151 (Body text)
- `Neutral/500` — #6B7280 (Secondary text)
- `Neutral/300` — #D1D5DB (Borders)
- `Neutral/100` — #F3F4F6 (Backgrounds)
- `Neutral/50` — #F9FAFB (Page background)
- `White` — #FFFFFF (Cards)

**Layout:**
```
┌──────────────────────────┐
│ Colors                   │
├──────────────────────────┤
│ PRIMARY                  │
│ ██ #3B82F6 Primary/500   │
│ ██ #2563EB Primary/600   │
│ ██ #60A5FA Primary/400   │
│                          │
│ SEMANTIC                 │
│ ██ #10B981 Success/500   │
│ ██ #F59E0B Warning/500   │
│ ██ #EF4444 Error/500     │
│                          │
│ NEUTRAL                  │
│ ██ #111827 Neutral/900   │
│ ██ #374151 Neutral/700   │
│ ██ #6B7280 Neutral/500   │
│ ██ #D1D5DB Neutral/300   │
│ ██ #F3F4F6 Neutral/100   │
│ ██ #F9FAFB Neutral/50    │
│ ██ #FFFFFF White         │
└──────────────────────────┘
```

---

#### Frame 2: Typography (600 x 1200)
**Name:** "Typography"

**Create text styles:**

**Headings (Inter Bold):**
- `Heading/H1` — 32px / Bold / Line height 40px / Neutral/900
- `Heading/H2` — 24px / Bold / Line height 32px / Neutral/900
- `Heading/H3` — 18px / Bold / Line height 24px / Neutral/900
- `Heading/H4` — 16px / Bold / Line height 22px / Neutral/900

**Body (Inter Regular):**
- `Body/Large` — 16px / Regular / Line height 24px / Neutral/700
- `Body/Normal` — 14px / Regular / Line height 20px / Neutral/700
- `Body/Small` — 12px / Regular / Line height 16px / Neutral/500

**Body (Inter Medium):**
- `Body/Large/Medium` — 16px / Medium / Line height 24px / Neutral/700
- `Body/Normal/Medium` — 14px / Medium / Line height 20px / Neutral/700

**Code (Fira Code):**
- `Code/Normal` — 14px / Regular / Line height 20px / Neutral/700

**Labels:**
- `Label/Large` — 14px / Medium / Line height 20px / Neutral/700
- `Label/Normal` — 12px / Medium / Line height 16px / Neutral/700
- `Label/Small` — 11px / Medium / Line height 14px / Neutral/500

**Layout:**
```
┌────────────────────────────────┐
│ Typography                     │
├────────────────────────────────┤
│ HEADINGS                       │
│ Heading 1                      │ H1
│ Heading 2                      │ H2
│ Heading 3                      │ H3
│ Heading 4                      │ H4
│                                │
│ BODY                           │
│ Large body text                │
│ Normal body text               │
│ Small body text                │
│                                │
│ CODE                           │
│ const example = "code";        │
│                                │
│ LABELS                         │
│ Large label • Normal label     │
└────────────────────────────────┘
```

---

#### Frame 3: Spacing System (400 x 600)
**Name:** "Spacing"

**Document spacing values:**

```
XS:  4px   ━━
S:   8px   ━━━━
M:   16px  ━━━━━━━━
L:   24px  ━━━━━━━━━━━━
XL:  32px  ━━━━━━━━━━━━━━━━
XXL: 48px  ━━━━━━━━━━━━━━━━━━━━━━━━
```

**Create these as visual examples with rulers**

---

#### Frame 4: Icons (800 x 800)
**Name:** "Icons"

**Icon set to use:** Heroicons or Lucide (import from plugin)

**Icons needed:**
- ✓ Checkmark (complete)
- ⏳ Clock (in progress)
- ⚠️ Warning triangle
- 🔍 Magnifying glass (investigation)
- 🎯 Target (intent)
- 🤖 Robot (coordinator agent)
- 📊 Chart bars (evidence/data)
- ⚙️ Gear (settings)
- 👤 User (profile)
- ➕ Plus (new decision)
- ← Back arrow
- → Forward arrow
- ▼ Chevron down
- ▲ Chevron up

**Size:** 20px × 20px (primary), 16px × 16px (secondary)

---

#### Frame 5: Effects (400 x 800)
**Name:** "Effects"

**Create effect styles:**

**Shadows:**
- `Shadow/SM` — Drop shadow, Y: 1px, Blur: 2px, Color: #000000 10%
- `Shadow/MD` — Drop shadow, Y: 4px, Blur: 6px, Color: #000000 10%
- `Shadow/LG` — Drop shadow, Y: 10px, Blur: 15px, Color: #000000 10%

**Border Radius:**
- `Radius/SM` — 4px (buttons, badges)
- `Radius/MD` — 8px (cards, inputs)
- `Radius/LG` — 12px (large cards)

**Document these visually with example rectangles**

---

## 🧩 Components Page

### Canvas Organization
Create components in this order:

---

### Component 1: Button
**Name:** "Button/Primary"

**Specifications:**
- Width: Auto (padding-based)
- Height: 40px
- Padding: 12px (horizontal) × 10px (vertical)
- Border radius: 4px
- Background: Primary/500 (#3B82F6)
- Text: Body/Normal/Medium, White
- Shadow: Shadow/SM

**Create variants:**
```
Property: State
- Default (Background: Primary/500)
- Hover (Background: Primary/600, Shadow/MD)
- Pressed (Background: Primary/600, Scale: 0.98)
- Disabled (Background: Neutral/300, Text: Neutral/500)
```

**Additional components:**
- `Button/Secondary` (Background: White, Border: 1px Neutral/300, Text: Neutral/700)
- `Button/Tertiary` (Background: None, Text: Primary/500)

---

### Component 2: Status Badge
**Name:** "Badge/Status"

**Specifications:**
- Height: 24px
- Padding: 8px (horizontal) × 4px (vertical)
- Border radius: 4px
- Text: Label/Small

**Create variants:**
```
Property: Type
- Complete (Background: Success/500 10%, Text: Success/500, Icon: ✓)
- InProgress (Background: Primary/500 10%, Text: Primary/500, Icon: ⏳)
- Queued (Background: Neutral/100, Text: Neutral/500, Icon: ⏸️)
- Warning (Background: Warning/500 10%, Text: Warning/500, Icon: ⚠️)
```

**Layout:**
```
┌────────────────┐
│ ✓ Complete     │ Green
├────────────────┤
│ ⏳ In Progress │ Blue
├────────────────┤
│ ⏸️ Queued      │ Gray
├────────────────┤
│ ⚠️ Warning     │ Yellow
└────────────────┘
```

---

### Component 3: Progress Bar
**Name:** "Progress/BMAD"

**Specifications:**
- Width: 280px
- Height: 8px
- Border radius: 4px
- Background: Neutral/100

**4-segment progress:**
```
┌────────────────────────────────┐
│ ████████░░░░░░░░░░░░░░░░░░░░   │
│ SAY   DO   TECH  BELIEVES      │
└────────────────────────────────┘
```

**Create variants:**
```
Property: Progress
- 0/4 (All gray)
- 1/4 (SAY filled, others gray)
- 2/4 (SAY + DO filled)
- 3/4 (SAY + DO + TECH filled)
- 4/4 (All filled)
```

**Each segment:**
- Width: 70px
- Gap: 4px between segments
- Filled: Success/500
- Empty: Neutral/200

---

### Component 4: Space Card
**Name:** "Card/Space"

**Specifications:**
- Width: 760px (will be responsive in layout)
- Height: Auto (padding-based)
- Padding: 24px
- Border radius: 8px
- Background: White
- Border: 1px Neutral/200
- Shadow: Shadow/SM

**Layout structure:**
```
┌──────────────────────────────────────────┐
│ 🔍 [Title]               [Status Badge]  │
│ [Progress Bar] 3/4 signals               │
│ [Metadata] • Started 12 min ago          │
│                      [Enter →] [Button]  │
└──────────────────────────────────────────┘
```

**Create variants:**
```
Property: State
- Investigating (Progress bar animating, In Progress badge)
- ReadyForReview (Progress complete, Complete badge)
- Synthesizing (Progress bar, different status text)
```

---

### Component 5: Agent Status Card
**Name:** "Card/Agent"

**Specifications:**
- Width: 280px
- Height: 320px
- Padding: 20px
- Border radius: 8px
- Background: Neutral/50
- Border: 1px Neutral/200

**Layout structure:**
```
┌────────────────────────┐
│ SAY          [✓ Badge] │
├────────────────────────┤
│                        │
│ 12 interviews          │
│ analyzed               │
│                        │
│ Key findings:          │
│ • "Turn off email      │
│   but keep Slack"      │
│   (3 quotes)           │
│                        │
│ [View All →]           │
└────────────────────────┘
```

**Create variants:**
```
Property: Type
- SAY (Icon: 💬, Title: "SAY")
- DO (Icon: 📊, Title: "DO")
- TECHNICAL (Icon: 💻, Title: "TECHNICAL")
- BELIEVES (Icon: 🎯, Title: "BELIEVES")

Property: Status
- Complete (Badge: ✓ Complete, Content visible)
- Working (Badge: ⏳ Working, Animated dots)
- Queued (Badge: ⏸️ Queued, Grayed out)
```

---

### Component 6: Coordinator Insight Card
**Name:** "Card/Coordinator"

**Specifications:**
- Width: 760px
- Height: Auto
- Padding: 24px
- Border radius: 8px
- Background: Warning/500 5%
- Border: 1px Warning/500 20%

**Layout structure:**
```
┌─────────────────────────────────────────────┐
│ 🤖 Coordinator Agent Insight                │
│                                             │
│ "Users SAY they want granular control,     │
│  but DO shows binary behavior. This         │
│  suggests granularity is desired but not    │
│  discoverable."                             │
│                                             │
│ Recommendation: Add per-channel toggles     │
│ with better UX education.                   │
│                                             │
│ Confidence: 87%                             │
└─────────────────────────────────────────────┘
```

---

### Component 7: Evidence Chain
**Name:** "Evidence/Chain"

**Specifications:**
- Width: 760px
- Height: Auto
- Tree structure with connecting lines

**Layout structure:**
```
┌──────────────────────────────────────────┐
│  Decision: Add per-channel toggles       │
│  └─┬─ SAY: "Turn off email..." (3x)     │
│    ├─ DO: 23% disable ALL (Datadog)     │
│    ├─ TECHNICAL: Service supports it     │
│    └─ BELIEVES: Q2 churn goal            │
└──────────────────────────────────────────┘
```

**Visual elements:**
- Tree lines: Neutral/300, 2px width
- Nodes: 8px circle, Primary/500
- Text: Body/Normal

---

### Component 8: Code Block
**Name:** "Code/Block"

**Specifications:**
- Width: 760px
- Height: Auto
- Padding: 16px
- Border radius: 6px
- Background: Neutral/900
- Border: 1px Neutral/700

**Layout:**
```
┌────────────────────────────────────┐
│ ```yaml                            │
│ feature: notification_preferences  │
│ files:                             │
│   - src/components/...             │
│ ```                                │
│ [Copy] [Download]                  │
└────────────────────────────────────┘
```

**Text styling:**
- Code: Fira Code, 14px, Neutral/100
- Keywords: Primary/400
- Strings: Success/400

---

## 🖼️ Screens Page

### Screen Layout Template
Each screen should be:
- **Frame size:** 1440px × 1024px (or auto height)
- **Background:** Neutral/50 (#F9FAFB)
- **Padding:** 64px (sides) × 48px (top)

---

### Screen 1: Home Dashboard
**Frame name:** "1. Home Dashboard"

**Layout grid:**
```
┌──────────────────────────────────────────────────────────┐
│  Intake                          👤 Profile  ⚙️          │ Header: 72px height
├──────────────────────────────────────────────────────────┤
│  [64px padding]                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │ ➕ New Product Decision      [Auto ▼]              │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
│  🟢 Active (3)                   [Heading/H3]           │
│  ┌────────────────────────────────────────────────────┐ │
│  │ [Space Card - Investigating variant]               │ │
│  └────────────────────────────────────────────────────┘ │
│  [16px gap]                                             │
│  ┌────────────────────────────────────────────────────┐ │
│  │ [Space Card - Ready variant]                       │ │
│  └────────────────────────────────────────────────────┘ │
│  [16px gap]                                             │
│  ┌────────────────────────────────────────────────────┐ │
│  │ [Space Card - Synthesizing variant]                │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
│  [32px gap]                                             │
│  📦 Ready for Review (2)         [Expand ▼]            │
│  🎯 Shipped to Cursor (12)       [View →]              │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

**Components to use:**
- Header (custom frame)
- Space Card component (3 instances, different variants)
- Button/Primary for "+ New Product Decision"

**Content examples:**
```
Card 1:
Title: "Notification Preferences"
Progress: 3/4 (SAY, DO, TECHNICAL complete)
Badge: ⏳ In Progress
Meta: "Started 12 min ago"
Note: "⚠️ Contradiction detected"

Card 2:
Title: "Dashboard Performance"
Progress: 4/4 (Complete)
Badge: ✓ Complete
Meta: "Ready for review • 92% confidence"

Card 3:
Title: "SSO Integration"
Progress: 2/4 (SAY, BELIEVES complete)
Badge: ⏳ In Progress
Meta: "Coordinator: Synthesizing..."
```

---

### Screen 2: Space Detail (Investigation)
**Frame name:** "2. Space Detail - Investigation"

**Layout:**
```
┌──────────────────────────────────────────────────────────┐
│  ← Back             Notification Preferences             │ Header
├──────────────────────────────────────────────────────────┤
│  [64px padding]                                          │
│  🎯 Intent                        [Heading/H4]           │
│  ┌────────────────────────────────────────────────────┐ │
│  │ "Add notification preferences so users can         │ │ Intent frame
│  │  control email vs Slack independently"             │ │
│  │ [Edit Intent]                                      │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
│  [32px gap]                                             │
│  🔍 BMAD Investigation            [Auto Mode]           │
│                                                          │
│  ┌─────────┬─────────┬─────────┬─────────┐            │
│  │ [Agent] │ [Agent] │ [Agent] │ [Agent] │            │ 4 Agent cards
│  │  SAY    │   DO    │ TECH    │ BELIEVES│            │
│  └─────────┴─────────┴─────────┴─────────┘            │
│                                                          │
│  [24px gap]                                             │
│  ⚠️ Contradiction Detected                              │
│  ┌────────────────────────────────────────────────────┐ │
│  │ [Coordinator Insight Card]                         │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
│  [Steer Investigation]  [Review Draft Spec →]          │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

**Components to use:**
- Agent Status Card (4 instances)
  - SAY: Complete variant
  - DO: Working variant (add animated dots)
  - TECHNICAL: Queued variant
  - BELIEVES: Complete variant
- Coordinator Insight Card
- Button/Secondary for "Steer Investigation"
- Button/Primary for "Review Draft Spec"

**Grid for agent cards:**
- 4 columns
- Gap: 16px between cards
- Auto layout horizontal

---

### Screen 3: Spec Review
**Frame name:** "3. Spec Review"

**Layout:**
```
┌──────────────────────────────────────────────────────────┐
│  ← Back              Notification Preferences            │
├──────────────────────────────────────────────────────────┤
│  Machine-Executable Spec    Confidence: 92% ✓           │
│                                                          │
│  📊 Evidence Chain                                       │
│  ┌────────────────────────────────────────────────────┐ │
│  │ [Evidence Chain component]                         │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
│  🎯 Implementation Plan                                  │
│  ┌────────────────────────────────────────────────────┐ │
│  │ UI/UX Changes (3)              [Expand ▼]          │ │
│  │ Data Model Updates (2)         [Expand ▼]          │ │
│  │ Business Logic (1)             [Expand ▼]          │ │
│  │ Acceptance Criteria (4)        [Expand ▼]          │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
│  📄 Cursor-Ready Output                                  │
│  ┌────────────────────────────────────────────────────┐ │
│  │ [Code Block component]                             │ │
│  │ YAML preview                                       │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
│  [Edit Spec]  [Investigate More]  [Ship to Cursor →]   │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

**Components to use:**
- Evidence Chain component
- Accordion items (create component for expandable sections)
- Code Block component
- Confidence indicator (circular progress: 92%)

---

### Screen 4: Onboarding - Step 1
**Frame name:** "4. Onboarding - Welcome"

**Layout:**
```
┌──────────────────────────────────────────────────────────┐
│                                                          │
│                  [80px from top]                         │
│               Welcome to Intake                          │ Heading/H1
│          "Cursor for Product Managers"                   │ Body/Large
│                                                          │
│  Transform scattered signals into machine-executable     │
│  specs in 90 seconds — not 4-5 days.                    │
│                                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │                                                    │ │
│  │  [Illustration placeholder: BMAD visual]          │ │ 600×300 frame
│  │  SAY → DO → TECHNICAL → BELIEVES → Spec          │ │
│  │                                                    │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
│  [Get Started →]              [Watch Demo (2 min)]      │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

**Components:**
- Button/Primary: "Get Started"
- Button/Secondary: "Watch Demo"
- Illustration frame (use placeholder or simple diagram)

---

### Screen 5: Onboarding - Step 2
**Frame name:** "5. Onboarding - Integrations"

**Layout:**
```
┌──────────────────────────────────────────────────────────┐
│  Step 1 of 3: Connect Your Data Sources                 │
│  ━━━━━━━━━━░░░░░░░░░░░░░░                               │ Progress
│                                                          │
│  Intake investigates 4 signals automatically:            │
│                                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │ SAY — What customers tell you                      │ │
│  │ [Connect Modjo] [Connect Gong] [Upload CSVs]      │ │
│  └────────────────────────────────────────────────────┘ │
│  [16px gap]                                             │
│  ┌────────────────────────────────────────────────────┐ │
│  │ DO — What customers actually do                    │ │
│  │ [Connect Datadog] [Connect Mixpanel] [Upload]     │ │
│  └────────────────────────────────────────────────────┘ │
│  [16px gap]                                             │
│  ┌────────────────────────────────────────────────────┐ │
│  │ TECHNICAL — What's possible in your codebase      │ │
│  │ [Connect GitHub] [Connect GitLab]                 │ │
│  └────────────────────────────────────────────────────┘ │
│  [16px gap]                                             │
│  ┌────────────────────────────────────────────────────┐ │
│  │ BELIEVES — What your strategy says                │ │
│  │ [Connect Notion] [Connect Confluence] [Upload]    │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
│  [Skip for Now]                        [Continue →]     │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

**Components:**
- Integration cards (create component)
- Progress bar (3-step)
- Multiple button instances

---

## 🔄 Prototype Page

### Create Interactive Prototype

**Flow to link:**
```
Home Dashboard
    ↓ Click "Enter" on Card 1
Space Detail (Investigation)
    ↓ Click "Review Draft Spec"
Spec Review
    ↓ Click "Ship to Cursor"
Success state (modal or toast)
```

**Prototype settings:**
- Device: Desktop
- Starting frame: "1. Home Dashboard"
- Transitions: Dissolve, 300ms
- Hover effects: Scale to 1.05

**Interactions to add:**
1. **Home → Space Detail**
   - Trigger: Click "Enter →" on space card
   - Action: Navigate to "2. Space Detail"
   - Animation: Slide left

2. **Space Detail → Spec Review**
   - Trigger: Click "Review Draft Spec →"
   - Action: Navigate to "3. Spec Review"
   - Animation: Slide left

3. **Spec Review → Success**
   - Trigger: Click "Ship to Cursor →"
   - Action: Open overlay (create success modal)
   - Animation: Fade in

4. **Button hover states**
   - Trigger: Mouse enter
   - Action: Change to hover variant
   - Animation: Instant

---

## ✅ Build Order Checklist

### Day 1: Foundation
- [ ] Create Figma file and pages
- [ ] Set up color styles (all 13 colors)
- [ ] Set up text styles (all 13 styles)
- [ ] Document spacing system
- [ ] Import icons (Heroicons or Lucide)
- [ ] Create shadow styles

### Day 2: Components (Part 1)
- [ ] Button component (3 variants)
- [ ] Status Badge component (4 types)
- [ ] Progress Bar component (5 states)
- [ ] Space Card component (3 states)

### Day 3: Components (Part 2)
- [ ] Agent Status Card (4 types × 3 states = 12 variants)
- [ ] Coordinator Insight Card
- [ ] Evidence Chain component
- [ ] Code Block component

### Day 4: Screens (Part 1)
- [ ] Screen 1: Home Dashboard
  - [ ] Add 3 space cards with different content
  - [ ] Add header with logo, profile, settings
  - [ ] Add "+ New Product Decision" CTA
  - [ ] Add collapsed sections ("Ready for Review", "Shipped")

### Day 5: Screens (Part 2)
- [ ] Screen 2: Space Detail
  - [ ] Add intent frame
  - [ ] Add 4 agent cards in grid
  - [ ] Add coordinator insight card
  - [ ] Add action buttons
- [ ] Screen 3: Spec Review
  - [ ] Add evidence chain
  - [ ] Add implementation plan (accordion)
  - [ ] Add code block
  - [ ] Add action buttons

### Day 6: Onboarding
- [ ] Screen 4: Welcome (Step 1)
- [ ] Screen 5: Integrations (Step 2)
- [ ] Screen 6: First Decision (Step 3)
- [ ] Screen 7: Watch BMAD (Step 4)

### Day 7: Prototype & Polish
- [ ] Link screens in prototype
- [ ] Add hover interactions
- [ ] Add success modal
- [ ] Test flow end-to-end
- [ ] Add annotations (optional)
- [ ] Export for presentation

---

## 🎨 Design Tips

### Auto Layout Best Practices
1. **Use Auto Layout for EVERYTHING** — Makes components responsive
2. **Set constraints properly** — Left/right for horizontal, top/bottom for vertical
3. **Use "Hug contents" for cards** — Let content determine size
4. **Use "Fill container" for full-width elements**

### Component Variant Tips
1. **Name properties clearly** — "State", "Type", "Status"
2. **Use booleans for toggles** — "Has Icon", "Is Selected"
3. **Keep variant structure consistent** — All variants should have same layers

### Naming Convention
```
Frame names:
- "1. Home Dashboard" (screens)
- "Button/Primary" (components)
- "Colors" (design system)

Layer names:
- "Icon/Check" (clear purpose)
- "Text/Title" (hierarchy)
- "Background" (function)
```

### Performance Tips
1. **Flatten complex illustrations** — Better performance
2. **Use components, not copy-paste** — Easier to update
3. **Organize layers** — Use groups and frames
4. **Name everything** — Helps with handoff

---

## 📤 Export & Handoff

### For Presentation
- Export PNG: 2x resolution, transparent background
- Export specific screens: Home, Space Detail, Spec Review

### For Development
- Use Figma Inspect mode
- Export icons as SVG
- Document spacing, colors, typography in Notion/Confluence

### For User Testing
- Share prototype link (set to "View only")
- Enable comments for feedback
- Test on actual users from 840+ PM list

---

## 🚀 Next Steps After Setup

1. **Share with team** — Get feedback on design system
2. **User test prototype** — Show to 3-5 PMs from your ICP
3. **Iterate based on feedback** — Especially the orchestration UI
4. **Prepare for dev handoff** — Document components, interactions
5. **Create marketing materials** — Screenshots for pitch deck

---

**Questions?** Review this guide section by section. Start with Design System, then Components, then Screens.

**Time estimate:** 5-7 full days of focused design work for complete mockup.
