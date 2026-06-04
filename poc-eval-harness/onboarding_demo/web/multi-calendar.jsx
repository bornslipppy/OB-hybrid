// multi-calendar.jsx — AHA-moment Multi-Calendar preview, ported from
// /Guesty-Pro-main 3/public/product-preview.jsx (CalendarProductPreview).
// Wrapped in IIFE so its top-level const declarations don't collide with the
// rest of the bundled React files in this prototype.
(function () {
  const { useState, useEffect, useRef, useMemo, useCallback } = React;
  const SkeletonImg = window.SkeletonImg;

  /* ===================== Visual config ===================== */
  const MC_CFG = {
    LISTING_COL: 200,
    DAY_W: 56,
    ROW_H: 56,
    HEADER_H: 40,
    MONTH_H: 26,
    CELL_BORDER: '#e5e7eb',
    CELL_BG: '#ffffff',
    RESERVATION_BG: '#54a18a',
    RESERVATION_FG: '#ffffff',
    BLOCK_BG: '#cbd3de',
    BLOCK_FG: '#1f2937',
    TODAY_LINE: '#e84393',
    TODAY_TINT: 'rgba(232, 67, 147, 0.06)',
  };

  const MC_DAY_COL_HOVER_TODAY = 'rgba(232, 67, 147, 0.12)';
  const MC_DAY_COL_HOVER_PLAIN = 'hsl(220 14% 96%)';

  const MC_WEEKDAYS = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
  const MC_MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  const MC_TODAY_INDEX = 3;
  const MC_DAY_COUNT_MIN = 14;
  const MC_DAY_COUNT_MAX = 52;
  const MC_DAY_COUNT_EXTENDED = 365;

  function buildMcDays(dayCount) {
    return Array.from({ length: dayCount }, (_, i) => {
      const d = new Date();
      d.setHours(0, 0, 0, 0);
      d.setDate(d.getDate() + (i - MC_TODAY_INDEX));
      return {
        weekday: MC_WEEKDAYS[d.getDay()],
        day: d.getDate(),
        month: `${MC_MONTHS[d.getMonth()]} ${d.getFullYear()}`,
      };
    });
  }

  function mcDayColCellBackground(colIndex, hoveredDayCol) {
    const isToday = colIndex === MC_TODAY_INDEX;
    const base = isToday ? MC_CFG.TODAY_TINT : MC_CFG.CELL_BG;
    if (hoveredDayCol === colIndex) {
      return isToday ? MC_DAY_COL_HOVER_TODAY : MC_DAY_COL_HOVER_PLAIN;
    }
    return base;
  }

  function mcBarPointerToColumn(bar, offsetX) {
    const spanDays = Math.max(1, bar.end - bar.start);
    let idx = Math.floor(offsetX / MC_CFG.DAY_W);
    idx = Math.max(0, Math.min(spanDays - 1, idx));
    return bar.start + idx;
  }

  /* ===================== Scroll-hint helpers ===================== */
  const easeInOutQuad = (t) => (t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t);

  function animateScrollTop(el, target, duration, done) {
    const start = el.scrollTop;
    const delta = target - start;
    if (duration <= 0 || Math.abs(delta) < 0.5) { el.scrollTop = target; done && done(); return; }
    const t0 = performance.now();
    const step = (t1) => {
      const u = Math.min(1, (t1 - t0) / duration);
      el.scrollTop = start + delta * easeInOutQuad(u);
      if (u < 1) requestAnimationFrame(step);
      else { el.scrollTop = target; done && done(); }
    };
    requestAnimationFrame(step);
  }

  function runCalendarHint(el, mark) {
    const maxY = el.scrollHeight - el.clientHeight;
    if (maxY >= 32) {
      const down = Math.min(110, maxY);
      animateScrollTop(el, down, 700, () => setTimeout(() => animateScrollTop(el, 0, 500, mark), 280));
      return;
    }
    mark();
  }

  function useOneTimeHint(key, scrollRef, delayMs, runHint) {
    const runHintRef = useRef(runHint);
    runHintRef.current = runHint;
    useEffect(() => {
      const el = scrollRef.current;
      if (!el) return;
      let reduced = false;
      try { reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches; } catch {}
      if (reduced) return;
      let seen = false;
      try { seen = !!sessionStorage.getItem('mc-hint-' + key); } catch {}
      if (seen) return;
      let cancelled = false;
      const mark = () => { try { sessionStorage.setItem('mc-hint-' + key, '1'); } catch {} };
      const cancel = () => { if (cancelled) return; cancelled = true; mark(); };
      el.addEventListener('wheel', cancel, { passive: true });
      el.addEventListener('pointerdown', cancel, { once: true });
      let rafId = 0;
      const tid = window.setTimeout(() => {
        if (cancelled) return;
        let frames = 0;
        const tryHint = () => {
          if (cancelled) return;
          if (el.scrollHeight - el.clientHeight >= 12) { runHintRef.current(el, mark); return; }
          if (++frames >= 90) { mark(); return; }
          rafId = requestAnimationFrame(tryHint);
        };
        tryHint();
      }, delayMs);
      return () => {
        window.clearTimeout(tid);
        if (rafId) cancelAnimationFrame(rafId);
        el.removeEventListener('wheel', cancel);
      };
    // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [key, delayMs]);
  }

  /* ===================== Demo data (Airbnb only, per AHA copy) ===================== */
  const MC_LISTINGS = [
    { id: 1, name: 'Seaside Loft',         img: 'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=480&q=70' },
    { id: 2, name: 'Garden Studio',        img: 'https://images.unsplash.com/photo-1493809842364-78817add7ffb?w=480&q=70' },
    { id: 3, name: 'City View Apartment',  img: 'https://images.unsplash.com/photo-1505691938895-1758d7feb511?w=480&q=70' },
    { id: 4, name: 'Beachfront Suite',     img: 'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=480&q=70' },
    { id: 5, name: 'Magnolia Suites',      img: 'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=480&q=70' },
    { id: 6, name: 'Urban Balcony Apt',    img: 'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=480&q=70' },
    { id: 7, name: 'Rooftop Haven',        img: 'https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=480&q=70' },
    { id: 8, name: 'Urban Nest',           img: 'https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?w=480&q=70' },
    { id: 9, name: 'Sunset Villa',         img: 'https://images.unsplash.com/photo-1600585154526-990dced4db0d?w=480&q=70' },
  ];

  // Airbnb reservation tapes (green) + Booking.com and Expedia (grey — subtle)
  const MC_BARS = [
    { id: 1, listingId: 1, channel: 'airbnb',  guest: 'Emma R.',      start: 2,  end: 5  },
    { id: 2, listingId: 3, channel: 'airbnb',  guest: 'Nina S.',      start: 0,  end: 3  },
    { id: 3, listingId: 5, channel: 'airbnb',  guest: 'Daniel K.',    start: 1,  end: 6  },
    { id: 4, listingId: 6, channel: 'airbnb',  guest: 'Omar L.',      start: 9,  end: 13 },
    { id: 5, listingId: 7, channel: 'airbnb',  guest: 'Peter Veelan', start: 5,  end: 9  },
    { id: 6, listingId: 9, channel: 'airbnb',  guest: 'Dana Shapiro', start: 11, end: 16 },
    // Subtle grey — Booking.com
    { id: 7,  listingId: 2, channel: 'booking', guest: 'R. Morin',     start: 3,  end: 7  },
    { id: 8,  listingId: 4, channel: 'booking', guest: 'T. Walsh',     start: 8,  end: 12 },
    // Subtle grey — Expedia
    { id: 9,  listingId: 8, channel: 'expedia', guest: 'L. Park',      start: 2,  end: 5  },
    { id: 10, listingId: 1, channel: 'expedia', guest: 'M. Chen',      start: 8,  end: 11 },
    { id: 11, listingId: 3, channel: 'expedia', guest: 'S. Brandt',    start: 6,  end: 9  },
    { id: 12, listingId: 7, channel: 'expedia', guest: 'A. Russo',     start: 12, end: 16 },
  ];

  /* ===================== Icons (inline Lucide SVGs) ===================== */
  // Airbnb Bélo — extracted path from assets/channel-airbnb.svg (15×17 viewBox).
  const AIRBNB_BELO_D = "M13.9475098,13.0747528c-0.1125183,0.8399963-0.678772,1.5674973-1.4700012,1.8912506c-0.3887634,0.1612473-0.8087463,0.2099991-1.2287598,0.1612473c-0.4037476-0.0487518-0.8087463-0.1787491-1.2287598-0.4199982c-0.5812378-0.3237534-1.1624756-0.8250046-1.8412476-1.5687561c1.0662537-1.3087463,1.7124939-2.5049973,1.9550171-3.5712433c0.113739-0.5012512,0.1300049-0.9524994,0.0812378-1.3737564c-0.0650024-0.4037476-0.2099915-0.7749939-0.4362488-1.0987473C9.2774963,6.3672485,8.4362488,5.9472504,7.5,5.9472504c-0.9375,0-1.7787476,0.4362488-2.2787476,1.1474991C4.9949951,7.4185028,4.8487549,7.7897491,4.7850037,8.1934967c-0.0650024,0.421257-0.0487671,0.8887558,0.0799866,1.3737564c0.2425232,1.066246,0.9049988,2.2787476,1.9550171,3.5874939c-0.6612549,0.7437515-1.2600098,1.2450027-1.8412476,1.5675049C4.5574951,14.9660034,4.1549988,15.0947495,3.75,15.1422501c-0.4362488,0.0487518-0.8562622-0.0149994-1.2287598-0.1612473c-0.7912292-0.3225021-1.3574829-1.0500031-1.4700012-1.8899994c-0.0474854-0.4050064-0.0162354-0.808754,0.1462708-1.2612534c0.0474854-0.1612473,0.1287537-0.3225021,0.2099915-0.5162506c0.1124878-0.2587509,0.2424927-0.5337524,0.3712463-0.8087463l0.0162659-0.0325012C2.9100037,8.0647507,4.105011,5.6084976,5.3500061,3.2160034L5.3987427,3.119751c0.1300049-0.2425003,0.2587585-0.5012512,0.3875122-0.7437515C5.9162598,2.1172485,6.0612488,1.8747482,6.238739,1.6647491c0.3399963-0.3874969,0.792511-0.597496,1.2937622-0.597496s0.9524841,0.2099991,1.292511,0.597496c0.1774902,0.2112503,0.3224792,0.4524994,0.4524841,0.7112503C9.40625,2.6184998,9.5362549,2.8772507,9.6650085,3.119751l0.0487366,0.0962524c1.2250061,2.4024963,2.4049988,4.8262482,3.5387573,7.2737503v0.0149994c0.1300049,0.2587433,0.2424927,0.5499954,0.3724976,0.8087463c0.0799866,0.1937485,0.1612549,0.3550034,0.2099915,0.5162506C13.9637451,12.2497482,14.0125122,12.6535034,13.9475098,13.0747528 M7.5,12.3147507c-0.8724976-1.0987473-1.4387512-2.1324997-1.6325073-3.0062485C5.7862549,8.9372482,5.769989,8.6147537,5.8187561,8.3235016C5.8512573,8.0647507,5.948761,7.838501,6.0775146,7.6447525C6.3850098,7.2085037,6.9012451,6.9335022,7.5,6.9335022c0.5975037,0,1.1312561,0.2574997,1.4212646,0.7112503C9.051239,7.838501,9.1487427,8.0647507,9.1812439,8.3235016c0.0475159,0.2912521,0.03125,0.6299973-0.0487366,0.9850006C8.9375,10.1660004,8.3724976,11.1997528,7.5,12.3147507 M14.7875061,11.4747467c-0.0800171-0.1949997-0.1612549-0.4049988-0.2412415-0.5824966c-0.1300049-0.2912521-0.2600098-0.5650024-0.3725281-0.8237534l-0.0162354-0.016243c-1.1149902-2.4237518-2.3112488-4.8800049-3.5712585-7.3050003L10.5375061,2.651001c-0.1325073-0.2525024-0.2625122-0.5049973-0.3875122-0.7600021C9.988739,1.5997467,9.8275146,1.2935028,9.5687561,1.0022507C9.051239,0.3560028,8.3074951-0.0002518,7.5162354-0.0002518c-0.8087463,0-1.5362244,0.3562546-2.0687256,0.9700012C5.2049866,1.2597504,5.0274963,1.5672531,4.8649902,1.8584976c-0.125,0.2550049-0.2550049,0.5087509-0.3874817,0.7600021L4.4299927,2.7147522c-1.2449951,2.4249954-2.457489,4.8812485-3.5724792,7.3050003l-0.0162659,0.0325012c-0.1124878,0.2587433-0.2424927,0.5337448-0.3712463,0.8237457c-0.0812378,0.1787491-0.1612549,0.371254-0.2424927,0.5812531c-0.210022,0.5987473-0.2749939,1.1650009-0.1937561,1.7462463c0.1774902,1.2112503,0.9862366,2.2300034,2.1012573,2.6825027c0.4199829,0.1787491,0.8562317,0.2587509,1.3087463,0.2587509c0.1287537,0,0.2912292-0.0162506,0.4199829-0.0325012c0.5337524-0.0650024,1.0825195-0.2425003,1.616272-0.5500031c0.6624756-0.3712463,1.2924805-0.9037476,2.0037537-1.6800003c0.7112427,0.7762527,1.3574829,1.308754,2.0037231,1.6800003c0.5337524,0.3075027,1.0825195,0.4850006,1.616272,0.5500031c0.1300049,0.0162506,0.2912292,0.0325012,0.4212341,0.0325012c0.4512634,0,0.9037476-0.0800018,1.3074951-0.2587509c1.1325073-0.4524994,1.9237671-1.4862518,2.1012573-2.6825027C15.0625,12.6372528,14.9974976,12.0722504,14.7875061,11.4747467";

  const IconAirbnb = ({ size = 14 }) => (
    <svg width={size} height={size} viewBox="0 0 15 17" fill="currentColor" aria-hidden="true">
      <path d={AIRBNB_BELO_D} />
    </svg>
  );

  const IconSearch = ({ size = 12, color = '#9ca3af' }) => (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
  );

  const IconMoon = ({ size = 9 }) => (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
  );

  const IconCalendar = ({ size = 16 }) => (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
  );

  /* ===================== Channel chip ===================== */
  function MultiCalendarChannelChip({ channel, size = 20 }) {
    if (channel === 'booking') {
      return (
        <span style={{
          width: size, height: size, borderRadius: '50%',
          background: 'white',
          display: 'inline-flex', alignItems: 'center', justifyContent: 'center',
          flexShrink: 0, overflow: 'hidden',
        }} aria-label="Booking.com">
          <SkeletonImg
            src="assets/channel-booking-logo.svg"
            alt=""
            style={{ width: size - 8, height: size - 8, objectFit: 'contain', display: 'block' }}
            wrapStyle={{ display: 'inline-block', width: size - 8, height: size - 8, lineHeight: 0, borderRadius: 2 }}
          />
        </span>
      );
    }
    if (channel === 'expedia') {
      return (
        <span style={{
          width: size, height: size, borderRadius: '50%',
          background: 'white',
          display: 'inline-flex', alignItems: 'center', justifyContent: 'center',
          flexShrink: 0, overflow: 'hidden',
        }} aria-label="Expedia">
          <SkeletonImg
            src="assets/channel-expedia-logo.svg"
            alt=""
            style={{ width: size - 4, height: size - 4, objectFit: 'contain', display: 'block' }}
            wrapStyle={{ display: 'inline-block', width: size - 4, height: size - 4, lineHeight: 0, borderRadius: 2 }}
          />
        </span>
      );
    }
    return (
      <span style={{
        width: size, height: size, borderRadius: '50%',
        background: 'white', color: '#FF5A5F',
        display: 'inline-flex', alignItems: 'center', justifyContent: 'center',
        flexShrink: 0,
      }} aria-label="Airbnb">
        <IconAirbnb size={size - 6} />
      </span>
    );
  }

  /* ===================== Reservation bar ===================== */
  function MultiCalendarBar({ bar, onDayColEnter, onDayColLeave }) {
    const isAirbnb = bar.channel === 'airbnb';
    const bg = isAirbnb ? MC_CFG.RESERVATION_BG : 'linear-gradient(to right, rgba(255,255,255,1) 0%, rgba(255,255,255,0.5) 100%)';
    const fg = isAirbnb ? MC_CFG.RESERVATION_FG : '#9ca3af';
    const barBorder = isAirbnb ? 'none' : '1.5px dashed #d1d5db';
    const [visible, setVisible] = useState(false);
    const [tooltipPos, setTooltipPos] = useState(null);
    useEffect(() => {
      const t = setTimeout(() => setVisible(true), bar.id * 90);
      return () => clearTimeout(t);
    }, [bar.id]);
    const left = bar.start * MC_CFG.DAY_W + MC_CFG.DAY_W * 0.5;
    const width = (bar.end - bar.start) * MC_CFG.DAY_W;
    const lastColRef = useRef(bar.start);

    const syncColFromPointer = (e) => {
      const el = e.currentTarget;
      const ox = e.clientX - el.getBoundingClientRect().left;
      const col = mcBarPointerToColumn(bar, ox);
      lastColRef.current = col;
      onDayColEnter(col);
    };

    const handleMouseEnter = (e) => {
      e.currentTarget.style.filter = 'brightness(0.92)';
      syncColFromPointer(e);
      if (!isAirbnb) {
        const rect = e.currentTarget.getBoundingClientRect();
        setTooltipPos({ x: rect.left + rect.width / 2, y: rect.top });
      }
    };

    const handleMouseLeave = (e) => {
      e.currentTarget.style.filter = '';
      onDayColLeave(lastColRef.current, e);
      setTooltipPos(null);
    };

    return (
      <div
        onMouseEnter={handleMouseEnter}
        onMouseMove={syncColFromPointer}
        onMouseLeave={handleMouseLeave}
        style={{
          position: 'absolute',
          top: 10,
          left,
          width,
          height: MC_CFG.ROW_H - 20,
          background: bg,
          color: fg,
          border: barBorder,
          borderRadius: 6,
          display: 'flex',
          alignItems: 'center',
          gap: 6,
          padding: '0 12px 0 4px',
          fontSize: 12.5,
          fontWeight: 500,
          overflow: 'visible',
          whiteSpace: 'nowrap',
          zIndex: 1,
          boxShadow: '0 1px 0 rgba(0,0,0,0.04)',
          cursor: 'pointer',
          opacity: visible ? 1 : 0,
          transition: 'opacity 320ms ease, filter 150ms ease',
        }}>
        {/* Tooltip rendered into document.body so it escapes the overflow:auto scroll container */}
        {!isAirbnb && tooltipPos && ReactDOM.createPortal(
          <div role="tooltip" style={{
            position: 'fixed',
            top: tooltipPos.y - 8,
            left: tooltipPos.x,
            transform: 'translateX(-50%) translateY(-100%)',
            background: 'hsl(215 28% 17%)',
            color: 'white',
            fontSize: 12,
            fontWeight: 500,
            padding: '5px 10px',
            borderRadius: 6,
            whiteSpace: 'nowrap',
            boxShadow: '0 2px 8px rgba(0,0,0,0.18)',
            zIndex: 9999,
            pointerEvents: 'none',
            lineHeight: 1.4,
          }}>
            Connect to Guesty after setup
            <div style={{
              position: 'absolute',
              top: '100%',
              left: '50%',
              transform: 'translateX(-50%)',
              width: 0, height: 0,
              borderLeft: '5px solid transparent',
              borderRight: '5px solid transparent',
              borderTop: '5px solid hsl(215 28% 17%)',
            }} />
          </div>,
          document.body
        )}
        <div style={{ display: 'flex', alignItems: 'center', gap: 6, overflow: 'hidden' }}>
          <MultiCalendarChannelChip channel={bar.channel} size={22} />
          <span style={{ overflow: 'hidden', textOverflow: 'ellipsis' }}>{bar.guest}</span>
        </div>
      </div>
    );
  }

  /* ===================== Row ===================== */
  function MultiCalendarRow({ listing, bars, listingColW, hoveredDayCol, onDayColEnter, onDayColLeave, days }) {
    return (
      <div style={{ position: 'relative', height: MC_CFG.ROW_H, display: 'flex' }}>
        <div
          onMouseEnter={(e) => { e.currentTarget.style.background = 'hsl(220 14% 96%)'; }}
          onMouseLeave={(e) => { e.currentTarget.style.background = 'white'; }}
          style={{
            position: 'sticky',
            left: 0,
            flexShrink: 0,
            width: listingColW,
            height: MC_CFG.ROW_H,
            background: 'white',
            borderRight: `1px solid ${MC_CFG.CELL_BORDER}`,
            borderBottom: `1px solid ${MC_CFG.CELL_BORDER}`,
            display: 'flex',
            alignItems: 'center',
            gap: 10,
            padding: '0 12px',
            zIndex: 3,
            cursor: 'pointer',
            transition: 'background 150ms',
          }}>
          <img
            src={listing.img}
            alt=""
            style={{ width: 32, height: 32, borderRadius: 6, objectFit: 'cover', flexShrink: 0 }}
          />
          <span style={{
            fontSize: 13,
            fontWeight: 500,
            color: '#1f2937',
            overflow: 'hidden',
            textOverflow: 'ellipsis',
            whiteSpace: 'nowrap',
          }}>{listing.name}</span>
        </div>
        <div style={{ position: 'relative', display: 'flex', flex: 1 }}>
          {days.map((d, i) => (
            <div
              key={i}
              data-mc-day-col={i}
              onMouseEnter={() => onDayColEnter(i)}
              onMouseLeave={(e) => onDayColLeave(i, e)}
              style={{
                flexShrink: 0,
                width: MC_CFG.DAY_W,
                height: MC_CFG.ROW_H,
                borderRight: i < days.length - 1 ? `1px solid ${MC_CFG.CELL_BORDER}` : 'none',
                borderBottom: `1px solid ${MC_CFG.CELL_BORDER}`,
                background: mcDayColCellBackground(i, hoveredDayCol),
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: '#9ca3af',
                cursor: 'pointer',
                transition: 'background 150ms',
              }}>
              <span style={{ fontSize: 11, fontWeight: 500 }}>$90</span>
            </div>
          ))}
          {bars.map(bar => (
            <MultiCalendarBar
              key={bar.id}
              bar={bar}
              onDayColEnter={onDayColEnter}
              onDayColLeave={onDayColLeave}
            />
          ))}
        </div>
      </div>
    );
  }

  /* ===================== Header ===================== */
  function MultiCalendarHeader({ listingColW, hoveredDayCol, onDayColEnter, onDayColLeave, days }) {
    const monthSpans = [];
    days.forEach((d, i) => {
      const last = monthSpans[monthSpans.length - 1];
      if (last && last.month === d.month) last.length += 1;
      else monthSpans.push({ month: d.month, length: 1, start: i });
    });

    const totalHeaderH = MC_CFG.MONTH_H + MC_CFG.HEADER_H;

    return (
      <div style={{ position: 'sticky', top: 0, zIndex: 4, background: 'white', display: 'flex', borderBottom: `1px solid ${MC_CFG.CELL_BORDER}` }}>
        <div style={{
          position: 'sticky', left: 0,
          flexShrink: 0,
          width: listingColW,
          height: totalHeaderH,
          background: 'white',
          borderRight: `1px solid ${MC_CFG.CELL_BORDER}`,
          zIndex: 1,
          display: 'flex',
          alignItems: 'center',
          padding: '0 10px',
          userSelect: 'none',
        }}>
          <div
            onMouseEnter={(e) => { e.currentTarget.style.background = 'hsl(220 14% 90%)'; }}
            onMouseLeave={(e) => { e.currentTarget.style.background = '#f3f4f6'; }}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: 6,
              background: '#f3f4f6',
              borderRadius: 999,
              padding: '6px 12px',
              width: '100%',
              cursor: 'pointer',
              transition: 'background 150ms',
            }}>
            <IconSearch size={13} />
            <span style={{ fontSize: 12, color: '#9ca3af', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
              Search
            </span>
          </div>
        </div>
        <div style={{ display: 'flex', flexDirection: 'column', flex: 1 }}>
          <div style={{ display: 'flex', height: MC_CFG.MONTH_H, borderBottom: `1px solid ${MC_CFG.CELL_BORDER}` }}>
            {monthSpans.map(span => (
              <div
                key={span.start}
                style={{
                  flexShrink: 0,
                  width: span.length * MC_CFG.DAY_W,
                  fontSize: 12,
                  fontWeight: 500,
                  color: '#6b7280',
                  display: 'flex',
                  alignItems: 'center',
                  padding: '0 10px',
                  borderRight: `1px solid ${MC_CFG.CELL_BORDER}`,
                }}
              >
                {span.month}
              </div>
            ))}
          </div>
          <div style={{ display: 'flex', height: MC_CFG.HEADER_H }}>
            {days.map((d, i) => {
              const isToday = i === MC_TODAY_INDEX;
              return (
                <div
                  key={i}
                  data-mc-day-col={i}
                  onMouseEnter={() => onDayColEnter(i)}
                  onMouseLeave={(e) => onDayColLeave(i, e)}
                  style={{
                    flexShrink: 0,
                    width: MC_CFG.DAY_W,
                    borderRight: i < days.length - 1 ? `1px solid ${MC_CFG.CELL_BORDER}` : 'none',
                    background: mcDayColCellBackground(i, hoveredDayCol),
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    justifyContent: 'center',
                    cursor: 'pointer',
                    transition: 'background 150ms',
                  }}>
                  <span style={{ fontSize: 10, color: '#9ca3af', fontWeight: 500, textTransform: 'uppercase', letterSpacing: 0.4 }}>
                    {d.weekday}
                  </span>
                  <span style={{
                    fontSize: 13,
                    fontWeight: 700,
                    color: isToday ? MC_CFG.TODAY_LINE : '#1f2937',
                  }}>
                    {d.day}
                  </span>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    );
  }

  /* ===================== Main panel ===================== */
  function CalendarAhaPanel({ logoFile }) {
    const [listingColW, setListingColW] = useState(MC_CFG.LISTING_COL);
    const listingColWRef = useRef(listingColW);
    listingColWRef.current = listingColW;
    const [hoveredDayCol, setHoveredDayCol] = useState(null);
    const [dayCount, setDayCount] = useState(MC_DAY_COUNT_MIN);
    const days = useMemo(() => buildMcDays(dayCount), [dayCount]);
    const scrollRef = useRef(null);

    // Auto-scroll hint — runs once per session, shows users the calendar is scrollable
    useOneTimeHint('mc-aha', scrollRef, 900, runCalendarHint);

    // Expand columns as user scrolls right
    useEffect(() => {
      const el = scrollRef.current;
      if (!el) return;
      const onScroll = () => {
        const remaining = el.scrollWidth - el.scrollLeft - el.clientWidth;
        if (remaining < MC_CFG.DAY_W * 4) {
          setDayCount(prev => Math.min(MC_DAY_COUNT_EXTENDED, prev + 14));
        }
      };
      el.addEventListener('scroll', onScroll, { passive: true });
      return () => el.removeEventListener('scroll', onScroll);
    }, []);

    useEffect(() => {
      const el = scrollRef.current;
      if (!el) return undefined;
      const measure = () => {
        const w = el.clientWidth;
        if (w <= 0) return;
        const lw = listingColWRef.current;
        const cols = Math.floor((w - lw) / MC_CFG.DAY_W);
        const next = Math.min(MC_DAY_COUNT_MAX, Math.max(MC_DAY_COUNT_MIN, cols));
        setDayCount((prev) => (prev === next ? prev : next));
      };
      measure();
      const ro = new ResizeObserver(measure);
      ro.observe(el);
      return () => ro.disconnect();
    }, [listingColW]);

    const onDayColEnter = useCallback((col) => {
      setHoveredDayCol(col);
    }, []);

    const onDayColLeave = useCallback((col, e) => {
      const r = e.relatedTarget;
      if (r instanceof Element && r.closest(`[data-mc-day-col="${col}"]`)) return;
      setHoveredDayCol((h) => (h === col ? null : h));
    }, []);

    const handleResizeStart = useCallback((e) => {
      e.preventDefault();
      const startX = e.clientX;
      const startW = listingColW;
      const onMove = (ev) => {
        const next = Math.max(120, Math.min(320, startW + (ev.clientX - startX)));
        setListingColW(next);
      };
      const onUp = () => {
        document.removeEventListener('mousemove', onMove);
        document.removeEventListener('mouseup', onUp);
      };
      document.addEventListener('mousemove', onMove);
      document.addEventListener('mouseup', onUp);
    }, [listingColW]);

    const totalWidth = listingColW + days.length * MC_CFG.DAY_W;
    const todayLineLeft = listingColW + MC_TODAY_INDEX * MC_CFG.DAY_W + MC_CFG.DAY_W * 0.5;
    const rowCount = MC_LISTINGS.length;
    const tableHeight = MC_CFG.MONTH_H + MC_CFG.HEADER_H + rowCount * MC_CFG.ROW_H;

    return (
      <div className="aha-mc-card">
        <div className="aha-mc-card-header">
          <div className="aha-mc-card-title">
            <div className="aha-mc-card-icon">
              {logoFile ? (
                <div style={{width:18, height:18, borderRadius:4, background:"linear-gradient(135deg, hsl(var(--gst-primary)), #2A6F66)", display:"flex", alignItems:"center", justifyContent:"center", color:"white", fontWeight:700, fontSize:9, lineHeight:1}}>MR</div>
              ) : (
                <IconCalendar size={18} />
              )}
            </div>
            <span>Multi-Calendar</span>
          </div>
          <span className="aha-mc-sync-tag">Synced from Airbnb</span>
        </div>
        <div className="aha-mc-viewport-wrap">
          <div
            ref={scrollRef}
            className="aha-mc-viewport"
            style={{
              overflowX: 'auto',
              overflowY: 'auto',
              WebkitOverflowScrolling: 'touch',
            }}
          >
            <div style={{ position: 'relative', width: totalWidth, minWidth: '100%' }}>
              <MultiCalendarHeader
                listingColW={listingColW}
                hoveredDayCol={hoveredDayCol}
                onDayColEnter={onDayColEnter}
                onDayColLeave={onDayColLeave}
                days={days}
              />
              {MC_LISTINGS.map((listing, i) => (
                <MultiCalendarRow
                  key={listing.id}
                  listing={listing}
                  bars={MC_BARS.filter(b => b.listingId === listing.id)}
                  listingColW={listingColW}
                  hoveredDayCol={hoveredDayCol}
                  onDayColEnter={onDayColEnter}
                  onDayColLeave={onDayColLeave}
                  days={days}
                />
              ))}
              {/* Today vertical line */}
              <div aria-hidden="true" style={{
                position: 'absolute',
                top: 0,
                left: todayLineLeft,
                width: 2,
                height: tableHeight,
                background: MC_CFG.TODAY_LINE,
                zIndex: 2,
                pointerEvents: 'none',
              }} />
              {/* Resize handle */}
              <div
                onMouseDown={handleResizeStart}
                title="Drag to resize"
                style={{
                  position: 'sticky',
                  left: listingColW - 3,
                  top: 0,
                  width: 6,
                  height: tableHeight,
                  marginTop: -tableHeight,
                  cursor: 'col-resize',
                  zIndex: 5,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  pointerEvents: 'auto',
                }}
              >
                <div style={{
                  width: 2,
                  height: 36,
                  borderRadius: 2,
                  background: 'rgba(107,114,128,0.4)',
                  opacity: 0,
                  transition: 'opacity 150ms',
                }}
                  onMouseEnter={e => e.currentTarget.style.opacity = 1}
                  onMouseLeave={e => e.currentTarget.style.opacity = 0}
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  window.CalendarAhaPanel = CalendarAhaPanel;
})();
