"""Validated run-config loader (Story 0.2 AC: startup validation).

Validates three invariants at load time (hard failures):
  1. ``temperatures.scored`` must be 0.0 — a non-zero value for any scored-slot code
     path is a startup error (FR-6 / §4.1).
  2. ``providers.agent.family != providers.simulator.family`` — same-family config
     aborts the run (D-3 / FR-21).
  3. ``run.k_runs >= 5`` — freeze discipline (FR-22).
  4. Every provider model is a dated snapshot, never a ``-latest`` / floating alias
     (R-7) — a moving model breaks run reproducibility and the freeze manifest.
"""

from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ProviderConfig:
    family: str
    model: str


@dataclass(frozen=True)
class RunConfig:
    """Parsed + validated run configuration."""

    project: str
    agent: ProviderConfig
    simulator: ProviderConfig
    extractor: ProviderConfig
    scored_temperature: float
    glue_temperature: float
    k_runs: int
    seed_base: int
    max_turns: int
    manifest_path: Path
    refreeze_count_path: Path
    dev_dir: Path
    scored_dir: Path
    schema_path: Path

    # Full raw dict kept for manifest hashing (§5.2).
    raw: dict  # type: ignore[type-arg]


class ConfigError(ValueError):
    """Raised when a run-config invariant is violated."""


def load_run_config(path: str | Path = "config/run_config.toml") -> RunConfig:
    p = Path(path)
    with p.open("rb") as fh:
        data = tomllib.load(fh)

    agent = ProviderConfig(**data["providers"]["agent"])
    simulator = ProviderConfig(**data["providers"]["simulator"])
    extractor = ProviderConfig(**data["providers"]["extractor"])
    temps = data["temperatures"]
    run = data["run"]
    freeze = data["freeze"]
    profiles = data["profiles"]
    schema = data["schema"]

    # --- Invariant 1: scored temperature must be 0.0 (FR-6) -----------------
    if float(temps["scored"]) != 0.0:
        raise ConfigError(
            f"temperatures.scored must be 0.0 (FR-6); got {temps['scored']!r}. "
            "No scored-slot code path may run at any other temperature."
        )

    # --- Invariant 2: provider decorrelation (FR-21) -------------------------
    if agent.family == simulator.family:
        raise ConfigError(
            f"Agent and simulator must use different provider families (FR-21 / D-3). "
            f"Both are set to {agent.family!r}. Use a different provider for the simulator."
        )

    # --- Invariant 3: k_runs >= 5 (FR-22) -----------------------------------
    if int(run["k_runs"]) < 5:
        raise ConfigError(
            f"run.k_runs must be >= 5 (FR-22 / FR-25); got {run['k_runs']!r}."
        )

    # --- Invariant 4: dated model snapshots only — no floating alias (R-7) ---
    for label, pc in (("agent", agent), ("simulator", simulator), ("extractor", extractor)):
        model = pc.model.strip().lower()
        if not model or "latest" in model or model.endswith("*"):
            raise ConfigError(
                f"providers.{label}.model must be a pinned dated snapshot, not a "
                f"floating/-latest alias (R-7); got {pc.model!r}. A moving model breaks "
                "run reproducibility and invalidates the freeze manifest."
            )

    return RunConfig(
        project=data["experiment"]["project"],
        agent=agent,
        simulator=simulator,
        extractor=extractor,
        scored_temperature=float(temps["scored"]),
        glue_temperature=float(temps["glue"]),
        k_runs=int(run["k_runs"]),
        seed_base=int(run["seed_base"]),
        max_turns=int(run["max_turns"]),
        manifest_path=Path(freeze["manifest_path"]),
        refreeze_count_path=Path(freeze["refreeze_count_path"]),
        dev_dir=Path(profiles["dev_dir"]),
        scored_dir=Path(profiles["scored_dir"]),
        schema_path=Path(schema["path"]),
        raw=data,
    )
