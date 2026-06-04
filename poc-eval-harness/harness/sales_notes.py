"""Load Salesforce handover-note exports for the stakeholder demo.

The Tamar export is a filtered Opportunities report: header row contains
Account Name, Number of Listings, Opportunity Name, Notes (often truncated at 255 chars).
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

import pandas as pd


@dataclass(frozen=True)
class SalesAccount:
    account_name: str
    listing_count: int | None
    opportunity_name: str
    opportunity_owner: str
    notes: str


_HEADER_ROW = 13
_EXPECTED_COLUMNS = (
    "opportunity_owner",
    "account_name",
    "listing_count",
    "opportunity_name",
    "notes",
)


def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    rename = {
        df.columns[1]: "opportunity_owner",
        df.columns[3]: "account_name",
        df.columns[4]: "listing_count",
        df.columns[5]: "opportunity_name",
        df.columns[6]: "notes",
    }
    out = df.rename(columns=rename)[list(_EXPECTED_COLUMNS)]
    return out.dropna(subset=["account_name"])


def load_sales_accounts(path: str | Path) -> list[SalesAccount]:
    """Parse the Salesforce 'Notes for Tamar' style export."""
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"sales notes workbook not found: {path}")

    raw = pd.read_excel(path, sheet_name=0, header=_HEADER_ROW)
    frame = _normalize_columns(raw)

    accounts: list[SalesAccount] = []
    for row in frame.itertuples(index=False):
        listing: int | None
        try:
            listing = int(row.listing_count) if pd.notna(row.listing_count) else None
        except (TypeError, ValueError):
            listing = None

        notes = "" if pd.isna(row.notes) else str(row.notes).strip()
        accounts.append(
            SalesAccount(
                account_name=str(row.account_name).strip(),
                listing_count=listing,
                opportunity_name="" if pd.isna(row.opportunity_name) else str(row.opportunity_name).strip(),
                opportunity_owner="" if pd.isna(row.opportunity_owner) else str(row.opportunity_owner).strip(),
                notes=notes,
            )
        )
    return accounts


@lru_cache(maxsize=4)
def _cached_accounts(path: str) -> tuple[SalesAccount, ...]:
    return tuple(load_sales_accounts(path))


def list_account_names(path: str | Path) -> list[str]:
    return sorted({a.account_name for a in _cached_accounts(str(path))})


def get_account(path: str | Path, account_name: str) -> SalesAccount | None:
    key = account_name.strip().casefold()
    for account in _cached_accounts(str(path)):
        if account.account_name.casefold() == key:
            return account
    return None


def search_accounts(path: str | Path, query: str, *, limit: int = 25) -> list[SalesAccount]:
    q = query.strip().casefold()
    if not q:
        return list(_cached_accounts(str(path)))[:limit]

    hits: list[SalesAccount] = []
    for account in _cached_accounts(str(path)):
        hay = " ".join(
            (account.account_name, account.opportunity_name, account.notes[:200])
        ).casefold()
        if q in hay:
            hits.append(account)
        if len(hits) >= limit:
            break
    return hits


def resolve_notes_path(explicit: str | Path | None = None) -> Path | None:
    """Find the Tamar sales-notes workbook (env, explicit path, or auto-detect)."""
    candidates: list[Path] = []

    if explicit is not None and str(explicit).strip():
        candidates.append(Path(explicit).expanduser())

    import os

    env = os.environ.get("SALES_NOTES_XLSX", "").strip()
    if env:
        candidates.append(Path(env).expanduser())

    downloads = Path.home() / "Downloads"
    if downloads.is_dir():
        candidates.extend(
            sorted(
                downloads.glob("Notes for Tamar*.xlsx"),
                key=lambda p: p.stat().st_mtime,
                reverse=True,
            )
        )

    data_dir = Path(__file__).resolve().parent.parent / "data"
    if data_dir.is_dir():
        candidates.extend(sorted(data_dir.glob("*.xlsx"), key=lambda p: p.stat().st_mtime, reverse=True))

    seen: set[str] = set()
    for path in candidates:
        key = str(path.resolve())
        if key in seen:
            continue
        seen.add(key)
        if path.is_file():
            return path
    return None
