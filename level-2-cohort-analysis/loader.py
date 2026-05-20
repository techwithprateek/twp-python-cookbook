# ============================================================
# loader.py — Loads the UCI Online Retail II Excel file
# ============================================================
# Level 2 skill covered: Reading Excel files with multiple sheets
# and combining them into one DataFrame with pd.concat().

import pandas as pd   # pandas handles Excel files natively with read_excel()
import os             # os.path.exists() lets us check if a file is present


# Path where the user should place the downloaded Excel file
DATA_FILE = os.path.join("data", "online_retail_II.xlsx")


def load_data():
    """
    Reads both sheets from the UCI Online Retail II Excel file,
    stacks them on top of each other, and returns one big DataFrame.

    If the file doesn't exist, generates a small sample dataset
    so the project can still be demonstrated without a download.
    """

    if not os.path.exists(DATA_FILE):
        # ── Fallback: generate sample data ──────────────────────────────────
        print(f"⚠  '{DATA_FILE}' not found. Using built-in sample data instead.")
        print("   To use real data: download from https://archive.ics.uci.edu/dataset/502/online+retail+ii")
        print("   and place the file at:  data/online_retail_II.xlsx\n")
        return _generate_sample_data()

    print(f"Loading '{DATA_FILE}'...")

    # pd.read_excel() reads one sheet at a time.
    # sheet_name='Year 2009-2010' matches the exact tab name in the file.
    sheet1 = pd.read_excel(DATA_FILE, sheet_name="Year 2009-2010")
    print(f"  Sheet 1 loaded: {len(sheet1):,} rows")

    sheet2 = pd.read_excel(DATA_FILE, sheet_name="Year 2010-2011")
    print(f"  Sheet 2 loaded: {len(sheet2):,} rows")

    # pd.concat() stacks DataFrames vertically (one on top of the other).
    # ignore_index=True resets the row numbers so they run 0, 1, 2... continuously.
    df = pd.concat([sheet1, sheet2], ignore_index=True)
    print(f"  Combined total: {len(df):,} rows\n")

    return df


def _generate_sample_data():
    """
    Builds a small realistic dataset with ~500 transactions
    so the project runs without needing the actual file download.
    """
    import numpy as np
    import random

    # Fix the random seed so results are the same every time
    random.seed(42)
    np.random.seed(42)

    # ── Build date range: Dec 2020 – Nov 2022 (24 months) ───────────────────
    # pd.date_range() creates a sequence of dates between two points.
    dates = pd.date_range(start="2020-12-01", end="2022-11-30", freq="D")

    # ── Simulate customers who might buy in multiple months ──────────────────
    customer_ids = list(range(12001, 12200))   # 200 unique customers

    rows = []
    for _ in range(600):
        rows.append({
            "Invoice"      : f"INV{random.randint(100000, 999999)}",
            "StockCode"    : f"SC{random.randint(1000, 9999)}",
            "Description"  : random.choice(["Mug", "Candle", "Poster", "Notebook"]),
            "Quantity"     : random.randint(1, 20),
            "InvoiceDate"  : random.choice(dates),
            "Price"        : round(random.uniform(1.0, 50.0), 2),
            "Customer ID"  : random.choice(customer_ids),
            "Country"      : random.choice(["United Kingdom", "Germany", "France"]),
        })

    df = pd.DataFrame(rows)
    print(f"  Sample data generated: {len(df):,} rows\n")
    return df
