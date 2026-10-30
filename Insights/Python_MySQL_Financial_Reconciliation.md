# NovaCart Python–MySQL Financial Reconciliation

## Objective
Verify that Python's cleaned order dataset and the MySQL export contain the same orders and financial values.

## Source files inspected
- Python source of truth: `Data/processed/orders_cleaned.csv`
- Complete MySQL export supplied for verification: `mysql_orders_reconciled(2).csv`
- Earlier partial export: `mysql_orders_financial_check.csv`
- Earlier source-check export: `mysql_orders_source_check(1).csv`

## Order coverage findings
| Export | Rows | Unique order IDs | Finding |
|---|---:|---:|---|
| Python cleaned orders | 50,000 | 50,000 | Complete |
| Earlier MySQL financial check | 45,868 | 45,868 | Partial; omitted 4,132 orders |
| MySQL source check | 10,000 | 10,000 | Partial; first 10,000 orders only |
| Reconciled MySQL export | 50,000 | 50,000 | Complete |

The earlier mismatch was caused by comparing Python's 50,000-row dataset with a 45,868-row MySQL export. The 10,000-row source-check file was also a partial export.

## Financial comparison
The complete 50,000-row MySQL reconciled export matches `Data/processed/orders_cleaned.csv` exactly for every order and each of the five financial columns.

| Metric | Python total | MySQL total | Difference |
|---|---:|---:|---:|
| Gross sales | ₹5,645,874,630.36 | ₹5,645,874,630.36 | ₹0.00 |
| Discount amount | ₹845,514,085.77 | ₹845,514,085.77 | ₹0.00 |
| Net revenue | ₹4,800,360,544.59 | ₹4,800,360,544.59 | ₹0.00 |
| Product cost | ₹4,187,946,350.20 | ₹4,187,946,350.20 | ₹0.00 |
| Profit | ₹598,903,173.30 | ₹598,903,173.30 | ₹0.00 |

## Additional inconsistency found
`Data/feature_engineered/orders_features.csv` contains 50,000 orders, but its financial totals differ from the cleaned dataset:
- Discount amount: ₹845,514,056.96
- Net revenue: ₹4,800,360,573.40
- Profit: ₹598,903,202.11

The file's financial columns should be refreshed from `orders_cleaned.csv` by `order_id` so downstream EDA and reporting use one consistent source. Do not update dashboard or README KPI values based on the stale feature-engineered totals.

## Conclusion
The provided complete MySQL export reconciles exactly to the Python cleaned dataset. The earlier 4,132-order gap and the one-paisa discrepancies were artifacts of the incomplete export used in the earlier comparison. The feature-engineered dataset is separately stale and should be regenerated/refreshed from the cleaned dataset before final publication.

## Reproducibility
Use the corrected `compare_python_mysql.py` included with this fix. Place the complete MySQL export at `Data/analysis_outputs/mysql_orders_reconciled.csv`, or pass its path using `--mysql`. The script checks duplicate IDs, coverage, row-level differences, and writes detailed and summary CSV reports.
