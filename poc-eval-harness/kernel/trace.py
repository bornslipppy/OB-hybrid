"""Trace event schema (architecture §3.3 / R-10) + append-only JSONL I/O (NFR-1).

The trace is *richer than a bare tool-call list* on purpose: false-write detection on
composite tools (FR-24 / EC-12) and questions-to-completion (excluding echo turns,
EC-32) cannot be reconstructed from tool calls alone. The metric computers consume the
``kind`` vocabulary below; the computation is identical for both systems (FR-13b/FR-24).

The trace is the durable source of truth (one JSONL file per run, append-only,
human-diffable, PII-free); everything downstream is derived from it.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Annotated, Any, Iterator, Literal, Union

from pydantic import BaseModel, Field, TypeAdapter


class UserFacingQuestion(BaseModel):
    """A question shown to the simulated host. Counts toward questions_to_completion.

    Echo turns are *not* this kind (they are ``echo_issued``) so they are excluded
    from the question count by construction (EC-32).
    """

    kind: Literal["user_facing_question"] = "user_facing_question"
    turn: int
    slot: str | None = None  # primary slot asked about; None for open-ended
    text: str


class ValueIntroduced(BaseModel):
    """A value entered the conversation (by the user or as a prefill candidate)."""

    kind: Literal["value_introduced"] = "value_introduced"
    turn: int
    slot: str
    subfield: str | None = None  # for composite tools (add_owner/add_fee/add_tax)
    value: Any = None


class EchoIssued(BaseModel):
    """The system echoed a value back for confirmation (echo-before-write gate)."""

    kind: Literal["echo_issued"] = "echo_issued"
    turn: int
    slot: str
    subfield: str | None = None
    value: Any = None


class UserConfirmed(BaseModel):
    """The user confirmed a previously echoed value/sub-field."""

    kind: Literal["user_confirmed"] = "user_confirmed"
    turn: int
    slot: str
    subfield: str | None = None


class UserCorrected(BaseModel):
    """The user corrected a previously echoed value/sub-field."""

    kind: Literal["user_corrected"] = "user_corrected"
    turn: int
    slot: str
    subfield: str | None = None
    corrected_value: Any = None


class ToolCallEvent(BaseModel):
    """A tool was invoked. ``call_type`` + ``temperature`` make FR-6 auditable.

    For a scored slot the invariant is ``call_type == "scored"`` and
    ``temperature == 0.0``; the report verifies this directly from the trace (§4.1).
    """

    kind: Literal["tool_call"] = "tool_call"
    turn: int
    tool: str
    args: dict[str, Any]
    call_type: Literal["scored", "glue"] = "scored"
    temperature: float = 0.0


class SessionEnd(BaseModel):
    """Terminal event. ``incomplete_turn_cap`` is a defined outcome, not a hang."""

    kind: Literal["session_end"] = "session_end"
    turn: int
    reason: Literal["completed", "incomplete_turn_cap", "errored"]


TraceEvent = Annotated[
    Union[
        UserFacingQuestion,
        ValueIntroduced,
        EchoIssued,
        UserConfirmed,
        UserCorrected,
        ToolCallEvent,
        SessionEnd,
    ],
    Field(discriminator="kind"),
]

_EVENT_ADAPTER: TypeAdapter[Any] = TypeAdapter(TraceEvent)


class TraceWriter:
    """Append-only JSONL writer — one file per run, one event per line.

    Append-only is enforced by opening in ``"a"`` mode; the writer never seeks or
    rewrites, so a written event is immutable.
    """

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def append(self, event: BaseModel) -> None:
        line = event.model_dump_json()
        with self.path.open("a", encoding="utf-8") as fh:
            fh.write(line + "\n")

    def extend(self, events: list[BaseModel]) -> None:
        for event in events:
            self.append(event)


class TraceReader:
    """Reads a JSONL trace back into validated, discriminated event models."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    def __iter__(self) -> Iterator[BaseModel]:
        with self.path.open("r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                yield _EVENT_ADAPTER.validate_python(json.loads(line))

    def events(self) -> list[BaseModel]:
        return list(self)
