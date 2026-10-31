# NovaCart — E-Commerce Business Intelligence & Customer Analytics

An end-to-end data analytics portfolio project demonstrating how Python, MySQL, and Power BI can transform transactional data into validated KPIs, business insights, and executive reporting.

> **Project type:** Data Analytics & Business Intelligence  
> **Tools:** Python · Pandas · NumPy · MySQL 8.0 · SQL · Power BI · Git  
> **Reporting period:** 2024–2025  
> **Data:** Synthetic data generated for educational and portfolio purposes

## Project at a Glance

NovaCart simulates an e-commerce business and analyzes sales performance, profitability, customer behavior, regional performance, and product returns.

The project follows an end-to-end analytics workflow:

**Business Understanding → Data Generation → Data Quality → Data Cleaning → EDA → Statistical Analysis → SQL → Power BI → Business Insights**

## Verified Project Results

| KPI | Result |
|---|---:|
| Orders analyzed | 50,000 |
| Customers | 5,000 |
| Products | 200 |
| Returned orders | 4,000 |
| Net revenue | ₹4,800,360,544.59 |
| Total profit | ₹598,903,173.30 |
| Profit margin | 12.48% |
| Average order value | ₹96,007.21 |
| Return rate | 8.00% |

The financial KPIs were verified using Python, and the Python-to-MySQL reconciliation confirmed that all 50,000 order IDs and the five compared financial metrics matched exactly.

## Key Business Findings

- **Revenue growth:** Net revenue increased by approximately 82.32% from 2024 to 2025.
- **Profit growth:** Total profit increased by approximately 80.71% over the same period.
- **Category performance:** Sports was the highest-performing category by revenue and profit in the analyzed data.
- **Regional performance:** The East region recorded the highest revenue.
- **Returns:** The overall return rate was 8.00%, with Size Issue identified as the most common return reason overall.

These findings describe the generated dataset and do not establish the causes of observed patterns.

## Executive Dashboard

The Power BI dashboard presents an executive overview of revenue trends, category performance, regional revenue, profitability, payment methods, and product returns.

![NovaCart Executive Dashboard](Dashboard_Screenshots/NovaCart_Executive_Dashboard.png)

**Dashboard screenshot:** [View the full-size dashboard image](https://github.com/bharath-bathini/NovaCart-Ecommerce-Analytics/blob/main/Dashboard_Screenshots/NovaCart_Executive_Dashboard.png).

**Interactive dashboard:** Open `PowerBI/NovaCart_Executive_Overview.pbix` in Power BI Desktop.

## Key Skills Demonstrated

- **Python:** Data generation, data cleaning, feature engineering, exploratory data analysis, and statistical analysis.
- **SQL and MySQL:** Data retrieval, filtering, joins, aggregations, business analysis, and KPI validation.
- **Power BI:** Executive dashboard development, KPI cards, business performance visualizations, and interactive date filtering.
- **Data Validation:** Data quality checks and Python-to-MySQL financial reconciliation.
- **Business Intelligence:** Revenue and profitability analysis, category performance, regional analysis, and product return analysis.
- **Documentation and Version Control:** Project documentation, Git, and GitHub.

## Project Structure

```text
NovaCart-Ecommerce-Analytics/
│
├── Python/
│   ├── generate_dataset.py
│   ├── data_quality.py
│   ├── data_cleaning.py
│   ├── eda.py
│   ├── statistical_analysis.py
│   ├── compare_python_mysql.py
│   └── final_kpi_verification.py
│
├── SQL/
│   ├── 01_database_setup.sql
│   ├── 02_basic_queries.sql
│   ├── 03_aggregation_groupby.sql
│   ├── 04_joins.sql
│   ├── 05_business_analysis.sql
│   ├── 06_advanced_sql.sql
│   └── 07_validation_and_kpis.sql
│
├── PowerBI/
│   └── NovaCart_Executive_Overview.pbix
│
├── Dashboard_Screenshots/
│   └── NovaCart_Executive_Dashboard.png
│
├── Business_Understanding/
│   ├── NovaCart_Business_Understanding.docx
│   ├── NovaCart_Day_1_Business_Understanding_DETAILED.docx
│   ├── NovaCart_Day_2_Dataset_Creation_and_Data_Understanding_DETAILED.docx
│   ├── NovaCart_Day_3_Data_Quality_Assessment_DETAILED.docx
│   ├── NovaCart_Day_4_Data_Cleaning_and_Transformation_DETAILED.docx
│   ├── NovaCart_Day_5_Feature_Engineering_and_EDA_DETAILED.docx
│   ├── NovaCart_Day_6_Statistical_and_Business_Analysis_DETAILED.docx
│   ├── NovaCart_Day_7_SQL_Analysis_DETAILED.docx
│   └── NovaCart_Day_8_Dashboard_Validation_and_Business_Insights.docx
│
├── Insights/
│   ├── NovaCart_Business_Insights.md
│   └── Python_MySQL_Financial_Reconciliation.md
│
├── requirements.txt
└── README.md
```

*Note: The project structure above highlights the main deliverables. Additional files, datasets, and generated outputs may also exist in the repository.*

## How to Explore the Project

1. **Review the business problem:** Read the documentation in `Business_Understanding/`.
2. **Explore the Python workflow:** Review the scripts in `Python/` to understand dataset generation, cleaning, analysis, and validation.
3. **Explore the SQL analysis:** Review the scripts in `SQL/` to understand database queries and business KPI calculations.
4. **Review the business findings:** Open the reports in `Insights/`.
5. **Explore the dashboard:** Open `PowerBI/NovaCart_Executive_Overview.pbix` in Power BI Desktop.

Python dependencies are listed in `requirements.txt`.

## Important Data Disclaimer

All datasets and results in this project are synthetic. They are not actual NovaCart company transactions or real customer records. The findings demonstrate analytical techniques and should not be interpreted as real-world business evidence.