"""FreezeManifest — content-hash gate for the frozen campaign (Story 4.4 / §5.2 / D-5).

Freeze = a ``manifest.json`` capturing **content hashes** of every input that could
change the result. The harness refuses to run in ``--frozen`` mode without a valid
manifest, and stamps the manifest hash into every ``RunRecord``. A post-freeze change
to *any* hashed input ⇒ hash mismatch ⇒ a forced re-freeze (new manifest, incremented
counter). Re-freezes are capped at 2 (FR-26); exceeding requires a recorded
``pm_override`` flag and is reported as a multiple-comparisons risk.

The manifest replaces the placeholder ``campaigns/proto-manifest.json``: it covers the
SUTs, the simulator, AND the scoring harness (EC-25) — a "silent patch" is impossible
because the patched file's hash no longer matches the manifest.

Hashed inputs (§5.2):
  * each of the 8 scored profiles + answer keys
  * the agent system prompt
  * the tree module
  * the simulator config + scripted turns
  * the scoring module
  * the schema version
  * the dependency lockfile
  * the git SHA
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# Re-freeze cap (FR-26): more than this many re-freezes requires a PM override.
MAX_REFREEZES = 2

_HASH_CHUNK = 1 << 16


class ManifestError(RuntimeError):
    """Raised on a freeze-discipline violation (missing manifest, cap exceeded, mismatch)."""


# ---------------------------------------------------------------------------
# Content hashing
# ---------------------------------------------------------------------------


def _hash_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        while chunk := fh.read(_HASH_CHUNK):
            h.update(chunk)
    return h.hexdigest()


def _hash_path(path: Path) -> str:
    """Content hash of a file, or of a directory tree (sorted, path-tagged).

    Directory hashing is order-independent and includes relative paths, so a renamed
    or moved file changes the hash. ``.pyc``/``__pycache__`` are excluded.
    """
    if path.is_file():
        return _hash_file(path)
    if path.is_dir():
        h = hashlib.sha256()
        files = sorted(
            p for p in path.rglob("*")
            if p.is_file() and "__pycache__" not in p.parts and p.suffix not in {".pyc", ".pyo"}
        )
        for p in files:
            rel = p.relative_to(path).as_posix()
            h.update(rel.encode("utf-8"))
            h.update(b"\0")
            h.update(_hash_file(p).encode("ascii"))
            h.update(b"\0")
        return h.hexdigest()
    raise ManifestError(f"manifest input does not exist: {path}")


def current_git_sha(root: str | Path = ".") -> str | None:
    """Best-effort current commit SHA; ``None`` if not a git checkout."""
    try:
        out = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=str(root), capture_output=True, text=True, check=True,
        )
        return out.stdout.strip() or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


# ---------------------------------------------------------------------------
# FreezeManifest
# ---------------------------------------------------------------------------


@dataclass
class FreezeManifest:
    """A content-hashed snapshot of all frozen inputs."""

    entries: dict[str, str]  # logical name -> sha256 of that input
    git_sha: str | None
    schema_version: str
    refreeze_count: int = 0
    pm_override: bool = False
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    # Resolved absolute paths kept for re-validation; not part of the hash.
    _resolved_paths: dict[str, str] = field(default_factory=dict, repr=False)

    # ------------------------------------------------------------------
    # The fingerprint
    # ------------------------------------------------------------------

    @property
    def manifest_hash(self) -> str:
        """Deterministic fingerprint of the frozen inputs (entries + git SHA + schema).

        ``refreeze_count`` / ``pm_override`` are freeze *metadata*, not inputs, so they
        do NOT change the hash — two re-freezes with identical inputs (e.g. a forced
        model-deprecation re-freeze) share a content fingerprint by design.
        """
        payload = {
            "entries": dict(sorted(self.entries.items())),
            "git_sha": self.git_sha,
            "schema_version": self.schema_version,
        }
        blob = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        return hashlib.sha256(blob).hexdigest()

    @property
    def short_hash(self) -> str:
        return self.manifest_hash[:12]

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    @classmethod
    def build(
        cls,
        inputs: dict[str, Path],
        *,
        schema_version: str,
        git_sha: str | None = None,
        refreeze_count: int = 0,
        pm_override: bool = False,
    ) -> "FreezeManifest":
        """Content-hash every input. ``inputs`` maps a logical name to a file or dir.

        Raises ``ManifestError`` if any input path is missing (a frozen manifest must
        hash real, present inputs), or if the re-freeze cap is exceeded without override.
        """
        cls.check_refreeze_cap(refreeze_count, pm_override)
        entries: dict[str, str] = {}
        resolved: dict[str, str] = {}
        for name, path in sorted(inputs.items()):
            p = Path(path)
            entries[name] = _hash_path(p)
            resolved[name] = str(p.resolve())
        return cls(
            entries=entries,
            git_sha=git_sha,
            schema_version=schema_version,
            refreeze_count=refreeze_count,
            pm_override=pm_override,
            _resolved_paths=resolved,
        )

    @staticmethod
    def check_refreeze_cap(refreeze_count: int, pm_override: bool) -> None:
        """Enforce FR-26: > MAX_REFREEZES re-freezes requires a recorded PM override."""
        if refreeze_count > MAX_REFREEZES and not pm_override:
            raise ManifestError(
                f"refreeze_count={refreeze_count} exceeds the cap of {MAX_REFREEZES} "
                "(FR-26). A further re-freeze requires pm_override=True, and the run is "
                "reported as a multiple-comparisons risk."
            )

    # ------------------------------------------------------------------
    # Validation (re-hash the recorded inputs and compare)
    # ------------------------------------------------------------------

    def validate(self) -> list[str]:
        """Re-hash every recorded input path; return the list of mismatched names.

        An empty list means every frozen input still matches its recorded hash. Names
        whose paths are missing or changed are returned so the caller can force a
        re-freeze (EC-25: a silent patch is structurally impossible).
        """
        mismatches: list[str] = []
        for name, expected in self.entries.items():
            resolved = self._resolved_paths.get(name)
            if resolved is None:
                mismatches.append(name)
                continue
            p = Path(resolved)
            if not p.exists():
                mismatches.append(name)
                continue
            if _hash_path(p) != expected:
                mismatches.append(name)
        return mismatches

    def is_valid(self) -> bool:
        try:
            return not self.validate()
        except ManifestError:
            return False

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def to_dict(self) -> dict[str, Any]:
        return {
            "manifest_hash": self.manifest_hash,
            "entries": dict(sorted(self.entries.items())),
            "git_sha": self.git_sha,
            "schema_version": self.schema_version,
            "refreeze_count": self.refreeze_count,
            "pm_override": self.pm_override,
            "created_at": self.created_at,
            "resolved_paths": dict(sorted(self._resolved_paths.items())),
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2, sort_keys=True)

    def save(self, path: str | Path) -> Path:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(self.to_json(), encoding="utf-8")
        return p

    @classmethod
    def load(cls, path: str | Path) -> "FreezeManifest":
        d = json.loads(Path(path).read_text(encoding="utf-8"))
        stored = d.get("manifest_hash")
        m = cls(
            entries=d["entries"],
            git_sha=d.get("git_sha"),
            schema_version=d["schema_version"],
            refreeze_count=d.get("refreeze_count", 0),
            pm_override=d.get("pm_override", False),
            created_at=d.get("created_at", ""),
            _resolved_paths=d.get("resolved_paths", {}),
        )
        # Integrity guard: a hand-edited entries block whose recorded hash no longer
        # matches the recomputed fingerprint is itself a tamper signal.
        if stored is not None and stored != m.manifest_hash:
            raise ManifestError(
                f"manifest file {path} is corrupt: stored hash {stored[:12]} != "
                f"recomputed {m.short_hash}."
            )
        return m

    def campaign_dir(self, base: str | Path = "campaigns") -> Path:
        """The immutable per-manifest campaign directory ``campaigns/<manifest_hash>/``."""
        return Path(base) / self.manifest_hash


# ---------------------------------------------------------------------------
# Default input map from RunConfig (§5.2)
# ---------------------------------------------------------------------------


def default_manifest_inputs(config: Any, root: str | Path = ".") -> dict[str, Path]:
    """Build the standard §5.2 input map from a loaded ``RunConfig``.

    Only paths that exist are included; the caller (``build``) will raise on any
    missing path, surfacing an incomplete freeze early.
    """
    root = Path(root)
    return {
        "scored_profiles": root / config.scored_dir,
        "agent_system_prompt": root / "agent" / "prompts" / "system_prompt.txt",
        "tree_module": root / "tree",
        "simulator_scripted_turns": root / "simulator" / "scripted_turns",
        "run_config": root / "config" / "run_config.toml",
        "scoring_module": root / "scoring",
        "schema": root / config.schema_path,
        "lockfile": root / "uv.lock",
    }
