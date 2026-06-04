"""Campaign-runner CLI (Story 4.4) — the entry point behind ``python -m harness.runner``.

Ties the frozen pieces together: load run-config → build + validate the §5.2 freeze
manifest → resolve the run plan (profiles × systems × k) → wire the decorrelated
provider clients into ``make_run_fn`` → drive ``run_campaign`` under freeze discipline.

``--dry-run`` stops after building + validating the manifest and resolving the plan,
making no live provider calls — the safe pre-flight before the scored run. ``run_fn`` is
injectable so the orchestration is unit-testable without live LLM clients.
"""

from __future__ import annotations

import argparse
import asyncio
from pathlib import Path
from typing import Any

from config.config_loader import load_run_config
from harness.freeze import build_freeze_manifest
from harness.profile_loader import make_dir_loader
from harness.runner import run_campaign
from harness.wiring import make_run_fn

_DEFAULT_SYSTEMS = ["agent", "tree"]


def enumerate_profiles(config: Any, which: str) -> list[str]:
    """Resolve ``--profiles`` to a sorted list of profile ids.

    ``scored`` / ``dev`` enumerate the configured directory; anything else is treated as
    an explicit comma-separated id list (preserving caller order).
    """
    which = which.strip()
    if which == "scored":
        return sorted(p.stem for p in Path(config.scored_dir).glob("*.json"))
    if which == "dev":
        return sorted(p.stem for p in Path(config.dev_dir).glob("*.json"))
    return [p.strip() for p in which.split(",") if p.strip()]


def _profiles_dir(config: Any, which: str) -> Path:
    if which.strip() == "dev":
        return Path(config.dev_dir)
    return Path(config.scored_dir)


def run_cli(argv: list[str] | None = None, *, run_fn: Any = None) -> int:
    ap = argparse.ArgumentParser(
        prog="harness.runner",
        description="Drive both systems against the scored profiles under freeze discipline (Story 4.4).",
    )
    ap.add_argument(
        "--campaign", default=None,
        help="(compat) kernel proto-manifest path; informational only. The full §5.2 freeze "
             "manifest is built from run_config inputs and supersedes the proto-manifest.",
    )
    ap.add_argument("--profiles", default="scored", help="'scored' | 'dev' | comma-separated ids.")
    ap.add_argument("--runs", type=int, default=None, help="k runs per (profile, system); default = run_config k_runs.")
    ap.add_argument("--config", default="config/run_config.toml")
    ap.add_argument("--root", default=".")
    ap.add_argument("--systems", default=",".join(_DEFAULT_SYSTEMS), help="Comma-separated: agent,tree.")
    ap.add_argument("--campaigns-dir", default=None, help="Base output dir (default: <root>/campaigns).")
    ap.add_argument("--max-concurrency", type=int, default=4)
    ap.add_argument("--dry-run", action="store_true",
                    help="Build + validate the freeze manifest and resolve the plan; no live calls.")
    args = ap.parse_args(argv)

    root = Path(args.root)
    cfg_path = Path(args.config)
    config = load_run_config(cfg_path if cfg_path.is_absolute() else root / cfg_path)

    profiles = enumerate_profiles(config, args.profiles)
    systems = [s.strip() for s in args.systems.split(",") if s.strip()]
    k = args.runs if args.runs is not None else config.k_runs

    if not profiles:
        print(f"ERROR: no profiles resolved for --profiles={args.profiles!r}.")
        return 2
    if not systems:
        print(f"ERROR: no systems resolved for --systems={args.systems!r}.")
        return 2

    manifest = build_freeze_manifest(config, root)
    mismatches = manifest.validate()

    print(f"freeze manifest : {manifest.short_hash}  ({len(manifest.entries)} inputs, "
          f"git {(manifest.git_sha or '—')[:12]})")
    print(f"validate        : {'CLEAN' if not mismatches else 'MISMATCH ' + str(sorted(mismatches))}")
    print(f"profiles ({len(profiles)})   : {', '.join(profiles)}")
    print(f"systems         : {', '.join(systems)}")
    print(f"k (runs)        : {k}")
    print(f"campaign dir    : campaigns/{manifest.manifest_hash}")
    if k < 5:
        print(f"WARNING: k={k} < 5 — below the FR-22 freeze-discipline floor for a scored run.")

    if mismatches:
        print("ERROR: freeze inputs changed since manifest build — refusing to run (EC-25). "
              "A re-freeze is required.")
        return 1
    if args.dry_run:
        print("dry-run: manifest built + validated, run plan resolved. No live calls made.")
        return 0

    base_dir = Path(args.campaigns_dir) if args.campaigns_dir else root / "campaigns"
    if run_fn is None:
        from harness.providers import LazyGeminiClientFactory, build_agent_client, load_env

        load_env()
        cursor_client = build_agent_client() if "agent" in systems else None
        # Lazy: Gemini client is built only when the first Group B/C profile is encountered.
        # Tree-only runs against Group-A profiles never need a live Gemini key.
        gemini_client = LazyGeminiClientFactory(config.simulator.model)
        run_fn = make_run_fn(
            config=config,
            profile_loader=make_dir_loader(_profiles_dir(config, args.profiles)),
            cursor_client=cursor_client,
            gemini_client=gemini_client,
        )

    result = asyncio.run(
        run_campaign(
            manifest,
            systems,
            profiles,
            run_fn=run_fn,
            k=k,
            base_dir=str(base_dir),
            frozen=True,
            seed_base=config.seed_base,
            max_concurrency=args.max_concurrency,
        )
    )

    print(
        f"\ncampaign complete: completed={result.completed} incomplete={result.incomplete} "
        f"errored={result.errored} skipped={result.skipped}"
    )
    print(f"records in: {result.campaign_dir}")
    return 0 if result.errored == 0 else 1
