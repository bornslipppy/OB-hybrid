"""Story 4.6 — false-write detection on composite tools (FR-24 / EC-12 / R-10).

Fixtures-first: these hand-computed traces are the acceptance gate for
``scoring.metrics.false_write_rate`` — the last high-risk pure function (§13).

The §3 definition (architecture §3.3): a ``tool_call`` on an ``echo_before_write``
field is a *false write* when an echo-required sub-field it writes has **no prior
``user_confirmed``** since that sub-field's value was last introduced/corrected.
For composite tools (``add_owner``, ``add_fee``, ``add_tax``) the check is applied
**per echo-required sub-field** (EC-12). Non-echo sub-fields (``owner_name``,
``email``, ``management_model``, …) are never false writes.

Trace contract these fixtures rely on (the producer — runner/system — emits):
  * ``value_introduced``  slot + (subfield for composite economics) when a value enters.
  * ``echo_issued``       when the system echoes that value for confirmation.
  * ``user_confirmed``    when the user confirms that (slot, subfield).
  * ``user_corrected``    re-opens the echo (a new value needs new confirmation).
  * ``tool_call``         the write; args carry the sub-field values directly.
For composite economics the (slot, subfield) is ("owners", "pmc_commission_rate")
etc.; for a scalar echo field it is (field_id, None).
"""

from __future__ import annotations

from kernel.trace import (
    EchoIssued,
    ToolCallEvent,
    UserConfirmed,
    UserCorrected,
    ValueIntroduced,
)
from scoring.metrics import FalseWriteResult, false_write_rate


# ---------------------------------------------------------------------------
# Trace builders — keep the fixtures readable and intent-revealing.
# ---------------------------------------------------------------------------


def _introduce(turn, slot, value, subfield=None):
    return ValueIntroduced(turn=turn, slot=slot, subfield=subfield, value=value)


def _echo(turn, slot, value, subfield=None):
    return EchoIssued(turn=turn, slot=slot, subfield=subfield, value=value)


def _confirm(turn, slot, subfield=None):
    return UserConfirmed(turn=turn, slot=slot, subfield=subfield)


def _correct(turn, slot, subfield=None, value=None):
    return UserCorrected(turn=turn, slot=slot, subfield=subfield, corrected_value=value)


def _add_owner(turn, **args):
    base = {
        "owner_name": "Acme PM",
        "email": "owner@example.com",
        "listings": ["L1"],
        "management_model": "commission",
    }
    base.update(args)
    return ToolCallEvent(turn=turn, tool="add_owner", args=base)


# ---------------------------------------------------------------------------
# The three required fixtures (per the build prompt).
# ---------------------------------------------------------------------------


class TestRequiredFixtures:
    def test_composite_all_subfields_confirmed_is_correct(self):
        """add_owner where every echo-required sub-field was confirmed → NO false write."""
        trace = [
            _introduce(1, "owners", 100.0, subfield="ownership_share"),
            _introduce(1, "owners", 15.0, subfield="pmc_commission_rate"),
            _echo(2, "owners", 100.0, subfield="ownership_share"),
            _echo(2, "owners", 15.0, subfield="pmc_commission_rate"),
            _confirm(3, "owners", subfield="ownership_share"),
            _confirm(3, "owners", subfield="pmc_commission_rate"),
            _add_owner(4, ownership_share=100.0, pmc_commission_rate=15.0),
        ]
        result = false_write_rate(trace)
        assert isinstance(result, FalseWriteResult)
        assert result.total_echo_writes == 2  # ownership_share + pmc_commission_rate
        assert result.false_writes == 0
        assert result.rate == 0.0
        assert result.is_clean is True
        assert result.detections == []

    def test_composite_subfield_introduced_but_not_confirmed_is_false_write(self):
        """A sub-field introduced but never confirmed before the write → false write (per sub-field)."""
        trace = [
            _introduce(1, "owners", 100.0, subfield="ownership_share"),
            _introduce(1, "owners", 15.0, subfield="pmc_commission_rate"),
            _echo(2, "owners", 100.0, subfield="ownership_share"),
            _echo(2, "owners", 15.0, subfield="pmc_commission_rate"),
            _confirm(3, "owners", subfield="ownership_share"),
            # pmc_commission_rate NEVER confirmed
            _add_owner(4, ownership_share=100.0, pmc_commission_rate=15.0),
        ]
        result = false_write_rate(trace)
        assert result.total_echo_writes == 2
        assert result.false_writes == 1
        assert result.rate == 0.5
        assert result.is_clean is False
        det = result.detections
        assert len(det) == 1
        assert det[0].slot == "owners"
        assert det[0].subfield == "pmc_commission_rate"
        assert det[0].turn == 4
        assert det[0].tool == "add_owner"

    def test_non_echo_subfield_is_never_a_false_write(self):
        """A non-echo sub-field (owner_name) unconfirmed is irrelevant; economics confirmed → clean."""
        trace = [
            _introduce(1, "owners", "Acme PM", subfield="owner_name"),  # non-echo, no confirm
            _introduce(1, "owners", 15.0, subfield="pmc_commission_rate"),
            _confirm(2, "owners", subfield="pmc_commission_rate"),
            _add_owner(3, pmc_commission_rate=15.0),
        ]
        result = false_write_rate(trace)
        # Only pmc_commission_rate is echo-required; owner_name is ignored entirely.
        assert result.total_echo_writes == 1
        assert result.false_writes == 0
        assert result.rate == 0.0
        assert result.is_clean is True


# ---------------------------------------------------------------------------
# Scalar echo field (record_answer on security_deposit_amount).
# ---------------------------------------------------------------------------


class TestScalarEchoField:
    def test_scalar_confirmed_is_clean(self):
        trace = [
            _introduce(1, "security_deposit_amount", 250.0),
            _echo(2, "security_deposit_amount", 250.0),
            _confirm(3, "security_deposit_amount"),
            ToolCallEvent(
                turn=4,
                tool="record_answer",
                args={"field_id": "security_deposit_amount", "value": 250.0, "source": "user_stated"},
            ),
        ]
        result = false_write_rate(trace)
        assert result.total_echo_writes == 1
        assert result.is_clean is True

    def test_scalar_written_without_confirmation_is_false_write(self):
        trace = [
            _introduce(1, "security_deposit_amount", 250.0),
            ToolCallEvent(
                turn=2,
                tool="record_answer",
                args={"field_id": "security_deposit_amount", "value": 250.0, "source": "user_stated"},
            ),
        ]
        result = false_write_rate(trace)
        assert result.false_writes == 1
        assert result.detections[0].slot == "security_deposit_amount"
        assert result.detections[0].subfield is None

    def test_non_echo_scalar_never_counts(self):
        """record_answer on a non-echo field (listing_count) is never an echo write."""
        trace = [
            _introduce(1, "listing_count", 5),
            ToolCallEvent(
                turn=2,
                tool="record_answer",
                args={"field_id": "listing_count", "value": 5, "source": "user_stated"},
            ),
        ]
        result = false_write_rate(trace)
        assert result.total_echo_writes == 0
        assert result.false_writes == 0
        assert result.rate == 0.0


# ---------------------------------------------------------------------------
# Worst case + correction re-open + add_fee / add_tax.
# ---------------------------------------------------------------------------


class TestEdgeCases:
    def test_write_with_no_introduce_no_confirm_is_false_write(self):
        """Worst case: economics value written with no echo lifecycle at all."""
        trace = [_add_owner(1, fixed_fee_amount=500.0, management_model="fixed_fee")]
        result = false_write_rate(trace)
        assert result.total_echo_writes == 1
        assert result.false_writes == 1
        assert result.detections[0].subfield == "fixed_fee_amount"

    def test_correction_reopens_confirmation(self):
        """user_corrected after confirm re-opens the echo; writing without re-confirm is a false write."""
        trace = [
            _introduce(1, "owners", 15.0, subfield="pmc_commission_rate"),
            _confirm(2, "owners", subfield="pmc_commission_rate"),
            _correct(3, "owners", subfield="pmc_commission_rate", value=12.0),  # re-opens
            _add_owner(4, pmc_commission_rate=12.0),
        ]
        result = false_write_rate(trace)
        assert result.false_writes == 1

    def test_correction_then_reconfirm_is_clean(self):
        trace = [
            _introduce(1, "owners", 15.0, subfield="pmc_commission_rate"),
            _confirm(2, "owners", subfield="pmc_commission_rate"),
            _correct(3, "owners", subfield="pmc_commission_rate", value=12.0),
            _confirm(4, "owners", subfield="pmc_commission_rate"),
            _add_owner(5, pmc_commission_rate=12.0),
        ]
        result = false_write_rate(trace)
        assert result.is_clean is True

    def test_add_fee_amount_requires_confirmation(self):
        bad = [
            _introduce(1, "mandatory_fees", 30.0, subfield="amount"),
            ToolCallEvent(turn=2, tool="add_fee", args={"fee_type": "resort", "amount": 30.0, "unit": "flat"}),
        ]
        good = [
            _introduce(1, "mandatory_fees", 30.0, subfield="amount"),
            _confirm(2, "mandatory_fees", subfield="amount"),
            ToolCallEvent(turn=3, tool="add_fee", args={"fee_type": "resort", "amount": 30.0, "unit": "flat"}),
        ]
        assert false_write_rate(bad).false_writes == 1
        assert false_write_rate(good).is_clean is True

    def test_add_tax_whole_record_requires_confirmation(self):
        bad = [
            _introduce(1, "taxes", "occupancy 6%"),
            ToolCallEvent(
                turn=2, tool="add_tax",
                args={"tax_type": "occupancy_tourist", "inclusivity": "exclusive",
                      "what_taxed": ["accommodation_fare"], "scope": "listing"},
            ),
        ]
        good = [
            _introduce(1, "taxes", "occupancy 6%"),
            _confirm(2, "taxes"),
            ToolCallEvent(
                turn=3, tool="add_tax",
                args={"tax_type": "occupancy_tourist", "inclusivity": "exclusive",
                      "what_taxed": ["accommodation_fare"], "scope": "listing"},
            ),
        ]
        assert false_write_rate(bad).false_writes == 1
        assert false_write_rate(good).is_clean is True

    def test_empty_trace_is_clean(self):
        result = false_write_rate([])
        assert result.total_echo_writes == 0
        assert result.rate == 0.0
        assert result.is_clean is True
