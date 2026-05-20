# ============================================================
# scraper.py — Fetches remote job data from the RemoteOK API
# ============================================================
# Level 1 skill covered: Reading data from the internet (API),
# working with JSON (which becomes a list of dictionaries),
# and loading it into pandas as a DataFrame.

import requests       # used to make HTTP requests (like visiting a website in code)
import pandas as pd   # pandas is the main tool for working with tabular data

def fetch_jobs():
    """
    Hits the RemoteOK public API and returns a pandas DataFrame.
    No API key needed — just a User-Agent header to identify our app.
    """

    # The URL of the RemoteOK API — returns a list of remote job postings as JSON
    url = "https://remoteok.com/api"

    # We add a User-Agent header so the server knows who is asking.
    # Without it the server returns a 403 (forbidden) error.
    headers = {"User-Agent": "twp-python-cookbook/1.0"}

    print("Connecting to RemoteOK API...")

    # requests.get() sends a GET request — like opening a URL in a browser.
    # timeout=15 means: if the server doesn't reply in 15 seconds, stop waiting.
    response = requests.get(url, headers=headers, timeout=15)

    # response.status_code tells us if the request worked.
    # 200 means OK, 403 means forbidden, 500 means server error, etc.
    if response.status_code != 200:
        raise Exception(f"API returned status code {response.status_code}. Expected 200.")

    # .json() converts the raw response text into a Python list/dict
    raw_data = response.json()

    # The first item in the list is metadata (API info), not a job.
    # So we skip it with [1:] — Python slice notation meaning "from index 1 onwards"
    jobs_list = raw_data[1:]

    print(f"Fetched {len(jobs_list)} job postings from the API.")

    # pd.DataFrame() turns a list of dictionaries into a table (rows = jobs, columns = fields)
    df = pd.DataFrame(jobs_list)

    return df
