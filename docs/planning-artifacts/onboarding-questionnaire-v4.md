---
title: "Guesty Pro: Smart Onboarding Questionnaire (V4)"
---

# Guesty Pro: Smart Onboarding Questionnaire (V4)

> **Target audience:** SMB accounts (5–20 listings).
> **Reference UX:** Typeform — one question per screen, generous whitespace, single confident CTA, auto-advance on selection.
> **Scope:** The online wizard between authentication+call-booking and Call 1 (Setup Call).
> **Out of scope:** Authentication, call booking flow, Airbnb OAuth itself (already built), post-questionnaire dashboard.

---

## Pre-Conditions (Available State Before Questionnaire Starts)

By the time the user lands on the cover screen, the following is known:

| Variable | Source | Notes |
|----------|--------|-------|
| `{{user_first_name}}` | Authentication | |
| `{{CSM_Name}}` | Call booking | Name of the assigned CSM |
| `{{call_date}}` | Call booking | Localized to user's timezone |
| `{{call_time}}` | Call booking | Localized to user's timezone |
| `{{timezone}}` | Call booking | |
| `{{call_countdown}}` | Computed | "in 2d 14h" — recomputed live |
| Salesforce account data | CRM lookup | `active_listing_count`, `connected_channels`, `Partners`, `industry`, `operative_account_segmentation`, `Expected_MRR__c`, `Owners`, `customer_churn_reason` |

---

## UX Principles (Typeform-Style)

1. **One question per screen.** Large type. Generous whitespace. Single focal point.
2. **Auto-advance on single-select.** No "Next" button needed when a clear choice is made.
3. **Single primary CTA per screen.** Secondary actions live as smaller links below.
4. **Animated transitions.** Slide up/down between questions.
5. **Escape hatch always visible** — but never the focal point.
6. **Save state on every interaction.** User can leave and return anytime before the call.

---

## Global UI Patterns

### Persistent Header (visible on every screen)

| Region | Element | Behavior |
|--------|---------|----------|
| **Top-left** | Progress / Section Nav | Clickable section list with status icons (`✓` done, `●` current, `○` unlocked, `🔒` locked) |
| **Top-center** | `📞 Call with {{CSM_Name}} in {{call_countdown}}` | Live countdown; subtle, non-alarming styling |
| **Top-right** | `🚪 Skip to Dashboard` | Tiered intercepts (see below) |

### Non-Linear Navigation Rules

- **Backward:** always allowed. User can revisit any answered question.
- **Forward:** only to (a) already-visited sections, or (b) the next unlocked section.
- **A section is "unlocked"** when its prerequisites are met:
  - Section 1 (Airbnb): always unlocked
  - Sections 2–7: unlocked once Section 1 is complete OR explicitly skipped
  - Section 8 (Handoff): unlocked once at least one core section (2, 3, or 5) is touched
- **Branch-skipped sections** (e.g., user delegated Financials to an accountant) appear in the nav as `→ Delegated to {{name}}` and are not revisitable from the user's side.

### Tiered Skip Intercepts

The `[🚪 Skip to Dashboard]` button's behavior adapts to investment level:

#### Tier 1 — Before Airbnb Sync (Section 1)

**System (Bot):** "I totally get it — you're ready to see Guesty in action. But if we jump in right now, your calendar and inbox will be completely empty. Give me 10 seconds to connect your Airbnb account first. It's view-only (zero risk to your live listings), and it means you'll actually have real data to play with when you hit the dashboard."

* **[Primary]** `Okay, give me 10 seconds (Connect Airbnb)`
* **[Secondary]** `I'll connect it later (Go to Dashboard)` → Safe exit; auto-pilot defaults applied (see Appendix B); persistent "Finish Setup" link in dashboard nav.

#### Tier 2 — During Operations or Communications (Sections 2–3)

**System (Bot):** "Your account is partially set up — your listings, calendar, and inbox are live. But you haven't configured **{{remaining_section}}** yet, which means you'll be setting it up manually before your first guest checks in. About 90 more seconds and you're done."

* **[Primary]** `Yes, let's finish`
* **[Secondary]** `Take me to the dashboard` → Safe exit; remaining items added to Call 1 Prep.

#### Tier 3 — During Team, Financials, or Call Prep (Sections 4–6)

**System (Bot):** "You're 80% set. The rest gets covered with **{{CSM_Name}}** on your first call — but if you've got 60 seconds, you'll walk into that call with everything ready, and we can spend it on strategy instead of setup."

* **[Primary]** `Quick finish`
* **[Secondary]** `I'll talk to {{CSM_Name}} about it` → Safe exit; items routed to call prep.

#### Tier 4 — Quick Wins (Section 7)

No intercept. Direct safe exit. Outstanding items added to Call 1 Prep silently.

---

## Section 0 — Cover Screen

**Big heading:** "Welcome, {{user_first_name}} 👋"

**Subheading:** "Your setup call with **{{CSM_Name}}** is on **{{call_date}} at {{call_time}}** ({{call_countdown}} from now)."

**Body:** "Let's get your account ready so we can use that call for strategy instead of setup."

**Reassurance row (3 chips):**
* ⏱ About 3 minutes
* ✋ Skip any question, anytime
* 🔁 Come back until your call

**Consent (tentative — pending legal/compliance review):**
> `[ ]` I authorize Guesty to configure my account (listings, messaging templates, payment rules) based on my responses. I can review and change everything later in Settings.

**[Let's get started →]** *(primary CTA, disabled until consent checked)*

---

## Section 1 — Connect Airbnb (The AHA Moment)

### Q1.1 — Airbnb Sync (first interactive step)

**Big heading:** "First — let's get your real data into Guesty."

**Body:** "Connect your Airbnb account in view-only mode. Nothing changes on Airbnb's side. Zero risk of double-bookings. About 10 seconds.

*(This is why: it means your dashboard, calendar, and inbox have your actual listings and reservations the moment you walk in — instead of empty grey screens.)*"

* **[Primary]** `Connect Airbnb (10 sec)` → Triggers existing OAuth flow
* **[Secondary]** `I'll do this later` → Triggers Tier 1 intercept

**Post-OAuth success state** *(2-second confirmation pause):*
> ✓ Synced. **{{listing_count}} listings**, **{{reservation_count}} upcoming reservations**, **{{unread_count}} unread messages**.

### Q1.2 — Post-Sync Routing
*(System analyzes live Airbnb data: `Next_Check_In_Date`)*

*Dynamic Branching:*

* *IF check-in < 48 hours away:*
  **System (Bot):** "Heads up — you have a check-in arriving in **{{hours_to_checkin}} hours**. Let's jump to **Financials** first so that payment is locked in safely."
  * **[Primary]** `Jump to Financials` → Section 5
  * **[Secondary]** `Continue in order` → Section 2

* *ELSE:*
  **System (Bot):** "Great. Next, we'll set up your turnovers and guest messaging — the two things that protect your day-to-day operations." → Auto-advance to Section 2

---

## Section 2 — Operations (Turnovers)
> *Outcome: Automate the physical turnover of the property.*

### Q2.1 — Cleaning System
*(System checks Accounts Data: `Partners`)*

*Dynamic Branching:*

* *IF `Partners` contains "Turno" or "Breezeway":*
  **System (Bot):** "We see you use **{{Partner_Name}}**. We'll auto-route your checkout data straight to them — nothing for you to set up here. ✓" → Auto-advance to Q2.2

* *ELSE:*
  **Big heading:** "How do you handle turnovers?"
  **Body:** *(Turnovers are the heartbeat of your business — every missed cleaning is a guest complaint waiting to happen.)*
  * **[A]** `In-house team`
  * **[B]** `External contractors / tool`
  * **[C]** `Not sure yet` → Bot: "No problem — most businesses your size start by managing it inside Guesty. We'll default to that for now."

### Q2.2 — Guest Access

**Big heading:** "How do guests usually get into your properties?"

**Body:** *(This is how we'll auto-generate the access info we send each guest before arrival.)*

* **[A]** `Smart Lock` → Inline dropdown: `Schlage / RemoteLock / August / Other`
* **[B]** `Lockbox / Keypad`
* **[C]** `In-person meet and greet`

---

## Section 3 — Communications (Automated Messaging)
> *Outcome: Pre-configure the messages that eat the most host time.*

### Q3.1 — Inbox & Automation Buy-In
*(Uses live Airbnb data: `Unread_Message_Count`)*

*Dynamic Branching:*

* *IF `Unread_Message_Count` > 5:*
  **Big heading:** "You've got {{unread_count}} unread messages on Airbnb right now."
  **Body:** "In Guesty, every message from every channel lands in one inbox. I can also set up automatic replies for the most common guest moments — check-in instructions, review requests — so you stop writing the same thing 30 times a week."

* *ELSE:*
  **Big heading:** "Want me to set up your automated messages?"
  **Body:** "One of Guesty's most-loved features is the Unified Inbox. I can also pre-configure automated replies for the moments that eat the most time: check-in instructions and review requests. About 30 seconds."

* **[Primary]** `Yes, set them up`
* **[Secondary]** `I'll do this later` → Skip to Section 4; flag "Automated Messaging" as Call 1 prep item

### Q3.2 — Check-In Template
*(System uses access method from Q2.2 — no new question; presents pre-drafted message for confirmation.)*

*Dynamic Branching on `access_method`:*

* **IF Smart Lock:**
  **Big heading:** "Here's your auto check-in message — sent 2 hours before arrival:"
  > *"Hi {{guest_first_name}}, you're all set for tomorrow! Your door code is {{pin_code}}. It activates at {{check_in_time}} and expires at {{check_out_time}}. Let me know if you need anything!"*
  * **[Primary]** `Use it` → Auto-advance to Q3.3
  * **[Secondary]** `Let me edit it` → Inline editor

* **IF Lockbox / Keypad:**
  **Big heading:** "Here's your auto check-in message — sent 24 hours before arrival:"
  > *"Hi {{guest_first_name}}, we're excited to host you! Your lockbox code is {{code}}. You'll find it at {{lockbox_location}}. Check-in is at {{check_in_time}}. Reach out anytime!"*
  * **[Primary]** `Use it`
  * **[Secondary]** `Let me edit it`

* **IF In-person:**
  **Big heading:** "Here's your auto pre-arrival message — sent 24 hours before:"
  > *"Hi {{guest_first_name}}, looking forward to welcoming you tomorrow! Could you confirm roughly what time you're planning to arrive? Check-in is any time after {{check_in_time}}."*
  * **[Primary]** `Use it`
  * **[Secondary]** `Let me edit it`

### Q3.3 — Review Request Automation

**Big heading:** "Auto-ask for reviews after every checkout?"

**Body:** "Properties that automatically request reviews get significantly more ratings — and more ratings mean higher Airbnb ranking. We'll send a friendly nudge 1 hour after every checkout."

* **[Primary]** `Yes, more reviews please`
* **[Secondary]** `No, I'll ask manually`

---

## Section 4 — Team & Governance
> *Outcome: Confirm who owns account decisions — feeds into Financials routing in Section 5.*

### Q4.1 — Decision Owner (SMB-Simplified)

**Big heading:** "Are you the primary owner of this account?"

**Body:** "For SMB accounts, one person usually owns admin, financials, and go-live decisions. *(Confirming this is how we know who to route account-level questions to.)*"

* **[Primary]** `Yes, I'm the primary owner`
* **[Secondary]** `Someone else owns financials` → Inline expand: name + email of the finance owner. This pre-populates Q5.1's delegation path.

> **Note:** Multi-role splits (separate Admin / Financials / Go-Live owners) are out of scope for SMB V1. The SME/Mid-Market path is documented in Appendix C.

---

## Section 5 — Financials (Revenue Protection)
> *Outcome: Lock in payment rules and mandatory fees.*

### Q5.1 — Delegation Check
*(Uses Q4.1 result.)*

*Dynamic Branching:*

* *IF Q4.1 = primary owner:*
  **Big heading:** "Ready to set up payments?"
  **Body:** "You're set as the financial owner. If you'd rather have your accountant handle this, I can send them a secure link instead."
  * **[Primary]** `I'll handle it now` → Q5.2
  * **[Secondary]** `Send to my accountant` → Inline: email field → Send secure link → Skip to Section 6

* *IF Q4.1 = delegated:*
  **Big heading:** "Send the financial setup to **{{financial_owner_name}}**?"
  **Body:** "We'll email them a secure link to complete this section. You can keep moving."
  * **[Primary]** `Send to {{financial_owner_name}}` → Skip to Section 6
  * **[Secondary]** `I'll walk through it now` → Q5.2

### Q5.2 — Payment Timing

**Big heading:** "When do you collect the balance from direct guests?"

**Body:** *(This is your default payment rule — overridable per booking later.)*

* **[A]** `100% at booking`
* **[B]** `50/50 split (half at booking, half 7 days before check-in)`
* **[C]** `What do you recommend?` → Bot: "Most businesses your size use the 50/50 split — it secures deposits early while keeping conversion rates high. Use that?" → Apply 50/50

### Q5.3 — Mandatory Fees
*(System checks Accounts Data: `industry`)*

**Big heading:** "Any mandatory fees on top of nightly rate?"

**Body:** *(Cleaning fees are already imported from Airbnb — no need to add those here.)*

*Default suggestion based on `industry`:*
* Urban → Damage Waiver highlighted
* Vacation → Resort Fee highlighted

*(Multi-select UI. Per-fee amount + unit configurable inline. "None" is a valid answer and auto-advances.)*

---

## Section 6 — Call 1 Focus ({{CSM_Name}}'s Prep)
> *Outcome: Personalize the CSM call.*

### Q6.1 — Priority Topic
*(System analyzes live Airbnb data + Onboarding Performance: `customer_churn_reason`)*

**Big heading:** "What should be the #1 topic on your call with {{CSM_Name}}?"

*Dynamic suggestion logic:*
* IF `Unread_Message_Count` > 5 AND user enabled automation in Q3.1 → Auto-suggest `Advanced Messaging Workflows`
* IF historical churn data for region/size = Accounting → Auto-suggest `Trust Accounting`
* IF user skipped Section 5 (Financials) → Auto-suggest `Financial Setup`

* **[Suggested 1]** (dynamic)
* **[Suggested 2]** (dynamic)
* **[Free text]** `Something else…`

---

## Section 7 — Quick Wins (While You're Here)
> *Outcome: High-value, low-effort items to walk into the dashboard feeling ahead.*

### Q7.1 — Owner Upload
*(System checks Accounts Data: `Owners` count)*

*Dynamic Branching:*

* *IF `Owners` = 0:* Skip this question entirely.

* *IF `Owners` > 0:*
  **Big heading:** "Upload your homeowner contacts now?"
  **Body:** "Since you manage properties for other owners, this lets us auto-generate their owner statements later. *(We won't email them until you explicitly tell us to.)*"
  * **[A]** `Upload now` → CSV picker / template download
  * **[B]** `I'll do this later`

### Q7.2 — Minimum Stay
*(System checks Accounts Data: `Partners` & live Airbnb data: `Average_Length_of_Stay`)*

*Dynamic Branching:*

* *IF `Partners` contains PriceLabs/Beyond:*
  **System (Bot):** "We see you use **{{Pricing_Partner}}**. We'll let them handle your rate strategy." → Auto-skip

* *ELSE:*
  **Big heading:** "Set a default minimum stay of 2 nights?"
  **Body:** "Your Airbnb history shows guests stay an average of **{{avg_los}} nights**. A 2-night minimum prevents 1-night calendar gaps. *(Override per property later.)*"
  * **[A]** `Yes, 2 nights`
  * **[B]** `Let me set a custom minimum…`

---

## Section 8 — Review & Hand-off
> *Outcome: Land the user on the dashboard with a clear sense of accomplishment.*

**Big heading:** "You're set, {{user_first_name}}!"

### ✓ What's Configured

* **{{listing_count}} listings** synced from Airbnb (view-only)
* **{{reservation_count}} upcoming reservations** in your calendar
* **Inbox** unified across all channels
* **Cleaning workflow:** {{cleaning_setup_summary}}
* **Guest access:** {{access_method_summary}}
* **Automated messaging:** {{messaging_setup_summary}}
* **Payment policy:** {{payment_setup_summary}}
* **Mandatory fees:** {{fees_summary}}
* **Minimum stay:** {{min_stay_summary}}

### 📞 Coming Up

* Your call with **{{CSM_Name}}** is **{{call_date}} at {{call_time}} {{timezone}}** ({{call_countdown}})
* *(Add to calendar: Google • Apple • Outlook)*

### 📋 To Cover With {{CSM_Name}}
*(Only renders if items were skipped — otherwise hidden.)*

* {{skipped_item_1}}
* {{skipped_item_2}}
* {{skipped_item_3}}

---

**[Go to Dashboard →]** *(primary)* **[View Call Prep]** *(secondary)*

---

# Appendix A — Section 8 Variable Definitions

| Variable | Source Question | Possible Output Values |
|----------|----------------|------------------------|
| `{{listing_count}}` | Airbnb sync | Integer |
| `{{reservation_count}}` | Airbnb sync | Integer (upcoming only) |
| `{{cleaning_setup_summary}}` | Q2.1 | • `Auto-routed to Turno`<br>• `Auto-routed to Breezeway`<br>• `Tracked inside Guesty (in-house team)`<br>• `Tracked inside Guesty (external contractors)`<br>• `Tracked inside Guesty (default)` — when "Not sure yet" was chosen<br>• `Not configured — covered on your call` — when skipped |
| `{{access_method_summary}}` | Q2.2 | • `Smart Lock — {{provider_name}}`<br>• `Lockbox / Keypad`<br>• `In-person meet & greet`<br>• `Not configured — covered on your call` |
| `{{messaging_setup_summary}}` | Q3.1, Q3.2, Q3.3 | • `Check-in instructions + review requests active`<br>• `Check-in instructions active`<br>• `Review requests active`<br>• `Inbox unified, automations off`<br>• `Not configured — covered on your call` |
| `{{payment_setup_summary}}` | Q5.2 | • `100% at booking`<br>• `50/50 (booking + 7 days before check-in)`<br>• `50/50 (recommended default)` — when "What do you recommend?" was chosen<br>• `Sent to your accountant for setup` — when Q5.1 delegated<br>• `Not configured — covered on your call` — when skipped |
| `{{fees_summary}}` | Q5.3 | • `None`<br>• Comma-separated list: e.g., `Damage Waiver ($25/stay), Resort Fee ($15/night)`<br>• `Not configured — covered on your call` |
| `{{min_stay_summary}}` | Q7.2 | • `2 nights (default)`<br>• `{{custom_value}} nights (custom)`<br>• `Managed by {{Pricing_Partner}}` — when partner detected<br>• `Not configured — using Airbnb defaults` |
| `{{skipped_item_N}}` | Computed | Human-readable label for each skipped section/question, e.g., `Financial setup`, `Smart messaging templates`, `Owner contacts upload` |

---

# Appendix B — Auto-Pilot Defaults

When a user skips the questionnaire (any tier), these defaults are applied to ensure a safe, functional account on first dashboard load. **Principle:** never auto-enable anything that sends messages, processes payments, or contacts a third party without explicit consent. Defaults are conservative.

| Config Item | Default When Skipped | Reasoning |
|------------|---------------------|-----------|
| **Airbnb sync** | Not connected | Cannot OAuth without user action. Dashboard shows empty-state CTA to connect. |
| **Cleaning workflow** | Tracked inside Guesty (manual) | No external integration assumed. Safe default. |
| **Guest access method** | Not set | Triggers a "complete setup" nudge on first reservation page view rather than guessing. |
| **Unified Inbox** | Active (read-only sync from Airbnb if connected) | Reading messages is safe. No auto-replies sent. |
| **Automated check-in messages** | OFF | Never send messages on behalf of the user without explicit opt-in. |
| **Review request automation** | OFF | Same reason. |
| **Team roles** | User assigned to all roles (Admin, Financials, Go-Live) | SMB default; matches the most common case. |
| **Financials — payment policy** | 100% at booking | Safest for the host; prevents cash-flow surprises. |
| **Financials — mandatory fees** | None | Never invent fees on the user's behalf. |
| **Minimum stay** | Inherited from Airbnb sync if available; else `1 night` | Don't change what's already live on Airbnb. |
| **Owner contacts** | Not uploaded | No auto-action. |
| **Call 1 prep** | All skipped items auto-flagged for CSM | The CSM picks up the slack. |
| **Consent record** | Not granted | If cover-screen consent wasn't given, no config writes happen at all — the user lands on a fully default account and is prompted to consent in-app when they first attempt a write action. |

---

# Appendix C — Deferred to V2

The following are intentionally out of V1 scope and documented here so they don't get lost:

1. **SME / Mid-Market role-split flow** — separate Admin / Financials / Go-Live owners with per-role email routing. V1 ships SMB-only with single-owner default.
2. **Profile output schema** — formal field-by-field mapping of questionnaire answers to system configuration writes. Will be defined after questionnaire UX is locked.
3. **Persistent dashboard "Call 1 Prep" widget** — UX/spec for the post-questionnaire dashboard element that surfaces skipped items, call countdown, and "Finish Setup" CTA.
4. **Non-Airbnb primary channel support** — users whose primary channel is Vrbo, Booking.com, or direct booking. V1 assumes Airbnb is primary.
5. **Multilingual templates** — guest message templates in languages other than English.
6. **Consent checkbox final wording** — pending legal/compliance review.
