"""Story 4.1 / 4.2 — UserSimulator unit tests.

What these tests verify:
  1. RespondentSpec rejects answer-key fields (FR-19/FR-20 fairness invariant).
  2. Group A scripted mode: slot-keyed lookup, variant overrides, fallback.
  3. LLM mode requires a Gemini client — scripted Group A never calls LLM.
  4. The scripted turns yaml is loadable and has expected keys.
  5. reply() in scripted mode never fabricates facts absent from the spec.
  6. reset() clears conversation history.
  7. Simulator mode auto-detects from group; can be overridden.
"""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from kernel.protocol import UserQuestion
from simulator.simulator import RespondentSpec, SimulatorMode, UserSimulator

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

A1_FACTS = {
    "listing_count": 5,
    "channels": ["airbnb", "vrbo", "direct"],
    "go_live": "asap",
    "ownership_model": "all_self_owned",
    "revenue_recognition": "check_in",
    "non_refundable_enabled": False,
    "security_deposit_type": "damage_waiver",
    "security_deposit_amount": 50,
    "payment_timing": "at_booking",
    "mandatory_fees": [],
    "focus_topics": ["pricing_strategy", "guest_messaging"],
    "pain": "Manual pricing takes too much time.",
    "website_brand_name": "Harbor Point Stays",
}

A2_FACTS = {
    "listing_count": 8,
    "channels": ["airbnb", "direct"],
    "go_live": "2-4w",
    "ownership_model": "all_managed_for_others",
    "payment_timing": "split",
    "payment_split": "50_50",
    "focus_topics": ["owner_reporting"],
}

A2_VARIANT_OVERRIDES = {
    "listing_count": "Eight listings across two properties.",
    "channels": "Airbnb and direct bookings — we don't use VRBO.",
    "ownership_model": "I manage properties for two other owners.",
    "website_brand_name": None,
    "website_domain": None,
}

B1_FACTS = {
    "listing_count": 3,
    "channels": ["airbnb", "direct"],
    "payment_timing": "split",
    "payment_split": "50_50",
    "note": "Depends on channel — Airbnb collects, I take 50% for direct",
}


@pytest.fixture
def a1_spec() -> RespondentSpec:
    return RespondentSpec(
        profile_id="A1",
        group="A",
        facts=A1_FACTS,
        persona="Cooperative, organized, answers directly.",
    )


@pytest.fixture
def a2_spec() -> RespondentSpec:
    return RespondentSpec(
        profile_id="A2",
        group="A",
        facts=A2_FACTS,
        persona="Cooperative, uses professional vocabulary.",
        variant_overrides=A2_VARIANT_OVERRIDES,
    )


@pytest.fixture
def b1_spec() -> RespondentSpec:
    return RespondentSpec(
        profile_id="B1",
        group="B",
        facts=B1_FACTS,
        persona="Slightly technical; answers in full sentences.",
    )


@pytest.fixture
def mock_gemini() -> MagicMock:
    """A _GeminiLike callable factory mock.

    ``mock_gemini(system_instruction)`` → mock model whose
    ``generate_content(contents, ...).text`` returns ``"Mock LLM reply"``.
    """
    mock_model = MagicMock()
    mock_model.generate_content.return_value.text = "Mock LLM reply"
    factory = MagicMock(return_value=mock_model)
    return factory


# ---------------------------------------------------------------------------
# RespondentSpec validation
# ---------------------------------------------------------------------------


class TestRespondentSpecValidation:
    def test_rejects_answer_key_field(self):
        with pytest.raises(ValueError, match="answer-key"):
            RespondentSpec(
                profile_id="X",
                group="A",
                facts={"answer_key": {"listing_count": "recorded:5"}},
            )

    def test_rejects_dispositions_field(self):
        with pytest.raises(ValueError, match="answer-key"):
            RespondentSpec(
                profile_id="X",
                group="A",
                facts={"dispositions": {}},
            )

    def test_accepts_clean_facts(self, a1_spec):
        assert a1_spec.profile_id == "A1"
        assert a1_spec.facts["listing_count"] == 5


# ---------------------------------------------------------------------------
# SimulatorMode auto-detection
# ---------------------------------------------------------------------------


class TestSimulatorModeDetection:
    def test_group_a_defaults_to_scripted(self, a1_spec):
        sim = UserSimulator(a1_spec)
        assert sim.mode is SimulatorMode.SCRIPTED

    def test_group_b_defaults_to_llm_mode(self, b1_spec, mock_gemini):
        sim = UserSimulator(b1_spec, gemini_client=mock_gemini)
        assert sim.mode is SimulatorMode.LLM

    def test_group_b_without_client_raises(self, b1_spec):
        with pytest.raises(ValueError, match="gemini_client"):
            UserSimulator(b1_spec)

    def test_mode_can_be_overridden_to_scripted(self, b1_spec):
        sim = UserSimulator(b1_spec, mode=SimulatorMode.SCRIPTED)
        assert sim.mode is SimulatorMode.SCRIPTED


# ---------------------------------------------------------------------------
# Group A scripted replies
# ---------------------------------------------------------------------------


class TestGroupAScriptedReplies:
    def test_listing_count_reply(self, a1_spec):
        sim = UserSimulator(a1_spec)
        q = UserQuestion(text="How many listings do you have?", primary_slot="listing_count")
        reply = sim.reply(q)
        assert "5" in reply, "A1 listing_count reply must mention 5"

    def test_channels_reply(self, a1_spec):
        sim = UserSimulator(a1_spec)
        q = UserQuestion(text="Which booking channels do you use?", primary_slot="channels")
        reply = sim.reply(q)
        assert reply  # must return something non-empty
        # For A1, channels include Airbnb, VRBO, direct
        lower = reply.lower()
        assert any(ch in lower for ch in ("airbnb", "vrbo", "direct"))

    def test_ownership_model_for_self_owned(self, a1_spec):
        sim = UserSimulator(a1_spec)
        q = UserQuestion(text="Tell me about your ownership structure.", primary_slot="ownership_model")
        reply = sim.reply(q)
        lower = reply.lower()
        assert "self" in lower or "own" in lower

    def test_payment_split_not_applicable_for_a1(self, a1_spec):
        sim = UserSimulator(a1_spec)
        q = UserQuestion(text="How do you split payments?", primary_slot="payment_split")
        reply = sim.reply(q)
        # payment_split is None in group_a.yaml (at_booking profile)
        assert reply  # should return the not-applicable response, not crash

    def test_unknown_slot_returns_fallback(self, a1_spec):
        sim = UserSimulator(a1_spec)
        q = UserQuestion(text="What is your CRM system?", primary_slot="crm_vendor")
        reply = sim.reply(q)
        assert reply  # should not crash

    def test_no_primary_slot_returns_fallback(self, a1_spec):
        sim = UserSimulator(a1_spec)
        q = UserQuestion(text="Anything else to add?", primary_slot=None)
        reply = sim.reply(q)
        assert reply

    def test_a2_variant_override_listing_count(self, a2_spec):
        sim = UserSimulator(a2_spec)
        q = UserQuestion(text="How many listings?", primary_slot="listing_count")
        reply = sim.reply(q)
        assert "eight" in reply.lower() or "8" in reply, "A2 variant must use A2 listing count"

    def test_a2_variant_override_none_returns_not_applicable(self, a2_spec):
        sim = UserSimulator(a2_spec)
        q = UserQuestion(text="What's your website brand?", primary_slot="website_brand_name")
        reply = sim.reply(q)
        # A2 has None override for website_brand_name → not applicable
        assert reply  # should not crash; return "not applicable" reply

    def test_mandatory_fees_a1_returns_no_account_level_fees(self, a1_spec):
        """Regression: A1 mandatory_fees reply must NOT mention a resort fee or any dollar amount.

        Previously the slot was missing from group-a.yaml, causing unknown_slot fallback
        ("I'm not sure exactly what you're asking. Can you rephrase?"). The agent then
        hallucinated a $25 resort fee, echoed it, and looped waiting for confirmation that
        never came because each re-ask of mandatory_fees returned the fallback again.
        """
        sim = UserSimulator(a1_spec)
        q = UserQuestion(text="Do you charge any mandatory fees to guests?", primary_slot="mandatory_fees")
        reply = sim.reply(q)
        lower = reply.lower()
        assert reply, "mandatory_fees reply must be non-empty"
        assert "rephrase" not in lower, (
            "mandatory_fees must not fall through to unknown_slot; add it to group-a.yaml"
        )
        assert "$" not in reply and "resort" not in lower, (
            "A1 has no account-level mandatory fees — reply must not fabricate a resort fee"
        )
        # The reply should communicate that cleaning fees are per-listing, not account-level
        assert "cleaning" in lower or "listing" in lower or "no" in lower or "nothing" in lower, (
            "A1 mandatory_fees reply should clarify there are no account-level fees"
        )

    def test_mandatory_fees_more_returns_closure(self, a1_spec):
        """After confirming no more fees, simulator must return a closing reply, not unknown_slot."""
        sim = UserSimulator(a1_spec)
        q = UserQuestion(text="Any other fees to add?", primary_slot="mandatory_fees_more")
        reply = sim.reply(q)
        lower = reply.lower()
        assert reply, "mandatory_fees_more reply must be non-empty"
        assert "rephrase" not in lower, "mandatory_fees_more must not hit unknown_slot fallback"


# ---------------------------------------------------------------------------
# LLM path (mocked)
# ---------------------------------------------------------------------------


class TestLLMSimulatorPath:
    def test_llm_reply_calls_gemini(self, b1_spec, mock_gemini):
        sim = UserSimulator(b1_spec, gemini_client=mock_gemini)
        q = UserQuestion(text="How do you handle payment timing?", primary_slot="payment_timing")
        reply = sim.reply(q)
        assert reply == "Mock LLM reply"
        mock_gemini.assert_called_once()  # factory called once to build the model

    def test_llm_system_prompt_excludes_answer_key(self, b1_spec, mock_gemini):
        """The system instruction passed to the Gemini factory must not contain answer-key fields."""
        sim = UserSimulator(b1_spec, gemini_client=mock_gemini)
        q = UserQuestion(text="Tell me about your listings.", primary_slot=None)
        sim.reply(q)
        system_instruction = mock_gemini.call_args.args[0]
        assert "answer_key" not in system_instruction.lower()
        assert "disposition" not in system_instruction.lower()

    def test_llm_history_accumulates(self, b1_spec, mock_gemini):
        sim = UserSimulator(b1_spec, gemini_client=mock_gemini, mode=SimulatorMode.LLM)
        sim.reply(UserQuestion(text="First question", primary_slot=None))
        sim.reply(UserQuestion(text="Second question", primary_slot=None))
        assert len(sim._history) == 4  # 2x (user + assistant)

    def test_reset_clears_history(self, b1_spec, mock_gemini):
        sim = UserSimulator(b1_spec, gemini_client=mock_gemini)
        sim.reply(UserQuestion(text="Hello", primary_slot=None))
        sim.reset()
        assert sim._history == []


# ---------------------------------------------------------------------------
# Scripted turns YAML load
# ---------------------------------------------------------------------------


class TestScriptedTurnsYaml:
    def test_yaml_loads_without_error(self, a1_spec):
        sim = UserSimulator(a1_spec)
        assert isinstance(sim._scripted, dict)
        assert len(sim._scripted) > 0

    def test_yaml_has_unknown_slot_fallback(self, a1_spec):
        sim = UserSimulator(a1_spec)
        assert "unknown_slot" in sim._scripted

    def test_yaml_has_key_schema_slots(self, a1_spec):
        sim = UserSimulator(a1_spec)
        required_slots = {"listing_count", "channels", "ownership_model", "payment_timing", "taxes"}
        for slot in required_slots:
            assert slot in sim._scripted, f"group_a.yaml must have an entry for '{slot}'"

    def test_yaml_a2_overrides_not_flattened(self, a1_spec):
        sim = UserSimulator(a1_spec)
        # a2_overrides is a sub-dict and must NOT appear as a top-level scripted key
        assert "a2_overrides" not in sim._scripted
