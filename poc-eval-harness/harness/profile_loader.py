"""Profile loader — split a frozen profile JSON into (respondent spec, answer key).

The on-disk profile bundles facts + persona + answer key in one file for authoring
convenience, but the simulator must NEVER receive the answer key (FR-19/FR-20). This
loader is the split point: it builds a ``RespondentSpec`` from facts/persona ONLY and a
separate ``AnswerKey`` from the dispositions. The spec's own ``__post_init__`` guard
rejects any answer-key field that leaks into ``facts``.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

from scoring.sar import AnswerKey, parse_disposition
from simulator.simulator import RespondentSpec

# H1 sections scored across the whole frame.
DEFAULT_H1_SECTIONS: list[str] = ["S0a", "S0b", "S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8"]


@dataclass(frozen=True)
class ProfileBundle:
    profile_id: str
    group: str
    spec: RespondentSpec           # facts + persona — NO answer key
    answer_key: AnswerKey
    sections: list[str] = field(default_factory=lambda: list(DEFAULT_H1_SECTIONS))
    tuning_only: bool = False
    advice_slots: list[str] = field(default_factory=list)


def load_profile(path: str | Path) -> ProfileBundle:
    """Load one profile JSON into a ``ProfileBundle`` (spec and key kept separate)."""
    data: dict[str, Any] = json.loads(Path(path).read_text(encoding="utf-8"))
    profile_id = data["profile_id"]
    group = data["group"]

    spec = RespondentSpec(
        profile_id=profile_id,
        group=group,
        facts=dict(data.get("facts", {})),  # facts ONLY — RespondentSpec guards against key leak
        persona=data.get("persona", ""),
        conversation_notes=data.get("conversation_notes", ""),
        variant_overrides=dict(data.get("variant_overrides", {})),
    )

    raw_key: dict[str, str] = data.get("answer_key", {})
    answer_key = AnswerKey(
        profile_id=profile_id,
        group=group,
        slots={sid: parse_disposition(str(raw), sid) for sid, raw in raw_key.items()},
    )

    return ProfileBundle(
        profile_id=profile_id,
        group=group,
        spec=spec,
        answer_key=answer_key,
        sections=list(data.get("sections", DEFAULT_H1_SECTIONS)),
        tuning_only=bool(data.get("tuning_only", False)),
        advice_slots=list(data.get("advice_slots", [])),
    )


def make_dir_loader(profiles_dir: str | Path) -> Callable[[str], ProfileBundle]:
    """A ``profile_id -> ProfileBundle`` loader reading ``{profiles_dir}/{profile_id}.json``."""
    base = Path(profiles_dir)

    def _load(profile_id: str) -> ProfileBundle:
        return load_profile(base / f"{profile_id}.json")

    return _load
