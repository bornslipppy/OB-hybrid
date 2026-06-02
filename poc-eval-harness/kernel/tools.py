"""The 7-tool contract (FR-2 / FR-13b).

The seven tools are the *only* path into ``ProfileState``. Both systems under test
(agent and tree) emit exactly these models; free-writes are structurally impossible
because there is no other mutation channel (architecture §3.1).

The same Pydantic models serve three roles:
  1. validate the agent's LLM tool-use blocks,
  2. validate the tree's direct calls,
  3. export JSON Schema for the agent's LLM tool definitions (``to_anthropic_tools``).
"""

from __future__ import annotations

from enum import Enum
from typing import Annotated, Any, Literal, Union

from pydantic import BaseModel, Field, model_validator


class Source(str, Enum):
    """Provenance of a recorded value (schema §1 source-precedence ladder)."""

    USER_STATED = "user_stated"
    SF_PREFILL = "sf_prefill"
    AI_EXTRACTED_FROM_NOTE = "ai_extracted_from_note"
    INFERRED = "inferred"
    HARDCODED_STARTER = "hardcoded_starter"


# --- The seven tools ---------------------------------------------------------


class RecordAnswer(BaseModel):
    """Record a scalar/enum/bool slot (schema §5)."""

    tool: Literal["record_answer"] = "record_answer"
    field_id: str
    value: Any
    source: Source


class AddFee(BaseModel):
    """Append one mandatory fee — ``mandatory_fees[]`` item_shape (schema S4)."""

    tool: Literal["add_fee"] = "add_fee"
    fee_type: str
    amount: float
    unit: Literal["flat", "percent"]


class AddTax(BaseModel):
    """Append one tax — ``taxes[]`` item_shape (schema S4).

    ``tax_type`` is intentionally a free ``str``, not a hard enum: G3 casing is
    provisional (OPEN-3 / R-12), so the value is carried verbatim and compared on
    a case/whitespace-normalized basis at scoring time rather than rejected here.
    """

    tool: Literal["add_tax"] = "add_tax"
    tax_type: str
    tax_type_other: str | None = None
    inclusivity: Literal["inclusive", "exclusive"]
    what_taxed: list[Literal["accommodation_fare", "cleaning_fee", "additional_fees"]]
    scope: Literal["listing", "account_wide"]


class AddOwner(BaseModel):
    """Append one owner record — S8 hero-branch ``owners[]`` item_shape.

    The per-owner economics sub-fields carry their own ``depends_on`` guards in the
    schema. They are enforced structurally here (see ``_enforce_depends_on``): an
    economics field that does not match ``management_model`` is a malformed write
    and is rejected, so the composite tool cannot smuggle a free-write past FR-2.

    ``who_pays_channel_commission`` is the *Channel Commission* (OTA fee) concept —
    distinct from ``pmc_commission_rate`` (PMC management commission) — and is
    therefore independent of ``management_model``.
    """

    tool: Literal["add_owner"] = "add_owner"
    owner_name: str
    email: str
    listings: list[str]
    ownership_share: float | None = None
    management_model: Literal["commission", "fixed_fee", "revenue_split", "other"]
    pmc_commission_rate: float | None = None
    fixed_fee_amount: float | None = None
    split_terms: str | None = None
    who_pays_channel_commission: Literal["owner", "pmc", "split"] | None = None

    @model_validator(mode="after")
    def _enforce_depends_on(self) -> "AddOwner":
        mm = self.management_model
        # Map each economics sub-field to the management_model(s) under which it is
        # in scope per the schema item_shape depends_on guards.
        allowed = {
            "pmc_commission_rate": {"commission"},
            "fixed_fee_amount": {"fixed_fee"},
            "split_terms": {"revenue_split", "other"},
        }
        for field_name, models in allowed.items():
            if getattr(self, field_name) is not None and mm not in models:
                raise ValueError(
                    f"{field_name} is only valid when management_model in {sorted(models)}; "
                    f"got management_model={mm!r}"
                )
        return self


class SkipQuestion(BaseModel):
    """Defer a field — sets status ``skipped`` (schema §5)."""

    tool: Literal["skip_question"] = "skip_question"
    field_id: str
    reason: str


class FlagForCall1(BaseModel):
    """Hand off to the human onboarder — sets a slot ``flagged`` (schema §5).

    ``field_id`` is an additive refinement of the §10.2 stub (flagged for DRI
    ratification before kernel freeze): the §3.2 ``end_section`` guard requires a
    flag to be addressable to a slot so a flagged slot counts as dispositioned.
    When ``field_id`` is ``None`` the flag is a brief-only / topic-level flag
    (e.g. ``customer_sentiment`` / ``risk_flags``, which never gate the flow and
    never disposition a frame slot).
    """

    tool: Literal["flag_for_call_1"] = "flag_for_call_1"
    topic: str
    user_quote: str
    note: str
    field_id: str | None = None


class EndSection(BaseModel):
    """Close a section — section transition (schema §5).

    The reducer rejects this while any reachable in-scope slot in the section is
    undispositioned or any echo awaits confirmation (architecture §3.2).
    """

    tool: Literal["end_section"] = "end_section"
    section_id: str


# Discriminated union: the ``tool`` literal selects the model, so an LLM/tree
# payload validates to exactly one type with no ambiguity.
ToolCall = Annotated[
    Union[
        RecordAnswer,
        AddFee,
        AddTax,
        AddOwner,
        SkipQuestion,
        FlagForCall1,
        EndSection,
    ],
    Field(discriminator="tool"),
]

# Ordered registry — single source of truth for names → models.
TOOL_MODELS: tuple[type[BaseModel], ...] = (
    RecordAnswer,
    AddFee,
    AddTax,
    AddOwner,
    SkipQuestion,
    FlagForCall1,
    EndSection,
)

TOOL_NAMES: tuple[str, ...] = (
    "record_answer",
    "add_fee",
    "add_tax",
    "add_owner",
    "skip_question",
    "flag_for_call_1",
    "end_section",
)

_NAME_TO_MODEL: dict[str, type[BaseModel]] = {
    name: model for name, model in zip(TOOL_NAMES, TOOL_MODELS)
}


def parse_tool_call(name: str, args: dict[str, Any]) -> BaseModel:
    """Validate a raw (name, args) pair from an LLM tool_use block into a ToolCall.

    Raises ``KeyError`` for an unknown tool name and ``pydantic.ValidationError``
    for malformed arguments — there is no permissive fallback.
    """
    model = _NAME_TO_MODEL[name]
    return model.model_validate({**args, "tool": name})


def to_openai_tools() -> list[dict[str, Any]]:
    """Export the 7 tools as OpenAI function-calling tool definitions.

    Each entry is ``{"type": "function", "function": {"name", "description", "parameters"}}``
    where ``parameters`` is the model's JSON Schema with the internal ``tool`` discriminator
    removed (the API supplies the name out-of-band via the function wrapper).
    Used by the Cursor-API agent (scored_completion / glue_completion).
    """
    defs: list[dict[str, Any]] = []
    for name, model in zip(TOOL_NAMES, TOOL_MODELS):
        schema = model.model_json_schema()
        schema.get("properties", {}).pop("tool", None)
        if "required" in schema:
            schema["required"] = [r for r in schema["required"] if r != "tool"]
        defs.append(
            {
                "type": "function",
                "function": {
                    "name": name,
                    "description": (model.__doc__ or "").strip().split("\n")[0],
                    "parameters": schema,
                },
            }
        )
    return defs


def to_anthropic_tools() -> list[dict[str, Any]]:
    """Export the 7 tools as Anthropic tool definitions.

    Retained for interoperability. Prefer ``to_openai_tools()`` for the Cursor-API agent.
    Each entry is ``{"name", "description", "input_schema"}`` where ``input_schema``
    is the model's JSON Schema with the internal ``tool`` discriminator removed.
    """
    defs: list[dict[str, Any]] = []
    for name, model in zip(TOOL_NAMES, TOOL_MODELS):
        schema = model.model_json_schema()
        schema.get("properties", {}).pop("tool", None)
        if "required" in schema:
            schema["required"] = [r for r in schema["required"] if r != "tool"]
        defs.append(
            {
                "name": name,
                "description": (model.__doc__ or "").strip().split("\n")[0],
                "input_schema": schema,
            }
        )
    return defs
