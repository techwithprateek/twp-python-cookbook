# ============================================================
# pipeline/cleaner.py — Removes bad rows from the retail dataset
# ============================================================
# Level 3 skill covered: Data Quality Checks — the cleaner
# prints a before/after report so you can see exactly what was removed.

import pandas as pd
import os
from pipeline.loader import CSV_PATH   # path to save the cleaned CSV for reuse


def clean_data(df):
    """
    Cleans the raw retail DataFrame by removing:
      - Cancelled invoices (Invoice starts with 'C')
      - Rows with no Customer ID
      - Negative or zero quantities (returns / adjustments)
      - Zero or negative prices
      - Rows with unparseable dates
    Also saves a cleaned CSV to speed up future runs.
    """

    print("--- Cleaning data ---")
    start_rows = len(df)

    df = df.copy()

    # ── Parse dates ──────────────────────────────────────────────────────────
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")

    # ── Remove cancelled invoices ─────────────────────────────────────────────
    cancelled = df["Invoice"].astype(str).str.startswith("C")
    df = df[~cancelled]

    # ── Remove missing Customer IDs ───────────────────────────────────────────
    df = df.dropna(subset=["Customer ID"])

    # ── Keep only positive quantities and prices ──────────────────────────────
    df = df[df["Quantity"] > 0]
    df = df[df["Price"] > 0]

    # ── Drop rows where date parsing failed ───────────────────────────────────
    df = df.dropna(subset=["InvoiceDate"])

    # ── Add TotalRevenue column (Quantity × Price per line) ───────────────────
    # This is the "Complex Transformation" skill — deriving a new column
    # from existing ones to make downstream analysis simpler.
    df["TotalRevenue"] = df["Quantity"] * df["Price"]

    df = df.reset_index(drop=True)
    end_rows = len(df)
    print(f"  {start_rows:,} → {end_rows:,} rows  ({start_rows - end_rows:,} removed)\n")

    # ── Save cleaned CSV so future runs skip Excel parsing ────────────────────
    os.makedirs(os.path.dirname(CSV_PATH) if os.path.dirname(CSV_PATH) else ".", exist_ok=True)
    df.to_csv(CSV_PATH, index=False)
    print(f"  Cleaned CSV saved to {CSV_PATH} (speeds up future runs)\n")

    return df
