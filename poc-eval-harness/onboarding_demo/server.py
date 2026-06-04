"""Single-origin dev server for the OB-V2 x Brain merge demo.

Serves the enhanced wizard frontend (./web) and a small JSON API backed by the
real brain extractors. Stdlib only — run with `uv run python -m onboarding_demo.server`
from the poc-eval-harness directory, or `python onboarding_demo/server.py`.

    GET /api/accounts?q=<query>&limit=<n>   -> account picker list
    GET /api/session/init?account=<name>    -> session context payload
"""

from __future__ import annotations

import json
import re
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

_HERE = Path(__file__).resolve().parent
_HARNESS_ROOT = _HERE.parent  # poc-eval-harness/ — makes `harness`/`kernel` importable
if str(_HARNESS_ROOT) not in sys.path:
    sys.path.insert(0, str(_HARNESS_ROOT))

from onboarding_demo import context_api, llm_copy  # noqa: E402

_WEB_DIR = _HERE / "web"


class PiiEgressError(RuntimeError):
    """An API payload would leak raw handover-note text to the browser."""


def _assert_no_raw_note(payload: object, raw_note: str | None) -> None:
    """Fail closed if any substantial span of the raw note appears in a response.

    The PII boundary (see context_api) says the browser receives only derived,
    enum-based context — never raw note prose. This enforces that in code instead
    of trusting the builders: short derived strings (business name, summary bullets)
    sit well under the 40-char span threshold, so they never trip it; a verbatim
    leak of note text would. The error message carries NO note content, so the
    fail-closed 500 itself cannot leak.
    """
    if not raw_note:
        return
    serialized = json.dumps(payload, ensure_ascii=False).lower()
    for span in re.split(r"[\n.]+", raw_note):
        span = span.strip().lower()
        if len(span) >= 40 and span in serialized:
            raise PiiEgressError("raw note span detected in API payload")


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(_WEB_DIR), **kwargs)

    def end_headers(self) -> None:  # noqa: N802
        # Dev server: never cache, so edits to web/ always reload on refresh.
        self.send_header("Cache-Control", "no-store, max-age=0")
        super().end_headers()

    def _send_json(self, payload: object, status: int = 200) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_account_json(self, payload: object, account_name: str, status: int = 200) -> None:
        """Send an account-scoped payload only after the PII egress guard clears it."""
        try:
            _assert_no_raw_note(payload, context_api.raw_note_for(account_name))
        except PiiEgressError:
            sys.stderr.write(
                f"[demo] PII GUARD: withheld response for {account_name!r} — raw note text in payload\n"
            )
            self._send_json({"error": "pii_guard", "detail": "response withheld"}, status=500)
            return
        self._send_json(payload, status)

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path.startswith("/api/"):
            self._handle_api(parsed.path, parse_qs(parsed.query))
            return
        super().do_GET()

    def do_POST(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path == "/api/normalize":
            self._handle_normalize()
            return
        self._send_json({"error": "unknown endpoint"}, status=404)

    def _handle_normalize(self) -> None:
        try:
            length = int(self.headers.get("Content-Length") or 0)
            raw = self.rfile.read(length) if length else b""
            body = json.loads(raw or b"{}")
            field = body.get("field") or {}
            text = str(body.get("text") or "")
            result = llm_copy.normalize_free_text(field, text)
            self._send_json({"result": result})
        except Exception as exc:
            self._send_json({"error": type(exc).__name__, "detail": str(exc)}, status=500)

    def _handle_api(self, path: str, query: dict[str, list[str]]) -> None:
        try:
            if path == "/api/accounts":
                q = (query.get("q") or [""])[0]
                limit = int((query.get("limit") or ["25"])[0])
                self._send_json({"accounts": context_api.list_accounts(q, limit=limit)})
                return
            if path == "/api/session/init":
                name = (query.get("account") or [""])[0].strip()
                if not name:
                    self._send_json({"error": "missing ?account="}, status=400)
                    return
                ctx = context_api.session_for(name)
                if ctx is None:
                    self._send_json({"error": f"account not found: {name}"}, status=404)
                    return
                ctx["ai_enabled"] = llm_copy.available()
                self._send_account_json(ctx, name)
                return
            if path == "/api/copy":
                name = (query.get("account") or [""])[0].strip()
                if not name:
                    self._send_json({"error": "missing ?account="}, status=400)
                    return
                session = context_api.session_for(name)
                if session is None:
                    self._send_json({"error": f"account not found: {name}"}, status=404)
                    return
                self._send_account_json({"copy": llm_copy.personalized_copy(session)}, name)
                return
            self._send_json({"error": "unknown endpoint"}, status=404)
        except Exception as exc:  # surface errors as JSON for the browser console
            self._send_json({"error": type(exc).__name__, "detail": str(exc)}, status=500)

    def log_message(self, fmt: str, *args) -> None:
        sys.stderr.write("[demo] " + (fmt % args) + "\n")


def main() -> None:
    import os

    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = int(os.environ.get("PORT", "5173"))
    # Bind to all interfaces when hosted (PaaS health checks hit the container's
    # external IP); default to loopback for local dev.
    host = os.environ.get("HOST", "0.0.0.0" if os.environ.get("PORT") else "127.0.0.1")
    httpd = ThreadingHTTPServer((host, port), Handler)
    print(f"OB-V2 x Brain demo: http://{host}:{port}")
    print(f"  serving frontend from {_WEB_DIR}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")


if __name__ == "__main__":
    main()
