# ============================================================
# cleaner.py — Cleans the raw job data
# ============================================================
# Level 1 skills covered:
#   - Selecting specific columns from a DataFrame
#   - Handling missing values (NaN = Not a Number)
#   - Filtering rows based on a condition
#   - Working with lists inside DataFrame cells

import pandas as pd   # pandas for data manipulation


def clean_jobs(df, keyword):
    """
    Takes the raw DataFrame from the API and:
    1. Keeps only the columns we care about
    2. Fills in missing salary info with 0
    3. Removes duplicate job posts
    4. Filters to jobs matching the user's keyword
    Returns a cleaned DataFrame.
    """

    print("\n--- Starting data cleaning ---")

    # ── Step 1: Keep only the columns we actually need ──────────────────────
    # The API returns 30+ columns — we only care about a handful.
    # We use a list of column names to select them.
    columns_we_want = ["id", "company", "position", "tags", "salary_min", "salary_max", "date"]

    # Some columns might not exist in every API response, so we filter
    # to only keep columns that are actually present in our data.
    existing_columns = [col for col in columns_we_want if col in df.columns]
    # .copy() prevents a "SettingWithCopyWarning" when we modify the DataFrame later.
    # Without it, pandas warns that we might be editing a view of the original data.
    df = df[existing_columns].copy()

    print(f"Kept {len(existing_columns)} columns: {existing_columns}")

    # ── Step 2: Handle missing salary values ────────────────────────────────
    # pd.to_numeric() converts a column to numbers.
    # errors='coerce' means: if a value can't be converted (e.g. empty string), turn it into NaN.
    # .fillna(0) then replaces all NaN values with 0 so we don't have gaps.
    if "salary_min" in df.columns:
        df["salary_min"] = pd.to_numeric(df["salary_min"], errors="coerce").fillna(0)
    if "salary_max" in df.columns:
        df["salary_max"] = pd.to_numeric(df["salary_max"], errors="coerce").fillna(0)

    # ── Step 3: Remove duplicate rows ───────────────────────────────────────
    # The API sometimes returns the same job twice.
    # We deduplicate on the "id" column only — the unique job identifier.
    # We can't use all columns because the "tags" column contains Python lists,
    # and lists can't be compared for equality in this context.
    rows_before = len(df)
    if "id" in df.columns:
        df = df.drop_duplicates(subset=["id"])
    rows_after = len(df)
    duplicates_removed = rows_before - rows_after
    print(f"Removed {duplicates_removed} duplicate rows. {rows_after} rows remaining.")

    # ── Step 4: Filter by the user's keyword ────────────────────────────────
    # Each job has a "tags" column which is a Python list e.g. ["python", "django", "remote"]
    # We need to convert that list to a single string so we can search it easily.

    if "tags" in df.columns:
        # .apply() runs a function on every row in the column.
        # lambda x: is a short anonymous function — it works like def but on one line.
        # isinstance(x, list) checks whether x is actually a Python list (returns True/False).
        # We need this check because some rows might have None or a plain string in the tags field
        # instead of a proper list — and calling .join() on those would crash.
        # If x is a list → join items into one comma-separated string e.g. "python,django,remote"
        # If x is anything else (None, string, etc.) → use an empty string so the row isn't skipped
        df["tags_str"] = df["tags"].apply(
            lambda x: ",".join(x) if isinstance(x, list) else ""
        )

        # Also check the "position" column (job title) for the keyword
        # .str.contains() returns True/False for each row — used to filter
        # na=False means: if the value is NaN, treat it as False (not a match)
        keyword_lower = keyword.lower()

        tag_match      = df["tags_str"].str.contains(keyword_lower, case=False, na=False)
        position_match = df["position"].str.contains(keyword_lower, case=False, na=False)

        # Keep a row if it matches in EITHER tags OR position
        df = df[tag_match | position_match]
    else:
        # If there's no tags column, search in position title only
        df = df[df["position"].str.contains(keyword.lower(), case=False, na=False)]

    print(f"Filtered for '{keyword}': {len(df)} matching jobs found.")

    # ── Step 5: Drop the helper column we no longer need ────────────────────
    # We created "tags_str" just to help with filtering — we don't need it in the output.
    if "tags_str" in df.columns:
        df = df.drop(columns=["tags_str"])

    # Reset the row index numbers so they start at 0 again after filtering
    df = df.reset_index(drop=True)

    return df
