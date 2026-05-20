# Level 2 — Cohort Analysis 📊

> **Python level:** Intermediate | **Skills practised:** See table below

## What this project does
Loads a UK retail dataset, cleans it, and answers:
*"Of customers who first bought in Month X, what percentage came back in later months?"*
Produces a retention matrix CSV and a colour-coded heatmap.

## Level 2 skills you will practise

| Skill | Where it appears |
|---|---|
| GroupBy Operations | `groupby('Customer ID')['InvoiceMonth'].min()` in cohort_engine.py |
| Merge & Join | `df.merge(first_purchase, on='Customer ID', how='left')` |
| Sorting and Ranking | `sort_values()` on top cohorts |
| Pivot Tables | `pivot_table(index='CohortMonth', columns='CohortIndex')` |
| Datetime Manipulation | `dt.to_period('M')`, period subtraction for CohortIndex |
| Exploratory Analysis | Summary stats printed in main.py before modelling |
| Statistical Visualizations | Heatmap with colour scale in visualiser.py |
| Data Validation | Removing cancellations, missing IDs, negative quantities |

## How to run

```bash
pip install -r requirements.txt
python3 main.py
```

> **Optional:** Download the real dataset from https://archive.ics.uci.edu/dataset/502/online+retail+ii  
> and place `online_retail_II.xlsx` inside the `data/` folder.  
> Without it the project auto-generates sample data so you can still run it.

## Output
```
output/
├── retention_matrix.csv   ← percentage table (cohorts × months)
└── cohort_heatmap.png     ← colour-coded retention heatmap
```
