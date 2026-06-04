// screens.jsx — all question screens (v2 Atlas-aligned copy)
// Wrapped in IIFE so its top-level const declarations don't collide with wizard.jsx
(function() {

const { useState, useEffect, useMemo, useRef } = React;

/* ===================== Mock data ===================== */

const SF_PREFILL = {
  business_name: "Mountain Retreats LLC",
  contact_email: "maya@mountainretreats.co",
  first_name: "Maya",
  listing_count: 8,
  channels: ["airbnb", "booking"],
  domain_hint: "mountainretreats.co",
  partner_cleaning: "Turno",
  partner_pricing: null,
  // Channel-prefill patch (2026-05-27) — provenance for chip attribution
  source_call_date: "2026-05-21", // 7 days before today's mock — "fresh" attribution
  other_channel_names: [],
};

const CSM_NAME = "Amanda";

// Expanded listing data — city, unit type, status, ownership, nickname, propertyType, address
const MOCK_LISTINGS = [
  { id: 1, name: "Aspen Loft — Downtown",      nickname: "ASP-01", propertyType: "Apartment", address: "412 E Hyman Ave, Aspen, CO", city: "Aspen",     unitType: "Single Unit", status: "Listed",   hostRole: "owner",   beds: 2, channel: "airbnb",  img: "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=400&h=300&fit=crop" },
  { id: 2, name: "Pine View Cabin",            nickname: "PINE",   propertyType: "Cabin",     address: "88 Pinecrest Rd, Aspen, CO",  city: "Aspen",     unitType: "Single Unit", status: "Listed",   hostRole: "owner",   beds: 3, channel: "airbnb",  img: "https://images.unsplash.com/photo-1518780664697-55e3ad937233?w=400&h=300&fit=crop" },
  { id: 3, name: "Studio on Main",             nickname: "MAIN-S", propertyType: "Studio",    address: "201 Main St, Aspen, CO",       city: "Aspen",     unitType: "Single Unit", status: "Listed",   hostRole: "owner",   beds: 1, channel: "airbnb",  img: "https://images.unsplash.com/photo-1493809842364-78817add7ffb?w=400&h=300&fit=crop" },
  { id: 4, name: "Riverside Retreat",          nickname: "RVR",    propertyType: "House",     address: "9 Roaring Fork, Aspen, CO",    city: "Aspen",     unitType: "Single Unit", status: "Listed",   hostRole: "co-host", beds: 4, channel: "airbnb",  img: "https://images.unsplash.com/photo-1568605114967-8130f3a36994?w=400&h=300&fit=crop" },
  { id: 5, name: "Snowmass Chalet",            nickname: "SNW",    propertyType: "Chalet",    address: "32 Wood Rd, Snowmass, CO",     city: "Snowmass",  unitType: "Multi Unit",  status: "Listed",   hostRole: "owner",   beds: 5, channel: "booking", img: "https://images.unsplash.com/photo-1449158743715-0a90ebb6d2d8?w=400&h=300&fit=crop" },
  { id: 6, name: "Maple Hollow A-Frame",       nickname: "MPL",    propertyType: "House",     address: "14 Maple Hollow, Aspen, CO",   city: "Aspen",     unitType: "Single Unit", status: "Listed",   hostRole: "owner",   beds: 2, channel: "airbnb",  img: "https://images.unsplash.com/photo-1505691938895-1758d7feb511?w=400&h=300&fit=crop" },
  { id: 7, name: "Birch & Oak Cottage",        nickname: "BIRCH",  propertyType: "Cottage",   address: "76 Birch Ln, Snowmass, CO",    city: "Snowmass",  unitType: "Single Unit", status: "Unlisted", hostRole: "owner",   beds: 2, channel: "airbnb",  img: "https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=400&h=300&fit=crop" },
  { id: 8, name: "Trail's End Townhouse",      nickname: "TRL",    propertyType: "Townhouse", address: "5 Trail's End, Aspen, CO",     city: "Aspen",     unitType: "Single Unit", status: "Listed",   hostRole: "owner",   beds: 3, channel: "airbnb",  img: "https://images.unsplash.com/photo-1480074568708-e7b720bb3f09?w=400&h=300&fit=crop" },
];

window.MOCK_LISTINGS = MOCK_LISTINGS;
// Merge real session context (from bootstrap.js → backend) over hardcoded
// defaults so the prototype still runs offline with the Mountain Retreats mock.
var __obSession = window.__OB_SESSION || {};
window.SF_PREFILL = Object.assign({}, SF_PREFILL, __obSession.sf_prefill || {});
window.CSM_NAME = __obSession.csm_name || CSM_NAME;
window.OB_CONTEXT = __obSession.ob_context || window.OB_CONTEXT || null;

/* ---- SkeletonImg — shimmer placeholder while a local asset loads ---- */
function SkeletonImg({ src, alt, className, style, wrapStyle, onLoad: onLoadProp, ...rest }) {
  const [loaded, setLoaded] = useState(false);
  const handleLoad  = (e) => { setLoaded(true); onLoadProp && onLoadProp(e); };
  const handleError = ()  => setLoaded(true);
  // Separate any caller-supplied opacity so we can animate 0 → target
  const { opacity: targetOpacity = 1, ...imgStyle } = style || {};
  return (
    <span className="skel-wrap" style={wrapStyle}>
      {!loaded && <span className="skel-shimmer" aria-hidden="true" />}
      <img
        src={src}
        alt={alt}
        className={className}
        style={{ ...imgStyle, opacity: loaded ? targetOpacity : 0 }}
        onLoad={handleLoad}
        onError={handleError}
        {...rest}
      />
    </span>
  );
}
window.SkeletonImg = SkeletonImg;

/* ===================== Small UI atoms ===================== */

function BotAlert({ children }) {
  const avatarRef = useRef(null);
  const shimmerRef = useRef(null);
  const bodyRef = useRef(null);

  useEffect(function() {
    // --- Avatar load via direct DOM (no state → no re-render) ---
    var img = new Image();
    img.onload = function() {
      if (avatarRef.current) avatarRef.current.style.backgroundImage = "url(assets/amanda-avatar.png)";
      if (shimmerRef.current) shimmerRef.current.style.display = "none";
    };
    img.onerror = function() {
      if (shimmerRef.current) shimmerRef.current.style.display = "none";
    };
    img.src = "assets/amanda-avatar.png";

    // --- Typewriter via direct DOM (no state → no re-render fight) ---
    if (!bodyRef.current) return;
    var divs = Array.from(bodyRef.current.querySelectorAll("div:not(.bot-name)"));
    var texts = divs.map(function(d) { return d.textContent || ""; });
    // Lock height before clearing so the bot-name row never shifts position
    divs.forEach(function(d) {
      d.style.minHeight = d.getBoundingClientRect().height + "px";
      d.textContent = "";
    });

    var reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (reducedMotion) {
      divs.forEach(function(d, i) { d.textContent = texts[i]; });
      return;
    }

    var SPEED = 22;
    var timers = [];
    var startDelay = 0;

    texts.forEach(function(text, lineIdx) {
      if (!text) return;
      var myDelay = startDelay;
      startDelay += text.length * SPEED + 150;
      var charCount = 0;
      var t = setTimeout(function() {
        var iv = setInterval(function() {
          charCount++;
          if (divs[lineIdx]) divs[lineIdx].textContent = text.slice(0, charCount);
          if (charCount >= text.length) clearInterval(iv);
        }, SPEED);
        timers.push(iv);
      }, myDelay);
      timers.push(t);
    });

    return function() { timers.forEach(function(id) { clearTimeout(id); clearInterval(id); }); };
  }, []);

  return (
    <div className="bot-alert">
      <div
        ref={avatarRef}
        className="bot-avatar"
        style={{
          backgroundSize: "cover",
          backgroundPosition: "center",
          position: "relative",
          overflow: "hidden",
        }}
      >
        <span ref={shimmerRef} className="skel-shimmer" aria-hidden="true" />
      </div>
      <div className="bot-body" ref={bodyRef}>
        <div className="bot-name">{CSM_NAME} · Onboarding specialist</div>
        {children}
      </div>
    </div>
  );
}

function InlineBot({ children }) {
  return (
    <div style={{
      fontSize: 14, fontStyle: "italic",
      color: "hsl(var(--gst-muted-foreground))",
      marginTop: -8,
      paddingLeft: 12,
      borderLeft: "2px solid hsl(var(--gst-border))",
    }}>{children}</div>
  );
}

function SourceChip({ label }) {
  return (
    <span className="source-chip">
      <span className="dot"></span>
      {label}
    </span>
  );
}

/* ===================== NormalizeField — free-text + AI interpretation ===================== */
// Controlled textarea that, on blur, POSTs the text to /api/normalize and shows
// how the onboarding assistant understood it (matched focus topics + a short
// echo). The structured result is persisted into `answers` so it lands on the
// Call 1 punch list. Degrades gracefully: if the endpoint is unavailable the
// raw text is still captured via `set(textKey, ...)`.
function NormalizeField({ answers, set, textKey, resultKey, field, placeholder, maxChars = 280 }) {
  const text = answers[textKey] ?? "";
  const stored = answers[resultKey] ?? null;
  const [busy, setBusy] = useState(false);
  // Track the text we last normalized so we don't refire for an unchanged value.
  const lastSent = useRef(stored ? stored.__text : null);
  const remaining = maxChars - text.length;

  // Debounced normalize: a short pause after the manager stops typing sends the
  // text to /api/normalize. Avoids per-keystroke calls and the stale-closure
  // pitfalls of an onBlur handler.
  useEffect(() => {
    const trimmed = text.trim();
    if (trimmed.length < 8 || trimmed === lastSent.current) return;
    const handle = setTimeout(() => {
      lastSent.current = trimmed;
      setBusy(true);
      fetch("/api/normalize", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ field, text: trimmed }),
      })
        .then((r) => (r.ok ? r.json() : null))
        .then((data) => {
          const result = data && data.result;
          if (result) set(resultKey, { ...result, __text: trimmed });
        })
        .catch(() => {})
        .finally(() => setBusy(false));
    }, 900);
    return () => clearTimeout(handle);
  }, [text]);

  return (
    <>
      <textarea
        className="input"
        placeholder={placeholder}
        value={text}
        onChange={(e) => set(textKey, e.target.value)}
      />
      <div style={{ fontSize: 11, color: remaining < 0 ? "hsl(var(--gst-warning))" : "hsl(var(--gst-muted-foreground))", textAlign: "right", marginTop: -12 }}>
        {busy ? "Reading your answer…" : remaining < 0 ? `Try to keep it under ${maxChars} characters — your CSM will dig in on the call.` : `${remaining} characters left`}
      </div>
      {stored && (stored.summary || (stored.matched_options || []).length) && (
        <div style={{
          marginTop: 4, padding: "12px 14px", borderRadius: 10,
          background: "hsl(var(--gst-primary) / 0.05)",
          border: "1px solid hsl(var(--gst-primary) / 0.18)",
        }}>
          <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: stored.summary ? 6 : 0 }}>
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="hsl(var(--gst-primary))" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M12 2l2.4 7.4H22l-6 4.5 2.3 7.1-6.3-4.6L5.7 21l2.3-7.1-6-4.5h7.6z" />
            </svg>
            <span style={{ fontSize: 12, fontWeight: 700, color: "hsl(var(--gst-primary))", letterSpacing: "0.01em" }}>
              Here's what I noted for your CSM
            </span>
          </div>
          {stored.summary && (
            <div style={{ fontSize: 13.5, color: "hsl(var(--gst-foreground))", lineHeight: 1.45 }}>{stored.summary}</div>
          )}
          {!!(stored.matched_options || []).length && (
            <div style={{ display: "flex", flexWrap: "wrap", gap: 6, marginTop: 8 }}>
              {stored.matched_options.map((opt) => (
                <span key={opt} style={{
                  fontSize: 12, fontWeight: 600, padding: "3px 10px", borderRadius: 999,
                  background: "hsl(var(--gst-primary) / 0.1)", color: "hsl(var(--gst-primary))",
                }}>{opt}</span>
              ))}
            </div>
          )}
          {stored.needs_confirmation && (
            <div style={{ fontSize: 12, color: "hsl(var(--gst-warning))", marginTop: 8, fontWeight: 500 }}>
              I'll flag this for {(window.OB_CONTEXT && window.OB_CONTEXT.specialist) || "your CSM"} to confirm the exact numbers on Call 1.
            </div>
          )}
        </div>
      )}
    </>
  );
}

/* ===================== QMeta context (dynamic visible index) ===================== */
const QMetaContext = React.createContext(null);
window.QMetaContext = QMetaContext;

function QMeta({ section, sectionName, qIndex, qTotal, subStep, subTotal }) {
  const ctx = React.useContext(QMetaContext);
  const displayIndex = ctx?.visibleQIndex ?? qIndex;
  const displayTotal = ctx?.visibleQTotal ?? qTotal;
  return (
    <div className="q-meta">
      <span>Question {displayIndex} of {displayTotal}</span>
      {subStep && (
        <>
          <span className="dot"></span>
          <span>Step {subStep} of {subTotal}</span>
        </>
      )}
    </div>
  );
}

function Option({ k, label, hint, icon, selected, onSelect }) {
  return (
    <button className={"opt" + (selected ? " selected" : "")} onClick={onSelect} type="button">
      {k && <span className="opt-key">{k}</span>}
      <span className="opt-label">
        {label}
        {hint && <div className="opt-hint">{hint}</div>}
      </span>
      {icon && <span className="opt-icon">{icon}</span>}
    </button>
  );
}

function CheckOpt({ label, hint, selected, onToggle, disabled }) {
  return (
    <button
      className={"opt" + (selected ? " selected" : "") + (disabled ? " opt-disabled" : "")}
      onClick={disabled ? undefined : onToggle}
      type="button"
      disabled={disabled}
      style={disabled ? { opacity: 0.45, cursor: "not-allowed" } : undefined}
    >
      <span className="opt-check">
        {selected && (
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round">
            <polyline points="20 6 9 17 4 12"></polyline>
          </svg>
        )}
      </span>
      <span className="opt-label">
        {label}
        {hint && <div className="opt-hint">{hint}</div>}
      </span>
    </button>
  );
}

/* ===================== Canvas content ===================== */

function CanvasVideo() {
  const [playing, setPlaying] = React.useState(false);
  return (
    <div className="wiz-canvas-inner" style={{padding: 32, display:"flex", flexDirection:"column", justifyContent:"center", gap: 20}}>
      <div
        style={{
          position: "relative",
          aspectRatio: "16 / 9",
          borderRadius: 12,
          overflow: "hidden",
          border: "1px solid hsl(var(--gst-border))",
          width: "100%",
          boxShadow: "0 4px 24px rgba(0,0,0,0.08)",
          background: "#000",
          cursor: playing ? "default" : "pointer",
        }}
        onClick={() => { if (!playing) setPlaying(true); }}
        role={playing ? undefined : "button"}
        aria-label={playing ? undefined : "Play video — Pre-connect to Airbnb"}
      >
        {!playing && (
          <>
            <SkeletonImg
              src="assets/video-thumbnail.png"
              alt="Pre-connect to Airbnb"
              style={{width:"100%", height:"100%", objectFit:"cover", display:"block", userSelect:"none"}}
              wrapStyle={{position:"absolute", inset:0, display:"block", lineHeight:0}}
            />
            <div style={{position:"absolute", inset:0, display:"flex", alignItems:"center", justifyContent:"center", zIndex:2}}>
              <div style={{
                width:72, height:72, borderRadius:"50%",
                background:"rgba(255,255,255,0.95)",
                display:"flex", alignItems:"center", justifyContent:"center",
                boxShadow:"0 8px 32px rgba(0,0,0,0.35)",
              }}>
                <svg width="26" height="26" viewBox="0 0 24 24" fill="hsl(var(--gst-primary))" stroke="none">
                  <path d="M8 5v14l11-7z"/>
                </svg>
              </div>
            </div>
            <div style={{
              position:"absolute", bottom:12, right:14,
              color:"white", fontSize:12, fontWeight:600,
              background:"rgba(0,0,0,0.5)", padding:"3px 10px", borderRadius:4,
              zIndex:2,
            }}>1:42</div>
          </>
        )}
        {playing && (
          <iframe
            src="https://www.youtube-nocookie.com/embed/LfFd_s2kz8Y?autoplay=1&rel=0&modestbranding=1&playsinline=1"
            title="Pre-connect to Airbnb"
            frameBorder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
            allowFullScreen
            style={{position:"absolute", inset:0, width:"100%", height:"100%", border:0, display:"block"}}
          ></iframe>
        )}
      </div>
      <div style={{fontSize:13, color:"hsl(var(--gst-muted-foreground))", lineHeight:1.55, textAlign:"center"}}>
        See how a view-only Airbnb connection works in under 2 minutes.
      </div>
    </div>
  );
}

function CanvasAHA({ importedCount }) {
  const cnt = importedCount ?? MOCK_LISTINGS.length;
  const shown = MOCK_LISTINGS.slice(0, cnt);
  return (
    <div className="wiz-canvas-inner">
      <div className="canvas-header">
        <h3>Your Airbnb account</h3>
        <span className="last-sync"><span className="dot"></span>View-only · synced just now</span>
      </div>

      <div className="aha-summary">
        <div className="stat">
          <div className="num">{cnt}</div>
          <div className="lbl">listings imported</div>
        </div>
        <div className="stat">
          <div className="num">22</div>
          <div className="lbl">reservations synced</div>
        </div>
        <div className="stat">
          <div className="num">3</div>
          <div className="lbl">guest messages</div>
        </div>
      </div>

      <div>
        <h3 style={{fontSize:12, fontWeight:600, color:"hsl(var(--gst-muted-foreground))", textTransform:"uppercase", letterSpacing:"0.06em", marginBottom:10}}>
          Listings imported in view-only mode
        </h3>
        <div className="listing-list">
          {shown.map((l, i) => (
            <div key={l.id} className="listing-card" style={{animationDelay: (80 * i) + "ms"}}>
              <div className="thumb" style={{backgroundImage: `url(${l.img})`}}></div>
              <div className="body">
                <div className="title">{l.name}</div>
                <div className="sub">
                  <span>{l.beds} bd</span>
                  <span>·</span>
                  <span className="channel">
                    <SkeletonImg
                      src={"assets/channel-" + l.channel + "-circle.svg"}
                      alt={l.channel}
                      wrapStyle={{display:"inline-block", width:14, height:14, borderRadius:"50%", overflow:"hidden", lineHeight:0, flexShrink:0}}
                    />
                    {l.channel === "airbnb" ? "Airbnb" : "Booking.com"}
                  </span>
                </div>
              </div>
              <span className="badge">{l.status}</span>
            </div>
          ))}
        </div>
        <div style={{
          marginTop: 14, padding: "10px 14px",
          background: "white",
          border: "1px solid hsl(var(--gst-border))",
          borderRadius: 10,
          fontSize: 12.5,
          color: "hsl(var(--gst-muted-foreground))",
          display: "flex", alignItems: "center", gap: 8,
        }}>
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="hsl(var(--gst-information))" strokeWidth="2"><circle cx="12" cy="12" r="10"/><path d="M12 8v4M12 16h.01"/></svg>
          View-only — nothing in Airbnb has changed.
        </div>
      </div>
    </div>
  );
}

function CanvasMilestone() {
  const plan = window.OB_adaptivePlan ? window.OB_adaptivePlan() : { order: [1, 2, 3, 4, 5, 6, 7, 8] };
  const names = window.OB_sectionNames || {};
  const order = plan.order;
  const finIdx = order.indexOf(4);
  const doneCount = finIdx >= 0 ? finIdx : 0;
  const lastDone = doneCount ? (names[order[doneCount - 1]] || "your last section") : "";
  const subtitle = doneCount
    ? `${lastDone} ${doneCount === 1 ? "is" : "and the sections before it are"} set. Financials next, then a few short sections after that.`
    : "Financials next, then a few short sections after that.";
  return (
    <div className="wiz-canvas-inner" style={{justifyContent:"center"}}>
      <div className="milestone-card">
        <div className="milestone-card-body">
          <div className="milestone-card-illustration" aria-hidden="true">
            <svg width="100%" height="100%" viewBox="0 0 270 181" fill="none" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid meet">
              <g clipPath="url(#clip0_ms_ill)">
                <path d="M176.709 155.254V80.6624C176.709 61.9691 191.862 46.8164 210.555 46.8164C229.248 46.8164 244.401 61.9691 244.401 80.6624V155.254" stroke="#072C23" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                <path d="M141.396 49.9867L125.141 36.0005L116.729 51.5577L95.7324 54.3713L113.453 61.9975L109.789 83.5689L135.323 74.4245L147.076 99.1261L159.368 78.8326L183.952 82.2266L173.049 62.7713L187.059 43.3688L161.109 52.8824L154.731 40.0217L141.396 49.9867Z" fill="#E6F784"/>
                <path d="M160.761 81.8687C162.959 80.7843 164.671 78.9789 165.843 76.8276C166.084 76.388 166.388 75.9718 166.705 75.5849C167.572 74.5298 168.604 73.5802 169.102 72.273C169.267 71.8509 169.267 71.3644 169.05 70.9658C168.534 70.0279 167.479 70.2565 166.775 70.7431C166.224 71.1241 165.767 71.6575 165.163 71.9506C165.028 69.6586 165.269 67.3608 165.339 65.0689C165.357 64.5237 165.357 63.9551 165.116 63.4569C164.894 62.9996 164.272 62.6948 163.762 62.7183C163.252 62.7417 162.754 62.3079 162.062 62.0266C161.324 61.7218 160.04 61.6338 159.36 61.4638C157.977 61.1239 156.752 62.7652 155.503 63.0583C154.7 63.2458 154.301 64.512 154.413 65.2857C154.905 68.8907 152.49 72.4488 153.088 76.0363C153.369 77.7186 154.296 79.2251 155.292 80.6085C155.872 81.4115 156.541 82.2322 157.484 82.5194C158.469 82.8184 159.524 82.4666 160.45 82.0153C160.55 81.9684 160.65 81.9156 160.749 81.8687H160.761Z" fill="#DDD7CE"/>
                <path d="M155.309 80.6082L153.738 102.162C153.491 105.562 155.098 108.833 157.941 110.714L186.423 129.548L192.396 111.822L165.455 100.204L164.488 78.8262L155.309 80.6082Z" fill="#DDD7CE"/>
                <path d="M165.257 99.5481C164.342 90.4506 164.688 81.2769 165.028 72.1384L165.356 63.4922C165.397 62.4312 164.354 61.6223 163.328 62.1792" stroke="#072C23" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                <path d="M164.122 79.5412C165.605 77.6302 167.094 75.7134 168.577 73.8025C168.958 73.316 169.345 72.8119 169.527 72.2198C169.708 71.6278 169.644 70.9185 169.204 70.4847C168.436 69.7227 167.141 70.1916 166.221 70.7661C164.632 71.7626 163.178 72.9701 161.906 74.3418" fill="#DDD7CE"/>
                <path d="M163.328 99.126L183.399 109.12" stroke="#072C23" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                <path d="M155.885 70.1806C158.042 69.5007 160.434 69.5944 162.532 70.4444" stroke="#072C23" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                <path d="M124.103 62.9415C123.206 61.4467 123.4 61.1302 122.685 60.2568C121.688 59.0434 120.481 57.9824 120.1 56.3528C120.41 54.6236 121.764 54.8346 122.608 55.4149C123.159 55.796 123.617 56.3294 124.22 56.6225C124.355 54.3305 123.253 49.6704 123.183 47.3726C123.154 46.4464 124.303 45.7019 127.655 46.1064C130.885 46.4933 132.72 46.7688 133.652 49.1604C134.977 52.5485 136.888 57.1207 136.284 60.7081C136.003 62.3905 135.076 63.8969 134.08 65.2803C133.5 66.0834 132.831 66.904 131.888 67.1913C130.903 67.4902 129.848 67.1385 128.922 66.6872C127.075 65.7962 125.416 64.5066 124.091 62.9415H124.103Z" fill="#DDD7CE"/>
                <path d="M134.903 62.3081L135.888 93.4225C135.999 96.9865 134.317 100.369 131.403 102.426L96.8013 126.852L90.8281 109.126L122.693 89.5068L125.717 60.5378L134.897 62.3198L134.903 62.3081Z" fill="#DDD7CE"/>
                <path d="M124.987 59.6533C124.588 57.0037 124.19 54.3542 123.791 51.6988C123.639 50.6847 122.812 48.3224 123.193 47.3728C123.738 46.0012 124.741 45.966 125.725 46.2532" stroke="#072C23" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                <path d="M123.002 55.3911C122.961 54.5763 121.865 54.1249 121.144 54.506C120.423 54.887 120.124 55.8073 120.224 56.6162C120.927 59.7171 123.143 61.077 124.649 63.75C123.846 74.4829 122.668 85.2042 122.422 95.9664" stroke="#072C23" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                <path d="M219.773 136.067L226.708 128.934L244.405 155.253H230.606L219.773 136.067Z" fill="#DDD7CE"/>
                <path d="M176.709 105.064L232.085 126.008L219.77 136.067L230.602 155.253L196.616 154.174L176.709 105.064Z" fill="#19C0A2"/>
                <path d="M227.653 129.83L178.959 112.303" stroke="white" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                <path d="M220.892 135.511L183.723 122.368" stroke="white" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                <path d="M223.785 143.823L187.008 130.464" stroke="white" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                <path d="M228.442 152.51L190.264 139.461" stroke="white" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                <path d="M215.118 155.253L194.391 148.67" stroke="white" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                <path d="M200.211 104.865L205.187 119.086C206.254 122.14 203.991 125.334 200.756 125.334C198.646 125.334 196.799 123.928 196.23 121.899L191.477 104.865H200.205H200.211Z" fill="#DDD7CE"/>
                <path d="M194.39 109.983C198.796 109.983 202.368 105.398 202.368 99.742C202.368 94.0863 198.796 89.5015 194.39 89.5015C189.984 89.5015 186.412 94.0863 186.412 99.742C186.412 105.398 189.984 109.983 194.39 109.983Z" fill="#DDD7CE"/>
                <path d="M199.359 107.755C193.796 113.336 186.269 107.673 186.41 99.7479C186.41 94.0912 189.98 89.5073 194.388 89.5073" stroke="#072C23" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                <path d="M196.953 90.9018C198.782 92.3145 199.978 94.5068 200.224 96.8046C200.294 97.4494 200.904 97.889 201.531 97.7132C202.235 97.5139 203.02 97.3791 203.448 97.2911C204.691 94.9112 202.85 91.6638 202.37 90.5501C201.309 88.0881 196.994 90.1222 196.625 90.7494" fill="#072C23"/>
                <path d="M201.171 97.5559C202.636 96.8935 204.359 97.5441 205.022 99.0096C205.684 100.475 205.033 102.198 203.568 102.861C202.103 103.523 200.379 102.873 199.717 101.407" fill="#DDD7CE"/>
                <path d="M218.512 82.0802C222.85 86.9983 216.332 96.2658 220.276 100.205C224.802 104.73 229.825 99.9939 234.386 98.7922C236.865 98.1357 239.996 98.6808 241.139 100.973C242.557 103.827 240.201 107.813 242.264 110.234C244.691 113.083 251.127 110.064 253.067 110.182L252.68 122.726C248.812 124.438 245.125 125.182 241.021 124.144C236.918 123.107 233.266 119.531 233.196 115.299C233.178 114.009 234.339 106.975 228.436 110.193C225.576 111.753 222.375 112.954 219.133 112.661C215.892 112.368 212.65 110.229 211.912 107.057C211.132 103.716 213.957 94.4134 210.071 91.4356C207.978 89.8295 206.062 90.1519 202.416 92.1918C201.355 92.7839 200.012 92.4204 199.397 91.3712C199.051 90.7791 198.969 90.0581 199.239 89.4309C201.255 84.6946 213.166 76.025 218.506 82.0744L218.512 82.0802Z" fill="#072C23"/>
                <path d="M194.592 83.7744C188.906 82.4731 185.835 87.7252 183.953 91.3947L194.041 94.5835C194.041 94.5835 195.935 90.5389 199.715 90.6913C199.715 90.6913 198.713 84.7181 194.598 83.7744H194.592Z" fill="#072C23"/>
                <path d="M269.401 155.253H176.709" stroke="#072C23" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                <path d="M50.178 134.186L25.0661 145.411C23.161 146.261 21.0156 144.866 21.0156 142.785V104.964C21.0156 100.222 21.9945 95.7029 23.7589 91.6055C24.4917 92.1799 26.1506 94.1671 26.6429 102.966C27.1705 112.374 28.9994 126.108 28.9583 125.117L45.2483 118.775L50.178 134.191V134.186Z" fill="#DDD7CE"/>
                <path d="M40.8638 120.586L25.4004 126.044" stroke="#072C23" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                <path d="M21.0156 179.55H88.7076V104.959C86.9314 60.075 22.7976 60.0632 21.0156 104.959V179.55Z" stroke="#072C23" strokeWidth="1.5" strokeLinejoin="round"/>
                <path d="M227.101 153.952C225.5 153.6 223.959 155.147 223.806 156.777C223.654 158.407 224.527 159.966 225.594 161.203C226.948 162.779 228.795 164.087 230.87 164.192C232.945 164.292 235.161 162.832 235.354 160.763C235.448 159.731 235.061 158.723 234.95 157.697C234.838 156.671 235.143 155.44 236.099 155.042C232.986 153.453 229.27 153.084 225.905 154.034" fill="#DDD7CE"/>
                <path d="M235.936 155.125C233.04 153.7 229.593 152.2 226.405 153.518C222.946 154.99 222.43 158.911 225.156 161.408C226.293 162.487 227.747 163.161 229.206 163.736" stroke="#072C23" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                <path d="M84.3012 95.4155L75.954 109.355C73.7735 112.995 76.3995 117.626 80.6435 117.626C82.6716 117.626 84.5298 116.506 85.4794 114.713L95.6614 95.4155H84.3012Z" fill="#DDD7CE"/>
                <path d="M95.3649 99.4938C99.8485 97.8415 101.763 91.8356 99.6421 86.0792C97.5207 80.3228 92.1663 76.9958 87.6827 78.6481C83.1991 80.3004 81.2842 86.3064 83.4055 92.0628C85.5269 97.8191 90.8813 101.146 95.3649 99.4938Z" fill="#DDD7CE"/>
                <path d="M90.1006 99.3605C97.6564 102.192 102.651 93.7801 99.6495 86.0777C97.5275 80.3215 92.1698 76.992 87.6855 78.645" stroke="#072C23" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                <path d="M97.0568 78.2463C100.064 70.8956 92.045 66.4524 84.7001 70.8722C81.9568 72.5252 80.1397 75.6144 81.2886 78.3811C81.781 79.5594 83.2933 79.1314 82.7306 77.8887C82.4316 77.2264 81.7165 76.7691 80.9193 76.6519C79.5711 76.4585 78.3401 77.115 77.4901 77.9943C75.9719 79.5594 75.5616 81.9158 76.476 83.815C77.0857 85.087 78.1349 84.2605 77.9005 83.645C77.5487 82.713 76.2064 83.0999 75.544 83.5923C74.0961 84.6708 73.3986 86.488 73.8031 88.1293C74.2075 89.7706 75.6964 91.1598 77.5194 91.5995C76.5991 93.3815 76.9802 95.6851 78.598 97.0099C80.2159 98.3347 83.1409 98.9736 84.8232 97.7485C86.2418 96.7168 87.0976 94.3721 87.0859 93.1997C87.0859 93.0884 87.2969 90.4154 88.2993 89.5068C88.7858 89.0672 88.0941 87.4786 87.3086 87.039C90.1399 89.1668 94.2021 87.971 93.9442 83.1233C93.8914 82.1854 93.4401 81.2944 92.7366 80.5969C91.7284 79.5887 95.3217 82.4609 97.0451 78.2522L97.0568 78.2463Z" fill="white"/>
                <path d="M97.0587 78.2463C100.066 70.8956 92.0469 66.4524 84.7021 70.8722C81.9588 72.5252 80.1416 75.6144 81.2905 78.3811C81.7829 79.5594 83.2953 79.1314 82.7325 77.8887C81.7243 75.884 78.682 76.5581 77.4979 77.9943C75.9797 79.5594 75.5694 81.9158 76.4839 83.815C77.0935 85.087 78.1427 84.2605 77.9083 83.645C77.5566 82.713 76.2142 83.0999 75.5518 83.5923C74.104 84.6708 73.4064 86.488 73.8109 88.1293C74.2153 89.7706 75.7042 91.1598 77.5272 91.5995C76.6069 93.3815 76.988 95.6851 78.6058 97.0099C80.2237 98.3347 83.1487 98.9736 84.831 97.7485C86.2496 96.7168 87.1054 94.3721 87.0937 93.1997C87.0937 93.0884 87.3047 90.4154 88.3071 89.5068C88.7936 89.0672 88.1019 87.4786 87.3164 87.039C90.1477 89.1668 94.2099 87.971 93.952 83.1233C93.8992 82.1854 93.4479 81.2944 92.7445 80.5969C91.7362 79.5887 95.3295 82.4609 97.0529 78.2522L97.0587 78.2463Z" stroke="#072C23" strokeWidth="1.5" strokeLinejoin="round"/>
                <path d="M89.3424 89.3544C87.7539 88.6334 85.8781 89.3427 85.163 90.9312C84.442 92.5198 85.1513 94.3955 86.7398 95.1107C88.3284 95.8317 90.2041 95.1224 90.9193 93.5339" fill="#DDD7CE"/>
                <path d="M89.3424 89.3544C87.7539 88.6334 85.8781 89.3427 85.163 90.9312C84.442 92.5198 85.1513 94.3955 86.7398 95.1107C88.3284 95.8317 90.2041 95.1224 90.9193 93.5339" stroke="#072C23" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                <path d="M25.3967 94.2376C24.793 92.2211 21.5455 90.2809 20.039 89.8178C18.9546 89.4837 17.6885 89.4251 16.7389 90.3102C15.9416 91.0546 15.5372 92.3501 15.5313 93.5576C15.5255 94.771 15.8654 95.9141 16.2992 96.9516C17.583 100.035 19.7342 102.462 22.3076 103.728" fill="#DDD7CE"/>
                <path d="M88.7051 179.55V158.858H45.4099L26.9805 179.55" fill="white"/>
                <path d="M88.7051 179.55V158.858H45.4099L26.9805 179.55" stroke="black" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                <path d="M63.3558 161.126L57.8398 179.55" stroke="black" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                <path d="M68.8026 164.327H84.014V179.562L64.3301 178.987L68.8026 164.327Z" fill="#19C0A2"/>
                <path d="M0.578125 179.685L88.7043 179.55" stroke="#072C23" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                <path d="M111.378 94.5779V121.519L102.468 124.784C98.8455 126.108 95.9204 128.846 94.3553 132.369L88.7104 158.864H39.2721L59.8059 131.548L49.4599 136.882L37.8184 120.235L63.3289 109.824C68.4638 107.732 73.9973 106.811 79.5309 107.134L88.7104 107.673L111.384 94.5779H111.378Z" fill="#072C23"/>
                <path d="M53.3382 152.944C53.6943 152.944 53.983 152.505 53.983 151.965C53.983 151.424 53.6943 150.986 53.3382 150.986C52.982 150.986 52.6934 151.424 52.6934 151.965C52.6934 152.505 52.982 152.944 53.3382 152.944Z" fill="#19C0A2"/>
                <path d="M76.7913 133.401C77.1474 133.401 77.4361 132.962 77.4361 132.422C77.4361 131.881 77.1474 131.443 76.7913 131.443C76.4352 131.443 76.1465 131.881 76.1465 132.422C76.1465 132.962 76.4352 133.401 76.7913 133.401Z" fill="#19C0A2"/>
                <path d="M70.3089 156.367C70.665 156.367 70.9537 155.929 70.9537 155.388C70.9537 154.847 70.665 154.409 70.3089 154.409C69.9527 154.409 69.6641 154.847 69.6641 155.388C69.6641 155.929 69.9527 156.367 70.3089 156.367Z" fill="#19C0A2"/>
                <path d="M90.7678 132.422C91.124 132.422 91.4126 131.984 91.4126 131.443C91.4126 130.902 91.124 130.464 90.7678 130.464C90.4117 130.464 90.123 130.902 90.123 131.443C90.123 131.984 90.4117 132.422 90.7678 132.422Z" fill="#19C0A2"/>
                <path d="M70.9553 113.037C71.3115 113.037 71.6001 112.599 71.6001 112.058C71.6001 111.517 71.3115 111.079 70.9553 111.079C70.5992 111.079 70.3105 111.517 70.3105 112.058C70.3105 112.599 70.5992 113.037 70.9553 113.037Z" fill="#19C0A2"/>
                <path d="M107.821 118.635C108.177 118.635 108.465 118.196 108.465 117.656C108.465 117.115 108.177 116.677 107.821 116.677C107.464 116.677 107.176 117.115 107.176 117.656C107.176 118.196 107.464 118.635 107.821 118.635Z" fill="#19C0A2"/>
                <path d="M87.2522 148.043C87.6083 148.043 87.897 147.605 87.897 147.064C87.897 146.524 87.6083 146.085 87.2522 146.085C86.8961 146.085 86.6074 146.524 86.6074 147.064C86.6074 147.605 86.8961 148.043 87.2522 148.043Z" fill="#19C0A2"/>
                <path d="M82.596 120.586C82.9521 120.586 83.2408 120.148 83.2408 119.608C83.2408 119.067 82.9521 118.629 82.596 118.629C82.2399 118.629 81.9512 119.067 81.9512 119.608C81.9512 120.148 82.2399 120.586 82.596 120.586Z" fill="#19C0A2"/>
                <path d="M49.6135 132.422C49.9697 132.422 50.2583 131.984 50.2583 131.443C50.2583 130.902 49.9697 130.464 49.6135 130.464C49.2574 130.464 48.9688 130.902 48.9688 131.443C48.9688 131.984 49.2574 132.422 49.6135 132.422Z" fill="#19C0A2"/>
                <path d="M95.0803 115.791C95.4365 115.791 95.7251 115.353 95.7251 114.812C95.7251 114.272 95.4365 113.833 95.0803 113.833C94.7242 113.833 94.4355 114.272 94.4355 114.812C94.4355 115.353 94.7242 115.791 95.0803 115.791Z" fill="#19C0A2"/>
                <path d="M62.6723 138.439C63.1997 138.32 63.5637 137.942 63.4853 137.595C63.407 137.247 62.9159 137.062 62.3885 137.181C61.8611 137.3 61.4971 137.678 61.5755 138.025C61.6538 138.373 62.1449 138.558 62.6723 138.439Z" fill="#19C0A2"/>
                <path d="M105.2 102.173C105.727 102.054 106.091 101.676 106.013 101.329C105.934 100.981 105.443 100.796 104.916 100.915C104.388 101.034 104.024 101.412 104.103 101.76C104.181 102.107 104.672 102.292 105.2 102.173Z" fill="#19C0A2"/>
                <path d="M74.7387 145.619C75.2661 145.5 75.6301 145.122 75.5517 144.775C75.4734 144.428 74.9823 144.242 74.4549 144.361C73.9275 144.48 73.5635 144.858 73.6419 145.206C73.7202 145.553 74.2113 145.738 74.7387 145.619Z" fill="#19C0A2"/>
                <path d="M61.7074 122.997C62.2348 122.878 62.5988 122.5 62.5205 122.153C62.4421 121.805 61.9511 121.62 61.4237 121.739C60.8963 121.858 60.5323 122.236 60.6106 122.583C60.689 122.931 61.18 123.116 61.7074 122.997Z" fill="#19C0A2"/>
                <path d="M49.7601 120.237C50.2875 120.118 50.6516 119.74 50.5732 119.393C50.4949 119.045 50.0038 118.86 49.4764 118.979C48.949 119.098 48.585 119.476 48.6634 119.823C48.7417 120.171 49.2328 120.356 49.7601 120.237Z" fill="#19C0A2"/>
              </g>
              <defs>
                <clipPath id="clip0_ms_ill">
                  <rect width="270" height="144.27" fill="white" transform="translate(0 36)"/>
                </clipPath>
              </defs>
            </svg>
          </div>
          <div className="milestone-card-text">
            <span className="crown">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                <path d="M5 16L3 8l5.5 5L12 4l3.5 9L21 8l-2 8H5z"></path>
              </svg>
              Milestone
            </span>
            <h2>You're halfway through.</h2>
            <p>{subtitle}</p>
            <div className="milestone-bar">
              {order.map((sec, i) => (
                <div key={sec} className={"seg" + (i < doneCount ? " done" : i === doneCount ? " now" : "")}></div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function screenVisible(id, answers) {
  const s = makeScreens().find((x) => x.id === id);
  if (!s) return false;
  return !s.showIf || s.showIf(answers);
}

function prettyChannelsDual(answers) {
  const cur = formatChannelList(answers.channels_current || answers.channels || [], []);
  const add = formatChannelList(answers.channels_to_add || [], []);
  if (!cur && !add) return "—";
  if (cur && add) return `Today: ${cur} · To add: ${add}`;
  if (cur) return `Today: ${cur}`;
  return `To add: ${add}`;
}

function prettyTaxesSummary(answers) {
  const taxes = answers.taxes;
  if (!taxes || !taxes.length) return "—";
  if (typeof taxes[0] === "string") return `${taxes.length} tax type${taxes.length === 1 ? "" : "s"}`;
  const n = taxes.length;
  const withRate = taxes.filter((t) => t.mode !== "unsure" && t.rate).length;
  return `${n} tax type${n === 1 ? "" : "s"} · ${withRate} rate${withRate === 1 ? "" : "s"} set`;
}

function prettyOnboardMore(a) {
  if (!a.onboard_more) return "—";
  if (a.onboard_more === "no") return "No";
  return a.onboard_more_count ? `Yes · ~${a.onboard_more_count}` : "Yes";
}

function prettyTiming(v) {
  return { pre_arrival: "Pre-arrival", pre_departure: "Pre-departure" }[v] || "—";
}

function prettyInspections(v) {
  return { yes: "Yes", no: "No" }[v] || "—";
}

function prettyOwnersGate(a) {
  if (!a.owners_gate) return "—";
  const map = { all: "Yes, all listings", some: "Yes, some listings", no: "No" };
  let s = map[a.owners_gate] || "—";
  if (a.owners_gate === "some" && (a.owner_listings || []).length) {
    s += ` · ${a.owner_listings.length} listing${a.owner_listings.length === 1 ? "" : "s"}`;
  }
  return s;
}

function prettyOwnerSplitType(a) {
  if (!a.owner_split_type) return "—";
  const map = { commission: "% commission", fixed: "Fixed fee", mixed: "Mixed" };
  let s = map[a.owner_split_type] || "—";
  if (a.owner_split_type === "mixed" && a.owner_split_breakdown) {
    const b = a.owner_split_breakdown;
    s += ` · ${b.pct || "—"}% / $${b.flat || "—"}`;
  }
  return s;
}

function prettyPricingTool(a) {
  if (!a.pricing_tool) return "—";
  if (a.pricing_tool === "no") return "No";
  return a.pricing_tool_name ? `Yes · ${a.pricing_tool_name}` : "Yes";
}

function prettySeasons(a) {
  // Seasons are now month ranges (ints 1–12); a missing end = single-month range.
  const fmt = (s, e) => (s ? `${MONTHS[s - 1]}–${MONTHS[(e || s) - 1]}` : null);
  const low = fmt(a.low_season_start, a.low_season_end);
  const high = fmt(a.high_season_start, a.high_season_end);
  if (!low && !high) return "—";
  if (low && high) return `Low: ${low} · High: ${high}`;
  return low ? `Low: ${low}` : `High: ${high}`;
}

function reviewRowsForSection(sectionNum, answers, skippedFn, valueFn) {
  const screens = makeScreens().filter((s) => s.section === sectionNum);
  const rows = [];
  const rowDefs = {
    1: [
      { qid: "Q7.1", label: "Brand logo", value: valueFn("Q7.1", answers.logo_file ? "Uploaded" : "—") },
    ],
    2: [
      { qid: "Q1.1", label: "Active listings", value: valueFn("Q1.1", `${answers.listing_count ?? SF_PREFILL.listing_count} listings`) },
      { qid: "Q2.onboard_more", label: "Onboarding more soon", value: valueFn("Q2.onboard_more", prettyOnboardMore(answers)) },
      { qid: "Q1.2", label: "Channels", value: valueFn("Q1.2", prettyChannelsDual(answers)) },
      { qid: "Q1.4", label: "Airbnb connection", value: answers.oauth_status === "success" ? valueFn("Q1.4", `View-only · ${(answers.selected_listings ?? MOCK_LISTINGS).length} listings`) : valueFn("Q1.4", "—") },
      { qid: "Q1.5", label: "Going live", value: valueFn("Q1.5", prettyGoLive(answers.go_live, answers.go_live_date)) },
    ],
    3: [
      { qid: "Q2.1", label: "Cleaning", value: valueFn("Q2.1", prettyCleaning(answers.cleaning_system, answers)) },
      { qid: "Q2.4", label: "Turnover checklist", value: valueFn("Q2.4", answers.checklist_choice === "upload" ? (answers.checklist_file ? "Uploaded" : "Upload pending") : answers.checklist_choice === "guesty" ? "Guesty template" : "—") },
      { qid: "Q2.timing", label: "Cleaning timing", value: valueFn("Q2.timing", prettyTiming(answers.cleaning_timing)) },
      { qid: "Q2.inspections", label: "Inspections", value: valueFn("Q2.inspections", prettyInspections(answers.inspections)) },
    ],
    4: [
      { qid: "Q3.1", label: "Revenue recognition", value: valueFn("Q3.1", prettyRevenue(answers.revenue_recognition)) },
      { qid: "Q3.2", label: "Non-refundable rates", value: valueFn("Q3.2", prettyNonref(answers.nonrefundable)) },
      { qid: "Q3.4", label: "Payment timing", value: valueFn("Q3.4", prettyPayment(answers)) },
      { qid: "Q3.6", label: "Mandatory fees", value: valueFn("Q3.6", (answers.fees_list || []).length ? `${(answers.fees_list || []).length} fee${(answers.fees_list || []).length === 1 ? "" : "s"}` : "None") },
      { qid: "Q3.7", label: "Taxes", value: valueFn("Q3.7", prettyTaxesSummary(answers)) },
    ],
    5: [
      { qid: "Q5.owners_gate", label: "Work with owners", value: valueFn("Q5.owners_gate", prettyOwnersGate(answers)) },
      { qid: "Q7.2", label: "Owner records", value: valueFn("Q7.2", answers.owners_csv ? "CSV uploaded" : "—") },
      { qid: "Q5.owner_split", label: "Revenue split", value: valueFn("Q5.owner_split", prettyOwnerSplitType(answers)) },
    ],
    6: [
      { qid: "Q6.pricing_tool", label: "Pricing tool", value: valueFn("Q6.pricing_tool", prettyPricingTool(answers)) },
      { qid: "Q7.3", label: "Season dates", value: valueFn("Q7.3", prettySeasons(answers)) },
    ],
    7: [
      { qid: "Q5.1", label: "Decision owners", value: valueFn("Q5.1", prettyOwner(answers.owner_split)) },
      { qid: "Q5.2", label: "Teammates invited", value: valueFn("Q5.2", `${answers.teammates_count || 0} invitations`) },
    ],
    8: [
      { qid: "Q6.1", label: "Topics for Call 1", value: valueFn("Q6.1", (answers.focus_topics || []).length ? (answers.focus_topics || []).join(" · ") : "—") },
      { qid: "Q6.2", label: "Biggest pain", value: valueFn("Q6.2", ((answers.pain || "").slice(0, 72) + ((answers.pain || "").length > 72 ? "…" : "")) || "—") },
    ],
  };
  (rowDefs[sectionNum] || []).forEach((r) => {
    if (screenVisible(r.qid, answers)) rows.push(r);
  });
  return rows;
}

function CanvasReview({ answers, onJumpTo }) {
  const skipped = (id) => (answers.__skipped || []).includes(id);

  const SkippedChip = () => (
    <span style={{
      fontSize: 11, fontWeight: 600,
      color: "hsl(var(--gst-warning))",
      background: "hsl(var(--gst-warning) / 0.12)",
      padding: "2px 8px", borderRadius: 999,
      whiteSpace: "nowrap",
    }}>Skipped</span>
  );

  const v = (id, value) => skipped(id) ? <SkippedChip /> : (value || "—");

  const Card = ({ name, rows }) => (
    <div style={{
      background: "white",
      borderRadius: 12,
      border: "1px solid hsl(var(--gst-border))",
      overflow: "hidden",
    }}>
      {/* Card header */}
      <div style={{
        display: "flex", alignItems: "center", justifyContent: "space-between",
        padding: "12px 16px",
        borderBottom: "1px solid hsl(var(--gst-border))",
      }}>
        <span style={{fontSize: 14, fontWeight: 600, color: "hsl(var(--gst-foreground))"}}>
          {name}
        </span>
      </div>
      {/* Rows */}
      <div style={{padding: "2px 0"}}>
        {rows.map((r, i) => (
          <div key={i} style={{
            display: "flex",
            alignItems: "baseline",
            justifyContent: "space-between",
            gap: 12,
            padding: "9px 16px",
            borderBottom: i < rows.length - 1 ? "1px solid hsl(var(--gst-border) / 0.6)" : "none",
          }}>
            <span style={{fontSize: 12.5, color: "hsl(var(--gst-muted-foreground))", flexShrink: 0, whiteSpace: "nowrap"}}>
              {r.label}
            </span>
            <span style={{display:"flex", alignItems:"center", gap:8, justifyContent:"flex-end", flexWrap:"wrap"}}>
              <span style={{fontSize: 13, fontWeight: 500, color: "hsl(var(--gst-foreground))", textAlign:"right"}}>
                {r.value}
              </span>
              <button onClick={() => onJumpTo && onJumpTo(r.qid)} style={{
                background: "transparent", border: 0, padding: 0,
                fontSize: 11.5, fontWeight: 600,
                color: "hsl(var(--gst-primary))",
                cursor: "pointer", fontFamily: "inherit", flexShrink: 0,
              }}>Edit</button>
            </span>
          </div>
        ))}
      </div>
    </div>
  );

  return (
    <div className="wiz-canvas-inner" style={{gap: 12}}>
      <div className="canvas-header">
        <h3>Your answers</h3>
        <span className="last-sync"><span className="dot"></span>Ready to confirm</span>
      </div>

      <Card name="Brand" rows={reviewRowsForSection(1, answers, skipped, v)} />
      <Card name="Portfolio & Channels" rows={reviewRowsForSection(2, answers, skipped, v)} />
      <Card name="Operations" rows={reviewRowsForSection(3, answers, skipped, v)} />
      <Card name="Financials" rows={reviewRowsForSection(4, answers, skipped, v)} />
      <Card name="Owners" rows={reviewRowsForSection(5, answers, skipped, v)} />
      <Card name="Rate strategy" rows={reviewRowsForSection(6, answers, skipped, v)} />
      <Card name="Governance" rows={reviewRowsForSection(7, answers, skipped, v)} />
      <Card name="Focus & context" rows={reviewRowsForSection(8, answers, skipped, v)} />
    </div>
  );
}

/* ===================== Pretty helpers ===================== */
const prettyGoLive = (v, date) => {
  const map = { asap: "Within 2 weeks", "2-4w": "2–4 weeks", "1-2m": "1–2 months", deadline: "Specific deadline" };
  if (!v) return "—";
  if (v === "deadline" && date) return `${map.deadline} · ${date}`;
  return map[v] || "—";
};
const prettyCleaning = (v, answers) => {
  const map = { external: "External provider", pms: "In current PMS", other: "Other" };
  let s = map[v] || "—";
  if (v === "external" && answers?.cleaning_provider) {
    const prov = answers.cleaning_provider === "other"
      ? (answers.cleaning_provider_other || "Other")
      : { breezeway: "Breezeway", turno: "Turno", properly: "Properly", maidthis: "MaidThis" }[answers.cleaning_provider] || answers.cleaning_provider;
    s += ` · ${prov}`;
  }
  return s;
};
const prettyCheckin = v => ({ smart_lock: "Smart lock or keypad", lockbox: "Lockbox", meet: "In-person hand-off", mix: "Mix of methods" }[v]);
const prettyRevenue = v => ({
  checkin: "Check-in date",
  checkout: "Check-out date",
  calendar: "Calendar dates (nights occupied)",
}[v]);
const prettyNonref = v => ({ all: "Yes, on all listings", some: "Yes, on some listings", no: "No" }[v]);
const prettyPayment = a => {
  if (!a.pay_timing) return "—";
  if (a.pay_timing === "full") return "Full amount at booking confirmation";
  if (a.pay_timing === "50_50") return "50% at confirmation, 50% at check-in";
  if (a.pay_timing === "80_20") return "80% at confirmation, 20% at check-in";
  if (a.pay_timing === "other" && a.pay_custom) {
    const c = a.pay_custom;
    return `Other · $${c.amount || "—"} deposit · balance ${c.balance_days ?? "—"} days before check-in`;
  }
  if (a.pay_timing === "other") return "Other";
  return "—";
};
const prettyOwner = v => ({ solo: "Just me", split: "Me plus teammates" }[v]);

window.prettyGoLive = prettyGoLive;
window.prettyCleaning = prettyCleaning;
window.prettyCheckin = prettyCheckin;
window.prettyRevenue = prettyRevenue;

/* ===================== UX Patch 1 — reusable primitives ===================== */

// Stop Enter/Space/Arrow from reaching the wizard's global nav handler (wizard.jsx ~219)
// so that activating a <button> control doesn't also advance/rewind the wizard.
function stopWizNav(e) {
  if (["Enter", " ", "Spacebar", "ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight"].includes(e.key)) {
    e.stopPropagation();
  }
}

// Modern +/- number input — minus left, typable number middle, plus right.
// Numeric input. The unit (prefix "$" / suffix "%" / "days") lives in its own
// divided, centered cell — never floating over the number. The +/- buttons are
// opt-in via `controls`: use them for small counters (e.g. listing counts), skip
// them for typed values like currency or precise percentages.
function Stepper({ value, onChange, min = 0, max = Infinity, step = 1, decimals = false, prefix, suffix, placeholder, ariaLabel, ariaDescribedBy, width = 160, controls = false }) {
  const num = value === "" || value == null ? null : parseFloat(value);
  const clamp = (n) => Math.min(max, Math.max(min, n));
  const round = (n) => decimals ? Math.round(n * 100) / 100 : Math.round(n);
  const bump = (dir) => {
    if (num == null || isNaN(num)) {
      const seed = dir > 0 ? (min > 0 ? min : step) : min;
      onChange(String(clamp(round(seed))));
      return;
    }
    onChange(String(clamp(round(num + dir * step))));
  };
  const atMin = num != null && !isNaN(num) && num <= min;
  const atMax = num != null && !isNaN(num) && num >= max;

  const combo = (
    <div className="stepper-combo" style={controls ? { flex: 1 } : { width }}>
      {prefix && <span className="stepper-cell stepper-cell-prefix">{prefix}</span>}
      <input
        className="stepper-input"
        type="number"
        inputMode={decimals ? "decimal" : "numeric"}
        min={min} max={max === Infinity ? undefined : max} step={decimals ? "any" : step}
        value={value ?? ""}
        placeholder={placeholder}
        aria-label={ariaLabel}
        aria-describedby={ariaDescribedBy}
        onChange={(e) => onChange(e.target.value)}
        onBlur={(e) => {
          if (e.target.value === "") return;
          const n = parseFloat(e.target.value);
          if (isNaN(n)) { onChange(""); return; }
          onChange(String(clamp(round(n))));
        }}
      />
      {suffix && <span className="stepper-cell stepper-cell-suffix">{suffix}</span>}
    </div>
  );

  if (!controls) return combo;

  return (
    <div className="stepper" style={{ display: "inline-flex", alignItems: "stretch", gap: 8, width }}>
      <button type="button" className="stepper-btn" aria-label="Decrease" disabled={atMin} onClick={() => bump(-1)} onKeyDown={stopWizNav}>
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round"><line x1="5" y1="12" x2="19" y2="12"/></svg>
      </button>
      {combo}
      <button type="button" className="stepper-btn" aria-label="Increase" disabled={atMax} onClick={() => bump(1)} onKeyDown={stopWizNav}>
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
      </button>
    </div>
  );
}

// Segmented radio — connected pills in one bordered track, the active one filled.
// A tighter replacement for a row of standalone radio boxes.
function SegmentedControl({ options, value, onSelect, ariaLabel, ariaDescribedBy }) {
  return (
    <div className="seg-control" role="radiogroup" aria-label={ariaLabel} aria-describedby={ariaDescribedBy}>
      {options.map((o) => {
        const sel = value === o.id;
        return (
          <button key={o.id} type="button" role="radio" aria-checked={sel}
            className={"seg-item" + (sel ? " seg-item-sel" : "")}
            onClick={() => onSelect(o.id)} onKeyDown={stopWizNav}>
            {o.label}
          </button>
        );
      })}
    </div>
  );
}

// Single-select big boxes (cleaning-provider page) — lifted from the focus-topics grid.
function BigBoxSelect({ options, value, onSelect, columns = 2 }) {
  return (
    <div style={{ display: "grid", gridTemplateColumns: `repeat(${columns}, 1fr)`, gap: 12 }}>
      {options.map((o) => {
        const sel = value === o.id;
        return (
          <button key={o.id} type="button" className="bigbox-opt" onClick={() => onSelect(o.id)} onKeyDown={stopWizNav}
            style={{
              display: "flex", alignItems: "center", gap: 14, padding: "16px 18px",
              border: "1.5px solid " + (sel ? "hsl(var(--gst-primary))" : "hsl(var(--gst-border))"),
              borderRadius: 10, background: sel ? "hsl(var(--gst-primary) / 0.06)" : "white",
              cursor: "pointer", textAlign: "left", fontFamily: "inherit", transition: "all 140ms",
              boxShadow: sel ? "0 0 0 3px hsl(var(--gst-primary) / 0.12)" : "none",
            }}>
            <span style={{ fontSize: 14, fontWeight: sel ? 600 : 500, color: sel ? "hsl(var(--gst-primary))" : "hsl(var(--gst-foreground))", lineHeight: 1.3 }}>{o.label}</span>
            {sel && (
              <span style={{ marginLeft: "auto", width: 18, height: 18, borderRadius: "50%", background: "hsl(var(--gst-primary))", display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0 }}>
                <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="3.5" strokeLinecap="round" strokeLinejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
              </span>
            )}
          </button>
        );
      })}
    </div>
  );
}

// Recurring season window — a 12-chip month strip; tap start then end, wraps across the year.
const MONTHS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];
function monthsInRange(start, end) {
  if (!start) return [];
  if (!end || end === start) return [start];
  const out = [];
  let m = start;
  for (let i = 0; i < 12; i++) { out.push(m); if (m === end) break; m = m === 12 ? 1 : m + 1; }
  return out;
}
function rangeLabel(start, end) {
  if (!start) return "";
  const span = monthsInRange(start, end);
  return `${MONTHS[start - 1]} – ${MONTHS[(end || start) - 1]} · ${span.length} month${span.length === 1 ? "" : "s"}`;
}
function MonthRangePicker({ value, onChange, tipId, monthTipKey, setMonthTipKey }) {
  const start = value?.start ?? null;
  const end = value?.end ?? null;
  const picking = start && !end ? "end" : "start";
  const inRange = new Set(monthsInRange(start, end));
  const click = (m) => {
    if (picking === "start" || (start && end)) onChange({ start: m, end: undefined }); // (re)start
    else onChange({ start, end: m });                                                  // complete
  };
  const rangeTip = "Tap start, then end. Can wrap across year-end.";
  const tipKey = (m) => `${tipId}:${m}`;
  const showTip = (m) => monthTipKey === tipKey(m);
  const activateTip = (m) => setMonthTipKey(tipKey(m));
  const deactivateTip = (m) => {
    if (monthTipKey === tipKey(m)) setMonthTipKey(null);
  };
  return (
    <div>
      <div className="month-strip" role="group" aria-label={`Select a month range. ${rangeTip}`} style={{ display: "grid", gridTemplateColumns: "repeat(12, 1fr)", gap: 4 }}>
        {MONTHS.map((label, i) => {
          const m = i + 1;
          const sel = inRange.has(m);
          const isEnd = m === start || m === end;
          const tipIdAttr = `month-tip-${tipId}-${m}`;
          return (
            <span key={m} className="month-chip-wrap"
              onMouseEnter={() => activateTip(m)}
              onMouseLeave={() => deactivateTip(m)}>
              <button type="button" aria-pressed={sel}
                aria-describedby={showTip(m) ? tipIdAttr : undefined}
                className={"month-chip" + (sel ? " sel" : "") + (isEnd ? " end" : "")}
                onClick={() => click(m)}
                onFocus={() => activateTip(m)}
                onBlur={(e) => {
                  if (!e.currentTarget.closest(".month-strip")?.contains(e.relatedTarget)) deactivateTip(m);
                }}
                onKeyDown={stopWizNav}>{label}</button>
              {showTip(m) && (
                <span className="month-chip-tooltip month-chip-tooltip--visible" id={tipIdAttr} role="tooltip">
                  {rangeTip}
                  <span className="fee-optional-tooltip-arrow" aria-hidden="true" />
                </span>
              )}
            </span>
          );
        })}
      </div>
      <div className="month-summary" aria-live="polite">
        {start && !end ? "Now pick the end month (it can wrap into next year)." : rangeLabel(start, end)}
      </div>
    </div>
  );
}

function SeasonDatesRender({ answers, set }) {
  const [monthTipKey, setMonthTipKey] = useState(null);
  return (
    <>
      <QMeta section={6} sectionName="Rate strategy" qIndex={2} qTotal={2} />
      <h1 className="q-title">What are your low and high seasons?</h1>
      <p className="q-help">We'll use these to set up your rate strategies — refine them in Guesty's pricing tool anytime.</p>
      <div style={{ display: "flex", flexDirection: "column", gap: 24 }}>
        <div>
          <div style={{ fontWeight: 600, marginBottom: 20 }}>Low season</div>
          <MonthRangePicker
            tipId="low"
            monthTipKey={monthTipKey}
            setMonthTipKey={setMonthTipKey}
            value={{ start: answers.low_season_start, end: answers.low_season_end }}
            onChange={({ start, end }) => set({ low_season_start: start, low_season_end: end })} />
        </div>
        <div>
          <div style={{ fontWeight: 600, marginBottom: 20 }}>High season</div>
          <MonthRangePicker
            tipId="high"
            monthTipKey={monthTipKey}
            setMonthTipKey={setMonthTipKey}
            value={{ start: answers.high_season_start, end: answers.high_season_end }}
            onChange={({ start, end }) => set({ high_season_start: start, high_season_end: end })} />
        </div>
      </div>
    </>
  );
}

/* ===================== Q1.4 Step 2 — Choose Listings table ===================== */
function ChooseListings({ answers, set, setMaxWidth, valueKey = "selected_listings", storeIds = false, defaultAll = true }) {
  useEffect(() => { setMaxWidth && setMaxWidth(988); return () => setMaxWidth && setMaxWidth(null); }, []);
  // Write either full listing objects (Airbnb) or bare ids (owners) under valueKey.
  const commit = (nextSet) => set(valueKey, storeIds
    ? MOCK_LISTINGS.filter(l => nextSet.has(l.id)).map(l => l.id)
    : MOCK_LISTINGS.filter(l => nextSet.has(l.id)));
  const [selected, setSelected] = useState(() => {
    const stored = answers[valueKey];
    if (stored) return new Set(storeIds ? stored : stored.map(l => l.id));
    return new Set(defaultAll ? MOCK_LISTINGS.map(l => l.id) : []);
  });
  const [city, setCity] = useState("All");
  const [status, setStatus] = useState("All");
  const [ownership, setOwnership] = useState("All");
  const [query, setQuery] = useState("");

  const cities = useMemo(() => ["All", ...Array.from(new Set(MOCK_LISTINGS.map(l => l.city)))], []);

  const filtered = MOCK_LISTINGS.filter(l => {
    if (city !== "All" && l.city !== city) return false;
    if (status !== "All" && l.status !== status) return false;
    if (ownership === "Owner" && l.hostRole !== "owner") return false;
    if (ownership === "Co-host" && l.hostRole !== "co-host") return false;
    if (query) {
      const q = query.toLowerCase();
      if (!(l.name.toLowerCase().includes(q) || (l.nickname || "").toLowerCase().includes(q) || l.address.toLowerCase().includes(q))) return false;
    }
    return true;
  });

  const allSelected = filtered.length > 0 && filtered.every(l => selected.has(l.id));
  const toggleAll = () => {
    const next = new Set(selected);
    if (allSelected) filtered.forEach(l => next.delete(l.id));
    else filtered.forEach(l => next.add(l.id));
    setSelected(next);
    commit(next);
  };
  const toggle = (id) => {
    const next = new Set(selected);
    next.has(id) ? next.delete(id) : next.add(id);
    setSelected(next);
    commit(next);
  };

  return (
    <div style={{display:"flex", flexDirection:"column", gap:14}}>
      {/* Toolbar */}
      <div style={{
        display: "flex", alignItems: "center", gap: 8, flexWrap: "wrap",
        padding: "8px 0", paddingLeft: 16,
      }}>
        <label style={{display:"flex", alignItems:"center", gap:8, fontSize:13, fontWeight:500, marginRight:4}}>
          <span style={{
            width: 18, height: 18, border: "1.5px solid hsl(var(--gst-input))", borderRadius: 4,
            background: allSelected ? "hsl(var(--gst-primary))" : "white",
            borderColor: allSelected ? "hsl(var(--gst-primary))" : "hsl(var(--gst-input))",
            display: "flex", alignItems: "center", justifyContent: "center",
            cursor: "pointer",
          }} onClick={toggleAll}>
            {allSelected && <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"><polyline points="20 6 9 17 4 12"/></svg>}
          </span>
          <span onClick={toggleAll} style={{cursor:"pointer"}}>Select all</span>
        </label>

        <FilterDropdown label="City"      value={city}      options={cities}                       onChange={setCity} />
        <FilterDropdown label="Status"    value={status}    options={["All", "Listed", "Unlisted"]}   onChange={setStatus} />
        <FilterDropdown label="Ownership" value={ownership} options={["All", "Owner", "Co-host"]}     onChange={setOwnership} />

        <div style={{width: 180, display:"flex", alignItems:"center", gap:6, marginLeft:8}}>
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="hsl(var(--gst-muted-foreground))" strokeWidth="2"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/></svg>
          <input
            className="input"
            style={{padding: "6px 8px", fontSize: 13, flex: 1, width: "100%"}}
            placeholder="Search…"
            aria-label="Search listings by name, nickname, or address"
            value={query}
            onChange={e => setQuery(e.target.value)}
          />
        </div>

      </div>

      {/* List */}
      {filtered.length === 0 ? (
        <div style={{padding: 24, textAlign:"center", color:"hsl(var(--gst-muted-foreground))", fontSize:13, border:"1px dashed hsl(var(--gst-border))", borderRadius:10}}>
          <div style={{fontWeight:600, color:"hsl(var(--gst-foreground))", marginBottom:4}}>
            {query ? `No listings match "${query}"` : "No listings match these filters"}
          </div>
          <div>{query ? "Check your spelling or try a broader search." : "Try removing a filter or adjusting your criteria."}</div>
        </div>
      ) : (
        <div style={{display:"flex", flexDirection:"column", gap:6}}>
          {filtered.map(l => {
            const isSel = selected.has(l.id);
            return (
              <div key={l.id} style={{
                display: "flex", alignItems: "center", gap: 16,
                padding: "0 16px",
                height: 100,
                minHeight: 100,
                background: "white",
                border: "1px solid " + (isSel ? "hsl(var(--gst-primary) / 0.4)" : "hsl(var(--gst-border))"),
                borderRadius: 8,
                cursor: "pointer",
                transition: "all 140ms",
                flexShrink: 0,
              }} onClick={() => toggle(l.id)}>
                <span style={{
                  width: 18, height: 18, borderRadius: 4,
                  border: "1.5px solid " + (isSel ? "hsl(var(--gst-primary))" : "hsl(var(--gst-input))"),
                  background: isSel ? "hsl(var(--gst-primary))" : "white",
                  display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0,
                }} aria-label={`Select listing ${l.name}`}>
                  {isSel && <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"><polyline points="20 6 9 17 4 12"/></svg>}
                </span>
                <div className="thumb" style={{
                  width: 100, height: 67, borderRadius: 6,
                  backgroundImage: `url(${l.img})`, backgroundSize:"cover", backgroundPosition:"center",
                  flexShrink: 0,
                }}></div>
                <div style={{flex:1, minWidth:0, display:"flex", flexDirection:"column", gap:5}}>
                  <div style={{display:"flex", alignItems:"center", gap:8}}>
                    {l.hostRole === "co-host" && (
                      <span title="You co-host this listing on Airbnb." style={{color:"hsl(var(--gst-information))", display:"inline-flex", flexShrink:0}}>
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/></svg>
                      </span>
                    )}
                    <span style={{fontSize:18, fontWeight:600, color:"hsl(var(--gst-foreground))", whiteSpace:"nowrap", overflow:"hidden", textOverflow:"ellipsis", lineHeight:1.2}}>{l.name}</span>
                    <span style={{
                      fontSize: 11, fontWeight: 600,
                      padding: "2px 7px", borderRadius: 4,
                      background: l.unitType === "Multi Unit" ? "hsl(var(--gst-information) / 0.12)" : "hsl(var(--gst-secondary))",
                      color: l.unitType === "Multi Unit" ? "hsl(var(--gst-information))" : "hsl(var(--gst-muted-foreground))",
                      flexShrink: 0,
                    }}>{l.unitType}</span>
                  </div>
                  <div style={{fontSize:13, color:"hsl(var(--gst-muted-foreground))", lineHeight:1.5}}>
                    {l.nickname} · {l.propertyType}
                  </div>
                  <div style={{fontSize:12.5, color:"hsl(var(--gst-muted-foreground))", lineHeight:1.5, whiteSpace:"nowrap", overflow:"hidden", textOverflow:"ellipsis"}}>
                    {l.address}
                  </div>
                </div>
                <span style={{
                  fontSize: 11, fontWeight: 600,
                  padding: "2px 8px", borderRadius: 999,
                  background: l.status === "Listed" ? "hsl(var(--gst-success) / 0.12)" : "hsl(var(--gst-warning) / 0.12)",
                  color: l.status === "Listed" ? "hsl(var(--gst-success))" : "hsl(var(--gst-warning))",
                  flexShrink: 0,
                }}>{l.status}</span>
              </div>
            );
          })}
        </div>
      )}


    </div>
  );
}

function FilterDropdown({ label, value, options, onChange }) {
  const [open, setOpen] = useState(false);
  return (
    <div style={{position:"relative"}}>
      <button onClick={() => setOpen(o => !o)} type="button" style={{
        display: "inline-flex", alignItems: "center", gap: 6,
        background: "white",
        border: "1px solid hsl(var(--gst-border))",
        borderRadius: 6,
        padding: "6px 10px",
        fontSize: 12.5,
        fontWeight: 500,
        cursor: "pointer",
        fontFamily: "inherit",
      }}>
        <span style={{color: "hsl(var(--gst-muted-foreground))"}}>{label}:</span>
        <span>{value}</span>
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><polyline points="6 9 12 15 18 9"/></svg>
      </button>
      {open && (
        <div style={{
          position: "absolute", top: "calc(100% + 4px)", left: 0, zIndex: 20,
          background: "white",
          border: "1px solid hsl(var(--gst-border))",
          borderRadius: 8,
          boxShadow: "var(--shadow-md)",
          minWidth: 140, padding: 4,
        }} onMouseLeave={() => setOpen(false)}>
          {options.map(o => (
            <button key={o} onClick={() => { onChange(o); setOpen(false); }} type="button" style={{
              display: "block", width: "100%", textAlign: "left",
              padding: "6px 10px",
              fontSize: 13, fontFamily: "inherit",
              background: o === value ? "hsl(var(--gst-muted))" : "transparent",
              color: o === value ? "hsl(var(--gst-primary))" : "hsl(var(--gst-foreground))",
              fontWeight: o === value ? 600 : 400,
              border: 0, borderRadius: 4, cursor: "pointer",
            }}>{o}</button>
          ))}
        </div>
      )}
    </div>
  );
}

/* ===================== Q3.6 Fee Builder (50/50 patch) ===================== */

const FEE_DICTIONARY_BASE = [
  "Damage Waiver",
  "Management Fee",
  "Credit Card Processing Fee",
  "Booking Fee",
  "Resort Fee",
  "Service Fee",
  "Linens Fee",
  "Pet Fee",
  "Cleaning fee",
  "Other",
];

function feeDictionaryFor(answers) {
  const showCleaning = !(answers.channels_current || answers.channels || []).includes("airbnb");
  return FEE_DICTIONARY_BASE.filter((n) => n !== "Cleaning fee" || showCleaning);
}

const ACCOUNT_CURRENCY = "USD";

function FeeBuilder({ answers, set }) {
  const fees = answers.fees_list || [];
  const [query, setQuery] = useState("");
  const [showAll, setShowAll] = useState(false);
  const inputRef = useRef(null);
  const FEE_DICTIONARY = feeDictionaryFor(answers);

  const addedDictNames = new Set(fees.filter(f => f.kind === "dictionary").map(f => f.name));
  const availableSuggestions = FEE_DICTIONARY.filter(n => !addedDictNames.has(n));

  const q = query.trim();
  const ql = q.toLowerCase();
  const matches = q
    ? availableSuggestions.filter(n => n.toLowerCase().includes(ql))
    : [];
  const exactInDict = q && FEE_DICTIONARY.some(n => n.toLowerCase() === ql);
  const queryIsCustom = q && !exactInDict;

  const addFee = (name, kind) => {
    set("fees_list", [...fees, { name, kind, amount: "", unitType: "$", unit: "" }]);
    if (answers.__no_fees) set("__no_fees", false);
    setQuery("");
    setShowAll(false);
    setTimeout(() => inputRef.current?.focus(), 0);
  };

  const removeLastFee = () => {
    set("fees_list", fees.slice(0, -1));
  };

  const onKeyDown = (e) => {
    if (e.key === "Backspace" && !query && fees.length > 0) {
      e.preventDefault();
      removeLastFee();
      return;
    }
    if (e.key === "Enter") {
      e.preventDefault();
      if (!q) return;
      const exact = availableSuggestions.find(n => n.toLowerCase() === ql);
      if (exact) addFee(exact, "dictionary");
      else if (matches.length > 0) addFee(matches[0], "dictionary");
      else addFee(q, "custom");
    }
  };

  const visibleSuggestions = showAll ? availableSuggestions : availableSuggestions.slice(0, 8);
  const extraCount = availableSuggestions.length - 8;
  const helperCopy = availableSuggestions.length === 0
    ? "Add another fee, or continue when you're done."
    : "Start typing to see matches, or pick a suggestion below.";

  return (
    <>
      <h1 className="q-title">What fees do you charge guests, on top of the nightly rate?</h1>
      <p className="q-help">Pick from the list, or add your own. You can edit each fee on the right.</p>

      <div className="fee-input-wrap">
        <input
          ref={inputRef}
          className="input fee-input"
          placeholder="Search or add a fee…"
          value={query}
          onChange={e => setQuery(e.target.value)}
          onKeyDown={onKeyDown}
          aria-label="Search or add a fee"
        />
        <div className="fee-helper" style={{marginTop: 6}}>{helperCopy}</div>
        {q && (matches.length > 0 || queryIsCustom) && (
          <div className="fee-dropdown" role="listbox">
            {matches.slice(0, 8).map(name => (
              <button
                key={name}
                className="fee-dropdown-item"
                onClick={() => addFee(name, "dictionary")}
                type="button"
              >
                {name}
              </button>
            ))}
            {queryIsCustom && (
              <button
                className="fee-dropdown-item fee-dropdown-custom"
                onClick={() => addFee(q, "custom")}
                type="button"
              >
                Add "{q}" as a custom fee
              </button>
            )}
          </div>
        )}
        {q && matches.length === 0 && !queryIsCustom && (
          <div className="fee-dropdown">
            <div className="fee-dropdown-empty">No matches. Press Enter to add "{q}" as a custom fee.</div>
          </div>
        )}
      </div>

      {availableSuggestions.length > 0 && (
        <>
          <div className="fee-suggestions-label">Suggestions</div>
          <div className="fee-chip-row">
            {visibleSuggestions.map(name => (
              <button
                key={name}
                className="fee-chip"
                onClick={() => addFee(name, "dictionary")}
                type="button"
              >
                {name}
              </button>
            ))}
            {!showAll && extraCount > 0 && (
              <button
                className="fee-chip fee-chip-more"
                onClick={() => setShowAll(true)}
                type="button"
              >
                +{extraCount} more
              </button>
            )}
          </div>
        </>
      )}
    </>
  );
}

function CanvasFeeBuilder({ answers, set }) {
  const fees = answers.fees_list || [];

  const removeFee = (idx) => {
    set("fees_list", fees.filter((_, i) => i !== idx));
  };
  const updateFee = (idx, patch) => {
    set("fees_list", fees.map((f, i) => i === idx ? { ...f, ...patch } : f));
  };

  // "I don't charge mandatory fees" — advance via wizard's keyboard handler
  const skipAsAnswer = () => {
    set("fees_list", []);
    set("__no_fees", true);
    setTimeout(() => {
      window.dispatchEvent(new KeyboardEvent("keydown", { key: "ArrowDown" }));
    }, 60);
  };

  return (
    <div className="wiz-canvas-inner fee-canvas">
      <div className="canvas-header">
        {fees.length > 0 && <span className="fee-counter">{fees.length} added</span>}
      </div>

      {fees.length === 0 ? (
        <div className="fee-empty">
          <SkeletonImg
            src="assets/type=User roles, value=Cleaner supervisor.svg"
            alt=""
            style={{width:72, height:72, objectFit:"contain", opacity:0.88}}
            wrapStyle={{display:"block", width:72, height:72, marginLeft:"auto", marginRight:"auto", marginBottom:12, borderRadius:8}}
          />
          <div className="fee-empty-heading">No fees added yet</div>
          <div className="fee-empty-body">Pick a fee on the left to start. We'll let you set the amount and how it's charged.</div>
          <button className="fee-no-fees-link" onClick={skipAsAnswer} type="button">
            I don't charge mandatory fees
          </button>
        </div>
      ) : (
        <div className="fee-card-list" aria-live="polite">
          {fees.map((fee, i) => (
            <FeeCard
              key={i}
              fee={fee}
              idx={i}
              onUpdate={updateFee}
              onRemove={removeFee}
            />
          ))}
        </div>
      )}
    </div>
  );
}

function FeeCard({ fee, idx, onUpdate, onRemove }) {
  const [editingName, setEditingName] = useState(false);
  const [draftName, setDraftName] = useState(fee.name);
  const nameInputRef = useRef(null);
  const amountInputId = `fee-amount-${idx}`;
  const amountTooltipId = `fee-amount-tooltip-${idx}`;
  const chargedSelectId = `fee-charged-${idx}`;
  const chargedTooltipId = `fee-charged-tooltip-${idx}`;

  useEffect(() => { setDraftName(fee.name); }, [fee.name]);

  const isCustom = fee.kind === "custom";
  const amountNum = parseFloat(fee.amount);
  const amountEmpty = fee.amount === "" || fee.amount === null || fee.amount === undefined;
  const amountInvalid = !amountEmpty && (isNaN(amountNum) || amountNum <= 0);
  const pctTooHigh = !amountEmpty && fee.unitType === "%" && amountNum > 100;

  // Soft (outlier) check
  const soft = (() => {
    if (amountEmpty || amountInvalid || pctTooHigh) return null;
    if (fee.unitType === "%" && amountNum > 50) return true;
    if (fee.unitType === "$" && fee.unit === "Per night" && amountNum > 200) return true;
    if (fee.unitType === "$" && fee.unit === "Per reservation" && amountNum > 500) return true;
    return null;
  })();

  const blocking = amountInvalid || pctTooHigh;
  const errMsg = amountInvalid
    ? "Amount must be greater than zero."
    : pctTooHigh
    ? "Percentages must be 100 or less."
    : null;

  const commitName = () => {
    const trimmed = draftName.trim();
    if (trimmed && trimmed.length <= 40) onUpdate(idx, { name: trimmed });
    else setDraftName(fee.name);
    setEditingName(false);
  };

  const startEdit = () => {
    if (!isCustom) return;
    setDraftName(fee.name);
    setEditingName(true);
    setTimeout(() => nameInputRef.current?.select(), 0);
  };

  return (
    <div className={"fee-card" + (blocking ? " fee-card-error" : soft ? " fee-card-warn" : "")}>
      <div className="fee-card-head">
        {editingName && isCustom ? (
          <input
            ref={nameInputRef}
            className="input fee-name-input"
            autoFocus
            value={draftName}
            onChange={e => setDraftName(e.target.value)}
            onBlur={commitName}
            onKeyDown={e => {
              if (e.key === "Enter") { e.preventDefault(); commitName(); }
              if (e.key === "Escape") { e.preventDefault(); setDraftName(fee.name); setEditingName(false); }
            }}
            maxLength={80}
          />
        ) : (
          <button
            className={"fee-card-title" + (isCustom ? " editable" : "")}
            onClick={startEdit}
            disabled={!isCustom}
            type="button"
            aria-label={isCustom ? "Edit fee name" : undefined}
          >
            <span>{fee.name}</span>
            {isCustom && (
              <svg className="pencil" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" />
                <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" />
              </svg>
            )}
          </button>
        )}
        {isCustom && !editingName && <span className="fee-custom-tag">Custom</span>}
        <button
          className="fee-card-close"
          onClick={() => onRemove(idx)}
          aria-label={`Remove ${fee.name}`}
          type="button"
        >
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2"><path d="M18 6L6 18M6 6l12 12" /></svg>
        </button>
      </div>

      <div className="fee-card-fields">
        <div className="fee-field fee-optional-field">
          <label className="fee-sentence-label" htmlFor={amountInputId}>Amount</label>
          <div className="fee-amount-row">
            <input
              id={amountInputId}
              className="input fee-amount"
              type="number"
              inputMode="decimal"
              value={fee.amount}
              onChange={e => onUpdate(idx, { amount: e.target.value })}
              aria-invalid={blocking ? "true" : "false"}
              aria-describedby={amountTooltipId}
            />
            <div className="fee-unit-toggle" role="group" aria-label="Amount unit">
              <button
                type="button"
                className={"u" + (fee.unitType === "$" ? " on" : "")}
                onClick={() => onUpdate(idx, { unitType: "$" })}
                aria-label={`Amount in ${ACCOUNT_CURRENCY}`}
                aria-pressed={fee.unitType === "$"}
              >$</button>
              <button
                type="button"
                className={"u" + (fee.unitType === "%" ? " on" : "")}
                onClick={() => onUpdate(idx, { unitType: "%" })}
                aria-label="Amount as percentage of subtotal"
                aria-pressed={fee.unitType === "%"}
              >%</button>
            </div>
          </div>
          <div className={"fee-field-hint" + (errMsg ? " err" : soft ? " warn" : "")}>
            {errMsg
              ? errMsg
              : soft
              ? <>That's higher than most accounts. Looks right? <button type="button" className="fee-confirm-link" onClick={() => { /* acknowledged silently */ }}>Confirm</button></>
              : (fee.unitType === "%" ? "Of the pre-tax subtotal" : `In ${ACCOUNT_CURRENCY}`)}
          </div>
          <div className="fee-optional-tooltip" id={amountTooltipId} role="tooltip">
            This field is optional. You can keep it blank.
            <span className="fee-optional-tooltip-arrow" aria-hidden="true" />
          </div>
        </div>

        <div className="fee-field fee-optional-field">
          <label className="fee-sentence-label" htmlFor={chargedSelectId}>Charged</label>
          <select
            id={chargedSelectId}
            className="input fee-charged"
            value={fee.unit || ""}
            onChange={e => onUpdate(idx, { unit: e.target.value })}
            aria-describedby={chargedTooltipId}
          >
            <option value="">Keep blank</option>
            <option>Per reservation</option>
            <option>Per night</option>
            <option>Per guest, per night</option>
          </select>
          <div className="fee-optional-tooltip" id={chargedTooltipId} role="tooltip">
            This field is optional. You can keep it blank.
            <span className="fee-optional-tooltip-arrow" aria-hidden="true" />
          </div>
        </div>
      </div>
    </div>
  );
}

/* ===================== Q1.2 / Q1.3 Salesforce channel prefill (2026-05-27 revB) ===================== */

const CHANNEL_NAME = {
  airbnb: "Airbnb",
  booking: "Booking.com",
  booking_com: "Booking.com",
  vrbo: "VRBO/Expedia",
  agoda: "Agoda",
  tripcom: "Trip.com",
  google_vr: "Google VR",
  direct: "Direct site",
  none: "None yet",
};

const CHANNEL_OPTIONS = [
  { id: "airbnb", label: "Airbnb", icon: "assets/channel-grid-airbnb.png" },
  { id: "booking", label: "Booking.com", icon: "assets/channel-grid-booking.png" },
  { id: "vrbo", label: "VRBO/Expedia", icon: "assets/channel-grid-vrbo.png" },
  { id: "agoda", label: "Agoda", icon: "assets/channel-grid-agoda.png" },
  { id: "tripcom", label: "Trip.com", icon: "assets/channel-grid-tripcom.png" },
  { id: "google_vr", label: "Google VR", icon: "assets/channel-grid-google.png" },
  { id: "direct", label: "Direct site" },
  { id: "none", label: "None yet" },
];

function ChannelGridOpt({ label, icon, hint, selected, onToggle, disabled }) {
  const tipId = hint ? `channel-grid-tip-${label.replace(/[^a-z0-9]+/gi, "-").toLowerCase()}` : undefined;
  const locked = disabled && !!hint;
  const btn = (
    <button
      type="button"
      className={"channel-grid-opt" + (selected ? " selected" : "") + (disabled ? " channel-grid-opt--disabled" : "")}
      onClick={disabled ? undefined : onToggle}
      disabled={disabled && !locked}
      aria-disabled={disabled || undefined}
      aria-pressed={selected}
      aria-describedby={locked ? tipId : undefined}
    >
      <span className="channel-grid-opt-check" aria-hidden="true">
        {selected && (
          <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3.5" strokeLinecap="round" strokeLinejoin="round">
            <polyline points="20 6 9 17 4 12" />
          </svg>
        )}
      </span>
      <span className="channel-grid-opt-icon">
        {icon
          ? <SkeletonImg src={icon} alt="" wrapStyle={{ width: "100%", height: "100%", display: "block" }} />
          : <span className="channel-grid-opt-fallback" aria-hidden="true">{label.slice(0, 1)}</span>}
      </span>
      <span className="channel-grid-opt-label">{label}</span>
    </button>
  );
  if (!hint) return btn;
  return (
    <span className="channel-grid-opt-wrap channel-grid-opt-wrap--locked" tabIndex={locked ? 0 : undefined}>
      {btn}
      <span className="channel-grid-opt-tooltip" id={tipId} role="tooltip">
        {hint}
        <span className="fee-optional-tooltip-arrow" aria-hidden="true" />
      </span>
    </span>
  );
}

// channels is always written = channels_current in the same update — never set channels alone.
function toggleChannelList(listKey, current, channelId, set) {
  const NONE = "none";
  let next;
  if (channelId === NONE) {
    next = current.includes(NONE) ? [] : [NONE];
  } else {
    const base = current.filter((c) => c !== NONE);
    next = base.includes(channelId) ? base.filter((c) => c !== channelId) : [...base, channelId];
  }
  if (listKey === "channels_current") {
    set((prev) => {
      const out = { ...prev, channels_current: next, channels: next };
      // Reconcile page 2: a channel that's now "on today" can't also be "to add".
      // Prune it from channels_to_add so back-nav can't leave a stale selection.
      if (Array.isArray(prev.channels_to_add)) {
        out.channels_to_add = prev.channels_to_add.filter((c) => !next.includes(c));
      }
      if (!next.includes("airbnb")) {
        out.oauth_status = undefined;
        out.selected_listings = undefined;
        Object.keys(out).forEach((k) => { if (k.startsWith("__airbnb_")) delete out[k]; });
      }
      return out;
    });
  } else {
    set({ channels_to_add: next });
  }
}

// UX Patch 3.2b — Page 1 of 2: "On today" only. The "To add" list is its own
// standalone page (ChannelsAddV5Render) that follows this one.
function ChannelsV5Render({ answers, set }) {
  useEffect(() => {
    if (answers.channels_current === undefined) {
      const cur = (SF_PREFILL.channels || []).slice();
      set({ channels_current: cur, channels: cur, channels_to_add: answers.channels_to_add || [] });
    }
  }, []);

  const current = answers.channels_current ?? answers.channels ?? [];

  return (
    <>
      <QMeta section={2} sectionName="Portfolio & Channels" qIndex={3} qTotal={7} />
      <h1 className="q-title">Which channels are your listings on today?</h1>
      <p className="q-help">Pick everywhere your listings are currently live. We'll connect Airbnb first when it's in your mix — that gives us the richest data.</p>

      <div className="channel-grid" role="group" aria-label="Channels your listings are on today">
        {CHANNEL_OPTIONS.map((c) => (
          <ChannelGridOpt
            key={"cur-" + c.id}
            label={c.label}
            icon={c.icon}
            selected={current.includes(c.id)}
            onToggle={() => toggleChannelList("channels_current", current, c.id, set)}
          />
        ))}
      </div>
    </>
  );
}

// UX Patch 3.2b — Page 2 of 2: "To add with Guesty". Standalone page that follows
// the "On today" page. Channels already on today are disabled here (you can't add
// what you already run); "None yet" is filtered out — you can't *add* "none".
// Edge case: when every addable channel is already on today, show an empty state.
function ChannelsAddV5Render({ answers, set }) {
  const current = answers.channels_current ?? answers.channels ?? [];
  const toAdd = answers.channels_to_add ?? [];
  const addable = CHANNEL_OPTIONS.filter((c) => c.id !== "none");
  const allOnToday = addable.every((c) => current.includes(c.id));

  return (
    <>
      <QMeta section={2} sectionName="Portfolio & Channels" qIndex={3} qTotal={7} />
      <h1 className="q-title">Which channels do you want to add with Guesty?</h1>
      <p className="q-help">Pick the new channels you'd like to launch. Channels you're already on are locked — we'll cover those in the steps ahead.</p>

      {allOnToday ? (
        <div className="channel-grid channel-grid--empty">
          <div className="channel-grid-empty-msg">
            You're already live on every channel we support — nothing to add here. Hit Continue to keep going.
          </div>
        </div>
      ) : (
        <div className="channel-grid" role="group" aria-label="Channels to add with Guesty">
          {addable.map((c) => {
            const onToday = current.includes(c.id);
            return (
              <ChannelGridOpt
                key={"add-" + c.id}
                label={c.label}
                icon={c.icon}
                hint={onToday ? "Already on this channel." : undefined}
                selected={toAdd.includes(c.id)}
                disabled={onToday}
                onToggle={() => toggleChannelList("channels_to_add", toAdd, c.id, set)}
              />
            );
          })}
        </div>
      )}
    </>
  );
}

// UX Patch 3.7 — taxes split: shared type defs + normalization, used by both the
// left pick-list (Q3.7 render) and the right CanvasTaxes builder.
const TAX_TYPE_DEFS = [
  { id: "sales", label: "Sales tax or VAT" },
  { id: "occupancy", label: "Occupancy or tourist tax" },
  { id: "city", label: "City or local tax" },
  { id: "other", label: "Other" },
];
function normalizeTaxes(raw) {
  if (!Array.isArray(raw) || !raw.length) return [];
  if (typeof raw[0] === "object") return raw;
  return raw.map((id) => ({ type: id, rate: "", mode: "" }));
}
function taxLabel(id) { return (TAX_TYPE_DEFS.find((x) => x.id === id) || {}).label || id; }

// Right canvas: per-selected-type card — rate Stepper on its own row, then
// Inclusive / Exclusive / Not sure radio-boxes on the row below.
function CanvasTaxes({ answers, set }) {
  const taxes = normalizeTaxes(answers.taxes);
  const updateTax = (type, patch) => set("taxes", taxes.map((x) => (x.type === type ? { ...x, ...patch } : x)));
  const removeTax = (type) => set("taxes", taxes.filter((x) => x.type !== type));
  const MODES = [
    { id: "inclusive", label: "Inclusive" },
    { id: "exclusive", label: "Exclusive" },
    { id: "unsure", label: "Not sure" },
  ];
  return (
    <div className="wiz-canvas-inner fee-canvas">
      <div className="canvas-header">
        {taxes.length > 0 && <span className="fee-counter">{taxes.length} added</span>}
      </div>
      {taxes.length === 0 ? (
        <div className="fee-empty">
          <SkeletonImg
            src="assets/type=User roles, value=Financial manager.svg"
            alt=""
            style={{width:72, height:72, objectFit:"contain", opacity:0.88}}
            wrapStyle={{display:"block", width:72, height:72, marginLeft:"auto", marginRight:"auto", marginBottom:12, borderRadius:8}}
          />
          <div className="fee-empty-heading">No taxes selected</div>
          <div className="fee-empty-body">Select a tax type on the left to set its rate.</div>
        </div>
      ) : (
        <div className="fee-card-list" aria-live="polite">
          {taxes.map((tx) => {
            const label = taxLabel(tx.type);
            const rateTooltipId = `tax-rate-tooltip-${tx.type}`;
            const modeTooltipId = `tax-mode-tooltip-${tx.type}`;
            const optionalTip = (
              <>
                This field is optional. You can keep it blank.
                <span className="fee-optional-tooltip-arrow" aria-hidden="true" />
              </>
            );
            return (
              <div key={tx.type} className="fee-card">
                <div className="fee-card-head">
                  <button type="button" className="fee-card-title" disabled>
                    <span>{label}</span>
                  </button>
                  <button
                    type="button"
                    className="fee-card-close"
                    onClick={() => removeTax(tx.type)}
                    aria-label={`Remove ${label}`}
                  >
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2"><path d="M18 6L6 18M6 6l12 12" /></svg>
                  </button>
                </div>
                <div className="fee-card-fields">
                  {tx.mode !== "unsure" && (
                    <div className="fee-field fee-optional-field">
                      <label className="fee-sentence-label">Rate</label>
                      <Stepper value={tx.rate} min={0} max={100} step={0.5} decimals suffix="%" width={108} ariaLabel={label + " rate"}
                        ariaDescribedBy={rateTooltipId}
                        onChange={(v) => updateTax(tx.type, { rate: v })} />
                      <div className="fee-optional-tooltip" id={rateTooltipId} role="tooltip">{optionalTip}</div>
                    </div>
                  )}
                  <div className="fee-field fee-optional-field">
                    <label className="fee-sentence-label">How is it charged?</label>
                    <SegmentedControl
                      options={MODES}
                      value={tx.mode}
                      ariaLabel={label + " charge mode"}
                      ariaDescribedBy={modeTooltipId}
                      onSelect={(id) => updateTax(tx.type, id === "unsure" ? { mode: "unsure", rate: "" } : { mode: id })} />
                    <div className="fee-optional-tooltip" id={modeTooltipId} role="tooltip">{optionalTip}</div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
window.CanvasTaxes = CanvasTaxes;

// Channel brand logos — used in the "Your listings are on these channels" pill.
const CHANNEL_LOGO = {
  airbnb:      { src: "assets/channel-airbnb.svg",       alt: "Airbnb" },
  booking:     { src: "assets/channel-booking-logo.svg", alt: "Booking.com" },
  booking_com: { src: "assets/channel-booking-logo.svg", alt: "Booking.com" },
  expedia:     { src: "assets/channel-expedia-logo.svg", alt: "Expedia" },
};

// Renders channel brand logos (falling back to the channel name as text for
// channels without a bundled logo, and for free-text "other" channels).
function ChannelLogos({ channels, otherNames }) {
  if (!channels || !channels.length) return null;
  const items = [];
  let unnamedOther = false;
  for (const c of channels) {
    if (c === "other") {
      const caps = (otherNames || []).filter(n => n && n.trim());
      if (caps.length) caps.forEach(n => items.push({ text: n.trim() }));
      else unnamedOther = true;
    } else if (CHANNEL_LOGO[c]) {
      items.push(CHANNEL_LOGO[c]);
    } else if (CHANNEL_NAME[c]) {
      items.push({ text: CHANNEL_NAME[c] });
    }
  }
  if (unnamedOther) items.push({ text: "one other channel" });
  if (!items.length) return null;
  return (
    <span className="channel-logos">
      {items.map((it, i) => it.src
        ? <img key={i} className="channel-logo-img" src={it.src} alt={it.alt} />
        : <span key={i} className="channel-logo-text">{it.text}</span>
      )}
    </span>
  );
}

// URL flag `?fallback=1` (or `?nosf=1`) forces the no-Salesforce baseline so the
// fallback path stays testable in this prototype.
function isFallbackForced() {
  if (typeof window === "undefined") return false;
  try {
    const p = new URLSearchParams(window.location.search);
    return p.has("fallback") || p.has("nosf");
  } catch { return false; }
}

function resolveChannelPrefill() {
  if (isFallbackForced()) return null;
  const sf = SF_PREFILL.channels || [];
  // Fallback per spec §3.5: missing, empty, or missing 'airbnb'
  if (!sf.length || !sf.includes("airbnb")) return null;
  return {
    channels: sf.slice(),
    sourceCallDate: SF_PREFILL.source_call_date || null,
    otherChannelNames: (SF_PREFILL.other_channel_names || []).slice(),
  };
}

function formatLongDate(iso) {
  if (!iso) return "";
  const d = new Date(iso);
  return d.toLocaleDateString("en-US", { year: "numeric", month: "long", day: "numeric" });
}

function isStale(iso) {
  if (!iso) return false;
  const d = new Date(iso);
  return (Date.now() - d.getTime()) > 30 * 24 * 60 * 60 * 1000;
}

// Build the prefilled-pill display string per spec §2 list-formatting rules.
function formatChannelList(channels, otherNames) {
  if (!channels || !channels.length) return "";
  const named = [];
  let unnamedOther = false;
  for (const c of channels) {
    if (c === "other") {
      const caps = (otherNames || []).filter(n => n && n.trim());
      if (caps.length) caps.forEach(n => named.push(n.trim()));
      else unnamedOther = true;
    } else if (CHANNEL_NAME[c]) {
      named.push(CHANNEL_NAME[c]);
    }
  }
  const all = unnamedOther ? [...named, "one other channel"] : named;
  if (all.length === 0) return "";
  if (all.length === 1) return all[0];
  if (all.length === 2) return `${all[0]} and ${all[1]}`;
  // 3+ — Oxford comma per Atlas style
  return `${all.slice(0, -1).join(", ")}, and ${all[all.length - 1]}`;
}

/* ===================== Q3.7 Educational expansion (taxes) ===================== */

function CanvasTaxesExplain({ onClose }) {
  const titleRef = useRef(null);

  // Focus the title on reveal (per accessibility spec §8)
  useEffect(() => {
    const t = setTimeout(() => { titleRef.current?.focus(); }, 380);
    return () => clearTimeout(t);
  }, []);

  // Esc dismisses (per §7)
  useEffect(() => {
    const onKey = (e) => {
      if (e.key === "Escape") {
        e.stopPropagation();
        onClose && onClose();
      }
    };
    window.addEventListener("keydown", onKey, true);
    return () => window.removeEventListener("keydown", onKey, true);
  }, [onClose]);

  return (
    <div className="explain-module" role="complementary" aria-label="Explanation: How taxes work in Guesty">
      <div className="explain-module-inner">
        <button
          className="explain-close"
          onClick={() => onClose && onClose()}
          aria-label="Close explanation"
          type="button"
        >
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path d="M18 6L6 18M6 6l12 12"/></svg>
        </button>
        <SkeletonImg
          src="assets/q3-7-tax-module-header.svg"
          alt=""
          aria-hidden="true"
          className="explain-header-art"
          wrapStyle={{display:"block", width:"100%", marginBottom:36, borderRadius:6, minHeight:72}}
        />
        <h2
          className="explain-title"
          ref={titleRef}
          tabIndex={-1}
        >How taxes work in Guesty</h2>
        <p className="explain-body">
          Setting up taxes in Guesty automatically applies them to your new reservations. Here is how it works:
        </p>
        <div className="explain-sections">
          <div className="explain-section">
            <div className="explain-section-label">Account vs. listing levels</div>
            <div className="explain-section-text">Set a default tax rate globally for your account, and override it at the listing level for properties in different tax jurisdictions.</div>
          </div>
          <div className="explain-section">
            <div className="explain-section-label">Airbnb syncing</div>
            <div className="explain-section-text">Taxes must be set at the listing level to sync directly with Airbnb. You can also configure Guesty to deduct this tax from the accommodation fare so it appears as a separate line item on the guest folio.</div>
          </div>
          <div className="explain-section">
            <div className="explain-section-label">New reservations only</div>
            <div className="explain-section-text">Taxes are not applied retroactively to existing reservations.</div>
          </div>
        </div>
        <a
          className="explain-academy-link"
          href="https://academy.guesty.com/"
          target="_blank"
          rel="noopener noreferrer"
          aria-label="Go deeper in the Guesty Academy (opens in new tab)"
        >
          Go deeper in the Guesty Academy
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true" style={{marginLeft:6, verticalAlign:"-3px"}}>
            <line x1="5" y1="12" x2="19" y2="12"/>
            <polyline points="12 5 19 12 12 19"/>
          </svg>
        </a>
      </div>
      {/* Polite live region — announces on reveal */}
      <div className="visually-hidden" aria-live="polite">
        Explanation: How taxes work in Guesty.
      </div>
    </div>
  );
}

/* ===================== Screen definitions ===================== */

function makeScreens() { return [

/* ============ Section 1 — Brand ============ */

// Q7.1 — Brand logo
{
  id: "Q7.1", section: 1, sectionName: "Brand", qIndex: 1, qTotal: 1,
  anchor: false, canvas: null,
  render: ({ answers, set }) => (
    <>
      <QMeta section="1" sectionName="Brand" qIndex={1} qTotal={1} />
      <h1 className="q-title">Bring your brand in</h1>
      <p className="q-help">Appears on your booking website and in guest emails. PNG or SVG, square works best.</p>
      <div className="upload-box">
        {answers.logo_file ? (
          <>
            <div style={{width:72, height:72, margin:"0 auto 10px", borderRadius:8, background:"linear-gradient(135deg, hsl(var(--gst-primary)), #2A6F66)", display:"flex", alignItems:"center", justifyContent:"center", color:"white", fontWeight:700, fontSize:24}}>MR</div>
            <div className="upload-title">{answers.logo_file}</div>
            <div style={{display:"flex", gap:8, justifyContent:"center", marginTop:8}}>
              <button className="btn btn-ghost" onClick={() => set("logo_file", "new-logo.svg")}>Replace logo</button>
              <button className="btn btn-ghost" onClick={() => set("logo_file", null)}>Remove logo</button>
            </div>
          </>
        ) : (
          <>
            <div className="upload-title">Drag your logo file here, or select from your computer.</div>
            <div className="upload-sub">PNG, JPG, or SVG. Up to 5 MB.</div>
            <button className="btn btn-secondary" onClick={() => set("logo_file", "mountainretreats-logo.svg")}>Upload logo</button>
          </>
        )}
      </div>
    </>
  ),
  valid: () => true,
  primaryLabel: () => "Continue",
  skipLabel: "I'll add this later",
},

/* ============ Section 2 — Portfolio & Channels ============ */

// Q1.1 — Active listing count
{
  id: "Q1.1", section: 2, sectionName: "Portfolio & Channels", qIndex: 1, qTotal: 7,
  anchor: false, canvas: null,
  render: ({ answers, set }) => {
    const editing = answers.__editing_count;
    return (
      <>
        <QMeta section="2" sectionName="Portfolio & Channels" qIndex={1} qTotal={7} />
        <BotAlert>
          <div>We've pulled most of this in automatically — you'll just confirm what's right.</div>
        </BotAlert>
        <h1 className="q-title">How many active listings do you have?</h1>
        <p className="q-help">We pulled this from your sales call. Confirm or update it before we connect Airbnb.</p>
        {!editing ? (
          <div style={{
            display: "inline-flex", alignItems: "center", gap: 10,
            height: 44, boxSizing: "border-box",
            padding: "0 20px",
            background: "white",
            border: "1.5px solid hsl(var(--gst-border))",
            borderRadius: 8,
            fontSize: 15, fontWeight: 600,
          }}>
            {answers.listing_count ?? SF_PREFILL.listing_count} active listings
            <SourceChip label="From your sales call" />
          </div>
        ) : (
          <div className="input-row" style={{maxWidth: 280}}>
            <input
              className="input lg"
              type="number"
              min="1"
              aria-label="Active listings"
              placeholder="e.g. 8"
              value={answers.listing_count ?? SF_PREFILL.listing_count}
              onChange={e => set("listing_count", parseInt(e.target.value) || 0)}
            />
          </div>
        )}
      </>
    );
  },
  valid: (a) => (a.listing_count ?? SF_PREFILL.listing_count) > 0,
  primaryLabel: (a) => a.__editing_count ? "Continue" : "Looks right",
  renderSecondary: ({ answers, set }) => {
    if (answers.__editing_count) return null;
    return (
      <button className="btn btn-secondary" onClick={() => set("__editing_count", true)}>Update count</button>
    );
  },
},

// v5: Q3 — Onboarding more soon?
{
  id: "Q2.onboard_more", section: 2, sectionName: "Portfolio & Channels", qIndex: 2, qTotal: 7,
  anchor: false, canvas: null,
  render: ({ answers, set }) => (
    <>
      <QMeta section={2} sectionName="Portfolio & Channels" qIndex={2} qTotal={7} />
      <h1 className="q-title">Are you about to onboard more listings soon?</h1>
      <div className="opt-list">
        <Option k="1" label="Yes" selected={answers.onboard_more === "yes"} onSelect={() => {
          if (answers.onboard_more === "no") set({ onboard_more: "yes", onboard_more_count: undefined });
          else set("onboard_more", "yes");
        }} />
        <Option k="2" label="No" selected={answers.onboard_more === "no"} onSelect={() => set({ onboard_more: "no", onboard_more_count: undefined })} />
      </div>
    </>
  ),
  valid: () => true,
  primaryLabel: () => "Continue",
},

// UX Patch 3.1 — onboard count promoted to its own standalone page + Stepper
{
  id: "Q2.onboard_count", section: 2, sectionName: "Portfolio & Channels", qIndex: 2, qTotal: 7,
  anchor: false, canvas: null,
  showIf: (a) => a.onboard_more === "yes",
  render: ({ answers, set }) => (
    <>
      <QMeta section={2} sectionName="Portfolio & Channels" qIndex={2} qTotal={7} />
      <h1 className="q-title">Roughly how many more listings?</h1>
      <p className="q-help">This helps us size your onboarding plan.</p>
      <Stepper value={answers.onboard_more_count ?? ""} min={1} step={1} placeholder="e.g. 3" controls width={150}
        ariaLabel="Number of additional listings"
        onChange={(v) => set("onboard_more_count", v === "" ? undefined : (parseInt(v) || undefined))} />
    </>
  ),
  valid: () => true,
  primaryLabel: () => "Continue",
},

// v5: Q1.2 — Channels page 1 of 2: "On today"
{
  id: "Q1.2", section: 2, sectionName: "Portfolio & Channels", qIndex: 3, qTotal: 7,
  anchor: false, canvas: null,
  render: (props) => <ChannelsV5Render {...props} />,
  valid: (a) => (a.channels_current ?? a.channels ?? []).length > 0,
  primaryLabel: () => "Continue",
},

// v5: Q1.2_add — Channels page 2 of 2: "To add with Guesty"
{
  id: "Q1.2_add", section: 2, sectionName: "Portfolio & Channels", qIndex: 3, qTotal: 7,
  anchor: false, canvas: null,
  render: (props) => <ChannelsAddV5Render {...props} />,
  valid: () => true,
  primaryLabel: () => "Continue",
},

// Q1.4 — Airbnb Connect, Step 1 (Pre-connect)
{
  id: "Q1.4", section: 2, sectionName: "Portfolio & Channels", qIndex: 4, qTotal: 7,
  anchor: false, canvas: null,
  showIf: (a) => (a.channels_current || a.channels || []).includes("airbnb"),
  subStep: 1, subTotal: 2,
  subStepLabel: "View-only connection",
  render: ({ answers, set, doOAuth, oauthState }) => {
    // While connecting — show only the working card, centered, nothing else
    if (oauthState === "working") {
      return (
        <div style={{
          minHeight: 360,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}>
          <div className="oauth-card oauth-working" style={{maxWidth: 440}}>
            <div className="spinner" style={{width:32, height:32, borderWidth:3}}></div>
            <div style={{fontSize:18, fontWeight:600, marginTop:4}}>Connecting to Airbnb…</div>
            <div style={{fontSize:14, color:"hsl(var(--gst-muted-foreground))", lineHeight:1.55, textAlign:"center"}}>
              Importing listings, reservations, and guest messages in view-only mode.
            </div>
          </div>
        </div>
      );
    }
    return (
      <>
        <QMeta section="2" sectionName="Portfolio & Channels" qIndex={4} qTotal={7} subStep={1} subTotal={2} />
        <BotAlert>
          <div>We only request view-only access — Guesty reads your listings but never changes them, messages guests, or accepts reservations on Airbnb's side.</div>
        </BotAlert>

        {/* Section A — header */}
        <div>
          <h1 className="q-title" style={{marginBottom:6}}>Airbnb listings to be imported</h1>
          <p className="q-help" style={{marginTop:0}}>A view-only connection will import data without making changes to your listings on Airbnb.</p>
        </div>
      </>
    );
  },
  valid: (a) => a.oauth_status === "success",
  primaryLabel: (a, oauth) => oauth === "working" ? "Connecting to Airbnb…" : "Pre-connect to Airbnb",
  primaryAction: "oauth", // wizard uses this to trigger OAuth
},

// Q1.4b — Airbnb Connect, Step 2 (Choose listings)
{
  id: "Q1.4b", section: 2, sectionName: "Portfolio & Channels", qIndex: 4, qTotal: 7,
  anchor: true, canvas: null,
  subStep: 2, subTotal: 2,
  subStepLabel: "Import listings",
  showIf: (a) => a.oauth_status === "success" && (a.channels_current || a.channels || []).includes("airbnb"),
  render: ({ answers, set }) => (
    <>
      <QMeta section="2" sectionName="Portfolio & Channels" qIndex={4} qTotal={7} subStep={2} subTotal={2} />
      <BotAlert>
        <div>Pick the listings you want to test Guesty with. You can always import the rest later.</div>
      </BotAlert>
      <h1 className="q-title">Choose listings to import</h1>
      <p className="q-help">Changes you make in Guesty won't sync to Airbnb until you fully connect the account and listings.</p>
      <ChooseListings answers={answers} set={set} />
    </>
  ),
  valid: (a) => (a.selected_listings ?? MOCK_LISTINGS).length > 0,
  primaryLabel: () => "Select listings",
  primaryDisabledTooltip: "Select at least one listing to continue.",
},

// Q1.AHA — Multi-Calendar AHA reveal (read-only preview after Airbnb sync)
{
  id: "Q1.AHA", section: 2, sectionName: "Portfolio & Channels", qIndex: 4, qTotal: 7,
  anchor: true, canvas: null,
  subStepLabel: "Airbnb is connected",
  fullWidth: true,                              // wizard renders this panel wider
  showIf: (a) => a.oauth_status === "success" && (a.channels_current || a.channels || []).includes("airbnb"),
  render: ({ answers }) => (
    <>
      <h1 className="q-title aha-title">Your Airbnb bookings are now on the calendar</h1>
      <p className="q-help aha-subtitle">See every reservation in one calendar.</p>
      {window.CalendarAhaPanel ? <window.CalendarAhaPanel logoFile={answers.logo_file} /> : null}
    </>
  ),
  valid: () => true,
  primaryLabel: () => "Continue setup",
},

// v5: Q5 — Go-live
{
  id: "Q1.5", section: 2, sectionName: "Portfolio & Channels", qIndex: 7, qTotal: 7,
  anchor: false, canvas: "aha",
  render: ({ answers, set }) => (
      <>
        <QMeta section={2} sectionName="Portfolio & Channels" qIndex={7} qTotal={7} />
        <BotAlert>
          <div>Your Airbnb data is in. Now we'll set up Guesty to match how you work.</div>
        </BotAlert>
        <h1 className="q-title">When do you want to go live with Guesty?</h1>
        <p className="q-help">This sets the pace for your onboarding calls — you can change it later.</p>
        <div className="opt-list">
          <Option k="1" label="Within 2 weeks" selected={answers.go_live === "asap"} onSelect={() => set({ go_live: "asap", go_live_date: undefined })} />
          <Option k="2" label="2–4 weeks" selected={answers.go_live === "2-4w"} onSelect={() => set({ go_live: "2-4w", go_live_date: undefined })} />
          <Option k="3" label="1–2 months" selected={answers.go_live === "1-2m"} onSelect={() => set({ go_live: "1-2m", go_live_date: undefined })} />
          <Option k="4" label="Specific deadline" selected={answers.go_live === "deadline"} onSelect={() => set("go_live", "deadline")} />
        </div>
      </>
  ),
  valid: (a) => !!a.go_live,
  primaryLabel: () => "Continue",
},

// UX Patch 3.3 — go-live "Specific deadline" date promoted to its own page
{
  id: "Q1.5_deadline", section: 2, sectionName: "Portfolio & Channels", qIndex: 7, qTotal: 7,
  anchor: false, canvas: null,
  showIf: (a) => a.go_live === "deadline",
  render: ({ answers, set }) => {
    const today = new Date().toISOString().slice(0, 10);
    const dateInvalid = answers.go_live_date && answers.go_live_date < today;
    return (
      <>
        <QMeta section={2} sectionName="Portfolio & Channels" qIndex={7} qTotal={7} />
        <h1 className="q-title">What's your target go-live date?</h1>
        <p className="q-help">Pick the date you want to be live in Guesty — you can change it later.</p>
        <input className="input" type="date" min={today} style={{ maxWidth: 220 }} value={answers.go_live_date || ""}
          onChange={e => set("go_live_date", e.target.value)} />
        {dateInvalid && <div style={{ fontSize: 12, color: "hsl(var(--gst-warning))", marginTop: 6 }}>Pick a date that's today or later.</div>}
      </>
    );
  },
  valid: (a) => {
    const today = new Date().toISOString().slice(0, 10);
    return !!a.go_live_date && a.go_live_date >= today;
  },
  primaryLabel: () => "Continue",
},

/* ============ Section 3 — Operations ============ */

// v5: Q6 — Cleaning
{
  id: "Q2.1", section: 3, sectionName: "Operations", qIndex: 1, qTotal: 4,
  anchor: false, canvas: null,
  render: ({ answers, set }) => {
    const editing = answers.__editing_cleaning;
    if (!editing && !answers.cleaning_system && SF_PREFILL.partner_cleaning) {
      set({ cleaning_system: "external", cleaning_provider: "turno" });
    }
    const showChip = !editing && SF_PREFILL.partner_cleaning && answers.cleaning_system === "external";
    return (
      <>
        <QMeta section={3} sectionName="Operations" qIndex={1} qTotal={4} />
        <h1 className="q-title">How do you manage cleaning today?</h1>
        <InlineBot>We'll match the rest of Guesty's settings to whatever you tell us here.</InlineBot>
        {showChip ? (
          <div style={{ display: "flex", alignItems: "center", gap: 12, padding: "14px 16px", border: "1.5px solid hsl(var(--gst-primary) / 0.3)", background: "hsl(var(--gst-muted) / 0.5)", borderRadius: 10, flexWrap: "wrap" }}>
            <div style={{ fontSize: 15, fontWeight: 600 }}>External provider · Turno</div>
            <SourceChip label="Pre-filled from your sales call. Looks right?" />
            <div style={{ flex: 1 }}></div>
            <button className="btn btn-secondary" onClick={() => set("__editing_cleaning", true)}>Change</button>
          </div>
        ) : (
          <div className="opt-list">
            <Option k="1" label="External provider (Breezeway, Turno, etc.)" selected={answers.cleaning_system === "external"} onSelect={() => set("cleaning_system", "external")} />
            <Option k="2" label="In current PMS" selected={answers.cleaning_system === "pms"} onSelect={() => set({ cleaning_system: "pms", cleaning_provider: undefined, cleaning_provider_other: undefined })} />
            <Option k="3" label="Other" selected={answers.cleaning_system === "other"} onSelect={() => set({ cleaning_system: "other", cleaning_provider: undefined, cleaning_provider_other: undefined })} />
          </div>
        )}
      </>
    );
  },
  valid: (a) => !!a.cleaning_system,
  primaryLabel: (a) => (a.__editing_cleaning || !SF_PREFILL.partner_cleaning) ? "Continue" : "Looks right",
},

// UX Patch 3.4 — cleaning provider promoted to its own big-box page + Other text
{
  id: "Q2.1_provider", section: 3, sectionName: "Operations", qIndex: 1, qTotal: 4,
  anchor: false, canvas: null,
  showIf: (a) => a.cleaning_system === "external",
  render: ({ answers, set }) => (
    <>
      <QMeta section={3} sectionName="Operations" qIndex={1} qTotal={4} />
      <h1 className="q-title">Which provider?</h1>
      <p className="q-help">We'll line up the right integration for your cleaning team.</p>
      <BigBoxSelect
        value={answers.cleaning_provider}
        onSelect={(id) => set("cleaning_provider", id)}
        options={[
          { id: "breezeway", label: "Breezeway" },
          { id: "turno", label: "Turno" },
          { id: "properly", label: "Properly" },
          { id: "maidthis", label: "MaidThis" },
          { id: "other", label: "Other" },
        ]}
      />
      {answers.cleaning_provider === "other" && (
        <textarea className="input" rows={3} style={{ marginTop: 14 }} placeholder="Tell us which provider you use"
          value={answers.cleaning_provider_other || ""} onChange={e => set("cleaning_provider_other", e.target.value)} />
      )}
    </>
  ),
  valid: () => true,
  primaryLabel: () => "Continue",
},

// Q2.4 — Turnover checklist
{
  id: "Q2.4", section: 3, sectionName: "Operations", qIndex: 2, qTotal: 4,
  anchor: false, canvas: null,
  render: ({ answers, set }) => (
    <>
      <QMeta section="3" sectionName="Operations" qIndex={2} qTotal={4} />
      <h1 className="q-title">Do you have a turnover checklist your cleaners follow?</h1>
      <div className="opt-list">
        <Option k="1" label="Yes — I'll upload it"          selected={answers.checklist_choice === "upload"} onSelect={() => set("checklist_choice", "upload")} />
        <Option k="2" label="Use Guesty's standard template" selected={answers.checklist_choice === "guesty"} onSelect={() => set("checklist_choice", "guesty")} />
        <Option k="3" label="Skip for now"                   selected={answers.checklist_choice === "skip"}   onSelect={() => set("checklist_choice", "skip")} />
      </div>
    </>
  ),
  valid: (a) => !!a.checklist_choice,
  primaryLabel: () => "Continue",
},

// UX Patch 3.5 — turnover checklist upload promoted to its own page
{
  id: "Q2.4_upload", section: 3, sectionName: "Operations", qIndex: 2, qTotal: 4,
  anchor: false, canvas: null,
  showIf: (a) => a.checklist_choice === "upload",
  render: ({ answers, set }) => (
    <>
      <QMeta section={3} sectionName="Operations" qIndex={2} qTotal={4} />
      <h1 className="q-title">Upload your turnover checklist</h1>
      <p className="q-help">We'll convert it into a Guesty task list your cleaners can follow.</p>
      <div className="upload-box">
        {answers.checklist_file ? (
          <>
            <div className="upload-title">{answers.checklist_file} · 2.1 MB</div>
            <div className="upload-sub">Uploaded. We'll convert it into a Guesty task list.</div>
            <div style={{display:"flex", gap:8, justifyContent:"center", marginTop:8}}>
              <button className="btn btn-ghost" onClick={() => set("checklist_file", "new-checklist.pdf")}>Replace</button>
              <button className="btn btn-ghost" onClick={() => set("checklist_file", null)}>Remove</button>
            </div>
          </>
        ) : (
          <>
            <div className="upload-title">Drag a file here, or select from your computer.</div>
            <div className="upload-sub">PDF, DOC, or DOCX. Up to 10 MB.</div>
            <button className="btn btn-secondary" onClick={() => set("checklist_file", "turnover-checklist.pdf")}>Upload checklist</button>
          </>
        )}
      </div>
    </>
  ),
  valid: () => true,
  skipLabel: "I'll upload it later",
  primaryLabel: () => "Continue",
},

// v5: Q8 — Cleaning timing
{
  id: "Q2.timing", section: 3, sectionName: "Operations", qIndex: 3, qTotal: 4,
  anchor: false, canvas: null,
  render: ({ answers, set }) => (
    <>
      <QMeta section={3} sectionName="Operations" qIndex={3} qTotal={4} />
      <h1 className="q-title">When does cleaning happen?</h1>
      <div className="opt-list">
        <Option k="1" label="Pre-arrival" selected={answers.cleaning_timing === "pre_arrival"} onSelect={() => set("cleaning_timing", "pre_arrival")} />
        <Option k="2" label="Pre-departure" selected={answers.cleaning_timing === "pre_departure"} onSelect={() => set("cleaning_timing", "pre_departure")} />
      </div>
    </>
  ),
  valid: () => true,
  primaryLabel: () => "Continue",
},

// v5: Q9 — Inspections
{
  id: "Q2.inspections", section: 3, sectionName: "Operations", qIndex: 4, qTotal: 4,
  anchor: false, canvas: null,
  render: ({ answers, set }) => (
    <>
      <QMeta section={3} sectionName="Operations" qIndex={4} qTotal={4} />
      <h1 className="q-title">Do you use professional inspections?</h1>
      <div className="opt-list">
        <Option k="1" label="Yes" selected={answers.inspections === "yes"} onSelect={() => set("inspections", "yes")} />
        <Option k="2" label="No" selected={answers.inspections === "no"} onSelect={() => set("inspections", "no")} />
      </div>
    </>
  ),
  valid: () => true,
  primaryLabel: () => "Continue",
},

/* ============ Section 4 — Financials ============ */

// v5: Q10 — Revenue recognition
{
  id: "Q3.1", section: 4, sectionName: "Financials", qIndex: 1, qTotal: 5,
  anchor: false, canvas: null,
  render: ({ answers, set }) => (
    <>
      <QMeta section={4} sectionName="Financials" qIndex={1} qTotal={5} />
      <BotAlert>
        <div>These choices shape how Guesty reports your earnings. Pick what matches your accountant's books.</div>
        <div>Guesty Pay / payment processing is handled later in onboarding, not here.</div>
      </BotAlert>
      <h1 className="q-title">When do you count revenue from a reservation?</h1>
      <div className="opt-list">
        <Option k="1" label="Check-in date" hint="Default — report for March counts reservations checking in during March." selected={answers.revenue_recognition === "checkin"} onSelect={() => set("revenue_recognition", "checkin")} />
        <Option k="2" label="Check-out date" hint="Counts reservations checking out during the month." selected={answers.revenue_recognition === "checkout"} onSelect={() => set("revenue_recognition", "checkout")} />
        <Option k="3" label="Calendar dates (nights occupied)" hint="Counts nights occupied during the month." selected={answers.revenue_recognition === "calendar"} onSelect={() => set("revenue_recognition", "calendar")} />
      </div>
    </>
  ),
  valid: (a) => !!a.revenue_recognition,
  primaryLabel: () => "Continue",
},

// Q3.2 — Non-refundable rates
{
  id: "Q3.2", section: 4, sectionName: "Financials", qIndex: 2, qTotal: 5,
  anchor: false, canvas: null,
  render: ({ answers, set }) => (
    <>
      <QMeta section="4" sectionName="Financials" qIndex={2} qTotal={7} />
      <h1 className="q-title">Do you offer non-refundable rates?</h1>
      {((answers.channels_current || []).includes("booking") || (answers.channels_to_add || []).includes("booking")) && (
        <p className="q-help">Booking.com supports non-refundable rate plans — we'll set one up for you.</p>
      )}
      <div className="opt-list">
        <Option k="1" label="Yes, on all listings"  selected={answers.nonrefundable === "all"} onSelect={() => set("nonrefundable", "all")} />
        <Option k="2" label="Yes, on some listings" selected={answers.nonrefundable === "some"} onSelect={() => set("nonrefundable", "some")} />
        <Option k="3" label="No"                     selected={answers.nonrefundable === "no"}  onSelect={() => set("nonrefundable", "no")} />
      </div>
    </>
  ),
  valid: (a) => !!a.nonrefundable,
  primaryLabel: () => "Continue",
},

// v5: Q12 — Payment timing
{
  id: "Q3.4", section: 4, sectionName: "Financials", qIndex: 3, qTotal: 5,
  anchor: false, canvas: null,
  render: ({ answers, set }) => (
    <>
      <QMeta section={4} sectionName="Financials" qIndex={3} qTotal={7} />
      <h1 className="q-title">When are guests charged?</h1>
      <div className="opt-list">
        <Option k="1" label="Full amount at booking confirmation" selected={answers.pay_timing === "full"} onSelect={() => set({ pay_timing: "full", pay_custom: undefined })} />
        <Option k="2" label="50% at confirmation, 50% at check-in" selected={answers.pay_timing === "50_50"} onSelect={() => set({ pay_timing: "50_50", pay_custom: undefined })} />
        <Option k="3" label="80% at confirmation, 20% at check-in" selected={answers.pay_timing === "80_20"} onSelect={() => set({ pay_timing: "80_20", pay_custom: undefined })} />
        <Option k="4" label="Other" selected={answers.pay_timing === "other"} onSelect={() => set("pay_timing", "other")} />
      </div>
    </>
  ),
  valid: (a) => !!a.pay_timing,
  primaryLabel: () => "Continue",
},

// UX Patch 3.6 — custom payment schedule promoted to its own page + Steppers
{
  id: "Q3.4_other", section: 4, sectionName: "Financials", qIndex: 3, qTotal: 5,
  anchor: false, canvas: null,
  showIf: (a) => a.pay_timing === "other",
  render: ({ answers, set }) => (
    <>
      <QMeta section={4} sectionName="Financials" qIndex={3} qTotal={5} />
      <h1 className="q-title">Set up your custom payment schedule</h1>
      <p className="q-help">Tell us your deposit and when the balance is due.</p>
      <div style={{ display: "flex", flexWrap: "wrap", gap: 16, alignItems: "flex-end", maxWidth: 520 }}>
        <div style={{ flex: "1 1 160px", minWidth: 140 }}>
          <label style={{ fontSize: 12, fontWeight: 600, display: "block", marginBottom: 6 }}>Deposit amount</label>
          <Stepper value={answers.pay_custom?.amount ?? ""} min={0} step={25} prefix="$" placeholder="250" ariaLabel="Deposit amount" width={160}
            onChange={(v) => set("pay_custom", { ...(answers.pay_custom || {}), amount: v === "" ? undefined : v })} />
        </div>
        <div style={{ flex: "1 1 200px", minWidth: 180 }}>
          <label style={{ fontSize: 12, fontWeight: 600, display: "block", marginBottom: 6 }}>Balance due (days before check-in)</label>
          <Stepper value={answers.pay_custom?.balance_days ?? ""} min={0} max={365} step={1} suffix="days" placeholder="14" ariaLabel="Balance due days before check-in" width={180}
            onChange={(v) => set("pay_custom", { ...(answers.pay_custom || {}), balance_days: v === "" ? undefined : parseInt(v) })} />
        </div>
      </div>
    </>
  ),
  valid: () => true,
  primaryLabel: () => "Continue",
},

// Q3.6 — Mandatory fees (50/50 layout per 2026-05-27 patch)
{
  id: "Q3.6", section: 4, sectionName: "Financials", qIndex: 4, qTotal: 5,
  anchor: false, canvas: null,
  render: ({ answers, set }) => (
    <>
      <QMeta section="4" sectionName="Financials" qIndex={4} qTotal={7} />
      <FeeBuilder answers={answers} set={set} />
    </>
  ),
  valid: (a) => {
    const fees = a.fees_list || [];
    if (a.__no_fees) return true;
    if (fees.length === 0) return true; // empty state lets user use skip link to advance
    // Block continue if any fee has invalid amount
    return fees.every(f => {
      if (f.amount === "" || f.amount === null || f.amount === undefined) return true;
      const n = parseFloat(f.amount);
      if (isNaN(n) || n <= 0) return false;
      if (f.unitType === "%" && n > 100) return false;
      return true;
    });
  },
  primaryLabel: () => "Continue",
  primaryDisabledTooltip: "Fix the highlighted fees before you continue.",
},

// v5: Q14 — Taxes
{
  id: "Q3.7", section: 4, sectionName: "Financials", qIndex: 5, qTotal: 5,
  anchor: false, canvas: null,
  render: ({ answers, set }) => {
    const taxes = normalizeTaxes(answers.taxes);
    const selectedIds = taxes.map((tx) => tx.type);
    const toggleType = (id) => {
      if (selectedIds.includes(id)) set("taxes", taxes.filter((x) => x.type !== id));
      else set("taxes", [...taxes, { type: id, rate: "", mode: "" }]);
    };
    return (
      <>
        <QMeta section={4} sectionName="Financials" qIndex={5} qTotal={5} />
        <h1 className="q-title">What taxes apply to your reservations?</h1>
        <p className="q-help">Select every tax type that applies. Set the rate and how it's charged on the right.</p>
        <div className="opt-list">
          {TAX_TYPE_DEFS.map((o) => (
            <CheckOpt key={o.id} label={o.label} selected={selectedIds.includes(o.id)} onToggle={() => toggleType(o.id)} />
          ))}
        </div>
      </>
    );
  },
  renderSecondary: ({ answers, set }) => {
    if (answers.__explain_taxes_open) return null;
    return (
      <button type="button" className="explain-cta" onClick={() => set("__explain_taxes_open", true)} aria-expanded="false">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
        <span>Explain taxes</span>
      </button>
    );
  },
  valid: (a) => {
    const taxes = a.taxes;
    if (!taxes || !taxes.length) return true;
    if (typeof taxes[0] === "string") return true;
    return taxes.every((tx) => {
      if (tx.mode === "unsure") return true;
      if (tx.mode !== "inclusive" && tx.mode !== "exclusive") return false;
      const n = parseFloat(tx.rate);
      return !isNaN(n) && n > 0 && n <= 100;
    });
  },
  primaryLabel: () => "Continue",
  primaryDisabledTooltip: "Add a rate for each selected tax.",
},

/* ============ Section 5 — Owners ============ */

// v5: Q15 — Owners gate
{
  id: "Q5.owners_gate", section: 5, sectionName: "Owners", qIndex: 1, qTotal: 3,
  anchor: false, canvas: null,
  render: ({ answers, set }) => (
    <>
      <QMeta section={5} sectionName="Owners" qIndex={1} qTotal={3} />
      <h1 className="q-title">Do you work with owners?</h1>
      <div className="opt-list">
        <Option k="1" label="Yes, all my listings have owners" selected={answers.owners_gate === "all"} onSelect={() => set({ owners_gate: "all", owner_listings: undefined })} />
        <Option k="2" label="Yes, some of my listings have owners" selected={answers.owners_gate === "some"} onSelect={() => set("owners_gate", "some")} />
        <Option k="3" label="No" selected={answers.owners_gate === "no"} onSelect={() => set({ owners_gate: "no", owner_listings: undefined, owners_csv: undefined, owners_count: undefined, owner_split_type: undefined, owner_split_breakdown: undefined })} />
      </div>
    </>
  ),
  valid: () => true,
  primaryLabel: () => "Continue",
},

// UX Patch 3.8 — owners "some" → standalone listing page (reuses the Airbnb ChooseListings table)
{
  id: "Q5.owners_listings", section: 5, sectionName: "Owners", qIndex: 1, qTotal: 3,
  anchor: false, canvas: null,
  fullWidth: true,
  showIf: (a) => a.owners_gate === "some",
  render: ({ answers, set }) => (
    <>
      <QMeta section={5} sectionName="Owners" qIndex={1} qTotal={3} />
      <h1 className="q-title">Which listings have owners?</h1>
      <p className="q-help">Pick the listings that are owned by someone you report to.</p>
      <ChooseListings answers={answers} set={set} valueKey="owner_listings" storeIds defaultAll={false} />
    </>
  ),
  valid: () => true,
  primaryLabel: () => "Continue",
},

// v5: Q16 — Owner records (Q7.2)
{
  id: "Q7.2", section: 5, sectionName: "Owners", qIndex: 2, qTotal: 3,
  anchor: false, canvas: null,
  showIf: (a) => a.owners_gate && a.owners_gate !== "no",
  render: ({ answers, set }) => (
    <>
      <QMeta section={5} sectionName="Owners" qIndex={2} qTotal={3} />
      <h1 className="q-title">Upload your owner records</h1>
      <p className="q-help">CSV with name, email, and listings owned — or add one by one. No invites are sent.</p>
      <button className="btn btn-ghost" style={{ alignSelf: "flex-start", fontSize: 12 }}>Download CSV template</button>
      <div className="upload-box">
        {answers.owners_csv ? (
          <>
            <div className="upload-title">{answers.owners_csv}</div>
            <div className="upload-sub">{answers.owners_count || 6} owners loaded</div>
          </>
        ) : (
          <>
            <div className="upload-title">Drag a CSV file here, or select from your computer.</div>
            <div className="upload-sub">CSV, up to 10 MB.</div>
            <button className="btn btn-secondary" onClick={() => { set("owners_csv", "owners.csv"); set("owners_count", 6); }}>Upload CSV</button>
          </>
        )}
      </div>
    </>
  ),
  valid: () => true,
  primaryLabel: () => "Continue",
  skipLabel: "I'll add owners later",
},

// v5: Q17 — Owner revenue split
{
  id: "Q5.owner_split", section: 5, sectionName: "Owners", qIndex: 3, qTotal: 3,
  anchor: false, canvas: null,
  showIf: (a) => a.owners_gate && a.owners_gate !== "no",
  render: ({ answers, set }) => (
    <>
      <QMeta section={5} sectionName="Owners" qIndex={3} qTotal={3} />
      <h1 className="q-title">Roughly how do you split revenue with owners?</h1>
      <div className="opt-list">
        <Option k="1" label="% commission" selected={answers.owner_split_type === "commission"} onSelect={() => set({ owner_split_type: "commission", owner_split_breakdown: undefined })} />
        <Option k="2" label="Fixed fee" selected={answers.owner_split_type === "fixed"} onSelect={() => set({ owner_split_type: "fixed", owner_split_breakdown: undefined })} />
        <Option k="3" label="Mixed" selected={answers.owner_split_type === "mixed"} onSelect={() => set("owner_split_type", "mixed")} />
      </div>
    </>
  ),
  valid: () => true,
  primaryLabel: () => "Continue",
},

// UX Patch 3.9 — owner split "Mixed" promoted to its own page + Steppers
{
  id: "Q5.owner_split_mixed", section: 5, sectionName: "Owners", qIndex: 3, qTotal: 3,
  anchor: false, canvas: null,
  showIf: (a) => a.owner_split_type === "mixed",
  render: ({ answers, set }) => (
    <>
      <QMeta section={5} sectionName="Owners" qIndex={3} qTotal={3} />
      <h1 className="q-title">How does your mixed split work?</h1>
      <p className="q-help">Roughly, for your mixed arrangements.</p>
      <div style={{ display: "flex", flexWrap: "wrap", gap: 16, alignItems: "flex-end", maxWidth: 520 }}>
        <div style={{ flex: "1 1 160px", minWidth: 140 }}>
          <label style={{ fontSize: 12, fontWeight: 600, display: "block", marginBottom: 6 }}>% to owner</label>
          <Stepper value={answers.owner_split_breakdown?.pct ?? ""} min={0} max={100} step={0.5} decimals suffix="%" ariaLabel="Percent to owner" width={160}
            onChange={(v) => set("owner_split_breakdown", { ...(answers.owner_split_breakdown || {}), pct: v === "" ? undefined : v })} />
        </div>
        <div style={{ flex: "1 1 160px", minWidth: 140 }}>
          <label style={{ fontSize: 12, fontWeight: 600, display: "block", marginBottom: 6 }}>Fixed fee</label>
          <Stepper value={answers.owner_split_breakdown?.flat ?? ""} min={0} step={25} prefix="$" ariaLabel="Fixed fee" width={160}
            onChange={(v) => set("owner_split_breakdown", { ...(answers.owner_split_breakdown || {}), flat: v === "" ? undefined : v })} />
        </div>
      </div>
    </>
  ),
  valid: () => true,
  primaryLabel: () => "Continue",
},

/* ============ Section 6 — Rate strategy ============ */

// v5: Q18 — Pricing tool
{
  id: "Q6.pricing_tool", section: 6, sectionName: "Rate strategy", qIndex: 1, qTotal: 2,
  anchor: false, canvas: null,
  render: ({ answers, set }) => (
    <>
      <QMeta section={6} sectionName="Rate strategy" qIndex={1} qTotal={2} />
      <h1 className="q-title">Are you using a pricing tool?</h1>
      <div className="opt-list">
        <Option k="1" label="Yes" selected={answers.pricing_tool === "yes"} onSelect={() => set({ pricing_tool: "yes", low_season_start: undefined, low_season_end: undefined, high_season_start: undefined, high_season_end: undefined })} />
        <Option k="2" label="No" selected={answers.pricing_tool === "no"} onSelect={() => set({ pricing_tool: "no", pricing_tool_name: undefined, low_season_start: undefined, low_season_end: undefined, high_season_start: undefined, high_season_end: undefined })} />
      </div>
    </>
  ),
  valid: () => true,
  primaryLabel: () => "Continue",
},

// UX Patch 3.10 — pricing tool "Yes" → standalone "Which one?" page
{
  id: "Q6.pricing_tool_name", section: 6, sectionName: "Rate strategy", qIndex: 1, qTotal: 2,
  anchor: false, canvas: null,
  showIf: (a) => a.pricing_tool === "yes",
  render: ({ answers, set }) => (
    <>
      <QMeta section={6} sectionName="Rate strategy" qIndex={1} qTotal={2} />
      <h1 className="q-title">Which pricing tool do you use?</h1>
      <p className="q-help">We'll note the integration so we don't double-manage pricing.</p>
      <input className="input" style={{ maxWidth: 320 }} value={answers.pricing_tool_name || ""}
        onChange={e => set("pricing_tool_name", e.target.value)} placeholder="e.g. PriceLabs" />
    </>
  ),
  valid: () => true,
  primaryLabel: () => "Continue",
},

// v5: Q19 — Season dates (Q7.3)
{
  id: "Q7.3", section: 6, sectionName: "Rate strategy", qIndex: 2, qTotal: 2,
  anchor: false, canvas: null,
  showIf: (a) => a.pricing_tool !== "yes",
  render: (props) => <SeasonDatesRender {...props} />,
  valid: () => true,
  primaryLabel: () => "Continue",
},

/* ============ Section 7 — Governance ============ */

// v5: Q20 — Decision owners
{
  id: "Q5.1", section: 7, sectionName: "Governance", qIndex: 1, qTotal: 2,
  anchor: false, canvas: null,
  render: ({ answers, set }) => (
    <>
      <QMeta section={7} sectionName="Governance" qIndex={1} qTotal={2} />
      <h1 className="q-title">Who makes the calls on Guesty settings?</h1>
      <InlineBot>Just you, or teammates helping set Guesty up?</InlineBot>
      <div className="opt-list">
        <Option k="1" label="Just me" selected={answers.owner_split === "solo"} onSelect={() => set("owner_split", "solo")} />
        <Option k="2" label="Me plus teammates" selected={answers.owner_split === "split"} onSelect={() => set("owner_split", "split")} />
      </div>
    </>
  ),
  valid: (a) => !!a.owner_split,
  primaryLabel: () => "Continue",
},

// Invite teammates (gated by Q20)
{
  id: "Q5.2", section: 7, sectionName: "Governance", qIndex: 2, qTotal: 2,
  showIf: (a) => a.owner_split === "split",
  anchor: false, canvas: null,
  render: ({ answers, set }) => {
    const rows = answers.teammate_rows ?? [{ email: "", role: "Admin — most settings, no billing" }];
    const update = (next) => {
      set("teammate_rows", next);
      set("teammates_count", next.filter(r => r.email).length);
    };
    return (
      <>
        <QMeta section={7} sectionName="Governance" qIndex={2} qTotal={2} />
        <h1 className="q-title">Invite anyone to help you set Guesty up?</h1>
        <p className="q-help">They'll get a link to join your account and pick up where you left off.</p>
        <div style={{display:"flex", flexDirection:"column", gap:8}}>
          {rows.map((r, i) => (
            <div key={i} className="fee-row">
              <input className="input" style={{flex:2}} placeholder="name@example.com" type="email"
                value={r.email} onChange={e => update(rows.map((x, j) => j === i ? { ...x, email: e.target.value } : x))} />
              <select className="input" style={{flex:1, maxWidth:240}}
                value={r.role} onChange={e => update(rows.map((x, j) => j === i ? { ...x, role: e.target.value } : x))}>
                <option>Account owner — full access</option>
                <option>Admin — most settings, no billing</option>
                <option>Operator — day-to-day operations only</option>
              </select>
              <button className="x" onClick={() => update(rows.filter((_, j) => j !== i))} aria-label="Remove teammate row">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M18 6L6 18M6 6l12 12"/></svg>
              </button>
            </div>
          ))}
          <button className="add-row" onClick={() => update([...rows, { email: "", role: "Admin — most settings, no billing" }])}>
            + Add another teammate
          </button>
        </div>
      </>
    );
  },
  valid: () => true,
  primaryLabel: (a) => (a.teammate_rows || []).some(r => r.email) ? "Send invitations" : "Skip for now",
},

/* ============ Section 8 — Focus & context ============ */

// Q6.1 — Focus topics
{
  id: "Q6.1", section: 8, sectionName: "Focus & context", qIndex: 1, qTotal: 2,
  anchor: false, canvas: null,
  render: ({ answers, set }) => {
    const topics = answers.focus_topics ?? [];
    const toggle = (t) => {
      if (topics.includes(t)) set("focus_topics", topics.filter(x => x !== t));
      else if (topics.length < 3) set("focus_topics", [...topics, t]);
    };

    const all = [
      {
        id: "Pricing strategy",
        icon: (
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
            <line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>
          </svg>
        ),
      },
      {
        id: "Channel mix",
        icon: (
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
            <rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/>
          </svg>
        ),
      },
      {
        id: "Guest messaging",
        icon: (
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
          </svg>
        ),
      },
      {
        id: "Cleaner workflows",
        icon: (
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
            <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/>
          </svg>
        ),
      },
      {
        id: "Accounting setup",
        icon: (
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/>
          </svg>
        ),
      },
      {
        id: "Owner reporting",
        icon: (
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
            <line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/><line x1="2" y1="20" x2="22" y2="20"/>
          </svg>
        ),
      },
      {
        id: "Booking website",
        icon: (
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
            <circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>
          </svg>
        ),
      },
      {
        id: "Reviews and reputation",
        icon: (
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
            <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
          </svg>
        ),
      },
    ];

    return (
      <>
        <QMeta section={8} sectionName="Focus & context" qIndex={1} qTotal={2} />
        <h1 className="q-title">What do you want to dig into on your first onboarding call?</h1>
        <InlineBot>Pick up to three. Your CSM will lead with these.</InlineBot>
        <div style={{display:"grid", gridTemplateColumns:"repeat(2, 1fr)", gap:12}}>
          {all.map(t => {
            const sel = topics.includes(t.id);
            const atLimit = topics.length >= 3 && !sel;
            return (
              <button
                key={t.id}
                type="button"
                onClick={() => toggle(t.id)}
                disabled={atLimit}
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: 14,
                  padding: "16px 18px",
                  border: "1.5px solid " + (sel ? "hsl(var(--gst-primary))" : "hsl(var(--gst-border))"),
                  borderRadius: 10,
                  background: sel ? "hsl(var(--gst-primary) / 0.06)" : "white",
                  cursor: atLimit ? "not-allowed" : "pointer",
                  opacity: atLimit ? 0.4 : 1,
                  textAlign: "left",
                  fontFamily: "inherit",
                  transition: "all 140ms",
                  boxShadow: sel ? "0 0 0 3px hsl(var(--gst-primary) / 0.12)" : "none",
                }}
              >
                <span style={{
                  color: sel ? "hsl(var(--gst-primary))" : "hsl(var(--gst-muted-foreground))",
                  flexShrink: 0,
                  transition: "color 140ms",
                }}>{t.icon}</span>
                <span style={{
                  fontSize: 14,
                  fontWeight: sel ? 600 : 500,
                  color: sel ? "hsl(var(--gst-primary))" : "hsl(var(--gst-foreground))",
                  lineHeight: 1.3,
                }}>{t.id}</span>
                {sel && (
                  <span style={{
                    marginLeft: "auto",
                    width: 18, height: 18,
                    borderRadius: "50%",
                    background: "hsl(var(--gst-primary))",
                    display: "flex", alignItems: "center", justifyContent: "center",
                    flexShrink: 0,
                  }}>
                    <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="3.5" strokeLinecap="round" strokeLinejoin="round">
                      <polyline points="20 6 9 17 4 12"/>
                    </svg>
                  </span>
                )}
              </button>
            );
          })}
        </div>
        {topics.length >= 3 && (
          <div style={{fontSize:13, color:"hsl(var(--gst-muted-foreground))", fontWeight:500}}>
            3 of 3 selected. Remove one to add another.
          </div>
        )}
      </>
    );
  },
  valid: () => true,
  primaryLabel: () => "Continue",
},

// Q6.2 — Biggest pain
{
  id: "Q6.2", section: 8, sectionName: "Focus & context", qIndex: 2, qTotal: 2,
  anchor: false, canvas: null,
  render: ({ answers, set }) => {
    const field = {
      label: "Biggest thing slowing you down right now",
      hint: "Free-text pain point from a property manager onboarding to Guesty. Map to the focus topics that best fit so the CSM can prep.",
      options: [
        "Pricing strategy", "Channel mix", "Guest messaging", "Cleaner workflows",
        "Accounting setup", "Owner reporting", "Booking website", "Reviews and reputation",
      ],
    };
    return (
      <>
        <QMeta section={8} sectionName="Focus & context" qIndex={2} qTotal={2} />
        <h1 className="q-title">In one sentence, what's the biggest thing slowing you down right now?</h1>
        <p className="q-help">Your CSM reads this before your call. The more specific, the better — I'll tag it to the right topics as you write.</p>
        <NormalizeField
          answers={answers}
          set={set}
          textKey="pain"
          resultKey="pain_normalized"
          field={field}
          placeholder="e.g. I'm losing hours every week chasing cleaners after late check-outs."
        />
      </>
    );
  },
  valid: () => true,
  primaryLabel: () => "Continue",
},

]; }

window.makeScreens = makeScreens;
window.BotAlert = BotAlert;
window.InlineBot = InlineBot;
// Exposed so wizard.jsx (separate IIFE) can reuse the pick-one option control
// on the homepage question carousel.
window.Option = Option;
window.CheckOpt = CheckOpt;
window.CanvasAHA = CanvasAHA;
window.CanvasMilestone = CanvasMilestone;
window.CanvasReview = CanvasReview;
window.CanvasVideo = CanvasVideo;
window.CanvasFeeBuilder = CanvasFeeBuilder;
window.CanvasTaxesExplain = CanvasTaxesExplain;

/* ===================== S0 Welcome — illustration panel (right canvas) ===================== */

function WelcomeIllustration() {
  return (
    <div className="welcome-illustration-panel">
      <div className="welcome-illustration-inner">
        <SkeletonImg
          src="assets/welcome-illustration.svg"
          alt=""
          aria-hidden="true"
          className="welcome-illustration-img"
          wrapStyle={{display:"block", width:"100%", height:"100%", maxWidth:640, maxHeight:720, borderRadius:16}}
        />
      </div>
    </div>
  );
}

window.WelcomeIllustration = WelcomeIllustration;

})();
