"""Interactive session step loop."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

import pytest

from harness.sales_notes import SalesAccount
from harness.session import StepKind, advance, create_session, submit_answer
from kernel.protocol import UserQuestion
from kernel.state import SlotStatus


@pytest.fixture
def root() -> Path:
    return Path(__file__).resolve().parent.parent


def test_create_session_with_sales_account_seeds_prefill(root: Path):
    account = SalesAccount(
        account_name="Demo Co",
        listing_count=3,
        opportunity_name="",
        opportunity_owner="Jordan",
        notes="From Hostaway. Wants GPO.",
    )
    session = create_session(
        system_id="agent",
        profile_id="live",
        config_path=root / "config/run_config.toml",
        root=root,
        sales_account=account,
    )
    assert session.sales_account is account
    assert session.state.slots["account_name"].status is SlotStatus.RECORDED
    assert session.state.slots["migration_source"].status is SlotStatus.PREFILLED_UNCONFIRMED


def test_submit_answer_auto_records_prefills_in_demo(root: Path):
    account = SalesAccount(
        account_name="Demo Co",
        listing_count=3,
        opportunity_name="",
        opportunity_owner="Jordan",
        notes="From Hostaway. Wants GPO.",
    )
    session = create_session(
        system_id="agent",
        profile_id="live",
        config_path=root / "config/run_config.toml",
        root=root,
        sales_account=account,
    )
    session.pending_question = UserQuestion(
        text="Sales noted Hostaway — still accurate?",
        primary_slot=None,
    )
    submit_answer(session, "Yes, that's still accurate.")
    assert session.state.slots["migration_source"].status is SlotStatus.RECORDED
    assert session.state.slots["addon_intent"].status is SlotStatus.RECORDED


def test_advance_waits_for_user_when_agent_asks(root: Path, monkeypatch: pytest.MonkeyPatch):
    account = SalesAccount(
        account_name="Demo Co",
        listing_count=3,
        opportunity_name="",
        opportunity_owner="Jordan",
        notes="From Hostaway.",
    )
    session = create_session(
        system_id="agent",
        profile_id="live",
        config_path=root / "config/run_config.toml",
        root=root,
        sales_account=account,
    )

    mock_system = MagicMock()
    mock_system.next_action.return_value = UserQuestion(
        text="Hello from the note.",
        primary_slot=None,
    )
    session.system = mock_system

    status = advance(session)
    assert status.kind is StepKind.WAITING
    assert status.question is not None
    assert session.pending_question is status.question
