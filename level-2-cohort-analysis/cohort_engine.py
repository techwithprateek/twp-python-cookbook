# ============================================================
# cohort_engine.py — Builds the cohort retention matrix
# ============================================================
# Level 2 skills covered:
#   - GroupBy Operations
#   - Merge & Join
#   - Pivot Tables
#   - Datetime Manipulation (period arithmetic)
#   - Sorting and ranking

import pandas as pd   # all cohort logic uses pandas


def build_retention_matrix(df):
    """
    Answers: "Of customers who first bought in Month X,
    what % came back in months X+1, X+2, X+3 ... ?"

    Steps:
      1. Find each customer's first-ever purchase month (their CohortMonth).
      2. Attach that CohortMonth to every transaction.
      3. Calculate how many months after their first purchase each transaction is (CohortIndex).
      4. Count unique customers per (CohortMonth, CohortIndex) pair.
      5. Divide by the cohort size to get a retention percentage.
    Returns: retention_pct (DataFrame of percentages), cohort_counts (raw numbers).
    """

    print("--- Building cohort retention matrix ---")

    # ── Step 1: Find each customer's first purchase month ───────────────────
    # groupby('Customer ID') splits the data into one group per customer.
    # ['InvoiceMonth'].min() finds the earliest month in each group.
    # .reset_index() turns the result back into a regular flat DataFrame.
    first_purchase = (
        df.groupby("Customer ID")["InvoiceMonth"]
        .min()
        .reset_index()
    )
    # Rename the column so it's clear this is the cohort (first purchase) month
    first_purchase.columns = ["Customer ID", "CohortMonth"]

    print(f"  Found {len(first_purchase):,} unique customers")

    # ── Step 2: Attach CohortMonth to every transaction ──────────────────────
    # merge() is like SQL JOIN — it matches rows from two DataFrames on a shared column.
    # on='Customer ID' means: connect rows where Customer ID matches.
    # how='left' means: keep ALL rows from the left DataFrame (df), even if no match exists.
    df = df.merge(first_purchase, on="Customer ID", how="left")

    # ── Step 3: Calculate CohortIndex (months since first purchase) ──────────
    # Subtracting two Period objects gives a number of months.
    # We use .apply() to do this row-by-row.
    # The result tells us: "this transaction happened N months after the customer first bought."
    df["CohortIndex"] = (df["InvoiceMonth"] - df["CohortMonth"]).apply(lambda x: x.n)

    # ── Step 4: Count unique customers per (CohortMonth, CohortIndex) ────────
    # groupby() groups by two columns at once.
    # nunique() counts unique Customer IDs (not total transactions) per group.
    cohort_counts = (
        df.groupby(["CohortMonth", "CohortIndex"])["Customer ID"]
        .nunique()
        .reset_index()
    )
    cohort_counts.columns = ["CohortMonth", "CohortIndex", "Customers"]

    # ── Step 5: Pivot into a matrix (CohortMonth = rows, CohortIndex = columns) ─
    # pivot_table() reshapes from "tall" format to "wide" format.
    # Each row = one cohort month; each column = months since first purchase (0, 1, 2, ...)
    cohort_pivot = cohort_counts.pivot_table(
        index="CohortMonth",
        columns="CohortIndex",
        values="Customers"
    )

    # ── Step 6: Calculate retention percentages ──────────────────────────────
    # Column 0 = the number of customers who made their FIRST purchase in that month.
    # We divide every column by column 0 to get "what % are still buying in month N?"
    cohort_size = cohort_pivot[0]   # Series of cohort sizes (one per row)

    # .divide(cohort_size, axis=0) divides each row by that row's cohort size
    # Multiply by 100 to convert to percentages. Round to 1 decimal place.
    retention_pct = cohort_pivot.divide(cohort_size, axis=0).mul(100).round(1)

    print(f"  Cohort matrix shape: {retention_pct.shape[0]} cohorts × {retention_pct.shape[1]} months\n")

    return retention_pct, cohort_pivot
