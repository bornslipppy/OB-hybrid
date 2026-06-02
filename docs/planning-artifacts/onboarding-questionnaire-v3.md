---
title: "Guesty Pro: Smart Onboarding Questionnaire (V3)"
---

# Guesty Pro: Smart Onboarding Questionnaire (V3)

**Format:** Conversational, one question at a time. The system acts as a digital assistant.
**Global UI Element:** `[🚪 Skip to Dashboard]` is visible on every screen in the top right corner.

---

## 0. Global Skip Behavior (Tiered Intercepts)

The `[🚪 Skip to Dashboard]` button is always available. Its behavior adapts to how much the user has already invested — heavier resistance early, lighter as they progress.

### Tier 1 — Before Airbnb Sync (Section 1.2)

**Trigger:** User clicks Skip before completing the Airbnb sync.

**System (Bot):** "I totally get it — you're ready to see Guesty in action. But if we jump in right now, your calendar and inbox will be completely empty. Give me 10 seconds to connect your Airbnb account first. It's view-only (zero risk to your live listings), and it means you'll actually have real data to play with when you hit the dashboard."

* **[Option A — Primary]** `Okay, give me 10 seconds (Connect Airbnb)`
* **[Option B — Secondary]** `I'll connect it later (Go to Dashboard)` → *(Safe exit; auto-pilot defaults applied; persistent "Finish Setup" widget appears on dashboard.)*

### Tier 2 — During Operations or Communications (Sections 2–3)

**Trigger:** User clicks Skip after the Airbnb sync but before completing operational setup.

**System (Bot):** "Your account is partially set up — your listings, calendar, and inbox are live. But you haven't configured **{{remaining_section}}** yet, which means you'll be setting it up manually before your first guest checks in. About 90 more seconds and you're done. Want to keep going?"

* **[Option A — Primary]** `Yes, let's finish`
* **[Option B — Secondary]** `Take me to the dashboard` → *(Safe exit; remaining items added to Call 1 Prep widget.)*

### Tier 3 — During Team, Financials, or Call Prep (Sections 4–6)

**Trigger:** User clicks Skip during the back-half configuration.

**System (Bot):** "You're 80% set. The rest of this gets covered with **{{CSM_Name}}** on your first call — but if you've got 60 seconds, you'll walk into that call with everything ready and we can spend it on strategy instead of setup."

* **[Option A — Primary]** `Quick finish`
* **[Option B — Secondary]** `I'll talk to {{CSM_Name}} about it` → *(Safe exit; outstanding items routed to call prep.)*

### Tier 4 — Quick Wins (Section 7)

**Trigger:** User clicks Skip during the optional quick-wins section.

**No intercept.** Direct safe exit to the dashboard. Outstanding items added to the Call 1 Prep widget without any modal interruption.

---

## Section 1: Pre-Flight & The "AHA!" Moment
> *Outcome: Establish trust, verify CRM data, and populate the system with real data immediately.*

### Q1.1 — Active Listing Verification
*(System pulls `active_listing_count` and `connected_channels` from Salesforce)*

**System (Bot):** "Hi there! I'm your digital setup assistant. I'm getting your account perfectly tuned so your first call with **{{CSM_Name}}** is pure strategy, not just clicking buttons. I see from your profile you have **{{active_listing_count}} active listings**, mostly on **Airbnb**. Does that still look right?"

* **[Option A]** `Yes, that's right` *(Auto-advances)*
* **[Option B]** `Actually, let me update those numbers...` *(Expands quick inline editor)*

### Q1.2 — The Airbnb Sync (The AHA Moment)

**System (Bot):** "Perfect. Let's get your actual properties into Guesty so you aren't staring at a blank screen. Click below to sync your Airbnb. We only pull this in **view-only mode** — nothing changes on Airbnb's side, zero risk of double-bookings. *(This is how your dashboard, calendar, and inbox will have real data the moment you walk in.)*"

* **[Option A]** `Connect Airbnb (Takes 10 seconds)` *(Triggers OAuth modal)*
* **[Option B]** `Skip this for now` → *(Triggers Tier 1 intercept)*

*(User selects Option A. Loading animation plays. Success! Live Airbnb data is now in memory.)*

### Q1.3 — Post-Sync Routing & Urgency
*(System analyzes live Airbnb Data: `Next_Check_In_Date`)*

**System (Bot):** "Sync complete! Your business is now inside Guesty. We pulled in your listings, your calendar, and your upcoming reservations.

*Dynamic Branching based on Data:*
* *IF a check-in is < 48 hours away:* "I see you have a check-in arriving very soon! Let's jump straight to your **Financials** to ensure that payment is processed smoothly." → *(Routes to Section 5)*
* *ELSE:* "We can jump straight to your dashboard now, but I highly recommend taking 2 minutes to set up your **Turnovers** and **Messaging**. This protects your revenue and ensures your guests get a professional first touch." → *(Routes to Section 2)*

---

## Section 2: Operations (Turnovers)
> *Outcome: Automate the physical turnover of the property seamlessly.*

### Q2.1 — Cleaning System
*(System checks Accounts Data: `Partners`)*

*Dynamic Branching:*
* *IF `Partners` contains "Turno" or "Breezeway":* **System (Bot):** "We see you use **{{Partner_Name}}** for your cleaning schedules. We'll automatically route your checkout data directly to them — no setup needed on this side. ✓" *(Auto-skips to Q2.2)*
* *ELSE:*
  **System (Bot):** "Turnovers are the heartbeat of your business — every missed cleaning is a guest complaint waiting to happen. Do you run cleaning with an in-house team, or use an external tool?"
  * **[Option A]** `In-house team`
  * **[Option B]** `External contractors/tool`
  * **[Option C]** `I'm not sure what's best` → *(Bot response: "No problem! Most businesses your size manage it inside Guesty to start. Should we default to that for now?")*

### Q2.2 — Access & Smart Locks

**System (Bot):** "How do guests usually get into your properties? *(This is how we'll auto-generate the access info we send each guest before arrival.)*"

* **[Option A]** `Smart Lock` *(Inline dropdown appears: "Which provider? e.g., Schlage, RemoteLock, August")*
* **[Option B]** `Lockbox / Keypad`
* **[Option C]** `In-person meet and greet`

---

## Section 3: Communications (Automated Messaging)
> *Outcome: Pre-configure high-impact automated messages so the user's inbox works on day 1.*

### Q3.1 — Unified Inbox & Automation Buy-In
*(System checks live Airbnb data: `Unread_Message_Count`)*

*Dynamic Branching:*

* *IF `Unread_Message_Count` > 5:*
  **System (Bot):** "Quick heads-up — you have **{{unread_count}} unread messages** sitting on Airbnb right now. In Guesty, every message from every channel lands in one inbox. I can also set up automatic replies for the most common guest moments — check-in instructions, post-checkout review requests — so you're not writing the same thing 30 times a week. Want me to activate those now?"

* *ELSE:*
  **System (Bot):** "One of Guesty's most-loved features is the Unified Inbox — every guest message from every channel in one place. I can also pre-configure automated replies for the moments that eat the most time: check-in instructions and review requests. Want me to set those up now? About 30 seconds."

* **[Option A — Primary]** `Yes, set them up`
* **[Option B — Secondary]** `I'll do this later` → *(Skips to Section 4; flags "Automated Messaging" as a Call 1 prep item.)*

### Q3.2 — Check-In Instructions
*(System uses access method captured in Q2.2. No new question — presents pre-drafted message for confirmation.)*

*Dynamic Branching on `access_method`:*

* **IF Smart Lock:**
  **System (Bot):** "Since your guests use smart locks, I'll send them a unique PIN code automatically, 2 hours before arrival. Here's the message they'll get:

  > *'Hi {{guest_first_name}}, you're all set for tomorrow! Your door code is {{pin_code}}. It activates at {{check_in_time}} and expires at {{check_out_time}}. Let me know if you need anything!'*

  Want to use this, or make it yours?"
  * **[Option A]** `Looks great — use it`
  * **[Option B]** `Let me edit it` → *(Inline text editor opens)*

* **IF Lockbox / Keypad:**
  **System (Bot):** "I'll send your lockbox code automatically 24 hours before arrival. Here's the draft:

  > *'Hi {{guest_first_name}}, we're excited to host you! Your lockbox code is {{code}}. You'll find it at {{lockbox_location}}. Check-in is at {{check_in_time}}. Reach out anytime!'*

  Good to go, or want to edit?"
  * **[Option A]** `Use it`
  * **[Option B]** `Let me edit it`

* **IF In-person meet & greet:**
  **System (Bot):** "Since you meet guests in person, I'll send an automatic message 24 hours before arrival asking them to confirm their arrival time — so you're never waiting around. Here's the draft:

  > *'Hi {{guest_first_name}}, looking forward to welcoming you tomorrow! Could you confirm roughly what time you're planning to arrive? Check-in is any time after {{check_in_time}}.'*

  Use this?"
  * **[Option A]** `Yes, perfect`
  * **[Option B]** `Let me edit it`

### Q3.3 — Review Request Automation

**System (Bot):** "Last one for this section: properties that automatically ask for reviews get significantly more ratings — and more ratings mean higher ranking on Airbnb. Should I schedule a review nudge to send automatically 1 hour after every checkout?"

* **[Option A]** `Yes — more reviews, please` → *(Auto-configures post-checkout review request)*
* **[Option B]** `No, I prefer to ask manually`

---

## Section 4: Team & Governance
> *Outcome: Establish who owns account decisions — before we ask role-specific questions in Financials.*

### Q4.1 — Decision Owners
*(System checks Salesforce: `operative_account_segmentation`)*

*Dynamic Branching:*

* *IF Segment = "SMB" (< 20 listings):*
  **System (Bot):** "For businesses your size, usually one person wears all the hats. Can we list you as the primary owner for Admin, Financials, and Go-Live approvals? *(This is so we know who to route account decisions to — and so the next few financial questions go to the right person.)*"
  * **[Option A]** `Yes, I'm all three` *(Auto-resolves all roles. Section 5 defaults to "you handle financials.")*
  * **[Option B]** `No, I need to split these roles` → *(Expands role-split UI)*

* *IF Segment = "SME" or "Mid-Market":*
  **System (Bot):** "Let's set up your team. Who owns the key decisions on your Guesty account? You can split Admin, Financials, and Go-Live approvals across different people. *(This means we route the right questions to the right person — for example, financial setup can go straight to your finance lead.)*"
  * *(Role-split UI: 3 fields — Admin, Financials, Go-Live — with email + name for each. Defaults to current user; user can change/add teammates.)*

---

## Section 5: Financials (Revenue Protection)
> *Outcome: Secure payment rules and cancellation policies.*

### Q5.1 — Delegation Check
*(Uses Q4.1 role assignment.)*

*Dynamic Branching:*

* *IF Q4.1 assigned Financials role to current user:*
  **System (Bot):** "Now let's protect your revenue. You're the financial owner on this account — should we keep going, or would you prefer your accountant handle this section?"
  * **[Option A]** `I'll handle it now` *(Continues to Q5.2)*
  * **[Option B]** `Send it to my accountant instead` → *(Asks for email; sends secure link; skips to Section 6.)*

* *IF Q4.1 assigned Financials role to a different team member:*
  **System (Bot):** "Quick check — you set **{{financial_owner_name}}** as your Financials owner. Want me to send the financial setup directly to them, or would you rather walk through it together now?"
  * **[Option A]** `Send to {{financial_owner_name}}` → *(Secure link sent; skips to Section 6.)*
  * **[Option B]** `I'll walk through it now` *(Continues to Q5.2)*

### Q5.2 — Payment Timing & Split
*(System checks Salesforce: `Expected_MRR__c` and Feature Adoption data)*

**System (Bot):** "Let's make sure you get paid safely. When do you want to collect the final balance from your direct guests? *(This sets your default payment rule — it can be overridden per booking later.)*"

* **[Option A]** `100% at the time of booking`
* **[Option B]** `Split 50/50 (Half at booking, half 7 days before check-in)`
* **[Option C]** `What do you recommend?` → *(Bot: "Since your expected revenue volume is high, most businesses your size use the 50/50 split — it secures deposits early while keeping conversion rates high. Use that?")*

### Q5.3 — Mandatory Fees
*(System checks Accounts Data: `industry`)*

**System (Bot):** "Do you charge any mandatory fees on top of the nightly rate? *(Cleaning fees are already imported from Airbnb — no need to add those here.)*"

* *IF `industry` = Urban:* Highlight "Damage Waiver" as the primary default suggestion.
* *IF `industry` = Vacation:* Highlight "Resort Fee" as the primary default suggestion.

*(Multi-select UI with common fee types; per-fee amount and unit (per-night / per-stay / per-guest) configurable inline. "None" is a valid answer.)*

---

## Section 6: Call 1 Focus ({{CSM_Name}}'s Prep)
> *Outcome: Personalize the CSM call based on real data.*

### Q6.1 — Priority Topics
*(System analyzes live Airbnb Data: `Unread_Message_Count` and Onboarding Performance: `customer_churn_reason`)*

**System (Bot):** "Almost done! I want to make sure your first call with **{{CSM_Name}}** is incredibly valuable — what should be the #1 topic?"

* *Dynamic Check 1:* If unread messages > 5 AND user chose to set up automated messaging in Q3.1 → Auto-suggest `[Advanced Messaging Workflows]` ("Now that your basics are set up, {{CSM_Name}} can help you build more sophisticated message flows.")
* *Dynamic Check 2:* If historical churn data for this region/size = Accounting → Auto-highlight `[Trust Accounting]`
* *Dynamic Check 3:* If user skipped Section 5 (Financials) → Auto-highlight `[Financial Setup]`
* **[Option C]** `Something else... (Free text)`

---

## Section 7: Quick Wins (While You're Here)
> *Outcome: Surface high-value, low-effort items the user can knock out now to walk into the platform feeling ahead.*

### Q7.1 — Owner Upload
*(System checks Accounts Data: `Owners` count)*

*Dynamic Branching:*

* *IF `Owners` = 0:* Skip this question entirely.
* *IF `Owners` > 0:* **System (Bot):** "Since you manage properties for other owners, want to upload their contact list now? *(This lets us auto-generate their owner statements later — and we promise we won't email them until you explicitly tell us to.)*"
  * **[Option A]** `Upload now` *(File picker / CSV template)*
  * **[Option B]** `I'll do this later`

### Q7.2 — Rate Strategy (Minimum Stay)
*(System checks Accounts Data: `Partners` & live Airbnb Data: `Average_Length_of_Stay`)*

*Dynamic Branching:*

* *IF `Partners` contains PriceLabs/Beyond:* **System (Bot):** "We see you use **{{Pricing_Partner}}**. We'll let them handle your rate strategy." *(Auto-skips)*
* *ELSE:*
  **System (Bot):** "Looking at your Airbnb history, your average guest stays for **{{avg_los}} nights**. Should we set your default minimum stay to **2 nights** to prevent 1-night calendar gaps? *(You can override this per property later.)*"
  * **[Option A]** `Yes, 2 nights looks good`
  * **[Option B]** `Let me set a custom minimum...`

---

## Section 8: Review & Hand-off
> *Outcome: Land the user on a populated, safe dashboard — with a clear sense of accomplishment and what comes next.*

**System (Bot):** "You're set, **{{user_first_name}}**! Here's what's now live in your Guesty account:"

### ✓ What's Configured

* **{{listing_count}} listings** synced from Airbnb (view-only)
* **Calendar** populated with your upcoming reservations
* **Inbox** unified across all your channels
* **Cleaning workflow:** {{cleaning_setup_summary}}
* **Guest access:** {{access_method_summary}}
* **Automated messaging:** {{messaging_setup_summary}}
* **Payment policy:** {{payment_setup_summary}}
* **Team roles:** {{team_summary}}

### 📞 Coming Up

* Your call with **{{CSM_Name}}** is **{{call_date}} at {{call_time}} {{timezone}}**
* *(Add to calendar: Google • Apple • Outlook)*

### 📋 To Cover With {{CSM_Name}}

*(Only shows if items were skipped — otherwise hidden.)*

* {{skipped_item_1}}
* {{skipped_item_2}}
* {{skipped_item_3}}

---

**[Go to Dashboard]** *(primary)* **[View Call Prep]** *(secondary)*

*Once on the dashboard, a persistent "Call 1 Prep" widget appears in the top-right with any skipped items, the call countdown, and a "Finish Setup" CTA.*
