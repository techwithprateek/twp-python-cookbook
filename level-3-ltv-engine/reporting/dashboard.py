# ============================================================
# reporting/dashboard.py — 4-panel matplotlib dashboard
# ============================================================
# Level 3 skill covered: Decision-ready insights — visualising
# all key metrics on one page so stakeholders get the full picture.

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config


# Consistent colour map for the five segments
SEGMENT_COLORS = {
    "Champions"  : "#2ecc71",   # green
    "Loyal"      : "#3498db",   # blue
    "At Risk"    : "#e67e22",   # orange
    "Hibernating": "#9b59b6",   # purple
    "Lost"       : "#e74c3c",   # red
}


def build_dashboard(rfm):
    """
    Creates a 2×2 grid of charts:
      Panel 1 (top-left)  — Segment customer count (pie chart)
      Panel 2 (top-right) — Revenue by segment (bar chart)
      Panel 3 (bot-left)  — RFM score distribution (histogram)
      Panel 4 (bot-right) — Recency vs Monetary scatter (sample)
    Saves the result as output/dashboard.png.
    """

    print("--- Building dashboard ---")

    # plt.subplots(2, 2) creates a 2-row, 2-column grid of chart panels.
    # fig is the overall canvas; axes is a 2×2 array of panels.
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("Customer LTV Dashboard", fontsize=16, fontweight="bold", y=1.01)

    # ── Panel 1: Pie chart — customer count by segment ───────────────────────
    ax1 = axes[0, 0]
    segment_counts = rfm["Segment"].value_counts()
    colors_ordered  = [SEGMENT_COLORS.get(s, "#aaa") for s in segment_counts.index]
    ax1.pie(
        segment_counts.values,
        labels=segment_counts.index,
        colors=colors_ordered,
        autopct="%1.1f%%",     # show percentage inside each slice e.g. "23.4%"
        startangle=90,
        pctdistance=0.8,       # how far from the centre the % labels sit (0.8 = 80% of the radius)
    )
    ax1.set_title("Customer Count by Segment", fontweight="bold")

    # ── Panel 2: Bar chart — revenue by segment ───────────────────────────────
    ax2 = axes[0, 1]
    revenue_by_seg = (rfm.groupby("Segment")["Monetary"]
                      .sum()
                      .sort_values(ascending=False))
    bar_colors = [SEGMENT_COLORS.get(s, "#aaa") for s in revenue_by_seg.index]
    bars = ax2.bar(revenue_by_seg.index, revenue_by_seg.values, color=bar_colors, edgecolor="white")
    ax2.set_title("Total Revenue by Segment", fontweight="bold")
    ax2.set_ylabel("Revenue (£)")
    ax2.tick_params(axis="x", rotation=20)
    # Add a revenue label on top of each bar.
    # bar.get_x()      = the left edge x-position of the bar
    # bar.get_width()  = the width of the bar
    # bar.get_height() = the height of the bar (= the revenue value)
    # We place the text at the horizontal centre and just 1% above the bar top.
    for bar in bars:
        ax2.text(bar.get_x() + bar.get_width() / 2,   # horizontal centre of bar
                 bar.get_height() * 1.01,              # 1% above the bar top
                 f"£{bar.get_height():,.0f}",          # label text e.g. "£12,345"
                 ha="center", va="bottom", fontsize=8)

    # ── Panel 3: Histogram — distribution of RFM total scores ────────────────
    ax3 = axes[1, 0]
    rfm["RFM_Total"] = rfm["R_score"] + rfm["F_score"] + rfm["M_score"]
    ax3.hist(rfm["RFM_Total"], bins=12, color="steelblue", edgecolor="white")
    ax3.set_title("Distribution of RFM Total Scores", fontweight="bold")
    ax3.set_xlabel("R + F + M Score (max = 15)")
    ax3.set_ylabel("Number of Customers")
    ax3.axvline(rfm["RFM_Total"].mean(), color="red", linestyle="--",
                label=f"Mean: {rfm['RFM_Total'].mean():.1f}")
    ax3.legend()

    # ── Panel 4: Scatter — Recency vs Monetary coloured by segment ───────────
    ax4 = axes[1, 1]
    # Plot a sample of max 300 points so the chart isn't too crowded
    sample = rfm.sample(min(300, len(rfm)), random_state=42)
    for seg, group in sample.groupby("Segment"):
        ax4.scatter(
            group["Recency"],
            group["Monetary"],
            c=SEGMENT_COLORS.get(seg, "#aaa"),
            label=seg,
            alpha=0.7,
            s=30,           # dot size
            edgecolors="none"
        )
    ax4.set_title("Recency vs Revenue (by Segment)", fontweight="bold")
    ax4.set_xlabel("Recency (days since last purchase)")
    ax4.set_ylabel("Total Revenue (£)")
    ax4.legend(fontsize=8, loc="upper right")

    plt.tight_layout()

    # ── Save the dashboard ───────────────────────────────────────────────────
    os.makedirs(config.OUTPUT_FOLDER, exist_ok=True)
    output_path = os.path.join(config.OUTPUT_FOLDER, config.DASHBOARD_IMG)
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Dashboard saved → {output_path}\n")
