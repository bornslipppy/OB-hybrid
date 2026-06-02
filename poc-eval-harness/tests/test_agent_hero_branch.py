"""Story 3.4 — Hero-branch ownership fan-out (intent-capture only).

Acceptance criteria tested here (Epic 3 / Story 3.4):

1. Owner fields (name, email, listings, share, management_model + economics) are
   captured via add_owner and score against `recorded:<value>`.
2. No BusinessModel creation appears in the tool trace.
3. Captured owner economics are accompanied by flag_for_call_1 with owner context.
4. who_pays_channel_commission is captured DISTINCTLY from pmc_commission_rate.
5. The agent asks "how do you get paid for managing these?" not "Business Models."
6. owners slot is IN scope when ownership_model in {all_managed_for_others, mixed}.
7. owners slot is OUT of scope when ownership_model = all_self_owned.
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from agent.agent import AgentSystem
from kernel.schema import FrameGraph, SchemaLoader
from kernel.state import ProfileState
from kernel.tools import AddOwner, FlagForCall1

SCHEMA_PATH = Path(__file__).resolve().parents[1] / "schema" / "guesty-pro-account-creation-schema.md"
_ALL_SECTIONS = ["S0a", "S0b", "S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8"]


def _make_agent() -> AgentSystem:
    return AgentSystem(
        cursor_client=MagicMock(),
        model="claude-test",
        schema_path=SCHEMA_PATH,
        system_prompt="Test agent.",
    )


# ---------------------------------------------------------------------------
# 1. owners slot reachability based on ownership_model
# ---------------------------------------------------------------------------


class TestOwnerSlotReachability:
    """FrameGraph must correctly gate owners on ownership_model (Story 3.4 / FR-3)."""

    @pytest.fixture(scope="class")
    def frame(self) -> FrameGraph:
        return FrameGraph(SchemaLoader().load(SCHEMA_PATH))

    def test_owners_in_scope_for_all_managed(self, frame):
        facts = {"ownership_model": "all_managed_for_others"}
        reachable = frame.reachable_slots(facts, ["S8"])
        assert "owners" in {s.id for s in reachable}

    def test_owners_in_scope_for_mixed(self, frame):
        facts = {"ownership_model": "mixed"}
        reachable = frame.reachable_slots(facts, ["S8"])
        assert "owners" in {s.id for s in reachable}

    def test_owners_NOT_in_scope_for_all_self_owned(self, frame):
        facts = {"ownership_model": "all_self_owned"}
        reachable = frame.reachable_slots(facts, ["S8"])
        assert "owners" not in {s.id for s in reachable}

    def test_owners_csv_in_scope_for_managed(self, frame):
        facts = {"ownership_model": "all_managed_for_others"}
        reachable = frame.reachable_slots(facts, ["S8"])
        assert "owners_csv" in {s.id for s in reachable}

    def test_owners_csv_NOT_in_scope_for_self_owned(self, frame):
        facts = {"ownership_model": "all_self_owned"}
        reachable = frame.reachable_slots(facts, ["S8"])
        assert "owners_csv" not in {s.id for s in reachable}


# ---------------------------------------------------------------------------
# 2. add_owner tool structure (FR-3 / Story 3.4)
# ---------------------------------------------------------------------------


class TestAddOwnerToolShape:
    """add_owner carries the full per-owner item_shape with management_model discrimination."""

    def test_add_owner_commission_model(self):
        """commission management_model: pmc_commission_rate must be populated."""
        owner = AddOwner(
            owner_name="Alice",
            email="alice@example.com",
            listings=["listing-1", "listing-2"],
            ownership_share=None,
            management_model="commission",
            pmc_commission_rate=20.0,
            who_pays_channel_commission="pmc",
        )
        assert owner.management_model == "commission"
        assert owner.pmc_commission_rate == 20.0
        assert owner.who_pays_channel_commission == "pmc"
        # split_terms must be None for commission model.
        assert owner.split_terms is None

    def test_add_owner_fixed_fee_model(self):
        owner = AddOwner(
            owner_name="Bob",
            email="bob@example.com",
            listings=["listing-3"],
            management_model="fixed_fee",
            fixed_fee_amount=500.0,
            who_pays_channel_commission="owner",
        )
        assert owner.fixed_fee_amount == 500.0
        assert owner.split_terms is None

    def test_add_owner_revenue_split_model(self):
        owner = AddOwner(
            owner_name="Carol",
            email="carol@example.com",
            listings=["listing-4"],
            management_model="revenue_split",
            split_terms="70% after platform fees",
        )
        assert owner.split_terms == "70% after platform fees"
        assert owner.pmc_commission_rate is None

    def test_add_owner_other_model(self):
        owner = AddOwner(
            owner_name="Dana",
            email="dana@example.com",
            listings=["listing-5"],
            management_model="other",
            split_terms="Negotiated case-by-case",
        )
        assert owner.management_model == "other"
        assert owner.split_terms is not None

    def test_add_owner_rejects_wrong_economics_for_model(self):
        """The kernel enforces depends_on: pmc_commission_rate must not appear on fixed_fee."""
        from pydantic import ValidationError

        with pytest.raises(ValidationError, match="pmc_commission_rate"):
            AddOwner(
                owner_name="Bad",
                email="bad@example.com",
                listings=["listing-x"],
                management_model="fixed_fee",
                pmc_commission_rate=20.0,  # invalid for fixed_fee
            )

    def test_who_pays_channel_commission_is_independent(self):
        """who_pays_channel_commission (Channel Commission / OTA fee) is distinct
        from pmc_commission_rate (PMC management commission) and is always optional."""
        owner_with = AddOwner(
            owner_name="E",
            email="e@e.com",
            listings=["l1"],
            management_model="commission",
            pmc_commission_rate=15.0,
            who_pays_channel_commission="split",
        )
        owner_without = AddOwner(
            owner_name="F",
            email="f@f.com",
            listings=["l2"],
            management_model="commission",
            pmc_commission_rate=15.0,
            who_pays_channel_commission=None,
        )
        assert owner_with.who_pays_channel_commission == "split"
        assert owner_without.who_pays_channel_commission is None


# ---------------------------------------------------------------------------
# 3. Hero branch present in system prompt (Story 3.4)
# ---------------------------------------------------------------------------


class TestHeroBranchSystemPrompt:
    @pytest.fixture(scope="class")
    def prompt_text(self) -> str:
        from agent.agent import _SYSTEM_PROMPT_PATH

        return _SYSTEM_PROMPT_PATH.read_text(encoding="utf-8")

    def test_no_business_model_write_instruction(self, prompt_text):
        """System prompt must explicitly say NOT to write BusinessModel records."""
        assert "NEVER write BusinessModel" in prompt_text or \
               "never write BusinessModel" in prompt_text.lower() or \
               "Never write BusinessModel" in prompt_text

    def test_plain_language_phrasing(self, prompt_text):
        """System prompt must instruct agent to use 'how do you get paid for managing these?'."""
        assert "how do you get paid for managing these" in prompt_text.lower()

    def test_intent_capture_flagging_instruction(self, prompt_text):
        """System prompt must instruct the agent to flag_for_call_1 for owner context."""
        assert "flag_for_call_1" in prompt_text
        assert "Jordan" in prompt_text

    def test_owner_economics_echo_instruction(self, prompt_text):
        """Owner economics (numbers/formulas) must be subject to echo-before-write."""
        assert "echo" in prompt_text.lower()
        assert ("commission_rate" in prompt_text or "pmc_commission_rate" in prompt_text or
                "fixed_fee_amount" in prompt_text)

    def test_channel_commission_distinction(self, prompt_text):
        """The two commission concepts must be EXPLICITLY distinguished in the prompt."""
        assert "who_pays_channel_commission" in prompt_text
        assert "pmc_commission_rate" in prompt_text or "PMC management commission" in prompt_text


# ---------------------------------------------------------------------------
# 4. Agent emits add_owner from LLM response (structural routing)
# ---------------------------------------------------------------------------


class TestAgentEmitsAddOwner:
    def test_add_owner_returned_as_tool_call_list(self):
        """When the LLM emits an add_owner block, next_action must return list[AddOwner]."""
        agent = AgentSystem(
            cursor_client=MagicMock(),
            model="claude-test",
            schema_path=SCHEMA_PATH,
            system_prompt="Test.",
        )
        agent._messages = [{"role": "assistant", "content": "What are the owner details?"}]

        owner_tool = AddOwner(
            owner_name="Alice",
            email="alice@example.com",
            listings=["prop-1"],
            management_model="commission",
            pmc_commission_rate=20.0,
            who_pays_channel_commission="pmc",
        )
        flag_tool = FlagForCall1(
            topic="Owner Alice economics",
            user_quote="20% commission, PMC pays channel",
            note="Alice: commission 20%, PMC pays channel commission",
            field_id="owners",
        )

        with patch("agent.agent.scored_completion",
                   return_value=("", [owner_tool, flag_tool])):
            state = ProfileState(profile_id="hero_test")
            action = agent.next_action(state, [{"role": "user", "content": "Alice, 20%"}])

        assert isinstance(action, list)
        assert len(action) == 2
        assert isinstance(action[0], AddOwner)
        assert isinstance(action[1], FlagForCall1)
        assert action[0].owner_name == "Alice"
        assert action[0].pmc_commission_rate == 20.0
        assert action[1].field_id == "owners"

    def test_no_business_model_tool_exists(self):
        """There must be no 'create_business_model' or similar tool in the tool defs.
        The 7 fixed tools are the only path into state — free writes are impossible (FR-2)."""
        agent = _make_agent()
        tool_names = {t["function"]["name"] for t in agent._tool_defs}
        # None of these must exist.
        forbidden = {
            "create_business_model",
            "write_business_model",
            "record_business_model",
            "create_owner_model",
        }
        overlap = forbidden & tool_names
        assert not overlap, f"Forbidden tool names found: {overlap}"
