// wizard.jsx — main wizard shell, routing, canvas reveal logic, S8/S9/S10
// Wrapped in IIFE so its top-level consts don't collide with screens.jsx
(function () {

  const { useState, useEffect, useMemo, useRef, useCallback } = React;
  const SCREENS = window.makeScreens();
  const SF_PREFILL = window.SF_PREFILL;
  const CSM_NAME = window.CSM_NAME;
  const MOCK_LISTINGS = window.MOCK_LISTINGS;
  const SkeletonImg = window.SkeletonImg;
  const Option = window.Option; // pick-one control reused on the homepage carousel

  // Shared Call 1 date — used by header countdown ticker and NextCallSection
  const CALL_TIME = new Date("2026-06-18T11:00:00-07:00");

  /* ============ Adaptive section ordering ============ */
  // The sales-notes "brain" surfaces what the manager cares about (focus topics,
  // add-on intent). We use that to reorder the *preference* sections so the most
  // relevant ones come first — while Brand (1) and Portfolio & Channels (2, which
  // holds the only real action: the view-only Airbnb pre-connect) stay anchored at
  // the front. `showIf` remains the hard safety gate; this only permutes whole
  // sections among themselves. With no signal, the canonical order is preserved.
  const ANCHOR_SECTIONS = [1, 2];
  const REORDERABLE_SECTIONS = [3, 4, 5, 6, 7, 8];
  // section number -> display name, taken from the screens themselves.
  const SECTION_NAMES = {};
  SCREENS.forEach((s) => { if (s.section && !SECTION_NAMES[s.section]) SECTION_NAMES[s.section] = s.sectionName; });
  // Note enum -> the section it makes most relevant.
  const FOCUS_SECTION = {
    pricing_strategy: 6, owner_reporting: 5, cleaner_workflows: 3, guest_messaging: 3,
    accounting_setup: 4, booking_website: 7, reviews_reputation: 3, channel_mix: 2,
  };
  const ADDON_SECTION = {
    gpo: 6, accounting: 4, guestypay: 4, locks: 3, auto_comply: 7, damage_protection: 7,
  };
  // Human phrase for the "let's start here" callout, keyed by the promoting signal.
  const FOCUS_PHRASE = {
    pricing_strategy: "pricing strategy", owner_reporting: "owner reporting",
    cleaner_workflows: "cleaner workflows", guest_messaging: "guest messaging",
    accounting_setup: "accounting setup", booking_website: "a direct booking site",
    reviews_reputation: "reviews & reputation", channel_mix: "your channel mix",
  };
  const ADDON_PHRASE = {
    gpo: "dynamic pricing", accounting: "accounting", guestypay: "payments",
    locks: "smart locks", auto_comply: "compliance", damage_protection: "damage protection",
  };

  let _planCache;
  function adaptivePlan() {
    if (_planCache) return _planCache;
    const prefill = (window.OB_CONTEXT && window.OB_CONTEXT.prefill) || {};
    const promoted = [];
    const reason = {};
    const add = (sec, phrase) => {
      if (!REORDERABLE_SECTIONS.includes(sec) || promoted.includes(sec)) return;
      promoted.push(sec);
      reason[sec] = phrase;
    };
    (prefill.focus_topics || []).forEach((t) => { if (FOCUS_SECTION[t]) add(FOCUS_SECTION[t], FOCUS_PHRASE[t] || t); });
    (prefill.addon_intent || []).forEach((a) => { if (ADDON_SECTION[a]) add(ADDON_SECTION[a], ADDON_PHRASE[a] || a); });
    const rest = REORDERABLE_SECTIONS.filter((s) => !promoted.includes(s));
    _planCache = { order: [...ANCHOR_SECTIONS, ...promoted, ...rest], reason, promoted };
    return _planCache;
  }
  // 0-based position of a section in the adaptive order (for monotonic progress).
  function adaptivePosition(section) {
    const idx = adaptivePlan().order.indexOf(section);
    return idx >= 0 ? idx : (section - 1);
  }
  // Expose for the canvas-side milestone panel, which lives in screens.jsx.
  window.OB_adaptivePlan = adaptivePlan;
  window.OB_sectionNames = SECTION_NAMES;

  /* ============ Phase model ============ */
  function buildPhases(answers) {
    const phases = [];
    // S0 — welcome (always first; not counted in section 1–8 progress)
    phases.push({ type: "welcome" });
    const eligible = SCREENS.filter((s) => !s.showIf || s.showIf(answers));
    // Regroup eligible screens by the adaptive section order, preserving each
    // section's canonical within-order. Any section not named in the plan (should
    // not happen) falls through at the end so no screen is ever dropped.
    const order = adaptivePlan().order;
    const rank = new Map(order.map((sec, i) => [sec, i]));
    const screens = eligible.slice().sort((a, b) => {
      const ra = rank.has(a.section) ? rank.get(a.section) : 99;
      const rb = rank.has(b.section) ? rank.get(b.section) : 99;
      return ra - rb; // stable sort keeps within-section canonical order
    });
    let lastSection = 0;
    for (const s of screens) {
      // Mid-funnel milestone travels with Financials (section 4) wherever it lands.
      if (s.section === 4 && lastSection !== 4) {
        phases.push({ type: "milestone", section: 4 });
      }
      phases.push({ type: "question", screen: s });
      lastSection = s.section;
    }
    phases.push({ type: "review" });
    // Bug 2 fix: removed dead { type: "confirm" } phase — confirmSetup now jumps directly to setup
    phases.push({ type: "setup" });
    phases.push({ type: "done" });
    return phases;
  }

  function App() {
    const [answers, setAnswers] = useState({
      listing_count: SF_PREFILL.listing_count,
      channels_current: (SF_PREFILL.channels || []).slice(),
      channels_to_add: [],
      channels: (SF_PREFILL.channels || []).slice(),
      __skipped: []
    });
    const [phaseIdx, setPhaseIdx] = useState(0);
    const [direction, setDirection] = useState(1); // 1 = forward (slide up), -1 = back (slide down)
    const [oauthState, setOauthState] = useState("idle"); // idle | working | success | error
    const oauthTimerRef = useRef(null); // Bug 3: cancel timer on navigate away
    // --- Dialog surface (wizard-surface-dialog-patch-2026-05-29) ---
    const [isDialogMode, setIsDialogMode] = useState(
      () => window.innerWidth >= 1024 && window.innerHeight >= 680
    );
    const [animState, setAnimState] = useState(""); // "" | "active" | "exiting"
    const [wizExited, setWizExited] = useState(false);
    const dialogRef = useRef(null);
    const entryStarted = useRef(false);
    const exitStarted = useRef(false);

    // Debug — `#done` or `#aha` (or legacy `?stage=done`) jumps straight to the named stage for review.
    useEffect(() => {
      setTimeout(() => {
        try {
          const sp = new URLSearchParams(window.location.search);
          if (sp.get("stage") === "done" || window.location.hash === "#done") {
            const idx = phases.findIndex(p => p.type === "done");
            if (idx >= 0) setPhaseIdx(idx);
          } else if (window.location.hash === "#milestone") {
            const idx = phases.findIndex(p => p.type === "milestone" && p.section === 4);
            if (idx >= 0) setPhaseIdx(idx);
          } else if (window.location.hash.startsWith("#q=")) {
            const qid = decodeURIComponent(window.location.hash.slice(3));
            const idx = phases.findIndex(p => p.type === "question" && p.screen.id === qid);
            if (idx >= 0) setPhaseIdx(idx);
          } else if (window.location.hash === "#aha") {
            // Seed answers so Q1.AHA's showIf passes, then jump to it
            setAnswers((a) => ({ ...a, oauth_status: "success" }));
            // Defer until phases rebuild
            setTimeout(() => {
              const builtPhases = buildPhases({ ...answers, oauth_status: "success" });
              const idx = builtPhases.findIndex(p => p.type === "question" && p.screen.id === "Q1.AHA");
              if (idx >= 0) setPhaseIdx(idx);
            }, 30);
          }
        } catch {}
      }, 0);
      // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);
    // Bug 6 fix: milestoneCountdown removed (was never decremented; dead state)
    const [showConfirm, setShowConfirm] = useState(false);
    const [toast, setToast] = useState(null);

    // Toast subsystem — listens for `wiz-toast` CustomEvents
    useEffect(() => {
      const onToastEvt = (e) => {
        const detail = e.detail;
        const data = typeof detail === "string" ? { message: detail } : detail;
        setToast(data);
        const t = setTimeout(() => setToast(null), data.onUndo ? 4000 : 2800);
        return () => clearTimeout(t);
      };
      window.addEventListener("wiz-toast", onToastEvt);
      return () => window.removeEventListener("wiz-toast", onToastEvt);
    }, []);

    const phases = useMemo(
      () => buildPhases(answers),
      // rebuild when branching conditions change OR when oauth completes (Q1.4b appears)
      [
        answers.onboard_more,
        answers.owners_gate,
        answers.pricing_tool,
        answers.pay_timing,
        answers.owner_split,
        answers.oauth_status,
        answers.channels_current,
        answers.cleaning_system,
        // UX Patch — new conditional standalone pages
        answers.go_live,          // Q1.5_deadline
        answers.checklist_choice, // Q2.4_upload
        answers.owner_split_type, // Q5.owner_split_mixed
      ]
    );
    const current = phases[phaseIdx];

    const set = useCallback((k, v) => {
      if (typeof k === "function") {
        setAnswers(k);
        return;
      }
      if (typeof k === "object" && v === undefined) {
        setAnswers((prev) => ({ ...prev, ...k }));
        return;
      }
      setAnswers((prev) => ({ ...prev, [k]: v }));
    }, []);

    /* OAuth simulation — triggered by primary CTA on Q1.4 step 1 */
    const doOAuth = useCallback(() => {
      // Bug 4 fix: early-return if already connected
      if (answers.oauth_status === "success") { onContinue(); return; }
      setOauthState("working");
      // Bug 3 fix: store timer ref so it can be cancelled on navigate away
      oauthTimerRef.current = setTimeout(() => {
        oauthTimerRef.current = null;
        setOauthState("success");
        setAnswers((a) => ({ ...a, oauth_status: "success" }));
        setDirection(1);
        setPhaseIdx((i) => i + 1);
      }, 1800);
    }, [answers.oauth_status]);

    // Bug 3 fix: cancel pending OAuth timer when phase changes
    useEffect(() => {
      return () => {
        if (oauthTimerRef.current) {
          clearTimeout(oauthTimerRef.current);
          oauthTimerRef.current = null;
          setOauthState("idle");
        }
      };
    }, [phaseIdx]);

    /* Canvas mode — AHA removed; milestone and review remain */
    const canvasMode = useMemo(() => {
      if (!current) return "hidden";
      if (current.type === "milestone") return "milestone";
      if (current.type === "review") return "review";
      if (current.type === "question" && current.screen.id === "Q1.4" && oauthState !== "working") return "video";
      if (current.type === "question" && current.screen.id === "Q3.6") return "feebuilder";
      if (current.type === "question" && current.screen.id === "Q3.7" && !answers.__explain_taxes_open) return "taxes_builder";
      if (current.type === "question" && current.screen.id === "Q3.7" && answers.__explain_taxes_open) return "taxes_explain";
      if (current.type === "welcome") return "hidden";
      return "hidden";
    }, [current, oauthState, answers.__explain_taxes_open]);

    // Reset the educational expansion when navigating away from Q3.7
    useEffect(() => {
      if (!(current?.type === "question" && current.screen.id === "Q3.7") && answers.__explain_taxes_open) {
        setAnswers((a) => ({ ...a, __explain_taxes_open: false }));
      }
    }, [current, answers.__explain_taxes_open]);

    /* Milestone — no auto-advance; user must click CTA */

    // Bug 1 fix: fireOnLeave — called by ALL navigation paths, not just onContinue
    const fireOnLeave = useCallback(() => {
      if (current?.type === "question" && current.screen.onLeave) {
        try { current.screen.onLeave({ answers, set }); } catch {}
      }
    }, [current, answers, set]);

    /* Navigation */
    const canGoBack = phaseIdx > 0 && current?.type !== "setup" && current?.type !== "done" && current?.type !== "welcome";
    const onBack = () => {
      fireOnLeave();
      setDirection(-1);
      setPhaseIdx((i) => Math.max(0, i - 1));
    };
    const onContinue = useCallback(() => {
      if (current?.type === "review") { setShowConfirm(true); return; }
      fireOnLeave();
      setDirection(1);
      setPhaseIdx((i) => Math.min(phases.length - 1, i + 1));
    }, [current, fireOnLeave, phases.length]);
    const onSkip = () => {
      if (current?.type === "question") {
        const id = current.screen.id;
        setAnswers((a) => ({ ...a, __skipped: [...(a.__skipped || []), id] }));
        if (id === "Q1.4") setAnswers((a) => ({ ...a, oauth_status: "skipped" }));
      }
      fireOnLeave();
      setDirection(1);
      setPhaseIdx((i) => Math.min(phases.length - 1, i + 1));
    };
    // Note-driven: rep flagged this account wants financials handled live on Call 1.
    // Mark the whole Financials block as skipped (→ punch list) and jump past it.
    const onDeferFinancials = () => {
      const finIds = phases
        .filter((p) => p.type === "question" && p.screen.section === 4)
        .map((p) => p.screen.id);
      setAnswers((a) => {
        const skipped = a.__skipped || [];
        const add = finIds.filter((id) => !skipped.includes(id));
        return { ...a, __skipped: [...skipped, ...add], __deferred_financials: true };
      });
      fireOnLeave();
      setDirection(1);
      const startIdx = phases.findIndex((p) => p.type === "milestone" && p.section === 4);
      let idx = startIdx + 1;
      while (idx < phases.length && phases[idx].type === "question" && phases[idx].screen.section === 4) idx++;
      setPhaseIdx(Math.min(phases.length - 1, idx));
    };
    const onJumpTo = (qid) => {
      fireOnLeave();
      const idx = phases.findIndex((p) => p.type === "question" && p.screen.id === qid);
      if (idx >= 0) { setDirection(idx > phaseIdx ? 1 : -1); setPhaseIdx(idx); }
    };
    const confirmSetup = () => {
      setShowConfirm(false);
      setDirection(1);
      const setupIdx = phases.findIndex(p => p.type === "setup");
      if (setupIdx >= 0) setPhaseIdx(setupIdx);
      else setPhaseIdx((i) => Math.min(phases.length - 1, i + 1));
    };

    /* Keyboard navigation */
    useEffect(() => {
      const handler = (e) => {
        const tag = document.activeElement?.tagName;
        if (tag === "INPUT" || tag === "TEXTAREA" || tag === "SELECT") return;
        if (showConfirm) return;
        // The conversational welcome drives its own flow — don't let global Enter/Arrow
        // keys skip past it.
        if (current?.type === "welcome") return;

        // Number keys — select nth option and auto-advance
        if (e.key >= "1" && e.key <= "9") {
          e.preventDefault();
          const idx = parseInt(e.key) - 1;
          const opts = document.querySelectorAll(".wiz-panel .opt");
          if (opts[idx]) {
            opts[idx].click();
            // Auto-advance after a short delay so the selection registers visually
            setTimeout(() => onContinue(), 320);
          }
          return;
        }

        if (e.key === "ArrowDown" || e.key === "Enter") {
          e.preventDefault();
          const isPrimaryOAuth = current?.type === "question" && current.screen.primaryAction === "oauth";
          if (isPrimaryOAuth && oauthState === "idle") {doOAuth();return;}
          onContinue();
        }
        if (e.key === "ArrowUp") {
          e.preventDefault();
          if (canGoBack) onBack();
        }
      };
      window.addEventListener("keydown", handler);
      return () => window.removeEventListener("keydown", handler);
    }, [current, oauthState, showConfirm, canGoBack, onContinue, onBack, doOAuth]);

    /* --- Dialog surface effects (wizard-surface-dialog-patch-2026-05-29) --- */

    // Viewport resize — updates isDialogMode when crossing 1024×680 threshold (§6)
    useEffect(() => {
      const onResize = () => setIsDialogMode(window.innerWidth >= 1024 && window.innerHeight >= 680);
      window.addEventListener("resize", onResize);
      return () => window.removeEventListener("resize", onResize);
    }, []);

    // Entry animation — fires once when dialog mode is first established (§5.1)
    useEffect(() => {
      if (!isDialogMode || wizExited || entryStarted.current) return;
      entryStarted.current = true;
      const t = setTimeout(() => setAnimState("active"), 30);
      return () => clearTimeout(t);
    }, [isDialogMode, wizExited]);

    // Exit animation — fires when done phase is reached in dialog mode (§5.3)
    useEffect(() => {
      if (!isDialogMode || wizExited || exitStarted.current) return;
      if (current?.type !== "done") return;
      exitStarted.current = true;
      setAnimState("exiting");
      const t = setTimeout(() => setWizExited(true), 560);
      return () => clearTimeout(t);
    }, [current?.type, isDialogMode, wizExited]);

    // Initial focus: move focus onto the dialog container itself so no button
    // gets a visible highlight on load. tabIndex={-1} on the surface makes this work.
    useEffect(() => {
      if (!isDialogMode || !dialogRef.current || animState !== "active") return;
      dialogRef.current.focus({ preventScroll: true });
    }, [animState, isDialogMode]);

    // Focus trap — Tab/Shift+Tab cycles only within the dialog (§7.2)
    useEffect(() => {
      if (!isDialogMode || wizExited) return;
      const onKeyDown = (e) => {
        if (e.key !== "Tab" || !dialogRef.current) return;
        const focusable = Array.from(dialogRef.current.querySelectorAll(
          "button:not([disabled]), [href], input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex=\"-1\"])"
        ));
        if (focusable.length === 0) return;
        const first = focusable[0];
        const last = focusable[focusable.length - 1];
        if (e.shiftKey) {
          if (document.activeElement === first) { e.preventDefault(); last.focus(); }
        } else {
          if (document.activeElement === last) { e.preventDefault(); first.focus(); }
        }
      };
      document.addEventListener("keydown", onKeyDown);
      return () => document.removeEventListener("keydown", onKeyDown);
    }, [isDialogMode, wizExited]);

    /* Progress — section-based so it never jumps when conditional Qs appear */
    const progressPct = useMemo(() => {
      if (!current || current.type === "setup" || current.type === "done") return 100;
      if (current.type === "review") return 93;
      if (current.type === "milestone") return Math.round(adaptivePosition(4) / 8 * 90); // before Financials, wherever it lands
      if (current.type === "question") {
        const s = current.screen;
        // Dynamic: position among the *active* (showIf-passing) screens in this section,
        // so conditional standalone pages slot in smoothly with no stall or leap.
        // sectionFrac uses the adaptive position so reordered sections still climb monotonically.
        const sectionScreens = phases.filter(p => p.type === "question" && p.screen.section === s.section);
        const pos = Math.max(0, sectionScreens.findIndex(p => p.screen.id === s.id));
        const total = Math.max(sectionScreens.length, 1);
        const sectionFrac = adaptivePosition(s.section) / 8;
        const withinFrac = pos / total / 8;
        return Math.round((sectionFrac + withinFrac) * 90);
      }
      return 0;
    }, [current, phases]);

    const isValid = useMemo(() => {
      if (!current || current.type !== "question") return true;
      return current.screen.valid ? current.screen.valid(answers) : true;
    }, [current, answers]);

    const showNavArrows = current?.type !== "setup" && current?.type !== "done" && current?.type !== "welcome";

    // Wizard done in dialog mode: live interactive DonePanel replaces the dialog (§5.3)
    if (wizExited) {
      return <DonePanel answers={answers} set={set} />;
    }

    // In dialog mode while exiting, suppress DonePanel inside the fading dialog surface;
    // the backdrop is already sharpening and becoming the live homepage (§5.3)
    const isDonePhase = current?.type === "done";
    const effectiveCurrent = (isDialogMode && isDonePhase) ? null : current;
    const shellClass = "wiz-shell" + (!isDialogMode && isDonePhase ? " wiz-shell--home" : "");
    const stageClass = "wiz-stage" +
      (canvasMode !== "hidden" ? " canvas-visible" : "") +
      (!isDialogMode && isDonePhase ? " wiz-stage--home" : "");

    const wizContent = (
      <div className={shellClass}>
        {current?.type !== "done" && (
          <Topbar
              progress={progressPct}
              sectionLabel={sectionLabel(current)}
              hideProgress={current?.type === "welcome"} />
        )}
        <div className={stageClass}>
          <PanelHost
              current={effectiveCurrent}
              answers={answers}
              set={set}
              oauthState={oauthState}
              doOAuth={doOAuth}
              canGoBack={canGoBack}
              isValid={isValid}
              direction={direction}
              onBack={onBack}
              onContinue={onContinue}
              onSkip={onSkip}
              onDeferFinancials={onDeferFinancials}
              onJumpTo={onJumpTo}
              phaseIdx={phaseIdx} />
          <div className="wiz-canvas" aria-hidden={canvasMode === "hidden"}>
            {canvasMode === "milestone" && <window.CanvasMilestone />}
            {/* Bug 7 fix: CanvasAHA removed — canvasMode never returns "aha" */}
            {canvasMode === "review" && <window.CanvasReview answers={answers} onJumpTo={onJumpTo} />}
            {canvasMode === "video" && <window.CanvasVideo />}
            {canvasMode === "feebuilder" && <window.CanvasFeeBuilder answers={answers} set={set} />}
            {canvasMode === "taxes_builder" && <window.CanvasTaxes answers={answers} set={set} />}
            {canvasMode === "taxes_explain" && <window.CanvasTaxesExplain onClose={() => set("__explain_taxes_open", false)} />}
            {canvasMode === "welcome_illustration" && <window.WelcomeIllustration />}
          </div>
        </div>
        {showNavArrows &&
          <WizNavArrows
            canGoBack={canGoBack}
            onBack={onBack}
            onForward={onContinue}
            canGoForward={current?.type !== "welcome"} />
        }
        {showConfirm &&
          <ConfirmDialog onCancel={() => setShowConfirm(false)} onConfirm={confirmSetup} />
        }
        {toast && (
          <div className="wiz-toast" role="status" aria-live="polite">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
              <polyline points="20 6 9 17 4 12"></polyline>
            </svg>
            <span>{toast.message}</span>
            {toast.onUndo && (
              <button type="button" className="wiz-toast-undo" onClick={() => { toast.onUndo(); setToast(null); }}>Undo</button>
            )}
          </div>
        )}
      </div>
    );

    // Full-bleed fallback — viewport below 1024×680 (§6, P-5)
    if (!isDialogMode) {
      return wizContent;
    }

    // Dialog surface presentation (P-1 through P-4)
    // Backdrop uses prefill defaults so it is visually stable from frame 0 (§7.4, §11 decision 2)
    const BACKDROP_ANSWERS = {
      focus_topics: ["Pricing strategy", "Channel mix"],
      selected_listings: MOCK_LISTINGS,
    };

    return (
      <div className={"wiz-dialog-root" + (animState ? " wiz-dialog-root--" + animState : "")}>
        {/* Backdrop layer: inert DonePanel (blurred platform homepage, §4) */}
        {/* No-op `set` keeps the question carousel static (non-interactive) here. */}
        <div className="wiz-backdrop" aria-hidden="true">
          <DonePanel answers={BACKDROP_ANSWERS} set={() => {}} />
        </div>
        {/* Scrim layer (§4.3). Intentional: scrim click does NOT close the wizard (§7.3) */}
        <div className="wiz-scrim" />
        {/* Dialog surface (§3) */}
        <div
          ref={dialogRef}
          role="dialog"
          aria-modal="true"
          aria-label="Guesty onboarding"
          className="wiz-dialog-surface"
          tabIndex={-1}
        >
          {wizContent}
        </div>
      </div>
    );

  }

  function sectionLabel(current) {
    if (!current) return "";
    if (current.type === "welcome") return "";
    if (current.type === "milestone") return "Milestone";
    if (current.type === "review") return "Section 8 of 8 · Review and confirm";
    if (current.type === "confirm") return "Confirming your setup";
    if (current.type === "setup") return "Setting up your Guesty account";
    if (current.type === "done") return "You're set up";
    const s = current.screen;
    if (s.subStepLabel) return s.subStepLabel;
    return `Section ${adaptivePosition(s.section) + 1} of 8 · ${s.sectionName}`;
  }

  function sectionOfEight(current) {
    if (!current) return null;
    if (current.type === "question") return current.screen.section;
    if (current.type === "review") return 8;
    if (current.type === "milestone") return 4;
    return null;
  }

  /* ============ Nav arrows (Typeform style, fixed bottom-right) ============ */
  // `canGoForward` is optional and defaults to true so the wizard's own usage
  // (which never passes it) keeps its original "forward always enabled" behavior.
  // The homepage question carousel passes it to disable forward on the last card.
  function WizNavArrows({ canGoBack, onBack, onForward, canGoForward = true }) {
    const KeyCap = ({ children, disabled }) =>
    <span style={{
      display: "inline-flex", alignItems: "center", justifyContent: "center",
      width: 32, height: 32,
      boxSizing: "border-box",
      background: disabled ? "rgba(255,255,255,0.06)" : "rgba(255,255,255,0.14)",
      border: "1px solid rgba(255,255,255,0.22)",
      borderRadius: 6,
      boxShadow: disabled
        ? "none"
        : "inset 0 -2px 0 rgba(255,255,255,0.18), 0 1px 0 rgba(0,0,0,0.35)",
      fontSize: 13,
      lineHeight: 1,
      color: disabled ? "rgba(255,255,255,0.25)" : "white"
    }}>{children}</span>;


    return (
      <div className="wiz-nav-arrows" role="group" aria-label="Question navigation">
      <span className="wiz-nav-tip" data-tooltip="Go back · ↑ key">
        <button onClick={onBack} disabled={!canGoBack} aria-label="Previous question (↑)">
          <KeyCap disabled={!canGoBack}>
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
              <polyline points="18 15 12 9 6 15"></polyline>
            </svg>
          </KeyCap>
        </button>
      </span>
      <span className="wiz-nav-tip" data-tooltip="Continue · ↓ key">
        <button onClick={onForward} disabled={!canGoForward} aria-label="Next question (↓)">
          <KeyCap disabled={!canGoForward}>
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
              <polyline points="6 9 12 15 18 9"></polyline>
            </svg>
          </KeyCap>
        </button>
      </span>
    </div>);

  }

  /* ============ Countdown Ticker (Arc Status badge style) ============ */
  function CountdownTicker() {
    const [timeLeft, setTimeLeft] = useState(() => CALL_TIME - Date.now());

    useEffect(() => {
      const id = setInterval(() => setTimeLeft(CALL_TIME - Date.now()), 1000);
      return () => clearInterval(id);
    }, []);

    const totalSecs = Math.max(0, Math.floor(timeLeft / 1000));
    const days = Math.floor(totalSecs / 86400);
    const hrs  = Math.floor((totalSecs % 86400) / 3600);
    const mins = Math.floor((totalSecs % 3600) / 60);
    const secs = totalSecs % 60;
    const pad  = (n) => String(n).padStart(2, "0");
    const isPast = timeLeft <= 0;

    return (
      <div className="wiz-countdown-ticker" aria-live="polite" aria-label="Time until Call 1">
        {isPast ? (
          <span>Call 1 is now</span>
        ) : (
          <span className="wiz-countdown-text">
            Call 1 in{" "}
            {days > 0
              ? `${days}:${pad(hrs)}:${pad(mins)}:${pad(secs)}`
              : `${pad(hrs)}:${pad(mins)}:${pad(secs)}`}
          </span>
        )}
      </div>
    );
  }

  /* ============ Topbar ============ */
  function Topbar({ progress, sectionLabel, hideProgress }) {
    return (
      <div className="wiz-topbar">
      <div className="wiz-brand">
        <SkeletonImg
          src="assets/guesty-pro-logo.svg"
          alt="Guesty Pro"
          style={{ height: "100%", width: "100%", display: "block", objectFit: "contain" }}
          wrapStyle={{ display: "inline-block", height: 19.36, aspectRatio: "663 / 117", lineHeight: 0, borderRadius: 3, flexShrink: 0 }}
        />
        <span className="sep" aria-hidden="true"></span>
        <span className="subtitle">{SF_PREFILL.business_name}</span>
      </div>
      {!hideProgress && (
      <div className="wiz-progress">
        <div style={{ fontSize: 11, fontWeight: 600, color: "hsl(var(--gst-muted-foreground))", textAlign: "center", marginBottom: 5, whiteSpace: "nowrap", letterSpacing: "0.02em" }}>{sectionLabel}</div>
        <div className="wiz-progress-track">
          <div className="wiz-progress-fill" style={{ width: progress + "%" }}></div>
        </div>
      </div>
      )}
      <div className="wiz-topbar-right">
        <CountdownTicker />
        <button className="wiz-exit" onClick={() => alert("Your progress is saved. You can resume any time from your dashboard.")}>
          Save and exit
        </button>
        {/* Internal reset button */}
        <button
          className="wiz-reset-btn"
          title="Reset prototype (clears all state)"
          aria-label="Reset prototype"
          onClick={() => {
            localStorage.clear();
            sessionStorage.clear();
            window.location.hash = '';
            window.location.reload();
          }}
        >
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
            <polyline points="1 4 1 10 7 10"/>
            <path d="M3.51 15a9 9 0 1 0 .49-4.5"/>
          </svg>
        </button>
      </div>
    </div>);

  }

  /* ============ Panel host ============ */
  function PanelHost(props) {
    const { current } = props;
    if (!current) return null;
    if (current.type === "welcome") return <WelcomePanel {...props} />;
    if (current.type === "question") return <QuestionPanel {...props} />;
    if (current.type === "milestone") return <MilestonePanel {...props} />;
    if (current.type === "review") return <ReviewPanel {...props} />;
    if (current.type === "setup") return <SetupPanel {...props} />;
    if (current.type === "done") return <DonePanel {...props} />;
    return null;
  }

  /* ============ Flag for review (Arc "Status — Warning" pattern) ============ */
  // Lets the user flag a question to review with their CSM on Call 1.
  // Once flagged: the button is replaced by a "Review in Call 1" label, a
  // "Needs review" status appears, and the question surfaces on the homepage
  // "Topics for Call 1" section.
  function FlagForReview({ screen, answers, set }) {
    const flagged = answers.__flagged || [];
    const isFlagged = flagged.some((f) => f.id === screen.id);

    const onFlag = () => {
      if (isFlagged) return;
      // Capture the question's title straight from the rendered panel so the
      // homepage can show a human-readable topic without per-screen metadata.
      let title = screen.id;
      try {
        const el = document.querySelector(".wiz-panel .q-title");
        const txt = el && el.textContent ? el.textContent.trim() : "";
        if (txt) title = txt;
      } catch {}
      set("__flagged", [
        ...flagged,
        { id: screen.id, title, section: screen.section, sectionName: screen.sectionName },
      ]);
      window.dispatchEvent(new CustomEvent("wiz-toast", {
        detail: {
          message: "Flagged for " + CSM_NAME + " — added to Call 1",
          onUndo: () => set("__flagged", flagged.filter(f => f.id !== screen.id)),
        },
      }));
    };

    if (isFlagged) {
      return (
        <span className="gst-badge gst-badge--info flag-review-status">Needs review</span>
      );
    }

    return (
      <span className="flag-cta-wrap" data-tooltip="Flag to review with you on Call 1.">
        <button type="button" className="flag-cta" onClick={onFlag}>
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
            <path d="M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1z" />
            <line x1="4" y1="22" x2="4" y2="15" />
          </svg>
          <span>Flag for {CSM_NAME}</span>
        </button>
      </span>
    );
  }

  /* ============ Question panel ============ */
  // A few natural, personalized lead-ins: on select screens, open with a line that
  // references something the user already told us — the intro confirmation or an
  // earlier answer — so the next question reads like a continuation, not a generic
  // form field. Returns renderable content or null (null = show nothing).
  function personalLead(screen, answers) {
    const id = screen.id;
    // First portfolio question — bridge straight out of the conversational intro.
    if (id === "Q1.1" && answers.intro_done) {
      if (answers.intro_migration_label) {
        return <>Since you're bringing everything over from <strong>{answers.intro_migration_label}</strong>, let's start by confirming the listings coming with you.</>;
      }
      const n = SF_PREFILL.listing_count;
      if (n) return <>You confirmed <strong>{n} listing{n === 1 ? "" : "s"}</strong> a moment ago — let's make sure we've got them all.</>;
    }
    // Wrap-up pain question — tie it back to the focus topic they just picked.
    if (id === "Q6.2") {
      const picked = ((answers.focus_topics || [])[0] || answers.intro_focus_label || "").toLowerCase();
      if (picked) return <>You flagged <strong>{picked}</strong> up top — let's get specific about where it's hurting.</>;
    }
    // Owner records upload — reference that they told us they manage for owners.
    if (id === "Q7.2" && (answers.owners_gate === "all" || answers.owners_gate === "some")) {
      const word = answers.owners_gate === "all" ? "every listing has an owner" : "some of your listings have owners";
      return <>Since {word}, a quick upload here saves a lot of manual entry later.</>;
    }
    return null;
  }

  function QuestionPanel({ current, answers, set, oauthState, doOAuth, isValid, direction, onContinue, onSkip, phaseIdx }) {
    const screen = current.screen;
    const primaryLabel = screen.primaryLabel ? screen.primaryLabel(answers, oauthState) : "Continue";
    const skipLabel = screen.skipLabel || null;
    const primaryIsOAuth = screen.primaryAction === "oauth";
    const primaryDisabled = primaryIsOAuth && oauthState === "working";
    const primaryHandler = primaryIsOAuth ? doOAuth : onContinue;
    const slideClass = direction >= 0 ? "slide-forward" : "slide-back";
    const isWide = screen.id === "Q1.4b" || screen.fullWidth === true;
    const isListingsWide = screen.id === "Q1.4b";
    const isAha = screen.id === "Q1.AHA";
    const wideMaxWidth = isAha ? 1200 : 988;

    // Dynamic question counter — only count visible screens in this section
    const allScreens = useMemo(() => makeScreens(), []);
    const sectionScreens = useMemo(() =>
      allScreens.filter(s => s.section === screen.section && (!s.showIf || s.showIf(answers))),
      [allScreens, screen.section, answers]
    );
    const visibleQIndex = sectionScreens.findIndex(s => s.id === screen.id) + 1 || screen.qIndex;
    const visibleQTotal = sectionScreens.length || screen.qTotal;
    const qMetaValue = { visibleQIndex, visibleQTotal };

    // "Surface priorities early" — when the sales notes promoted this section, show
    // an Amanda note on the section's first question explaining why it's up front.
    const promotedPhrase = adaptivePlan().reason[screen.section];
    const isFirstInSection = sectionScreens.length > 0 && sectionScreens[0].id === screen.id;
    const showPriorityCallout = isFirstInSection && !!promotedPhrase;
    const specialist = (window.OB_CONTEXT && window.OB_CONTEXT.specialist) || CSM_NAME || "Amanda";

    // Personalized lead-in — only when we're not already showing the priority
    // callout, so a question never opens with two stacked Amanda bubbles.
    const leadContent = personalLead(screen, answers);
    const showPersonalLead = !showPriorityCallout && !!leadContent;

    // One Amanda bubble per page: fold the priority callout / personal lead AND
    // the screen's own framing note (screen.lead) into a single box, instead of
    // stacking two separate Amanda bubbles.
    const screenLead = typeof screen.lead === "function" ? screen.lead(answers) : screen.lead;
    const leadNodes = [];
    if (showPriorityCallout) {
      leadNodes.push(<>Your sales call flagged <strong>{promotedPhrase}</strong> as a priority, so I've moved it up front.</>);
    } else if (showPersonalLead) {
      leadNodes.push(leadContent);
    }
    if (screenLead) leadNodes.push(screenLead);

    return (
      <div className="wiz-panel">
      <div className="wiz-panel-scroll">
        <div
            className={"wiz-panel-inner " + slideClass + (isAha ? " wiz-panel-inner--aha" : "")}
            key={phaseIdx}
            style={isWide ? { maxWidth: wideMaxWidth } : undefined}>

          {leadNodes.length > 0 && (
            <window.AmandaBubble compact name={specialist} style={{ marginBottom: 18 }}>
              <div style={{ display: "flex", flexDirection: "column", gap: 8, fontSize: 13.5, lineHeight: 1.45 }}>
                {leadNodes.map((node, i) => <div key={i}>{node}</div>)}
              </div>
            </window.AmandaBubble>
          )}

          <QMetaContext.Provider value={qMetaValue}>
          {screen.render({ answers, set, oauthState, doOAuth })}
          </QMetaContext.Provider>

          {/* Inline CTA — directly below content, left-aligned */}
          {!(primaryIsOAuth && oauthState === "working") &&
            <div className="q-actions question-q-actions" style={{ flexDirection: "row", alignItems: "center", flexWrap: "wrap" }}>
              <span className="wiz-kb-tip" data-tooltip="Press ↵ Enter">
              <button
                className="btn btn-primary"
                onClick={primaryHandler}
                disabled={primaryDisabled}
                title={screen.primaryDisabledTooltip || undefined}
                style={{ fontSize: 15, padding: "11px 22px", borderRadius: 8 }}>
                
                {primaryLabel}
                <span style={{
                  display: "inline-flex", alignItems: "center", justifyContent: "center",
                  marginLeft: 8, opacity: 0.7,
                  background: "rgba(255,255,255,0.15)", borderRadius: 4,
                  padding: "1px 5px", fontSize: 11, fontWeight: 600, letterSpacing: "0.02em"
                }}>⏎</span>
                {primaryIsOAuth && oauthState === "working" &&
                <span className="spinner" style={{ width: 12, height: 12, borderWidth: 2, marginLeft: 8 }}></span>
                }
              </button>
              </span>
              {/* Inline secondary CTA — educational expansion etc. */}
              {!(primaryIsOAuth && oauthState === "working") && screen.renderSecondary &&
                screen.renderSecondary({ answers, set })
              }
              {/* Flag for review — surfaces this question on the Call 1 punch list */}
              <span className="q-actions-trailing question-q-actions-trailing">
                <FlagForReview screen={screen} answers={answers} set={set} />
                {(skipLabel || !screen.anchor) && !isWide &&
                <button className="skip-link" onClick={onSkip}>{skipLabel || "Skip for now"}</button>
                }
              </span>
              {isListingsWide &&
              <span style={{ fontSize: 15, fontWeight: 500, color: "hsl(var(--gst-muted-foreground))" }}>
                  {(answers.selected_listings || window.MOCK_LISTINGS).length} listing{(answers.selected_listings || window.MOCK_LISTINGS).length === 1 ? "" : "s"} selected
                </span>
              }
            </div>
            }
          {primaryIsOAuth && oauthState === "working" && null}
        </div>
      </div>
    </div>);

  }

  /* ============ Rich (bold-aware) text ============ */
  // Amanda's lines can carry **double-asterisk** spans around the concrete facts
  // pulled from the handover (listing count, focus topic, add-on, migration source)
  // so those variables render bold. We parse the markers into segments once and
  // render either statically (RichBold) or progressively (TypewriterText). The
  // `**` markers are display-only and are stripped from the visible text, so the
  // char-by-char typewriter never pauses on a marker.
  function parseBoldSegments(text) {
    const segs = [];
    const re = /\*\*([\s\S]+?)\*\*/g;
    let last = 0, m;
    while ((m = re.exec(text)) !== null) {
      if (m.index > last) segs.push({ text: text.slice(last, m.index), bold: false });
      segs.push({ text: m[1], bold: true });
      last = m.index + m[0].length;
    }
    if (last < text.length) segs.push({ text: text.slice(last), bold: false });
    return segs;
  }
  // Render segments up to `limit` visible chars (null = all). Returns React nodes.
  function boldSegmentNodes(segments, limit) {
    let remaining = limit == null ? Infinity : limit;
    const out = [];
    for (let i = 0; i < segments.length && remaining > 0; i++) {
      const seg = segments[i];
      const slice = remaining === Infinity ? seg.text : seg.text.slice(0, remaining);
      if (remaining !== Infinity) remaining -= slice.length;
      if (!slice) continue;
      out.push(seg.bold
        ? <strong key={i}>{slice}</strong>
        : <React.Fragment key={i}>{slice}</React.Fragment>);
    }
    return out;
  }
  // Static bold-aware text (used for past turns in the thread).
  function RichBold({ text }) {
    if (!text) return null;
    return <>{boldSegmentNodes(parseBoldSegments(text), null)}</>;
  }
  window.RichBold = RichBold;

  /* ============ TypewriterText ============ */
  // Renders `text` character-by-character starting after `delay` ms,
  // one character every `speed` ms.  Respects prefers-reduced-motion.
  // Honors **bold** markers via the shared segment parser.
  function TypewriterText({ text, delay = 0, speed = 28, onDone }) {
    const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const segments = useMemo(() => parseBoldSegments(text || ""), [text]);
    const visibleLen = useMemo(
      () => segments.reduce((a, s) => a + s.text.length, 0),
      [segments],
    );
    const [count, setCount] = useState(reducedMotion ? visibleLen : 0);
    // Keep the latest onDone without re-triggering the typing effect when it changes.
    const doneRef = useRef(onDone);
    doneRef.current = onDone;
    useEffect(() => {
      const fireDone = () => { if (doneRef.current) doneRef.current(); };
      if (!text || reducedMotion) {
        setCount(visibleLen);
        const id = setTimeout(fireDone, 0);
        return () => clearTimeout(id);
      }
      setCount(0);
      let current = 0;
      let tick = null;
      const start = setTimeout(() => {
        tick = setInterval(() => {
          current += 1;
          setCount(current);
          if (current >= visibleLen) { clearInterval(tick); fireDone(); }
        }, speed);
      }, delay);
      return () => { clearTimeout(start); if (tick) clearInterval(tick); };
    }, [text, delay, speed, reducedMotion, visibleLen]);
    if (!text) return null;
    return <>{boldSegmentNodes(segments, count)}</>;
  }
  // Expose so screens.jsx BotAlert can use it at render time (wizard.jsx loads first in call order)
  window.TypewriterText = TypewriterText;

  // Progressive LLM copy (P2): track both the copy and whether the round-trip has
  // *settled* (succeeded or failed). `settled` lets the welcome show a typing
  // indicator while Gemini is in flight and only render real copy once it lands.
  function useObCopy() {
    const [state, setState] = useState({
      copy: window.OB_COPY || null,
      settled: !!window.OB_COPY_SETTLED,
    });
    useEffect(() => {
      if (window.OB_COPY_SETTLED) {
        setState({ copy: window.OB_COPY || null, settled: true });
      }
      const onCopy = (e) => setState({ copy: e.detail || window.OB_COPY || null, settled: true });
      window.addEventListener("ob-copy", onCopy);
      // Safety net: never hang the spinner if the event somehow never fires.
      const t = setTimeout(() => setState((s) => (s.settled ? s : { ...s, settled: true })), 12000);
      return () => { window.removeEventListener("ob-copy", onCopy); clearTimeout(t); };
    }, []);
    return state;
  }

  /* ============ Conversational welcome (S0) ============ */
  // Browser-side label maps (mirror context_api.py) so the intro can speak the
  // note's enum signals as natural language — without ever shipping raw note text.
  const INTRO_MIGRATION = {
    hostaway: "Hostaway", lodgify: "Lodgify", smoobu: "Smoobu", avantio: "Avantio",
    hostfully: "Hostfully", uplisting: "Uplisting", streamline: "Streamline",
    ownerrez: "OwnerRez", hospitable: "Hospitable", guesty_lite: "Guesty Lite",
    guesty_for_hosts: "Guesty for Hosts", beds24: "Beds24", cloudbeds: "Cloudbeds",
  };
  const INTRO_ADDON = {
    gpo: "GPO dynamic pricing", guestypay: "Guesty Pay", damage_protection: "Damage Protection",
    locks: "smart locks", accounting: "Accounting", abw: "the advanced bookings widget",
    auto_comply: "AutoComply", premium_channels: "premium channels",
  };
  const INTRO_FOCUS = {
    owner_reporting: "owner reporting", pricing_strategy: "pricing strategy",
    guest_messaging: "guest messaging", cleaner_workflows: "cleaner workflows",
    accounting_setup: "accounting setup", booking_website: "a direct booking site",
    reviews_reputation: "reviews & reputation", channel_mix: "channel mix",
  };
  function introJoin(arr) {
    const a = (arr || []).filter(Boolean);
    if (a.length <= 1) return a[0] || "";
    if (a.length === 2) return a[0] + " and " + a[1];
    return a.slice(0, -1).join(", ") + ", and " + a[a.length - 1];
  }

  function WelcomePanel({ onContinue, phaseIdx, answers, set }) {
    const ctx = window.OB_CONTEXT || null;
    const prefill = (ctx && ctx.prefill) || {};
    const csmName = CSM_NAME || "Amanda";
    const firstName = SF_PREFILL.first_name;
    const repFirst = ctx && ctx.rep ? String(ctx.rep).trim().split(/\s+/)[0] : null;

    // Progressive LLM copy: when AI is on we briefly show a typing indicator, then
    // swap the deterministic opening for Gemini's note-aware line once it lands.
    const { copy: obCopy, settled: obSettled } = useObCopy();
    const aiEnabled = !!(window.__OB_SESSION && window.__OB_SESSION.ai_enabled);
    const llmBotLine = obCopy && obCopy.bot_line ? String(obCopy.bot_line).trim() : "";

    // --- Honest fact fragments, drawn only from signals that actually exist ---
    const n = SF_PREFILL.listing_count;
    const migration = prefill.migration_source
      ? (INTRO_MIGRATION[prefill.migration_source] || null)
      : null;
    const firstTime = prefill.prior_pms_experience === "none_first_time";
    const experienced = prefill.prior_pms_experience === "experienced";
    const addons = (prefill.addon_intent || []).map((a) => INTRO_ADDON[a] || a).filter(Boolean);
    const focusLabels = (prefill.focus_topics || []).map((f) => INTRO_FOCUS[f] || f).filter(Boolean);

    // Headline — the one-line "here's what I have" the user confirms first.
    const headParts = [];
    if (n) headParts.push("**" + n + " listing" + (n === 1 ? "" : "s") + "**");
    if (migration) headParts.push("moving over from **" + migration + "**");
    else if (firstTime) headParts.push("new to running a PMS");
    if (addons.length) headParts.push("with **" + introJoin(addons) + "** in the mix");
    const hasFacts = headParts.length > 0;
    const headline = hasFacts ? headParts.join(", ") : "";

    // Softer signals worth a second confirm — only surfaced when present.
    const hasSofter = focusLabels.length > 0 || experienced || firstTime;
    const notePresent = !!(ctx && ctx.note && ctx.note.present);

    // --- Bot lines per conversation node ---
    // Only claim to have read notes if notes actually exist, and only ask the
    // user to confirm facts when we actually have facts to show.
    const greetLines = (() => {
      const lines = [
        firstName
          ? "Hi " + firstName + " — I'm " + csmName + ", your onboarding specialist."
          : "Hi — I'm " + csmName + ", your onboarding specialist.",
      ];
      if (notePresent) {
        lines.push(repFirst
          ? "I read through " + repFirst + "'s handover notes before we start."
          : "I read through the notes from your sales call before we start.");
      }
      if (hasFacts) {
        lines.push("Here's what I've got: " + headline + ".");
        lines.push("Does that all look right?");
      } else {
        lines.push("I don't have much on file yet, so we'll build it together as we go.");
      }
      return lines;
    })();
    const confirm2Lines = (() => {
      const bits = [];
      if (experienced) bits.push("you've run a PMS before, so you know your way around");
      else if (firstTime) bits.push("this is your first time on a PMS");
      if (focusLabels.length) bits.push("the thing you most want to get right is **" + introJoin(focusLabels) + "**");
      const lead = bits.length === 2
        ? "One more read from the notes: " + bits[0] + ", and " + bits[1] + "."
        : "One more read from the notes — " + (bits[0] || "") + ".";
      return [lead, "Did I get that right?"];
    })();
    // Prefer the LLM opening (a single warm bubble that ends in one confirm question);
    // fall back to the deterministic multi-line greeting offline or while it loads.
    const confirm1Lines = llmBotLine ? [llmBotLine] : greetLines;
    const linesFor = {
      confirm1: confirm1Lines,
      clarify1_change: ["Got it — what changed?"],
      clarify1_off: ["No problem. What should I fix?"],
      confirm2: confirm2Lines,
      clarify2: ["Tell me a little more and I'll adjust."],
      ready: [focusLabels.length
        ? "Perfect — I've moved your **" + introJoin(focusLabels) + "** section up so we get to it sooner. Let's dive in."
        : "Perfect — I've got what I need to get started. Let's dive in."],
    };

    const choices1 = hasFacts
      ? [
          { kind: "yes", label: "Yep, that's us" },
          { kind: "change", label: "Mostly right — one thing changed" },
          { kind: "off", label: "Not quite" },
        ]
      : [{ kind: "yes", label: "Sounds good" }];
    const choices2 = [
      { kind: "yes", label: "Spot on" },
      { kind: "adjust", label: "Let me adjust" },
    ];

    // --- Conversation state ---
    const [history, setHistory] = useState([]); // [{role:'bot',lines:[]}|{role:'user',text}]
    const [node, setNode] = useState("confirm1");
    const [inputReady, setInputReady] = useState(false);
    const [draft, setDraft] = useState("");
    const [thinking, setThinking] = useState(false);
    const [ackText, setAckText] = useState("");
    const ackNextRef = useRef("ready");
    const scrollRef = useRef(null);

    // Reset the per-turn input gate whenever Amanda starts a new line of dialogue.
    useEffect(() => { setInputReady(false); setDraft(""); }, [node]);
    // Keep the freshest turn in view as the thread grows.
    useEffect(() => {
      if (scrollRef.current) scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }, [history, node, inputReady, thinking, ackText]);

    const curLines = linesFor[node] || [];
    // Hold the opening bubble on a typing indicator until Gemini's copy settles.
    const waitingForCopy = aiEnabled && !obSettled && node === "confirm1";
    const SPEED = 18;
    let twCursor = 220;
    const timings = curLines.map((ln) => {
      const start = twCursor;
      twCursor += Math.max(ln.length * SPEED, 380) + 120;
      return start;
    });

    const pushBot = (lines) => setHistory((h) => [...h, { role: "bot", lines }]);
    const pushUser = (text) => setHistory((h) => [...h, { role: "user", text }]);
    const afterConfirm1 = () => (hasSofter ? "confirm2" : "ready");

    const runAck = (text) => {
      setThinking(true);
      setAckText("");
      const field = {
        label: "Clarification about the account setup",
        hint: "The user is correcting or adding detail to what we have on file.",
        options: [],
      };
      const passthrough = "Got it — I've noted that and passed it to " + csmName + " for your first call.";
      fetch("/api/normalize", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ field, text }),
      })
        .then((r) => (r.ok ? r.json() : null))
        .then((data) => {
          const summary = (data && data.result && data.result.summary) || passthrough;
          setThinking(false);
          setAckText(summary);
        })
        .catch(() => { setThinking(false); setAckText(passthrough); });
      setNode("ack");
    };

    const ackDone = () => {
      pushBot([ackText]);
      setNode(ackNextRef.current);
    };

    const choose1 = (choice) => {
      pushBot(confirm1Lines);
      pushUser(choice.label);
      if (choice.kind === "yes") { setNode(afterConfirm1()); return; }
      ackNextRef.current = afterConfirm1();
      setNode(choice.kind === "change" ? "clarify1_change" : "clarify1_off");
    };
    const choose2 = (choice) => {
      pushBot(confirm2Lines);
      pushUser(choice.label);
      if (choice.kind === "yes") { setNode("ready"); return; }
      ackNextRef.current = "ready";
      setNode("clarify2");
    };
    const submitText = () => {
      const t = draft.trim();
      if (t.length < 2 || thinking) return;
      pushBot(linesFor[node]);
      pushUser(t);
      runAck(t);
    };
    const finish = () => {
      if (set) set({
        intro_done: true,
        intro_focus_label: focusLabels[0] || null,
        intro_focus_all: focusLabels,
        intro_migration_label: migration || null,
        intro_first_time: firstTime,
        intro_experienced: experienced,
      });
      onContinue();
    };

    return (
      <div className="wiz-panel">
      <div className="wiz-panel-scroll" ref={scrollRef}>
        <div className="wiz-panel-inner welcome-panel-inner" key={phaseIdx}>
          <div className="intro-thread">
            {history.map((turn, i) => turn.role === "bot" ? (
              <window.AmandaBubble key={"h" + i} name={csmName} compact>
                {turn.lines.map((ln, j) => <div key={j} className="intro-bot-line"><RichBold text={ln} /></div>)}
              </window.AmandaBubble>
            ) : (
              <div key={"h" + i} className="intro-user">
                <div className="intro-user-bubble">{turn.text}</div>
              </div>
            ))}

            {node === "ack" ? (
              <window.AmandaBubble key="ack" name={csmName} compact>
                {thinking || !ackText
                  ? <window.TypingDots />
                  : <div className="intro-bot-line">
                      <TypewriterText text={ackText} delay={120} speed={SPEED} onDone={ackDone} />
                    </div>}
              </window.AmandaBubble>
            ) : (
              <window.AmandaBubble key={"node-" + node} name={csmName} compact>
                {waitingForCopy
                  ? <window.TypingDots />
                  : curLines.map((ln, i) => (
                      <div key={i} className="intro-bot-line">
                        <TypewriterText
                          text={ln}
                          delay={timings[i]}
                          speed={SPEED}
                          onDone={i === curLines.length - 1 ? () => setInputReady(true) : undefined}
                        />
                      </div>
                    ))}
              </window.AmandaBubble>
            )}
          </div>

          {inputReady && (node === "confirm1" || node === "confirm2") && (
            <div className="intro-choices">
              {(node === "confirm1" ? choices1 : choices2).map((c) => (
                <button
                  key={c.kind}
                  className="intro-choice"
                  onClick={() => (node === "confirm1" ? choose1(c) : choose2(c))}
                >
                  {c.label}
                </button>
              ))}
            </div>
          )}

          {inputReady && (node === "clarify1_change" || node === "clarify1_off" || node === "clarify2") && (
            <div className="intro-composer">
              <textarea
                className="intro-input"
                rows={2}
                value={draft}
                placeholder="Type your answer…"
                autoFocus
                onChange={(e) => setDraft(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); submitText(); }
                }}
              />
              <button
                className="intro-send"
                onClick={submitText}
                disabled={draft.trim().length < 2 || thinking}
              >
                Send
              </button>
            </div>
          )}

          {node === "ready" && inputReady && (
            <div className="q-actions welcome-q-actions">
              <span className="wiz-kb-tip" data-tooltip="Press ↵ Enter">
                <button
                  className="btn btn-primary"
                  onClick={finish}
                  autoFocus
                  style={{ fontSize: 15, padding: "12px 28px", borderRadius: 8 }}
                >
                  Let's go
                  <span style={{
                    display: "inline-flex", alignItems: "center", justifyContent: "center",
                    marginLeft: 8, opacity: 0.7,
                    background: "rgba(255,255,255,0.15)", borderRadius: 4,
                    padding: "1px 5px", fontSize: 11, fontWeight: 600, letterSpacing: "0.02em"
                  }}>⏎</span>
                </button>
              </span>
            </div>
          )}

        </div>
      </div>
    </div>);
  }

  /* ============ Milestone panel ============ */
  function MilestonePanel({ onContinue, onDeferFinancials, direction, phaseIdx }) {
    const slideClass = direction >= 0 ? "slide-forward" : "slide-back";
    const ctx = window.OB_CONTEXT || null;
    const deferFin = !!(ctx && ctx.flags && ctx.flags.defer_financials);
    const csmName = window.CSM_NAME || "your specialist";
    const repFirst = ctx && ctx.rep ? String(ctx.rep).trim().split(/\s+/)[0] : "";

    const order = adaptivePlan().order;
    const finIdx = order.indexOf(4);
    const done = finIdx >= 0 ? order.slice(0, finIdx) : order.slice();
    const after = finIdx >= 0 ? order.slice(finIdx + 1) : [];
    const doneCount = done.length;
    const doneLabel = doneCount + " section" + (doneCount === 1 ? "" : "s") + " complete";
    const lastDoneName = doneCount ? (SECTION_NAMES[done[doneCount - 1]] || "your last section") : "";
    const subtitle = doneCount
      ? <>{lastDoneName} {doneCount === 1 ? "is" : "and the sections before it are"} set.{" "}</>
      : <>You're off to a strong start.{" "}</>;

    return (
      <div className="wiz-panel">
      <div className="wiz-panel-scroll">
        <div className={"wiz-panel-inner " + slideClass} key={phaseIdx}>
          <div className="q-meta">
            <span>Milestone</span>
            <span className="dot"></span>
            <span>{doneLabel}</span>
          </div>
          <h1 className="q-title">Nice work.</h1>
          <p className="q-help">
            {deferFin
              ? <>{subtitle}{repFirst ? repFirst + " noted" : "Your notes say"} you'd rather walk through taxes &amp; fees live — your call, below.</>
              : <>{subtitle}Take a breath — we'll move on to financials next.</>}
          </p>
          <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
            {done.map((sec) => (
              <MilestoneRow key={sec} icon="✓" label={"Section " + (adaptivePosition(sec) + 1) + " — " + (SECTION_NAMES[sec] || "")} done />
            ))}
            <MilestoneRow icon="●" label={"Section " + (adaptivePosition(4) + 1) + " — Financials"} active />
            {after.map((sec) => (
              <MilestoneRow key={sec} icon="○" label={"Section " + (adaptivePosition(sec) + 1) + " — " + (SECTION_NAMES[sec] || "")} />
            ))}
            <MilestoneRow icon="○" label="Review and confirm" />
          </div>
          <div className="q-actions" style={{ display: "flex", alignItems: "center", gap: 14 }}>
            <span className="wiz-kb-tip" data-tooltip="Press ↵ Enter">
              <button className="btn btn-primary" onClick={onContinue} style={{ fontSize: 15, padding: "11px 22px" }}>
                {deferFin ? "Walk through financials now" : "Continue"}
                <span style={{ display: "inline-flex", alignItems: "center", justifyContent: "center", marginLeft: 8, opacity: 0.7, background: "rgba(255,255,255,0.15)", borderRadius: 4, padding: "1px 5px", fontSize: 11, fontWeight: 600 }}>⏎</span>
              </button>
            </span>
            {deferFin && onDeferFinancials && (
              <button className="skip-link" onClick={onDeferFinancials}>
                Skip — cover taxes &amp; fees with {csmName} on Call 1
              </button>
            )}
          </div>
        </div>
      </div>
    </div>);

  }

  function MilestoneRow({ icon, label, done, active }) {
    return (
      <div style={{
        display: "flex", alignItems: "center", gap: 12,
        padding: "10px 14px",
        border: "1px solid hsl(var(--gst-border))",
        borderRadius: 10,
        background: done ? "hsl(var(--gst-muted) / 0.5)" : active ? "hsl(var(--gst-primary) / 0.06)" : "white",
        opacity: !done && !active ? 0.55 : 1
      }}>
      <div style={{
          width: 22, height: 22, borderRadius: 999,
          background: done ? "hsl(var(--gst-success))" : active ? "hsl(var(--gst-primary))" : "hsl(var(--gst-border))",
          color: "white",
          display: "flex", alignItems: "center", justifyContent: "center",
          fontSize: 12, fontWeight: 700, flexShrink: 0
        }}>{icon}</div>
      <div style={{ flex: 1, fontSize: 14, fontWeight: active || done ? 600 : 400 }}>{label}</div>
    </div>);

  }

  /* ============ Review panel ============ */
  function ReviewPanel({ canGoBack, onBack, onContinue, answers, direction, phaseIdx }) {
    const skipCount = (answers.__skipped || []).length;
    const slideClass = direction >= 0 ? "slide-forward" : "slide-back";
    return (
      <div className="wiz-panel">
      <div className="wiz-panel-scroll">
        <div className={"wiz-panel-inner " + slideClass} key={phaseIdx}>
          <div className="q-meta"><span>Section 8 of 8 · Review and confirm</span></div>
          <window.BotAlert>
            <div>Last step before we set everything up. Look it over — anything off, click "Edit" to fix it.</div>
          </window.BotAlert>
          <h1 className="q-title">Review your answers</h1>
          <p className="q-help">Once you confirm, we'll set up your Guesty account with these choices. You can change anything later in settings.</p>

          {skipCount > 0 &&
            <div style={{ display: "flex", alignItems: "flex-start", gap: 10, padding: "12px 14px", background: "hsl(var(--gst-warning) / 0.08)", border: "1px solid hsl(var(--gst-warning) / 0.25)", borderRadius: 8 }}>
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="hsl(var(--gst-warning))" strokeWidth="2" style={{ flexShrink: 0, marginTop: 1 }}><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z" /><line x1="12" y1="9" x2="12" y2="13" /><line x1="12" y1="17" x2="12.01" y2="17" /></svg>
              <div style={{ flex: 1, fontSize: 13 }}>
                <strong>{skipCount} item{skipCount === 1 ? "" : "s"} will go to your Call 1 punch list</strong> — your CSM will help you finish them.{" "}
                <button style={{ background: "transparent", border: 0, color: "hsl(var(--gst-primary))", fontWeight: 600, fontSize: 13, padding: 0, cursor: "pointer", fontFamily: "inherit" }}>See punch list</button>
              </div>
            </div>
            }

          <div className="q-actions review-q-actions">
            <span className="wiz-kb-tip" data-tooltip="Press ↵ Enter">
              <button className="btn btn-primary" onClick={onContinue} style={{ fontSize: 15, padding: "11px 22px" }}>
                Confirm and continue
                <span style={{ display: "inline-flex", alignItems: "center", justifyContent: "center", marginLeft: 8, opacity: 0.7, background: "rgba(255,255,255,0.15)", borderRadius: 4, padding: "1px 5px", fontSize: 11, fontWeight: 600 }}>⏎</span>
              </button>
            </span>
            {canGoBack &&
              <button className="skip-link" onClick={onBack}>Go back to edit</button>
              }
          </div>
        </div>
      </div>
    </div>);

  }

  /* ============ Confirmation dialog ============ */
  function ConfirmDialog({ onCancel, onConfirm }) {
    return (
      <div style={{
        position: "fixed", inset: 0, zIndex: 100,
        background: "hsl(var(--gst-foreground) / 0.5)",
        display: "flex", alignItems: "center", justifyContent: "center",
        padding: 20,
        animation: "fade 200ms ease forwards"
      }} onClick={onCancel}>
      <div style={{
          background: "white",
          borderRadius: 12,
          padding: 28,
          maxWidth: 460, width: "100%",
          boxShadow: "var(--shadow-lg)"
        }} onClick={(e) => e.stopPropagation()}>
        <h2 style={{ margin: "0 0 8px", fontSize: 20, fontWeight: 600 }}>Confirm your setup?</h2>
        <p style={{ margin: "0 0 22px", fontSize: 14, color: "hsl(var(--gst-muted-foreground))", lineHeight: 1.55 }}>
          We'll start setting up your account with these answers. You can change settings later, but you can't reopen this wizard.
        </p>
        <div style={{ display: "flex", gap: 10, justifyContent: "flex-end" }}>
          <button className="btn btn-secondary" onClick={onCancel}>Keep reviewing</button>
          <button className="btn btn-primary" onClick={onConfirm}>Confirm setup</button>
        </div>
      </div>
    </div>);

  }

  /* ============ Section 9 — Setup loader ============ */
  function SetupPanel({ onContinue }) {
    // Verb+object specific copy, with done variant
    const tasks = [
    { run: "Connecting Airbnb sync engine…", done: "Airbnb sync engine connected" },
    { run: "Importing reservations…", done: "Reservations imported" },
    { run: "Loading guest profiles…", done: "Guest profiles loaded" },
    { run: "Setting up cleaning workflow…", done: "Cleaning workflow set up" },
    { run: "Setting up fees and taxes…", done: "Fees and taxes configured" },
    { run: "Building your booking website…", done: "Booking website ready" },
    { run: "Briefing " + CSM_NAME + " on your setup…", done: CSM_NAME + " is briefed" }];

    const [step, setStep] = useState(0);

    useEffect(() => {
      if (step < tasks.length) {
        const dur = 700 + Math.random() * 600;
        const t = setTimeout(() => setStep((s) => s + 1), dur);
        return () => clearTimeout(t);
      } else {
        const t = setTimeout(() => onContinue(), 900);
        return () => clearTimeout(t);
      }
    }, [step]);

    const remainingSeconds = Math.max(0, Math.round((tasks.length - step) * 1.0));

    return (
      <div className="s9-stage" style={{ gridColumn: "1 / -1" }}>
      <div className="s9-card">
        <h1>Setting up your Guesty account</h1>
        <p className="sub">This usually takes under a minute. You can leave this tab open — we'll let you know when it's done.</p>
        <div className="s9-tasks">
          {tasks.map((t, i) => {
              const done = i < step;
              const active = i === step;
              const pending = i > step;
              return (
                <div key={i} className={"s9-task " + (done ? "done" : active ? "" : "pending")}>
                <div className="icn">
                  {done &&
                    <svg className="tick" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round">
                      <polyline points="20 6 9 17 4 12"></polyline>
                    </svg>
                    }
                  {active && <div className="spinner"></div>}
                  {pending && <div style={{ width: 12, height: 12, border: "2px solid hsl(var(--gst-border))", borderRadius: 999 }}></div>}
                </div>
                <div className="label">{done ? t.done : t.run}</div>
              </div>);

            })}
        </div>
        <div style={{
            marginTop: 18,
            display: "flex", justifyContent: "space-between",
            fontSize: 12, color: "hsl(var(--gst-muted-foreground))"
          }}>
          <span>{step} of {tasks.length} steps complete</span>
          {step > 0 && step < tasks.length && <span>About {remainingSeconds} seconds left</span>}
        </div>
      </div>
    </div>);

  }

  /* ============ Section 10 — Done = Guesty homepage mock ============ */

  const ACADEMY_BASE = "https://academy.guesty.com/";
  const TOPIC_META = {
    "Pricing strategy": {
      desc: "Dynamic pricing, seasonal rates, and minimum-stay rules.",
      url: ACADEMY_BASE + "pricing-strategy",
    },
    "Channel mix": {
      desc: "Choosing which channels to list on and how to balance them.",
      url: ACADEMY_BASE + "channel-manager",
    },
    "Guest messaging": {
      desc: "Templates, automation, and unified inbox best practices.",
      url: ACADEMY_BASE + "unified-inbox",
    },
    "Cleaner workflows": {
      desc: "Turnover tasks, cleaner assignments, and quality checks.",
      url: ACADEMY_BASE + "operations-cleaners",
    },
    "Accounting setup": {
      desc: "Chart of accounts, revenue recognition, and owner statements.",
      url: ACADEMY_BASE + "accounting",
    },
    "Owner reporting": {
      desc: "Statements, reservation breakdowns, and owner portals.",
      url: ACADEMY_BASE + "owner-reporting",
    },
    "Booking website": {
      desc: "Customizing your direct booking site and reducing OTA fees.",
      url: ACADEMY_BASE + "booking-website",
    },
    "Reviews and reputation": {
      desc: "Collecting reviews, responding fast, and improving scores.",
      url: ACADEMY_BASE + "reviews",
    },
  };

  function DonePanel({ answers, set }) {
    const focusTopics = (answers.focus_topics ?? ["Pricing strategy", "Channel mix"]).slice(0, 3);
    const importedCount = (answers.selected_listings || window.MOCK_LISTINGS).length;

    return (
      <div className="home-shell" style={{ gridColumn: "1 / -1" }}>
        <HomeHeader />
        <div className="home-body">
          <HomeSidebar />
          <main className="home-main">
            <HomeGreeting firstName={SF_PREFILL.first_name} importedCount={importedCount} />
            <NextCallSection csmName={CSM_NAME} />
            <QuestionCarouselSection answers={answers} set={set} />
            <TopicsSection topics={focusTopics} flagged={answers.__flagged || []} />
            <DailyOverviewSection />
            <TrendsOverviewSection />
            <RevenueSection />
          </main>
        </div>
      </div>
    );
  }

  /* -------- Header (teal, fixed 56px) -------- */
  function HomeHeader() {
    return (
      <header className="home-header">
        <div className="home-header-brand">
          <button className="home-iconbtn home-iconbtn--onTeal" aria-label="Toggle navigation">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
          </button>
          <SkeletonImg
            src="assets/guesty-home-logo.svg"
            alt="Guesty"
            className="home-header-logo-img"
            wrapStyle={{ display: "inline-block", height: 22, width: 68, lineHeight: 0, borderRadius: 3 }}
          />
        </div>
        <div className="home-search">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
          <span className="home-search-placeholder">Type</span>
          <kbd className="home-search-kbd">/</kbd>
          <span className="home-search-placeholder">to search</span>
        </div>
        <div className="home-header-utilities">
          <button className="home-iconbtn home-iconbtn--onTeal" aria-label="Guesty AI">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#c4b5fd" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"><path d="M12 3l1.7 4.6 4.6 1.7-4.6 1.7L12 15.6 10.3 11 5.7 9.3 10.3 7.6z" fill="#c4b5fd"/><circle cx="19" cy="5" r="1.4" fill="#c4b5fd"/><circle cx="5" cy="19" r="1.4" fill="#c4b5fd"/></svg>
          </button>
          <button className="home-iconbtn home-iconbtn--onTeal" aria-label="Bookmarks">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/></svg>
          </button>
          <button className="home-iconbtn home-iconbtn--onTeal" aria-label="Create new">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="16"/><line x1="8" y1="12" x2="16" y2="12"/></svg>
          </button>
          <button className="home-iconbtn home-iconbtn--onTeal" aria-label="Apps">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>
          </button>
          <button className="home-iconbtn home-iconbtn--onTeal" aria-label="Notifications">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M18 8a6 6 0 0 0-12 0c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>
          </button>
          <button className="home-iconbtn home-iconbtn--onTeal" aria-label="Help">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
          </button>
          <div className="home-avatar" aria-label={SF_PREFILL.first_name + " account menu"}>
            {SF_PREFILL.first_name[0]}
          </div>
        </div>
      </header>
    );
  }

  /* -------- Sidebar -------- */
  function HomeSidebar() {
    const S = { fill:"none", stroke:"currentColor", strokeWidth:"2", strokeLinecap:"round", strokeLinejoin:"round" };
    const V = { width:18, height:18, viewBox:"0 0 20 20", ...S };

    const IconHome         = () => <svg {...V}><path d="M7.5 18.3332V9.99984H12.5V18.3332M2.5 7.49984L10 1.6665L17.5 7.49984V16.6665C17.5 17.1085 17.3244 17.5325 17.0118 17.845C16.6993 18.1576 16.2754 18.3332 15.8333 18.3332H4.16667C3.72464 18.3332 3.30072 18.1576 2.98816 17.845C2.67559 17.5325 2.5 17.1085 2.5 16.6665V7.49984Z"/></svg>;
    const IconInbox        = () => <svg {...V}><path d="M18.3332 10.0002H13.3332L11.6665 12.5002H8.33317L6.6665 10.0002H1.6665M1.6665 10.0002L4.5415 4.2585C4.67948 3.98082 4.89219 3.74714 5.15571 3.58373C5.41922 3.42032 5.7231 3.33366 6.03317 3.3335H13.9665C14.2766 3.33366 14.5805 3.42032 14.844 3.58373C15.1075 3.74714 15.3202 3.98082 15.4582 4.2585L18.3332 10.0002V15.0002C18.3332 15.4422 18.1576 15.8661 17.845 16.1787C17.5325 16.4912 17.1085 16.6668 16.6665 16.6668H3.33317C2.89114 16.6668 2.46722 16.4912 2.15466 16.1787C1.8421 15.8661 1.6665 15.4422 1.6665 15.0002V10.0002Z"/></svg>;
    const IconCalendar     = () => <svg {...V}><path d="M7.5 2.5H4.16667C3.72464 2.5 3.30072 2.67559 2.98816 2.98816C2.67559 3.30072 2.5 3.72464 2.5 4.16667V7.5M7.5 2.5H15.8333C16.2754 2.5 16.6993 2.67559 17.0118 2.98816C17.3244 3.30072 17.5 3.72464 17.5 4.16667V7.5M7.5 2.5V17.5M2.5 7.5V15.8333C2.5 16.2754 2.67559 16.6993 2.98816 17.0118C3.30072 17.3244 3.72464 17.5 4.16667 17.5H7.5M2.5 7.5H17.5M17.5 7.5V15.8333C17.5 16.2754 17.3244 16.6993 17.0118 17.0118C16.6993 17.3244 16.2754 17.5 15.8333 17.5H7.5"/></svg>;
    const IconListings     = () => <svg {...V}><path d="M11.6665 5.83341L14.1665 8.33342M7.83317 8.8335L1.6665 15.0002V17.5002C1.6665 18.0002 1.99984 18.3335 2.49984 18.3335H5.83317V15.8335H8.33317V13.3335H9.99984L11.1665 12.1668M10.3331 2.25C11.0831 1.5 12.4164 1.5 13.1664 2.25L17.7498 6.83333C18.4998 7.58333 18.4998 8.91667 17.7498 9.66667L14.6664 12.75C13.9164 13.5 12.5831 13.5 11.8331 12.75L7.24976 8.16667C6.49976 7.41667 6.49976 6.08333 7.24976 5.33333L10.3331 2.25Z"/></svg>;
    const IconMarketing    = () => <svg {...V}><path d="M3.33317 9.99984C2.89114 9.99984 2.46722 9.82424 2.15466 9.51168C1.8421 9.19912 1.6665 8.7752 1.6665 8.33317V5.83317L5.3415 2.15817C5.49655 2.0022 5.68094 1.87845 5.88403 1.79407C6.08712 1.70968 6.30491 1.66633 6.52484 1.6665H13.4748C13.6948 1.66633 13.9126 1.70968 14.1156 1.79407C14.3187 1.87845 14.5031 2.0022 14.6582 2.15817L18.3332 5.83317V8.33317C18.3332 8.7752 18.1576 9.19912 17.845 9.51168C17.5325 9.82424 17.1085 9.99984 16.6665 9.99984M1.6665 5.83317H18.3332M3.33317 9.99984V16.6665C3.33317 17.1085 3.50877 17.5325 3.82133 17.845C4.13389 18.1576 4.55781 18.3332 4.99984 18.3332H14.9998C15.4419 18.3332 15.8658 18.1576 16.1783 17.845C16.4909 17.5325 16.6665 17.1085 16.6665 16.6665V9.99984M3.33317 9.99984C3.82006 9.97304 4.28506 9.78879 4.65817 9.47484C4.7576 9.40298 4.87716 9.36431 4.99984 9.36431C5.12252 9.36431 5.24207 9.40298 5.3415 9.47484C5.71461 9.78879 6.17962 9.97304 6.6665 9.99984C7.15339 9.97304 7.6184 9.78879 7.9915 9.47484C8.09094 9.40298 8.21049 9.36431 8.33317 9.36431C8.45585 9.36431 8.5754 9.40298 8.67484 9.47484C9.04795 9.78879 9.51295 9.97304 9.99984 9.99984C10.4867 9.97304 10.9517 9.78879 11.3248 9.47484C11.4243 9.40298 11.5438 9.36431 11.6665 9.36431C11.7892 9.36431 11.9087 9.40298 12.0082 9.47484C12.3813 9.78879 12.8463 9.97304 13.3332 9.99984C13.8201 9.97304 14.2851 9.78879 14.6582 9.47484C14.7576 9.40298 14.8772 9.36431 14.9998 9.36431C15.1225 9.36431 15.2421 9.40298 15.3415 9.47484C15.7146 9.78879 16.1796 9.97304 16.6665 9.99984M12.4998 18.3332V14.9998C12.4998 14.5578 12.3242 14.1339 12.0117 13.8213C11.6991 13.5088 11.2752 13.3332 10.8332 13.3332H9.1665C8.72448 13.3332 8.30055 13.5088 7.98799 13.8213C7.67543 14.1339 7.49984 14.5578 7.49984 14.9998V18.3332"/></svg>;
    const IconFinancials   = () => <svg {...V}><path d="M17.5 13.3333V16.6667C17.5 16.8877 17.4122 17.0996 17.2559 17.2559C17.0996 17.4122 16.8877 17.5 16.6667 17.5H4.16667C3.72464 17.5 3.30072 17.3244 2.98816 17.0118C2.67559 16.6993 2.5 16.2754 2.5 15.8333V4.16667C2.5 3.72464 2.67559 3.30072 2.98816 2.98816C3.30072 2.67559 3.72464 2.5 4.16667 2.5H15C15.221 2.5 15.433 2.5878 15.5893 2.74408C15.7455 2.90036 15.8333 3.11232 15.8333 3.33333V5.83333M2.5 4.16667C2.5 4.60869 2.67559 5.03262 2.98816 5.34518C3.30072 5.65774 3.72464 5.83333 4.16667 5.83333H16.6667C16.8877 5.83333 17.0996 5.92113 17.2559 6.07741C17.4122 6.23369 17.5 6.44565 17.5 6.66667V10M17.5 10H15C14.558 10 14.134 10.1756 13.8215 10.4882C13.5089 10.8007 13.3333 11.2246 13.3333 11.6667C13.3333 12.1087 13.5089 12.5326 13.8215 12.8452C14.134 13.1577 14.558 13.3333 15 13.3333H17.5M17.5 10C17.721 10 17.933 10.0878 18.0893 10.2441C18.2455 10.4004 18.3333 10.6123 18.3333 10.8333V12.5C18.3333 12.721 18.2455 12.933 18.0893 13.0893C17.933 13.2455 17.721 13.3333 17.5 13.3333"/></svg>;
    const IconGuestPay     = () => <svg {...V}><path d="M1.6665 8.33317H18.3332M3.33317 4.1665H16.6665C17.587 4.1665 18.3332 4.9127 18.3332 5.83317V14.1665C18.3332 15.087 17.587 15.8332 16.6665 15.8332H3.33317C2.4127 15.8332 1.6665 15.087 1.6665 14.1665V5.83317C1.6665 4.9127 2.4127 4.1665 3.33317 4.1665Z"/></svg>;
    const IconAccounting   = () => <svg {...V}><path d="M9.99984 5.83333C9.99984 4.94928 9.64865 4.10143 9.02353 3.47631C8.39841 2.85119 7.55056 2.5 6.6665 2.5H1.6665V15H7.49984C8.16288 15 8.79876 15.2634 9.2676 15.7322C9.73645 16.2011 9.99984 16.837 9.99984 17.5M9.99984 5.83333V17.5M9.99984 5.83333C9.99984 4.94928 10.351 4.10143 10.9761 3.47631C11.6013 2.85119 12.4491 2.5 13.3332 2.5H18.3332V15H12.4998C11.8368 15 11.2009 15.2634 10.7321 15.7322C10.2632 16.2011 9.99984 16.837 9.99984 17.5"/></svg>;
    const IconIntegrations = () => <svg {...V}><path d="M10 2.5V16.6667C10 16.8877 9.9122 17.0996 9.75592 17.2559C9.59964 17.4122 9.38768 17.5 9.16667 17.5H4.16667C3.72464 17.5 3.30072 17.3244 2.98816 17.0118C2.67559 16.6993 2.5 16.2754 2.5 15.8333V4.16667C2.5 3.72464 2.67559 3.30072 2.98816 2.98816C3.30072 2.67559 3.72464 2.5 4.16667 2.5H15.8333C16.2754 2.5 16.6993 2.67559 17.0118 2.98816C17.3244 3.30072 17.5 3.72464 17.5 4.16667V9.16667C17.5 9.38768 17.4122 9.59964 17.2559 9.75592C17.0996 9.9122 16.8877 10 16.6667 10H2.5M13.3333 15.8333H18.3333M15.8333 18.3333V13.3333"/></svg>;
    const IconSettings     = () => <svg {...V}><path d="M10.1833 1.6665H9.81667C9.37464 1.6665 8.95072 1.8421 8.63816 2.15466C8.3256 2.46722 8.15 2.89114 8.15 3.33317V3.48317C8.1497 3.77544 8.07255 4.0625 7.92628 4.31553C7.78002 4.56857 7.56978 4.7787 7.31667 4.92484L6.95834 5.13317C6.70497 5.27945 6.41756 5.35646 6.125 5.35646C5.83244 5.35646 5.54503 5.27945 5.29167 5.13317L5.16667 5.0665C4.78422 4.84589 4.32987 4.78604 3.90334 4.90009C3.47681 5.01415 3.11296 5.29278 2.89167 5.67484L2.70833 5.9915C2.48772 6.37395 2.42787 6.82831 2.54192 7.25484C2.65598 7.68137 2.93461 8.04521 3.31667 8.2665L3.44167 8.34984C3.69356 8.49526 3.90302 8.70408 4.04921 8.95553C4.1954 9.20698 4.27325 9.49231 4.275 9.78317V10.2082C4.27617 10.5019 4.19971 10.7906 4.05337 11.0453C3.90703 11.2999 3.69601 11.5113 3.44167 11.6582L3.31667 11.7332C2.93461 11.9545 2.65598 12.3183 2.54192 12.7448C2.42787 13.1714 2.48772 13.6257 2.70833 14.0082L2.89167 14.3248C3.11296 14.7069 3.47681 14.9855 3.90334 15.0996C4.32987 15.2136 4.78422 15.1538 5.16667 14.9332L5.29167 14.8665C5.54503 14.7202 5.83244 14.6432 6.125 14.6432C6.41756 14.6432 6.70497 14.7202 6.95834 14.8665L7.31667 15.0748C7.56978 15.221 7.78002 15.4311 7.92628 15.6841C8.07255 15.9372 8.1497 16.2242 8.15 16.5165V16.6665C8.15 17.1085 8.3256 17.5325 8.63816 17.845C8.95072 18.1576 9.37464 18.3332 9.81667 18.3332H10.1833C10.6254 18.3332 11.0493 18.1576 11.3618 17.845C11.6744 17.5325 11.85 17.1085 11.85 16.6665V16.5165C11.8503 16.2242 11.9275 15.9372 12.0737 15.6841C12.22 15.4311 12.4302 15.221 12.6833 15.0748L13.0417 14.8665C13.295 14.7202 13.5824 14.6432 13.875 14.6432C14.1676 14.6432 14.455 14.7202 14.7083 14.8665L14.8333 14.9332C15.2158 15.1538 15.6701 15.2136 16.0967 15.0996C16.5232 14.9855 16.887 14.7069 17.1083 14.3248L17.2917 13.9998C17.5123 13.6174 17.5721 13.163 17.4581 12.7365C17.344 12.31 17.0654 11.9461 16.6833 11.7248L16.5583 11.6582C16.304 11.5113 16.093 11.2999 15.9466 11.0453C15.8003 10.7906 15.7238 10.5019 15.725 10.2082V9.7915C15.7238 9.49782 15.8003 9.20904 15.9466 8.95441C16.093 8.69978 16.304 8.48834 16.5583 8.3415L16.6833 8.2665C17.0654 8.04521 17.344 7.68137 17.4581 7.25484C17.5721 6.82831 17.5123 6.37395 17.2917 5.9915L17.1083 5.67484C16.887 5.29278 16.5232 5.01415 16.0967 4.90009C15.6701 4.78604 15.2158 4.84589 14.8333 5.0665L14.7083 5.13317C14.455 5.27945 14.1676 5.35646 13.875 5.35646C13.5824 5.35646 13.295 5.27945 13.0417 5.13317L12.6833 4.92484C12.4302 4.7787 12.22 4.56857 12.0737 4.31553C11.9275 4.0625 11.8503 3.77544 11.85 3.48317V3.33317C11.85 2.89114 11.6744 2.46722 11.3618 2.15466C11.0493 1.8421 10.6254 1.6665 10.1833 1.6665Z"/><path d="M10 12.4998C11.3807 12.4998 12.5 11.3805 12.5 9.99984C12.5 8.61913 11.3807 7.49984 10 7.49984C8.61929 7.49984 7.5 8.61913 7.5 9.99984C7.5 11.3805 8.61929 12.4998 10 12.4998Z"/></svg>;

    const items = [
      { id: "home",         label: "Home",             selected: true, icon: <IconHome /> },
      { id: "inbox",        label: "Inbox",            badge: 24,      icon: <IconInbox /> },
      { id: "calendar",     label: "Calendar",                         icon: <IconCalendar /> },
      { id: "listings",     label: "Listings",                         icon: <IconListings /> },
      { id: "marketing",    label: "Marketing & Sales",                icon: <IconMarketing /> },
      { id: "financials",   label: "Financials",                       icon: <IconFinancials /> },
      { id: "guestpay",     label: "Guest payments",                   icon: <IconGuestPay /> },
      { id: "accounting",   label: "Accounting",                       icon: <IconAccounting /> },
      { id: "integrations", label: "Integrations",                     icon: <IconIntegrations /> },
      { id: "settings",     label: "Settings",                         icon: <IconSettings /> },
    ];

    return (
      <nav className="home-sidebar" aria-label="Main navigation">
        <ul className="home-nav-list">
          {items.map(it => (
            <li key={it.id}>
              <a href="#" className={"home-nav-item" + (it.selected ? " is-selected" : "")} aria-current={it.selected ? "page" : undefined}>
                <span className="home-nav-icon">{it.icon}</span>
                <span className="home-nav-label">{it.label}</span>
                {it.badge !== undefined && <span className="home-nav-badge">{it.badge}</span>}
              </a>
            </li>
          ))}
        </ul>
      </nav>
    );
  }

  /* -------- Greeting banner -------- */
  function HomeGreeting({ firstName, importedCount }) {
    return (
      <div className="home-greeting">
        <div className="home-greeting-row">
          <button className="home-iconbtn home-iconbtn--inline" aria-label="Toggle side panel">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect x="3" y="3" width="18" height="18" rx="2"/><line x1="9" y1="3" x2="9" y2="21"/></svg>
          </button>
          <h1 className="home-greeting-title">Welcome to Guesty, {firstName}</h1>
          <button className="home-customize-btn">Customize</button>
        </div>
      </div>
    );
  }

  /* -------- Daily overview -------- */
  function DonutChart({ value, total, color }) {
    const pct = value / total;
    const r = 18;
    const c = 2 * Math.PI * r;
    const offset = c * (1 - pct);
    return (
      <svg width="48" height="48" viewBox="0 0 48 48" className="donut-chart" aria-hidden="true">
        <circle cx="24" cy="24" r={r} fill="none" stroke="hsl(var(--gst-border))" strokeWidth="5" />
        <circle cx="24" cy="24" r={r} fill="none" stroke={color} strokeWidth="5"
          strokeDasharray={c} strokeDashoffset={offset}
          strokeLinecap="round"
          transform="rotate(-90 24 24)" />
      </svg>
    );
  }

  function DailyOverviewSection() {
    const [period, setPeriod] = useState("Today");
    return (
      <section className="home-section">
        <header className="home-section-header home-section-header--row">
          <h2 className="home-section-title">Daily overview</h2>
          <div className="home-section-toggle">
            {["Today", "Tomorrow", "7 days"].map(p => (
              <button key={p}
                className={"home-toggle-btn" + (period === p ? " is-active" : "")}
                onClick={() => setPeriod(p)}>{p}</button>
            ))}
          </div>
        </header>
        <div className="daily-grid">
          {/* Checked in */}
          <div className="daily-card">
            <div className="daily-card-top">
              <div>
                <div className="daily-card-num">42/70</div>
                <div className="daily-card-label">Checked in</div>
              </div>
              <DonutChart value={42} total={70} color="hsl(var(--gst-primary))" />
            </div>
            <ul className="daily-alerts">
              <li><IconCreditCard /><span>9 awaiting payment</span><IconWarn /></li>
              <li><IconClipboard /><span>15 unassigned units</span></li>
              <li><IconClipboard /><span>15 unassigned units</span></li>
              <li className="daily-alerts-more">+ 12 more</li>
            </ul>
          </div>
          {/* Checked out */}
          <div className="daily-card">
            <div className="daily-card-top">
              <div>
                <div className="daily-card-num">42/70</div>
                <div className="daily-card-label">Checked out</div>
              </div>
              <DonutChart value={42} total={70} color="hsl(150 60% 45%)" />
            </div>
            <ul className="daily-alerts">
              <li><IconCreditCard /><span>9 awaiting payment</span><IconWarn /></li>
            </ul>
          </div>
          {/* Turnovers */}
          <div className="daily-card">
            <div className="daily-card-top">
              <div>
                <div className="daily-card-num">4</div>
                <div className="daily-card-label">Turnovers</div>
              </div>
            </div>
            <div className="daily-info-pill">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
              <span>Shortest gap: 5 hrs</span>
            </div>
          </div>
          {/* Staying */}
          <div className="daily-card">
            <div className="daily-card-top">
              <div>
                <div className="daily-card-num">144</div>
                <div className="daily-card-label">Staying</div>
              </div>
            </div>
            <ul className="daily-alerts">
              <li><IconCreditCard /><span>9 awaiting payment</span><IconWarn /></li>
            </ul>
          </div>
        </div>
      </section>
    );
  }

  // Small inline icons for the daily alert rows
  function IconCreditCard() {
    return <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="daily-alert-icon"><rect x="2" y="5" width="20" height="14" rx="2"/><line x1="2" y1="10" x2="22" y2="10"/></svg>;
  }
  function IconClipboard() {
    return <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="daily-alert-icon"><path d="M9 2h6a2 2 0 0 1 2 2v0a2 2 0 0 1-2 2H9a2 2 0 0 1-2-2v0a2 2 0 0 1 2-2z"/><rect x="4" y="4" width="16" height="18" rx="2"/></svg>;
  }
  function IconWarn() {
    return <svg width="14" height="14" viewBox="0 0 24 24" fill="hsl(var(--gst-warning))" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="daily-alert-warn" aria-label="Warning"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>;
  }

  /* -------- Trends overview -------- */
  function TrendsOverviewSection() {
    const [period, setPeriod] = useState("7 days");

    // Mock data per day — [checkins, checkouts, turnovers, occupancyPct]
    const days = [
      { label: "Aug 25", ci: 120, co: 165, tn: 85,  oc: 45 },
      { label: "Aug 26", ci: 350, co: 395, tn: 320, oc: 72 },
      { label: "Aug 27", ci: 215, co: 260, tn: 180, oc: 64 },
      { label: "Aug 28", ci: 270, co: 320, tn: 240, oc: 56 },
      { label: "Aug 29", ci: 120, co: 165, tn: 85,  oc: 40 },
      { label: "Aug 30", ci: 295, co: 345, tn: 260, oc: 60 },
      { label: "Aug 31", ci: 120, co: 165, tn: 85,  oc: 56 },
    ];

    // Chart geometry
    const W = 760, H = 260;
    const PAD_L = 36, PAD_R = 40, PAD_T = 12, PAD_B = 32;
    const innerW = W - PAD_L - PAD_R;
    const innerH = H - PAD_T - PAD_B;
    const groupW = innerW / days.length;
    const barW = 14;
    const barGap = 4;
    const groupBarsW = barW * 3 + barGap * 2;
    const maxY = 400;

    // Smooth curve through occupancy points (catmull-rom-ish via cubic bezier)
    const occPoints = days.map((d, i) => ({
      x: PAD_L + groupW * i + groupW / 2,
      y: PAD_T + innerH * (1 - d.oc / 100),
    }));
    const smoothPath = (pts) => {
      if (!pts.length) return "";
      let d = `M${pts[0].x},${pts[0].y}`;
      for (let i = 0; i < pts.length - 1; i++) {
        const p0 = pts[i - 1] || pts[i];
        const p1 = pts[i];
        const p2 = pts[i + 1];
        const p3 = pts[i + 2] || p2;
        const cp1x = p1.x + (p2.x - p0.x) / 6;
        const cp1y = p1.y + (p2.y - p0.y) / 6;
        const cp2x = p2.x - (p3.x - p1.x) / 6;
        const cp2y = p2.y - (p3.y - p1.y) / 6;
        d += ` C${cp1x.toFixed(1)},${cp1y.toFixed(1)} ${cp2x.toFixed(1)},${cp2y.toFixed(1)} ${p2.x},${p2.y}`;
      }
      return d;
    };
    const curveD = smoothPath(occPoints);
    const fillD = curveD + ` L${PAD_L + innerW},${PAD_T + innerH} L${PAD_L},${PAD_T + innerH} Z`;

    return (
      <section className="home-section">
        <header className="home-section-header home-section-header--row">
          <h2 className="home-section-title">Trends overview</h2>
          <div className="home-section-toggle">
            {["7 days", "30 days"].map(p => (
              <button key={p}
                className={"home-toggle-btn" + (period === p ? " is-active" : "")}
                onClick={() => setPeriod(p)}>{p}</button>
            ))}
          </div>
        </header>
        <div className="trends-summary">
          <span className="trends-metric">
            <span className="trends-metric-icon trends-metric-icon--ci">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round"><line x1="17" y1="7" x2="7" y2="17"/><polyline points="17 17 7 17 7 7"/></svg>
            </span>
            <strong>450</strong> Check-ins
          </span>
          <span className="trends-metric">
            <span className="trends-metric-icon trends-metric-icon--co">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round"><line x1="7" y1="17" x2="17" y2="7"/><polyline points="7 7 17 7 17 17"/></svg>
            </span>
            <strong>360</strong> Check-outs
          </span>
          <span className="trends-metric">
            <span className="trends-metric-icon trends-metric-icon--tn">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round"><polyline points="17 1 21 5 17 9"/><path d="M3 11V9a4 4 0 0 1 4-4h14"/><polyline points="7 23 3 19 7 15"/><path d="M21 13v2a4 4 0 0 1-4 4H3"/></svg>
            </span>
            <strong>32</strong> Turnovers
          </span>
          <span className="trends-metric">
            <span className="trends-metric-icon trends-metric-icon--oc">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round"><path d="M21.21 15.89A10 10 0 1 1 8 2.83"/><path d="M22 12A10 10 0 0 0 12 2v10z"/></svg>
            </span>
            <strong>95%</strong> Occupancy
          </span>
        </div>
        <div className="trends-chart-wrap">
          <svg className="trends-chart" viewBox={`0 0 ${W} ${H}`} preserveAspectRatio="none" aria-hidden="true">
            {/* Y-axis grid lines + labels (left = counts 0-400, right = % 0-100) */}
            {[0, 1, 2, 3, 4].map(i => {
              const y = PAD_T + innerH * (i / 4);
              const countLbl = maxY - (maxY * i / 4);
              const pctLbl = 100 - (100 * i / 4);
              return (
                <g key={i}>
                  <line x1={PAD_L} y1={y} x2={PAD_L + innerW} y2={y} stroke="hsl(var(--gst-border))" strokeWidth="1" strokeDasharray={i === 4 ? "0" : "0"} opacity={i === 4 ? "1" : "0.6"} />
                  <text x={PAD_L - 8} y={y + 4} fontSize="10.5" fill="hsl(var(--gst-muted-foreground))" textAnchor="end">{countLbl === 0 ? "0" : countLbl}</text>
                  <text x={PAD_L + innerW + 8} y={y + 4} fontSize="10.5" fill="hsl(var(--gst-muted-foreground))" textAnchor="start">{pctLbl === 0 ? "0" : pctLbl + "%"}</text>
                </g>
              );
            })}
            {/* Occupancy area + curve */}
            <path d={fillD} fill="#E0D1B6" opacity="0.2" />
            <path d={curveD} stroke="hsl(40 50% 60%)" strokeWidth="2" fill="none" strokeLinecap="round" strokeLinejoin="round" />
            {/* Grouped bars */}
            {days.map((d, i) => {
              const cx = PAD_L + groupW * i + groupW / 2;
              const groupX = cx - groupBarsW / 2;
              const bars = [
                { v: d.ci, color: "hsl(220 90% 78%)", x: groupX },
                { v: d.co, color: "hsl(150 50% 55%)", x: groupX + barW + barGap },
                { v: d.tn, color: "hsl(8 80% 70%)",   x: groupX + (barW + barGap) * 2 },
              ];
              return (
                <g key={i}>
                  {bars.map((b, j) => {
                    const h = innerH * (b.v / maxY);
                    return (
                      <rect key={j}
                        x={b.x} y={PAD_T + innerH - h}
                        width={barW} height={h}
                        rx="3"
                        fill={b.color} />
                    );
                  })}
                  <text x={cx} y={H - 8}
                    fontSize="11"
                    fill={i === 0 ? "hsl(var(--gst-primary))" : "hsl(var(--gst-muted-foreground))"}
                    fontWeight={i === 0 ? "600" : "500"}
                    textAnchor="middle">{d.label}</text>
                </g>
              );
            })}
          </svg>
        </div>
      </section>
    );
  }

  /* -------- Revenue -------- */
  function RevenueSection() {
    const [metric, setMetric] = useState("total");

    // Two line series — current (blue, solid) and previous (green, dashed)
    const months = ["Aug 1", "Aug 7", "Aug 13", "Aug 19", "Aug 25", "Aug 31"];
    const current  = [5000, 7600, 5800, 2200, 5400, 5200];
    const previous = [3000, 5000, 4400, 3600, 3800, 3600];

    const W = 760, H = 260;
    const PAD_L = 40, PAD_R = 16, PAD_T = 16, PAD_B = 32;
    const innerW = W - PAD_L - PAD_R;
    const innerH = H - PAD_T - PAD_B;
    const maxY = 8000;
    const stepX = innerW / (current.length - 1);

    const ptsToCmd = (vals) => {
      const pts = vals.map((v, i) => ({
        x: PAD_L + stepX * i,
        y: PAD_T + innerH * (1 - v / maxY),
      }));
      let d = `M${pts[0].x},${pts[0].y}`;
      for (let i = 0; i < pts.length - 1; i++) {
        const p0 = pts[i - 1] || pts[i];
        const p1 = pts[i];
        const p2 = pts[i + 1];
        const p3 = pts[i + 2] || p2;
        const cp1x = p1.x + (p2.x - p0.x) / 6;
        const cp1y = p1.y + (p2.y - p0.y) / 6;
        const cp2x = p2.x - (p3.x - p1.x) / 6;
        const cp2y = p2.y - (p3.y - p1.y) / 6;
        d += ` C${cp1x.toFixed(1)},${cp1y.toFixed(1)} ${cp2x.toFixed(1)},${cp2y.toFixed(1)} ${p2.x},${p2.y}`;
      }
      return d;
    };

    return (
      <section className="home-section">
        <header className="home-section-header home-section-header--row">
          <h2 className="home-section-title">Revenue</h2>
          <div className="month-picker">
            <button className="month-picker-arrow" aria-label="Previous month">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round"><polyline points="15 18 9 12 15 6"/></svg>
            </button>
            <span className="month-picker-label">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
              August 2025
            </span>
            <button className="month-picker-arrow" aria-label="Next month">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round"><polyline points="9 18 15 12 9 6"/></svg>
            </button>
          </div>
        </header>
        <div className="revenue-metrics">
          <button className={"revenue-metric-card" + (metric === "total" ? " is-active" : "")} onClick={() => setMetric("total")}>
            <span className={"revenue-radio" + (metric === "total" ? " is-active" : "")}>
              {metric === "total" && <span className="revenue-radio-dot"></span>}
            </span>
            <span className="revenue-metric-text">
              <span className="revenue-metric-label">Total revenue</span>
              <span className="revenue-metric-value">$72,775</span>
            </span>
          </button>
          <button className={"revenue-metric-card" + (metric === "adr" ? " is-active" : "")} onClick={() => setMetric("adr")}>
            <span className={"revenue-radio" + (metric === "adr" ? " is-active" : "")}>
              {metric === "adr" && <span className="revenue-radio-dot"></span>}
            </span>
            <span className="revenue-metric-text">
              <span className="revenue-metric-label">Average daily rate</span>
              <span className="revenue-metric-value">$145</span>
            </span>
          </button>
        </div>
        <div className="revenue-chart-wrap">
          <svg className="revenue-chart" viewBox={`0 0 ${W} ${H}`} preserveAspectRatio="none" aria-hidden="true">
            {/* Y-axis grid + labels */}
            {[0, 2000, 4000, 6000, 8000].map(v => {
              const y = PAD_T + innerH * (1 - v / maxY);
              return (
                <g key={v}>
                  <line x1={PAD_L} y1={y} x2={W - PAD_R} y2={y} stroke="hsl(var(--gst-border))" strokeWidth="1" opacity="0.5" />
                  <text x={PAD_L - 8} y={y + 4} fontSize="10.5" fill="hsl(var(--gst-muted-foreground))" textAnchor="end">{(v / 1000) + "K"}</text>
                </g>
              );
            })}
            {/* Previous (dashed green) */}
            <path d={ptsToCmd(previous)} stroke="hsl(150 45% 50%)" strokeWidth="2" fill="none" strokeDasharray="6 5" strokeLinecap="round" strokeLinejoin="round" />
            {/* Current (solid blue) */}
            <path d={ptsToCmd(current)} stroke="hsl(220 85% 72%)" strokeWidth="2.4" fill="none" strokeLinecap="round" strokeLinejoin="round" />
            {/* X-axis labels */}
            {months.map((m, i) => (
              <text key={m} x={PAD_L + stepX * i} y={H - 8}
                fontSize="11"
                fill="hsl(var(--gst-muted-foreground))"
                textAnchor="middle">{m}</text>
            ))}
          </svg>
        </div>
        <div className="revenue-legend">
          <span><span className="revenue-legend-dot revenue-legend-dot--current"></span>Current period</span>
          <span><span className="revenue-legend-dot revenue-legend-dot--previous"></span>Previous period</span>
        </div>
        <div className="revenue-compare">
          <label className="revenue-compare-label">Compare to</label>
          <div className="revenue-compare-select">
            2022 (same month)
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polyline points="6 9 12 15 18 9"/></svg>
          </div>
        </div>
      </section>
    );
  }

  /* -------- Next onboarding call card -------- */
  function NextCallSection({ csmName }) {
    const [timeLeft, setTimeLeft] = useState(() => CALL_TIME - Date.now());
    useEffect(() => {
      const id = setInterval(() => setTimeLeft(CALL_TIME - Date.now()), 1000);
      return () => clearInterval(id);
    }, []);

    const totalSecs = Math.max(0, Math.floor(timeLeft / 1000));
    const days  = Math.floor(totalSecs / 86400);
    const hrs   = Math.floor((totalSecs % 86400) / 3600);
    const mins  = Math.floor((totalSecs % 3600) / 60);
    const secs  = totalSecs % 60;
    const pad   = (n) => String(n).padStart(2, "0");
    const isPast = timeLeft <= 0;

    return (
      <section className="home-section home-section--call">
        <header className="home-section-header">
          <h2 className="home-section-title">Your next onboarding call</h2>
        </header>
        <div className="next-call-card">
          <div className="next-call-date">
            <span className="next-call-month">JUN</span>
            <span className="next-call-day">18</span>
            <span className="next-call-weekday">Thursday</span>
          </div>
          <div className="next-call-body">
            <div className="next-call-title">
              <SkeletonImg
                src="assets/amanda-avatar.png"
                alt={csmName}
                className="next-call-host-photo"
                wrapStyle={{ display: "inline-block", width: 32, height: 32, borderRadius: "50%", overflow: "hidden", lineHeight: 0, flexShrink: 0 }}
              />
              Call 1 with {csmName}
              <span className="next-call-title-sep" aria-hidden="true">·</span>
              <div className="next-call-meta">
                <span className="next-call-meta-item">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
                  11:00 AM PT · 45 min
                </span>
              </div>
            </div>
          </div>
          {/* Countdown — own grid row so it aligns with the date card's center */}
          <div className="next-call-countdown" aria-live="polite" aria-label="Time until call">
            {isPast ? (
              <span className="next-call-countdown-live">Your call is starting now</span>
            ) : (
              <>
                <div className="next-call-countdown-units">
                  {days > 0 && (
                    <div className="countdown-unit">
                      <span className="countdown-num">{days}</span>
                      <span className="countdown-lbl">day{days !== 1 ? "s" : ""}</span>
                    </div>
                  )}
                  <div className="countdown-unit">
                    <span className="countdown-num">{pad(hrs)}</span>
                    <span className="countdown-lbl">hr</span>
                  </div>
                  <div className="countdown-unit">
                    <span className="countdown-num">{pad(mins)}</span>
                    <span className="countdown-lbl">min</span>
                  </div>
                  <div className="countdown-unit">
                    <span className="countdown-num">{pad(secs)}</span>
                    <span className="countdown-lbl">sec</span>
                  </div>
                </div>
              </>
            )}
          </div>
          <div className="next-call-actions">
            <button className="home-btn home-btn--primary">
              Add to calendar
            </button>
            <button className="home-btn home-btn--ghost">Reschedule</button>
          </div>
        </div>
      </section>
    );
  }

  /* -------- Homepage question carousel (§8 data model) -------- */
  // Seeds the "answer at your own pace" carousel with the 4 questions removed
  // from the mandatory wizard. Adding a future question = append an object here.
  const HOME_QUESTIONS = [
    {
      id: "damage_protection",
      eyebrow: "Damage protection",
      title: "How do you handle damage protection?",
      hint: "Sets your deposit and claims defaults.",
      type: "single",                       // 'single' | 'form'
      options: [
        { k: "deposit",   label: "Security deposit" },
        { k: "waiver",    label: "Damage waiver fee" },
        { k: "insurance", label: "Third-party insurance" },
        { k: "none",      label: "I don't collect anything yet" },
      ],
      summary: (v, opts) => opts.find(o => o.k === v)?.label,   // Answered one-liner
    },
    {
      id: "business_profile",
      eyebrow: "Business profile",
      title: "Tell us about your business",
      type: "form",
      fields: [
        { k: "business_name",  label: "Business name",  input: "text",  placeholder: "e.g. Northshore Stays",
          helper: "Shown on your booking site and booking-related emails." },
        { k: "business_email", label: "Business email", input: "email", placeholder: "you@yourbusiness.com",
          helper: "For booking confirmations and guest messages from direct bookings." },
        { k: "domain",         label: "Domain",         input: "text",  placeholder: "e.g. book.northshorestays.com",
          helper: "Used for your booking engine or guest-facing links." },
      ],
      summary: (v) => v?.business_name,
    },
    {
      id: "terms",
      eyebrow: "Booking website",
      title: "Set your booking-site terms & conditions",
      type: "single",
      options: [
        { k: "default", label: "Use Guesty's default" },   // may link to a preview
        { k: "upload",  label: "Upload my own" },           // reveals file picker
      ],
      summary: (v, opts) => opts.find(o => o.k === v)?.label,
    },
    {
      id: "cookie",
      eyebrow: "Booking website",
      title: "Set your cookie policy",
      type: "single",
      options: [
        { k: "default", label: "Use Guesty's default" },   // may link to a preview
        { k: "upload",  label: "Upload my own" },           // reveals file picker
      ],
      summary: (v, opts) => opts.find(o => o.k === v)?.label,
    },
  ];

  /* -------- Homepage question carousel (§3–§9) -------- */
  function QuestionCarouselSection({ answers, set }) {
    const total = HOME_QUESTIONS.length;

    // Transient UI state — never persisted to `answers` (§7).
    const [cardIndex, setCardIndex] = useState(0);
    const [expanded, setExpanded] = useState(false);
    const [draft, setDraft] = useState(null);        // in-progress answer: string (single) | object (form)
    const [uploadName, setUploadName] = useState(""); // chosen file label for the "upload" option

    // Keyboard: ArrowRight / Down advance (looping); ArrowLeft / Up go back.
    // Disabled while a card is expanded to protect unsaved input.
    // Hook must live before any early return (React rules).
    useEffect(() => {
      if (total === 0) return;
      const handler = (e) => {
        const tag = document.activeElement?.tagName;
        if (tag === "INPUT" || tag === "TEXTAREA" || tag === "SELECT") return;
        if (e.key === "ArrowRight" || e.key === "ArrowDown") {
          e.preventDefault();
          if (!expanded) setCardIndex((i) => (i + 1) % total);
        } else if (e.key === "ArrowLeft" || e.key === "ArrowUp") {
          e.preventDefault();
          if (!expanded) setCardIndex((i) => Math.max(0, i - 1));
        }
      };
      window.addEventListener("keydown", handler);
      return () => window.removeEventListener("keydown", handler);
    }, [expanded, total]);

    // §9: with zero questions the section does not render at all.
    if (total === 0) return null;

    const saved = answers.home_q || {};
    const hasAnswer = (id) => {
      const v = saved[id];
      return v !== undefined && v !== null && v !== "";
    };
    const answeredCount = HOME_QUESTIONS.filter((q) => hasAnswer(q.id)).length;
    const allAnswered = answeredCount === total;

    const q = HOME_QUESTIONS[cardIndex];
    const savedValue = saved[q.id];
    const isAnswered = hasAnswer(q.id);

    const goNext = () => { if (!expanded) setCardIndex((i) => (i + 1) % total); };

    const openEditor = () => {
      setDraft(q.type === "form" ? { ...(savedValue || {}) } : (savedValue ?? null));
      setUploadName("");
      setExpanded(true);
    };
    const cancel = () => { setExpanded(false); setDraft(null); setUploadName(""); };
    const save = () => {
      // set() shallow-merges at the top level, so spread the sub-object ourselves (§7).
      set("home_q", { ...saved, [q.id]: draft });
      setExpanded(false);
      setDraft(null);
      setUploadName("");
    };

    // Keep Answered summaries non-empty by gating Save on a meaningful value.
    const canSave = q.type === "form"
      ? !!(draft && String(draft.business_name || "").trim())
      : (draft !== null && draft !== undefined && draft !== "");

    const summaryText = isAnswered
      ? (q.type === "form" ? q.summary(savedValue) : q.summary(savedValue, q.options))
      : "";

    return (
      <section className="home-section">
        <header className="home-section-header home-section-header--row">
          <h2 className="home-section-title">Set up at your own pace</h2>
          <span className={"qcarousel-progress" + (allAnswered ? " qcarousel-progress--done" : "")}>
            {allAnswered ? "You're all set ✓" : `${answeredCount} of ${total} answered`}
          </span>
        </header>

        <div className="qcarousel-body">
          <div className={"qcarousel-card" + (expanded ? " qcarousel-card--expanded" : "")}>
            {/* Column: all textual / interactive content */}
            <div className="qcarousel-card-inner">
              <div className={"qcarousel-eyebrow" + (isAnswered ? " qcarousel-eyebrow--answered" : "")}>
                <span>{q.eyebrow}</span>
                {isAnswered && (
                  <span className="qcarousel-answered-tag">
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                      <polyline points="20 6 9 17 4 12"></polyline>
                    </svg>
                    Answered
                  </span>
                )}
              </div>

              <h3 className="qcarousel-title">{q.title}</h3>

              {/* Collapsed + answered → one-line summary */}
              {isAnswered && !expanded && summaryText && (
                <p className="qcarousel-summary">{summaryText}</p>
              )}
              {/* Collapsed + unanswered → hint */}
              {!isAnswered && !expanded && q.hint && (
                <p className="qcarousel-hint">{q.hint}</p>
              )}

              {/* Expanded → answer controls + Save/Cancel */}
              {expanded && (
                <div className="qcarousel-controls">
                  {q.type === "single" && (
                    <div className="opt-list">
                      {q.options.map((opt, i) => (
                        <Option
                          key={opt.k}
                          k={i + 1}
                          label={opt.label}
                          selected={draft === opt.k}
                          onSelect={() => { setDraft(opt.k); setUploadName(""); }}
                        />
                      ))}
                      {draft === "upload" && (
                        <label className="qcarousel-upload">
                          <span className="qcarousel-upload-label">Upload your policy file</span>
                          <input
                            type="file"
                            accept=".pdf,.html,.txt"
                            onChange={(e) => setUploadName(e.target.files && e.target.files[0] ? e.target.files[0].name : "")}
                          />
                          {uploadName && <span className="qcarousel-upload-name">{uploadName}</span>}
                        </label>
                      )}
                      {draft === "default" && (
                        <a
                          href="#"
                          className="qcarousel-preview-link"
                          onClick={(e) => e.preventDefault()}
                        >
                          Preview Guesty's default
                        </a>
                      )}
                    </div>
                  )}

                  {q.type === "form" && (
                    <div className="qcarousel-form">
                      {q.fields.map((f) => (
                        <div className="qcarousel-field" key={f.k}>
                          <label htmlFor={"qc-" + q.id + "-" + f.k}>{f.label}</label>
                          <input
                            id={"qc-" + q.id + "-" + f.k}
                            type={f.input || "text"}
                            placeholder={f.placeholder}
                            value={(draft && draft[f.k]) || ""}
                            onChange={(e) => {
                              const val = e.target.value;
                              setDraft((d) => ({ ...(d || {}), [f.k]: val }));
                            }}
                          />
                          {f.helper && <span className="qcarousel-field-helper">{f.helper}</span>}
                        </div>
                      ))}
                    </div>
                  )}

                  <div className="qcarousel-edit-actions">
                    <button type="button" className="home-btn home-btn--primary" disabled={!canSave} onClick={save}>Save</button>
                    <button type="button" className="home-btn home-btn--ghost" onClick={cancel}>Cancel</button>
                  </div>
                </div>
              )}

              {/* Collapsed → CTA + position dots */}
              {!expanded && (
                <div className="qcarousel-cta-row">
                  {isAnswered ? (
                    <button type="button" className="qcarousel-cta qcarousel-cta--edit" onClick={openEditor}>Edit</button>
                  ) : (
                    <button type="button" className="qcarousel-cta" onClick={openEditor}>Answer</button>
                  )}
                  <div className="qcarousel-dots" aria-hidden="true">
                    {HOME_QUESTIONS.map((item, i) => (
                      <span
                        key={item.id}
                        className={"qcarousel-dot" + (i === cardIndex ? " qcarousel-dot--active" : "")}
                      />
                    ))}
                  </div>
                </div>
              )}
            </div>

            {/* Next button — loops back to the first card after the last */}
            <button
              type="button"
              className="btn btn-secondary qcarousel-next-btn"
              disabled={expanded}
              onClick={goNext}
              aria-label="Next question"
            >
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                <polyline points="9 18 15 12 9 6"/>
              </svg>
            </button>
          </div>{/* .qcarousel-card */}
        </div>{/* .qcarousel-body */}
      </section>
    );
  }

  /* -------- Topics for Call 1 -------- */
  // Academy landing per onboarding section — used for questions flagged for review.
  const SECTION_ACADEMY = {
    "Pre-flight":   ACADEMY_BASE + "getting-started",
    "Operations":   ACADEMY_BASE + "operations-cleaners",
    "Financials":   ACADEMY_BASE + "accounting",
    "Governance":   ACADEMY_BASE + "team-management",
    "Focus topics": ACADEMY_BASE,
    "Business":     ACADEMY_BASE + "business-setup",
  };

  function TopicsSection({ topics, flagged = [] }) {
    return (
      <section className="home-section">
        <header className="home-section-header">
          <h2 className="home-section-title">Topics for Call 1</h2>
          <p className="home-section-sub">{CSM_NAME} will lead with these on Thursday. Get a head start by reading up before the call.</p>
        </header>
        <ul className="topics-list">
          {topics.map((topic, i) => {
            const meta = TOPIC_META[topic] || { desc: "", url: ACADEMY_BASE };
            return (
              <li key={topic} className="topic-row">
                <div className="topic-num">{i + 1}</div>
                <div className="topic-body">
                  <div className="topic-name">{topic}</div>
                  <div className="topic-desc">{meta.desc}</div>
                </div>
                <a
                  href={meta.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="topic-cta"
                  aria-label={`Learn about ${topic} in the Guesty Academy (opens in new tab)`}
                >
                  Learn in Academy
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="7" y1="17" x2="17" y2="7"/><polyline points="7 7 17 7 17 17"/></svg>
                </a>
              </li>
            );
          })}
          {flagged.map((item, i) => {
            const url = SECTION_ACADEMY[item.sectionName] || ACADEMY_BASE;
            return (
              <li key={"flag-" + item.id} className="topic-row topic-row--flagged">
                <div className="topic-num">{topics.length + i + 1}</div>
                <div className="topic-body">
                  <div className="topic-name">
                    {item.title}
                    <span className="gst-badge gst-badge--info flag-review-status">Needs review</span>
                  </div>
                  <div className="topic-desc">You flagged this to review with {CSM_NAME} on Call 1.</div>
                </div>
                <a
                  href={url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="topic-cta"
                  aria-label={`Learn about ${item.title} in the Guesty Academy (opens in new tab)`}
                >
                  Learn in Academy
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="7" y1="17" x2="17" y2="7"/><polyline points="7 7 17 7 17 17"/></svg>
                </a>
              </li>
            );
          })}
        </ul>
      </section>
    );
  }

  /* -------- Daily overview -------- */
  /* (legacy daily/trends/revenue and recap/resources widgets removed in 2026-05-28 Figma rebuild) */



  const PUNCH_LABELS = {
    "Q7.1": ["Upload brand logo", "Brand"],
    "Q1.1": ["Confirm listing count", "Portfolio & Channels"],
    "Q2.onboard_more": ["Onboarding more listings", "Portfolio & Channels"],
    "Q1.2": ["Confirm channels", "Portfolio & Channels"],
    "Q1.4": ["Connect Airbnb account", "Portfolio & Channels"],
    "Q1.5": ["Confirm going-live timeline", "Portfolio & Channels"],
    "Q2.1": ["Confirm cleaning setup", "Operations"],
    "Q2.4": ["Upload turnover checklist", "Operations"],
    "Q2.timing": ["Cleaning schedule timing", "Operations"],
    "Q2.inspections": ["Professional inspections", "Operations"],
    "Q3.1": ["Pick revenue recognition method", "Financials"],
    "Q3.2": ["Decide on non-refundable rates", "Financials"],
    "Q3.4": ["Pick payment timing", "Financials"],
    "Q3.6": ["Add mandatory fees", "Financials"],
    "Q3.7": ["Configure taxes", "Financials"],
    "Q5.owners_gate": ["Owner relationship", "Owners"],
    "Q7.2": ["Upload owner records", "Owners"],
    "Q5.owner_split": ["Owner revenue split", "Owners"],
    "Q6.pricing_tool": ["Pricing tool", "Rate strategy"],
    "Q7.3": ["Season date windows", "Rate strategy"],
    "Q5.1": ["Confirm decision owners", "Governance"],
    "Q5.2": ["Invite teammates", "Governance"],
    "Q6.1": ["Pick Call 1 focus topics", "Focus & context"],
    "Q6.2": ["Share biggest pain", "Focus & context"],
  };
  function punchLabel(id) {return (PUNCH_LABELS[id] || [id])[0];}
  function punchSection(id) {return (PUNCH_LABELS[id] || ["", "—"])[1];}

  /* ============ Mount ============ */
  const root = ReactDOM.createRoot(document.getElementById("root"));
  root.render(<App />);

})();