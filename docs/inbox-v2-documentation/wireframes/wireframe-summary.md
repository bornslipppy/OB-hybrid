---
title: Calendar-Based Automations - Wireframe Summary
date: 2026-02-09
workflow: create-wireframe
status: COMPLETE
type: Web App (Responsive)
fidelity: Medium
style: Classic Wireframe
screens: 5
---

# Calendar-Based Automations - Wireframe Summary

## Wireframe Details

**Project**: Inbox v2 - Calendar-Based Automations
**Date Created**: February 9, 2026
**Type**: Web App (Responsive)
**Fidelity Level**: Medium (showing layout, components, and basic interactions)
**Visual Style**: Classic Wireframe (grayscale, professional)
**Total Screens**: 5

## File Locations

- **Main Wireframe**: `calendar-automations-wireframes-2026-02-09.excalidraw`
- **Theme**: `theme.json` (Classic Wireframe style)

## Screen Overview

### Screen 1: Dashboard - Calendar Triggers Tab (Collapsed View)
**Purpose**: Shows the main dashboard with a list of existing calendar triggers in their collapsed state

**Key Elements**:
- Header with "Automated Messages" title
- Tab navigation (Reservation Triggers | Calendar Triggers)
- Two example trigger cards:
  - "Trash Day Reminder" - Every Thursday at 8:00 AM
  - "Pool Service Reminder" - Monday, Wednesday, Friday at 9:00 AM
- Each card displays:
  - Trigger name
  - Schedule summary with calendar emoji
  - Active status badge (green)
  - Next send preview
- Primary CTA: "+ Add Calendar Trigger" button

**Design Notes**:
- Collapsed cards are clean and scannable
- Status badges use color coding (green for active)
- Next send preview provides immediate context

---

### Screen 2: Create New Calendar Trigger (Inline Expansion)
**Purpose**: Shows the inline expansion form for creating a new calendar trigger

**Key Elements**:
- Expanded card with teal border (indicating active state)
- **Days Selector**: 7-day circular buttons (S M T W T F S)
  - Thursday selected (teal background)
  - Quick shortcuts: "Weekdays" and "Weekends" pills
- **Time Picker**: Input showing "8:00 AM"
  - Timezone display: "EDT - Property local time"
- **Advanced Options**: Collapsible accordion (collapsed by default)
- **Next Send Preview**: Green box showing "Next send: Thu, May 18 at 8:00 AM (in 2 days)"
- **Action Buttons**: "Cancel" (secondary) and "Save" (primary)

**Design Notes**:
- Inline expansion avoids modal overlay
- Progressive disclosure with Advanced Options
- Real-time preview updates as user selects days/times
- Clear visual hierarchy with teal accent color

---

### Screen 3: Edit Existing Trigger with Warning
**Purpose**: Shows the editing experience for an active trigger with impact warning banner

**Key Elements**:
- **Warning Banner** (prominent yellow):
  - Warning icon (⚠)
  - Title: "Changing active trigger schedule"
  - Body: "This trigger is active and scheduled. Changing days/times will update future sends only. Past messages are not affected."
  - Close button (×)
- **Expanded Edit Form**:
  - Trigger name: "Trash Day Reminder"
  - Days selector showing both Thursday and Friday selected (teal)
  - Time picker showing "9:00 AM"
  - Active/Inactive toggle (currently ON)
- **Next Send Preview**: Shows updated schedule with both days
- **Action Buttons**: "Cancel" and "Save Changes"

**Design Notes**:
- Warning banner provides critical context before changes
- Multi-day selection illustrated (Thursday + Friday)
- Toggle allows users to pause trigger without deleting
- Preview updates to reflect schedule changes

---

### Screen 4: Empty State (First-Time User)
**Purpose**: Welcoming empty state when no calendar triggers exist yet

**Key Elements**:
- Large calendar emoji icon (📅)
- **Heading**: "Schedule messages by calendar"
- **Body Text**: "Set up recurring messages (trash day, pool service, lawn care) without needing reservations"
- Primary CTA: "+ Add Calendar Trigger" button

**Design Notes**:
- Friendly, inviting tone
- Clear explanation of the feature's purpose
- Examples help users understand use cases
- Single clear call-to-action

---

### Screen 5: Mobile View (Responsive Adaptation)
**Purpose**: Shows how the calendar triggers interface adapts to mobile devices (375px width)

**Key Elements**:
- **Mobile Frame**: iPhone-sized viewport (375×812px)
- **Header**: Simplified "Calendar Triggers" title
- **Trigger Card**: Stacked vertical layout
  - Compact trigger name and schedule
  - Status badge and next send on same line
- **Bottom Navigation**: Tab bar with "Reservation" and "Calendar" tabs
  - Active tab indicated with teal underline

**Design Notes**:
- Single-column layout for mobile
- Compact information density
- Bottom navigation for easy thumb access
- Maintains visual hierarchy from desktop

---

## Design System Integration

### Components Used (from @guestyci/arc)

1. **Button Component**
   - Primary: "+ Add Calendar Trigger" (teal background)
   - Secondary: "Cancel" (white with border)

2. **Badge Component**
   - Status indicators (Active/Inactive)
   - Color-coded: Green for active

3. **Tabs Component**
   - "Reservation Triggers" and "Calendar Triggers"
   - Active tab indication

4. **Input Component**
   - Time picker input field

### Custom Components (Designed)

1. **DaySelector Component**
   - 7 circular buttons for days of week
   - Multi-select capability
   - Selected state: teal background
   - Quick shortcuts: Weekdays/Weekends

2. **CalendarTriggerCard Component**
   - Collapsed state: Name, schedule, badge, next send
   - Expanded state: Full edit form
   - Inline expansion (no modal)

3. **NextSendPreview Component**
   - Green success-styled box
   - Real-time preview of next scheduled send

4. **ImpactWarningBanner Component**
   - Yellow warning color scheme
   - Icon, title, body text, dismiss button
   - Contextual display when editing active triggers

---

## Color Palette (Classic Wireframe Theme)

- **Background**: `#ffffff` (White)
- **Container**: `#f5f5f5` (Light Gray)
- **Border**: `#9e9e9e` (Gray)
- **Text**: `#424242` (Dark Gray)
- **Primary (Teal)**: `#17847B`
- **Success (Green)**: `#4CAF50`
- **Warning (Yellow)**: `#FBC02D`
- **Error (Red)**: `#EF5350`

---

## Interaction Patterns

### Primary User Flows

1. **Create New Trigger Flow**:
   - Click "+ Add Calendar Trigger"
   - New card expands inline below existing triggers
   - Select days via circular buttons or shortcuts
   - Set time via time picker
   - Preview updates in real-time
   - Click "Save" to create trigger

2. **Edit Existing Trigger Flow**:
   - Click on existing trigger card
   - Card expands inline with current settings
   - Warning banner appears if trigger is active
   - Modify days/time
   - Preview updates to show new schedule
   - Click "Save Changes" to update

3. **First-Time User Flow**:
   - User sees empty state with explanation
   - Click "+ Add Calendar Trigger"
   - Immediately enters creation flow

### Key Interaction Principles

- **Inline Expansion**: No modals, cards expand in place
- **Progressive Disclosure**: Advanced options hidden by default
- **Real-time Feedback**: Preview updates as selections change
- **Contextual Warnings**: Impact banners appear when relevant
- **Optimistic UI**: Immediate visual feedback on selections

---

## Responsive Breakpoints

Based on UX Design Specification responsive strategy:

- **Desktop** (≥1024px): Full 3-column layout with expanded cards
- **Tablet** (768px-1023px): 2-column layout, slightly compressed
- **Mobile** (≤767px): Single-column, stacked layout (as shown in Screen 5)

---

## Accessibility Considerations

- **Color Contrast**: All text meets WCAG 2.1 Level AA standards
- **Touch Targets**: Minimum 44×44px for mobile interactions
- **Keyboard Navigation**: Tab order follows visual layout
- **Screen Reader Support**: Proper ARIA labels for day selector buttons
- **Focus Indicators**: Visible focus states on all interactive elements

---

## Annotations & Design Intent

### Visual Annotations Included

1. **Screen 1**: "← Click card to expand inline (no modal)"
2. **Screen 2**: 
   - "Selected day shows teal background →"
   - "← Real-time preview updates"
3. **Screen 3**: "← Warning appears when editing active trigger"
4. **Flow Arrow**: Dashed arrow from "+ Add Calendar Trigger" to Screen 2

---

## Next Steps (Recommended)

### Implementation Phase

1. **Component Development**:
   - Build DaySelector component with arc Button base
   - Implement CalendarTriggerCard with expansion logic
   - Create NextSendPreview with calculation logic
   - Build ImpactWarningBanner with dismissal state

2. **Integration**:
   - Connect to Calendar Trigger API endpoints
   - Implement real-time preview calculations
   - Add form validation and error handling

3. **Testing**:
   - Responsive testing across breakpoints
   - Accessibility audit with screen readers
   - User acceptance testing with property managers

### Design Refinement

1. **High-Fidelity Mockups**: Convert wireframes to pixel-perfect designs in Figma
2. **Interactive Prototype**: Create clickable prototype for user testing
3. **Design QA**: Validate against arc design system tokens

---

## Files Generated

1. `calendar-automations-wireframes-2026-02-09.excalidraw` - Main wireframe file (all 5 screens)
2. `theme.json` - Classic Wireframe color theme
3. `wireframe-summary.md` - This summary document

---

## Design Credits

**UX Specialist**: Emma (BMAD Method)
**Workflow**: Create Excalidraw Wireframe v1.0
**Design System**: @guestyci/arc (Nebula)
**Inspiration**: Intercom workflows, Linear clean UI, Notion flexible layouts

---

**Status**: ✅ WIREFRAMES COMPLETE - Ready for design refinement and implementation
