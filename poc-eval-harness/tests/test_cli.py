"""Tests for harness.cli, harness.freeze, and harness.providers (Story 4.4 glue)."""

from __future__ import annotations

import asyncio
import json
import shutil
from pathlib import Path

import pytest

from config.config_loader import load_run_config
from harness.cli import enumerate_profiles, run_cli
from harness.freeze import build_freeze_manifest, schema_version
from harness.manifest import FreezeManifest
from harness.providers import (
    ProviderError,
    _AnthropicClientAdapter,
    build_agent_client,
    build_cursor_client,
    build_gemini_client_factory,
    load_env,
)
from harness.records import RunRecord, RunStatus
from harness.runner import RunContext

_ROOT = Path(__file__).resolve().parents[1]
_CONFIG = _ROOT / "config" / "run_config.toml"


# ---------------------------------------------------------------------------
# harness.freeze
# ---------------------------------------------------------------------------


class TestBuildFreezeManifest:
    def test_all_inputs_hashed_and_valid(self):
        config = load_run_config(_CONFIG)
        manifest = build_freeze_manifest(config, _ROOT)

        assert isinstance(manifest, FreezeManifest)
        mismatches = manifest.validate()
        assert mismatches == [], f"manifest inputs changed: {mismatches}"

    def test_manifest_hash_is_deterministic(self):
        config = load_run_config(_CONFIG)
        m1 = build_freeze_manifest(config, _ROOT)
        m2 = build_freeze_manifest(config, _ROOT)
        assert m1.manifest_hash == m2.manifest_hash

    def test_manifest_includes_expected_input_keys(self):
        config = load_run_config(_CONFIG)
        manifest = build_freeze_manifest(config, _ROOT)
        for key in ("scored_profiles", "agent_system_prompt", "tree_module",
                    "simulator_scripted_turns", "run_config", "scoring_module",
                    "schema", "lockfile"):
            assert key in manifest.entries, f"missing entry: {key}"

    def test_schema_version_extracted(self):
        ver = schema_version(_ROOT / "schema" / "guesty-pro-account-creation-schema.md")
        assert "0.3" in ver

    def test_manifest_git_sha_populated(self):
        config = load_run_config(_CONFIG)
        manifest = build_freeze_manifest(config, _ROOT)
        assert manifest.git_sha is not None and len(manifest.git_sha) >= 7

    def test_save_and_load_roundtrip(self, tmp_path):
        config = load_run_config(_CONFIG)
        manifest = build_freeze_manifest(config, _ROOT)
        out = tmp_path / "manifest.json"
        manifest.save(out)
        loaded = FreezeManifest.load(out)
        assert loaded.manifest_hash == manifest.manifest_hash
        assert list(loaded.entries.keys()) == list(manifest.entries.keys())


# ---------------------------------------------------------------------------
# harness.providers — unit tests (no live network calls)
# ---------------------------------------------------------------------------


class TestLoadEnv:
    def test_sets_env_from_dotenv(self, tmp_path, monkeypatch):
        env_file = tmp_path / ".env"
        env_file.write_text("TEST_VAR_CLI=hello\nTEST_OTHER=world\n", encoding="utf-8")
        monkeypatch.delenv("TEST_VAR_CLI", raising=False)
        monkeypatch.delenv("TEST_OTHER", raising=False)
        import os
        load_env(env_file)
        assert os.environ.get("TEST_VAR_CLI") == "hello"
        assert os.environ.get("TEST_OTHER") == "world"

    def test_does_not_overwrite_existing(self, tmp_path, monkeypatch):
        env_file = tmp_path / ".env"
        env_file.write_text("TEST_VAR_CLI=from_file\n", encoding="utf-8")
        monkeypatch.setenv("TEST_VAR_CLI", "pre_existing")
        import os
        load_env(env_file)
        assert os.environ["TEST_VAR_CLI"] == "pre_existing"

    def test_missing_file_is_silent(self):
        load_env(Path("/nonexistent/.env"))  # must not raise


class TestBuildCursorClient:
    def test_raises_on_missing_api_key_non_gemini(self, monkeypatch):
        """Non-Gemini CURSOR_BASE_URL but no CURSOR_API_KEY → ProviderError."""
        monkeypatch.delenv("CURSOR_API_KEY", raising=False)
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        monkeypatch.setenv("CURSOR_BASE_URL", "http://localhost:8765/v1")
        with pytest.raises(ProviderError, match="CURSOR_API_KEY"):
            build_cursor_client()

    def test_raises_when_neither_base_url_nor_anthropic_key(self, monkeypatch):
        """Neither CURSOR_BASE_URL nor ANTHROPIC_API_KEY → ProviderError listing both options."""
        monkeypatch.delenv("CURSOR_BASE_URL", raising=False)
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
        with pytest.raises(ProviderError, match="ANTHROPIC_API_KEY"):
            build_cursor_client()

    def test_explicit_args_bypass_env(self):
        """Explicit base_url → non-Gemini path, regardless of env."""
        client = build_cursor_client(api_key="fake_key", base_url="http://127.0.0.1:8765/v1")
        assert client is not None
        assert hasattr(client, "chat")

    def test_gemini_endpoint_uses_gemini_api_key(self, monkeypatch):
        """CURSOR_BASE_URL = googleapis.com → GEMINI_API_KEY is used, not CURSOR_API_KEY."""
        monkeypatch.delenv("CURSOR_API_KEY", raising=False)
        monkeypatch.setenv("CURSOR_BASE_URL", "https://generativelanguage.googleapis.com/v1beta/openai/")
        monkeypatch.setenv("GEMINI_API_KEY", "fake-gemini-key")
        client = build_agent_client()
        assert hasattr(client, "chat")

    def test_gemini_endpoint_missing_key_raises(self, monkeypatch):
        """CURSOR_BASE_URL = googleapis.com but no GEMINI_API_KEY → ProviderError."""
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        monkeypatch.delenv("CURSOR_API_KEY", raising=False)
        monkeypatch.setenv("CURSOR_BASE_URL", "https://generativelanguage.googleapis.com/v1beta/openai/")
        with pytest.raises(ProviderError, match="GEMINI_API_KEY"):
            build_agent_client()

    def test_anthropic_path_when_no_cursor_base_url(self, monkeypatch):
        """ANTHROPIC_API_KEY set + no CURSOR_BASE_URL → returns _AnthropicClientAdapter."""
        monkeypatch.delenv("CURSOR_BASE_URL", raising=False)
        monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-fake")
        client = build_agent_client()
        assert isinstance(client, _AnthropicClientAdapter)
        assert hasattr(client, "chat")
        assert hasattr(client.chat, "completions")
        assert hasattr(client.chat.completions, "create")

    def test_cursor_path_takes_priority_over_anthropic(self, monkeypatch):
        """CURSOR_BASE_URL + ANTHROPIC_API_KEY → OpenAI-compat path wins."""
        monkeypatch.setenv("CURSOR_BASE_URL", "http://localhost:8765/v1")
        monkeypatch.setenv("CURSOR_API_KEY", "crsr-fake")
        monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-fake")
        client = build_agent_client()
        assert not isinstance(client, _AnthropicClientAdapter)
        assert hasattr(client, "chat")


class TestBuildGeminiClientFactory:
    def test_raises_on_missing_api_key(self, monkeypatch):
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
        with pytest.raises(ProviderError, match="GEMINI_API_KEY"):
            build_gemini_client_factory("gemini-1.5-pro-002")

    def test_returns_callable_factory(self, monkeypatch):
        monkeypatch.setenv("GEMINI_API_KEY", "fake_key")
        factory = build_gemini_client_factory("gemini-1.5-pro-002")
        assert callable(factory)


# ---------------------------------------------------------------------------
# enumerate_profiles
# ---------------------------------------------------------------------------


class TestEnumerateProfiles:
    def test_scored_enumerates_profiles_dir(self):
        config = load_run_config(_CONFIG)
        profiles = enumerate_profiles(config, "scored")
        assert len(profiles) == 8
        assert "A1" in profiles and "C2" in profiles
        assert profiles == sorted(profiles)

    def test_explicit_ids_returned_as_is(self):
        config = load_run_config(_CONFIG)
        profiles = enumerate_profiles(config, "A1,B2, C1 ")
        assert profiles == ["A1", "B2", "C1"]

    def test_dev_enumerates_dev_dir(self):
        config = load_run_config(_CONFIG)
        profiles = enumerate_profiles(config, "dev")
        # dev dir may be empty; must not raise and must return a list
        assert isinstance(profiles, list)


# ---------------------------------------------------------------------------
# run_cli — dry-run exercising the full manifest build + plan resolution
# ---------------------------------------------------------------------------


class TestRunCliDryRun:
    def test_dry_run_exits_zero_with_valid_inputs(self):
        rc = run_cli(["--profiles", "scored", "--dry-run", "--root", str(_ROOT)])
        assert rc == 0

    def test_dry_run_tree_only(self):
        rc = run_cli(["--profiles", "scored", "--systems", "tree", "--dry-run", "--root", str(_ROOT)])
        assert rc == 0

    def test_empty_profiles_explicit_empty_string_exits_nonzero(self):
        # Passing an explicit id list that resolves to nothing (blanks + commas only).
        config = load_run_config(_CONFIG)
        rc = run_cli(["--profiles", ",, ,", "--dry-run", "--root", str(_ROOT)])
        assert rc != 0


# ---------------------------------------------------------------------------
# run_cli with injected run_fn (no live LLM calls)
# ---------------------------------------------------------------------------


class TestRunCliWithFakeRunFn:
    def test_single_tree_run_completes(self, tmp_path):
        """CLI with a fake run_fn writes a RunRecord and exits 0."""
        import uuid

        async def _fake_run_fn(ctx: RunContext) -> RunRecord:
            return RunRecord(
                manifest_hash=ctx.manifest_hash,
                profile_id=ctx.profile_id,
                system_id=ctx.system_id,
                run_index=ctx.run_index,
                status=RunStatus.COMPLETED,
                end_reason="completed",
                seed=ctx.seed,
                metrics={"sar": 1.0, "numerator": 1, "denominator": 1,
                         "false_write_rate": 0.0, "false_writes": 0, "total_echo_writes": 0,
                         "questions_to_completion": 3, "clarification_efficiency": 0.0,
                         "human_rating_pending": []},
                usage={"input_tokens": 10, "output_tokens": 5, "cost_usd": 0.0, "wall_clock_ms": 100},
                tag=ctx.tag,
            )

        rc = run_cli(
            ["--profiles", "A1", "--systems", "tree", "--runs", "5",
             "--campaigns-dir", str(tmp_path / "campaigns"),
             "--root", str(_ROOT)],
            run_fn=_fake_run_fn,
        )
        assert rc == 0
        # All 5 run records written
        manifests = list((tmp_path / "campaigns").glob("*/runs/*.json"))
        assert len(manifests) == 5, f"expected 5 records, got {len(manifests)}"

    def test_errored_run_exits_nonzero(self, tmp_path):
        async def _erroring_fn(ctx: RunContext) -> RunRecord:
            return RunRecord(
                manifest_hash=ctx.manifest_hash,
                profile_id=ctx.profile_id,
                system_id=ctx.system_id,
                run_index=ctx.run_index,
                status=RunStatus.ERRORED,
                end_reason="errored",
                seed=ctx.seed,
                error="synthetic failure",
                tag=ctx.tag,
            )

        rc = run_cli(
            ["--profiles", "A1", "--systems", "tree", "--runs", "1",
             "--campaigns-dir", str(tmp_path / "campaigns"),
             "--root", str(_ROOT)],
            run_fn=_erroring_fn,
        )
        assert rc != 0
