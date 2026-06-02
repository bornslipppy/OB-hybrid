"""Frame loader + depends_on DAG (architecture §10.2, schema §4).

``SchemaLoader`` parses the field-definition JSON blocks out of
``guesty-pro-account-creation-schema.md`` into ``SlotDef`` objects. ``FrameGraph``
builds the ``depends_on`` reachability graph and evaluates which slots are
reachable for a given set of recorded facts — the shared primitive behind the
``end_section`` guard (state.py) and the scoring in-scope resolver (R-5/R-6).

The depends_on grammar seen in schema v0.3:
    <field> == '<value>'
    <field> in ['<v1>','<v2>', ...]
    <field> includes '<value>'        (membership in a list-valued fact)
    <field> is recorded               (the field has a recorded value)
    <clause> OR <clause>              (disjunction)
Clauses that are not machine-evaluable from facts alone (e.g. "user volunteers a
split", "user volunteers website intent") are treated as runtime *signals*: False
unless explicitly supplied via the ``signals`` map (FR-4 / EC-27).
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

_HEADING_SECTION = re.compile(r"^#{1,6}\s+(S\d[a-z]?)\b")
_JSON_FENCE_OPEN = re.compile(r"^```json\s*$")
_FENCE_CLOSE = re.compile(r"^```\s*$")


@dataclass
class SlotDef:
    """One field in the frame. Mirrors the schema field metadata (schema §1)."""

    id: str
    section: str
    priority: str = "optional"  # required | recommended | optional
    type: str = ""
    depends_on: str | None = None
    surface_when: str | None = None
    echo_before_write: bool = False
    human_handoff: str | None = None
    options: list[str] = field(default_factory=list)
    item_shape: dict[str, Any] = field(default_factory=dict)
    raw: dict[str, Any] = field(default_factory=dict)

    @property
    def condition(self) -> str | None:
        """The reachability guard for this slot (``depends_on`` else ``surface_when``)."""
        return self.depends_on or self.surface_when


def _strip_jsonc_comments(text: str) -> str:
    """Remove ``//`` line comments while preserving ``//`` inside string literals."""
    out: list[str] = []
    in_string = False
    escaped = False
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        if in_string:
            out.append(ch)
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                in_string = False
            i += 1
            continue
        if ch == '"':
            in_string = True
            out.append(ch)
            i += 1
            continue
        if ch == "/" and i + 1 < n and text[i + 1] == "/":
            # Skip to end of line.
            while i < n and text[i] != "\n":
                i += 1
            continue
        out.append(ch)
        i += 1
    return "".join(out)


class SchemaLoader:
    """Parses the schema markdown's field-definition JSON blocks into ``SlotDef``s."""

    def load(self, schema_path: str | Path) -> list[SlotDef]:
        lines = Path(schema_path).read_text(encoding="utf-8").splitlines()
        slots: list[SlotDef] = []
        current_section: str | None = None
        i = 0
        n = len(lines)
        while i < n:
            line = lines[i]
            heading = _HEADING_SECTION.match(line.strip())
            if heading:
                current_section = heading.group(1)
                i += 1
                continue
            if _JSON_FENCE_OPEN.match(line.strip()):
                block: list[str] = []
                i += 1
                while i < n and not _FENCE_CLOSE.match(lines[i].strip()):
                    block.append(lines[i])
                    i += 1
                i += 1  # consume closing fence
                slots.extend(self._parse_block("\n".join(block), current_section))
                continue
            i += 1
        return slots

    def _parse_block(self, raw: str, section: str | None) -> list[SlotDef]:
        cleaned = _strip_jsonc_comments(raw)
        try:
            data = json.loads(cleaned)
        except json.JSONDecodeError:
            return []  # non field-definition block (e.g. a runtime-state example)
        objects = data if isinstance(data, list) else [data]
        out: list[SlotDef] = []
        for obj in objects:
            if not isinstance(obj, dict) or "id" not in obj:
                continue  # only field definitions become SlotDefs
            out.append(self._to_slot_def(obj, section))
        return out

    @staticmethod
    def _to_slot_def(obj: dict[str, Any], section: str | None) -> SlotDef:
        return SlotDef(
            id=obj["id"],
            section=obj.get("section") or section or "",
            priority=obj.get("priority", "optional"),
            type=obj.get("type", ""),
            depends_on=obj.get("depends_on"),
            surface_when=obj.get("surface_when"),
            echo_before_write=bool(obj.get("echo_before_write", False)),
            human_handoff=obj.get("human_handoff"),
            options=list(obj.get("options", [])),
            item_shape=dict(obj.get("item_shape", {})),
            raw=obj,
        )


# --- depends_on condition evaluation ----------------------------------------

_RE_IS_RECORDED = re.compile(r"^(\w+)\s+is\s+recorded$", re.IGNORECASE)
_RE_INCLUDES = re.compile(r"^(\w+)\s+includes\s+'([^']+)'$", re.IGNORECASE)
_RE_IN_LIST = re.compile(r"^(\w+)\s+in\s+\[(.*)\]$", re.IGNORECASE)
_RE_EQ = re.compile(r"^(\w+)\s*==\s*'([^']+)'$")


def _eval_clause(clause: str, facts: dict[str, Any], signals: dict[str, bool]) -> bool:
    clause = clause.strip()

    m = _RE_IS_RECORDED.match(clause)
    if m:
        val = facts.get(m.group(1))
        return val is not None

    m = _RE_INCLUDES.match(clause)
    if m:
        field_val = facts.get(m.group(1))
        return isinstance(field_val, (list, tuple, set)) and m.group(2) in field_val

    m = _RE_IN_LIST.match(clause)
    if m:
        options = [p.strip().strip("'\"") for p in m.group(2).split(",") if p.strip()]
        return facts.get(m.group(1)) in options

    m = _RE_EQ.match(clause)
    if m:
        return facts.get(m.group(1)) == m.group(2)

    # Not machine-evaluable from facts (e.g. "user volunteers a split"). Look it up
    # as an explicit runtime signal; default False.
    key = re.sub(r"[^a-z0-9]+", "_", clause.lower()).strip("_")
    return bool(signals.get(key, False))


def evaluate_condition(
    condition: str | None,
    facts: dict[str, Any],
    signals: dict[str, bool] | None = None,
) -> bool:
    """Evaluate a depends_on/surface_when condition. ``None`` means unconditional."""
    if condition is None:
        return True
    signals = signals or {}
    # Disjunction only (no AND appears in schema v0.3); any clause true -> reachable.
    return any(
        _eval_clause(part, facts, signals)
        for part in re.split(r"\s+OR\s+", condition, flags=re.IGNORECASE)
    )


class FrameGraph:
    """The depends_on reachability graph over a list of ``SlotDef``s."""

    def __init__(self, slots: list[SlotDef]) -> None:
        self.slots = slots
        self._by_id = {s.id: s for s in slots}
        # Edge map child_id -> the fields its guard references (for cascade work).
        self.depends_on_fields: dict[str, list[str]] = {
            s.id: self._referenced_fields(s.condition) for s in slots
        }

    def get(self, slot_id: str) -> SlotDef | None:
        return self._by_id.get(slot_id)

    def reachable_slots(
        self,
        profile_facts: dict[str, Any],
        sections: list[str],
        signals: dict[str, bool] | None = None,
    ) -> list[SlotDef]:
        """Every slot in ``sections`` whose guard is satisfied by ``profile_facts``."""
        wanted = set(sections)
        return [
            s
            for s in self.slots
            if s.section in wanted
            and evaluate_condition(s.condition, profile_facts, signals)
        ]

    @staticmethod
    def _referenced_fields(condition: str | None) -> list[str]:
        if condition is None:
            return []
        fields: list[str] = []
        for part in re.split(r"\s+OR\s+", condition, flags=re.IGNORECASE):
            for rx in (_RE_IS_RECORDED, _RE_INCLUDES, _RE_IN_LIST, _RE_EQ):
                m = rx.match(part.strip())
                if m:
                    fields.append(m.group(1))
                    break
        return fields
