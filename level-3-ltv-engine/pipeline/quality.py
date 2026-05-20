# ============================================================
# pipeline/quality.py — Automated data quality checks
# ============================================================
# Level 3 skill covered: Data Quality Checks.
# Before we run any analysis, we programmatically verify
# the data meets our expectations and flag any problems.

import pandas as pd


def run_checks(df):
    """
    Runs a series of assertions against the cleaned DataFrame.
    Prints a PASS/FAIL line for each check.
    Raises a ValueError if any critical check fails so the
    pipeline stops rather than producing wrong results.
    """

    print("--- Running data quality checks ---")
    failures = []

    # ── Check 1: No duplicate Invoice + StockCode combinations ───────────────
    # Each combination should appear once. Duplicates suggest data loading errors.
    dup_count = df.duplicated(subset=["Invoice", "StockCode"]).sum()
    _report("No duplicate Invoice+StockCode rows", dup_count == 0,
            f"{dup_count} duplicates found", failures)

    # ── Check 2: Date range looks reasonable ─────────────────────────────────
    # We expect dates to be within a believable range (not 1900 or 2099).
    min_date = df["InvoiceDate"].min()
    max_date = df["InvoiceDate"].max()
    date_ok  = min_date.year >= 2000 and max_date.year <= 2030
    _report(f"Date range: {min_date.date()} to {max_date.date()}", date_ok,
            "Dates outside expected range", failures)

    # ── Check 3: All Customer IDs are numeric ─────────────────────────────────
    # Customer IDs should be numbers (e.g. 12345), not strings or NaN.
    ids_are_numeric = pd.to_numeric(df["Customer ID"], errors="coerce").notna().all()
    _report("All Customer IDs are numeric", ids_are_numeric,
            "Some Customer IDs are non-numeric", failures)

    # ── Check 4: No negative revenue ─────────────────────────────────────────
    neg_revenue = (df["TotalRevenue"] < 0).sum()
    _report("No negative TotalRevenue rows", neg_revenue == 0,
            f"{neg_revenue} rows have negative revenue", failures)

    # ── Check 5: At least 100 rows of data ───────────────────────────────────
    _report(f"At least 100 rows present ({len(df):,} rows)", len(df) >= 100,
            "Too few rows — data may be missing", failures)

    print()

    # If any critical check failed, stop the pipeline immediately
    if failures:
        raise ValueError(f"Data quality failed: {'; '.join(failures)}")


def _report(label, passed, fail_message, failures_list):
    """Helper — prints PASS or FAIL and collects failures."""
    if passed:
        print(f"  ✓ {label}")
    else:
        print(f"  ✗ {label}  ←  {fail_message}")
        failures_list.append(fail_message)
