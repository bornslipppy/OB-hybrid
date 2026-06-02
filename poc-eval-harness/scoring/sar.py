"""SAR (Slot Accuracy Rate) scorer — Story 4.5.

Implements the §6.1 scoring rubric:

  recorded:<value>  → score 1 if the system recorded the slot with a matching
                      value (exact for enums/numbers; human-rated for free-text).
                      Score 0 if missing, skipped, flagged, or wrong value.
  flagged           → score 1 if the system used FlagForCall1 for the slot
                      without recording a definitive answer. Score 0 if
                      definitively recorded or silently dropped.
  skipped           → excluded from SAR denominator (not scored).

Cascade/sensitivity-band support (§6.5 / R-6):
  ``cascade_tag`` re-resolves the denominator under BEST and WORST adjudication
  for a set of contested slots (those without agreed ground truth), producing
  a SAR sensitivity band. This is called once per profile, after scoring with
  adjudicated values.

Design invariants:
  - The scorer is a pure function over (ProfileState, AnswerKey, sections, schema).
  - It consumes only the *final* ProfileState from the system run.
  - Value matching for free-text types (``pain``, ``split_terms``) is flagged as
    ``requires_human_rating=True`` — programmatic string equality is inappropriate
    for narrative values (§6.1 value-match tolerance).
  - Numbers (money/percentages) require exact match — a misheard 15% vs 50% is
    a failure (§6.1 / research §7).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal

from kernel.state import ProfileState, SlotStatus
from scoring.resolver import AdjudicationChoice, resolve_inscope_slots

# ---------------------------------------------------------------------------
# Answer-key data structures
# ---------------------------------------------------------------------------

_FREE_TEXT_SLOTS = {"pain", "split_terms", "notes", "handover_note_raw"}
_NUMERIC_TYPES = {"percentage", "money", "integer", "float"}


@dataclass
class ExpectedDisposition:
    """Parsed form of one answer-key entry.

    Attributes:
        disposition: "recorded" | "flagged" | "skipped" | "conditional"
        value:       The expected value for "recorded" dispositions.
        value_type:  How to compare the value: "exact" | "numeric" | "free_text"
        condition:   For "conditional" entries, the surfacing condition string.
        provisional: True for G3-provisional entries (enum casing may change).
    """

    disposition: Literal["recorded", "flagged", "skipped", "conditional"]
    value: Any = None
    value_type: Literal["exact", "numeric", "free_text"] = "exact"
    condition: str | None = None
    provisional: bool = False


@dataclass
class AnswerKey:
    """Ground-truth answer key for one profile.

    ``slots`` maps slot_id -> ExpectedDisposition.
    Only slots whose expected disposition is NOT ``skipped`` are in the
    SAR denominator (see ``denominator_slots`` property).
    """

    profile_id: str
    group: str  # "A" | "B" | "C"
    slots: dict[str, ExpectedDisposition] = field(default_factory=dict)

    def denominator_slots(self) -> dict[str, ExpectedDisposition]:
        """Slots in the SAR denominator (everything except skipped + conditional)."""
        return {
            sid: disp
            for sid, disp in self.slots.items()
            if disp.disposition not in ("skipped", "conditional")
        }


# ---------------------------------------------------------------------------
# Score results
# ---------------------------------------------------------------------------


@dataclass
class SlotScore:
    """Scoring result for one slot."""

    slot_id: str
    section: str
    expected_disposition: str
    expected_value: Any
    actual_status: SlotStatus | str
    actual_value: Any
    score: int  # 1 = correct, 0 = wrong
    reason: str
    requires_human_rating: bool = False


@dataclass
class ProfileScore:
    """SAR result for one (profile, system) pair."""

    profile_id: str
    group: str  # "A" | "B" | "C"
    system_id: str
    sar: float  # numerator / denominator
    numerator: int
    denominator: int
    slot_scores: list[SlotScore] = field(default_factory=list)
    skipped_slots: list[str] = field(default_factory=list)
    human_rating_pending: list[str] = field(default_factory=list)


@dataclass
class CascadeResult:
    """Sensitivity band from cascade re-resolution (§6.5)."""

    profile_id: str
    contested_slots: list[str]
    sar_nominal: float  # with adjudicated values (full facts)
    sar_best: float  # contested roots assumed satisfied → widest denominator
    sar_worst: float  # contested roots assumed absent → narrowest denominator
    denominator_nominal: int
    denominator_best: int
    denominator_worst: int


# ---------------------------------------------------------------------------
# Disposition parsing
# ---------------------------------------------------------------------------

_PROVISIONAL_MARK = re.compile(r"\[provisional\s+\w+\]", re.IGNORECASE)


def parse_disposition(raw: str, slot_id: str = "") -> ExpectedDisposition:
    """Parse a raw disposition string from the answer-key format into ``ExpectedDisposition``.

    Accepted formats (case-insensitive prefix matching):
      - ``recorded: <value>``
      - ``flagged`` / ``flag_for_call_1`` / ``flagged: <reason>``
      - ``skipped``
      - ``conditional: <condition>``
    """
    # Strip provisional markers before parsing.
    raw_clean = _PROVISIONAL_MARK.sub("", raw).strip()
    provisional = bool(_PROVISIONAL_MARK.search(raw))

    lower = raw_clean.lower()

    # --- skipped ---
    if lower.startswith("skipped") or lower == "skip":
        return ExpectedDisposition(disposition="skipped", provisional=provisional)

    # --- flagged ---
    if lower.startswith("flagged") or lower.startswith("flag_for_call_1") or lower == "flag":
        return ExpectedDisposition(disposition="flagged", provisional=provisional)

    # --- conditional ---
    if lower.startswith("conditional"):
        condition = raw_clean[raw_clean.index(":") + 1:].strip() if ":" in raw_clean else ""
        return ExpectedDisposition(
            disposition="conditional", condition=condition, provisional=provisional
        )

    # --- recorded ---
    if lower.startswith("recorded"):
        value_str = raw_clean[raw_clean.index(":") + 1:].strip() if ":" in raw_clean else ""
        value = _parse_value(value_str, slot_id)
        value_type = _classify_value_type(slot_id, value)
        return ExpectedDisposition(
            disposition="recorded",
            value=value,
            value_type=value_type,
            provisional=provisional,
        )

    # Fallback: treat anything else as recorded with the raw string as the value.
    return ExpectedDisposition(
        disposition="recorded",
        value=raw_clean,
        value_type=_classify_value_type(slot_id, raw_clean),
        provisional=provisional,
    )


def _parse_value(value_str: str, slot_id: str = "") -> Any:
    """Light parsing: try int, float, then return as string."""
    if not value_str:
        return None
    stripped = value_str.strip("\"'")
    # Free-text slots: return as-is without numeric coercion.
    if slot_id in _FREE_TEXT_SLOTS:
        return stripped
    try:
        return int(stripped)
    except ValueError:
        pass
    try:
        return float(stripped)
    except ValueError:
        pass
    # List-like: [a, b, c]
    if stripped.startswith("[") and stripped.endswith("]"):
        inner = stripped[1:-1]
        items = [p.strip().strip("\"'") for p in inner.split(",") if p.strip()]
        return items
    return stripped


def _classify_value_type(slot_id: str, value: Any) -> Literal["exact", "numeric", "free_text"]:
    if slot_id in _FREE_TEXT_SLOTS:
        return "free_text"
    if isinstance(value, (int, float)):
        return "numeric"
    return "exact"


# ---------------------------------------------------------------------------
# Slot scoring (§6.1 rubric)
# ---------------------------------------------------------------------------


def score_slot(
    slot_id: str,
    section: str,
    expected: ExpectedDisposition,
    state: ProfileState,
) -> SlotScore:
    """Score one slot against its expected disposition.

    Args:
        slot_id:  The slot being scored.
        section:  Section label for reporting (e.g. "S4").
        expected: The parsed expected disposition from the answer key.
        state:    The final ProfileState from the system run.
    Returns:
        A ``SlotScore`` with score 1 (correct) or 0 (wrong).
    """
    slot = state.slots.get(slot_id)
    actual_status = slot.status if slot else SlotStatus.UNANSWERED
    actual_value = slot.value if slot else None

    expected_str = (
        f"recorded:{expected.value}"
        if expected.disposition == "recorded"
        else expected.disposition
    )

    # --- expected: flagged ---
    if expected.disposition == "flagged":
        if actual_status is SlotStatus.FLAGGED:
            return SlotScore(
                slot_id=slot_id, section=section,
                expected_disposition="flagged", expected_value=None,
                actual_status=actual_status, actual_value=actual_value,
                score=1, reason="correctly flagged for Call 1",
            )
        elif actual_status is SlotStatus.RECORDED:
            return SlotScore(
                slot_id=slot_id, section=section,
                expected_disposition="flagged", expected_value=None,
                actual_status=actual_status, actual_value=actual_value,
                score=0, reason="recorded a definitive answer instead of flagging",
            )
        else:
            return SlotScore(
                slot_id=slot_id, section=section,
                expected_disposition="flagged", expected_value=None,
                actual_status=actual_status, actual_value=actual_value,
                score=0, reason=f"slot not dispositioned (status={actual_status}); should have been flagged",
            )

    # --- expected: recorded ---
    if expected.disposition == "recorded":
        if actual_status is not SlotStatus.RECORDED:
            return SlotScore(
                slot_id=slot_id, section=section,
                expected_disposition=expected_str, expected_value=expected.value,
                actual_status=actual_status, actual_value=actual_value,
                score=0, reason=f"expected recorded; got {actual_status}",
            )

        # Free-text: flag for human rating.
        if expected.value_type == "free_text":
            return SlotScore(
                slot_id=slot_id, section=section,
                expected_disposition=expected_str, expected_value=expected.value,
                actual_status=actual_status, actual_value=actual_value,
                score=1, reason="recorded (free-text; human rating required for correctness)",
                requires_human_rating=True,
            )

        # Numeric: exact match on parsed float.
        if expected.value_type == "numeric":
            ok = _numeric_match(expected.value, actual_value)
            return SlotScore(
                slot_id=slot_id, section=section,
                expected_disposition=expected_str, expected_value=expected.value,
                actual_status=actual_status, actual_value=actual_value,
                score=1 if ok else 0,
                reason="numeric match" if ok else f"numeric mismatch: expected {expected.value!r}, got {actual_value!r}",
            )

        # Enum / exact: normalize to lowercase string for comparison.
        ok = _exact_match(expected.value, actual_value)
        return SlotScore(
            slot_id=slot_id, section=section,
            expected_disposition=expected_str, expected_value=expected.value,
            actual_status=actual_status, actual_value=actual_value,
            score=1 if ok else 0,
            reason="exact match" if ok else f"value mismatch: expected {expected.value!r}, got {actual_value!r}",
        )

    # --- expected: skipped (should not reach here; filtered from denominator) ---
    return SlotScore(
        slot_id=slot_id, section=section,
        expected_disposition="skipped", expected_value=None,
        actual_status=actual_status, actual_value=actual_value,
        score=1, reason="skipped (not in denominator)",
    )


def _numeric_match(expected: Any, actual: Any) -> bool:
    try:
        return abs(float(expected) - float(actual)) < 1e-9
    except (TypeError, ValueError):
        return False


def _exact_match(expected: Any, actual: Any) -> bool:
    if expected is None and actual is None:
        return True
    if isinstance(expected, list) and isinstance(actual, list):
        return sorted(str(x).lower() for x in expected) == sorted(str(x).lower() for x in actual)
    return str(expected).lower().strip() == str(actual).lower().strip()


# ---------------------------------------------------------------------------
# Profile-level scoring
# ---------------------------------------------------------------------------


def score_profile(
    state: ProfileState,
    answer_key: AnswerKey,
    sections: list[str],
    *,
    schema_path: str | Path,
    system_id: str,
    human_ratings: dict[str, int] | None = None,
) -> ProfileScore:
    """Score a completed system run against the answer key.

    The denominator is the intersection of:
      - Slots resolved as in-scope by ``resolve_inscope_slots`` (public schema +
        profile facts) — ensures the resolver and scorer use identical logic.
      - Slots in the answer key whose expected disposition is not ``skipped`` or
        ``conditional``.

    This double-check catches the R-5 risk: an in-scope slot absent from the
    answer key, or a slot in the answer key that the resolver doesn't consider
    in-scope, should both surface as a misalignment.

    Args:
        state:       Final ProfileState from the system run.
        answer_key:  Answer key for this profile.
        sections:    The sections to score (e.g. all H1 sections).
        schema_path: Path to the schema file (must match the frozen manifest).
        system_id:   "agent" | "tree" (recorded in the ProfileScore).
        human_ratings:
            Adjudicated free-text scores (slot_id -> 0/1) from the FR-35 blind-rater
            protocol (``scoring.rater_queue``). When provided, a free-text slot's
            provisional pass is replaced by its adjudicated score and the slot is
            removed from ``human_rating_pending``. Slots absent here remain pending
            (scored 1 provisionally) — never fabricated.
    Returns:
        A ``ProfileScore`` with SAR, slot-level scores, and human-rating flags.
    """
    human_ratings = human_ratings or {}
    profile_facts = state.recorded_facts()
    in_scope = resolve_inscope_slots(profile_facts, sections, schema_path=schema_path)
    in_scope_ids = {r.slot_id: r for r in in_scope}

    denominator_answer_key = answer_key.denominator_slots()
    # Score only slots that are both in-scope AND in the answer key denominator.
    denominator_ids = in_scope_ids.keys() & denominator_answer_key.keys()

    slot_scores: list[SlotScore] = []
    human_rating_pending: list[str] = []
    skipped: list[str] = [
        sid for sid, disp in answer_key.slots.items()
        if disp.disposition in ("skipped", "conditional")
    ]

    for slot_id in sorted(denominator_ids):
        expected = denominator_answer_key[slot_id]
        resolved = in_scope_ids[slot_id]
        ss = score_slot(slot_id, resolved.section, expected, state)
        if ss.requires_human_rating and slot_id in human_ratings:
            # Adjudicated: replace the provisional pass with the rated score and
            # treat the slot as resolved (no longer pending).
            ss.score = int(human_ratings[slot_id])
            ss.requires_human_rating = False
            ss.reason = f"free-text adjudicated by blind raters → {ss.score}"
        slot_scores.append(ss)
        if ss.requires_human_rating:
            human_rating_pending.append(slot_id)

    numerator = sum(ss.score for ss in slot_scores if not ss.requires_human_rating)
    # Still-pending human-rated slots contribute 1 (provisionally) until adjudicated.
    numerator += len(human_rating_pending)
    denominator = len(slot_scores)
    sar = numerator / denominator if denominator > 0 else 0.0

    return ProfileScore(
        profile_id=answer_key.profile_id,
        group=answer_key.group,
        system_id=system_id,
        sar=sar,
        numerator=numerator,
        denominator=denominator,
        slot_scores=slot_scores,
        skipped_slots=skipped,
        human_rating_pending=human_rating_pending,
    )


# ---------------------------------------------------------------------------
# Cascade / sensitivity band (§6.5)
# ---------------------------------------------------------------------------


def cascade_tag(
    state: ProfileState,
    answer_key: AnswerKey,
    sections: list[str],
    *,
    schema_path: str | Path,
    contested_slots: list[str],
    system_id: str,
) -> CascadeResult:
    """Compute the SAR sensitivity band for contested slots (§6.5 / R-6).

    For each contested slot, we re-resolve the in-scope denominator under:
      BEST  → assume the contested root was handled correctly (max denominator).
      WORST → assume the contested root was not handled (min denominator).
      NEUTRAL → the adjudicated nominal answer key (normal scoring).

    ``contested_slots`` are the slot IDs whose ground-truth disposition could not
    be agreed upon by the primary reviewers and have been sent to a tie-breaker.
    While awaiting the tie-breaker, they are treated as "absent" from facts for
    re-resolution purposes.

    Args:
        state:            Final ProfileState from the system run.
        answer_key:       Answer key (with adjudicated values where available).
        sections:         Sections to score.
        schema_path:      Path to the schema file.
        contested_slots:  Slot IDs with undecided ground truth.
        system_id:        "agent" | "tree".
    Returns:
        A ``CascadeResult`` with sar_nominal, sar_best, sar_worst, and denominator sizes.
    """
    nominal = score_profile(
        state, answer_key, sections, schema_path=schema_path, system_id=system_id
    )

    # Remove contested roots from facts for re-resolution.
    facts = state.recorded_facts()
    facts_without_contested = {k: v for k, v in facts.items() if k not in contested_slots}

    best_in_scope = resolve_inscope_slots(
        facts_without_contested, sections,
        schema_path=schema_path, adjudication=AdjudicationChoice.BEST
    )
    worst_in_scope = resolve_inscope_slots(
        facts_without_contested, sections,
        schema_path=schema_path, adjudication=AdjudicationChoice.WORST
    )

    best_denom = len({r.slot_id for r in best_in_scope} & answer_key.denominator_slots().keys())
    worst_denom = len({r.slot_id for r in worst_in_scope} & answer_key.denominator_slots().keys())

    # SAR numerator stays fixed (slots scored correctly do not change);
    # only the denominator changes between BEST and WORST.
    num = nominal.numerator
    sar_best = num / best_denom if best_denom > 0 else 0.0
    sar_worst = num / worst_denom if worst_denom > 0 else 0.0

    return CascadeResult(
        profile_id=answer_key.profile_id,
        contested_slots=list(contested_slots),
        sar_nominal=nominal.sar,
        sar_best=sar_best,
        sar_worst=sar_worst,
        denominator_nominal=nominal.denominator,
        denominator_best=best_denom,
        denominator_worst=worst_denom,
    )
