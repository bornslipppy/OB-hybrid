"""Generate a fully synthetic sales-notes workbook for the demo.

The real Tamar export contains PII (handover notes with names, emails, free
text) and must never be shared or hosted. This builds a drop-in replacement
with the SAME shape `harness.sales_notes` expects — header on row 13, the
account/owner/listings/opportunity/notes columns at positions 1/3/4/5/6 — but
every account, contact, and note here is invented. Nothing maps to a real
customer.

The notes are written to exercise the deterministic extractors in
`harness.account_context` (migration source, add-on intent, focus topics,
go-live, prior-PMS, third-party tools, country hints, defer-financials), so
the hosted demo shows varied, realistic context without any private data.

    uv run python onboarding_demo/make_sample_data.py
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

# Header labels mirror the Salesforce export. Only positions 1, 3, 4, 5, 6 are
# read by the loader; columns 0 and 2 are filler to match the real layout.
_COLUMNS = [
    "Opportunity ID",
    "Opportunity Owner",
    "Stage",
    "Account Name",
    "Number of Listings",
    "Opportunity Name",
    "Notes",
]

# (owner, account, listings, opportunity, note) — all invented.
_ROWS = [
    (
        "OPP-1001", "Amanda", "Closed Won", "Sunset Coast Rentals", 24,
        "Sunset Coast - Onboarding",
        "Primary contact: Marcus. Coming over from Hostaway, 24 active listings. "
        "Keen on GPO dynamic pricing and damage protection. Wants to focus on "
        "owner reporting and cleaner workflows. Already using PriceLabs and Turno. "
        "Looking to go live ASAP. Based in San Diego.",
    ),
    (
        "OPP-1002", "Jordan", "Closed Won", "Highland Stays Ltd", 12,
        "Highland Stays - Onboarding",
        "Primary contact: Priya. Currently on Lodgify, 12 listings in London, "
        "United Kingdom. First time really automating guest messaging. Interested "
        "in smart locks (RemoteLock) and premium channels. A bit nervous about tax "
        "and the financial setup, wants to defer that to later on call. Timeline is "
        "1-2 months.",
    ),
    (
        "OPP-1003", "Amanda", "Closed Won", "Blue Lizard Guesthouse", 6,
        "Blue Lizard - Onboarding",
        "Primary contact: Diego. New to PMS, managing 6 units on spreadsheets right "
        "now. Wants a direct booking website and better reviews. Go live in 2-4 "
        "weeks. Located in Barcelona, Spain, prefers Spanish.",
    ),
    (
        "OPP-1004", "Jordan", "Closed Won", "Pelican Bay Management", 40,
        "Pelican Bay - Onboarding",
        "Primary contact: Sarah. Migrating from Smoobu, 40 listings. Heavy on "
        "accounting, uses QuickBooks today. Wants help with pricing strategy and "
        "channel mix. Interested in the accounting add-on and the advanced bookings "
        "widget (ABW). Go live this week, fairly urgent.",
    ),
    (
        "OPP-1005", "Amanda", "Closed Won", "Mountain Echo Cabins", 9,
        "Mountain Echo - Onboarding",
        "Coming from Hostfully, 9 cabins. Wants owner statements and automated guest "
        "messaging templates. Interested in Guesty Pay and smart locks (Yale). "
        "Mostly happy with the plan, go live 1-2 months.",
    ),
    (
        "OPP-1006", "Jordan", "Closed Won", "Coastal Breeze Co", 15,
        "Coastal Breeze - Onboarding",
        "Primary contact: Leila. Currently using Uplisting for 15 properties in "
        "Sydney, Australia. Focus on reviews & reputation and pricing (PriceLabs "
        "already in place). Wants premium channels and damage protection. Just "
        "looking / exploring timing for now.",
    ),
]

_HEADER_STARTROW = 13  # loader reads the header from this 0-based row


def main() -> None:
    out_path = Path(__file__).resolve().parent / "sample-accounts.xlsx"
    frame = pd.DataFrame(_ROWS, columns=_COLUMNS)
    with pd.ExcelWriter(out_path, engine="openpyxl") as writer:
        # Leave the first 13 rows empty so the header lands on row index 13,
        # exactly where load_sales_accounts expects it.
        frame.to_excel(writer, sheet_name="Opportunities", index=False, startrow=_HEADER_STARTROW)
    print(f"wrote {len(_ROWS)} synthetic accounts -> {out_path}")


if __name__ == "__main__":
    main()
