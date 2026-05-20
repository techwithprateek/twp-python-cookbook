# ============================================================
# main.py — Entry point for the LTV Engine
# ============================================================
# Run this file with:  python3 main.py
#
# What this project teaches (Level 3 skills):
#   ✔ Complex Transformations (multi-step aggregation)
#   ✔ Window Functions (pd.qcut quintile scoring)
#   ✔ Pipeline Automation (config-driven, modular stages)
#   ✔ Data Quality Checks (automated assertions before analysis)
#   ✔ Decision-ready insights (segments + dashboard)

import os
import sys

# Add the current directory to the Python path so imports work correctly
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pipeline.loader    import load_data
from pipeline.cleaner   import clean_data
from pipeline.quality   import run_checks
from pipeline.rfm       import compute_rfm
from pipeline.segmenter import assign_segments
from reporting.dashboard    import build_dashboard
from reporting.email_report import send_report
import config


def main():
    """
    Runs the full LTV Engine pipeline:
    load → clean → quality checks → RFM scores → segments → dashboard → email
    """

    print("\n🏆 LTV Engine Pipeline\n" + "=" * 45)

    # ── Stage 1: Load raw data ────────────────────────────────────────────────
    raw_df = load_data()

    # ── Stage 2: Clean data ───────────────────────────────────────────────────
    clean_df = clean_data(raw_df)

    # ── Stage 3: Run automated quality checks ────────────────────────────────
    # This stops the pipeline early if the data doesn't meet our expectations.
    run_checks(clean_df)

    # ── Stage 4: Compute RFM scores ───────────────────────────────────────────
    rfm = compute_rfm(clean_df)

    # ── Stage 5: Assign LTV segments ─────────────────────────────────────────
    rfm = assign_segments(rfm)

    # ── Stage 6: Save results to CSV ─────────────────────────────────────────
    os.makedirs(config.OUTPUT_FOLDER, exist_ok=True)
    csv_path = os.path.join(config.OUTPUT_FOLDER, config.LTV_CSV)

    # Drop the helper date column before saving — it's not needed in the output
    output_cols = ["Customer ID", "Recency", "Frequency", "Monetary",
                   "R_score", "F_score", "M_score", "RFM_Score", "Segment"]
    rfm[output_cols].to_csv(csv_path, index=False)
    print(f"Customer LTV data saved → {csv_path}")

    # ── Stage 7: Build 4-panel dashboard ─────────────────────────────────────
    build_dashboard(rfm)

    # ── Stage 8: Send email report (skips if email not configured) ────────────
    send_report(rfm)

    # ── Final summary ─────────────────────────────────────────────────────────
    print("=" * 45)
    print("✅  All done!")
    print(f"   Customers analysed : {len(rfm):,}")
    print(f"   Segments assigned  : {rfm['Segment'].nunique()}")
    print(f"   CSV                : {csv_path}")
    print(f"   Dashboard          : {config.OUTPUT_FOLDER}/{config.DASHBOARD_IMG}")
    print("=" * 45)


if __name__ == "__main__":
    main()
