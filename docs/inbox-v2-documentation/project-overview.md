---
title: "Inbox v2 - Project Overview"
---

# Inbox v2 - Project Overview

**Scan Type:** Quick Scan (Pattern-Based)  
**Date:** 2026-02-11  
**Project:** inbox-v2  
**Location:** `/Users/yair.cohen/Documents/GitHub/inbox-v2`

---

## Executive Summary

**Inbox v2** is a React 18-based communications platform serving as a unified messaging hub for property management. The application handles multi-channel communications (Email, WhatsApp, Direct Messages) with intelligent features including AI-powered reply suggestions, reservation integration, and differentiated views for HQ staff and property owners.

**Architecture:** Micro-frontend with module federation, Redux state management, and multi-dimensional deployment (HQ, Owner Portal, Lite versions).

---

## Technology Stack

### Core Framework
- **React**: 18.0.0
- **React Router**: 5.2.0 (client-side routing)
- **Redux**: 4.0.4 + Redux Thunk + Redux Form
- **Styled Components**: 6.1.8 (CSS-in-JS)

### Guesty Internal Ecosystem (@guestyci packages)
- **@guestyci/arc**: UI component library (0.38.1)
- **@guestyci/arc-styles**: Design system styles (0.30.2)
- **@guestyci/foundation**: Core utilities (13.1.2)
- **@guestyci/agni**: [Component library] (5.0.1)
- **@guestyci/dio**: [Service layer] (1.19.2)
- **@guestyci/thread-message**: Thread messaging components (0.18.0)
- **@guestyci/feature-toggle-fe**: Feature flag management (2.1.5)
- **@guestyci/module-federation**: Micro-frontend orchestration (0.1.3)
- **@guestyci/localize**: Internationalization (3.3.5)

### Rich Text & Communication
- **TinyMCE**: Rich text editor (@tinymce/tinymce-react 3.3.2)
- **DOMPurify**: HTML sanitization (3.2.6)

### Testing & Quality
- **Cypress**: E2E testing (13.6.0) + visual regression (@cypress/react 7.0.3)
- **@testing-library/react**: Component testing (14.0.0)
- **Code Coverage**: @bahmutov/cypress-code-coverage

### Utilities
- **Moment.js**: Date/time manipulation (2.29.4 + timezone 0.5.45)
- **Lodash**: Utility functions (4.17.21)
- **React Virtualized / React Window**: List virtualization for performance

---

## Architecture Overview

### Multi-Dimensional Views
The application supports **3 distinct dimensions** (runtime configurations):

1. **HQ View** (`REACT_APP_DIMENSION='hq'`)
   - Full-featured staff/admin interface
   - Access to all conversations and management features

2. **Owner Portal** (`REACT_APP_DIMENSION='owner-portal'`)
   - Simplified interface for property owners
   - Limited to owner-specific conversations

3. **Default/Lite** (no dimension flag)
   - Standard user view

**Entry Points:**
- `src/App/index.js` - Main HQ application
- `src/App/OwnerPortalApp.js` - Owner portal application

### Micro-Frontend Pattern
Uses **Module Federation** (@guestyci/module-federation) to load remote widgets/modules dynamically:
- `src/App/remotes.js` - Remote module configuration
- `src/components/RemoteWidgetWrapperFT` - Feature-toggled remote widget loader

---

## Core Feature Modules

### 1. Feed (`src/App/feed/`)
**Purpose:** Main inbox feed showing conversations across all channels

**Key Components:**
- `FeedContainer.js` - Main container orchestrating feed logic
- `FeedCard.js` / `FeedCardDirect.js` - Conversation cards
- `FeedCardAltContent.js` - Alternative content view
- `FeedTopBar.js` - Search, filters, and actions
- `OwnerConversationTabs.js` - Tab navigation for owner portal
- `Person.js` / `PersonDirect.js` - Contact/participant representations
- `AddAViewModal.js` / `DeleteAViewModal.js` - Custom view management

**State Management:**
- `feedReducer.js` + `feedActions.js` + `feedSelectors.js`
- Full Redux pattern with tests

**Features:**
- Multi-channel conversation aggregation
- Custom saved views
- Real-time updates
- Virtualized list rendering (performance optimization)

### 2. Thread (`src/App/thread/`)
**Purpose:** Individual conversation thread view with message history

**Key Components:** (22 files detected)
- Full conversation threading
- Message composition and sending
- Attachment handling
- Reply/forward capabilities

**State Management:**
- Redux-managed thread state
- Integration with @guestyci/thread-message library

### 3. Email Integration (`src/App/emailIntegration/`)
**Purpose:** Email sync and company email integration

**Components:** (15 files)
- `src/components/companyEmailIntegration/` - Company-level email setup
- Personal email account connection
- Inbox synchronization
- Email-to-thread mapping

### 4. WhatsApp (`src/App/whatsApp/`)
**Purpose:** WhatsApp Business integration

**Components:** (14 files)
- WhatsApp-specific message rendering
- Media attachment support
- Template messages
- Status indicators

### 5. Reply AI (`src/App/replyAI/`)
**Purpose:** AI-powered reply suggestions and composition assistance

**Key Components:**
- `PostResponseSection.js` - AI-generated response UI
- `ReplayAIAdvancedSettings.js` - Configuration for AI behavior
- `ReplayAiPremiumFeatures.js` - Premium AI capabilities

### 6. Reservation Context (`src/App/reservation/`)
**Purpose:** Link conversations to property reservations

**State Management:**
- `reservationReducer.js` + `reservationActions.js` + `reservationSelectors.js`

**Features:**
- Reservation metadata in conversation context
- Booking details display
- Guest information integration

### 7. Guest Management (`src/App/guest/`)
**Purpose:** Guest profile and communication preferences

### 8. Widget System (`src/App/widget/`)
**Purpose:** Embeddable widgets for external views (e.g., smart locks)

**Key Components:**
- `WidgetContainerFC.js` - Functional component wrapper
- `WidgetSection.js` - Widget layout
- `useSmartLocksWidget.js` - Smart lock integration hook

**State Management:**
- `widget.reducer.js` + `widget.actions.js` + `widgetSelectors.js`

### 9. Announcements (`src/App/announcments/`)
**Purpose:** In-app notifications and announcements

**Key Components:**
- `ChannelConversationsMainAnnouncment.js` - Channel-specific announcements

### 10. App Configuration (`src/App/appConfig/`)
**Purpose:** Global app settings and configuration

**State Management:**
- `appConfigReducer.js` + `appConfigActions.js` + `appConfigSelectors.js`
- `constants.js` - Application-wide constants

---

## Shared Components (`src/components/`)

### Communication Components
- **MessageVariablesDropdown** - Variable insertion (e.g., {{guestName}})
- **AIImproveButton** - AI-powered message enhancement
- **messageImportState** - Import message handling

### UI Components
- **appBar** - Top navigation/app bar
- **IconNavBar** - Icon-based navigation
- **status** - Status indicators
- **listing** - Property listing representations
- **ErrorBoundary** - Error handling wrapper
- **LiteEmptyStateWrapper** - Empty states for lite version
- **emptyStateElements** - Generic empty state components
- **screenDimBlocker** - Modal/overlay blocker

### Reservation-Specific
- **reservationApproveDecline** - Booking approval UI
- **reservationStayIndicator** - Current/upcoming stay indicators

### Integration Components
- **OwnersDirectCreator** - Owner direct message creation
- **RemoteWidgetWrapperFT** - Feature-toggled remote widgets
- **companyEmailIntegration** - Company email setup

---

## State Management

### Redux Structure
**Store Organization:**
- `feed` - Feed state (conversations, filters, views)
- `thread` - Active thread state
- `reservation` - Reservation context
- `widget` - Widget state
- `appConfig` - Global configuration
- `layout` - UI layout preferences
- `announcements` - Announcement state

**State Containers:**
- `src/containers/ReduxProvider` - Redux store provider
- `src/containers/GLContainer` - GL (General Ledger?) container
- `src/containers/HQContainer` - HQ-specific container

### Middleware
- **Redux Thunk** - Async action handling
- **Redux Form** - Form state management

### Selectors
- Uses **Reselect** (4.0.0) for memoized selectors
- Pattern: `<module>Selectors.js` files throughout

---

## Routing & Layouts

### Layouts (`src/App/layouts/`)
- `OwnerPortalLayout.js` - Owner portal-specific layout
- `useMediaQueryToStore.js` - Responsive design hook
- Redux-managed layout state (mobile/desktop preferences)

### Router
- `src/App/routerWrapper/` - Router configuration wrapper
- React Router 5.2.0 (standard client-side routing)

---

## Testing Strategy

### E2E Testing (Cypress)
**Location:** `cypress/e2e/`
- **Lite tests:** `cypress/e2e/lite/` - Lite version-specific tests
- **Archived tests:** `cypress/archivedTests/` - Historical/deprecated tests

**Test Data:**
- `cypress/fixtures/users/` - User test data
- `cypress/fixtures/data/` - Mock data for tests

**Configuration:**
- `cypress/config/` - Environment-specific configs
- `cypress/plugins/` - Custom Cypress plugins
- `cypress/support/pre-sets/` - Test setup utilities

**Scripts:**
- `cypress:run` - Headless test execution
- `cypress:run-ci` - CI-optimized test run (TZ=UTC)
- `cypress:open` - Interactive test runner
- `cypress:run-ct` - Component tests

### Unit/Component Testing
- **React Testing Library** (14.0.0)
- **Test files:** Pattern `*.test.js` throughout codebase
  - Example: `src/App/feed/feedReducer.test.js`

### Code Coverage
- **NYC/Istanbul** via @bahmutov/cypress-code-coverage
- **Coverager** (@guestyci/coverager 1.0.31)
- Visual regression testing (cypress-image-snapshot)

---

## Internationalization (i18n)

### Localization
- **@guestyci/localize** (3.3.5)
- Translation files: `translations/` directory
- Script: `yarn translate` - Translation management

---

## Development Workflow

### Local Development
```bash
yarn start              # HQ view (default)
yarn start:hq           # Explicit HQ view
yarn start:owner        # Owner portal view
```

### Build Process
```bash
yarn build              # Production build (ESLint disabled for speed)
yarn build:local        # Local build with full linting
```

### Key Dev Features
- **Hot Reload** via Create React App
- **Custom Webpack Config** via react-app-rewired + customize-cra
- **ESLint** disabled in dev for speed (`ESLINT_NO_DEV_ERRORS=true`)
- **Code Coverage** instrumentation (@cypress/instrument-cra)

---

## Deployment

### Firebase Hosting
- **Firebase Config:** `.firebaserc` + `.firebase/` folder
- **Deploy Script:** `yarn deploy:firebase` via @guestyci/ebisu

### Docker Support
- `Dockerfile` present for containerized deployment

### CI/CD
- `.github/workflows/` - GitHub Actions workflows
- Cypress CI integration with JUnit reporting
- `yarn junit:merge` - Merge test results for CI dashboard

---

## Critical Directories

### Source Code
```
src/
├── App/
│   ├── feed/              # Main inbox feed
│   ├── thread/            # Conversation thread view
│   ├── emailIntegration/  # Email sync
│   ├── whatsApp/          # WhatsApp integration
│   ├── replyAI/           # AI reply features
│   ├── reservation/       # Reservation context
│   ├── guest/             # Guest management
│   ├── widget/            # Embeddable widgets
│   ├── announcments/      # Announcements
│   ├── appConfig/         # Global config
│   ├── layouts/           # Layout components
│   ├── account/           # Account management
│   └── routerWrapper/     # Routing config
├── components/            # Shared components
├── containers/            # Redux containers
├── hooks/                 # Custom React hooks
│   ├── useAsync/          # Async operation hook
│   └── useLazyAsync/      # Lazy async hook
├── constants/             # Constants
├── utils/                 # Utility functions
├── middleware/            # Redux middleware
└── svg/                   # SVG assets
```

### Testing
```
cypress/
├── e2e/                   # End-to-end tests
│   └── lite/              # Lite version tests
├── fixtures/              # Test data
│   ├── users/             # User fixtures
│   └── data/              # Mock data
├── support/               # Test helpers
│   └── pre-sets/          # Test setup
├── plugins/               # Cypress plugins
└── archivedTests/         # Historical tests
```

---

## Integration Points

### External Services
1. **Email Providers** - Email sync (personal + company)
2. **WhatsApp Business API** - WhatsApp messaging
3. **Firebase** - Hosting and possibly real-time features
4. **Guesty Platform** - Core PMS integration via @guestyci packages
5. **Smart Lock Systems** - Smart lock widget integration
6. **AI Services** - Reply AI functionality

### Module Federation Remotes
- Remote widgets loaded dynamically
- Configuration in `src/App/remotes.js`
- Feature-toggle controlled loading

---

## Performance Optimizations

1. **List Virtualization** - react-virtualized + react-window for long conversation lists
2. **Code Splitting** - React Router lazy loading (inferred from structure)
3. **Memoization** - @guestyci/memoize + Reselect selectors
4. **Module Federation** - Dynamic loading of widgets reduces initial bundle size

---

## Key Patterns & Conventions

### Redux Pattern
- **Reducer:** `<module>.reducer.js` or `<module>Reducer.js`
- **Actions:** `<module>.actions.js` or `<module>Actions.js`
- **Selectors:** `<module>Selectors.js` or `<module>.selectors.js`
- **Tests:** `<module>.test.js` alongside source files

### Component Naming
- **Containers:** Suffix `Container` (e.g., `FeedContainer.js`)
- **Functional Components:** Suffix `FC` (e.g., `WidgetContainerFC.js`)
- **Hooks:** Prefix `use` (e.g., `useSmartLocksWidget.js`, `useMediaQueryToStore.js`)

### File Organization
- **Co-located tests:** Tests alongside source files
- **Feature-based folders:** Each feature module is self-contained
- **Shared code:** `components/`, `hooks/`, `utils/` for reusable code

---

## Multi-Channel Support

### Supported Channels
1. **Email** - Full email integration (personal + company)
2. **WhatsApp** - WhatsApp Business messaging
3. **Direct Messages** - Platform-native messaging
4. **Reservation Messages** - Booking-related communications

### Channel-Specific Features
- **Email:** Rich text editing, attachments, threading
- **WhatsApp:** Media messages, templates, status indicators
- **Direct:** Quick replies, AI suggestions

---

## Feature Flags

- **@guestyci/feature-toggle-fe** (2.1.5)
- Feature-gated functionality throughout app
- Example: `RemoteWidgetWrapperFT` - Feature-toggled widget loading

---

## Next Steps for Deep Dive

**Recommended Deep Dive Areas (based on customer data to be analyzed):**

1. **Feed Module** - If customer feedback mentions "finding conversations" or "search issues"
2. **Reply AI** - If feedback requests more AI capabilities
3. **Email Integration** - If sync or email issues are common in support tickets
4. **WhatsApp** - If WhatsApp-specific feature requests exist
5. **Owner Portal** - If owner-specific complaints are present in feedback

---

## Quick Reference: Key Files

| Purpose | Location |
|---------|----------|
| Main App Entry | `src/App/index.js` |
| Owner Portal Entry | `src/App/OwnerPortalApp.js` |
| Redux Store Setup | `src/containers/ReduxProvider/` |
| Main Feed Container | `src/App/feed/FeedContainer.js` |
| Thread View | `src/App/thread/` |
| AI Reply Features | `src/App/replyAI/` |
| Email Integration | `src/App/emailIntegration/` |
| WhatsApp Integration | `src/App/whatsApp/` |
| Package Dependencies | `package.json` |
| Cypress E2E Tests | `cypress/e2e/` |

---

## Architecture Decisions Inferred

1. **Why Module Federation?** Allows splitting inbox into micro-frontends, enabling independent deployment of widgets
2. **Why Multiple Dimensions?** Supports different user types (HQ staff, owners) with tailored UX from same codebase
3. **Why Redux?** Complex state management across multi-channel conversations requires centralized state
4. **Why Cypress?** E2E testing critical for messaging UX where user flows span multiple interactions
5. **Why TinyMCE?** Rich text editing needed for email composition with formatting

---

**Generated by:** Document Project Workflow (Quick Scan)  
**Next Recommended Action:** Analyze customer feedback, feature requests, support tickets, and usage data to prioritize next build phase.
