# ============================================================
# config.py — All settings for the LTV Engine in one place
# ============================================================
# Level 3 skill covered: Pipeline Automation (config-driven pipelines).
# Instead of hard-coding values throughout the code, we store them
# all here. To change behaviour, you only edit this one file.

# ── Date range ───────────────────────────────────────────────────────────────
# The "snapshot date" is the reference point for calculating Recency.
# Set this to the last date in your dataset, or today's date for live data.
SNAPSHOT_DATE = "2011-12-10"

# ── RFM Scoring ───────────────────────────────────────────────────────────────
# We split each metric into 5 equal-sized buckets (quintiles).
# NUM_QUANTILES controls how many buckets.
NUM_QUANTILES = 5

# ── Segment Thresholds ───────────────────────────────────────────────────────
# These are the minimum R, F, M scores needed to qualify for each tier.
# Scores range from 1 (lowest) to 5 (highest).
SEGMENT_RULES = {
    "Champions"   : {"r_min": 4, "f_min": 4, "m_min": 4},
    "Loyal"       : {"r_min": 0, "f_min": 3, "m_min": 3},
    "At Risk"     : {"r_max": 2, "f_min": 3, "m_min": 0},
    "Hibernating" : {"r_max": 2, "f_max": 2, "m_min": 0},
}
# Any customer not matching the above rules will be labelled "Lost"

# ── Output paths ─────────────────────────────────────────────────────────────
OUTPUT_FOLDER  = "output"
LTV_CSV        = "customers_ltv.csv"
DASHBOARD_IMG  = "dashboard.png"

# ── Email settings (optional — only needed if you use scheduler.py) ──────────
# Use a Gmail App Password (not your real password).
# Generate one at: myaccount.google.com/apppasswords
SMTP_HOST   = "smtp.gmail.com"
SMTP_PORT   = 587
EMAIL_FROM  = "your_email@gmail.com"
EMAIL_TO    = ["recipient@example.com"]
EMAIL_PASS  = ""   # leave blank if not using email
