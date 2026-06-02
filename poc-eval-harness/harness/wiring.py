"""run_fn factory — wire system + simulator + scoring into a RunRecord (Story 4.4).

``make_run_fn`` builds the ``RunFn`` that ``run_campaign`` invokes per
``(manifest, profile, system, run_index)``. One run is a pure function of its frozen
inputs (D-4): load the profile (spec/key split), construct the system (agent or tree,
``trace_writer=None`` because the harness owns the canonical trace), construct the
decorrelated simulator, drive ``run_conversation``, then score the trace + final state
into a ``RunRecord``.

Model snapshots come from ``config.run_config.toml`` (dated snapshots, never ``-latest``
— R-7, enforced in ``config_loader``) and are stamped into every record's ``models`` so a
record is self-describing and the snapshots travel inside the freeze manifest.

Provider wiring (FR-21 / D-3):
  cursor_client — OpenAI-compatible client pointed at Cursor's API (family="cursor").
  gemini_client — ``_GeminiLike`` callable factory for the Gemini simulator
                  (family="gemini"). See ``kernel.llm._GeminiLike`` for the contract.
"""

from __future__ import annotations

import asyncio
from typing import Any, Callable

from config.config_loader import RunConfig
from harness.profile_loader import ProfileBundle
from harness.records import RunRecord, status_from_end_reason
from harness.runner import RunContext, run_conversation
from kernel.schema import FrameGraph, SchemaLoader
from kernel.state import StateReducer
from kernel.trace import TraceReader, TraceWriter
from scoring.metrics import (
    clarification_efficiency,
    cost_latency,
    false_write_rate,
    inappropriate_advice_rate,
    questions_to_completion,
)
from scoring.sar import score_profile

# Factory contracts (injectable so the wiring is unit-testable with fakes).
SystemFactory = Callable[[str, ProfileBundle], Any]          # (system_id, bundle) -> System
SimulatorFactory = Callable[[ProfileBundle, "int | None"], Any]  # (bundle, seed) -> simulator
ProfileLoader = Callable[[str], ProfileBundle]                # profile_id -> ProfileBundle
HumanRatingsProvider = Callable[[RunContext], "dict[str, int] | None"]


def default_system_factory(
    config: RunConfig, *, cursor_client: Any | None = None
) -> SystemFactory:
    """Build agent/tree systems with ``trace_writer=None`` (harness owns the trace).

    The tree is imported lazily so an agent-only run never depends on the tree module.
    """

    def _make(system_id: str, bundle: ProfileBundle) -> Any:
        if system_id == "agent":
            if cursor_client is None:
                raise ValueError("system_id='agent' requires a cursor_client.")
            from agent.agent import AgentSystem

            return AgentSystem(
                cursor_client=cursor_client,
                model=config.agent.model,
                schema_path=config.schema_path,
                trace_writer=None,  # harness owns the canonical trace; agent drains echo events
            )
        if system_id == "tree":
            from tree.tree import TreeSystem

            return TreeSystem(schema_path=config.schema_path)
        raise ValueError(f"unknown system_id {system_id!r} (expected 'agent' | 'tree')")

    return _make


def default_simulator_factory(
    config: RunConfig, *, gemini_client: Any | None = None
) -> SimulatorFactory:
    """Build the decorrelated user simulator (scripted for Group A; LLM for B/C)."""

    def _make(bundle: ProfileBundle, seed: int | None) -> Any:
        from simulator.simulator import UserSimulator

        return UserSimulator(
            bundle.spec,
            gemini_client=gemini_client,
            model=config.simulator.model,
            seed=seed,
        )

    return _make


def make_run_fn(
    *,
    config: RunConfig,
    profile_loader: ProfileLoader,
    system_factory: SystemFactory | None = None,
    simulator_factory: SimulatorFactory | None = None,
    cursor_client: Any | None = None,
    gemini_client: Any | None = None,
    human_ratings_provider: HumanRatingsProvider | None = None,
):
    """Return the async ``RunFn`` for ``run_campaign``.

    Either inject ``system_factory``/``simulator_factory`` (e.g. fakes in tests) or pass
    the provider clients and let the default factories build the real agent/tree/simulator.
    """
    system_factory = system_factory or default_system_factory(config, cursor_client=cursor_client)
    simulator_factory = simulator_factory or default_simulator_factory(config, gemini_client=gemini_client)

    # Frame is needed for the reducer's end_section guard; build it once and reuse.
    frame = FrameGraph(SchemaLoader().load(config.schema_path))

    models = {"agent": config.agent.model, "simulator": config.simulator.model}
    provider_config = {
        "agent": config.agent.family,
        "simulator": config.simulator.family,
        "extractor_model": config.extractor.model,
    }

    def _execute(ctx: RunContext) -> RunRecord:
        bundle = profile_loader(ctx.profile_id)
        system = system_factory(ctx.system_id, bundle)
        simulator = simulator_factory(bundle, ctx.seed)

        writer = TraceWriter(ctx.trace_path)
        state, end_reason = run_conversation(
            system,
            simulator,
            reducer=StateReducer(frame=frame),
            trace=writer,
            profile_id=ctx.profile_id,
            max_turns=config.max_turns,
        )

        events = TraceReader(ctx.trace_path).events()
        human_ratings = human_ratings_provider(ctx) if human_ratings_provider else None
        score = score_profile(
            state,
            bundle.answer_key,
            bundle.sections,
            schema_path=config.schema_path,
            system_id=ctx.system_id,
            human_ratings=human_ratings,
        )

        fw = false_write_rate(events)
        clar = clarification_efficiency(events)
        usage = cost_latency(events)
        metrics: dict[str, Any] = {
            "sar": score.sar,
            "numerator": score.numerator,
            "denominator": score.denominator,
            "false_write_rate": fw.rate,
            "false_writes": fw.false_writes,
            "total_echo_writes": fw.total_echo_writes,
            "questions_to_completion": questions_to_completion(events),
            "clarification_efficiency": clar.rate,
            "human_rating_pending": score.human_rating_pending,
        }
        if bundle.advice_slots:
            adv = inappropriate_advice_rate(events, advice_slots=bundle.advice_slots)
            metrics["inappropriate_advice_rate"] = adv.rate
            metrics["inappropriate_advice_count"] = adv.inappropriate

        return RunRecord(
            manifest_hash=ctx.manifest_hash,
            profile_id=ctx.profile_id,
            system_id=ctx.system_id,
            run_index=ctx.run_index,
            status=status_from_end_reason(end_reason),
            end_reason=end_reason,
            seed=ctx.seed,
            models=dict(models),
            provider_config=dict(provider_config),
            trace_path=f"runs/{ctx.key}.trace.jsonl",
            in_scope_slots=[ss.slot_id for ss in score.slot_scores],
            metrics=metrics,
            usage={
                "input_tokens": usage.input_tokens,
                "output_tokens": usage.output_tokens,
                "cost_usd": usage.cost_usd,
                "wall_clock_ms": usage.wall_clock_ms,
            },
            tag=ctx.tag,
        )

    async def run_fn(ctx: RunContext) -> RunRecord:
        # The conversation + scoring is synchronous and (for the agent) I/O-bound on the
        # provider SDK. Run it off the event loop so run_campaign's bounded concurrency is
        # real even with synchronous SDK clients.
        return await asyncio.to_thread(_execute, ctx)

    return run_fn
