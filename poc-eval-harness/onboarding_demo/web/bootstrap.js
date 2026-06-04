// bootstrap.js — fetch real session context from the backend BEFORE the wizard
// mounts, then inject the Babel-transpiled app scripts. Falls back to the
// hardcoded SF_PREFILL in screens.jsx when the API is unavailable (offline view).
(function () {
  'use strict';

  var DEFAULT_ACCOUNT = 'City and Coastal';
  var params = new URLSearchParams(location.search);
  var account = params.get('account') || DEFAULT_ACCOUNT;

  function ready(fn) {
    if (document.readyState !== 'loading') fn();
    else document.addEventListener('DOMContentLoaded', fn);
  }

  function injectApp() {
    // Dev cache-buster: a fresh token per load so edits to the .jsx always reload.
    var v = '?v=' + Date.now();
    ['screens.jsx', 'multi-calendar.jsx', 'wizard.jsx'].forEach(function (src) {
      var s = document.createElement('script');
      s.type = 'text/babel';
      s.setAttribute('data-presets', 'react');
      s.src = src + v;
      document.body.appendChild(s);
    });
    if (window.Babel && window.Babel.transformScriptTags) {
      window.Babel.transformScriptTags();
    }
  }

  // --- Small floating account picker so the demo can switch notes live ---
  function mountPicker() {
    fetch('/api/accounts?q=&limit=40')
      .then(function (r) {
        return r.ok ? r.json() : { accounts: [] };
      })
      .then(function (data) {
        var accounts = (data && data.accounts) || [];
        if (!accounts.length) return;
        if (
          !accounts.some(function (a) {
            return a.name === account;
          })
        ) {
          accounts.unshift({ name: account });
        }
        var wrap = document.createElement('div');
        wrap.className = 'ob-account-picker';
        wrap.style.cssText =
          'position:fixed;top:10px;right:12px;z-index:9999;display:flex;gap:6px;' +
          'align-items:center;background:rgba(255,255,255,.92);backdrop-filter:blur(6px);' +
          'border:1px solid rgba(0,0,0,.1);border-radius:8px;padding:5px 8px;' +
          'font:12px/1.2 system-ui,sans-serif;box-shadow:0 2px 8px rgba(0,0,0,.08)';
        var label = document.createElement('span');
        label.textContent = 'Demo account';
        label.style.cssText = 'opacity:.6;font-weight:600';
        var sel = document.createElement('select');
        sel.style.cssText = 'font:12px system-ui,sans-serif;border:0;background:transparent;max-width:220px';
        accounts.forEach(function (a) {
          var opt = document.createElement('option');
          opt.value = a.name;
          opt.textContent = a.name + (a.listing_count ? ' (' + a.listing_count + ')' : '');
          if (a.name === account) opt.selected = true;
          sel.appendChild(opt);
        });
        sel.addEventListener('change', function () {
          params.set('account', sel.value);
          location.search = params.toString();
        });
        wrap.appendChild(label);
        wrap.appendChild(sel);
        document.body.appendChild(wrap);
      })
      .catch(function () {});
  }

  // --- Progressive LLM copy (P2): fetched in parallel, applied when it arrives ---
  // The deterministic note-aware copy renders immediately; if the model returns
  // personalized copy a moment later, we broadcast it and the WelcomePanel swaps it in.
  // Always settle the copy phase — success OR failure dispatches `ob-copy` (detail
  // may be null) and sets OB_COPY_SETTLED, so the WelcomePanel can stop its spinner
  // and fall back to deterministic copy instead of waiting forever.
  function settleCopy(copy) {
    window.OB_COPY = copy || null;
    window.OB_COPY_SETTLED = true;
    window.dispatchEvent(new CustomEvent('ob-copy', { detail: copy || null }));
  }

  function fetchCopy() {
    fetch('/api/copy?account=' + encodeURIComponent(account))
      .then(function (r) {
        return r.ok ? r.json() : null;
      })
      .then(function (data) {
        settleCopy(data && data.copy);
      })
      .catch(function () {
        settleCopy(null);
      });
  }

  fetch('/api/session/init?account=' + encodeURIComponent(account))
    .then(function (r) {
      return r.ok ? r.json() : null;
    })
    .then(function (data) {
      if (data && !data.error) {
        window.__OB_SESSION = data;
        window.OB_CONTEXT = data.ob_context || null;
        if (data.ai_enabled) fetchCopy();
      } else if (data && data.error) {
        console.warn('[ob] session init:', data.error, data.detail || '');
      }
    })
    .catch(function (e) {
      console.warn('[ob] session init failed, using offline defaults', e);
    })
    .finally(function () {
      ready(function () {
        injectApp();
        mountPicker();
      });
    });
})();
