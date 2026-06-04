"""Interactive onboarding session — you play the customer (not the simulator).

Usage::

    cd poc-eval-harness
    uv run python -m harness.interactive --system agent --profile A1
    uv run python -m harness.interactive --system tree --profile B1

Requires the same ``.env`` keys as a normal harness run (Gemini for agent when
``CURSOR_BASE_URL`` points at the Google OpenAI-compat endpoint).
"""

from __future__ import annotations

import argparse
from pathlib import Path

from config.config_loader import load_run_config
from harness.session import create_session, format_summary, run_to_completion
from kernel.protocol import UserQuestion


class HumanSimulator:
    """Reads your replies from stdin instead of scripted/LLM simulation."""

    def __init__(self, *, persona_hint: str = "") -> None:
        self._persona_hint = persona_hint.strip()

    def reply(self, question: UserQuestion) -> str:
        print()
        print("─" * 60)
        if question.primary_slot:
            print(f"[slot: {question.primary_slot}]")
        print(question.text)
        print("─" * 60)
        if self._persona_hint:
            print(f"(persona hint: {self._persona_hint[:120]}{'…' if len(self._persona_hint) > 120 else ''})")
        try:
            return input("You> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n(session ended)")
            raise SystemExit(0) from None


def run_interactive(
    *,
    system_id: str,
    profile_id: str,
    config_path: Path,
    root: Path,
    max_turns: int | None = None,
    show_tools: bool = False,
) -> int:
    config = load_run_config(config_path if config_path.is_absolute() else root / config_path)
    session = create_session(
        system_id=system_id,
        profile_id=profile_id,
        config_path=config_path,
        root=root,
        max_turns=max_turns,
    )

    if show_tools and system_id == "agent":
        _orig_next = session.system.next_action

        def _next_with_log(state, history):
            action = _orig_next(state, history)
            if isinstance(action, list):
                for tc in action:
                    print(f"\n[tool] {tc.tool}({tc.model_dump(exclude={'tool'})})")
            return action

        session.system.next_action = _next_with_log  # type: ignore[method-assign]

    cap = max_turns if max_turns is not None else config.max_turns
    sim = HumanSimulator(persona_hint=session.persona_hint)

    print(f"Interactive onboarding — system={system_id}  profile={profile_id}")
    print(f"Model (agent): {config.agent.model if system_id == 'agent' else 'n/a (deterministic tree)'}")
    print(f"Turn cap: {cap}  |  Type your answers at the prompt. Ctrl+C to quit.")
    print()

    state, end_reason = run_to_completion(session, sim)
    print()
    print("=" * 60)
    print(format_summary(state, end_reason))
    print("=" * 60)
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Play the customer in a live onboarding session (agent or tree).",
    )
    ap.add_argument("--system", choices=["agent", "tree"], default="agent")
    ap.add_argument("--profile", default="A1", help="Scored profile id (e.g. A1, B1, C1).")
    ap.add_argument("--config", default="config/run_config.toml")
    ap.add_argument("--root", default=".")
    ap.add_argument("--max-turns", type=int, default=None)
    ap.add_argument(
        "--show-tools",
        action="store_true",
        help="Print agent tool calls as they happen (agent only).",
    )
    args = ap.parse_args(argv)

    root = Path(args.root)
    scored_dir = root / "profiles/scored"
    if not (scored_dir / f"{args.profile}.json").is_file():
        print(f"ERROR: profile not found: {scored_dir / f'{args.profile}.json'}")
        return 2

    return run_interactive(
        system_id=args.system,
        profile_id=args.profile,
        config_path=Path(args.config),
        root=root,
        max_turns=args.max_turns,
        show_tools=args.show_tools,
    )


if __name__ == "__main__":
    raise SystemExit(main())
