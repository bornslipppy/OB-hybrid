---
title: "Intake Figma Quick Checklist"
---

# Intake Figma Quick Checklist

**Use this as your build checklist. Check off items as you complete them.**

---

## 🎨 Design System (Day 1)

### Colors
- [ ] Primary/500 — #3B82F6
- [ ] Primary/600 — #2563EB
- [ ] Success/500 — #10B981
- [ ] Warning/500 — #F59E0B
- [ ] Error/500 — #EF4444
- [ ] Neutral/900, 700, 500, 300, 100, 50 — Grays
- [ ] White — #FFFFFF

### Typography (Inter + Fira Code)
- [ ] H1: 32px Bold
- [ ] H2: 24px Bold
- [ ] H3: 18px Bold
- [ ] Body/Large: 16px
- [ ] Body/Normal: 14px
- [ ] Body/Small: 12px
- [ ] Code: 14px Fira Code

### Spacing
- [ ] XS: 4px, S: 8px, M: 16px, L: 24px, XL: 32px, XXL: 48px

### Icons
- [ ] Import Heroicons or Lucide (20px primary)
- [ ] ✓ ⏳ ⚠️ 🔍 🎯 🤖 📊 ⚙️ 👤 ➕ ← → ▼ ▲

### Effects
- [ ] Shadow/SM, MD, LG
- [ ] Radius: 4px, 8px, 12px

---

## 🧩 Components (Days 2-3)

### Buttons
- [ ] Button/Primary (variants: default, hover, pressed, disabled)
- [ ] Button/Secondary
- [ ] Button/Tertiary

### Badges
- [ ] Badge/Status (variants: Complete, InProgress, Queued, Warning)

### Progress
- [ ] Progress/BMAD (4-segment bar, variants: 0/4, 1/4, 2/4, 3/4, 4/4)

### Cards
- [ ] Card/Space (variants: Investigating, ReadyForReview, Synthesizing)
- [ ] Card/Agent (types: SAY/DO/TECHNICAL/BELIEVES, states: Complete/Working/Queued)
- [ ] Card/Coordinator (warning style with insight text)

### Evidence & Code
- [ ] Evidence/Chain (tree structure)
- [ ] Code/Block (YAML preview)

---

## 🖼️ Screens (Days 4-6)

### Screen 1: Home Dashboard
- [ ] Header (logo, profile, settings)
- [ ] "+ New Product Decision" CTA
- [ ] 3 Space Cards (different states)
- [ ] Collapsed sections (Ready for Review, Shipped)

**Content:**
- [ ] Card 1: "Notification Preferences" (investigating, 3/4)
- [ ] Card 2: "Dashboard Performance" (ready, 4/4)
- [ ] Card 3: "SSO Integration" (synthesizing, 2/4)

### Screen 2: Space Detail
- [ ] Back button + title
- [ ] Intent frame ("Add notification preferences...")
- [ ] 4 Agent Status Cards in grid
  - [ ] SAY: Complete
  - [ ] DO: Working (animated)
  - [ ] TECHNICAL: Queued
  - [ ] BELIEVES: Complete
- [ ] Coordinator Insight Card (contradiction alert)
- [ ] Action buttons (Steer, Review Spec)

### Screen 3: Spec Review
- [ ] Back button + title + confidence (92%)
- [ ] Evidence Chain visualization
- [ ] Implementation Plan (4 accordion sections)
- [ ] Code Block (YAML preview)
- [ ] Action buttons (Edit, Investigate, Ship)

### Screen 4-7: Onboarding
- [ ] Welcome screen (intro + illustration)
- [ ] Connect integrations (4 signal sources)
- [ ] First decision setup
- [ ] Watch BMAD in action

---

## 🔄 Prototype (Day 7)

### Link Interactions
- [ ] Home → Space Detail (click "Enter")
- [ ] Space Detail → Spec Review (click "Review Draft Spec")
- [ ] Spec Review → Success modal (click "Ship to Cursor")

### Add Hover States
- [ ] All buttons scale to 1.05 on hover
- [ ] Space cards show shadow on hover

---

## 📐 Technical Specs Quick Reference

**Canvas:** 1440px width
**Page background:** #F9FAFB
**Card background:** #FFFFFF
**Padding:** 64px (sides), 48px (top)
**Component gaps:** 16px (standard), 24px (sections), 32px (major sections)

---

## ✅ Definition of Done

Your mockup is complete when:
- [ ] All 7 screens built
- [ ] All components have proper variants
- [ ] Prototype flows work (Home → Space → Spec)
- [ ] Design system documented
- [ ] Ready to share with PMs for feedback

---

**Estimated time:** 5-7 full days

**Pro tip:** Build in order: Design System → Components → Screens → Prototype. Don't skip ahead!
