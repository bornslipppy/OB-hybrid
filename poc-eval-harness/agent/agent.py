"""AgentSystem — LLM-backed System policy (Epic 3).

Implements the ``System`` protocol from ``kernel/protocol.py`` as a policy over
kernel-v1. The kernel is frozen; this module imports it read-only and adds only
the LLM reasoning layer on top.

Design invariants (all load-bearing):

* **Temperature enforcement (FR-6/D-2):** every tool-emitting turn routes through
  ``kernel.llm.scored_completion()`` at temperature 0.0. The greeting uses
  ``glue_completion()`` at 0.2 — the *only* non-scored call. There is no way to
  reach a scored-slot code path at any other temperature.

* **Tool-use loop (FR-2):** the OpenAI-compatible (Cursor) API requires one
  ``role="tool"`` message per tool-call ID after the assistant emits ``tool_calls``.
  The agent maintains ``_messages`` (an internal OpenAI-format message list) and
  ``_pending_tool_ids`` to inject synthetic ``role="tool"`` messages before the next
  API call. This keeps the harness loop clean: it always receives ``list[ToolCall]``
  without needing to understand the wire format.

* **Stop condition (FR-1/Story 3.1):** the agent pursues ALL reachable in-scope
  slots across all three priority tiers (required + recommended + optional). Stopping
  at the MVP-completeness line while recommended/optional slots remain undispositioned
  is a SAR penalty. ``_is_done()`` checks this programmatically via FrameGraph so the
  decision is structural, not left to LLM output parsing.

* **Schema-driven selection (FR-1):** the FrameGraph + ``_format_slot_status()``
  inject the current dispositioned/unanswered slot picture into the system prompt on
  every turn. The LLM reasons over this to select the next slot — no fixed order.

* **Trace (FR-2/NFR-1/Story 3.7):** ``ToolCallEvent`` events with ``call_type="scored"``
  and ``temperature=0.0`` are emitted inline to ``self._trace`` when a ``TraceWriter`` is
  passed (standalone use). In a harness run the runner owns the canonical trace and
  constructs the agent with ``trace_writer=None``; the agent instead surfaces
  echo-lifecycle events (``value_introduced`` / ``echo_issued`` / ``user_confirmed`` /
  ``user_corrected``) via ``drain_trace_events()`` (Story 4.6 enablement / R-10) so
  ``false_write_rate`` is meaningful on live traces.
"""

from __future__ import annotations

import re
import uuid
from pathlib import Path
from typing import Any

from kernel.llm import glue_completion, scored_completion
from kernel.protocol import EndConversation, NextAction, UserQuestion
from kernel.schema import FrameGraph, SchemaLoader
from kernel.state import ProfileState, SlotStatus
from kernel.tools import to_openai_tools
from kernel.trace import (
    EchoIssued,
    ToolCallEvent,
    TraceWriter,
    UserConfirmed,
    UserCorrected,
    ValueIntroduced,
)

# All schema sections the agent works across.
_ALL_SECTIONS = ["S0a", "S0b", "S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8"]

# Slot statuses that count as "dispositioned" (no further action needed).
_DISPOSITIONED = frozenset({SlotStatus.RECORDED, SlotStatus.SKIPPED, SlotStatus.FLAGGED})

# Slots whose values are brief-only and must never appear in a user-facing turn.
_BRIEF_ONLY = frozenset({"tech_level", "customer_sentiment", "risk_flags"})

# Fields whose depends_on guards reference list-typed facts but whose membership
# tests are machine-evaluable from recorded_facts alone (no extra signals needed).
# Signals are only needed for free-text phrases the schema cannot evaluate.
_DEFAULT_SIGNALS: dict[str, bool] = {
    "user_volunteers_website_intent": False,
    "user_volunteers_a_split": False,
}

_SYSTEM_PROMPT_PATH = Path(__file__).parent / "prompts" / "system_prompt.txt"

_MAX_TURNS = 60

# --- Echo-lifecycle marker protocol (Story 4.6 enablement / R-10) -------------
# The kernel's 7 tools are frozen (no echo tool), so the agent surfaces the echo
# lifecycle via machine-readable markers the LLM emits in its text. The agent parses
# them into ValueIntroduced / EchoIssued / UserConfirmed / UserCorrected events
# (drained by the harness into the canonical trace) and STRIPS them before the user
# sees the message. A write with no parseable prior confirmation is — correctly — a
# false write (fail-safe for SM-C1). Markers (one per line, subfield "-" ⇒ scalar):
#   [[ECHO slot=<slot> subfield=<sub|-> value=<value>]]   — echoing a value to confirm
#   [[CONFIRM slot=<slot> subfield=<sub|->]]               — user confirmed the echo
#   [[CORRECT slot=<slot> subfield=<sub|-> value=<new>]]   — user corrected the echo
_ECHO_TAG = re.compile(r"\[\[ECHO\s+slot=(\S+)\s+subfield=(\S+)\s+value=(.*?)\]\]", re.DOTALL)
_CONFIRM_TAG = re.compile(r"\[\[CONFIRM\s+slot=(\S+)\s+subfield=(\S+)\]\]")
_CORRECT_TAG = re.compile(r"\[\[CORRECT\s+slot=(\S+)\s+subfield=(\S+)(?:\s+value=(.*?))?\]\]", re.DOTALL)
_ANY_TAG = re.compile(r"\[\[(?:ECHO|CONFIRM|CORRECT)\b.*?\]\]", re.DOTALL)


class AgentSystem:
    """LLM-backed ``System`` policy for the Guesty Pro onboarding PoC.

    Args:
        cursor_client:
            An OpenAI-compatible client pointing at Cursor's API (or a test double
            satisfying the ``_CursorLike`` protocol from ``kernel.llm``).
        model:
            Dated model snapshot string (e.g. ``"claude-opus-4-6"``). Never a
            ``-latest`` alias (R-7).
        schema_path:
            Path to the frozen schema markdown (``schema/guesty-pro-account-creation-schema.md``).
        system_prompt:
            Override the base system prompt (default: loads from
            ``agent/prompts/system_prompt.txt``). Pass a string for unit tests.
        trace_writer:
            ``TraceWriter`` for JSONL event emission (Story 3.7 / NFR-1). If
            ``None`` the agent runs without emitting trace events; the harness
            always provides one for scored runs.
    """

    system_id: str = "agent"

    def __init__(
        self,
        *,
        cursor_client: Any,
        model: str,
        schema_path: str | Path,
        system_prompt: str | None = None,
        trace_writer: TraceWriter | None = None,
    ) -> None:
        self._client = cursor_client
        self._model = model
        self._tool_defs = to_openai_tools()

        # Base system prompt — tunable on the dev set, frozen before scoring (FR-26).
        self._system_prompt_base: str = (
            system_prompt
            if system_prompt is not None
            else _SYSTEM_PROMPT_PATH.read_text(encoding="utf-8")
        )

        # Load schema once; FrameGraph is kept for _is_done() and _format_slot_status().
        slots = SchemaLoader().load(schema_path)
        self._frame = FrameGraph(slots)

        self._trace: TraceWriter | None = trace_writer

        # Internal Anthropic-format message list. The harness passes the simplified
        # conversation_history; the agent syncs from it and maintains the full
        # tool_use / tool_result round-trip internally.
        self._messages: list[dict[str, Any]] = []

        # After returning list[ToolCall], the next call must inject tool_result
        # blocks before calling the API. We store the synthetic tool_use_ids here.
        self._pending_tool_ids: list[str] | None = None

        # Echo-lifecycle events parsed from the model's markers this turn, drained by
        # the harness (``run_conversation``) into the canonical trace each turn.
        self._pending_trace_events: list[Any] = []

    # ------------------------------------------------------------------
    # Harness trace hook
    # ------------------------------------------------------------------

    def drain_trace_events(self) -> list[Any]:
        """Return and clear the echo-lifecycle events emitted since the last drain.

        Called by ``run_conversation`` after every ``next_action`` so the events land
        in the canonical trace in the right order (confirmations before the write).
        """
        events, self._pending_trace_events = self._pending_trace_events, []
        return events

    # ------------------------------------------------------------------
    # System protocol implementation
    # ------------------------------------------------------------------

    def next_action(
        self,
        state: ProfileState,
        conversation_history: list[dict[str, Any]],
    ) -> NextAction:
        """Decide the next agent action.

        Args:
            state:
                Current ``ProfileState`` from the kernel reducer. Read-only here;
                mutations happen via returned ``ToolCall`` objects applied by the
                harness.
            conversation_history:
                Full message log maintained by the harness. The agent syncs new
                user messages from this list into its internal Anthropic-format
                ``_messages``. Format: list of ``{"role": str, "content": str|list}``
                dicts compatible with the Anthropic messages API.

        Returns:
            One of:
                ``UserQuestion``     — ask the simulator this text.
                ``list[ToolCall]``   — apply these to ``ProfileState`` then call again.
                ``EndConversation``  — the session is done.
        """
        # --- §8 invariant 7: turn cap ---
        if state.turn_count >= _MAX_TURNS:
            self._emit_session_end(state.turn_count, "incomplete_turn_cap")
            return EndConversation(reason="incomplete_turn_cap")

        # --- First call: opening greeting via glue_completion (temperature 0.2) ---
        if not self._messages:
            system = self._build_system_prompt(state)
            greeting = glue_completion(
                messages=[{"role": "user", "content": "Ready to start the onboarding."}],
                system=system,
                _client=self._client,
                _model=self._model,
            )
            self._messages.append({"role": "assistant", "content": greeting})
            return UserQuestion(text=greeting, primary_slot=None)

        # --- Inject role="tool" messages for every pending tool_call_id (OpenAI API) ---
        if self._pending_tool_ids is not None:
            for tid in self._pending_tool_ids:
                self._messages.append({"role": "tool", "tool_call_id": tid, "content": "OK"})
            self._pending_tool_ids = None
        else:
            # Sync the latest user message (simulator reply) from conversation_history.
            # The harness appends it after the last UserQuestion; we add it to our
            # internal list exactly once.
            self._sync_latest_user_message(conversation_history)

        # --- Stop condition check (Story 3.1 / FR-1) ---
        if self._is_done(state):
            self._emit_session_end(state.turn_count, "completed")
            return EndConversation(reason="completed")

        # --- All tool-emitting turns route through scored_completion (FR-6/D-2) ---
        system = self._build_system_prompt(state)
        text, tool_calls = scored_completion(
            messages=self._messages,
            tools=self._tool_defs,
            system=system,
            _client=self._client,
            _model=self._model,
        )

        # --- Parse echo-lifecycle markers (present on BOTH question and tool-call
        # turns) into trace events before branching. Confirmations parsed here are
        # drained ahead of this turn's ToolCallEvent, so a write is preceded by its
        # confirmation in trace order (false_write_rate / EC-12). ---
        clean_text, echo_events = self._extract_echo_events(text or "", state.turn_count)
        self._pending_trace_events.extend(echo_events)

        # --- Tool calls returned ---
        if tool_calls:
            # Build synthetic tool_calls objects for our internal message log (OpenAI format).
            # Synthetic IDs (uuid hex) are used because scored_completion discards the raw
            # response; the IDs only need to match the role="tool" messages injected on the
            # next call — both sides are under our control.
            import json as _json
            tool_ids = [f"call_{uuid.uuid4().hex[:12]}" for _ in tool_calls]
            tool_call_objects: list[dict[str, Any]] = [
                {
                    "id": tid,
                    "type": "function",
                    "function": {
                        "name": tc.tool,
                        "arguments": _json.dumps(tc.model_dump(exclude={"tool"})),
                    },
                }
                for tc, tid in zip(tool_calls, tool_ids)
            ]
            self._messages.append(
                {"role": "assistant", "content": None, "tool_calls": tool_call_objects}
            )
            self._pending_tool_ids = tool_ids

            # Emit trace events for each tool call (NFR-1/Story 3.7).
            if self._trace is not None:
                for tc in tool_calls:
                    self._trace.append(
                        ToolCallEvent(
                            turn=state.turn_count,
                            tool=tc.tool,
                            args=tc.model_dump(exclude={"tool"}),
                            call_type="scored",
                            temperature=0.0,
                        )
                    )

            return tool_calls  # type: ignore[return-value]

        # --- Text-only response → next question or done ---
        if text:
            # Keep the raw text (with markers) in the model's own message history;
            # the user only ever sees the stripped, clean text.
            self._messages.append({"role": "assistant", "content": text})
            primary = _extract_primary_slot_hint(clean_text, state)
            return UserQuestion(text=clean_text, primary_slot=primary)

        # --- Empty response (should not happen in practice) ---
        self._emit_session_end(state.turn_count, "completed")
        return EndConversation(reason="completed")

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _sync_latest_user_message(
        self, conversation_history: list[dict[str, Any]]
    ) -> None:
        """Add the most recent user message from the harness history if not yet present.

        The harness history contains only ``role="user"`` simulator replies.
        OpenAI-format tool results use ``role="tool"`` — they come from us, not the
        simulator, and are injected directly into ``self._messages`` above; they never
        appear in ``conversation_history``, so no special filter is needed here.
        """
        if not conversation_history:
            return
        latest = conversation_history[-1]
        if latest.get("role") != "user":
            return
        # Only add if not already the last message (avoid double-adding).
        if self._messages and self._messages[-1] == latest:
            return
        self._messages.append(latest)

    def _build_system_prompt(self, state: ProfileState) -> str:
        """Append the current slot status to the base system prompt (FR-1/Story 3.1)."""
        return f"{self._system_prompt_base}\n\n{self._format_slot_status(state)}"

    def _format_slot_status(self, state: ProfileState) -> str:
        """Render current slot dispositions into a human-readable status block.

        The LLM reads this on every turn to decide which slot to pursue next.
        This is the mechanism that makes slot selection schema-driven rather than
        scripted (FR-1 / Story 3.1).
        """
        facts = state.recorded_facts()
        signals = _detect_signals(facts)
        reachable = self._frame.reachable_slots(facts, _ALL_SECTIONS, signals=signals)
        reachable_ids = {s.id for s in reachable}

        recorded: list[str] = []
        skipped: list[str] = []
        flagged: list[str] = []
        echo_pending: list[str] = []
        unanswered: list[tuple[str, str, str]] = []  # (id, section, priority)

        for slot in reachable:
            s = state.slots.get(slot.id)
            status = s.status if s else SlotStatus.UNANSWERED

            if slot.id in _BRIEF_ONLY:
                continue  # brief-only slots never appear in user-facing status

            if status == SlotStatus.RECORDED:
                val = (s.value if s else None)
                recorded.append(f"  - {slot.id}: {val!r}")
            elif status == SlotStatus.SKIPPED:
                skipped.append(f"  - {slot.id}")
            elif status == SlotStatus.FLAGGED:
                flagged.append(f"  - {slot.id}")
            elif s and s.echo_pending:
                echo_pending.append(f"  - {slot.id} (awaiting user confirmation of echoed value)")
            else:
                unanswered.append((slot.id, slot.section, slot.priority))

        # Also surface any reachable but not-yet-recorded owners list status.
        owners_count = len(state.owners)
        if owners_count > 0 and "owners" in reachable_ids:
            recorded.append(f"  - owners: {owners_count} owner record(s) captured so far")

        lines = ["## CURRENT COLLECTION STATUS\n"]

        if recorded:
            lines.append("**RECORDED:**")
            lines.extend(recorded)
            lines.append("")

        if flagged:
            lines.append("**FLAGGED (handed to Jordan):**")
            lines.extend(flagged)
            lines.append("")

        if skipped:
            lines.append("**SKIPPED:**")
            lines.extend(skipped)
            lines.append("")

        if echo_pending:
            lines.append("**ECHO PENDING (awaiting confirmation before write):**")
            lines.extend(echo_pending)
            lines.append("")

        if unanswered:
            lines.append("**UNANSWERED — pursue these (all tiers):**")
            for fid, sec, pri in unanswered:
                lines.append(f"  - {fid} ({sec}, {pri})")
            lines.append("")

        if not unanswered and not echo_pending:
            lines.append("**All reachable slots are dispositioned. You may end the session.**")

        return "\n".join(lines)

    def _is_done(self, state: ProfileState) -> bool:
        """True when every reachable in-scope slot (all tiers) is dispositioned.

        This is the programmatic stop-condition gate for FR-1 / Story 3.1.
        'Reachable' is evaluated against confirmed (recorded) facts only, so a
        skipped upstream slot correctly collapses the dependent branch.
        """
        facts = state.recorded_facts()
        signals = _detect_signals(facts)
        reachable = self._frame.reachable_slots(facts, _ALL_SECTIONS, signals=signals)

        for slot_def in reachable:
            if slot_def.id in _BRIEF_ONLY:
                continue  # brief-only slots are never dispositioned interactively
            s = state.slots.get(slot_def.id)
            if s is None or s.status not in _DISPOSITIONED:
                return False
            if s.echo_pending:
                return False  # §8 inv 7: cannot end while echo awaits confirmation

        return True

    def _extract_echo_events(self, text: str, turn: int) -> tuple[str, list[Any]]:
        """Parse echo-lifecycle markers from ``text`` → events; return (clean_text, events).

        Emits ``ValueIntroduced`` + ``EchoIssued`` for each ``[[ECHO ...]]`` (the value
        entered and was echoed for confirmation), ``UserConfirmed`` for ``[[CONFIRM ...]]``,
        and ``UserCorrected`` for ``[[CORRECT ...]]``. ``clean_text`` has every marker
        removed so the user never sees the protocol.
        """
        events: list[Any] = []
        for m in _ECHO_TAG.finditer(text):
            slot, sub, raw = m.group(1), m.group(2), m.group(3).strip()
            subfield = None if sub == "-" else sub
            value = _coerce_value(raw)
            events.append(ValueIntroduced(turn=turn, slot=slot, subfield=subfield, value=value))
            events.append(EchoIssued(turn=turn, slot=slot, subfield=subfield, value=value))
        for m in _CONFIRM_TAG.finditer(text):
            slot, sub = m.group(1), m.group(2)
            events.append(UserConfirmed(turn=turn, slot=slot, subfield=None if sub == "-" else sub))
        for m in _CORRECT_TAG.finditer(text):
            slot, sub, raw = m.group(1), m.group(2), m.group(3)
            events.append(
                UserCorrected(
                    turn=turn, slot=slot, subfield=None if sub == "-" else sub,
                    corrected_value=_coerce_value(raw.strip()) if raw else None,
                )
            )
        clean = _ANY_TAG.sub("", text)
        # Collapse the whitespace a stripped marker leaves behind.
        clean = re.sub(r"[ \t]+\n", "\n", clean)
        clean = re.sub(r"\n{3,}", "\n\n", clean).strip()
        return clean, events

    def _emit_session_end(self, turn: int, reason: str) -> None:
        """Write a SessionEnd event to the trace if a writer is attached."""
        if self._trace is None:
            return
        from kernel.trace import SessionEnd

        valid_reasons = {"completed", "incomplete_turn_cap", "errored"}
        safe_reason = reason if reason in valid_reasons else "errored"
        self._trace.append(SessionEnd(turn=turn, reason=safe_reason))  # type: ignore[arg-type]


# ------------------------------------------------------------------
# Module-level helpers (pure functions — no class state)
# ------------------------------------------------------------------


def _coerce_value(raw: str) -> Any:
    """Light coercion of a marker value: int, then float, else the trimmed string."""
    s = raw.strip().strip("\"'")
    if not s:
        return None
    try:
        return int(s)
    except ValueError:
        pass
    try:
        return float(s)
    except ValueError:
        return s


def _detect_signals(facts: dict[str, Any]) -> dict[str, bool]:
    """Build the runtime signals dict for non-evaluable depends_on clauses.

    Direct-booking signals drive conditional S5 surfacing (FR-4 / Story 3.5).
    The LLM detects "user_volunteers_website_intent" conversationally; here we
    derive what we can from recorded facts alone. The FrameGraph passes these
    signals to ``evaluate_condition`` for the ``surface_when`` guards.
    """
    channels: list[str] = facts.get("channels") or []
    focus_topics: list[str] = facts.get("focus_topics") or []
    return {
        **_DEFAULT_SIGNALS,
        "channels_includes_direct": "direct" in channels,
        "focus_topics_includes_booking_website": "booking_website" in focus_topics,
    }


def _extract_primary_slot_hint(text: str, state: ProfileState) -> str | None:
    """Heuristically extract the primary slot being asked about in ``text``.

    Used to populate ``UserQuestion.primary_slot`` — a hint for the Group A
    simulator's slot-keyed scripted-turn lookup (FR-19 / EC-27). Returns ``None``
    when no single slot is identifiable (open-ended questions).
    """
    text_lower = text.lower()

    # Map key phrases to canonical slot IDs. Ordered by specificity (longer phrases first).
    _HINT_MAP: list[tuple[str, str]] = [
        # S8 hero branch
        ("management model", "owners"),
        ("get paid for managing", "owners"),
        ("commission rate", "owners"),
        ("fixed fee", "owners"),
        ("revenue split", "owners"),
        ("split terms", "owners"),
        ("who pays", "owners"),
        ("owner", "owners"),
        # S4 financials
        ("security deposit", "security_deposit_type"),
        ("cleaning fee", "mandatory_fees"),
        ("additional fee", "mandatory_fees"),
        ("tax", "taxes"),
        ("payment", "payment_timing"),
        ("revenue recognition", "revenue_recognition"),
        ("non-refundable", "non_refundable_enabled"),
        ("nonrefundable", "non_refundable_enabled"),
        # S2 pre-flight
        ("listing", "listing_count"),
        ("channel", "channels"),
        ("go live", "go_live"),
        ("timeline", "go_live"),
        # S7 focus
        ("focus", "focus_topics"),
        ("priority", "focus_topics"),
        ("pain", "pain"),
        ("biggest challenge", "pain"),
        # S8 ownership
        ("ownership", "ownership_model"),
        ("self-owned", "ownership_model"),
        ("managed for", "ownership_model"),
        ("mixed", "ownership_model"),
        ("rate strategy", "rate_strategy"),
        ("pricing tool", "rate_strategy"),
        # S5 booking website
        ("website", "website_brand_name"),
        ("direct booking", "website_brand_name"),
        ("booking site", "website_brand_name"),
        # S6 governance
        ("decision", "decision_owner"),
        ("teammate", "teammates"),
        # S3 operations
        ("cleaning", "cleaning_system"),
        ("lock", "smart_locks"),
        # S0b
        ("prior system", "migration_source"),
        ("previous pms", "migration_source"),
        ("coming from", "migration_source"),
        ("language", "ob_language"),
    ]

    for phrase, slot_id in _HINT_MAP:
        if phrase in text_lower:
            # Verify the slot is actually unanswered before returning the hint.
            s = state.slots.get(slot_id)
            if s is None or s.status == SlotStatus.UNANSWERED:
                return slot_id

    return None
