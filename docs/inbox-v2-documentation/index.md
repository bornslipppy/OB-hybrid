# Inbox v2 - Project Documentation Index

**Documentation Generated:** 2026-02-11  
**Scan Level:** Quick Scan (Pattern-Based)  
**Project Location:** `/Users/yair.cohen/Documents/GitHub/inbox-v2`

---

## Project Overview

**Type:** React 18 SPA (Single Page Application)  
**Architecture:** Micro-frontend with Module Federation  
**Primary Purpose:** Multi-channel communications hub for property management

---

## Quick Reference

**Tech Stack:**
- **Frontend:** React 18 + Redux + Styled Components
- **Routing:** React Router 5
- **Testing:** Cypress E2E + React Testing Library
- **Deployment:** Firebase Hosting + Docker
- **Build:** Create React App (customized with react-app-rewired)

**Key Features:**
- Multi-channel inbox (Email, WhatsApp, Direct)
- AI-powered reply suggestions
- Reservation integration
- Multi-dimensional views (HQ, Owner Portal, Lite)
- Rich text editing (TinyMCE)
- Smart lock widget integration

---

## Generated Documentation

### Core Documents
- [📄 Project Overview](./project-overview.md) - Complete architecture and feature breakdown

### Documents To Be Generated
- [🏗️ Architecture Deep Dive](./architecture.md) _(To be generated)_
- [🧩 Component Inventory](./component-inventory.md) _(To be generated)_
- [🌳 Source Tree Analysis](./source-tree-analysis.md) _(To be generated)_
- [🔧 Development Guide](./development-guide.md) _(To be generated)_
- [📡 API Integration Map](./api-integration-map.md) _(To be generated)_
- [🎨 UI/UX Patterns](./ui-ux-patterns.md) _(To be generated)_

---

## Existing Documentation Found

- [README.md](../../inbox-v2/README.md) - Create React App standard documentation (121KB)

---

## Core Modules Identified

1. **Feed** - Main inbox feed with conversations
2. **Thread** - Individual conversation threads
3. **Email Integration** - Email sync and company email
4. **WhatsApp** - WhatsApp Business integration
5. **Reply AI** - AI-powered suggestions
6. **Reservation** - Booking context integration
7. **Guest** - Guest profile management
8. **Widget** - Embeddable widgets (smart locks, etc.)
9. **Announcements** - In-app notifications
10. **App Config** - Global settings

---

## Getting Started

### For AI-Assisted Development

**Use this documentation to:**
1. Understand inbox-v2 architecture before adding features
2. Reference existing patterns (Redux, component structure)
3. Identify reusable components before building new ones
4. Understand integration points for new channels

### For Product Planning

**Next Steps:**
1. ✅ **Analyze customer data** (feedback, feature requests, support tickets, usage)
2. **Identify gaps** between what exists and what customers need
3. **Prioritize features** based on pain + demand + strategic fit
4. **Create PRD** for next build phase

---

**Ready for Customer Data Analysis!** 🎯

Use the research workflow to analyze:
- Customer feedback (docx)
- Feature requests (2 CSVs)
- Support tickets (2 CSVs)
- Usage data (PDF + CSV)
