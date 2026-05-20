# ============================================================
# visualiser.py — Creates a bar chart of top hiring companies
# ============================================================
# Level 1 skill covered: Basic visualizations with matplotlib

import matplotlib.pyplot as plt   # the standard Python charting library
import os                         # used to work with file paths and folders


def plot_top_companies(df, keyword, output_folder="output"):
    """
    Takes the cleaned DataFrame and draws a horizontal bar chart
    showing the top 10 companies with the most job postings
    for the given keyword. Saves the chart as a PNG image.
    """

    print("\n--- Creating bar chart ---")

    # ── Step 1: Count jobs per company ──────────────────────────────────────
    # .value_counts() counts how many times each company name appears.
    # It returns a Series sorted from most to least.
    company_counts = df["company"].value_counts()

    # Keep only the top 10 companies (head(10) = first 10 rows)
    top_10 = company_counts.head(10)

    # If there are no results, tell the user and stop
    if top_10.empty:
        print("No data to plot — skipping chart.")
        return

    # ── Step 2: Set up the chart ─────────────────────────────────────────────
    # plt.figure() creates a blank canvas. figsize=(width, height) in inches.
    fig, ax = plt.subplots(figsize=(10, 6))

    # .barh() draws a HORIZONTAL bar chart (easier to read long company names)
    # top_10.values = the count numbers (bar lengths)
    # top_10.index  = the company names (y-axis labels)
    # color sets the bar colour; edgecolor adds a thin border to each bar
    ax.barh(top_10.index, top_10.values, color="steelblue", edgecolor="white")

    # ── Step 3: Add labels and a title ──────────────────────────────────────
    ax.set_xlabel("Number of Job Postings", fontsize=12)
    ax.set_ylabel("Company", fontsize=12)
    ax.set_title(f"Top 10 Companies Hiring for '{keyword}'", fontsize=14, fontweight="bold")

    # Invert the y-axis so the company with the MOST jobs appears at the TOP
    ax.invert_yaxis()

    # Add a light grid on the x-axis to make values easier to read
    ax.xaxis.grid(True, linestyle="--", alpha=0.7)
    ax.set_axisbelow(True)   # grid lines go behind the bars

    # tight_layout() automatically adjusts spacing so nothing is cut off
    plt.tight_layout()

    # ── Step 4: Save the chart to a file ────────────────────────────────────
    # Make sure the output folder exists (create it if it doesn't)
    os.makedirs(output_folder, exist_ok=True)

    # Build the full file path e.g. "output/top_companies.png"
    output_path = os.path.join(output_folder, "top_companies.png")

    # savefig() saves the chart as an image file. dpi=150 gives a crisp image.
    plt.savefig(output_path, dpi=150)

    # Close the figure to free up memory
    plt.close()

    print(f"Chart saved → {output_path}")
