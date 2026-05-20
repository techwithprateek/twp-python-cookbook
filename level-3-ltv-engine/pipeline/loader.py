# ============================================================
# pipeline/loader.py — Loads the retail dataset (or sample data)
# ============================================================
# Level 3 skill covered: Pipeline Automation — the loader detects
# which input format is available and handles it automatically.

import pandas as pd
import os


XLSX_PATH = os.path.join("data", "online_retail_II.xlsx")
CSV_PATH  = os.path.join("data", "online_retail_II_clean.csv")


def load_data():
    """
    Loads data in this priority order:
    1. Cleaned CSV (fastest — from a previous run)
    2. Raw Excel file (slower — needs parsing)
    3. Generated sample data (fallback — no download needed)
    """

    # ── Option 1: Use cleaned CSV if it already exists ──────────────────────
    # Running the pipeline twice is much faster because we skip Excel parsing.
    if os.path.exists(CSV_PATH):
        print(f"Loading cleaned CSV from previous run: {CSV_PATH}")
        df = pd.read_csv(CSV_PATH, parse_dates=["InvoiceDate"])
        print(f"  Loaded {len(df):,} rows\n")
        return df

    # ── Option 2: Read from the Excel file ──────────────────────────────────
    if os.path.exists(XLSX_PATH):
        print(f"Loading Excel file: {XLSX_PATH}  (this may take a minute...)")
        sheet1 = pd.read_excel(XLSX_PATH, sheet_name="Year 2009-2010")
        sheet2 = pd.read_excel(XLSX_PATH, sheet_name="Year 2010-2011")
        df = pd.concat([sheet1, sheet2], ignore_index=True)
        print(f"  Loaded {len(df):,} rows from 2 sheets\n")
        return df

    # ── Option 3: Generate sample data ──────────────────────────────────────
    print("⚠  No data file found. Using built-in sample data.")
    print("   Place online_retail_II.xlsx in the data/ folder for real results.\n")
    return _generate_sample_data()


def _generate_sample_data():
    """Generates a realistic sample dataset with ~800 rows for testing."""
    import numpy as np
    import random

    random.seed(99)
    np.random.seed(99)

    # Create a 2-year date range
    dates = pd.date_range(start="2009-12-01", end="2011-12-09", freq="D")

    # 300 customers spread across the date range
    customer_ids = list(range(12001, 12301))

    rows = []
    for _ in range(800):
        rows.append({
            "Invoice"     : f"INV{random.randint(100000, 999999)}",
            "StockCode"   : f"SC{random.randint(1000, 9999)}",
            "Description" : random.choice(["Mug", "Frame", "Candle", "Vase", "Tin"]),
            "Quantity"    : random.randint(1, 30),
            "InvoiceDate" : random.choice(dates),
            "Price"       : round(random.uniform(0.5, 80.0), 2),
            "Customer ID" : random.choice(customer_ids),
            "Country"     : "United Kingdom",
        })

    df = pd.DataFrame(rows)
    # Add a small number of "bad" rows that the cleaner should remove
    bad_rows = pd.DataFrame([{
        "Invoice": "C99999", "StockCode": "SC0000", "Description": "Return",
        "Quantity": -5, "InvoiceDate": dates[0], "Price": 2.0,
        "Customer ID": 12001, "Country": "United Kingdom",
    }])
    df = pd.concat([df, bad_rows], ignore_index=True)

    print(f"  Sample data generated: {len(df):,} rows\n")
    return df
