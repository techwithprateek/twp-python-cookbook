# Level 3 — Customer LTV Engine 🏆

> **Python level:** Advanced | **Skills practised:** See table below

## What this project does
Loads retail transaction data, cleans it, computes RFM scores (Recency, Frequency, Monetary)
for every customer, assigns them to one of five LTV tiers, produces a 4-panel dashboard,
and (optionally) sends a weekly HTML email report — all driven by a single config file.

## Level 3 skills you will practise

| Skill | Where it appears |
|---|---|
| Complex Transformations | Multi-column `agg()` to build the RFM table in rfm.py |
| Window Functions | `pd.qcut()` splits customers into 5 ranked buckets per metric |
| Pipeline Automation | Every stage is a separate module wired together in main.py, all settings in config.py |
| Data Quality Checks | `quality.py` runs assertions before analysis and stops the pipeline on failure |
| Decision-ready Insights | Segment labels + 4-panel dashboard + optional email in reporting/ |

## How to run

```bash
pip install -r requirements.txt
python3 main.py
```

> **Optional real data:** Download from https://archive.ics.uci.edu/dataset/502/online+retail+ii  
> Place `online_retail_II.xlsx` in `data/`. Without it, sample data is generated automatically.

> **Optional email:** Fill in `EMAIL_FROM`, `EMAIL_TO`, `EMAIL_PASS` in `config.py`.

## Output
```
output/
├── customers_ltv.csv   ← RFM scores + segment for every customer
└── dashboard.png       ← 4-panel: pie, bar, histogram, scatter
```

## Project structure
```
level-3-ltv-engine/
├── main.py          ← run this
├── config.py        ← all settings live here
├── pipeline/
│   ├── loader.py    ← load xlsx / csv / sample data
│   ├── cleaner.py   ← remove bad rows
│   ├── quality.py   ← automated data quality checks
│   ├── rfm.py       ← RFM computation + quintile scoring
│   └── segmenter.py ← assign Champions / Loyal / At Risk / etc.
└── reporting/
    ├── dashboard.py     ← 4-panel matplotlib dashboard
    └── email_report.py  ← HTML email with embedded chart
```
