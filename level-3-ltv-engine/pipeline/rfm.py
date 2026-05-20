# ============================================================
# pipeline/rfm.py — Calculates RFM scores for each customer
# ============================================================
# Level 3 skills covered:
#   - Complex Transformations (multi-step aggregation)
#   - Window Functions (quintile-based ranking with pd.qcut)

import pandas as pd
import sys
import os

# Add parent directory to path so we can import config
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config


def compute_rfm(df):
    """
    Computes three metrics per customer as of the SNAPSHOT_DATE:

    RECENCY   — How many days ago was their last purchase?
                (lower = better: they bought recently)

    FREQUENCY — How many times have they bought in total?
                (higher = better: they buy often)

    MONETARY  — How much total revenue have they generated?
                (higher = better: they spend more)

    Each metric is then scored 1–5 using quintiles (pd.qcut),
    where 5 is always the best score.
    Returns a DataFrame with one row per customer.
    """

    print("--- Computing RFM scores ---")

    # Parse the snapshot date — this is our "today" reference point
    snapshot = pd.Timestamp(config.SNAPSHOT_DATE)

    # ── Step 1: Aggregate one row per customer ───────────────────────────────
    # groupby() + agg() lets us compute multiple statistics at once.
    # Each key in the dict is the output column name;
    # each value is a tuple of (source_column, aggregation_function).
    rfm = df.groupby("Customer ID").agg(
        LastPurchaseDate = ("InvoiceDate",   "max"),   # date of most recent order
        Frequency        = ("Invoice",       "nunique"),  # count of unique invoices
        Monetary         = ("TotalRevenue",  "sum"),   # total £ spent
    ).reset_index()

    # ── Step 2: Calculate Recency ────────────────────────────────────────────
    # Recency = number of days between the last purchase and the snapshot date.
    # (snapshot - LastPurchaseDate) gives a Timedelta; .dt.days extracts the integer.
    rfm["Recency"] = (snapshot - rfm["LastPurchaseDate"]).dt.days

    # ── Step 3: Score each metric into 5 quintile buckets ────────────────────
    # pd.qcut() splits the data into N equal-sized groups (by count, not by value).
    # labels=[1,2,3,4,5] assigns a score to each group.
    # rank(method='first') breaks ties by the order the values appear.

    q = config.NUM_QUANTILES

    # RECENCY: lower days = better → we INVERT the labels so score 5 = most recent
    rfm["R_score"] = pd.qcut(rfm["Recency"],
                             q=q,
                             labels=list(range(q, 0, -1)),   # [5,4,3,2,1]
                             duplicates="drop")

    # FREQUENCY: higher = better → score 5 = most frequent
    rfm["F_score"] = pd.qcut(rfm["Frequency"].rank(method="first"),
                             q=q,
                             labels=list(range(1, q + 1)))   # [1,2,3,4,5]

    # MONETARY: higher = better → score 5 = highest spend
    rfm["M_score"] = pd.qcut(rfm["Monetary"].rank(method="first"),
                             q=q,
                             labels=list(range(1, q + 1)))

    # Convert score columns from "category" dtype to plain integers
    rfm["R_score"] = rfm["R_score"].astype(int)
    rfm["F_score"] = rfm["F_score"].astype(int)
    rfm["M_score"] = rfm["M_score"].astype(int)

    # Create a combined RFM string score e.g. "543" for quick reference
    rfm["RFM_Score"] = (rfm["R_score"].astype(str)
                        + rfm["F_score"].astype(str)
                        + rfm["M_score"].astype(str))

    print(f"  RFM computed for {len(rfm):,} customers\n")
    return rfm
