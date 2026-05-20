# Level 1 — Remote Job Scraper 🔍

> **Python level:** Beginner | **Skills practised:** See table below

## What this project does
Hits the free [RemoteOK API](https://remoteok.com/api), downloads live remote job listings,
cleans the raw data, filters by a keyword you choose, saves a tidy CSV, and draws a bar chart
of the top 10 hiring companies — all from one command.

## Level 1 skills you will practise

| Skill | Where it appears |
|---|---|
| Python Syntax & Variables | Every file — reading the keyword, storing counts |
| Lists & Dictionaries | JSON from the API is a list of dicts → DataFrame |
| Loops & Functions | `apply()` in cleaner.py loops over every row |
| Reading CSVs | Output written with `to_csv()`, readable with `read_csv()` |
| Selecting Rows & Columns | `df[columns_we_want]` in cleaner.py |
| Filtering Data | `.str.contains()` to match keyword in tags/title |
| Handling Missing Values | `pd.to_numeric(..., errors='coerce').fillna(0)` |
| Basic Visualizations | Horizontal bar chart with matplotlib in visualiser.py |

## How to run

```bash
# Install dependencies
pip install -r requirements.txt

# Run with any keyword
python main.py python
python main.py data
python main.py react
```

## Output
```
output/
├── jobs_clean.csv       ← filtered & cleaned job listings
└── top_companies.png    ← bar chart of top 10 hiring companies
```
