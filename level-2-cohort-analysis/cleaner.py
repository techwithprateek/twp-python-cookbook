# ============================================================
# cleaner.py — Removes bad rows from the retail dataset
# ============================================================
# Level 2 skills covered:
#   - Filtering rows with multiple conditions
#   - Datetime parsing and manipulation
#   - Data Validation (checking for nulls, negatives, etc.)

import pandas as pd   # for DataFrame operations


def clean_data(df):
    """
    Removes rows that would corrupt the analysis:
      - Cancelled invoices (Invoice starts with 'C')
      - Missing Customer IDs (can't track a cohort without knowing the customer)
      - Negative quantities (returns / adjustments)
      - Non-positive prices
    Also parses InvoiceDate into a proper datetime type
    and adds an 'InvoiceMonth' column (year + month only).
    Returns a clean copy of the DataFrame.
    """

    print("--- Cleaning data ---")
    start_rows = len(df)

    # ── Step 1: Parse InvoiceDate as a datetime ──────────────────────────────
    # Dates often come in as plain strings like "2020-12-01 09:31:00".
    # pd.to_datetime() converts them so we can do maths on them (e.g. subtract months).
    # errors='coerce' turns unparseable dates into NaT (Not a Time) instead of crashing.
    df = df.copy()   # work on a copy so we don't modify the original
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")

    # ── Step 2: Remove cancelled invoices ───────────────────────────────────
    # Cancelled invoices start with the letter 'C' (e.g. "C536379").
    # .astype(str) ensures the column is text before we call .str.startswith().
    cancelled_mask = df["Invoice"].astype(str).str.startswith("C")
    df = df[~cancelled_mask]   # ~ means NOT — keep rows that are NOT cancelled
    print(f"  Removed {cancelled_mask.sum():,} cancelled invoices")

    # ── Step 3: Remove rows with no Customer ID ──────────────────────────────
    # .isna() returns True for every NaN / NaT / None value.
    # We drop those rows because we can't track a cohort without knowing the customer.
    missing_customers = df["Customer ID"].isna().sum()
    df = df.dropna(subset=["Customer ID"])
    print(f"  Removed {missing_customers:,} rows with missing Customer ID")

    # ── Step 4: Remove negative or zero quantities ───────────────────────────
    # Negative quantities mean returned goods — we exclude them.
    neg_qty = (df["Quantity"] <= 0).sum()
    df = df[df["Quantity"] > 0]
    print(f"  Removed {neg_qty:,} rows with non-positive Quantity")

    # ── Step 5: Remove zero or negative prices ───────────────────────────────
    neg_price = (df["Price"] <= 0).sum()
    df = df[df["Price"] > 0]
    print(f"  Removed {neg_price:,} rows with non-positive Price")

    # ── Step 6: Remove rows where date parsing failed ────────────────────────
    bad_dates = df["InvoiceDate"].isna().sum()
    df = df.dropna(subset=["InvoiceDate"])
    print(f"  Removed {bad_dates:,} rows with unparseable dates")

    # ── Step 7: Add InvoiceMonth column ──────────────────────────────────────
    # We only care about the MONTH of each purchase, not the exact day or time.
    # dt.to_period('M') converts a full datetime (e.g. 2020-12-05 09:31:00)
    # into a "Month Period" object that represents the whole month (e.g. 2020-12).
    # A Period is better than a datetime here because all transactions in December 2020
    # will have the SAME value (2020-12), making grouping by month straightforward.
    # If we kept full datetimes, 2020-12-05 and 2020-12-19 would look like different groups.
    df["InvoiceMonth"] = df["InvoiceDate"].dt.to_period("M")

    # Reset row index after all the filtering
    df = df.reset_index(drop=True)

    end_rows = len(df)
    print(f"  Kept {end_rows:,} of {start_rows:,} rows ({start_rows - end_rows:,} removed total)\n")

    return df
