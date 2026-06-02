"""Story 4.4 — FreezeManifest content-hash + freeze-discipline tests (§5.2 / FR-26 / EC-25)."""

from __future__ import annotations

import pytest

from harness.manifest import MAX_REFREEZES, FreezeManifest, ManifestError


def _make_inputs(tmp_path):
    (tmp_path / "profiles").mkdir()
    (tmp_path / "profiles" / "p1.json").write_text('{"profile_id": "A1"}', encoding="utf-8")
    (tmp_path / "profiles" / "p1.key.json").write_text('{"slots": {}}', encoding="utf-8")
    (tmp_path / "prompt.txt").write_text("system prompt v1", encoding="utf-8")
    (tmp_path / "lock").write_text("locked", encoding="utf-8")
    return {
        "scored_profiles": tmp_path / "profiles",
        "agent_system_prompt": tmp_path / "prompt.txt",
        "lockfile": tmp_path / "lock",
    }


class TestBuildAndHash:
    def test_build_hashes_all_inputs(self, tmp_path):
        m = FreezeManifest.build(_make_inputs(tmp_path), schema_version="v0.3", git_sha="abc123")
        assert set(m.entries) == {"scored_profiles", "agent_system_prompt", "lockfile"}
        assert len(m.manifest_hash) == 64
        assert m.short_hash == m.manifest_hash[:12]

    def test_hash_is_deterministic(self, tmp_path):
        inputs = _make_inputs(tmp_path)
        a = FreezeManifest.build(inputs, schema_version="v0.3", git_sha="abc")
        b = FreezeManifest.build(inputs, schema_version="v0.3", git_sha="abc")
        assert a.manifest_hash == b.manifest_hash

    def test_changed_input_changes_hash(self, tmp_path):
        inputs = _make_inputs(tmp_path)
        a = FreezeManifest.build(inputs, schema_version="v0.3", git_sha="abc")
        (tmp_path / "prompt.txt").write_text("system prompt v2", encoding="utf-8")
        b = FreezeManifest.build(inputs, schema_version="v0.3", git_sha="abc")
        assert a.manifest_hash != b.manifest_hash

    def test_git_sha_and_schema_are_part_of_hash(self, tmp_path):
        inputs = _make_inputs(tmp_path)
        a = FreezeManifest.build(inputs, schema_version="v0.3", git_sha="abc")
        b = FreezeManifest.build(inputs, schema_version="v0.4", git_sha="abc")
        c = FreezeManifest.build(inputs, schema_version="v0.3", git_sha="def")
        assert len({a.manifest_hash, b.manifest_hash, c.manifest_hash}) == 3

    def test_refreeze_count_does_not_change_hash(self, tmp_path):
        inputs = _make_inputs(tmp_path)
        a = FreezeManifest.build(inputs, schema_version="v0.3", git_sha="abc", refreeze_count=0)
        b = FreezeManifest.build(inputs, schema_version="v0.3", git_sha="abc", refreeze_count=1)
        assert a.manifest_hash == b.manifest_hash  # metadata, not an input

    def test_missing_input_raises(self, tmp_path):
        with pytest.raises(ManifestError, match="does not exist"):
            FreezeManifest.build({"missing": tmp_path / "nope"}, schema_version="v0.3")


class TestValidation:
    def test_validate_clean_after_build(self, tmp_path):
        m = FreezeManifest.build(_make_inputs(tmp_path), schema_version="v0.3", git_sha="abc")
        assert m.validate() == []
        assert m.is_valid()

    def test_validate_detects_post_freeze_edit(self, tmp_path):
        m = FreezeManifest.build(_make_inputs(tmp_path), schema_version="v0.3", git_sha="abc")
        (tmp_path / "prompt.txt").write_text("SILENT PATCH", encoding="utf-8")  # EC-25
        assert "agent_system_prompt" in m.validate()
        assert not m.is_valid()

    def test_validate_detects_deleted_input(self, tmp_path):
        m = FreezeManifest.build(_make_inputs(tmp_path), schema_version="v0.3", git_sha="abc")
        (tmp_path / "lock").unlink()
        assert "lockfile" in m.validate()


class TestRefreezeCap:
    def test_under_cap_ok(self):
        FreezeManifest.check_refreeze_cap(MAX_REFREEZES, pm_override=False)  # no raise

    def test_over_cap_without_override_raises(self):
        with pytest.raises(ManifestError, match="exceeds the cap"):
            FreezeManifest.check_refreeze_cap(MAX_REFREEZES + 1, pm_override=False)

    def test_over_cap_with_override_ok(self):
        FreezeManifest.check_refreeze_cap(MAX_REFREEZES + 5, pm_override=True)

    def test_build_enforces_cap(self, tmp_path):
        with pytest.raises(ManifestError, match="exceeds the cap"):
            FreezeManifest.build(
                _make_inputs(tmp_path), schema_version="v0.3",
                refreeze_count=MAX_REFREEZES + 1, pm_override=False,
            )


class TestPersistence:
    def test_save_load_roundtrip(self, tmp_path):
        m = FreezeManifest.build(_make_inputs(tmp_path), schema_version="v0.3", git_sha="abc")
        path = m.save(tmp_path / "campaigns" / "manifest.json")
        loaded = FreezeManifest.load(path)
        assert loaded.manifest_hash == m.manifest_hash
        assert loaded.is_valid()

    def test_load_detects_corrupt_hash(self, tmp_path):
        import json
        m = FreezeManifest.build(_make_inputs(tmp_path), schema_version="v0.3", git_sha="abc")
        path = m.save(tmp_path / "manifest.json")
        d = json.loads(path.read_text())
        d["entries"]["agent_system_prompt"] = "deadbeef" * 8  # tamper, keep stale top hash
        path.write_text(json.dumps(d), encoding="utf-8")
        with pytest.raises(ManifestError, match="corrupt"):
            FreezeManifest.load(path)

    def test_campaign_dir_uses_manifest_hash(self, tmp_path):
        m = FreezeManifest.build(_make_inputs(tmp_path), schema_version="v0.3", git_sha="abc")
        assert m.campaign_dir("campaigns").name == m.manifest_hash
