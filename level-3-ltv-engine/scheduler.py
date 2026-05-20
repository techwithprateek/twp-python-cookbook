# ============================================================
# scheduler.py — Runs the LTV pipeline on a weekly schedule
# ============================================================
# Level 3 skill covered: Pipeline Automation.
# Instead of running main.py manually each time, this script
# keeps running in the background and fires the pipeline
# automatically every week (Monday at 08:00 by default).
#
# Run with:  python3 scheduler.py
# Stop with: Ctrl+C

import schedule   # lightweight job scheduler (pip install schedule)
import time       # time.sleep() pauses the loop between checks
import sys
import os

# Add the project root to the path so our pipeline imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the full pipeline from main.py — we just call main() on schedule
from main import main


def run_pipeline():
    """
    Wrapper around main() that catches any errors so a single failure
    doesn't kill the scheduler — it will try again next week.
    """
    print("\n⏰  Scheduled run starting...")
    try:
        main()
        print("⏰  Scheduled run complete.\n")
    except Exception as e:
        # Print the error but keep the scheduler alive
        print(f"⚠  Pipeline failed this run: {e}")
        print("   Will retry next scheduled time.\n")


# ── Schedule the job ─────────────────────────────────────────────────────────
# schedule.every().monday.at("08:00") means: run every Monday at 8am.
# You can change this to:
#   schedule.every().day.at("06:00")   — every day at 6am
#   schedule.every(3).hours            — every 3 hours
#   schedule.every(1).minutes          — every minute (useful for testing)
schedule.every().monday.at("08:00").do(run_pipeline)

print("🗓  LTV Engine Scheduler started.")
print("   Pipeline will run every Monday at 08:00.")
print("   Press Ctrl+C to stop.\n")

# ── Also run immediately on startup ──────────────────────────────────────────
# This lets you verify everything works the first time you start the scheduler.
print("▶  Running pipeline now (first-time startup run)...")
run_pipeline()

# ── Keep the scheduler alive ─────────────────────────────────────────────────
# This loop runs forever, waking up every 60 seconds to check if a job is due.
# schedule.run_pending() looks at all registered jobs and runs any whose time has arrived.
# "Pending" means "scheduled but not yet run since it was last due".
# time.sleep(60) pauses the script for 60 seconds before checking again.
# Without this loop the script would exit immediately — we must keep it running.
while True:
    schedule.run_pending()
    time.sleep(60)   # check every 60 seconds — no need to check more often
