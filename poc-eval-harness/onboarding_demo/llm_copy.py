"""LLM-backed copy + free-text normalization for the OB-V2 wizard merge demo.

Gemini via the OpenAI-compatible endpoint (``gemini-2.5-flash`` by default), with the
key loaded from the repo ``.env`` (``GEMINI_API_KEY``) by ``harness.providers.load_env``.

Both entry points degrade gracefully: if no key is configured or the call fails, they
return ``None`` and the caller falls back to deterministic copy / a passthrough echo, so
the demo always works offline.

PII boundary: callers pass only the browser-safe derived context (first name, business
name, rep name, enum-derived summary bullets) — never the raw note text.
"""

from __future__ import annotations

import json
import os
import re
from typing import Any

from harness import providers

_MODEL = os.environ.get("OB_LLM_MODEL", "gemini-2.5-flash")
_GEMINI_OPENAI_BASE = "https://generativelanguage.googleapis.com/v1beta/openai/"

_client: Any = None
_client_tried = False

_JSON_FENCE = re.compile(r"^```(?:json)?\s*|\s*```$", re.IGNORECASE)


def _get_client() -> Any:
    global _client, _client_tried
    if _client_tried:
        return _client
    _client_tried = True
    try:
        providers.load_env()
    except Exception:
        pass
    key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not key:
        return None
    try:
        from openai import OpenAI

        _client = OpenAI(api_key=key, base_url=_GEMINI_OPENAI_BASE)
    except Exception:
        _client = None
    return _client


def available() -> bool:
    return _get_client() is not None


def _complete(system: str, user: str, *, max_tokens: int = 400, temperature: float = 0.3) -> str | None:
    client = _get_client()
    if client is None:
        return None
    try:
        resp = client.chat.completions.create(
            model=_MODEL,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        )
        return (resp.choices[0].message.content or "").strip()
    except Exception:
        return None


def _parse_json(raw: str | None) -> dict[str, Any] | None:
    if not raw:
        return None
    text = _JSON_FENCE.sub("", raw.strip())
    try:
        obj = json.loads(text)
        return obj if isinstance(obj, dict) else None
    except Exception:
        # last-resort: grab the first {...} block
        m = re.search(r"\{.*\}", text, re.DOTALL)
        if not m:
            return None
        try:
            obj = json.loads(m.group(0))
            return obj if isinstance(obj, dict) else None
        except Exception:
            return None


# ---------------------------------------------------------------------------
# P2 — personalized onboarding copy (Amanda's opening line + a one-line intro)
# ---------------------------------------------------------------------------

_COPY_SYSTEM = (
    "You are {specialist}, a warm, concise Guesty onboarding specialist writing the very "
    "first message of a self-serve onboarding questionnaire. You are greeting a business (a "
    "property manager) whose sales handover notes you have just read.\n"
    "Write `bot_line` as your opening message to them. It MUST:\n"
    "1. Greet the business by name (use business_name as-is; never address it as a person).\n"
    "2. Show you read the handover — reflect 2-3 specific facts from handover_highlights, woven "
    "into natural sentences (never a bulleted list, never quote the list verbatim).\n"
    "3. End with exactly ONE confirmation question covering those facts "
    "(e.g. 'Does that all line up?').\n"
    "Keep it to 2-4 short sentences, first person, friendly and human (no emojis).\n"
    "STRICT RULES: never invent facts not present in the context; never mention or imply tax "
    "rates, fees, percentages, or prices (a listing count is fine if given); do not promise "
    "outcomes; ask only ONE question total.\n"
    'Return ONLY minified JSON with exactly these keys: {{"bot_line": string, "intro": string}}. '
    "intro is one short sentence (max ~160 chars) setting expectations for the questionnaire."
)


def personalized_copy(session: dict[str, Any]) -> dict[str, Any] | None:
    """Return ``{"bot_line", "intro", "source": "llm"}`` or ``None`` to use the fallback."""
    ctx = session.get("ob_context") or {}
    sf = session.get("sf_prefill") or {}
    payload = {
        "business_name": sf.get("business_name"),
        "sales_rep": ctx.get("rep"),
        "listing_count": sf.get("listing_count"),
        "handover_highlights": (ctx.get("note") or {}).get("summary_bullets") or [],
    }
    if not payload["handover_highlights"]:
        # Nothing to personalize from — let the deterministic copy stand.
        return None
    system = _COPY_SYSTEM.format(specialist=ctx.get("specialist") or "Amanda")
    # gemini-2.5-flash thinking tokens count against max_tokens — leave generous headroom.
    raw = _complete(system, json.dumps(payload), max_tokens=1200, temperature=0.4)
    parsed = _parse_json(raw)
    if not parsed:
        return None
    bot_line = str(parsed.get("bot_line") or "").strip()
    intro = str(parsed.get("intro") or "").strip()
    if not bot_line and not intro:
        return None
    return {"bot_line": bot_line, "intro": intro, "source": "llm"}


# ---------------------------------------------------------------------------
# P3 — free-text normalization into a structured value
# ---------------------------------------------------------------------------

_NORMALIZE_SYSTEM = (
    "You normalize a property manager's free-text answer into a structured value for an "
    "onboarding form. STRICT RULES: do not invent hard numbers (tax %, fees, prices); if the "
    "user states such a number, capture it verbatim in `normalized` and set "
    "`needs_confirmation` true. If the field offers options, map to the matching option "
    "id(s); otherwise return a cleaned value. "
    'Return ONLY minified JSON with exactly these keys: '
    '{"normalized": string, "matched_options": string[], "summary": string, '
    '"needs_confirmation": boolean}. '
    "summary is a short first-person echo of how you understood the answer (max ~120 chars)."
)


def normalize_free_text(field: dict[str, Any], text: str) -> dict[str, Any] | None:
    """Return a normalized structured result, or ``None`` to use the passthrough fallback."""
    text = (text or "").strip()
    if not text:
        return None
    payload = {
        "field_label": field.get("label"),
        "field_hint": field.get("hint"),
        "options": field.get("options") or [],
        "user_text": text,
    }
    raw = _complete(_NORMALIZE_SYSTEM, json.dumps(payload), max_tokens=1200, temperature=0.1)
    parsed = _parse_json(raw)
    if not parsed:
        return None
    return {
        "normalized": str(parsed.get("normalized") or text).strip(),
        "matched_options": [str(o) for o in (parsed.get("matched_options") or [])],
        "summary": str(parsed.get("summary") or "").strip(),
        "needs_confirmation": bool(parsed.get("needs_confirmation")),
        "source": "llm",
    }
