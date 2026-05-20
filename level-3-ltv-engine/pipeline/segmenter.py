# ============================================================
# pipeline/segmenter.py — Assigns each customer a LTV segment
# ============================================================
# Level 3 skill covered: Decision-ready insights.
# We turn raw RFM scores into business-friendly labels
# that a stakeholder can act on immediately.

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config


def assign_segments(rfm):
    """
    Reads each customer's R, F, M scores and assigns them
    to one of five business segments:

    Champions    — buy often, spend a lot, bought recently
    Loyal        — buy regularly and spend well
    At Risk      — used to buy often but haven't lately
    Hibernating  — low recency AND low frequency
    Lost         — everyone else (low scores across the board)

    The rules come from config.py so they can be tuned without changing code.
    Returns the rfm DataFrame with a new 'Segment' column.
    """

    print("--- Assigning customer segments ---")

    def _get_segment(row):
        """
        Applies the segment rules to a single row.
        Rules are checked in priority order — the first match wins.
        """
        r = row["R_score"]
        f = row["F_score"]
        m = row["M_score"]

        rules = config.SEGMENT_RULES

        # Champions: high on ALL three metrics
        c = rules["Champions"]
        if r >= c["r_min"] and f >= c["f_min"] and m >= c["m_min"]:
            return "Champions"

        # Loyal: good frequency and monetary (recency not checked)
        l = rules["Loyal"]
        if f >= l["f_min"] and m >= l["m_min"]:
            return "Loyal"

        # At Risk: low recency but was frequent (lapsed loyal customer)
        ar = rules["At Risk"]
        if r <= ar["r_max"] and f >= ar["f_min"]:
            return "At Risk"

        # Hibernating: low recency AND low frequency
        h = rules["Hibernating"]
        if r <= h["r_max"] and f <= h["f_max"]:
            return "Hibernating"

        # Default: Lost
        return "Lost"

    # .apply() runs _get_segment() on every row.
    # axis=1 tells pandas to pass each ROW as a Series into the function.
    # Without axis=1, pandas would pass each COLUMN instead — which is not what we want.
    rfm = rfm.copy()
    rfm["Segment"] = rfm.apply(_get_segment, axis=1)

    # ── Print segment breakdown ───────────────────────────────────────────────
    print("\n  Segment breakdown:")
    summary = (rfm.groupby("Segment")
               .agg(Customers=("Customer ID", "count"),
                    Revenue=("Monetary", "sum"))
               .sort_values("Revenue", ascending=False))

    for segment, row in summary.iterrows():
        # f-string format specifiers control column alignment for neat printing:
        #   {segment:<15}  = left-align the segment name, padded to 15 characters wide
        #   {int(...):>5}  = right-align the customer count in 5 characters
        #   {:>10,.0f}     = right-align revenue in 10 chars, with comma separators, no decimals
        print(f"  {segment:<15}: {int(row['Customers']):>5} customers   "
              f"£{row['Revenue']:>10,.0f} revenue")

    print()
    return rfm
