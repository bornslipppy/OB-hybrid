"""Story 4.4 — run_fn factory wires system + simulator + scoring into a RunRecord."""

from __future__ import annotations

import asyncio
import json
from pathlib import Path

from config.config_loader import load_run_config
from harness.profile_loader import (
    DEFAULT_H1_SECTIONS,
    ProfileBundle,
    load_profile,
    make_dir_loader,
)
from harness.records import RunStatus
from harness.runner import RunContext
from harness.wiring import make_run_fn
from kernel.protocol import EndConversation, UserQuestion
from kernel.tools import RecordAnswer
from kernel.trace import EchoIssued, ValueIntroduced
from scoring.sar import AnswerKey
from simulator.simulator import RespondentSpec

_CONFIG = Path(__file__).resolve().parents[1] / "config" / "run_config.toml"
_FIXTURE = Path(__file__).resolve().parent / "fixtures" / "profile_dev_a1.json"


def _ctx(tmp_path, system_id, profile_id="FAKE", tag="tuning") -> RunContext:
    return RunContext(
        manifest_hash="hsh",
        profile_id=profile_id,
        system_id=system_id,
        run_index=0,
        seed=42,
        campaign_dir=tmp_path / "campaign",
        tag=tag,
    )


class _FakeSim:
    def reply(self, q):
        return "yes"


class _FakeSystem:
    """Echoes a deposit then writes WITHOUT a confirmation → a false write (fail-safe)."""

    system_id = "agent"

    def __init__(self):
        self._step = 0
        self._pending = []

    def next_action(self, state, history):
        s, self._step = self._step, self._step + 1
        if s == 0:
            self._pending = [
                ValueIntroduced(turn=state.turn_count, slot="security_deposit_amount", subfield=None, value=250),
                EchoIssued(turn=state.turn_count, slot="security_deposit_amount", subfield=None, value=250),
            ]
            return UserQuestion(text="A $250 deposit?", primary_slot="security_deposit_amount")
        if s == 1:
            return [RecordAnswer(field_id="security_deposit_amount", value=250, source="user_stated")]
        return EndConversation(reason="completed")

    def drain_trace_events(self):
        ev, self._pending = self._pending, []
        return ev


class TestProfileLoaderSplit:
    def test_spec_carries_facts_only_key_kept_separate(self):
        bundle = load_profile(_FIXTURE)
        # The simulator-visible spec has facts but never an answer key.
        assert "answer_key" not in bundle.spec.facts
        assert bundle.spec.facts["ownership_model"] == "all_self_owned"
        # The key is parsed into dispositions on the side.
        assert "taxes" in bundle.answer_key.slots
        assert bundle.group == "A" and bundle.tuning_only is True


class TestRunFnWithFakes:
    def test_builds_runrecord_with_metrics_and_snapshots(self, tmp_path):
        config = load_run_config(_CONFIG)
        bundle = ProfileBundle(
            profile_id="FAKE",
            group="A",
            spec=RespondentSpec(profile_id="FAKE", group="A", facts={}),
            answer_key=AnswerKey(profile_id="FAKE", group="A", slots={}),
            sections=list(DEFAULT_H1_SECTIONS),
            advice_slots=["non_refundable_enabled"],
        )
        run_fn = make_run_fn(
            config=config,
            profile_loader=lambda pid: bundle,
            system_factory=lambda sid, b: _FakeSystem(),
            simulator_factory=lambda b, seed: _FakeSim(),
        )
        ctx = _ctx(tmp_path, "agent")
        record = asyncio.run(run_fn(ctx))

        assert record.status is RunStatus.COMPLETED
        assert record.tag == "tuning"
        assert record.models == {"agent": config.agent.model, "simulator": config.simulator.model}
        assert record.trace_path == "runs/FAKE__agent__00.trace.jsonl"
        assert ctx.trace_path.exists()
        # The unconfirmed echo write is surfaced (SM-C1 fail-safe).
        assert record.metrics["total_echo_writes"] == 1
        assert record.metrics["false_writes"] == 1
        assert "inappropriate_advice_rate" in record.metrics
        assert record.usage is not None and record.usage["input_tokens"] == 0  # frozen kernel → no usage


class TestRunFnEndToEndTree:
    """Real TreeSystem + scripted Group A simulator + real scoring — no LLM clients."""

    def test_tree_run_is_clean_and_scored(self, tmp_path):
        config = load_run_config(_CONFIG)
        profiles_dir = tmp_path / "profiles"
        profiles_dir.mkdir()
        data = json.loads(_FIXTURE.read_text(encoding="utf-8"))
        data["profile_id"] = "A1"
        (profiles_dir / "A1.json").write_text(json.dumps(data), encoding="utf-8")

        run_fn = make_run_fn(config=config, profile_loader=make_dir_loader(profiles_dir))
        ctx = _ctx(tmp_path, "tree", profile_id="A1", tag="scored")
        record = asyncio.run(run_fn(ctx))

        assert record.system_id == "tree"
        assert record.status in {RunStatus.COMPLETED, RunStatus.INCOMPLETE}
        # Tree is false-write-free by construction (SM-C1).
        assert record.metrics["false_write_rate"] == 0.0
        assert 0.0 <= record.metrics["sar"] <= 1.0
        assert ctx.trace_path.exists()
