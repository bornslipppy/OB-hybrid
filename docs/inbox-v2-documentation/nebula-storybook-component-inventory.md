---
title: "Nebula/Guesty Design System Component Inventory for Calendar-Based Automations"
---

# Nebula/Guesty Design System Component Inventory for Calendar-Based Automations

**Date:** 2026-02-11  
**Source:** Inbox v2 codebase analysis + UX Design Specification  
**Storybook URL:** https://livebook.guesty.com/nebula/?path=/story/introduction--introduction

> **Note:** Direct access to the Storybook at livebook.guesty.com was not possible (timeout/network). This document is compiled from **inbox-v2 codebase imports** of `@guestyci/arc`, `@guestyci/foundation`, and `@guestyci/foundation-legacy`. For visual verification and additional components, manually explore the Storybook sidebar.

---

## 1. Date/Time Components

### Current Usage in Inbox v2
| Component | Package | Usage | Status for Calendar UI |
|-----------|---------|-------|------------------------|
| **NumberInput** | `@guestyci/arc` | `OwnerDateFilterField.jsx` – days input (1–365) | ✅ Use for "days before/after" if needed |
| **Combobox** (date-related) | `@guestyci/arc` | Date filter options (e.g., "Is in the future", "Is in the past") | ✅ Use for time presets |
| **FormattedDate** | `@guestyci/localize` | `ThreadBodyLogMessage.js` – localized date display | ✅ Use for "Next send: Thu, May 18" |

### Gaps for Calendar Scheduling (from UX spec)
- **DatePicker** – Not found in current imports. Needed for optional date ranges ("📆 Date Range").
- **TimePicker** – Not found. Needed for "8:00 AM EDT – Property local time".
- **DaySelector / DayCheckboxGrid** – Not found. UX spec: "Visual day selector (checkbox grid: S M T W T F S)" with Weekdays/Weekends shortcuts.

### Recommendation
Check Nebula Storybook for: **DatePicker**, **TimePicker**, **Calendar**, **DaySelector**, **DayCheckboxGroup**. If missing, build a lightweight DaySelector using **Checkbox** or custom clickable grid styled with Arc tokens.

---

## 2. Input Components

### From @guestyci/arc (used in inbox-v2)
| Component | Key Props/Features | Usage |
|-----------|-------------------|-------|
| **Input** | Standard text input | `PersonInfo.js`, `FeedTopBar.js` |
| **Combobox** | `value`, `onValueChange`, `itemKey`, `multiple`, `disabled` | `OwnerFilterField`, `OwnerDateFilterField`, `OwnersDirectCreator`, `MemberAssigneeCombobox`, `GroupAssigneeCombobox` |
| **ComboboxTrigger** | `placeholder`, `renderTrigger` | Custom display in dropdown trigger |
| **ComboboxContent** | Wrapper for dropdown content | |
| **ComboboxSearchInput** | `placeholder`, `searchValue`, `onSearchChange` | Searchable lists |
| **ComboboxList** | `loading`, `hasMore`, `onLoadMore` | Paginated lists |
| **ComboboxItem** | `value`, `selected` | Individual options |
| **Checkbox** | Standard checkbox | `OwnerFiltersContainer.jsx` |
| **Label** | Form labels | `OwnerFiltersContainer`, `OwnerFilterField`, `OwnerDateFilterField` |
| **NumberInput** | `value`, `onChange`, `min`, `max`, `formatOptions` | `OwnerDateFilterField.jsx` |
| **TextField** | From foundation | Various forms |

### From @guestyci/foundation
| Component | Key Props | Usage |
|-----------|-----------|-------|
| **TextField** | Form text input | Throughout |
| **TextArea** | Multi-line input | `ThreadMessageBoxDirect.js` |
| **Dropdown** / **Option** | `@guestyci/foundation/Dropdown` | `ThreadTopBarIcons.js` |
| **IconDropdown** | Legacy dropdown with icon | `ThreadTopBarIcons.js` |

### Toggle
- Not directly found in current imports. Check Storybook for **Toggle** or **Switch**. UX spec mentions "Advanced" toggle for date ranges.

---

## 3. Layout Components

### From @guestyci/arc
| Component | Key Props | Usage |
|-----------|-----------|-------|
| **Row** | Flex row layout | `ThreadMessageBoxDirect`, `FeedTopBar`, `SuggestedTasks`, `OwnerFiltersTopBar` |
| **Col** | Flex column layout | `ThreadMessageBoxDirect`, `OwnerFiltersContainer`, `MessageBoxMethodsDropdown` |
| **Section** | Layout section | `SideMenuGmailTooltip.js` |

### From @guestyci/foundation
| Component | Key Props | Usage |
|-----------|-----------|-------|
| **Row** / **Col** | `@guestyci/foundation/Layout` | Layout |
| **Section** | `@guestyci/foundation/Layout` | `SideMenuGmailTooltip.js` |
| **Drawer** | `@guestyci/foundation-legacy/Drawer` | `WidgetContainerFC.js`, `FeedContainer.js` |
| **Fade** | `@guestyci/foundation-legacy/Fade` | Transitions |
| **ListItem** | `@guestyci/foundation-legacy/List` | `FeedCardDirect.js`, `FeedCard.js` |

### Card / Accordion / Collapsible
- **Card** – Not explicitly imported; check Storybook for `Card` or similar.
- **Accordion / Expandable / Collapsible** – UX spec: "Inline expandable configuration (Intercom-inspired)" for calendar trigger. Not found in current imports. Check Storybook for **Accordion**, **Collapsible**, **Expandable**.

---

## 4. Feedback Components

### From @guestyci/arc
| Component | Key Props | Usage |
|-----------|-----------|-------|
| **Badge** | Status labels | `OwnerConversationTabs.js`, `ReplayAiPremiumFeatures.js` |
| **Status** | Status indicator | `TaskDetails.js` (SuggestedTasks) |
| **Tooltip** | `TooltipTrigger`, `TooltipContent`, `TooltipProvider` | `FeedTopBar.js` |
| **Skeleton** | Loading state | `ThreadMessageBoxContainer.js`, `SuggestionPanel.js` |

### From @guestyci/foundation
| Component | Key Props | Usage |
|-----------|-----------|-------|
| **Tooltip** | `@guestyci/foundation/Tooltip` | `ThreadTopBarIcons.js`, `PersonDirect.js`, `KeyValueField.js` |
| **Badge** | `@guestyci/foundation-legacy/Badge` | `PersonDirect.js` |
| **Toast** | `useToast` from `@guestyci/foundation/Toast` | `WidgetContainerFC.js` |
| **Dialog** | `@guestyci/foundation-legacy/Dialog` | `ApproveDeclineBtns.js` |
| **Alert** | `@guestyci/foundation-legacy/Alert` | `ListingEditField.js` |

### Modal / Notification
- **Dialog** (foundation-legacy) – For warning modals: "Changing the schedule will affect future sends."
- **Toast** – For success: "✓ 24 messages sent (Thursday 8:00 AM)".
- Check Storybook for **Modal**, **Notification**, **Snackbar**.

---

## 5. Button Components

### From @guestyci/arc
| Component | Variants | Usage |
|-----------|-----------|-------|
| **Button** | `variant="plain"`, `size="default"` | `ThreadTopBar.js`, `ThreadBody.js`, `MessageBoxBottomBar.js`, `WhatsAppTemplatesButton.js` |
| **IconButton** | Icon-only | `ThreadBody.js`, `AIImproveButton.js`, `ReplyAIDropdown.js`, `ImageAttachmentButton.jsx` |

### From @guestyci/foundation
| Component | Usage |
|-----------|-------|
| **Button** | `ThreadTopBarIcons.js` (e.g., archive) |
| **RaisedButton** | `ApproveDeclineBtns.js` |
| **FixedRaisedButton** | `PreApprove.js` |

### Dropdown Menu (Arc)
| Component | Usage |
|-----------|-------|
| **DropdownMenu** | `ReplyAIDropdown.js`, `AdjustMenu.js`, `MessageBoxMethodsDropdown.js` |
| **DropdownMenuTrigger** | |
| **DropdownMenuContent** | |
| **DropdownMenuItem** | |
| **DropdownMenuLabel** | |
| **DropdownMenuSeparator** | |

---

## 6. Other Arc Components Used

| Component | Usage |
|-----------|-------|
| **Carousel**, **CarouselContent**, **CarouselItem** | `SuggestionPanel.js` |
| **Separator** | `SuggestionPanel.js` |
| **Tabs**, **TabsList**, **TabsTrigger** | `OwnerConversationTabs.js` (Calendar vs Reservation tabs) |
| **Avatar**, **AvatarImage**, **AvatarFallback** | `OwnerFilterField.jsx` |
| **useHover** | `TaskDetails.js` |

---

## 7. Visual Style (from codebase & UX spec)

### Colors
- **Primary/Teal** – Brand, calendar triggers
- **Gray** – Neutral, reservation triggers
- **Success/Active** – Green
- **Paused** – Yellow
- **Error** – Red (e.g., `red400`)
- **Theme tokens** – `@guestyci/foundation/theme/colors` (`gray50`, `white`, `blue600`, `brandBlue100`, `darkBlue800`)

### Typography
- Labels: `gst-text-sm gst-font-medium gst-text-gray-800`
- Body: regular weight
- Timestamps: small, gray

### Spacing
- Gaps: `gst-gap-1.5`, `gst-gap-2`
- Arc Tailwind-style classes: `gst-w-full`, `gst-mt-2`, etc.

---

## 8. Calendar-Based Automations – Component Mapping

| UX Requirement | Recommended Component(s) | Source |
|----------------|--------------------------|--------|
| Day selector (S M T W T F S) | Custom grid + **Checkbox** or new DaySelector | Arc / custom |
| Time picker | Check Storybook for **TimePicker** | Nebula |
| Weekdays/Weekends shortcuts | **Button** or **Checkbox** | Arc |
| Tab: Calendar vs Reservation | **Tabs**, **TabsList**, **TabsTrigger** | Arc (OwnerConversationTabs) |
| Status badges (Active/Paused/Error) | **Badge**, **Status** | Arc |
| Save/Cancel buttons | **Button** | Arc |
| Dropdowns for presets | **Combobox** | Arc |
| Inline expand/collapse | Check Storybook for **Accordion**/Collapsible | Nebula |
| Warning modal | **Dialog** (foundation-legacy) | Foundation |
| Success notification | **Toast** (`useToast`) | Foundation |
| Next send countdown text | **Text** | Arc |
| Form layout | **Row**, **Col**, **Label** | Arc |
| Loading states | **Skeleton** | Arc |

---

## 9. Next Steps

1. **Open Storybook** – Manually browse https://livebook.guesty.com/nebula/ and document any DatePicker, TimePicker, DaySelector, Accordion, Toggle, Card.
2. **Confirm Arc vs Nebula** – Inbox v2 uses `@guestyci/arc`. Confirm whether Nebula is Arc’s Storybook or a separate system.
3. **Check arc package** – After `yarn install`, inspect `node_modules/@guestyci/arc` for full exports (DatePicker, TimePicker, etc.).
4. **Prototype** – Use existing Arc components for layout and feedback; add custom DaySelector and time input if needed.
