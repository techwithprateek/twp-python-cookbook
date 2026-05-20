# ============================================================
# main.py — Entry point for the Remote Job Scraper
# ============================================================
# Run this file with:  python main.py <keyword>
# Example:             python main.py python
#
# What this project teaches (Level 1 skills):
#   ✔ Python Syntax & Variables
#   ✔ Lists & Dictionaries (JSON data)
#   ✔ Loops & Functions
#   ✔ Reading and filtering a DataFrame
#   ✔ Handling missing values
#   ✔ Basic Visualizations

import sys    # sys.argv lets us read command-line arguments (the keyword the user types)
import os     # os helps with file and folder operations

# Import our own modules — each file handles one responsibility
from scraper    import fetch_jobs
from cleaner    import clean_jobs
from visualiser import plot_top_companies


def main():
    """
    Orchestrates the full pipeline:
    fetch → clean → save CSV → plot chart
    """

    # ── Step 1: Read the keyword from the command line ───────────────────────
    # sys.argv is a list of strings the user typed after "python main.py"
    # sys.argv[0] = "main.py" (the script name itself)
    # sys.argv[1] = the first argument the user typed, e.g. "python"
    if len(sys.argv) < 2:
        # If no keyword was provided, show instructions and exit
        print("Usage:   python main.py <keyword>")
        print("Example: python main.py python")
        sys.exit(1)   # exit with code 1 signals an error

    # Store the keyword; .lower() makes the search case-insensitive
    keyword = sys.argv[1].lower()
    print(f"\n🔍 Searching for '{keyword}' jobs on RemoteOK...\n")

    # ── Step 2: Fetch raw data from the API ──────────────────────────────────
    raw_df = fetch_jobs()

    # ── Step 3: Clean and filter the data ────────────────────────────────────
    clean_df = clean_jobs(raw_df, keyword)

    # ── Step 4: Stop early if no results were found ──────────────────────────
    if clean_df.empty:
        print(f"\nNo jobs found for '{keyword}'. Try a different keyword.")
        sys.exit(0)

    # ── Step 5: Save the cleaned data to a CSV file ──────────────────────────
    # Create the output folder if it doesn't already exist
    output_folder = "output"
    os.makedirs(output_folder, exist_ok=True)

    # Build the CSV file path
    csv_path = os.path.join(output_folder, "jobs_clean.csv")

    # .to_csv() writes the DataFrame to a CSV file.
    # index=False means don't write the row numbers (0, 1, 2...) as a column.
    clean_df.to_csv(csv_path, index=False)
    print(f"\nCSV saved  → {csv_path}  ({len(clean_df)} rows)")

    # ── Step 6: Create a bar chart of top hiring companies ───────────────────
    plot_top_companies(clean_df, keyword, output_folder)

    # ── Step 7: Print a summary for the user ─────────────────────────────────
    print("\n" + "=" * 50)
    print("✅  All done!")
    print(f"   Keyword  : {keyword}")
    print(f"   Jobs found: {len(clean_df)}")
    print(f"   CSV       : {csv_path}")
    print(f"   Chart     : {output_folder}/top_companies.png")
    print("=" * 50)


# This block ensures main() only runs when we execute this file directly.
# It does NOT run if another file imports this module.
if __name__ == "__main__":
    main()
