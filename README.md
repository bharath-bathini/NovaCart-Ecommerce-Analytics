# NovaCart — E-Commerce Business Intelligence & Customer Analytics

## 1. Project Overview

NovaCart is an end-to-end e-commerce analytics portfolio project that investigates sales performance, product profitability, customer purchasing behavior, regional performance, and product returns.

The project demonstrates a complete analytics workflow using Python, MySQL, and Power BI, transforming synthetic transactional data into validated KPIs, business findings, and interactive visualizations.

**Project type:** Data Analytics / Business Intelligence  
**Tools:** Python, Pandas, NumPy, MySQL 8.0, SQL, Power BI  
**Data:** Synthetically generated for educational and portfolio purposes

> All data and results in this project are synthetic. They do not represent actual company transactions or real customer behavior.

## 2. Business Objectives

The main objectives are to:

- Analyze revenue and profit trends over time.
- Identify high-performing and loss-making products.
- Compare revenue and profitability across product categories.
- Evaluate regional sales performance.
- Understand customer purchasing behavior and historical customer value.
- Measure product return rates and identify common return reasons.
- Validate data quality and business KPIs.
- Communicate findings through an interactive Power BI dashboard.

## 3. Tools and Technologies

| Technology | Purpose |
|---|---|
| Python | Dataset generation, cleaning, feature engineering, and analysis |
| Pandas | Data manipulation and analysis |
| NumPy | Numerical operations and statistical calculations |
| MySQL 8.0 | Relational database and analytical queries |
| SQL | Filtering, aggregation, joins, CTEs, subqueries, window functions, and KPI validation |
| Power BI | Interactive dashboards and business reporting |
| DAX | Dashboard measures and KPI calculations |
| Visual Studio Code | Development environment |
| Git and GitHub | Version control and portfolio publishing |

## 4. Dataset Overview

The project uses four synthetically generated datasets.

| Dataset | Records | Description |
|---|---:|---|
| Customers | 5,000 | Customer demographics, location, and signup information |
| Products | 200 | Product names, categories, selling prices, and costs |
| Orders | 50,000 | Order transactions, quantities, discounts, and analytical measures |
| Returns | 4,000 | Returned orders, return dates, and return reasons |

The data was generated using Python and subsequently processed, validated, and prepared for analysis.

The datasets are designed to demonstrate analytical methods rather than reproduce a real business's performance.

## 5. Business Questions

The project investigates questions such as:

### Sales and Profitability
- How much revenue and profit does the business generate?
- How do revenue and profit change over time?
- Which product categories generate the highest revenue and profit?
- Which products generate the highest revenue?
- Which products have negative total profit?
- How does profit margin change as revenue grows?

### Customer and Regional Performance
- Which customers generate the highest historical revenue?
- Which regions contribute the most revenue?
- How do category results differ across regions?
- Which payment methods are used most frequently?

### Product Returns
- What percentage of orders are returned?
- What are the most common return reasons?
- Which product categories have higher return rates?
- Which products may require further investigation because of their return patterns?

## 6. Project Workflow

The project was completed in stages.

### Day 1 — Business Understanding
Defined the analytical objectives, business problem, and key questions.

### Day 2 — Dataset Generation
Generated synthetic customer, product, order, and return datasets using Python.

### Day 3 — Data Quality Assessment
Examined dataset structures, missing values, duplicate records, and return-date validity.

### Day 4 — Data Cleaning and Validation
Standardized data values and checked important business rules, including dates, quantities, discounts, and shipping costs.

### Day 5 — Feature Engineering and Exploratory Data Analysis
Created analytical features and examined sales, profitability, and return patterns.

### Day 6 — Statistical and Business Analysis
Investigated descriptive statistics, variability, outliers, and correlations.

### Day 7 — SQL Analytics
Developed and executed SQL queries for aggregation, joins, business analysis, advanced querying, and KPI validation using MySQL 8.0.

### Day 8 — Power BI Dashboard and Business Insights
Developed the executive dashboard, reviewed KPI consistency, and documented business findings and recommendations.

### Day 9 — Project Documentation and Finalization
Organized project documentation, prepared the main README, and reviewed repository files for portfolio readiness.

## 7. Key Performance Indicators

The completed Python analysis reported the following results.

## Executive Business KPIs

The NovaCart synthetic e-commerce dataset contains 50,000 unique orders, 5,000 customers, 200 products, and 4,000 returned orders.

| KPI | Verified Result |
|---|---:|
| Total Orders | 50,000 |
| Net Revenue | ₹4,800,360,544.59 |
| Total Profit | ₹598,903,173.30 |
| Overall Profit Margin | 12.48% |
| Average Order Value | ₹96,007.21 |
| Returned Orders | 4,000 |
| Return Rate | 8.00% |

### Year-over-Year Performance

| Metric | 2024 | 2025 | Growth |
|---|---:|---:|---:|
| Net Revenue | ₹1,700,350,305.05 | ₹3,100,010,290.81 | 82.32% |
| Total Profit | ₹213,353,642.79 | ₹385,549,560.50 | 80.71% |
| Profit Margin | 12.55% | 12.44% | −0.11 percentage points |
| Total Orders | 17,763 | 32,237 | 81.49% |

**Key finding:** Revenue and profit grew significantly in 2025, while overall profit margin decreased slightly. Further analysis of discounts, costs, and category-level profitability may help explain this change.

*Note: All figures are derived from a synthetic dataset created for portfolio and analytical demonstration purposes.*

These figures are calculated from the synthetic datasets. They should be interpreted within the context of this portfolio project, not as actual company results. The dashboard displays rounded values (for example, revenue as 4.80bn and profit as 598.90M); the detailed figures above retain the precision recorded in this README. Before publishing, refresh the report from the final source data and confirm that the underlying KPI measures agree, allowing for display rounding.

## 8. Key Business Insights

The completed analysis identified the following patterns in the generated data.

### Revenue and Profit Growth
- Revenue increased by approximately 82.32% from 2024 to 2025.
- Profit increased by approximately 80.71%.
- Profit margin decreased slightly, from 12.55% in 2024 to 12.44% in 2025.

This suggests that revenue and profit growth should be evaluated alongside profitability.

### Product Category Performance
The Sports category recorded the highest revenue and profit among the analyzed categories.

- Revenue: approximately ₹107.51 crore.
- Profit: approximately ₹14.69 crore.
- Profit margin: approximately 13.66%.
- Return rate: approximately 8.27%.

### Regional and Payment Performance
- The East region recorded the highest revenue.
- Net Banking was the most-used payment method.

### Product Returns
- The overall return rate was 8.00%.
- Size Issue was the most common return reason overall.
- Damaged Product was the most common return reason within the Sports category.

These results identify patterns worth investigating. They do not establish why customers returned products or why financial measures changed.

## 9. Business Recommendations

Based on the observed patterns, the following actions are recommended for further investigation.

1. **Investigate damaged returns:** Identify Sports products with high damaged-product return counts.
2. **Review product handling:** Examine packaging, shipping, and product quality as possible contributors to damaged returns.
3. **Investigate size-related returns:** Analyze size-related returns by product and subcategory.
4. **Monitor profitability:** Track profit margin alongside revenue and total profit.
5. **Evaluate regional performance:** Compare regions by category and time period.
6. **Monitor KPIs regularly:** Use the Power BI dashboard to review performance and investigate significant changes.

These recommendations are proposed investigative actions, not confirmed causes or guaranteed solutions.

## 10. SQL Scripts

The `SQL/` directory contains seven scripts.

| Script | Purpose |
|---|---|
| `01_database_setup.sql` | Database setup |
| `02_basic_queries.sql` | Basic selection, filtering, and sorting |
| `03_aggregation_groupby.sql` | Aggregate functions and grouping |
| `04_joins.sql` | Combining related datasets |
| `05_business_analysis.sql` | Sales, profit, customer, and return analysis |
| `06_advanced_sql.sql` | Advanced queries, subqueries, CTEs, date functions, and rankings |
| `07_validation_and_kpis.sql` | Data validation and KPI calculations |

Together, these scripts demonstrate relational data analysis and the use of SQL to answer business questions.

## 11. Power BI Dashboard

The Power BI executive overview is designed for a quick review of sales, profitability, order volume, and returns across the 2024–2025 reporting period. The screenshot is a static preview; use the `.pbix` file for interactive filtering.

The Power BI dashboard is saved at:

`PowerBI/NovaCart_Executive_Overview.pbix`

The executive dashboard includes KPI cards and visual analyses covering:

- Monthly revenue trends.
- Revenue and profit by product category.
- Revenue by region.
- Return rate by category.
- Payment method distribution.
- Return reasons.
- Date-based filtering.

Open the `.pbix` file in Power BI Desktop to explore the dashboard interactively.

### Executive Dashboard Preview

![NovaCart Executive Business Overview Dashboard](Dashboard_Screenshots/NovaCart_Executive_Dashboard.png)

*The dashboard summarizes revenue, profitability, order volume, product returns, regional performance, payment methods, and return reasons for 2024–2025.*

Open `PowerBI/NovaCart_Executive_Overview.pbix` in Power BI Desktop to explore the interactive dashboard.


## 12. Repository Structure

The project is organized into the following main directories.

```text
NovaCart-Ecommerce-Analytics/
├── Business_Understanding/
│   └── Day-wise project documentation
├── Data/
│   ├── raw/
│   ├── processed/
│   ├── feature_engineered/
│   ├── analysis_outputs/
│   └── eda_outputs/
├── Python/
│   ├── generate_dataset.py
│   ├── data_understanding.py
│   ├── data_quality.py
│   ├── data_cleaning.py
│   ├── check_customer_duplicates.py
│   ├── eda.py
│   └── statistical_analysis.py
├── SQL/
│   ├── 01_database_setup.sql
│   ├── 02_basic_queries.sql
│   ├── 03_aggregation_groupby.sql
│   ├── 04_joins.sql
│   ├── 05_business_analysis.sql
│   ├── 06_advanced_sql.sql
│   └── 07_validation_and_kpis.sql
├── PowerBI/
│   └── NovaCart_Executive_Overview.pbix
├── Dashboard_Screenshots/
├── Insights/
│   └── NovaCart_Business_Insights.md
└── README.md
```

This is the intended high-level structure. Confirm that the listed directories and files match the final repository before publishing. The dashboard image should be saved in `Dashboard_Screenshots/` with the exact filename `NovaCart_Executive_Dashboard.png` so the preview above renders on GitHub.

## 13. How to Run the Project

### Python Setup and Reproducibility

### Prerequisites

- Python 3.12 or a compatible Python 3 version
- pip, Python's package installer
- Visual Studio Code or another Python-compatible editor

### Install Dependencies

Clone or download the repository and open a terminal in the project root directory.

Install the required Python libraries:

```bash
python -m pip install -r requirements.txt
```

The `requirements.txt` file contains the dependencies used by the project:

- pandas
- numpy
- matplotlib
- seaborn

### Project Data Pipeline

Run the scripts from the **project root directory**, not from inside the `Python` folder, because the scripts use relative paths.

**1. Generate synthetic datasets (optional)**

```bash
python Python/generate_dataset.py
```

This script generates customer, product, order, and return datasets in `Data/raw/`. Run it only when you intentionally want to regenerate the source data.

**2. Assess data quality**

```bash
python Python/data_quality.py
```

This script checks the raw datasets before cleaning.

**3. Clean the datasets**

```bash
python Python/data_cleaning.py
```

The cleaned datasets are saved in `Data/processed/`.

**4. Perform exploratory data analysis and feature engineering**

```bash
python Python/eda.py
```

This script creates feature-engineered datasets in `Data/feature_engineered/` and analytical outputs in `Data/eda_outputs/`.

**5. Perform statistical and business analysis**

```bash
python Python/statistical_analysis.py
```

This script uses the feature-engineered datasets and saves statistical summaries in `Data/analysis_outputs/`.

### Expected Data Flow

`Data/raw/` → `Data/processed/` → `Data/feature_engineered/` → `Data/eda_outputs/` and `Data/analysis_outputs/`

### Important Notes

- Run commands from the repository root so that relative file paths resolve correctly.
- The data is synthetic and is intended for analytical demonstration and portfolio development.
- Some scripts overwrite existing CSV outputs when rerun.
- Review each script's input and output paths before changing the execution order.
- The `Data/` folders are created automatically by scripts where directory creation is implemented.

### SQL Analysis

1. Install MySQL 8.0 and open MySQL Workbench or another MySQL client.
2. Ensure the NovaCart database and its required tables are available.
3. Execute `01_database_setup.sql`.
4. Run the remaining SQL scripts in numerical order.
5. Review the returned results and investigate failed validation checks.
6. Compare the SQL results with the Python analysis and Power BI KPIs.

Check each script's database and table references before executing it in a new environment.

### Power BI Dashboard

1. Install Power BI Desktop.
2. Open `PowerBI/NovaCart_Executive_Overview.pbix`.
3. Check the data-source configuration if prompted.
4. Refresh the data if the source is available.
5. Explore the KPI cards, charts, and date filters.

## 14. Project Status

### Completed
- Business understanding and analytical planning.
- Synthetic dataset generation.
- Data quality assessment.
- Data cleaning and validation.
- Feature engineering and exploratory analysis.
- Statistical and business analysis.
- SQL analytics and KPI validation.
- Power BI executive dashboard.
- Dashboard validation and business insights.
- Main project documentation.

### Remaining Portfolio Tasks
- Complete final repository and file checks.
- Review files for sensitive information and unnecessary duplicates.
- Publish the project to GitHub.
- Prepare a concise resume description and interview explanation.

## 15. Limitations and Disclaimer

- The datasets are synthetic and do not represent real customers or company transactions.
- Findings describe the generated data and should not be generalized to a real e-commerce business.
- Correlations and descriptive patterns do not establish causation.
- Recommendations require further investigation before being used as operational decisions.
- Reported KPIs should be checked against the final versions of the source data and analytical queries.

NovaCart is an educational portfolio project intended to demonstrate data analytics, SQL, statistical analysis, and business intelligence skills.

