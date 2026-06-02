"""Shared neutral kernel for the AI Adaptive Onboarding PoC eval harness.

Authored by the neutral harness engineer (FR-10 / architecture R-8). This package
is frozen and version-tagged before either ``agent/`` (Epic 3) or ``tree/``
(Epic 2) is touched; both import this surface read-only and nothing else.

Public surface (architecture §10.2):
  - tools:    the 7 ToolCall models + union + JSON-schema export
  - state:    SlotStatus, SlotState, ProfileState, StateReducer
  - trace:    the trace event schema + TraceWriter / TraceReader
  - protocol: System protocol + NextAction types
  - llm:      scored_completion / glue_completion / simulator_completion
  - schema:   SchemaLoader + FrameGraph
"""

from __future__ import annotations

from .protocol import (
    EndConversation,
    NextAction,
    System,
    UserQuestion,
)
from .schema import FrameGraph, SchemaLoader, SlotDef
from .state import ProfileState, SlotState, SlotStatus, StateReducer
from .tools import (
    AddFee,
    AddOwner,
    AddTax,
    EndSection,
    FlagForCall1,
    RecordAnswer,
    SkipQuestion,
    Source,
    ToolCall,
    parse_tool_call,
    to_anthropic_tools,
)
from .trace import (
    EchoIssued,
    SessionEnd,
    ToolCallEvent,
    TraceEvent,
    TraceReader,
    TraceWriter,
    UserConfirmed,
    UserCorrected,
    UserFacingQuestion,
    ValueIntroduced,
)

__all__ = [
    # tools
    "RecordAnswer",
    "AddFee",
    "AddTax",
    "AddOwner",
    "SkipQuestion",
    "FlagForCall1",
    "EndSection",
    "Source",
    "ToolCall",
    "parse_tool_call",
    "to_anthropic_tools",
    # state
    "SlotStatus",
    "SlotState",
    "ProfileState",
    "StateReducer",
    # trace
    "UserFacingQuestion",
    "ValueIntroduced",
    "EchoIssued",
    "UserConfirmed",
    "UserCorrected",
    "ToolCallEvent",
    "SessionEnd",
    "TraceEvent",
    "TraceWriter",
    "TraceReader",
    # protocol
    "System",
    "UserQuestion",
    "EndConversation",
    "NextAction",
    # schema
    "SchemaLoader",
    "FrameGraph",
    "SlotDef",
]
