"""RunRecord — the immutable, write-once artifact of a single run (Story 4.4 / §3.4 / D-4).

A run is a pure function of ``(frozen inputs, run_index, seed)``; its durable output is
one ``RunRecord``. The record carries everything needed to audit and re-score the run
WITHOUT re-running it: the manifest hash (proving which frozen inputs produced it), the
dated model snapshot(s), provider config, seed, the trace location, the realized
in-scope slot set, computed metrics, usage, and the terminal status.

Write-once invariant: ``RunRecord.write`` refuses to overwrite an existing file. A
completed record is never recomputed (idempotent resume — see ``runner.run_campaign``).
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any


class RunStatus(str, Enum):
    """Terminal outcome of a run.

    ``ERRORED`` is distinct from ``INCOMPLETE`` (architecture perf-notes): an
    incomplete run hit the turn cap (a defined outcome); an errored run exhausted
    transient-error retries or raised, and is surfaced in the report — never
    silently dropped.
    """

    COMPLETED = "completed"
    INCOMPLETE = "incomplete"  # hit the §8 invariant-7 turn cap
    ERRORED = "errored"


# Maps a SessionEnd.reason to a RunStatus.
_END_REASON_TO_STATUS = {
    "completed": RunStatus.COMPLETED,
    "incomplete_turn_cap": RunStatus.INCOMPLETE,
    "errored": RunStatus.ERRORED,
}


def status_from_end_reason(reason: str | None) -> RunStatus:
    return _END_REASON_TO_STATUS.get(reason or "", RunStatus.ERRORED)


@dataclass(frozen=True)
class RunRecord:
    """Immutable record of one (manifest, profile, system, run_index) run."""

    manifest_hash: str
    profile_id: str
    system_id: str  # "agent" | "tree"
    run_index: int

    status: RunStatus
    end_reason: str | None = None

    seed: int | None = None
    models: dict[str, str] = field(default_factory=dict)  # {"agent": snapshot, "simulator": snapshot}
    provider_config: dict[str, Any] = field(default_factory=dict)

    trace_path: str | None = None  # path to the JSONL trace, relative to the campaign dir
    in_scope_slots: list[str] = field(default_factory=list)
    metrics: dict[str, Any] = field(default_factory=dict)
    usage: dict[str, Any] | None = None

    # Proves tuning happened on dev only (Story 4.4 AC): scored runs are tagged.
    tag: str = "scored"  # "scored" | "tuning"
    error: str | None = None
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    # ------------------------------------------------------------------
    # Identity
    # ------------------------------------------------------------------

    @staticmethod
    def make_key(profile_id: str, system_id: str, run_index: int) -> str:
        """Stable per-run key (architecture perf-notes idempotency key, minus the
        manifest hash which scopes the campaign directory)."""
        return f"{profile_id}__{system_id}__{run_index:02d}"

    @property
    def key(self) -> str:
        return self.make_key(self.profile_id, self.system_id, self.run_index)

    # ------------------------------------------------------------------
    # Serialization
    # ------------------------------------------------------------------

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["status"] = self.status.value
        return d

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "RunRecord":
        d = dict(d)
        d["status"] = RunStatus(d["status"])
        return cls(**d)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2, sort_keys=True)

    @classmethod
    def load(cls, path: str | Path) -> "RunRecord":
        return cls.from_dict(json.loads(Path(path).read_text(encoding="utf-8")))

    def write(self, path: str | Path, *, overwrite: bool = False) -> Path:
        """Write the record once. Refuses to clobber unless ``overwrite=True``."""
        p = Path(path)
        if p.exists() and not overwrite:
            raise FileExistsError(
                f"RunRecord already exists at {p} — records are write-once (D-4). "
                "A completed run is never recomputed; resume runs only the missing keys."
            )
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(self.to_json(), encoding="utf-8")
        return p
