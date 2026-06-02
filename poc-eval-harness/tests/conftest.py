"""Shared test fixtures and paths for the kernel test suite."""

from __future__ import annotations

from pathlib import Path

import pytest

from kernel.schema import SchemaLoader, SlotDef

# The frozen schema copy lives inside the harness (manifest input, §5.2).
SCHEMA_PATH = Path(__file__).resolve().parents[1] / "schema" / "guesty-pro-account-creation-schema.md"


@pytest.fixture(scope="session")
def schema_slots() -> list[SlotDef]:
    return SchemaLoader().load(SCHEMA_PATH)
