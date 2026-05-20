# ============================================================
# main.py — Entry point for the Cohort Analysis pipeline
# ============================================================
# Run this file with:  python3 main.py
#
# What this project teaches (Level 2 skills):
#   ✔ GroupBy Operations
#   ✔ Merge & Join
#   ✔ Pivot Tables
#   ✔ Datetime Manipulation
#   ✔ Exploratory Analysis
#   ✔ Statistical Visualizations (heatmap)
#   ✔ Data Validation

import os

# Import each step of the pipeline from its own file
from loader         import load_data
from cleaner        import clean_data
from cohort_engine  import build_retention_matrix
from visualiser     import plot_heatmap


def main():
    """
    Runs the full cohort analysis pipeline:
    load → clean → build matrix → save CSV → draw heatmap
    """

    print("\n📊 Cohort Analysis Pipeline\n" + "=" * 40)

    # ── Step 1: Load raw data ────────────────────────────────────────────────
    raw_df = load_data()

    # ── Step 2: Clean the data ───────────────────────────────────────────────
    clean_df = clean_data(raw_df)

    # ── Step 3: Quick exploratory summary ────────────────────────────────────
    # This is the "Exploratory Analysis" skill — always inspect your data before modelling.
    print("--- Exploratory summary ---")
    print(f"  Date range   : {clean_df['InvoiceDate'].min().date()} → {clean_df['InvoiceDate'].max().date()}")
    print(f"  Unique customers: {clean_df['Customer ID'].nunique():,}")
    print(f"  Unique months   : {clean_df['InvoiceMonth'].nunique()}")
    print(f"  Total invoices  : {clean_df['Invoice'].nunique():,}\n")

    # ── Step 4: Build cohort retention matrix ────────────────────────────────
    retention_pct, cohort_counts = build_retention_matrix(clean_df)

    # ── Step 5: Save the retention matrix to CSV ─────────────────────────────
    output_folder = "output"
    os.makedirs(output_folder, exist_ok=True)

    csv_path = os.path.join(output_folder, "retention_matrix.csv")
    # Convert Period index to strings before saving (CSV doesn't know about Periods)
    retention_pct.index = retention_pct.index.astype(str)
    retention_pct.to_csv(csv_path)
    print(f"Retention matrix saved → {csv_path}")

    # ── Step 6: Print top cohorts by 3-month retention ───────────────────────
    # Column 3 = retention at month 3 (customers who came back 3 months later)
    if 3 in cohort_counts.columns:
        print("\n--- Top 3 cohorts by 3-month retention ---")
        # Sort by the month-3 retention percentage, descending
        top_3 = retention_pct[3].dropna().sort_values(ascending=False).head(3)
        for cohort_month, pct in top_3.items():
            print(f"  {cohort_month}: {pct:.1f}%")

    # ── Step 7: Draw heatmap ─────────────────────────────────────────────────
    # reload with Period index for the chart
    retention_pct, cohort_counts = build_retention_matrix(clean_df)
    plot_heatmap(retention_pct, output_folder)

    # ── Final summary ────────────────────────────────────────────────────────
    print("\n" + "=" * 40)
    print("✅  All done!")
    print(f"   CSV    : {csv_path}")
    print(f"   Heatmap: {output_folder}/cohort_heatmap.png")
    print("=" * 40)


if __name__ == "__main__":
    main()
