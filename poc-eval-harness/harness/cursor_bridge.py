"""Minimal OpenAI-compatible HTTP bridge to the Cursor agent CLI.

Listens on http://127.0.0.1:8765 and accepts POST /v1/chat/completions in the
standard OpenAI format.  Each request:

  1. Flattens messages into a single prompt string (system → preamble, then
     alternating user/assistant turns ending with the last user turn).
  2. Calls ``agent <prompt> --print --trust --output-format text
     --model <model>`` as a subprocess.
  3. Wraps the stdout text in an OpenAI ChatCompletion response (non-streaming).

Tool calls are handled by embedding the tool schema in the system preamble and
parsing the model's JSON response (the model is instructed to reply with a
JSON object when it wants to call a tool).

Usage
-----
    python -m harness.cursor_bridge          # default port 8765
    python -m harness.cursor_bridge --port 9000

Requires Python 3.12 and the ``agent`` CLI to be on PATH.  Set
CURSOR_API_KEY in the environment (or .env) if the CLI needs it.
"""

from __future__ import annotations

import argparse
import http.server
import json
import os
import re
import subprocess
import sys
import textwrap
import threading
import time
import uuid
from pathlib import Path
from typing import Any

_AGENT_BIN = os.environ.get(
    "CURSOR_AGENT_BIN",
    str(Path.home() / ".local" / "bin" / "agent"),
)
_DEFAULT_MODEL = "claude-4.6-sonnet-medium"

# ---------------------------------------------------------------------------
# Prompt construction
# ---------------------------------------------------------------------------


def _build_prompt(messages: list[dict], tools: list[dict] | None) -> tuple[str, str | None]:
    """Return (system_text | None, user_prompt) from an OpenAI message list.

    The ``user_prompt`` is what gets passed as the positional argument to
    ``agent``.  The system content (if any) is returned separately and
    prepended by the caller.
    """
    system_parts: list[str] = []
    dialog_parts: list[str] = []

    for msg in messages:
        role = msg.get("role", "user")
        content = msg.get("content") or ""
        if role == "system":
            system_parts.append(content)
        elif role == "user":
            dialog_parts.append(f"User: {content}")
        elif role == "assistant":
            # Assistant's previous turn (multi-turn)
            dialog_parts.append(f"Assistant: {content}")

    # Embed tool schemas into the system preamble so the model knows what
    # JSON shapes to emit when it wants to call a tool.
    if tools:
        tool_desc_lines: list[str] = [
            "\n\nAvailable tools — output ONLY valid JSON (matching the schema exactly) to call a tool:",
        ]
        for t in tools:
            fn = t.get("function", t)
            schema = fn.get("parameters", {})
            props = schema.get("properties", {})
            required_params = schema.get("required", [])

            param_parts: list[str] = []
            for pname, pdef in props.items():
                ptype: str = pdef.get("type", "any")
                if pdef.get("enum"):
                    ptype = " | ".join(f'"{v}"' for v in pdef["enum"])
                elif ptype == "array":
                    items = pdef.get("items", {})
                    item_type = items.get("type", "string")
                    if items.get("enum"):
                        item_type = " | ".join(f'"{v}"' for v in items["enum"])
                    ptype = f"list[{item_type}]"
                opt = "" if pname in required_params else "?"
                param_parts.append(f"{pname}{opt}: {ptype}")

            params_str = ", ".join(param_parts) if param_parts else "..."
            tool_desc_lines.append(
                f'  • {fn["name"]}({params_str})'
                f' — {fn.get("description", "")}'
            )

        tool_desc_lines.append(
            "\nTo call a tool output ONLY this JSON on its own line (nothing else before or after):\n"
            '{"tool": "<name>", "args": {<params>}}\n'
            "IMPORTANT: use EXACTLY the enum values shown above — do not invent new values."
        )
        system_parts.append("\n".join(tool_desc_lines))

    system_text: str | None = "\n\n".join(system_parts) if system_parts else None

    # The last user message is the live prompt; preceding turns give context.
    if dialog_parts:
        user_prompt = "\n".join(dialog_parts)
    else:
        user_prompt = "(no user message)"

    return system_text, user_prompt


def _run_agent(model: str, system: str | None, prompt: str) -> str:
    """Invoke the Cursor agent CLI synchronously and return its stdout text."""
    full_prompt = prompt
    if system:
        full_prompt = f"{system}\n\n---\n\n{prompt}"

    cmd = [
        _AGENT_BIN,
        "--print",
        "--trust",
        "--output-format", "text",
        "--model", model,
        full_prompt,
    ]
    env = {**os.environ}  # inherit, including CURSOR_API_KEY

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120,
            env=env,
        )
        if result.returncode != 0:
            err = (result.stderr or result.stdout or "").strip()
            raise RuntimeError(f"agent exited {result.returncode}: {err}")
        return (result.stdout or "").strip()
    except subprocess.TimeoutExpired:
        raise RuntimeError("agent subprocess timed out (120 s)")


# ---------------------------------------------------------------------------
# Tool-call parsing
# ---------------------------------------------------------------------------

_TOOL_JSON_RE = re.compile(
    r'\{\s*"tool"\s*:\s*"([^"]+)"\s*,\s*"args"\s*:\s*(\{.*?\})\s*\}',
    re.DOTALL,
)


def _parse_tool_call(text: str) -> dict | None:
    """Try to extract a tool-call JSON object from the model's reply."""
    m = _TOOL_JSON_RE.search(text)
    if not m:
        return None
    try:
        args = json.loads(m.group(2))
        return {"name": m.group(1), "args": args}
    except json.JSONDecodeError:
        return None


# ---------------------------------------------------------------------------
# OpenAI response builder
# ---------------------------------------------------------------------------


def _make_response(text: str, model: str) -> dict:
    """Wrap agent output in an OpenAI ChatCompletion response object."""
    tc = _parse_tool_call(text)
    if tc:
        message: dict[str, Any] = {
            "role": "assistant",
            "content": None,
            "tool_calls": [
                {
                    "id": f"call_{uuid.uuid4().hex[:8]}",
                    "type": "function",
                    "function": {
                        "name": tc["name"],
                        "arguments": json.dumps(tc["args"]),
                    },
                }
            ],
        }
    else:
        message = {"role": "assistant", "content": text}

    return {
        "id": f"chatcmpl-{uuid.uuid4().hex}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": model,
        "choices": [
            {
                "index": 0,
                "message": message,
                "finish_reason": "stop" if not tc else "tool_calls",
            }
        ],
        "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
    }


# ---------------------------------------------------------------------------
# HTTP server
# ---------------------------------------------------------------------------


class _Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, fmt: str, *args: Any) -> None:  # silence default access log
        pass

    def _send_json(self, code: int, body: dict) -> None:
        raw = json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self) -> None:  # noqa: N802
        if self.path in ("/health", "/v1/health"):
            self._send_json(200, {"ok": True, "bridge": "cursor_bridge.py"})
        else:
            self._send_json(404, {"error": "not found"})

    def do_POST(self) -> None:  # noqa: N802
        if self.path not in ("/v1/chat/completions",):
            self._send_json(404, {"error": "not found"})
            return

        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length))

        model: str = body.get("model") or _DEFAULT_MODEL
        messages: list[dict] = body.get("messages") or []
        tools: list[dict] | None = body.get("tools") or None

        try:
            system, prompt = _build_prompt(messages, tools)
            text = _run_agent(model, system, prompt)
            self._send_json(200, _make_response(text, model))
        except Exception as exc:  # noqa: BLE001
            self._send_json(500, {"error": {"message": str(exc), "code": "bridge_error"}})


def serve(port: int = 8765) -> None:
    server = http.server.ThreadingHTTPServer(("127.0.0.1", port), _Handler)
    print(f"cursor_bridge listening on http://127.0.0.1:{port}", flush=True)
    print(f"  agent bin : {_AGENT_BIN}", flush=True)
    print(f"  model hint: {_DEFAULT_MODEL} (per-request override accepted)", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Cursor agent → OpenAI bridge")
    ap.add_argument("--port", type=int, default=8765)
    args = ap.parse_args()
    serve(args.port)
