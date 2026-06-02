"""ProfileState + the pure StateReducer (architecture §3.2).

Every state mutation flows through this reducer; there is no other write path
(FR-2). The reducer is *pure* — it returns a new ``ProfileState`` and never
mutates its input.

Two refinements over the §10.2 ``apply(state, tool_call)`` stub, ratified for the
build (a bare free function cannot satisfy §3.2 without leaking the scored set or
free-writing):

  1. ``StateReducer(frame)`` binds the *public-schema* ``FrameGraph`` once. The
     ``end_section`` guard needs ``depends_on`` reachability against recorded facts;
     the frame is built from the public schema (never the answer key), so binding it
     leaks no scored-slot membership.
  2. Value/disposition writes come only from the 7 tools (``apply``); the echo
     ``echo_pending`` flag is a conversational-protocol signal driven by a separate
     ``observe(state, trace_event)`` over the echo-lifecycle events. This keeps
     "no value enters state except via a tool" intact while the ``end_section``
     guard can still see a pending echo.
"""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field

from .schema import FrameGraph
from .tools import (
    AddFee,
    AddOwner,
    AddTax,
    EndSection,
    FlagForCall1,
    RecordAnswer,
    SkipQuestion,
)
from .trace import EchoIssued, UserConfirmed, UserCorrected


class SlotStatus(str, Enum):
    """The runtime field-state machine (schema §1)."""

    UNANSWERED = "unanswered"
    RECORDED = "recorded"
    SKIPPED = "skipped"
    FLAGGED = "flagged"
    PREFILLED_UNCONFIRMED = "prefilled_unconfirmed"


# A slot is "dispositioned" once it leaves the open states. UNANSWERED and
# PREFILLED_UNCONFIRMED are open: an unconfirmed prefill is not yet an answer.
_DISPOSITIONED = {SlotStatus.RECORDED, SlotStatus.SKIPPED, SlotStatus.FLAGGED}


class SlotState(BaseModel):
    field_id: str
    status: SlotStatus = SlotStatus.UNANSWERED
    value: Any = None
    source: str | None = None
    flag_ref: str | None = None
    echo_pending: bool = False  # True between echo_issued and user_confirmed/corrected


class ProfileState(BaseModel):
    profile_id: str
    slots: dict[str, SlotState] = Field(default_factory=dict)
    owners: list[dict] = Field(default_factory=list)
    fees: list[dict] = Field(default_factory=list)
    taxes: list[dict] = Field(default_factory=list)
    flags: list[dict] = Field(default_factory=list)  # topic-level (field_id-less) flags
    turn_count: int = 0

    def recorded_facts(self) -> dict[str, Any]:
        """The recorded-value view used to evaluate ``depends_on`` reachability.

        Only ``recorded`` scalar slots contribute facts; an unconfirmed prefill is
        deliberately excluded so reachability reflects confirmed ground truth.
        """
        return {
            fid: s.value
            for fid, s in self.slots.items()
            if s.status is SlotStatus.RECORDED and s.value is not None
        }

    def _slot(self, field_id: str) -> SlotState:
        return self.slots.get(field_id, SlotState(field_id=field_id))


class EndSectionError(ValueError):
    """Raised when ``end_section`` is attempted with the section not yet closable."""


class StateReducer:
    """Pure reducer over the kernel tool/echo vocabulary.

    ``frame`` is the public-schema dependency graph used solely for the
    ``end_section`` reachability guard. It may be ``None`` for unit tests that only
    exercise tool application; an ``end_section`` with no frame is a usage error.
    """

    def __init__(self, frame: FrameGraph | None = None) -> None:
        self.frame = frame

    # --- tool application (the only value/disposition write path) ----------

    def apply(self, state: ProfileState, tool_call: BaseModel) -> ProfileState:
        new = state.model_copy(deep=True)

        if isinstance(tool_call, RecordAnswer):
            self._disposition(
                new,
                tool_call.field_id,
                SlotStatus.RECORDED,
                value=tool_call.value,
                source=tool_call.source.value,
            )

        elif isinstance(tool_call, AddFee):
            new.fees.append(tool_call.model_dump(exclude={"tool"}))
            self._disposition(new, "mandatory_fees", SlotStatus.RECORDED)

        elif isinstance(tool_call, AddTax):
            new.taxes.append(tool_call.model_dump(exclude={"tool"}))
            self._disposition(new, "taxes", SlotStatus.RECORDED)

        elif isinstance(tool_call, AddOwner):
            new.owners.append(tool_call.model_dump(exclude={"tool"}))
            self._disposition(new, "owners", SlotStatus.RECORDED)

        elif isinstance(tool_call, SkipQuestion):
            self._disposition(new, tool_call.field_id, SlotStatus.SKIPPED)

        elif isinstance(tool_call, FlagForCall1):
            if tool_call.field_id is not None:
                self._disposition(
                    new,
                    tool_call.field_id,
                    SlotStatus.FLAGGED,
                    flag_ref=tool_call.topic,
                )
            else:
                new.flags.append(tool_call.model_dump(exclude={"tool"}))

        elif isinstance(tool_call, EndSection):
            self._guard_end_section(new, tool_call.section_id)

        else:  # pragma: no cover - exhaustive over ToolCall union
            raise TypeError(f"Unknown tool call: {type(tool_call).__name__}")

        return new

    # --- echo-lifecycle observation (no value writes) ----------------------

    def observe(self, state: ProfileState, event: BaseModel) -> ProfileState:
        """Reduce an echo-lifecycle trace event into the ``echo_pending`` flag.

        Non echo-lifecycle events are a no-op (state returned unchanged), so the
        harness may feed every emitted trace event through ``observe`` uniformly.
        """
        if isinstance(event, EchoIssued):
            new = state.model_copy(deep=True)
            slot = new._slot(event.slot)
            slot.echo_pending = True
            new.slots[event.slot] = slot
            return new

        if isinstance(event, (UserConfirmed, UserCorrected)):
            new = state.model_copy(deep=True)
            slot = new._slot(event.slot)
            slot.echo_pending = False
            new.slots[event.slot] = slot
            return new

        return state

    # --- helpers -----------------------------------------------------------

    @staticmethod
    def _disposition(
        state: ProfileState,
        field_id: str,
        status: SlotStatus,
        *,
        value: Any = None,
        source: str | None = None,
        flag_ref: str | None = None,
    ) -> None:
        slot = state._slot(field_id)
        slot.status = status
        if value is not None:
            slot.value = value
        if source is not None:
            slot.source = source
        if flag_ref is not None:
            slot.flag_ref = flag_ref
        slot.echo_pending = False  # a committed write clears any pending echo
        state.slots[field_id] = slot

    def _guard_end_section(self, state: ProfileState, section_id: str) -> None:
        if self.frame is None:
            raise EndSectionError(
                "StateReducer was constructed without a frame; cannot validate "
                "end_section. Pass a FrameGraph to enable the §3.2 guard."
            )
        reachable = self.frame.reachable_slots(state.recorded_facts(), [section_id])
        offending: list[str] = []
        for slot_def in reachable:
            slot = state.slots.get(slot_def.id)
            if slot is None or slot.status not in _DISPOSITIONED:
                offending.append(slot_def.id)
            elif slot.echo_pending:
                offending.append(f"{slot_def.id}(echo_pending)")
        if offending:
            raise EndSectionError(
                f"end_section({section_id!r}) rejected: reachable in-scope slots not "
                f"dispositioned / echo pending: {sorted(offending)}"
            )
