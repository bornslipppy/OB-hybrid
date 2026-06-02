"""Story 0.2 — run-config TOML startup validation."""

from __future__ import annotations

from pathlib import Path

import pytest

from config.config_loader import ConfigError, load_run_config

_VALID_TOML = """\
[experiment]
project = "Test"
version = "0.0.1"

[providers.agent]
family = "anthropic"
model  = "claude-test"

[providers.simulator]
family = "openai"
model  = "gpt-test"

[providers.extractor]
family = "anthropic"
model  = "claude-test"

[temperatures]
scored    = 0.0
glue      = 0.2
simulator = 0.0

[run]
k_runs    = 5
seed_base = 42
max_turns = 60

[freeze]
manifest_path       = "campaigns/manifest.json"
refreeze_count_path = "campaigns/refreeze_count.json"

[profiles]
dev_dir    = "profiles/dev"
scored_dir = "profiles/scored"

[schema]
path = "schema/guesty-pro-account-creation-schema.md"
"""


def _write_config(tmp_path: Path, toml: str) -> Path:
    p = tmp_path / "run_config.toml"
    p.write_text(toml)
    return p


def test_valid_config_loads(tmp_path):
    cfg = load_run_config(_write_config(tmp_path, _VALID_TOML))
    assert cfg.agent.family == "anthropic"
    assert cfg.simulator.family == "openai"
    assert cfg.scored_temperature == 0.0
    assert cfg.k_runs == 5


def test_scored_temperature_nonzero_is_startup_error(tmp_path):
    bad = _VALID_TOML.replace("scored    = 0.0", "scored    = 0.2")
    with pytest.raises(ConfigError, match="temperatures.scored must be 0.0"):
        load_run_config(_write_config(tmp_path, bad))


def test_same_provider_family_is_startup_error(tmp_path):
    bad = _VALID_TOML.replace(
        '[providers.simulator]\nfamily = "openai"',
        '[providers.simulator]\nfamily = "anthropic"',
    )
    with pytest.raises(ConfigError, match="different provider families"):
        load_run_config(_write_config(tmp_path, bad))


def test_k_runs_below_five_is_startup_error(tmp_path):
    bad = _VALID_TOML.replace("k_runs    = 5", "k_runs    = 3")
    with pytest.raises(ConfigError, match="k_runs must be >= 5"):
        load_run_config(_write_config(tmp_path, bad))
