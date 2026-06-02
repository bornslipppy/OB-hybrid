---
title: "Intake Figma Dimensions Reference"
---

# Intake Figma Dimensions Reference

**Quick copy-paste specs for building in Figma**

---

## 🎯 Component Dimensions

### Button/Primary
```
Width: Auto (padding-based)
Height: 40px
Padding: 12px (H) × 10px (V)
Border radius: 4px
Text: 14px Medium
Gap (icon + text): 8px
```

### Badge/Status
```
Height: 24px
Padding: 8px (H) × 4px (V)
Border radius: 4px
Text: 11px Medium
Gap (icon + text): 4px
Icon size: 12px
```

### Progress Bar (4-segment BMAD)
```
Total width: 280px
Height: 8px
Border radius: 4px
Each segment: 70px
Gap between: 4px
```

### Space Card
```
Width: 760px (or fill container)
Height: Auto
Padding: 24px
Border radius: 8px
Border: 1px
Shadow: Y:2px, Blur:4px, 10% opacity

Internal structure:
├─ Title row: 24px height
│  ├─ Icon: 20px
│  ├─ Gap: 8px
│  ├─ Title: 18px Bold
│  └─ Badge: align right
├─ Gap: 12px
├─ Progress bar: 8px height
├─ Gap: 8px
├─ Metadata text: 14px
├─ Gap: 16px
└─ Button: align right
```

### Agent Status Card
```
Width: 280px
Height: 320px (or auto)
Padding: 20px
Border radius: 8px
Border: 1px
Background: Neutral/50

Internal structure:
├─ Header: 32px height
│  ├─ Label (SAY/DO/etc): 14px Bold
│  └─ Badge: align right
├─ Gap: 16px
├─ Metric: 20px
│  └─ "12 interviews analyzed"
├─ Gap: 16px
├─ Key findings section
│  ├─ Label: 12px Medium "Key findings:"
│  ├─ Gap: 8px
│  └─ Bullet list: 14px Regular
├─ Spacer (fill remaining)
└─ Link button: 14px Medium
```

### Coordinator Insight Card
```
Width: 760px (or fill container)
Height: Auto
Padding: 24px
Border radius: 8px
Border: 1px Warning/500 20%
Background: Warning/500 5%

Internal structure:
├─ Header: 24px
│  ├─ Icon: 20px 🤖
│  ├─ Gap: 8px
│  └─ "Coordinator Agent Insight" (16px Bold)
├─ Gap: 16px
├─ Insight text: 14px Regular, line height 20px
├─ Gap: 16px
├─ Recommendation: 14px Regular
├─ Gap: 16px
└─ Confidence: 14px Medium "Confidence: 87%"
```

### Evidence Chain
```
Width: 760px
Height: Auto
Padding: 20px
Border radius: 8px
Background: Neutral/50

Tree structure:
├─ Root node: 16px Bold
├─ Vertical line: 2px width, Neutral/300
├─ Branch nodes:
│  ├─ Horizontal line: 16px length, 2px width
│  ├─ Circle: 8px diameter, Primary/500
│  ├─ Gap: 8px
│  └─ Text: 14px Regular
```

### Code Block
```
Width: 760px
Height: Auto
Padding: 16px
Border radius: 6px
Border: 1px Neutral/700
Background: Neutral/900

Internal:
├─ Code text: 14px Fira Code, Neutral/100
├─ Line height: 20px
├─ Gap (bottom): 16px
└─ Action buttons: 12px text
```

---

## 📱 Screen Layouts

### Screen 1: Home Dashboard (1440 × 1024)
```
┌──────────────────────────────────────────────────┐
│ [0, 0]           Header: 72px height             │
│ ├─ Logo: 32px @ (64, 20)                        │
│ ├─ Title: 18px @ (112, 26)                      │
│ └─ Profile + Settings: @ (1312, 20)             │
├──────────────────────────────────────────────────┤
│ [64, 120]        Content starts                  │
│                                                  │
│ [64, 120]        "+ New Product Decision"       │
│ Width: 760px, Height: 56px                      │
│                                                  │
│ [64, 200]        "🟢 Active (3)" heading        │
│ Font: 18px Bold                                 │
│                                                  │
│ [64, 240]        Space Card 1                   │
│ Width: 760px, Height: auto (~140px)             │
│                                                  │
│ [64, 396]        Space Card 2                   │
│ Gap from Card 1: 16px                           │
│                                                  │
│ [64, 552]        Space Card 3                   │
│ Gap from Card 2: 16px                           │
│                                                  │
│ [64, 740]        Collapsed sections             │
│ "📦 Ready for Review (2)"                       │
│ "🎯 Shipped to Cursor (12)"                     │
│                                                  │
└──────────────────────────────────────────────────┘
```

### Screen 2: Space Detail (1440 × 1200)
```
┌──────────────────────────────────────────────────┐
│ [0, 0]           Header: 72px                    │
│ ├─ Back button: @ (64, 26)                      │
│ └─ Title: @ (112, 26)                           │
├──────────────────────────────────────────────────┤
│ [64, 120]        Intent section                  │
│ ├─ "🎯 Intent" label: 16px Bold                 │
│ ├─ Gap: 12px                                    │
│ └─ Intent frame: 760px × auto (~100px)          │
│                                                  │
│ [64, 264]        "🔍 BMAD Investigation"        │
│ Font: 18px Bold                                 │
│                                                  │
│ [64, 312]        Agent Cards Grid               │
│ ├─ 4 columns × 1 row                            │
│ ├─ Card size: 280px × 320px each                │
│ ├─ Gap: 16px                                    │
│ └─ Total width: (280×4) + (16×3) = 1168px      │
│                                                  │
│ [64, 668]        Contradiction Alert            │
│ "⚠️ Contradiction Detected"                     │
│                                                  │
│ [64, 700]        Coordinator Card               │
│ Width: 760px, Height: auto (~180px)             │
│                                                  │
│ [64, 916]        Action buttons                 │
│ ├─ "Steer Investigation" (Secondary)            │
│ ├─ Gap: 12px                                    │
│ └─ "Review Draft Spec →" (Primary)              │
│                                                  │
└──────────────────────────────────────────────────┘
```

### Screen 3: Spec Review (1440 × 1400)
```
┌──────────────────────────────────────────────────┐
│ [0, 0]           Header: 72px                    │
│ ├─ Back + Title: @ (64, 26)                     │
│ └─ Confidence: @ (1240, 26) "92% ✓"             │
├──────────────────────────────────────────────────┤
│ [64, 120]        "📊 Evidence Chain"            │
│ Font: 16px Bold                                 │
│                                                  │
│ [64, 156]        Evidence Chain component       │
│ Width: 760px, Height: auto (~160px)             │
│                                                  │
│ [64, 348]        "🎯 Implementation Plan"       │
│ Font: 16px Bold                                 │
│                                                  │
│ [64, 384]        Accordion sections             │
│ Width: 760px                                    │
│ ├─ UI/UX Changes: 48px height (collapsed)       │
│ ├─ Gap: 8px                                     │
│ ├─ Data Model: 48px                             │
│ ├─ Gap: 8px                                     │
│ ├─ Business Logic: 48px                         │
│ ├─ Gap: 8px                                     │
│ └─ Acceptance Criteria: 48px                    │
│                                                  │
│ [64, 600]        "📄 Cursor-Ready Output"       │
│                                                  │
│ [64, 636]        Code Block                     │
│ Width: 760px, Height: auto (~240px)             │
│                                                  │
│ [64, 908]        Action buttons                 │
│ ├─ "Edit Spec" (Tertiary)                       │
│ ├─ "Investigate More" (Secondary)               │
│ └─ "Ship to Cursor →" (Primary, align right)    │
│                                                  │
└──────────────────────────────────────────────────┘
```

---

## 🎨 Grid System

### Desktop Layout (1440px)
```
Left margin: 64px
Right margin: 64px (leaves 64px gutter)
Content max width: 1312px
Primary content width: 760px
Secondary content width: 500px
```

### Component Grid (4-column Agent Cards)
```
Container: 1168px (fits in 1312px with margins)
Column width: 280px
Gap: 16px
Calculation: (280 × 4) + (16 × 3) = 1168px
```

### Vertical Rhythm
```
Section spacing: 32px (XXL)
Component spacing: 16px (M)
Internal spacing: 12px or 8px
Micro spacing: 4px (XS)
```

---

## 🔢 Quick Math

### Calculating Auto Layout Containers

**Horizontal spacing (4 cards):**
```
Total = (Card × Count) + (Gap × (Count - 1))
     = (280 × 4) + (16 × 3)
     = 1120 + 48
     = 1168px
```

**Vertical spacing (stacked cards):**
```
Total = (Card × Count) + (Gap × (Count - 1))
     = (140 × 3) + (16 × 2)
     = 420 + 32
     = 452px
```

---

## 📏 Typography Line Heights

### Optimal Readability
```
Headings (Inter Bold):
├─ H1: 32px / 40px (1.25 ratio)
├─ H2: 24px / 32px (1.33 ratio)
└─ H3: 18px / 24px (1.33 ratio)

Body (Inter Regular):
├─ Large: 16px / 24px (1.5 ratio)
├─ Normal: 14px / 20px (1.43 ratio)
└─ Small: 12px / 16px (1.33 ratio)

Code (Fira Code):
└─ Normal: 14px / 20px (1.43 ratio)
```

---

## 🎯 Alignment Reference

### Button Alignment in Cards
```
Space Card:
├─ Primary CTA: Align right, 16px from bottom
├─ From right edge: 24px padding
└─ Total from right: 40px

Agent Card:
├─ "View All →" link: Align left, 20px from bottom
└─ From left edge: 20px padding
```

### Icon + Text Alignment
```
Button with icon:
├─ Icon: 20px
├─ Gap: 8px
├─ Text: 14px (vertically centered with icon)
└─ Total height: 40px (both centered)

Badge with icon:
├─ Icon: 12px
├─ Gap: 4px
├─ Text: 11px
└─ Total height: 24px
```

---

## 🎨 Shadow Values

### CSS-to-Figma Translation
```
Shadow/SM:
├─ X: 0
├─ Y: 1px
├─ Blur: 3px
├─ Spread: 0
└─ Color: #000000 10% opacity

Shadow/MD:
├─ X: 0
├─ Y: 4px
├─ Blur: 6px
├─ Spread: -1px
└─ Color: #000000 10%

Shadow/LG:
├─ X: 0
├─ Y: 10px
├─ Blur: 15px
├─ Spread: -3px
└─ Color: #000000 10%
```

---

## 🔄 State Changes

### Interactive Element Transformations

**Button Hover:**
```
Default → Hover:
├─ Scale: 1.0 → 1.05
├─ Shadow: SM → MD
└─ Duration: 150ms
```

**Card Hover:**
```
Default → Hover:
├─ Shadow: SM → MD
├─ Border: Neutral/200 → Primary/300
└─ Duration: 200ms
```

**Progress Bar Animation:**
```
Working state:
├─ Opacity pulse: 1.0 → 0.6 → 1.0
├─ Duration: 1500ms
└─ Loop: Infinite
```

---

**Pro tip:** Keep this reference open in a second monitor or printed out while building in Figma!
