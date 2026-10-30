# ============================================================
# NOVACART - STATISTICAL & BUSINESS ANALYSIS
# DAY 6
# ============================================================

import pandas as pd
import numpy as np

print("=" * 70)
print("NOVACART - DAY 6 STATISTICAL & BUSINESS ANALYSIS")
print("=" * 70)


# ============================================================
# LOAD FEATURE-ENGINEERED DATA
# ============================================================

customers = pd.read_csv(
    "Data/feature_engineered/customers_features.csv"
)

products = pd.read_csv(
    "Data/feature_engineered/products_features.csv"
)

orders = pd.read_csv(
    "Data/feature_engineered/orders_features.csv"
)

returns = pd.read_csv(
    "Data/feature_engineered/returns_features.csv"
)


# ============================================================
# CONVERT DATE COLUMNS
# ============================================================

customers["signup_date"] = pd.to_datetime(
    customers["signup_date"]
)

orders["order_date"] = pd.to_datetime(
    orders["order_date"]
)

returns["return_date"] = pd.to_datetime(
    returns["return_date"]
)


# ============================================================
# DATASET OVERVIEW
# ============================================================

print("\nDATASET SHAPES")
print("-" * 70)

print("Customers:", customers.shape)
print("Products :", products.shape)
print("Orders   :", orders.shape)
print("Returns  :", returns.shape)


print("\nDATE COLUMNS")
print("-" * 70)

print("Customer signup date:",
      customers["signup_date"].dtype)

print("Order date:",
      orders["order_date"].dtype)

print("Return date:",
      returns["return_date"].dtype)


print("\nDAY 6 STEP 1 COMPLETED")
print("=" * 70)

# ============================================================
# DAY 6 STEP 2 - DESCRIPTIVE STATISTICS
# ============================================================

print("\nDESCRIPTIVE STATISTICS")
print("-" * 70)

numeric_columns = [
    "quantity",
    "discount",
    "gross_sales",
    "discount_amount",
    "net_revenue",
    "product_cost",
    "shipping_cost",
    "profit",
    "profit_margin"
]

statistics_summary = orders[numeric_columns].describe().T

print(statistics_summary)

print("\nDAY 6 STEP 2 COMPLETED")
print("=" * 70)

# ============================================================
# DAY 6 STEP 3 - MEAN VS MEDIAN
# ============================================================

print("\nMEAN VS MEDIAN ANALYSIS")
print("-" * 70)

comparison_columns = [
    "quantity",
    "discount",
    "gross_sales",
    "net_revenue",
    "product_cost",
    "shipping_cost",
    "profit",
    "profit_margin"
]

mean_median = pd.DataFrame({
    "Mean": orders[comparison_columns].mean(),
    "Median": orders[comparison_columns].median()
})

mean_median["Difference"] = (
    mean_median["Mean"] - mean_median["Median"]
)

print(mean_median)

print("\nDAY 6 STEP 3 COMPLETED")
print("=" * 70)

# ============================================================
# DAY 6 STEP 4 - VARIABILITY AND STANDARD DEVIATION
# ============================================================

print("\nVARIABILITY AND STANDARD DEVIATION")
print("-" * 70)

variability_columns = [
    "quantity",
    "discount",
    "gross_sales",
    "net_revenue",
    "product_cost",
    "shipping_cost",
    "profit",
    "profit_margin"
]

variability_summary = pd.DataFrame({
    "Mean": orders[variability_columns].mean(),
    "Std_Dev": orders[variability_columns].std(),
    "Min": orders[variability_columns].min(),
    "Q1": orders[variability_columns].quantile(0.25),
    "Median": orders[variability_columns].median(),
    "Q3": orders[variability_columns].quantile(0.75),
    "Max": orders[variability_columns].max()
})

print(variability_summary)

print("\nDAY 6 STEP 4 COMPLETED")
print("=" * 70)

# ============================================================
# DAY 6 STEP 5 - IQR AND OUTLIER ANALYSIS
# ============================================================

print("\nIQR AND OUTLIER ANALYSIS")
print("-" * 70)

outlier_columns = [
    "gross_sales",
    "net_revenue",
    "product_cost",
    "profit",
    "profit_margin"
]

outlier_summary = []

for column in outlier_columns:

    Q1 = orders[column].quantile(0.25)
    Q3 = orders[column].quantile(0.75)

    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    outliers = orders[
        (orders[column] < lower_bound) |
        (orders[column] > upper_bound)
    ]

    outlier_summary.append({
        "Column": column,
        "Q1": Q1,
        "Q3": Q3,
        "IQR": IQR,
        "Lower_Bound": lower_bound,
        "Upper_Bound": upper_bound,
        "Outlier_Count": len(outliers),
        "Outlier_Percentage": len(outliers) / len(orders) * 100
    })

outlier_summary = pd.DataFrame(outlier_summary)

print(outlier_summary)

print("\nDAY 6 STEP 5 COMPLETED")
print("=" * 70)

# ============================================================
# DAY 6 STEP 6 - CORRELATION ANALYSIS
# ============================================================

print("\nCORRELATION ANALYSIS")
print("-" * 70)

correlation_columns = [
    "quantity",
    "discount",
    "gross_sales",
    "discount_amount",
    "net_revenue",
    "product_cost",
    "shipping_cost",
    "selling_price",
    "profit",
    "profit_margin"
]

correlation_matrix = orders[correlation_columns].corr()

print(correlation_matrix)

print("\nCORRELATION WITH PROFIT")
print("-" * 70)

profit_correlation = (
    correlation_matrix["profit"]
    .sort_values(ascending=False)
)

print(profit_correlation)

print("\nDAY 6 STEP 6 COMPLETED")
print("=" * 70)

## ============================================================
# DAY 6 STEP 7 - BUSINESS GROUP COMPARISONS
# ============================================================

print("\nBUSINESS GROUP COMPARISONS")
print("-" * 70)

# ------------------------------------------------------------
# MERGE PRODUCT INFORMATION
# ------------------------------------------------------------

orders_with_product = orders.merge(
    products[
        [
            "product_id",
            "category",
            "sub_category"
        ]
    ],
    on="product_id",
    how="left"
)

print("\nOrders + Product Information Shape:")
print(orders_with_product.shape)

# ------------------------------------------------------------
# CATEGORY ANALYSIS
# ------------------------------------------------------------
# CATEGORY ANALYSIS

category_analysis = orders_with_product.groupby("category").agg(
    Orders=("order_id", "count"),
    Revenue=("net_revenue", "sum"),
    Profit=("profit", "sum"),
    Average_Profit=("profit", "mean")
)

category_analysis["Profit_Margin"] = (
    category_analysis["Profit"]
    / category_analysis["Revenue"]
    * 100
)

category_analysis = category_analysis.sort_values(
    "Profit",
    ascending=False
)

print("\nCATEGORY ANALYSIS")
print(category_analysis)
# ------------------------------------------------------------
# MERGE CUSTOMER INFORMATION
# ------------------------------------------------------------

orders_with_customer = orders_with_product.merge(
    customers[
        [
            "customer_id",
            "gender",
            "age",
            "age_group",
            "city",
            "state",
            "region"
        ]
    ],
    on="customer_id",
    how="left"
)

# ------------------------------------------------------------
# REGION ANALYSIS
# ------------------------------------------------------------

# REGION ANALYSIS

region_analysis = orders_with_customer.groupby("region").agg(
    Orders=("order_id", "count"),
    Revenue=("net_revenue", "sum"),
    Profit=("profit", "sum"),
    Average_Profit=("profit", "mean")
)

region_analysis["Profit_Margin"] = (
    region_analysis["Profit"]
    / region_analysis["Revenue"]
    * 100
)

region_analysis = region_analysis.sort_values(
    "Profit",
    ascending=False
)

print("\nREGION ANALYSIS")
print(region_analysis)
# ------------------------------------------------------------
# AGE GROUP ANALYSIS
# ------------------------------------------------------------

# AGE GROUP ANALYSIS

age_group_analysis = orders_with_customer.groupby("age_group").agg(
    Orders=("order_id", "count"),
    Revenue=("net_revenue", "sum"),
    Profit=("profit", "sum"),
    Average_Profit=("profit", "mean")
)

age_group_analysis["Profit_Margin"] = (
    age_group_analysis["Profit"]
    / age_group_analysis["Revenue"]
    * 100
)

age_group_analysis = age_group_analysis.sort_values(
    "Profit",
    ascending=False
)

print("\nAGE GROUP ANALYSIS")
print(age_group_analysis)
# ============================================================
# DAY 6 STEP 8 - LOSS-MAKING ORDER ANALYSIS
# ============================================================

print("\nLOSS-MAKING ORDER ANALYSIS")
print("-" * 70)

loss_orders = orders_with_customer[
    orders_with_customer["profit"] < 0
].copy()

print("\nLoss-Making Orders:", len(loss_orders))

print(
    "Loss-Making Order Percentage:",
    round(len(loss_orders) / len(orders) * 100, 2),
    "%"
)

print(
    "Total Revenue from Loss-Making Orders:",
    loss_orders["net_revenue"].sum()
)

print(
    "Total Loss:",
    loss_orders["profit"].sum()
)

print(
    "Average Loss per Loss-Making Order:",
    loss_orders["profit"].mean()
)

print("\nLOSS ORDERS BY CATEGORY")
print("-" * 70)

loss_by_category = loss_orders.groupby("category").agg(
    Loss_Orders=("order_id", "count"),
    Total_Loss=("profit", "sum"),
    Average_Loss=("profit", "mean"),
    Average_Discount=("discount", "mean"),
    Average_Quantity=("quantity", "mean")
).sort_values("Total_Loss")

print(loss_by_category)

print("\nLOSS ORDERS BY ORDER STATUS")
print("-" * 70)

loss_by_status = loss_orders.groupby("order_status").agg(
    Loss_Orders=("order_id", "count"),
    Total_Loss=("profit", "sum"),
    Average_Loss=("profit", "mean")
).sort_values("Total_Loss")

print(loss_by_status)

print("\nLOSS ORDERS BY DISCOUNT CATEGORY")
print("-" * 70)

loss_by_discount = loss_orders.groupby("discount_category").agg(
    Loss_Orders=("order_id", "count"),
    Total_Loss=("profit", "sum"),
    Average_Loss=("profit", "mean")
).sort_values("Total_Loss")

print(loss_by_discount)

print("\nLOSS-MAKING ORDER SUMMARY")
print("-" * 70)

print(
    "Average Quantity:",
    round(loss_orders["quantity"].mean(), 2)
)

print(
    "Average Discount:",
    round(loss_orders["discount"].mean() * 100, 2),
    "%"
)

print(
    "Average Shipping Cost:",
    round(loss_orders["shipping_cost"].mean(), 2)
)

print(
    "Average Net Revenue:",
    round(loss_orders["net_revenue"].mean(), 2)
)

print("\nDAY 6 STEP 8 COMPLETED")
print("=" * 70)

# ============================================================
# DAY 6 STEP 9 - DISCOUNT STRATEGY ANALYSIS
# ============================================================

print("\nDISCOUNT STRATEGY ANALYSIS")
print("-" * 70)

discount_analysis = orders_with_customer.groupby(
    "discount_category"
).agg(
    Orders=("order_id", "count"),
    Revenue=("net_revenue", "sum"),
    Total_Profit=("profit", "sum"),
    Average_Profit=("profit", "mean"),
    Average_Discount=("discount", "mean"),
    Average_Net_Revenue=("net_revenue", "mean")
)

# Calculate profit margin
discount_analysis["Profit_Margin"] = (
    discount_analysis["Total_Profit"]
    / discount_analysis["Revenue"]
    * 100
)

# Calculate loss-making orders
loss_counts = orders_with_customer[
    orders_with_customer["profit"] < 0
].groupby("discount_category").size()

discount_analysis["Loss_Making_Orders"] = (
    loss_counts.reindex(
        discount_analysis.index,
        fill_value=0
    )
)

# Calculate percentage of orders that are loss-making
discount_analysis["Loss_Order_Percentage"] = (
    discount_analysis["Loss_Making_Orders"]
    / discount_analysis["Orders"]
    * 100
)

# Arrange categories in logical business order
discount_order = [
    "No Discount",
    "Low Discount",
    "Medium Discount",
    "High Discount"
]

discount_analysis = discount_analysis.reindex(
    discount_order
)

print("\nDISCOUNT ANALYSIS")
print(discount_analysis)

print("\nDISCOUNT ANALYSIS SUMMARY")
print("-" * 70)

for category in discount_analysis.index:
    row = discount_analysis.loc[category]

    print(f"\n{category}")
    print("Orders:", int(row["Orders"]))
    print("Revenue:", round(row["Revenue"], 2))
    print("Total Profit:", round(row["Total_Profit"], 2))
    print("Average Profit:", round(row["Average_Profit"], 2))
    print(
        "Average Discount:",
        round(row["Average_Discount"] * 100, 2),
        "%"
    )
    print(
        "Profit Margin:",
        round(row["Profit_Margin"], 2),
        "%"
    )
    print(
        "Loss-Making Orders:",
        int(row["Loss_Making_Orders"])
    )
    print(
        "Loss Order Percentage:",
        round(row["Loss_Order_Percentage"], 2),
        "%"
    )

print("\nDAY 6 STEP 9 COMPLETED")
print("=" * 70)

# ============================================================
# DAY 6 STEP 10 - RETURN ANALYSIS
# ============================================================

print("\nRETURN ANALYSIS")
print("-" * 70)

# ------------------------------------------------------------
# 1. Identify returned orders
# ------------------------------------------------------------

returned_order_ids = set(returns["order_id"])

orders_with_customer["is_returned"] = (
    orders_with_customer["order_id"].isin(returned_order_ids)
)

print("\nRETURNED VS NON-RETURNED ORDERS")
print("-" * 70)

return_summary = orders_with_customer.groupby(
    "is_returned"
).agg(
    Orders=("order_id", "count"),
    Revenue=("net_revenue", "sum"),
    Total_Profit=("profit", "sum"),
    Average_Profit=("profit", "mean"),
    Average_Net_Revenue=("net_revenue", "mean")
)

return_summary["Order_Percentage"] = (
    return_summary["Orders"]
    / len(orders_with_customer)
    * 100
)

print(return_summary)


# ------------------------------------------------------------
# 2. Overall return rate
# ------------------------------------------------------------

total_orders = len(orders_with_customer)

returned_orders = orders_with_customer[
    orders_with_customer["is_returned"]
]

return_rate = (
    len(returned_orders)
    / total_orders
    * 100
)

print("\nOVERALL RETURN RATE")
print("-" * 70)

print("Total Orders:", total_orders)
print("Returned Orders:", len(returned_orders))
print("Return Rate:", round(return_rate, 2), "%")


# ------------------------------------------------------------
# 3. Return reasons
# ------------------------------------------------------------

print("\nRETURN REASONS")
print("-" * 70)

return_reason_analysis = returns.groupby(
    "return_reason"
).agg(
    Returns=("return_id", "count")
).sort_values(
    "Returns",
    ascending=False
)

return_reason_analysis["Return_Percentage"] = (
    return_reason_analysis["Returns"]
    / len(returns)
    * 100
)

print(return_reason_analysis)


# ------------------------------------------------------------
# 4. Return rate by category
# ------------------------------------------------------------

print("\nRETURN RATE BY CATEGORY")
print("-" * 70)

category_return_analysis = orders_with_customer.groupby(
    "category"
).agg(
    Total_Orders=("order_id", "count"),
    Returned_Orders=("is_returned", "sum")
)

category_return_analysis["Return_Rate"] = (
    category_return_analysis["Returned_Orders"]
    / category_return_analysis["Total_Orders"]
    * 100
)

category_return_analysis = category_return_analysis.sort_values(
    "Return_Rate",
    ascending=False
)

print(category_return_analysis)


# ------------------------------------------------------------
# 5. Return rate by region
# ------------------------------------------------------------

print("\nRETURN RATE BY REGION")
print("-" * 70)

region_return_analysis = orders_with_customer.groupby(
    "region"
).agg(
    Total_Orders=("order_id", "count"),
    Returned_Orders=("is_returned", "sum")
)

region_return_analysis["Return_Rate"] = (
    region_return_analysis["Returned_Orders"]
    / region_return_analysis["Total_Orders"]
    * 100
)

region_return_analysis = region_return_analysis.sort_values(
    "Return_Rate",
    ascending=False
)

print(region_return_analysis)


# ------------------------------------------------------------
# 6. Return delay analysis
# ------------------------------------------------------------

print("\nRETURN DELAY ANALYSIS")
print("-" * 70)

returns_with_orders = returns.merge(
    orders[[
        "order_id",
        "order_date"
    ]],
    on="order_id",
    how="left"
)

returns_with_orders["return_delay_days"] = (
    returns_with_orders["return_date"]
    - returns_with_orders["order_date"]
).dt.days

print(
    returns_with_orders["return_delay_days"].describe()
)


# ------------------------------------------------------------
# 7. Returned vs non-returned profitability
# ------------------------------------------------------------

print("\nRETURNED VS NON-RETURNED PROFITABILITY")
print("-" * 70)

profitability_comparison = orders_with_customer.groupby(
    "is_returned"
).agg(
    Orders=("order_id", "count"),
    Average_Revenue=("net_revenue", "mean"),
    Average_Profit=("profit", "mean"),
    Total_Profit=("profit", "sum"),
    Average_Profit_Margin=("profit_margin", "mean")
)

print(profitability_comparison)


print("\nDAY 6 STEP 10 COMPLETED")
print("=" * 70)

# ============================================================
# DAY 6 STEP 11 - ANSWER NOVACART BUSINESS QUESTIONS
# ============================================================

print("\nNOVACART BUSINESS QUESTIONS")
print("=" * 70)


# ------------------------------------------------------------
# BUSINESS QUESTION 1
# What is the total revenue?
# ------------------------------------------------------------

total_revenue = orders["net_revenue"].sum()

print("\n1. TOTAL NET REVENUE")
print("-" * 70)
print("Total Net Revenue:", round(total_revenue, 2))


# ------------------------------------------------------------
# BUSINESS QUESTION 2
# What is the total profit?
# ------------------------------------------------------------

total_profit = orders["profit"].sum()

print("\n2. TOTAL PROFIT")
print("-" * 70)
print("Total Profit:", round(total_profit, 2))


# ------------------------------------------------------------
# BUSINESS QUESTION 3
# What is the overall profit margin?
# ------------------------------------------------------------

overall_profit_margin = (
    total_profit
    / total_revenue
    * 100
)

print("\n3. OVERALL PROFIT MARGIN")
print("-" * 70)
print(
    "Overall Profit Margin:",
    round(overall_profit_margin, 2),
    "%"
)


# ------------------------------------------------------------
# BUSINESS QUESTION 4
# What is the average order value?
# ------------------------------------------------------------

aov = (
    total_revenue
    / orders["order_id"].nunique()
)

print("\n4. AVERAGE ORDER VALUE")
print("-" * 70)
print("Average Order Value:", round(aov, 2))


# ------------------------------------------------------------
# BUSINESS QUESTION 5
# Which category generates the highest revenue?
# ------------------------------------------------------------

category_revenue = orders_with_product.groupby(
    "category"
)["net_revenue"].sum().sort_values(
    ascending=False
)

print("\n5. REVENUE BY CATEGORY")
print("-" * 70)
print(category_revenue)

print(
    "Highest Revenue Category:",
    category_revenue.index[0]
)


# ------------------------------------------------------------
# BUSINESS QUESTION 6
# Which category generates the highest profit?
# ------------------------------------------------------------

category_profit = orders_with_product.groupby(
    "category"
)["profit"].sum().sort_values(
    ascending=False
)

print("\n6. PROFIT BY CATEGORY")
print("-" * 70)
print(category_profit)

print(
    "Highest Profit Category:",
    category_profit.index[0]
)


# ------------------------------------------------------------
# BUSINESS QUESTION 7
# Which category has the highest profit margin?
# ------------------------------------------------------------

category_margin = orders_with_product.groupby(
    "category"
).agg(
    Revenue=("net_revenue", "sum"),
    Profit=("profit", "sum")
)

category_margin["Profit_Margin"] = (
    category_margin["Profit"]
    / category_margin["Revenue"]
    * 100
)

category_margin = category_margin.sort_values(
    "Profit_Margin",
    ascending=False
)

print("\n7. PROFIT MARGIN BY CATEGORY")
print("-" * 70)
print(category_margin)

print(
    "Highest Profit Margin Category:",
    category_margin.index[0]
)


# ------------------------------------------------------------
# BUSINESS QUESTION 8
# Which region generates the highest revenue?
# ------------------------------------------------------------

region_revenue = orders_with_customer.groupby(
    "region"
)["net_revenue"].sum().sort_values(
    ascending=False
)

print("\n8. REVENUE BY REGION")
print("-" * 70)
print(region_revenue)

print(
    "Highest Revenue Region:",
    region_revenue.index[0]
)


# ------------------------------------------------------------
# BUSINESS QUESTION 9
# Which region has the highest profit?
# ------------------------------------------------------------

region_profit = orders_with_customer.groupby(
    "region"
)["profit"].sum().sort_values(
    ascending=False
)

print("\n9. PROFIT BY REGION")
print("-" * 70)
print(region_profit)

print(
    "Highest Profit Region:",
    region_profit.index[0]
)


# ------------------------------------------------------------
# BUSINESS QUESTION 10
# Which age group generates the highest revenue?
# ------------------------------------------------------------

age_revenue = orders_with_customer.groupby(
    "age_group"
)["net_revenue"].sum().sort_values(
    ascending=False
)

print("\n10. REVENUE BY AGE GROUP")
print("-" * 70)
print(age_revenue)

print(
    "Highest Revenue Age Group:",
    age_revenue.index[0]
)


# ------------------------------------------------------------
# BUSINESS QUESTION 11
# Which discount category is most profitable?
# ------------------------------------------------------------

discount_profit = orders.groupby(
    "discount_category"
)["profit"].sum().sort_values(
    ascending=False
)

print("\n11. PROFIT BY DISCOUNT CATEGORY")
print("-" * 70)
print(discount_profit)

print(
    "Highest Total Profit Discount Category:",
    discount_profit.index[0]
)


# ------------------------------------------------------------
# BUSINESS QUESTION 12
# Which discount category has the highest loss rate?
# ------------------------------------------------------------

discount_loss_rate = orders.groupby(
    "discount_category"
).apply(
    lambda x: (x["profit"] < 0).mean() * 100,
    include_groups=False
).sort_values(
    ascending=False
)

print("\n12. LOSS RATE BY DISCOUNT CATEGORY")
print("-" * 70)
print(discount_loss_rate)

print(
    "Highest Loss Rate Discount Category:",
    discount_loss_rate.index[0]
)


# ------------------------------------------------------------
# BUSINESS QUESTION 13
# What is the overall return rate?
# ------------------------------------------------------------

returned_orders_count = orders[
    orders["is_returned"]
]["order_id"].nunique()

return_rate = (
    returned_orders_count
    / orders["order_id"].nunique()
    * 100
)

print("\n13. OVERALL RETURN RATE")
print("-" * 70)
print(
    "Return Rate:",
    round(return_rate, 2),
    "%"
)


# ------------------------------------------------------------
# BUSINESS QUESTION 14
# Which category has the highest return rate?
# ------------------------------------------------------------

category_return_rate = orders_with_customer.groupby(
    "category"
).agg(
    Orders=("order_id", "count"),
    Returned=("is_returned", "sum")
)

category_return_rate["Return_Rate"] = (
    category_return_rate["Returned"]
    / category_return_rate["Orders"]
    * 100
)

category_return_rate = category_return_rate.sort_values(
    "Return_Rate",
    ascending=False
)

print("\n14. RETURN RATE BY CATEGORY")
print("-" * 70)
print(category_return_rate)

print(
    "Highest Return Rate Category:",
    category_return_rate.index[0]
)


# ------------------------------------------------------------
# BUSINESS QUESTION 15
# What is the most common return reason?
# ------------------------------------------------------------

most_common_return_reason = (
    returns["return_reason"]
    .value_counts()
    .idxmax()
)

most_common_return_count = (
    returns["return_reason"]
    .value_counts()
    .max()
)

print("\n15. MOST COMMON RETURN REASON")
print("-" * 70)
print(
    "Most Common Return Reason:",
    most_common_return_reason
)
print(
    "Number of Returns:",
    most_common_return_count
)


# ------------------------------------------------------------
# BUSINESS QUESTION 16
# How many customers made purchases?
# ------------------------------------------------------------

purchasing_customers = orders[
    "customer_id"
].nunique()

print("\n16. PURCHASING CUSTOMERS")
print("-" * 70)
print(
    "Customers with Orders:",
    purchasing_customers
)


# ------------------------------------------------------------
# BUSINESS QUESTION 17
# How many customers are repeat customers?
# ------------------------------------------------------------

customer_order_counts = orders.groupby(
    "customer_id"
)["order_id"].nunique()

repeat_customers = (
    customer_order_counts[
        customer_order_counts > 1
    ].count()
)

repeat_customer_rate = (
    repeat_customers
    / customers["customer_id"].nunique()
    * 100
)

print("\n17. REPEAT CUSTOMERS")
print("-" * 70)
print("Repeat Customers:", repeat_customers)
print(
    "Repeat Customer Rate:",
    round(repeat_customer_rate, 2),
    "%"
)


# ------------------------------------------------------------
# BUSINESS QUESTION 18
# Which year generated the highest revenue?
# ------------------------------------------------------------

year_revenue = orders.groupby(
    "order_year"
)["net_revenue"].sum().sort_values(
    ascending=False
)

print("\n18. REVENUE BY YEAR")
print("-" * 70)
print(year_revenue)

print(
    "Highest Revenue Year:",
    year_revenue.index[0]
)


# ------------------------------------------------------------
# BUSINESS QUESTION 19
# Which month generated the highest revenue?
# ------------------------------------------------------------

month_revenue = orders.groupby(
    ["order_year", "order_month"]
)["net_revenue"].sum().sort_values(
    ascending=False
)

print("\n19. HIGHEST REVENUE MONTH")
print("-" * 70)
print(month_revenue.head(5))

print(
    "Highest Revenue Month:",
    month_revenue.index[0]
)


# ------------------------------------------------------------
# BUSINESS QUESTION 20
# How many orders are loss-making?
# ------------------------------------------------------------

loss_making_orders = orders[
    orders["profit"] < 0
]

loss_order_rate = (
    len(loss_making_orders)
    / len(orders)
    * 100
)

print("\n20. LOSS-MAKING ORDERS")
print("-" * 70)

print(
    "Loss-Making Orders:",
    len(loss_making_orders)
)

print(
    "Loss-Making Order Rate:",
    round(loss_order_rate, 2),
    "%"
)


print("\nDAY 6 STEP 11 COMPLETED")
print("=" * 70)

# ============================================================
# STEP 13: SAVE ANALYSIS OUTPUTS
# ============================================================

import os

output_folder = "Data/analysis_outputs"

os.makedirs(output_folder, exist_ok=True)

print("\n" + "=" * 70)
print("SAVING STATISTICAL ANALYSIS OUTPUTS")
print("=" * 70)

# 1. Descriptive statistics
statistics_summary.to_csv(
    f"{output_folder}/descriptive_statistics.csv"
)

# 2. Mean vs Median
mean_median.to_csv(
    f"{output_folder}/mean_median_comparison.csv"
)

# 3. Variability summary
variability_summary.to_csv(
    f"{output_folder}/variability_summary.csv"
)

# 4. Correlation matrix
correlation_matrix.to_csv(
    f"{output_folder}/correlation_matrix.csv"
)

# 5. Category analysis
category_analysis = orders_with_customer.groupby("category").agg(
    Orders=("order_id", "count"),
    Revenue=("net_revenue", "sum"),
    Profit=("profit", "sum"),
    Average_Profit=("profit", "mean")
)

category_analysis["Profit_Margin"] = (
    category_analysis["Profit"]
    / category_analysis["Revenue"]
    * 100
)

category_analysis.to_csv(
    f"{output_folder}/category_analysis.csv"
)

# 6. Region analysis
region_analysis = orders_with_customer.groupby("region").agg(
    Orders=("order_id", "count"),
    Revenue=("net_revenue", "sum"),
    Profit=("profit", "sum"),
    Average_Profit=("profit", "mean")
)

region_analysis["Profit_Margin"] = (
    region_analysis["Profit"]
    / region_analysis["Revenue"]
    * 100
)

region_analysis.to_csv(
    f"{output_folder}/region_analysis.csv"
)

# 7. Age group analysis
age_group_analysis = orders_with_customer.groupby("age_group").agg(
    Orders=("order_id", "count"),
    Revenue=("net_revenue", "sum"),
    Profit=("profit", "sum")
)

age_group_analysis["Profit_Margin"] = (
    age_group_analysis["Profit"]
    / age_group_analysis["Revenue"]
    * 100
)

age_group_analysis.to_csv(
    f"{output_folder}/age_group_analysis.csv"
)

# 8. Loss analysis
loss_analysis = pd.DataFrame({
    "Metric": [
        "Total Orders",
        "Loss Making Orders",
        "Loss Making Order Rate",
        "Total Loss",
        "Average Loss Per Loss Order"
    ],
    "Value": [
        len(orders_with_customer),
        len(loss_orders),
        len(loss_orders) / len(orders_with_customer) * 100,
        loss_orders["profit"].sum(),
        loss_orders["profit"].mean()
    ]
})

loss_analysis.to_csv(
    f"{output_folder}/loss_analysis.csv",
    index=False
)

# 9. Discount analysis
discount_analysis.to_csv(
    f"{output_folder}/discount_analysis.csv"
)

# 10. Return analysis
return_analysis = orders_with_customer.groupby("is_returned").agg(
    Orders=("order_id", "count"),
    Revenue=("net_revenue", "sum"),
    Profit=("profit", "sum"),
    Average_Profit=("profit", "mean")
)

return_analysis.to_csv(
    f"{output_folder}/return_analysis.csv"
)

print("\nAll analysis outputs saved successfully!")

print("\nOutput folder:")
print(output_folder)

print("\nFiles created:")
for file in os.listdir(output_folder):
    print("-", file)

print("\n" + "=" * 70)
print("STEP 13 COMPLETED")
print("=" * 70)