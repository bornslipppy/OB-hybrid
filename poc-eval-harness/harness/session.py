"""Step-based interactive session for CLI and demo UI.

Wraps the same conversation loop as ``run_conversation``, but pauses when the
policy emits a ``UserQuestion`` so a human (terminal or web UI) can answer.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

from config.config_loader import load_run_config
from harness.account_context import (
    apply_demo_auto_confirm,
    build_demo_prompt_overlay,
    build_opening_user_message,
    seed_account_prefill,
)
from harness.profile_loader import make_dir_loader
from harness.providers import build_agent_client, load_env
from harness.runner import _MAX_ITERATIONS, _drain_trace_events
from harness.sales_notes import SalesAccount
from kernel.protocol import EndConversation, UserQuestion
from kernel.state import EndSectionError, ProfileState, SlotStatus, StateReducer
from kernel.schema import FrameGraph, SchemaLoader
from kernel.tools import ToolCall


class StepKind(str, Enum):
    WAITING = "waiting"
    DONE = "done"
    ERRORED = "errored"


@dataclass(frozen=True)
class StepStatus:
    kind: StepKind
    question: UserQuestion | None = None
    end_reason: str | None = None
    tool_calls: tuple[ToolCall, ...] = ()


@dataclass
class InteractiveSession:
    system: Any
    reducer: StateReducer
    state: ProfileState
    history: list[dict[str, Any]]
    max_turns: int
    profile_id: str
    persona_hint: str
    system_id: str
    sales_account: SalesAccount | None = None
    pending_question: UserQuestion | None = None
    end_reason: str | None = None
    recent_tool_calls: list[ToolCall] = field(default_factory=list)


def list_scored_profiles(root: Path) -> list[str]:
    scored_dir = root / "profiles/scored"
    if not scored_dir.is_dir():
        return []
    return sorted(p.stem for p in scored_dir.glob("*.json"))


def _resolve_path(root: Path, path: Path) -> Path:
    return path if path.is_absolute() else root / path


def _agent_system_prompt(root: Path, account_brief: str | None) -> str | None:
    """Merge sales-note context into the base prompt (works without AgentSystem.account_brief)."""
    if not account_brief:
        return None
    base_path = root / "agent/prompts/system_prompt.txt"
    base = base_path.read_text(encoding="utf-8")
    return f"{base}\n\n{account_brief}"


def create_session(
    *,
    system_id: str,
    profile_id: str,
    config_path: Path,
    root: Path,
    max_turns: int | None = None,
    sales_account: SalesAccount | None = None,
) -> InteractiveSession:
    load_env()
    config = load_run_config(config_path if config_path.is_absolute() else root / config_path)

    if sales_account is not None:
        persona = f"You represent {sales_account.account_name}. Answer as yourself using the sales note context."
        effective_profile_id = profile_id or "live-account"
    else:
        loader = make_dir_loader(_resolve_path(root, Path(config.scored_dir)))
        bundle = loader(profile_id)
        persona = bundle.spec.persona or "(no persona — answer as yourself)"
        effective_profile_id = profile_id

    schema_path = _resolve_path(root, config.schema_path)
    frame = FrameGraph(SchemaLoader().load(schema_path))
    reducer = StateReducer(frame=frame)
    demo_overlay = build_demo_prompt_overlay(sales_account) if sales_account else None
    opening_message = build_opening_user_message(sales_account) if sales_account else None

    if system_id == "agent":
        client = build_agent_client()
        from agent.agent import AgentSystem

        system: Any = AgentSystem(
            cursor_client=client,
            model=config.agent.model,
            schema_path=schema_path,
            system_prompt=_agent_system_prompt(root, demo_overlay),
            opening_user_message=opening_message,
            trace_writer=None,
        )
    elif system_id == "tree":
        from tree.tree import TreeSystem

        system = TreeSystem(schema_path=schema_path)
    else:
        raise ValueError(f"unknown system {system_id!r} (use agent or tree)")

    cap = max_turns if max_turns is not None else config.max_turns
    state = ProfileState(profile_id=effective_profile_id)
    if sales_account is not None:
        state = seed_account_prefill(state, sales_account)

    return InteractiveSession(
        system=system,
        reducer=reducer,
        state=state,
        history=[],
        max_turns=cap,
        profile_id=effective_profile_id,
        persona_hint=persona,
        system_id=system_id,
        sales_account=sales_account,
    )


def advance(session: InteractiveSession) -> StepStatus:
    """Run the policy until the next user question or session end."""
    if session.end_reason is not None:
        return StepStatus(kind=StepKind.DONE, end_reason=session.end_reason)
    if session.pending_question is not None:
        return StepStatus(kind=StepKind.WAITING, question=session.pending_question)

    session.recent_tool_calls = []
    tools_this_step: list[ToolCall] = []

    for _ in range(_MAX_ITERATIONS):
        if session.state.turn_count >= session.max_turns:
            session.end_reason = "incomplete_turn_cap"
            return StepStatus(kind=StepKind.DONE, end_reason=session.end_reason)

        action = session.system.next_action(session.state, session.history)
        session.state = _drain_trace_events(session.system, None, session.state, session.reducer)

        if isinstance(action, EndConversation):
            session.end_reason = action.reason
            return StepStatus(kind=StepKind.DONE, end_reason=session.end_reason, tool_calls=tuple(tools_this_step))

        if isinstance(action, UserQuestion):
            session.pending_question = action
            session.recent_tool_calls = tools_this_step
            return StepStatus(
                kind=StepKind.WAITING,
                question=action,
                tool_calls=tuple(tools_this_step),
            )

        if isinstance(action, list):
            for tc in action:
                tools_this_step.append(tc)
                session.recent_tool_calls.append(tc)
                try:
                    session.state = session.reducer.apply(session.state, tc)
                except EndSectionError:
                    pass
            continue

        session.end_reason = "errored"
        return StepStatus(kind=StepKind.ERRORED, end_reason=session.end_reason, tool_calls=tuple(tools_this_step))

    session.end_reason = "errored"
    return StepStatus(kind=StepKind.ERRORED, end_reason=session.end_reason, tool_calls=tuple(tools_this_step))


def submit_answer(session: InteractiveSession, text: str) -> None:
    """Record the user's reply and resume the conversation loop."""
    if session.pending_question is None:
        raise RuntimeError("no pending question")
    question = session.pending_question
    session.pending_question = None
    session.history.append({"role": "assistant", "content": question.text})
    session.history.append({"role": "user", "content": text})
    session.state = session.state.model_copy(update={"turn_count": session.state.turn_count + 1})
    if session.sales_account is not None:
        session.state = apply_demo_auto_confirm(
            session.state,
            user_text=text,
            question=question,
            reducer=session.reducer,
        )


def run_to_completion(session: InteractiveSession, simulator: Any) -> tuple[ProfileState, str]:
    """Blocking loop for CLI — same semantics as the old ``run_conversation`` path."""
    while True:
        status = advance(session)
        if status.kind is StepKind.WAITING and status.question is not None:
            reply = simulator.reply(status.question)
            submit_answer(session, reply)
            continue
        end_reason = status.end_reason or session.end_reason or "errored"
        return session.state, end_reason


def format_summary(state: ProfileState, end_reason: str) -> str:
    recorded = [fid for fid, s in state.slots.items() if s.status is SlotStatus.RECORDED]
    skipped = [fid for fid, s in state.slots.items() if s.status is SlotStatus.SKIPPED]
    flagged = [fid for fid, s in state.slots.items() if s.status is SlotStatus.FLAGGED]

    lines = [
        f"Session ended: {end_reason}  (turns: {state.turn_count})",
    ]
    if recorded:
        lines.append(f"Recorded ({len(recorded)}): {', '.join(sorted(recorded))}")
    if skipped:
        lines.append(f"Skipped ({len(skipped)}): {', '.join(sorted(skipped))}")
    if flagged:
        lines.append(f"Flagged ({len(flagged)}): {', '.join(sorted(flagged))}")
    if state.owners:
        lines.append(f"Owners: {len(state.owners)} record(s)")
    if state.fees:
        lines.append(f"Fees: {len(state.fees)} record(s)")
    if state.taxes:
        lines.append(f"Taxes: {len(state.taxes)} record(s)")
    return "\n".join(lines)


def format_tool_call(tc: ToolCall) -> str:
    args = tc.model_dump(exclude={"tool"})
    inner = ", ".join(f"{k}={v!r}" for k, v in args.items())
    return f"{tc.tool}({inner})"
