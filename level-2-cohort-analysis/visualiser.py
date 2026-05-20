# ============================================================
# visualiser.py — Draws a colour-coded cohort heatmap
# ============================================================
# Level 2 skill covered: Statistical Visualizations (heatmap)

import matplotlib.pyplot as plt   # base plotting library
import matplotlib.ticker as mticker
import os                         # file path helpers


def plot_heatmap(retention_pct, output_folder="output"):
    """
    Draws a heatmap where:
      - Each ROW is a cohort month (customers who first bought that month)
      - Each COLUMN is how many months later (0 = first month, 1 = one month later, etc.)
      - The cell COLOUR and NUMBER show what % of that cohort returned
    Saves the chart as cohort_heatmap.png.
    """

    print("--- Drawing cohort heatmap ---")

    # ── Convert Period index to strings so matplotlib can label them ─────────
    # Period objects (like 2020-12) need to be strings for axis labels
    retention_display = retention_pct.copy()
    retention_display.index = retention_display.index.astype(str)

    # ── Set up the figure ────────────────────────────────────────────────────
    # Make the figure tall enough that row labels don't overlap
    fig_height = max(6, len(retention_display) * 0.5)
    fig, ax = plt.subplots(figsize=(14, fig_height))

    # ── Draw the heatmap using imshow ────────────────────────────────────────
    # imshow() draws a 2D grid of coloured cells — perfect for a matrix.
    # .values extracts the underlying numpy array from the DataFrame.
    # vmin=0, vmax=100 fixes the colour scale from 0% to 100%.
    # cmap='YlOrRd' = yellow (low) → orange → red (high) colour scheme.
    im = ax.imshow(
        retention_display.values,
        aspect="auto",        # don't force square cells
        cmap="YlOrRd",
        vmin=0, vmax=100
    )

    # ── Add a colour bar legend on the right ─────────────────────────────────
    cbar = plt.colorbar(im, ax=ax, shrink=0.8)
    cbar.set_label("Retention %", fontsize=11)

    # ── Label axes ───────────────────────────────────────────────────────────
    ax.set_xticks(range(len(retention_display.columns)))
    ax.set_xticklabels([f"Month {c}" for c in retention_display.columns], rotation=45, ha="right")

    ax.set_yticks(range(len(retention_display.index)))
    ax.set_yticklabels(retention_display.index)

    ax.set_xlabel("Months Since First Purchase", fontsize=12)
    ax.set_ylabel("Cohort (First Purchase Month)", fontsize=12)
    ax.set_title("Customer Retention by Cohort", fontsize=14, fontweight="bold")

    # ── Write the percentage number inside each cell ──────────────────────────
    for row_idx in range(len(retention_display.index)):
        for col_idx in range(len(retention_display.columns)):
            value = retention_display.values[row_idx, col_idx]
            if not __import__("math").isnan(value):
                # Pick text colour: white on dark cells, black on light cells
                text_color = "white" if value > 60 else "black"
                ax.text(
                    col_idx, row_idx,       # x, y position (column, row)
                    f"{value:.0f}%",        # formatted text e.g. "42%"
                    ha="center", va="center",
                    fontsize=7,
                    color=text_color
                )

    plt.tight_layout()

    # ── Save the chart ───────────────────────────────────────────────────────
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, "cohort_heatmap.png")
    plt.savefig(output_path, dpi=150)
    plt.close()
    print(f"Heatmap saved → {output_path}")
