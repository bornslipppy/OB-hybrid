"""System protocol + NextAction types (architecture §3.4).

The agent (Epic 3) and the tree (Epic 2) are two implementations of this one
protocol. The harness loop is system-agnostic: ask -> simulator answers -> policy
emits tool calls or the next question -> reduce -> repeat, until ``EndConversation``
or the 60 user-facing-turn cap (§8 invariant 7), which marks the run ``incomplete``.

Because neither system owns the tool surface, the reducer, or the trace, an outcome
difference between systems is provably attributable to the policy (D-1).
"""

from __future__ import annotations

from typing import Protocol, Union, runtime_checkable

from pydantic import BaseModel

from .state import ProfileState
from .tools import ToolCall


class UserQuestion(BaseModel):
    """The policy asks the simulated host a question."""

    text: str
    # Hint for the simulator's slot-keyed scripted lookup (FR-19 / EC-27). The Group A
    # simulator answers by which slot is targeted, not by sequence position.
    primary_slot: str | None = None


class EndConversation(BaseModel):
    """The policy declares the conversation complete."""

    reason: str


# A turn yields exactly one of: a question, a batch of tool calls, or termination.
NextAction = Union[UserQuestion, list[ToolCall], EndConversation]


@runtime_checkable
class System(Protocol):
    """A policy over the shared kernel. ``agent`` and ``tree`` both satisfy this."""

    system_id: str  # "agent" | "tree" — distinct provider/author, recorded per run

    def next_action(
        self,
        state: ProfileState,
        conversation_history: list[dict],
    ) -> NextAction: ...
