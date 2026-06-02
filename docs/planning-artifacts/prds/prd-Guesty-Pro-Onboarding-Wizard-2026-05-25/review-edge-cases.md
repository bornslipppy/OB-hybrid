---
title: "PRD Edge-Case Review — Guesty Pro Onboarding Wizard"
---

# PRD Edge-Case Review — Guesty Pro Onboarding Wizard

**Reviewer:** Adversarial Edge-Case Hunter
**Date:** 2026-05-25
**Subject:** `prd-Guesty-Pro-Onboarding-Wizard-2026-05-25/prd.md`
**Method:** Exhaustive path enumeration across each FR, Section, state machine, and integration boundary. Reports only unhandled / under-specified paths. Polite framing intentionally omitted.

---

## Verdict

The PRD is structurally strong on the happy path and on consent semantics, but it under-specifies (a) **concurrency between operator and accountant**, (b) **identity / account-shape edge cases** (multiple Guesty accounts, multiple Airbnb accounts, account swap mid-flow, re-authentication), (c) **branching invalidation under data refresh** (FR-11 is hand-waved with "doesn't retroactively re-route" but does not say what happens when the new data invalidates an earlier *answer*, not just a route), (d) **the Stripped Section 5 lifecycle** (cancel, resend, replace, accountant-disagrees-with-operator, accountant-finishes-after-operator-fills-in-themselves), and (e) **rollout / feature-flag boundary states** for the phased rollout. The Profile Output Schema is correctly flagged as a blocker but several FRs already make assumptions about its shape that may not survive contact with reality.

---

## CRITICAL severity

These describe scenarios where, as written, the Wizard can produce **wrong configuration on a live business**, **data leakage**, or **silent data loss**.

### C-1. Operator-and-accountant race on Section 5 (§4.5 / FR-26, FR-28)
**Missing scenario:** Operator chooses delegation, then changes their mind and walks Q5.2/Q5.3 themselves while the accountant is simultaneously filling out the Stripped View — last-write-wins is unspecified and the PRD's nav update language ("on completion") assumes one-sided completion.
**Fix:** Introduce a delegation lifecycle (`pending` / `in_progress` / `completed` / `cancelled` / `superseded`) where opening the stripped view by the accountant locks operator-side Section 5, or operator self-completion auto-cancels the link and emails the accountant.

### C-2. Accountant link expired but operator has already skipped Section 5 (§4.5 / FR-27)
**Missing scenario:** 14-day expiry passes before the accountant clicks the link; Section 5 remains `delegated` in operator's nav forever and never resolves; payment policy never written; Safe Exit auto-pilot was never triggered because operator did not Safe Exit.
**Fix:** Specify a delegation-expiry behavior — surface an in-app notice to the operator, revert Section 5 from `delegated` to `unlocked`, and offer "resend link" or "I'll do it myself" — and consider auto-applying Auto-Pilot Defaults after some grace period.

### C-3. Customer has two Guesty accounts under the same email/identity (§4.1 / FR-4)
**Missing scenario:** Multi-account operators (common in property management) — Wizard does not specify which Guesty account is selected, and Salesforce Account Data fetch ambiguity could load the wrong account's `Partners`, `industry`, etc., causing wrong configuration writes to the wrong live business.
**Fix:** Require an account-selection step before the Cover Screen when the authenticated user has >1 Guesty account in scope; bind the Wizard session to a single `account_id` for the duration.

### C-4. Two Airbnb accounts on one Guesty account (§4.3 / FR-13–FR-15)
**Missing scenario:** Operator connects Airbnb account A, gets sync, mid-flow returns to OAuth and adds Airbnb account B — `listing_count`, `Unread_Message_Count`, `Next_Check_In_Date` become non-deterministic across accounts; branching that already fired on account A may now contradict account B.
**Fix:** Specify single-Airbnb-connection scope for V1 and disable re-OAuth from within the Wizard; or define multi-Airbnb aggregation semantics for the five Live Airbnb Data Hooks.

### C-5. Consent Record exists but Stripped Section 5 writes occur via accountant (§4.5 / FR-28, §4.9 / FR-43)
**Missing scenario:** FR-43 says writes are Consent-Record-gated, but Consent Record is captured against the *operator's* user ID. When the accountant — a different authenticated identity who has *not* seen the consent text — completes Q5.2/Q5.3, do those writes count as authorized?
**Fix:** Explicitly state the consent model for accountant-completed writes — either operator's pre-consent covers them (and the email must surface this in the link copy), or the accountant sees a delegation-scoped consent banner before they can submit.

### C-6. Accountant Secure Link land in operator's inbox, operator opens it (§4.5 / FR-27, FR-28)
**Missing scenario:** Accountant forwards the link back to operator, or operator BCC'd themselves on the delegation email and clicks it. Operator now lands in the Stripped Section 5 View, completes it as the "accountant," and Section 5 marks done — bypassing whatever extra consent scoping the accountant flow has.
**Fix:** Require an additional weak authentication on the secure link (e.g., emailed magic code, or accountant email re-confirmation on first open) and refuse the link if the requester's session matches the operator's identity.

### C-7. Branching evaluated against stale Salesforce data after CRM update mid-session (§4.2 / FR-7, FR-4)
**Missing scenario:** Salesforce fetch is once per Wizard entry. A CSM updates `Partners` to add "Turno" in Salesforce *during* the user's session. Q2.1 still asks the user the cleaning question and writes a contradictory `cleaning_workflow` value; Q7.2 may still ask about min stay though PriceLabs was added.
**Fix:** Either accept the snapshot semantics explicitly and document the contradiction handling (last write wins on the Guesty account), or re-fetch Salesforce on each branching evaluation, or treat partner detection as authoritative at write time, not at question time.

### C-8. Salesforce `Partners` array contains conflicting members ("Turno" AND "Breezeway", or "PriceLabs" AND "Beyond") (§4.4 / FR-18, §4.6 / FR-34)
**Missing scenario:** Both partner detections fire; auto-advance copy hard-codes a single `{{Partner_Name}}`. Which wins? What is written to `cleaning_workflow`?
**Fix:** Define partner-priority order (e.g., first match wins, or operator-confirms-which) and corresponding write semantics for `cleaning_workflow` / `min_stay`.

### C-9. Write succeeds on Guesty side but Consent Record write fails (§4.1 / FR-2, §4.9 / FR-43)
**Missing scenario:** Race where Profile Configuration Writes begin while the Consent Record persistence is still in flight or has silently failed. FR-43 says "Consent Record absence is detected at every write attempt (not cached per session)" — but if the consent write itself is lost, all subsequent writes silently fail and FR-49's "queue and retry on next entry" creates a hidden config drift.
**Fix:** Require consent write to be synchronously confirmed (transactional or read-after-write verified) before the Cover Screen CTA proceeds; treat consent persistence failure as a hard block, not a non-blocking toast.

### C-10. Half-applied configuration on Safe Exit interrupted by network failure (§4.7 / FR-37, §4.9 / FR-47, FR-49)
**Missing scenario:** Safe Exit triggers a batch of Auto-Pilot Default writes; partway through the batch the network drops. Some defaults are applied, others are queued via FR-49's retry. The user lands on a dashboard that is neither fully default nor fully configured, and has no visibility into which writes survived.
**Fix:** Specify batch atomicity per write domain (FR-43 already gestures at this — "execute atomically per write domain") and define an idempotent retry sequence + a user-visible status surface for partial application.

### C-11. The "Wizard does not render — error to ops" path on missing booking values (§4.1 / FR-1)
**Missing scenario:** A real user lands on the Wizard URL with any of the five booking values missing. The PRD says the Wizard does not render — but the user is sitting in front of a broken screen with no idea why, and FR-5 also auto-redirects them here from post-booking, so this is reachable in production.
**Fix:** Define a user-facing fallback screen ("Your Setup Call info isn't ready yet — refresh in a moment, or contact your specialist") with an explicit retry CTA and a path to the dashboard.

### C-12. Q4.1 captures Financial Owner email that is the operator's own email (§4.5 / FR-25, FR-27)
**Missing scenario:** Operator enters their own email as the "someone else owns financials" Financial Owner. Secure link gets sent to them; if they click it they bypass operator-side flow (see C-6) and the system records a delegation that never happened.
**Fix:** Validate that Financial Owner email ≠ operator email; either block submit or warn ("This looks like your own email — did you mean to do it yourself?").

---

## HIGH severity

Behavior that, as specified, will produce user confusion, lost progress, or specification-defying state machines.

### H-1. Resume to "last-answered + 1" when "+1" is now invalid under new branch (§4.2 / FR-10, FR-7)
**Missing scenario:** User answers Q1.2 routes them to Section 5; they exit at Q5.1; Live Airbnb re-poll on next entry says `Next_Check_In_Date` has now slipped past 48 hours. Resume to "Q5.2" is fine — but the user's mental model said "I'm in the urgent path." FR-11 says "does not retroactively re-route" — but it does not say whether the urgent-path UI framing persists or reverts.
**Fix:** Define UI-state stickiness — once an urgent-route is taken, it remains visually framed as urgent for the rest of the session, even if data has changed.

### H-2. Backward navigation to a Question whose branching predicate has flipped (§4.2 / FR-8, FR-11)
**Missing scenario:** User answered Q3.1 with the ">5 unread" variant copy. They navigate Backward after a re-poll that now shows 2 unread. The Question copy now wants to render the other variant, but the answer is already stored. Does the variant copy update to match new data? Does the answer get cleared?
**Fix:** Specify: prior answers are immutable on Backward unless the user explicitly edits; variant copy renders the version originally shown to the user, archived per-session.

### H-3. Stripped Section 5 View — accountant disagrees with operator's Q4.1 answer (§4.5 / FR-25, FR-28)
**Missing scenario:** Operator entered Q4.1 = "Someone else owns financials, name=Jane, email=jane@x.com". Jane opens the link and the Q5.1 confirmation says "you've been asked by Marcus to set up financials" — but Jane is the bookkeeper, not the owner, and doesn't actually have authority. There is no path for Jane to push back.
**Fix:** Add a "this isn't for me" CTA on the Stripped Section 5 entry that notifies the operator and reverts Section 5 to `unlocked`.

### H-4. Accountant submits Q5.3 with implausible fees (e.g., $9999/stay) (§4.5 / FR-31)
**Missing scenario:** FR-31 sets a 4-digit max integer for fees. A bookkeeper entering Damage Waiver = $9999/stay passes validation; this writes to the live customer's payment configuration with no operator review or confirmation, and the operator only sees the result in the next Wizard load notification — by which point bookings may already be priced.
**Fix:** Require a "summary for review" step on operator's next login before fees-from-accountant are persisted to live config; or add reasonableness validation with industry-relative ranges.

### H-5. Operator completes Section 5 themselves AFTER delegation sent but BEFORE accountant clicks (§4.5 / FR-26)
**Missing scenario:** Operator delegated, then changed their mind, navigated back to Section 5 — but FR-8 says delegated Sections "are not revisitable from the nav." So operator is locked out of fixing their own mistake.
**Fix:** Add a "cancel delegation" CTA visible on the operator's Section 5 nav item when status is `delegated`, with invalidation of the outstanding secure link.

### H-6. Q5.1 delegation email send fails silently (§4.5 / FR-27)
**Missing scenario:** Email infra accepts the send but downstream bounces (invalid mailbox, spam-blocked). Operator's nav shows `→ Delegated to Jane`, but Jane never receives a link. No feedback path.
**Fix:** Specify bounce / delivery-failure handling — surface a notice to the operator on next session if delivery failed; allow resend; allow swap-email.

### H-7. User changes browser timezone mid-session (§4.1 / FR-1)
**Missing scenario:** User flies HST → ET mid-onboarding. Call countdown was rendered in HST; on return it renders in ET; the call moment displayed shifts apparently. Hours-to-checkin in Q1.2 may also flip across the 48-hour threshold from the user's perceived position.
**Fix:** Anchor all displayed times to the timezone captured at booking (`{{timezone}}`), not the browser TZ; or annotate timezone explicitly on every time render.

### H-8. Setup Call at midnight UTC for user in HST renders as same-day-evening previous day (§4.1 / FR-1)
**Missing scenario:** A call scheduled at 00:00 UTC Wednesday is 14:00 HST Tuesday. The "Thursday in 2d 14h" countdown phrasing could resolve to a wall-clock date the user doesn't expect; "Thursday" might not be Thursday in user's timezone.
**Fix:** Spell out the timezone semantics for countdown and date copy — use `{{timezone}}`-localized day and time, not UTC-day.

### H-9. Setup Call passes mid-session (countdown reaches zero while user is mid-Wizard) (§4.1 / FR-1, §4.8)
**Missing scenario:** PRD does not specify what the persistent header shows when `call_countdown` ≤ 0; what happens to Section 8's "Coming Up" copy if the call has started or finished while the user is still in the Wizard.
**Fix:** Define a "call in progress" header state and a "call past" state with appropriate copy and CTAs (e.g., "your call is happening now" / "reschedule" link).

### H-10. User finishes Wizard but Call 1 was canceled / rescheduled by CSM during the session (§4.1, §4.8 / FR-40)
**Missing scenario:** The Salesforce snapshot at entry held the original call_date; the call was canceled in CRM during session; Section 8 still renders the old date and the calendar invite is invalid.
**Fix:** Re-fetch call metadata at Section 8 render; if changed, surface a notice and provide an updated calendar add.

### H-11. Q6.1 priority topic suggestion depends on data that has changed since Section 3 (§4.6 / FR-32)
**Missing scenario:** "If `Unread_Message_Count > 5` AND Q3.1 = 'Yes'" — but `Unread_Message_Count` is re-polled on entry; the snapshot used for Q3.1's variant copy may differ from the snapshot at Q6.1.
**Fix:** Define which snapshot governs Q6.1 suggestions — the one at Q3.1 answer time, or the freshest one — and document the choice.

### H-12. Q3.2 "Use it" → backward to Q3.2 → "Let me edit it" idempotency (§4.9 / FR-45)
**Missing scenario:** FR-45 says re-writing same value is a no-op, but going from "Use it" (active template) to "edit" (template still active but content changes) is not a no-op — it's a content update that should hot-swap the live template. The PRD does not specify whether messages already queued under the old template content are updated.
**Fix:** Specify message-template update semantics — does editing affect already-queued outbound messages, only future-scheduled ones, or both?

### H-13. Cover screen consent uncheck after Wizard started (§4.1 / FR-2)
**Missing scenario:** FR-2 says unchecking does not revoke the Consent Record. But it also says re-checking persists a Consent Record — so unchecking-then-rechecking could create two Consent Records, or overwrite, with no specification.
**Fix:** Define: consent record is created once and is append-only; further toggles do not write additional records; revocation is a separate flow per FR-46.

### H-14. Feature-flag boundary mid-session during phased rollout (§14)
**Missing scenario:** User starts Wizard during Phase 2 (10% rollout); flag flips to Phase 3 (50%) overnight; user re-enters and the flag now puts them in a different cohort/variant. Conversely, a user starts at 11% then flag rolls back to 9% — user is mid-Wizard but no longer "in" the feature.
**Fix:** Specify feature-flag stickiness — once a user starts the Wizard, they stay on it regardless of subsequent flag flips, until completion or expiry; flag check happens once at entry and is persisted to session.

### H-15. User answers Q4.1 with Financial Owner, then changes Q4.1 to "primary owner" via Backward (§4.5 / FR-25, FR-26)
**Missing scenario:** Q5.1 was pre-populated with the now-orphaned Financial Owner. Does Q5.1 still offer "Send to {{financial_owner_name}}"? Is the captured name/email cleared?
**Fix:** Specify cleanup behavior — changing Q4.1 to primary clears the captured Financial Owner; if a secure link was already sent, that delegation must be cancelled.

### H-16. CSV upload at Q7.1 partial failure (§4.6 / FR-33)
**Missing scenario:** CSV has 200 rows; row 47 has a malformed email; FR-33 says "Missing required columns surface an inline error" — but row-level data errors are unspecified. Does the upload fail entirely, skip the bad row, or import 1–46?
**Fix:** Specify row-level validation behavior and reporting — likely "import valid rows, report invalid rows by line number, no partial-row writes."

### H-17. CSV upload with duplicate owner_email / property_ref (§4.6 / FR-33)
**Missing scenario:** Two rows reference the same `property_ref` with different owner data; or same owner emails on different properties; deduplication policy unspecified.
**Fix:** Define dedup keys and behavior — last-row-wins, error, or warn-and-allow.

### H-18. User who has not connected Airbnb but Salesforce shows `connected_channels = ["airbnb"]` (§4.3, §4.1 / FR-4)
**Missing scenario:** Customer connected Airbnb via a prior flow (e.g., a sales-led demo or a CSM-initiated link); Salesforce records the connection, but the Wizard's session has no live data. Q1.1 still asks them to connect even though it's already connected; or the system tries to skip Q1.1 and the live data hooks are empty.
**Fix:** Specify the cross-check between Salesforce `connected_channels` and the Wizard's own sync state; if already connected, prefill the success state and re-poll immediately rather than re-OAuth.

### H-19. Wizard expiry at 30 days passes during accountant link validity (§8 NFRs)
**Missing scenario:** Resume State expires at 30 days; Accountant Secure Link expires at 14 days. But what if the operator's session has expired (no fresh start) while a delegation link is still valid and the accountant completes the section? Does the writeback still happen?
**Fix:** Specify that accountant link is independent of operator Resume State and writes are permitted regardless; clearly document that completing the delegation does not unfreeze the expired operator session.

### H-20. User connects Airbnb account, then disconnects it from Guesty Settings mid-Wizard (§4.3 / FR-13–FR-15)
**Missing scenario:** Operator opens another browser tab, disconnects Airbnb under Settings, returns to Wizard. Live Airbnb hooks are now empty; branching on `Partners`, `Average_Length_of_Stay` is invalid.
**Fix:** Re-poll on every entry should detect disconnection; if disconnection detected mid-session, surface a "your Airbnb connection was removed — reconnect to continue" state.

### H-21. User answers Q5.3 with currency that does not match Salesforce data (§4.5 / FR-31)
**Missing scenario:** Fee inputs are "currency-formatted positive numbers" — but the PRD never specifies which currency, where it comes from (operator account default? Salesforce field? listing-level?), or what happens if listings span multiple currencies.
**Fix:** Define currency source as a single value on the operator's Guesty account; validate that fees inputs match this currency; if listings have mixed currencies, surface this.

### H-22. Auto-Pilot Default for messaging is OFF but user previously confirmed Q3.2 then Safe Exits at Section 4 (§4.7 / FR-37, §4.9 / FR-47)
**Missing scenario:** Auto-Pilot Defaults are supposed to apply "for any unanswered Question." But Q3.2 was answered "Use it" — so the check-in template is already active. Then Safe Exit triggers Auto-Pilot which says `automated_check_in_messages = OFF`. Does Auto-Pilot overwrite the active template?
**Fix:** Specify that Auto-Pilot Defaults only apply to Questions that are *unanswered*; answered Question writes are preserved.

### H-23. Q3.2 inline editor allows free editing — but stored template uses `{{guest_first_name}}` placeholders (§4.4 / FR-21)
**Missing scenario:** User edits template and removes or breaks `{{pin_code}}`, `{{guest_first_name}}` placeholders. Live outbound messages now ship with literal `{{pin_code}}` text or fail.
**Fix:** Validate edited templates against required placeholders; show inline warning or auto-restore them.

### H-24. Section 1 "explicitly skipped via Tier 1 intercept" unlocks Sections 2–7 with empty data (§4.2 / FR-8)
**Missing scenario:** Sections 2–7 unlock per FR-8 "when Section 1 is `done` OR explicitly skipped." But all the live-Airbnb-dependent branching (FR-7 conditions for Q1.2, Q3.1, Q6.1, Q7.2) silently has no signal. Are the variants chosen default? Does Q3.1 take its `>5 unread` branch when count is unknown?
**Fix:** Define the "no Airbnb data" branch for every Question that depends on Live Airbnb hooks — explicit default branch per Question.

### H-25. User clicks Skip-to-Dashboard during OAuth flow (mid-redirect to Airbnb) (§4.3 / FR-13, §4.7)
**Missing scenario:** User has bounced to Airbnb's OAuth screen; closes the tab and returns to a stale Wizard tab; clicks Skip. The Wizard does not know whether the OAuth completed or not; subsequent re-OAuth attempt may collide.
**Fix:** Specify the OAuth in-flight state — Q1.1 should track a pending-OAuth session ID and reconcile on Wizard re-entry rather than letting the user re-trigger or skip from an indeterminate state.

### H-26. "Help — what went wrong?" article does not exist at launch (§4.3 / FR-17)
**Missing scenario:** Assumption flagged ("support article exists or will be authored"). If it doesn't exist on launch day, the CTA links to nothing or a 404.
**Fix:** Make the article a launch-blocker — either author it or remove the CTA from V1.

---

## MEDIUM severity

Specification gaps that will eventually cause bugs or confusion but won't break the live business.

### M-1. Persistent header `Esc` key behavior conflict (§4.7 / FR-36)
**Missing scenario:** FR-36 says `Esc` dismisses the intercept modal without exit. But typeform-style flows often map `Esc` or arrow keys to navigation; what's the global keyboard map?
**Fix:** Define the full keyboard model: Enter (advance), arrows (Backward/Forward where allowed), Esc (close modals only).

### M-2. Multi-select "None" pseudo-option interaction with other selections (§4.5 / FR-31, §4.2 / FR-6)
**Missing scenario:** Q5.3 allows multi-select including "None." What if user selects "None" plus another fee? Mutually exclusive or last-clicked wins?
**Fix:** "None" selection clears all other selections and locks them; selecting another option clears "None."

### M-3. Free-text limits not enforced consistently (§4.4, §4.6)
**Missing scenario:** Q2.2 "Other" smart-lock provider is 60 chars; Q6.1 priority topic is 200; Q7.2 custom min-stay is integer 1–14. PRD does not specify behavior at the boundary — truncation, hard stop, validation error.
**Fix:** Document input behavior at each limit (hard cap with counter visible at 80% of limit).

### M-4. Q6.1 suggestion logic when ALL three IFs fire simultaneously (§4.6 / FR-32)
**Missing scenario:** "Up to two suggestions" — what if 3 conditions match? Which two?
**Fix:** Specify ordering (most-recent-event-driven first?) or rank the three rules explicitly.

### M-5. Tier intercept triggered while a write is in flight (§4.7 / FR-35, §4.9 / FR-49)
**Missing scenario:** User clicks Skip after answering Q5.2; the write is mid-flight; Safe Exit applies Auto-Pilot to "unanswered" Questions. Race on whether Q5.2 is considered answered.
**Fix:** Drain in-flight writes before evaluating Auto-Pilot scope; otherwise apply Auto-Pilot only for Questions with no pending write.

### M-6. Browser refresh during Section 8 render (§4.8 / FR-39)
**Missing scenario:** User refreshes on Section 8; PRD says all Questions in branch path answered → resume at Section 8. Fine — but the calendar-add buttons (FR-40) may regenerate fresh tokens / files; idempotency unspecified.
**Fix:** Calendar entries are stable per-session; refresh does not invalidate previous calendar adds.

### M-7. Section 8 renders with no Airbnb sync (Tier 1 safe-exited user later returns) (§4.2 / FR-8, §4.8 / FR-39)
**Missing scenario:** Section 8 unlock condition is "at least one of Sections 2, 3, or 5 has been touched." Can be reached without Section 1. `{{listing_count}}` etc. are 0 / null. FR-39 says "appropriate empty-state copy" — but the empty-state copy is unspecified.
**Fix:** Author the empty-state copy explicitly; surface "Connect Airbnb later from your dashboard" CTA.

### M-8. Multiple concurrent Wizard sessions for same user (§4.2 / FR-9, FR-10)
**Missing scenario:** User opens Wizard in two browser tabs. Both write to Resume State. Last-write-wins; earlier tab's answers may be lost without notice.
**Fix:** Single-session lock with an "another tab is open" notice; or last-write-wins with a session-update toast.

### M-9. Section nav back to Section 1 after sync — what does Q1.1 show? (§4.3, §4.2 / FR-8)
**Missing scenario:** Backward to Q1.1 after successful sync; does it show the original "Connect Airbnb" CTA, the success state, or a "you're already connected, continue" affordance?
**Fix:** Define Q1.1 post-sync re-render — show the persistent success state with the "✓ Synced" summary, no re-OAuth.

### M-10. WCAG 2.1 AA for auto-advance UX (§8 NFRs, §4.2 / FR-6)
**Missing scenario:** Auto-advance on single-select can disorient screen-reader users — focus moves without warning. FR-6 doesn't address screen-reader behavior.
**Fix:** Auto-advance only after the screen reader announces the selection; provide an accessibility-mode toggle that requires explicit Continue.

### M-11. Persistent "Finish Setup" link visibility race with completion (§4.1 / FR-5)
**Missing scenario:** Link disappears when all Sections are `done` or `delegated.` But `delegated` sections may transition back to `unlocked` (per H-2/H-5/C-2). The link's visibility logic is reactive — when do these transitions update the dashboard?
**Fix:** Specify that the "Finish Setup" link visibility is computed on every dashboard load (not cached), and a Section returning to `unlocked` re-shows the link.

### M-12. Q3.2 access method changed via Backward after template was activated (§4.4 / FR-21)
**Missing scenario:** User accepted "Use it" with Smart Lock template; Backward to Q2.2; change access to Lockbox/Keypad; Q3.2 now wants a different template variant. The activated template — is it deactivated, swapped, or duplicated?
**Fix:** Changing Q2.2 invalidates the Q3.2 answer and reverts Q3.2 to its unanswered state with the new variant; the previously-activated template is deactivated.

### M-13. Branching depends on `customer_churn_reason` for "region/size" (§4.6 / FR-32)
**Missing scenario:** What if there's no churn data for the user's specific region/size cohort? Branch fallback unspecified.
**Fix:** Default to "no suggestion" branch when data is absent; never display "Trust Accounting" speculatively.

### M-14. Operator's first name has special characters / very long (§4.1 / FR-1)
**Missing scenario:** Names with apostrophes, RTL characters, very long names, or empty strings; cover screen "Welcome, {{user_first_name}}" rendering.
**Fix:** Specify max length (truncate at 30 chars with ellipsis), HTML-escape, fallback for empty.

### M-15. CSM `{{CSM_Name}}` not yet assigned at booking time (§4.1 / FR-1, §13)
**Missing scenario:** Round-robin CSM assignment can be deferred; what if booking occurred but CSM is TBD?
**Fix:** Treat as a missing booking value per FR-1 fallback; or show a generic "your Setup Specialist" copy.

### M-16. Q5.2 "What do you recommend?" path UX timing (§4.5 / FR-30)
**Missing scenario:** "Recommend" applies the 50/50 default after the bot recommendation — but what if user changes their mind mid-recommendation? Is there a confirm step?
**Fix:** Recommendation is a two-step: show recommendation copy → explicit confirm CTA → write.

### M-17. Wizard URL deep-link to a Section the user hasn't unlocked (§11)
**Missing scenario:** PRD says "Section navigation does not change the URL by Section in V1." But if a user bookmarks the URL mid-session, returns later — what about deep links a CSM might share?
**Fix:** Bookmark always resolves to last-answered Question per Resume State; CSM sharing of Wizard URL is not supported.

### M-18. Q7.2 `avg_los` for new host (zero history) (§4.6 / FR-34)
**Missing scenario:** Brand-new Airbnb host has no `Average_Length_of_Stay`. Bot copy references it directly.
**Fix:** Branch when `avg_los` is null — show alternate copy without the data reference.

### M-19. Multilingual user with English-only V1 (§5, §16 Open Q5)
**Missing scenario:** Operator's Airbnb data contains non-English guest names, listing titles; Q3.2 template includes `{{guest_first_name}}` — what if the guest name uses non-Latin script?
**Fix:** Templates are UTF-8 safe; document that user-facing Wizard UI is English-only, but template variable values may be in any language.

### M-20. Calendar add fails (FR-40) — no fallback to manual entry (§4.8)
**Missing scenario:** Google Calendar API failure, malformed ICS, etc. — no recovery path defined.
**Fix:** Fallback to a copyable "details" block with call time/CSM/link.

### M-21. Q1.2 fast-tracks to Section 5; user then Backwards from Section 5 (§4.3 / FR-16, §4.2 / FR-8)
**Missing scenario:** Backward from Section 5 goes where? Back to Section 1? To the Q1.2 routing prompt?
**Fix:** Backward navigation order is defined by the linear V4 order, not by the fast-track route; or persistent "you fast-tracked here, go back to Section 2 to continue normally" affordance.

### M-22. Profile Output Schema isn't locked before MVP scope is shared with engineering (§4.9 / FR-44, §6, §16 Open Q3)
**Missing scenario:** PRD flags this as a blocker but does not specify what happens if the schema slips. Without it, FRs FR-43, FR-45, FR-47 cannot be implemented or tested.
**Fix:** Make schema lock a gating milestone in §14 rollout; Phase 1 cannot start without it.

### M-23. "non-blocking toast" wording / behavior unspecified across many FRs (§4.2 / FR-9, FR-11, FR-12, §4.9 / FR-49)
**Missing scenario:** "Non-blocking toast" semantics — duration, dismissal, max queued toasts, A11y announcements — not specified.
**Fix:** Define a shared toast component spec used across FRs.

### M-24. Section 5 stripped view — failed authentication "single error page" exposes nothing — but what about the operator? (§4.5 / FR-29)
**Missing scenario:** Accountant gets a "link expired" page; does the operator get any notification? PRD only specifies "no operator data leaked," not whether the operator is alerted.
**Fix:** Specify that operator receives an in-app notice when accountant hits an expired/invalid link state.

### M-25. Per-Question skip surfaces same Tier as Section (§4.2 / FR-6) — but Tier 3 (Sections 4–6) spans Section 5 (financials) where data sensitivity is highest (§4.7 / FR-35)
**Missing scenario:** Per-Question skip from inside Section 5 surfaces Tier 3 generic copy, but financials has a stronger consequence (skipped financials means default payment policy is conservative but not necessarily right). Tier copy doesn't differentiate.
**Fix:** Specify per-Section skip copy overrides where the consequences are materially different (Section 5 has its own copy).

### M-26. The bot "voice" — is it text-only? Animated? Avatar? (§10, multiple FRs)
**Missing scenario:** V4 uses "System (Bot):" framing extensively; PRD doesn't specify whether the bot is a visual character, just typography, or something else.
**Fix:** Define the bot UX surface (likely a stylized text bubble) and reference it consistently.

### M-27. Section 1 "explicitly skipped via Tier 1 intercept" creates an OAuth-able-later state — but what if Auto-Pilot already wrote `unified_inbox = active`? (§4.7 / FR-37, V4 Appendix B)
**Missing scenario:** Auto-Pilot says "Unified Inbox active (read-only sync from Airbnb if connected)" — but no Airbnb connection. The "if connected" branch is hand-waved; what does "active inbox, no source" look like?
**Fix:** Specify inbox state when no source is connected — empty inbox with a "connect a channel" CTA.

### M-28. Two delegations sent to the same accountant for two different operators (§4.5 / FR-27)
**Missing scenario:** Accountant Jane manages financials for Marcus AND for another Guesty operator. She receives two secure links; they should be independently scoped. PRD says "URL is unique per delegation" — fine — but does Jane's session token persist across the two? Cross-contamination risk?
**Fix:** Each secure link starts a fresh, scoped session; no cross-link state sharing; explicit document in FR-28.

### M-29. Multi-monitor or full-screen split with persistent header (§3, §10)
**Missing scenario:** Wizard at narrow widths (split-screen on desktop) — persistent header may overflow or wrap. Mobile is explicitly out, but desktop at narrow widths is in.
**Fix:** Specify minimum viewport width supported (e.g., 1024px); below that, show "best experienced wider" copy.

### M-30. Phase 1 dogfood with employees — real Salesforce records? (§14)
**Missing scenario:** Internal dogfood requires test accounts; what about Salesforce data sources? Employees may not have realistic `Partners`, `industry`, etc.
**Fix:** Define a test-account seeding plan for Phase 1; or accept that branching logic won't be fully exercised in Phase 1.

---

## LOW severity

Niceties and small-population edge cases.

### L-1. Cover screen "Welcome, {{user_first_name}} 👋" — emoji rendering varies (§4.1 / FR-1)
**Fix:** Use a font-stack that renders waving-hand consistently across Chrome/Edge/Firefox/Safari; or use SVG.

### L-2. Countdown phrasing for very-near calls (call in 8 minutes) (§4.1 / FR-1)
**Fix:** Define <1 hour copy ("in 45 minutes"), <5 minutes ("starting soon"), and post-start.

### L-3. Calendar add ICS file for users with no default calendar handler (§4.8 / FR-40)
**Fix:** Default to ICS download for "Other" calendar; document on UX side.

### L-4. Q7.1 CSV template download — what if user uploads modified template with extra columns? (§4.6 / FR-33)
**Fix:** Ignore extra columns silently; validate only required ones.

### L-5. Branding / co-brand for white-label partners (§9, §10)
**Fix:** Out of scope explicit — Wizard is Guesty-branded only in V1.

### L-6. Free-text Q6.1 abuse / XSS / prompt-injection (§4.6 / FR-32)
**Fix:** Sanitize free-text on render to CSM-facing surfaces and to Salesforce; document the encoding.

### L-7. Skipped item labels — translation when source Question copy was variant (§4.8 / FR-41)
**Fix:** "Smart messaging templates" label is variant-agnostic; document mapping.

### L-8. SM-4 "Resume rate" metric definition — does an OAuth-redirect-bounce count as a resume? (§7)
**Fix:** Resume = re-entry initiated by the user from outside the Wizard surface after >1 minute of inactivity; OAuth bounce excluded.

### L-9. Cover screen renders before consent: does it count as an SM-2 impression? (§7)
**Fix:** SM-2 impression fires on first paint, regardless of consent state.

### L-10. NFR "First Question render under 2s P95" — is this from URL nav or from CTA click? (§8)
**Fix:** Define start of timer (navigation start) and end (first contentful paint of Question content).

### L-11. Phase 2 (10% rollout) — random sampling vs. CSM-controlled allocation? (§14)
**Fix:** Specify allocation method — random hash on customer ID, sticky.

### L-12. SM-C5 (3-month MRR churn guardrail) lag means signals arrive after 100% rollout (§7)
**Fix:** Acknowledge measurement lag; add a leading proxy metric (e.g., 30-day activation).

### L-13. The PRD itself has no versioning beyond "draft v1" — change log absent (§17)
**Fix:** Add a small change log table at the end; reference `.decision-log.md`.

### L-14. Risk row "Mobile users encounter desktop-only experience" mitigation copy is unauthored (§15)
**Fix:** Author the copy; UX owns; flagged in §16 Open Q13.

### L-15. The bot copy "we see you use Turno" surfaces Salesforce data to user verbatim — Salesforce data hygiene risk (§4.4 / FR-18)
**Fix:** Only surface partner names from a whitelist; opaque or generic message for unrecognized partner strings.

### L-16. SM-8 "% of Call 1 time spent on review vs. walkthrough" — CSM self-report has bias (§7)
**Fix:** Add a CSM survey methodology note; cross-check with a sample of recorded calls if possible.

### L-17. Section 8 calendar adds with multi-day rolling Setup Calls (rare for SMB but possible) (§4.8 / FR-40)
**Fix:** Out of scope confirm — V1 supports single-event Setup Calls only.

### L-18. Persistent header "Skip to Dashboard" wording on Section 8 (already past skip-meaningfulness) (§4.7, §4.8)
**Fix:** Section 8 hides Skip button or replaces with "Go to Dashboard" primary CTA (already the case per FR-42 — but redundancy in header should be specified).

### L-19. The phrase "AHA moment" appears in PRD prose but not as a defined product surface (§4.3)
**Fix:** Either define AHA-moment instrumentation event (`aha_moment_fired` when Q1.1 success state renders) or remove from PRD prose.

### L-20. Salesforce `Owners` field semantic — count of third-party homeowners, not Guesty user owners (§4.6 / FR-33)
**Fix:** Add to Glossary that `Owners` means third-party property owners, to disambiguate from operator's role.

### L-21. The PRD distinguishes "primary owner" from "Decision Owner" — slight glossary drift (§4.5 / FR-25, §3)
**Fix:** Use "Decision Owner" consistently in FRs; treat "primary owner" as Q4.1 user-facing copy only.

### L-22. Q5.3 fee unit "per stay" vs. "per night" — currency-relative semantics on display (§4.5 / FR-31)
**Fix:** Section 8 fees summary uses currency symbol from the operator's Guesty account; document the formatting rule.

### L-23. UJ-5 (Hannah / Turno + PriceLabs) has no path back if she WANTS to set those up in Guesty instead (§2.4)
**Fix:** Provide a "use Guesty instead" override on partner auto-advance; out of scope for V1 if expensive, but flag in V2.

### L-24. CSV upload at Q7.1 — 1 MB cap for 5-20 listings of contacts is generous; realistic file is <10 KB (§4.6 / FR-33)
**Fix:** Cap is fine but flag that the limit is the file-system limit, not a typical-case constraint.

### L-25. FR-48 event field `was_via_accountant_link` is a boolean — what about future expansion (e.g., CSM-completed)? (§4.9)
**Fix:** Replace boolean with enum `actor: operator | accountant | csm | system_default`.

---

## Severity totals

- **Critical:** 12
- **High:** 26
- **Medium:** 30
- **Low:** 25
- **Total:** 93

---

## Findings spanning multiple FRs (cross-cutting themes)

1. **Delegation lifecycle** is under-specified. Affects FR-26, FR-27, FR-28, FR-8, FR-25. Need an explicit state machine: `not_offered → offered → sent → opened → in_progress → completed | expired | cancelled | superseded`.
2. **Data freshness and snapshot semantics** are under-specified. FR-4, FR-7, FR-11, FR-15, FR-32 mix snapshot-at-entry with re-poll-at-entry with assumed-live evaluation. Needs a single coherent freshness model.
3. **Concurrent / multi-actor writes**. Operator + accountant; operator + Guesty Settings; operator + CSM updating Salesforce. None of the FR-43–FR-49 write semantics consider non-Wizard actors.
4. **Empty / null / missing data branches**. FR-7 enumerates positive branches; the "what if the data is missing" branch is unspecified for Q1.2, Q3.1, Q6.1, Q7.2, Q5.3.
5. **OAuth bounce-and-recover** is hand-waved. FR-13, FR-17 specify success and explicit failure but not in-flight ambiguity (user closed tab, redirect lost, partial scope grant).
6. **Backward navigation post-write** has no specified rollback / re-write contract anywhere. FR-8, FR-45 imply idempotency; H-12, M-12 show edits cause re-writes that may have side effects (template hot-swap, deactivation cascades).
7. **Feature-flag stickiness** during phased rollout is unspecified. H-14.
8. **Localization** (Open Q5) intersects with M-19, FR-21 templates, FR-31 currency, H-7/H-8 timezones, L-1 emoji — needs a unified plan even for English-only V1.

---

*End of review.*
