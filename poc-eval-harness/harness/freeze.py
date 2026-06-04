"""Freeze-manifest generation (Story 4.4 / §5.2 / D-5).

Builds the full ``FreezeManifest`` from a loaded ``RunConfig`` by content-hashing the
§5.2 input set (8 scored profiles + answer keys, agent system prompt, tree module,
simulator scripted turns, run-config, scoring module, schema, lockfile) plus the git
SHA and schema version. This is the manifest that supersedes the kernel-only
``campaigns/proto-manifest.json`` and gates every ``--frozen`` campaign run.

Use as a library (``build_freeze_manifest``) or standalone::

    uv run python -m harness.freeze            # writes campaigns/manifest.json
    uv run python -m harness.freeze --out /tmp/manifest.json
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from harness.manifest import FreezeManifest, current_git_sha, default_manifest_inputs

_VERSION_RE = re.compile(r"^version:\s*(.+)$", re.MULTILINE)


def schema_version(schema_path: str | Path) -> str:
    """Read the ``version:`` front-matter line from the schema markdown (R-7 audit)."""
    text = Path(schema_path).read_text(encoding="utf-8")
    m = _VERSION_RE.search(text)
    return m.group(1).strip() if m else "unknown"


def _read_refreeze_state(path: Path) -> tuple[int, bool]:
    """Load (refreeze_count, pm_override) from the persisted counter; default (0, False)."""
    if path.exists():
        d = json.loads(path.read_text(encoding="utf-8"))
        return int(d.get("refreeze_count", 0)), bool(d.get("pm_override", False))
    return 0, False


def build_freeze_manifest(config: Any, root: str | Path = ".") -> FreezeManifest:
    """Content-hash the §5.2 inputs into a ``FreezeManifest`` (raises on any missing path)."""
    root = Path(root)
    inputs = default_manifest_inputs(config, root)
    refreeze_count, pm_override = _read_refreeze_state(root / config.refreeze_count_path)
    return FreezeManifest.build(
        inputs,
        schema_version=schema_version(root / config.schema_path),
        git_sha=current_git_sha(root),
        refreeze_count=refreeze_count,
        pm_override=pm_override,
    )


def main(argv: list[str] | None = None) -> int:
    from config.config_loader import load_run_config

    ap = argparse.ArgumentParser(
        prog="harness.freeze",
        description="Generate the §5.2 freeze manifest from run_config inputs.",
    )
    ap.add_argument("--config", default="config/run_config.toml")
    ap.add_argument("--root", default=".")
    ap.add_argument("--out", default=None, help="Output path (default: <root>/<config.manifest_path>).")
    args = ap.parse_args(argv)

    root = Path(args.root)
    cfg_path = Path(args.config)
    config = load_run_config(cfg_path if cfg_path.is_absolute() else root / cfg_path)

    manifest = build_freeze_manifest(config, root)
    out = Path(args.out) if args.out else root / config.manifest_path
    manifest.save(out)

    mismatches = manifest.validate()
    print(f"freeze manifest : {manifest.short_hash}  ({len(manifest.entries)} inputs)")
    print(f"git sha         : {manifest.git_sha or '—'}")
    print(f"schema version  : {manifest.schema_version}")
    print(f"refreeze count  : {manifest.refreeze_count}")
    print(f"written to      : {out}")
    print(f"validate        : {'CLEAN' if not mismatches else 'MISMATCH ' + str(mismatches)}")
    return 0 if not mismatches else 1


if __name__ == "__main__":
    raise SystemExit(main())
