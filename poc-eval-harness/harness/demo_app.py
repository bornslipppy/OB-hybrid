"""Streamlit stakeholder demo — chat UI over the interactive onboarding session.

Usage::

    cd poc-eval-harness
    export SALES_NOTES_XLSX="/path/to/Notes for Tamar....xlsx"
    uv sync --extra demo
    uv run streamlit run harness/demo_app.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st  # noqa: E402

from config.config_loader import load_run_config  # noqa: E402
from harness.account_context import build_account_brief, suggested_replies  # noqa: E402
from harness.providers import load_env  # noqa: E402
from harness.sales_notes import (  # noqa: E402
    SalesAccount,
    get_account,
    list_account_names,
    resolve_notes_path,
    search_accounts,
)
from harness.session import (  # noqa: E402
    StepKind,
    advance,
    create_session,
    format_summary,
    format_tool_call,
    list_scored_profiles,
    submit_answer,
)

CONFIG_PATH = ROOT / "config/run_config.toml"


def _init_state() -> None:
    defaults = {
        "phase": "setup",
        "session": None,
        "messages": [],
        "tool_log": [],
        "end_reason": None,
        "final_state": None,
        "account_search": "",
        "notes_xlsx_path": "",
        "pending_chip_reply": "",
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)


def _notes_path() -> Path | None:
    override = st.session_state.get("notes_xlsx_path", "").strip()
    if override:
        return resolve_notes_path(override)
    return resolve_notes_path()


def _render_sidebar() -> tuple[str, str, int, bool, bool, SalesAccount | None]:
    config = load_run_config(CONFIG_PATH)
    notes_path = _notes_path()

    st.sidebar.header("Session")
    system_id = st.sidebar.selectbox("System", ["agent"], index=0)
    default_turns = 40 if notes_path is not None else config.max_turns
    max_turns = st.sidebar.number_input(
        "Max turns",
        min_value=1,
        max_value=120,
        value=default_turns,
    )
    show_tools = st.sidebar.checkbox("Show tool calls (dev)", value=False)
    show_suggested = st.sidebar.checkbox("Suggested replies", value=True)

    sales_account: SalesAccount | None = None
    profile_id = "live"

    if notes_path is not None:
        st.sidebar.subheader("Salesforce account")
        st.sidebar.caption(f"Notes: `{notes_path.name}` ({len(list_account_names(notes_path))} accounts)")

        search = st.sidebar.text_input(
            "Search account",
            value=st.session_state.account_search,
            placeholder="e.g. City and Coastal",
        )
        st.session_state.account_search = search

        matches = search_accounts(notes_path, search, limit=30)
        if not matches and search.strip():
            st.sidebar.warning("No accounts match — try a shorter name.")
        elif matches:
            labels = [
                f"{a.account_name} ({a.listing_count or '?'} listings)"
                for a in matches
            ]
            pick = st.sidebar.selectbox("Account", labels, index=0)
            picked_name = matches[labels.index(pick)].account_name
            sales_account = get_account(notes_path, picked_name)
            if sales_account:
                with st.sidebar.expander("Handover note", expanded=False):
                    st.text(sales_account.notes or "(empty)")
                with st.sidebar.expander("Agent brief preview", expanded=False):
                    st.markdown(build_account_brief(sales_account))
    else:
        st.sidebar.subheader("Sales notes file")
        st.sidebar.caption(
            "Point to your Tamar export (.xlsx). It is loaded locally and never committed to git."
        )
        default_path = st.session_state.notes_xlsx_path or str(
            resolve_notes_path() or Path.home() / "Downloads" / "Notes for Tamar-2026-06-02-13-51-50 (1).xlsx"
        )
        path_input = st.sidebar.text_input(
            "Workbook path",
            value=default_path,
            placeholder="/path/to/Notes for Tamar....xlsx",
        )
        st.session_state.notes_xlsx_path = path_input.strip()
        retry = resolve_notes_path(path_input) if path_input.strip() else None
        if retry is not None:
            st.sidebar.success(f"Found: `{retry.name}`")
            st.rerun()
        else:
            st.sidebar.error("File not found — check the path above.")
        profiles = list_scored_profiles(ROOT) or ["A1"]
        profile_id = st.sidebar.selectbox(
            "Synthetic profile (fallback until workbook loads)",
            profiles,
            index=profiles.index("A1") if "A1" in profiles else 0,
        )

    if st.sidebar.button("Start session", type="primary"):
        _start_session(system_id, profile_id, int(max_turns), show_tools, sales_account)

    return system_id, profile_id, int(max_turns), show_tools, show_suggested, sales_account


def _start_session(
    system_id: str,
    profile_id: str,
    max_turns: int,
    show_tools: bool,
    sales_account: SalesAccount | None,
) -> None:
    st.session_state.phase = "chatting"
    st.session_state.messages = []
    st.session_state.tool_log = []
    st.session_state.end_reason = None
    st.session_state.final_state = None

    session = create_session(
        system_id=system_id,
        profile_id=profile_id,
        config_path=CONFIG_PATH,
        root=ROOT,
        max_turns=max_turns,
        sales_account=sales_account,
    )
    st.session_state.session = session

    with st.spinner("Agent reading sales note…"):
        status = advance(session)
    _apply_status(status, show_tools)


def _apply_status(status, show_tools: bool) -> None:
    session = st.session_state.session
    if status.tool_calls and show_tools:
        for tc in status.tool_calls:
            st.session_state.tool_log.append(format_tool_call(tc))

    if status.kind is StepKind.WAITING and status.question is not None:
        st.session_state.messages.append(
            {
                "role": "assistant",
                "text": status.question.text,
                "slot": status.question.primary_slot,
            }
        )
        return

    if status.kind in {StepKind.DONE, StepKind.ERRORED}:
        st.session_state.phase = "done"
        st.session_state.end_reason = status.end_reason or session.end_reason or "errored"
        st.session_state.final_state = session.state


def _handle_user_send(user_text: str, show_tools: bool) -> None:
    session = st.session_state.session
    if not user_text.strip() or session is None or st.session_state.phase != "chatting":
        return

    st.session_state.messages.append({"role": "user", "text": user_text.strip()})
    submit_answer(session, user_text.strip())

    with st.spinner("Agent thinking…"):
        status = advance(session)
    _apply_status(status, show_tools)


def main() -> None:
    st.set_page_config(page_title="Onboarding Demo", page_icon="💬", layout="centered")
    load_env()
    _init_state()

    st.title("Onboarding Demo")
    st.caption("Pick a Salesforce account — the agent confirms from the sales note instead of cold questions.")

    system_id, profile_id, max_turns, show_tools, show_suggested, sales_account = _render_sidebar()

    session = st.session_state.session
    if session is None:
        if sales_account:
            st.info("Account selected in the sidebar — click **Start session**.")
            config = load_run_config(CONFIG_PATH)
            st.markdown(
                f"**Ready:** `{sales_account.account_name}` · "
                f"{sales_account.listing_count or '?'} listings · "
                f"model `{config.agent.model}`"
            )
        elif _notes_path() is None:
            st.info(
                "In the **sidebar**, paste the path to your Tamar `.xlsx` export. "
                "When the file is found, the **Account** search box appears."
            )
        else:
            st.info("Search for an account in the **sidebar**, then click **Start session**.")
        return

    if session.sales_account:
        st.markdown(f"**Account:** {session.sales_account.account_name}")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["text"])
            if msg["role"] == "assistant" and msg.get("slot") and show_tools:
                st.caption(f"slot: {msg['slot']}")
            if msg["role"] == "assistant" and session.persona_hint and not session.sales_account:
                with st.expander("Persona hint", expanded=False):
                    st.caption(session.persona_hint)

    if show_tools and st.session_state.tool_log:
        with st.expander("Tool calls", expanded=False):
            for line in st.session_state.tool_log:
                st.code(line, language=None)

    if st.session_state.phase == "done" and st.session_state.final_state is not None:
        st.success("Session complete")
        st.text(format_summary(st.session_state.final_state, st.session_state.end_reason or "completed"))
        return

    if st.session_state.phase == "chatting" and session.pending_question is not None:
        chips: list[str] = []
        if show_suggested and session.sales_account is not None:
            chips = suggested_replies(
                session.sales_account,
                question_text=session.pending_question.text,
                primary_slot=session.pending_question.primary_slot,
                turn_count=session.state.turn_count,
                state=session.state,
            )
            if chips:
                chip_cols = st.columns(len(chips))
                for idx, label in enumerate(chips):
                    if chip_cols[idx].button(label, key=f"chip_{len(st.session_state.messages)}_{idx}"):
                        st.session_state.pending_chip_reply = label

        if st.session_state.pending_chip_reply:
            reply = st.session_state.pending_chip_reply
            st.session_state.pending_chip_reply = ""
            _handle_user_send(reply, show_tools)
            st.rerun()

        if prompt := st.chat_input("Your answer…"):
            _handle_user_send(prompt, show_tools)
            st.rerun()


if __name__ == "__main__":
    main()
