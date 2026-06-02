"""Story 0.1 — trace event schema (§3.3) + append-only JSONL I/O (NFR-1)."""

from __future__ import annotations

from kernel.trace import (
    EchoIssued,
    SessionEnd,
    ToolCallEvent,
    TraceReader,
    TraceWriter,
    UserConfirmed,
    UserFacingQuestion,
    ValueIntroduced,
)


def test_tool_call_event_audits_call_type_and_temperature():
    ev = ToolCallEvent(turn=9, tool="record_answer", args={"field_id": "go_live"})
    assert ev.call_type == "scored"
    assert ev.temperature == 0.0


def test_richer_than_tool_calls_events_exist():
    # The events false-write detection (FR-24) needs beyond a bare tool-call list.
    assert ValueIntroduced(turn=8, slot="x", subfield="amount", value=500).kind == "value_introduced"
    assert EchoIssued(turn=8, slot="x", value=500).kind == "echo_issued"
    assert UserConfirmed(turn=9, slot="x").kind == "user_confirmed"


def test_writer_is_append_only_and_reader_roundtrips(tmp_path):
    path = tmp_path / "runs" / "B1_agent_0.jsonl"
    writer = TraceWriter(path)
    events = [
        UserFacingQuestion(turn=1, slot="go_live", text="When do you want to go live?"),
        ValueIntroduced(turn=2, slot="go_live", value="asap"),
        ToolCallEvent(turn=2, tool="record_answer", args={"field_id": "go_live"}),
        SessionEnd(turn=3, reason="completed"),
    ]
    writer.extend(events)

    # Append-only: a second append adds a line, never rewrites.
    writer.append(SessionEnd(turn=4, reason="errored"))
    assert path.read_text().count("\n") == 5

    read_back = TraceReader(path).events()
    assert [type(e) for e in read_back[:4]] == [type(e) for e in events]
    assert read_back[0].text.startswith("When do you")
    assert read_back[-1].reason == "errored"
