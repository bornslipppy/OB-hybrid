"""In-scope slot resolver — the single source of truth for the SAR denominator.

``resolve_inscope_slots`` is the most load-bearing pure function in the system
(architecture §6.1 / R-5 / R-6). It is used in two places:

  1. **SAR denominator computation** — the set of slots the system is scored
     against for a given profile.
  2. **Cascade/sensitivity re-resolution** (§6.5) — when a contested slot
     is a ``depends_on`` root, the whole downstream disposition set is
     re-resolved under best/worst adjudication. The band must propagate through
     the dependency chain, so this one function must be called for both uses.

Design invariants:
  - Pure function: no side effects, always the same output for the same inputs.
  - Consumes only the *public schema* (FrameGraph over SlotDefs) + profile facts.
    It never sees the answer key — so the denominator and the scoring use
    identical reachability logic without any answer-key leak (D-6 / FR-10).
  - The adjudication-choice parameter (BEST / WORST) governs how *absent*
    ``depends_on`` roots are treated: BEST assumes the most favorable path
    (root treated as satisfied), WORST treats them as unsatisfied.
    Only *absent* roots are affected — *present* roots are always evaluated
    against their recorded value, regardless of adjudication choice.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any

from kernel.schema import FrameGraph, SchemaLoader, SlotDef, evaluate_condition


class AdjudicationChoice(str, Enum):
    """How to treat absent depends_on roots in the sensitivity band (§6.5 / R-6).

    NEUTRAL is the default (exact facts only — no expansion or contraction).
    BEST expands the denominator (assume contested root is satisfied / present).
    WORST contracts the denominator (assume contested root is absent / fails).
    """

    NEUTRAL = "neutral"
    BEST = "best"
    WORST = "worst"


@dataclass(frozen=True)
class ResolvedSlot:
    """One in-scope slot entry in the SAR denominator.

    Carries the metadata the SAR scorer needs without re-querying the schema.
    """

    slot_id: str
    section: str
    priority: str  # "required" | "recommended" | "optional"
    echo_before_write: bool
    human_handoff: str | None
    depends_on: str | None
    type: str
    slot_def: SlotDef  # the original def, for downstream scoring helpers


def _load_frame(schema_path: str | Path) -> FrameGraph:
    slots = SchemaLoader().load(schema_path)
    return FrameGraph(slots)


# Module-level schema cache: FrameGraph is expensive to re-parse per call.
_FRAME_CACHE: dict[str, FrameGraph] = {}


def _get_frame(schema_path: str | Path) -> FrameGraph:
    key = str(Path(schema_path).resolve())
    if key not in _FRAME_CACHE:
        _FRAME_CACHE[key] = _load_frame(key)
    return _FRAME_CACHE[key]


def resolve_inscope_slots(
    profile_facts: dict[str, Any],
    sections: list[str],
    *,
    schema_path: str | Path,
    adjudication: AdjudicationChoice = AdjudicationChoice.NEUTRAL,
    signals: dict[str, bool] | None = None,
) -> list[ResolvedSlot]:
    """Compute the in-scope slot set (SAR denominator) for ``profile_facts``.

    Args:
        profile_facts:
            Recorded profile facts (field_id -> value). These are the ground-truth
            inputs from the profile spec (not a live ProfileState) — every value here
            is treated as confirmed. For adjudication purposes, *absent* keys are the
            roots that may be contested.
        sections:
            The section IDs to include (e.g. ``["S2", "S4", "S8"]``). Only slots
            in these sections are considered.
        schema_path:
            Path to the schema markdown file (frozen in the manifest, §5.2).
        adjudication:
            NEUTRAL (default) evaluates conditions strictly against present facts.
            BEST assumes absent roots are satisfied (maximum denominator).
            WORST assumes absent roots are not satisfied (minimum denominator).
        signals:
            Runtime signals for non-evaluable depends_on clauses (e.g.
            ``user_volunteers_a_split``). These are evaluated as-is regardless of
            adjudication choice (they represent conversational context, not facts).

    Returns:
        A deduplicated, schema-order list of ``ResolvedSlot`` objects — each
        representing one slot in the SAR denominator.
    """
    frame = _get_frame(schema_path)
    signals = signals or {}

    # Collect slots from the requested sections in schema order.
    wanted = set(sections)
    result: list[ResolvedSlot] = []
    seen: set[str] = set()

    for slot_def in frame.slots:
        if slot_def.section not in wanted:
            continue
        if slot_def.id in seen:
            continue

        condition = slot_def.condition
        if _eval_with_adjudication(condition, profile_facts, signals, adjudication, frame):
            result.append(
                ResolvedSlot(
                    slot_id=slot_def.id,
                    section=slot_def.section,
                    priority=slot_def.priority,
                    echo_before_write=slot_def.echo_before_write,
                    human_handoff=slot_def.human_handoff,
                    depends_on=slot_def.depends_on,
                    type=slot_def.type,
                    slot_def=slot_def,
                )
            )
            seen.add(slot_def.id)

    return result


def _eval_with_adjudication(
    condition: str | None,
    facts: dict[str, Any],
    signals: dict[str, bool],
    adjudication: AdjudicationChoice,
    frame: FrameGraph,
) -> bool:
    """Evaluate a condition with adjudication semantics for absent root fields.

    For NEUTRAL and when all referenced fields are present: standard evaluation.
    For BEST: if any referenced field is absent, assume that clause is True.
    For WORST: if any referenced field is absent, assume that clause is False.
    """
    if condition is None:
        return True

    if adjudication is AdjudicationChoice.NEUTRAL:
        return evaluate_condition(condition, facts, signals)

    # Adjudication only applies to *absent* root fields. If all referenced
    # fields are present, evaluate normally (the contested value is decided).
    import re

    clauses = re.split(r"\s+OR\s+", condition, flags=re.IGNORECASE)
    clause_results: list[bool] = []
    for clause in clauses:
        # Extract the referenced field name from the clause (if any).
        ref_field = _extract_field_name(clause.strip())
        if ref_field is not None and ref_field not in facts:
            # The root field is absent — adjudication governs the outcome.
            if adjudication is AdjudicationChoice.BEST:
                clause_results.append(True)
            else:  # WORST
                clause_results.append(False)
        else:
            # Root is present (or clause has no evaluable field) — evaluate normally.
            from kernel.schema import _eval_clause
            clause_results.append(_eval_clause(clause.strip(), facts, signals))

    return any(clause_results)


def _extract_field_name(clause: str) -> str | None:
    """Return the LHS field name from a simple depends_on clause, or None."""
    import re

    patterns = [
        r"^(\w+)\s+is\s+recorded$",
        r"^(\w+)\s+includes\s+",
        r"^(\w+)\s+in\s+\[",
        r"^(\w+)\s*==\s*'",
    ]
    for pat in patterns:
        m = re.match(pat, clause, re.IGNORECASE)
        if m:
            return m.group(1)
    return None
