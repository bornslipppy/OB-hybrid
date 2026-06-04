"""Single-origin dev server for the OB-V2 x Brain merge demo.

Serves the enhanced wizard frontend (./web) and a small JSON API backed by the
real brain extractors. Stdlib only — run with `uv run python -m onboarding_demo.server`
from the poc-eval-harness directory, or `python onboarding_demo/server.py`.

    GET /api/accounts?q=<query>&limit=<n>   -> account picker list
    GET /api/session/init?account=<name>    -> session context payload
"""

from __future__ import annotations

import json
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
                self._send_json(ctx)
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
                self._send_json({"copy": llm_copy.personalized_copy(session)})
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
    httpd = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print(f"OB-V2 x Brain demo: http://127.0.0.1:{port}")
    print(f"  serving frontend from {_WEB_DIR}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")


if __name__ == "__main__":
    main()
