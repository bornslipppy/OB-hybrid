"""User simulator — Story 4.1 (faithful + leak-free) and Story 4.2 (decorrelated).

Two modes:
  SCRIPTED — Group A profiles: slot-keyed canned replies loaded from
             ``scripted_turns/group_a.yaml``. Deterministic; no LLM call.
  LLM      — Group B/C profiles: OpenAI ``simulator_completion()``
             (decorrelated from the Anthropic agent — FR-21).

Fairness invariant (FR-19/FR-20):
  The ``UserSimulator`` constructor takes a ``RespondentSpec`` (facts + persona)
  **not** an answer key. The answer key is never passed to this module —
  verifiable from the call signature. ``reply()`` additionally asserts that no
  answer-key field is present in the spec it received.
"""

from __future__ import annotations

import re
import textwrap
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

import yaml

from kernel.protocol import UserQuestion

_SCRIPTED_TURNS_DIR = Path(__file__).parent / "scripted_turns"


# ---------------------------------------------------------------------------
# RespondentSpec — no answer key
# ---------------------------------------------------------------------------


@dataclass
class RespondentSpec:
    """Everything the simulator is *allowed* to know about a respondent.

    Fields:
        profile_id:    Unique profile identifier (e.g. "A1", "B2", "C1").
        group:         "A" | "B" | "C"  (used to select simulator mode).
        facts:         Ground-truth business facts (slot_id -> value).
        persona:       Short natural-language directive for the LLM simulator.
        conversation_notes: Optional free-text tone notes (e.g. "pushes back
                       on financial questions").
        variant_overrides: For Group A, overrides that differ from the base
                       scripted turns (e.g. A2-specific replies keyed by slot_id).
    """

    profile_id: str
    group: str  # "A" | "B" | "C"
    facts: dict[str, Any]
    persona: str = ""
    conversation_notes: str = ""
    variant_overrides: dict[str, str | None] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _FORBIDDEN_KEYS = {"answer_key", "dispositions", "expected_dispositions", "key"}
        intersection = _FORBIDDEN_KEYS & set(self.facts.keys())
        if intersection:
            raise ValueError(
                f"RespondentSpec.facts must not contain answer-key fields: {intersection}"
            )


# ---------------------------------------------------------------------------
# SimulatorMode
# ---------------------------------------------------------------------------


class SimulatorMode(str, Enum):
    SCRIPTED = "scripted"  # Group A — deterministic canned turns
    LLM = "llm"  # Group B/C — OpenAI (decorrelated from Anthropic agent)


# ---------------------------------------------------------------------------
# UserSimulator
# ---------------------------------------------------------------------------


class UserSimulator:
    """Stateful user simulator for the eval harness.

    Args:
        spec:          The respondent spec (facts + persona, NO answer key).
        openai_client: Required for LLM mode; ignored for scripted mode.
        mode:          Override the auto-detected mode (useful in tests).
        model:         OpenAI model name for LLM mode.
        seed:          Best-effort seed for OpenAI reproducibility.
    """

    def __init__(
        self,
        spec: RespondentSpec,
        *,
        openai_client: Any | None = None,
        mode: SimulatorMode | None = None,
        model: str = "gpt-4o",
        seed: int | None = None,
    ) -> None:
        self._spec = spec
        self._client = openai_client
        self._model = model
        self._seed = seed
        self._history: list[dict[str, str]] = []

        if mode is not None:
            self._mode = mode
        elif spec.group == "A":
            self._mode = SimulatorMode.SCRIPTED
        else:
            self._mode = SimulatorMode.LLM

        if self._mode is SimulatorMode.LLM and openai_client is None:
            raise ValueError(
                "UserSimulator in LLM mode requires an openai_client. "
                "Pass one or override with mode=SimulatorMode.SCRIPTED for testing."
            )

        # Load scripted turns (always, so tests can verify the map).
        self._scripted: dict[str, str | None] = self._load_scripted_turns()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    @property
    def mode(self) -> SimulatorMode:
        return self._mode

    @property
    def spec(self) -> RespondentSpec:
        return self._spec

    def reply(self, question: UserQuestion) -> str:
        """Return the simulator's natural-language reply to ``question``.

        The reply contains only facts from ``self._spec`` — never answer-key
        dispositions.  If asked about something absent from the spec, returns
        a context-appropriate "I don't know" variant.

        Args:
            question: A ``UserQuestion`` from the System (agent or tree).
        Returns:
            A natural-language reply string.
        """
        if self._mode is SimulatorMode.SCRIPTED:
            reply_text = self._scripted_reply(question)
        else:
            reply_text = self._llm_reply(question)

        # Track turn history for LLM mode (scripted ignores history).
        self._history.append({"role": "user", "content": question.text})
        self._history.append({"role": "assistant", "content": reply_text})
        return reply_text

    def reset(self) -> None:
        """Clear conversation history (use between runs)."""
        self._history = []

    # ------------------------------------------------------------------
    # Scripted path
    # ------------------------------------------------------------------

    def _scripted_reply(self, question: UserQuestion) -> str:
        """Look up the canned reply by ``primary_slot``.

        Selection order:
          1. variant_overrides[primary_slot]  (profile-specific override)
          2. base scripted turns[primary_slot]
          3. "unknown_slot" fallback
        """
        slot = question.primary_slot

        # Check variant overrides first (e.g. A2 differences from base).
        if slot and slot in self._spec.variant_overrides:
            val = self._spec.variant_overrides[slot]
            if val is not None:
                return str(val).strip()
            # None override → slot not applicable for this profile.
            return self._not_applicable_reply(slot)

        if slot and slot in self._scripted:
            val = self._scripted[slot]
            if val is not None:
                return str(val).strip()
            return self._not_applicable_reply(slot)

        # No primary_slot hint or no scripted entry → generic fallback.
        return str(self._scripted.get("unknown_slot", "I'm not sure about that one.")).strip()

    def _not_applicable_reply(self, slot: str) -> str:
        """Reply for a slot that is genuinely not applicable for this profile."""
        return f"That doesn't apply to my situation — I don't have that set up."

    # ------------------------------------------------------------------
    # LLM path (Group B/C)
    # ------------------------------------------------------------------

    def _llm_reply(self, question: UserQuestion) -> str:
        from kernel.llm import simulator_completion

        system_prompt = self._build_system_prompt()
        messages = list(self._history) + [{"role": "user", "content": question.text}]
        return simulator_completion(
            messages,
            system_prompt,
            _client=self._client,
            _model=self._model,
            seed=self._seed,
        )

    def _build_system_prompt(self) -> str:
        """Build the LLM simulator system prompt from the respondent spec.

        Critically: only ``facts`` and ``persona`` are included — never
        ``answer_key`` or ``variant_overrides``.
        """
        facts_block = "\n".join(
            f"  {k}: {v}" for k, v in self._spec.facts.items() if v is not None
        )
        notes = self._spec.conversation_notes.strip()
        notes_block = f"\nConversation notes: {notes}" if notes else ""

        return textwrap.dedent(f"""\
            You are a real vacation-rental operator participating in a product onboarding interview.
            You answer ONLY from the facts below — you do NOT invent facts absent from this list.
            If asked about something not listed, say "I don't know" or "That doesn't apply to me."
            Do not volunteer information that hasn't been asked.
            Do not ask questions back.
            Keep replies concise (1–3 sentences).

            Persona: {self._spec.persona or "Cooperative, organized, answers directly."}
            {notes_block}

            Your facts:
            {facts_block}
        """)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _load_scripted_turns() -> dict[str, str | None]:
        """Load the base Group A scripted turns from group_a.yaml.

        Returns a flat dict: slot_id -> reply text (or None if not applicable).
        The ``a2_overrides`` sub-key is NOT flattened here — it is used by
        ``variant_overrides`` in the A2 RespondentSpec instead.
        """
        path = _SCRIPTED_TURNS_DIR / "group-a.yaml"
        if not path.exists():
            return {}
        raw: dict[str, Any] = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        # Exclude the a2_overrides sub-dict — those are loaded externally.
        return {k: v for k, v in raw.items() if k != "a2_overrides" and not isinstance(v, dict)}
