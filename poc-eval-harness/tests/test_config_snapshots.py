"""R-7 — provider models must be pinned dated snapshots, never floating aliases."""

from __future__ import annotations

from pathlib import Path

import pytest

from config.config_loader import ConfigError, load_run_config

_CONFIG = Path(__file__).resolve().parents[1] / "config" / "run_config.toml"


def test_real_config_loads_and_pins_dated_snapshots():
    cfg = load_run_config(_CONFIG)
    for model in (cfg.agent.model, cfg.simulator.model, cfg.extractor.model):
        assert "latest" not in model.lower()
        assert model  # non-empty, pinned


@pytest.mark.parametrize("bad", ["claude-latest", "claude-opus-latest", "gpt-4o-LATEST", "model-*"])
def test_latest_alias_is_rejected(tmp_path, bad):
    text = _CONFIG.read_text(encoding="utf-8").replace('model    = "gemini-2.5-flash"', f'model    = "{bad}"', 1)
    p = tmp_path / "run_config.toml"
    p.write_text(text, encoding="utf-8")
    with pytest.raises(ConfigError, match="R-7"):
        load_run_config(p)
