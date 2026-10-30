import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================
# NOVACART - DAY 5
# FEATURE ENGINEERING & EDA
# ==========================================

# Load processed datasets

customers = pd.read_csv("Data/processed/customers_cleaned.csv")
products = pd.read_csv("Data/processed/products_cleaned.csv")
orders = pd.read_csv("Data/processed/orders_cleaned.csv")
returns = pd.read_csv("Data/processed/returns_cleaned.csv")


print("Datasets loaded successfully!")

print("\nCustomers:", customers.shape)
print("Products:", products.shape)
print("Orders:", orders.shape)
print("Returns:", returns.shape)


# Convert date columns to datetime

customers["signup_date"] = pd.to_datetime(customers["signup_date"])

orders["order_date"] = pd.to_datetime(orders["order_date"])

returns["return_date"] = pd.to_datetime(returns["return_date"])


print("\nDate conversion completed!")

print("Customer signup date:", customers["signup_date"].dtype)
print("Order date:", orders["order_date"].dtype)
print("Return date:", returns["return_date"].dtype)

# ==========================================
# TIME-BASED FEATURES
# ==========================================

orders["order_year"] = orders["order_date"].dt.year

orders["order_month"] = orders["order_date"].dt.month

orders["order_month_name"] = orders["order_date"].dt.month_name()

orders["order_quarter"] = orders["order_date"].dt.quarter

orders["order_day_of_week"] = orders["order_date"].dt.day_name()


print("\nTime-based features created!")

print(
    orders[
        [
            "order_date",
            "order_year",
            "order_month",
            "order_month_name",
            "order_quarter",
            "order_day_of_week"
        ]
    ].head()
)

print("\nUnique Years:")
print(orders["order_year"].unique())

print("\nUnique Months:")
print(orders["order_month"].unique())

print("\nUnique Quarters:")
print(orders["order_quarter"].unique())

print("\nUnique Days:")
print(orders["order_day_of_week"].unique())

# ==========================================
# CUSTOMER AGE GROUP
# ==========================================

customers["age_group"] = pd.cut(
    customers["age"],
    bins=[17, 24, 34, 44, 54, 65],
    labels=[
        "18-24",
        "25-34",
        "35-44",
        "45-54",
        "55-65"
    ]
)


print("\nCustomer Age Groups:")
print(customers["age_group"].value_counts().sort_index())

# ==========================================
# DISCOUNT CATEGORY
# ==========================================

orders["discount_category"] = pd.cut(
    orders["discount"],
    bins=[-0.001, 0, 0.10, 0.20, 0.30],
    labels=[
        "No Discount",
        "Low Discount",
        "Medium Discount",
        "High Discount"
    ]
)


print("\nDiscount Categories:")
print(orders["discount_category"].value_counts().sort_index())

# ==========================================
# PROFIT CATEGORY
# ==========================================

orders["profit_category"] = orders["profit"].apply(
    lambda x: "Loss" if x < 0
    else "Break-even" if x == 0
    else "Profit"
)


print("\nProfit Categories:")
print(orders["profit_category"].value_counts())

# ==========================================
# RETURN FLAG
# ==========================================

returned_order_ids = set(returns["order_id"])

orders["is_returned"] = orders["order_id"].isin(returned_order_ids)


print("\nReturn Flag:")
print(orders["is_returned"].value_counts())

print("\nFinal Orders Columns:")

print(orders.columns.tolist())

# ==========================================
# SAVE FEATURE-ENGINEERED DATA
# ==========================================

import os

os.makedirs("Data/feature_engineered", exist_ok=True)


customers.to_csv(
    "Data/feature_engineered/customers_features.csv",
    index=False
)

products.to_csv(
    "Data/feature_engineered/products_features.csv",
    index=False
)

orders.to_csv(
    "Data/feature_engineered/orders_features.csv",
    index=False
)

returns.to_csv(
    "Data/feature_engineered/returns_features.csv",
    index=False
)


print("\nFeature-engineered datasets saved successfully!")


# ==========================================
# LOAD FEATURE-ENGINEERED DATA
# ==========================================

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


print("Feature-engineered datasets loaded successfully!")

print("\nCustomers:", customers.shape)
print("Products:", products.shape)
print("Orders:", orders.shape)
print("Returns:", returns.shape)

orders["order_date"] = pd.to_datetime(orders["order_date"])
customers["signup_date"] = pd.to_datetime(customers["signup_date"])
returns["return_date"] = pd.to_datetime(returns["return_date"])

print("\nDate columns converted successfully!")


# ==========================================
# EDA - DATASET OVERVIEW
# ==========================================

print("\n========== DATASET OVERVIEW ==========")

print("\nCustomers:")
customers.info()

print("\nProducts:")
products.info()

print("\nOrders:")
orders.info()

print("\nReturns:")
returns.info()

print("\n========== NUMERICAL SUMMARY ==========")

print("\nCustomers:")
print(customers.describe())

print("\nProducts:")
print(products.describe())

print("\nOrders:")
print(orders.describe())

print("\n========== BASIC BUSINESS METRICS ==========")

total_customers = customers["customer_id"].nunique()

total_products = products["product_id"].nunique()

total_orders = orders["order_id"].nunique()

total_returns = returns["return_id"].nunique()

print("Total Customers:", total_customers)
print("Total Products:", total_products)
print("Total Orders:", total_orders)
print("Total Returns:", total_returns)

total_gross_sales = orders["gross_sales"].sum()

total_discount = orders["discount_amount"].sum()

total_net_revenue = orders["net_revenue"].sum()

total_product_cost = orders["product_cost"].sum()

total_profit = orders["profit"].sum()


print("\nTotal Gross Sales:", round(total_gross_sales, 2))
print("Total Discount:", round(total_discount, 2))
print("Total Net Revenue:", round(total_net_revenue, 2))
print("Total Product Cost:", round(total_product_cost, 2))
print("Total Profit:", round(total_profit, 2))

aov = total_net_revenue / total_orders

print("\nAverage Order Value:", round(aov, 2))

overall_profit_margin = (
    total_profit / total_net_revenue
) * 100

print(
    "Overall Profit Margin:",
    round(overall_profit_margin, 2),
    "%"
)


returned_orders = orders["is_returned"].sum()

return_rate = (
    returned_orders / total_orders
) * 100

print("\nReturned Orders:", returned_orders)

print(
    "Return Rate:",
    round(return_rate, 2),
    "%"
)

# ==========================================
# ORDER STATUS DISTRIBUTION
# ==========================================

plt.figure(figsize=(8, 5))

sns.countplot(
    data=orders,
    x="order_status"
)

plt.title("Order Status Distribution")
plt.xlabel("Order Status")
plt.ylabel("Number of Orders")

plt.tight_layout()
plt.show()

plt.figure(figsize=(9, 5))

sns.countplot(
    data=orders,
    x="payment_method"
)

plt.title("Orders by Payment Method")
plt.xlabel("Payment Method")
plt.ylabel("Number of Orders")

plt.xticks(rotation=30)

plt.tight_layout()
plt.show()

plt.figure(figsize=(8, 5))

sns.countplot(
    data=products,
    x="category"
)

plt.title("Number of Products by Category")
plt.xlabel("Category")
plt.ylabel("Number of Products")

plt.xticks(rotation=30)

plt.tight_layout()
plt.show()

plt.figure(figsize=(8, 5))

sns.histplot(
    data=customers,
    x="age",
    bins=10,
    kde=True
)

plt.title("Customer Age Distribution")
plt.xlabel("Age")
plt.ylabel("Number of Customers")

plt.tight_layout()
plt.show()

plt.figure(figsize=(8, 5))

sns.countplot(
    data=customers,
    x="age_group"
)

plt.title("Customers by Age Group")
plt.xlabel("Age Group")
plt.ylabel("Number of Customers")

plt.tight_layout()
plt.show()

plt.figure(figsize=(8, 5))

sns.histplot(
    data=orders,
    x="profit",
    bins=50,
    kde=True
)

plt.title("Order-Level Profit Distribution")
plt.xlabel("Profit")
plt.ylabel("Number of Orders")

plt.tight_layout()
plt.show()

plt.figure(figsize=(7, 5))

sns.countplot(
    data=orders,
    x="profit_category"
)

plt.title("Orders by Profit Category")
plt.xlabel("Profit Category")
plt.ylabel("Number of Orders")

plt.tight_layout()
plt.show()

# ==========================================
# YEARLY REVENUE ANALYSIS
# ==========================================

yearly_revenue = (
    orders
    .groupby("order_year")["net_revenue"]
    .sum()
    .reset_index()
)

print("\n========== YEARLY REVENUE ==========")
print(yearly_revenue)

plt.figure(figsize=(8, 5))

sns.barplot(
    data=yearly_revenue,
    x="order_year",
    y="net_revenue"
)

plt.title("Yearly Net Revenue")
plt.xlabel("Year")
plt.ylabel("Net Revenue")

plt.tight_layout()
plt.show()

yearly_revenue["revenue_growth_%"] = (
    yearly_revenue["net_revenue"]
    .pct_change()
    * 100
)

print("\n========== YEARLY REVENUE GROWTH ==========")
print(yearly_revenue)

# ==========================================
# MONTHLY REVENUE ANALYSIS
# ==========================================

monthly_revenue = (
    orders
    .groupby(
        [
            "order_year",
            "order_month",
            "order_month_name"
        ]
    )["net_revenue"]
    .sum()
    .reset_index()
)

monthly_revenue = monthly_revenue.sort_values(
    ["order_year", "order_month"]
)

print("\n========== MONTHLY REVENUE ==========")
print(monthly_revenue)

plt.figure(figsize=(12, 6))

sns.lineplot(
    data=monthly_revenue,
    x="order_month",
    y="net_revenue",
    hue="order_year",
    marker="o"
)

plt.title("Monthly Net Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Net Revenue")
plt.xticks(range(1, 13))

plt.tight_layout()
plt.show()

highest_revenue_month = monthly_revenue.loc[
    monthly_revenue["net_revenue"].idxmax()
]

print("\n========== HIGHEST REVENUE MONTH ==========")

print(
    "Year:",
    highest_revenue_month["order_year"]
)

print(
    "Month:",
    highest_revenue_month["order_month_name"]
)

print(
    "Revenue:",
    round(highest_revenue_month["net_revenue"], 2)
)

# ==========================================
# MERGE PRODUCT INFORMATION
# ==========================================

orders_with_product = orders.merge(
    products[
        [
            "product_id",
            "product_name",
            "category",
            "sub_category"
        ]
    ],
    on="product_id",
    how="left"
)

category_revenue = (
    orders_with_product
    .groupby("category")["net_revenue"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

print("\n========== REVENUE BY CATEGORY ==========")
print(category_revenue)

plt.figure(figsize=(9, 5))

sns.barplot(
    data=category_revenue,
    x="category",
    y="net_revenue"
)

plt.title("Net Revenue by Product Category")
plt.xlabel("Category")
plt.ylabel("Net Revenue")

plt.xticks(rotation=30)

plt.tight_layout()
plt.show()

category_profit = (
    orders_with_product
    .groupby("category")["profit"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

print("\n========== PROFIT BY CATEGORY ==========")
print(category_profit)

plt.figure(figsize=(9, 5))

sns.barplot(
    data=category_profit,
    x="category",
    y="profit"
)

plt.title("Profit by Product Category")
plt.xlabel("Category")
plt.ylabel("Profit")

plt.xticks(rotation=30)

plt.tight_layout()
plt.show()

# ==========================================
# TOP 10 PRODUCTS BY REVENUE
# ==========================================

top_products_revenue = (
    orders_with_product
    .groupby(
        [
            "product_id",
            "product_name"
        ]
    )["net_revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

print("\n========== TOP 10 PRODUCTS BY REVENUE ==========")
print(top_products_revenue)

plt.figure(figsize=(10, 6))

sns.barplot(
    data=top_products_revenue,
    x="net_revenue",
    y="product_name"
)

plt.title("Top 10 Products by Net Revenue")
plt.xlabel("Net Revenue")
plt.ylabel("Product")

plt.tight_layout()
plt.show()

top_products_profit = (
    orders_with_product
    .groupby(
        [
            "product_id",
            "product_name"
        ]
    )["profit"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

print("\n========== TOP 10 PRODUCTS BY PROFIT ==========")
print(top_products_profit)

plt.figure(figsize=(10, 6))

sns.barplot(
    data=top_products_profit,
    x="profit",
    y="product_name"
)

plt.title("Top 10 Products by Profit")
plt.xlabel("Profit")
plt.ylabel("Product")

plt.tight_layout()
plt.show()

category_units = (
    orders_with_product
    .groupby("category")["quantity"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

print("\n========== UNITS SOLD BY CATEGORY ==========")
print(category_units)

plt.figure(figsize=(9, 5))

sns.barplot(
    data=category_units,
    x="category",
    y="quantity"
)

plt.title("Units Sold by Product Category")
plt.xlabel("Category")
plt.ylabel("Units Sold")

plt.xticks(rotation=30)

plt.tight_layout()
plt.show()

average_quantity = orders["quantity"].mean()

print(
    "\nAverage Quantity per Order:",
    round(average_quantity, 2)
)

discount_analysis = (
    orders
    .groupby("discount_category", observed=False)
    .agg(
        total_orders=("order_id", "count"),
        total_revenue=("net_revenue", "sum"),
        total_profit=("profit", "sum"),
        average_profit=("profit", "mean")
    )
    .reset_index()
)

print("\n========== DISCOUNT ANALYSIS ==========")
print(discount_analysis)

plt.figure(figsize=(9, 5))

sns.barplot(
    data=discount_analysis,
    x="discount_category",
    y="average_profit"
)

plt.title("Average Profit by Discount Category")
plt.xlabel("Discount Category")
plt.ylabel("Average Profit")

plt.xticks(rotation=20)

plt.tight_layout()
plt.show()

revenue_summary = (
    orders_with_product
    .groupby("category")
    .agg(
        total_orders=("order_id", "count"),
        units_sold=("quantity", "sum"),
        gross_sales=("gross_sales", "sum"),
        discount=("discount_amount", "sum"),
        net_revenue=("net_revenue", "sum"),
        product_cost=("product_cost", "sum"),
        profit=("profit", "sum")
    )
    .reset_index()
)

print("\n========== CATEGORY BUSINESS SUMMARY ==========")
print(revenue_summary)

revenue_summary["profit_margin_%"] = (
    revenue_summary["profit"]
    / revenue_summary["net_revenue"]
) * 100

print("\n========== CATEGORY BUSINESS SUMMARY WITH MARGIN ==========")

print(
    revenue_summary.sort_values(
        "net_revenue",
        ascending=False
    )
)

print("\n========== CATEGORY BUSINESS SUMMARY WITH MARGIN ==========")

print(
    revenue_summary.sort_values(
        "net_revenue",
        ascending=False
    )
)

# ==========================================
# MERGE CUSTOMER INFORMATION
# ==========================================

orders_with_customer = orders.merge(
    customers[
        [
            "customer_id",
            "customer_name",
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

print("\nOrders with customer information:")
print(orders_with_customer.shape)

customer_summary = (
    orders_with_customer
    .groupby(
        [
            "customer_id",
            "customer_name",
            "gender",
            "age",
            "age_group",
            "city",
            "state",
            "region"
        ]
    )
    .agg(
        total_orders=("order_id", "count"),
        total_units=("quantity", "sum"),
        total_revenue=("net_revenue", "sum"),
        total_profit=("profit", "sum"),
        average_order_value=("net_revenue", "mean")
    )
    .reset_index()
)

print("\n========== CUSTOMER SUMMARY ==========")
print(customer_summary.head())

total_registered_customers = customers["customer_id"].nunique()

purchasing_customers = customer_summary["customer_id"].nunique()

print("\nRegistered Customers:", total_registered_customers)
print("Customers with Orders:", purchasing_customers)

repeat_customers = customer_summary[
    customer_summary["total_orders"] > 1
]

repeat_customer_count = repeat_customers["customer_id"].nunique()

repeat_customer_rate = (
    repeat_customer_count
    / purchasing_customers
) * 100

print("\n========== REPEAT CUSTOMER ANALYSIS ==========")

print("Repeat Customers:", repeat_customer_count)

print(
    "Repeat Customer Rate:",
    round(repeat_customer_rate, 2),
    "%"
)

plt.figure(figsize=(9, 5))

sns.histplot(
    data=customer_summary,
    x="total_revenue",
    bins=40,
    kde=True
)

plt.title("Customer Revenue Distribution")
plt.xlabel("Total Customer Revenue")
plt.ylabel("Number of Customers")

plt.tight_layout()
plt.show()

top_customers = (
    customer_summary
    .sort_values(
        "total_revenue",
        ascending=False
    )
    .head(10)
)

print("\n========== TOP 10 CUSTOMERS BY REVENUE ==========")

print(
    top_customers[
        [
            "customer_id",
            "customer_name",
            "total_orders",
            "total_revenue",
            "total_profit"
        ]
    ]
)

plt.figure(figsize=(10, 6))

sns.barplot(
    data=top_customers,
    x="total_revenue",
    y="customer_name"
)

plt.title("Top 10 Customers by Revenue")
plt.xlabel("Total Revenue")
plt.ylabel("Customer")

plt.tight_layout()
plt.show()

age_group_analysis = (
    orders_with_customer
    .groupby("age_group", observed=False)
    .agg(
        customers=("customer_id", "nunique"),
        orders=("order_id", "count"),
        revenue=("net_revenue", "sum"),
        profit=("profit", "sum")
    )
    .reset_index()
)

print("\n========== AGE GROUP ANALYSIS ==========")
print(age_group_analysis)
plt.figure(figsize=(9, 5))

sns.barplot(
    data=age_group_analysis,
    x="age_group",
    y="revenue"
)

plt.title("Revenue by Customer Age Group")
plt.xlabel("Age Group")
plt.ylabel("Revenue")

plt.tight_layout()
plt.show()

plt.figure(figsize=(9, 5))

sns.barplot(
    data=age_group_analysis,
    x="age_group",
    y="profit"
)

plt.title("Profit by Customer Age Group")
plt.xlabel("Age Group")
plt.ylabel("Profit")

plt.tight_layout()
plt.show()


gender_analysis = (
    orders_with_customer
    .groupby("gender")
    .agg(
        customers=("customer_id", "nunique"),
        orders=("order_id", "count"),
        units=("quantity", "sum"),
        revenue=("net_revenue", "sum"),
        profit=("profit", "sum")
    )
    .reset_index()
)

print("\n========== GENDER ANALYSIS ==========")
print(gender_analysis)

plt.figure(figsize=(7, 5))

sns.barplot(
    data=gender_analysis,
    x="gender",
    y="revenue"
)

plt.title("Revenue by Gender")
plt.xlabel("Gender")
plt.ylabel("Revenue")

plt.tight_layout()
plt.show()

regional_analysis = (
    orders_with_customer
    .groupby("region")
    .agg(
        customers=("customer_id", "nunique"),
        orders=("order_id", "count"),
        units=("quantity", "sum"),
        gross_sales=("gross_sales", "sum"),
        discount=("discount_amount", "sum"),
        revenue=("net_revenue", "sum"),
        profit=("profit", "sum"),
        returned_orders=("is_returned", "sum")
    )
    .reset_index()
)

print("\n========== REGIONAL ANALYSIS ==========")
print(regional_analysis)

regional_analysis["profit_margin_%"] = (
    regional_analysis["profit"]
    / regional_analysis["revenue"]
) * 100

regional_analysis["return_rate_%"] = (
    regional_analysis["returned_orders"]
    / regional_analysis["orders"]
) * 100

print("\n========== REGIONAL BUSINESS SUMMARY ==========")

print(
    regional_analysis.sort_values(
        "revenue",
        ascending=False
    )
)

plt.figure(figsize=(8, 5))

sns.barplot(
    data=regional_analysis,
    x="region",
    y="revenue"
)

plt.title("Revenue by Region")
plt.xlabel("Region")
plt.ylabel("Revenue")

plt.tight_layout()
plt.show()

plt.figure(figsize=(8, 5))

sns.barplot(
    data=regional_analysis,
    x="region",
    y="profit"
)

plt.title("Profit by Region")
plt.xlabel("Region")
plt.ylabel("Profit")

plt.tight_layout()
plt.show()

plt.figure(figsize=(8, 5))

sns.barplot(
    data=regional_analysis,
    x="region",
    y="return_rate_%"
)

plt.title("Return Rate by Region")
plt.xlabel("Region")
plt.ylabel("Return Rate (%)")

plt.tight_layout()
plt.show()

city_analysis = (
    orders_with_customer
    .groupby(
        [
            "city",
            "state",
            "region"
        ]
    )
    .agg(
        customers=("customer_id", "nunique"),
        orders=("order_id", "count"),
        revenue=("net_revenue", "sum"),
        profit=("profit", "sum")
    )
    .reset_index()
)

top_cities = (
    city_analysis
    .sort_values(
        "revenue",
        ascending=False
    )
    .head(10)
)

print("\n========== TOP 10 CITIES BY REVENUE ==========")
print(top_cities)

plt.figure(figsize=(10, 6))

sns.barplot(
    data=top_cities,
    x="revenue",
    y="city"
)

plt.title("Top 10 Cities by Revenue")
plt.xlabel("Revenue")
plt.ylabel("City")

plt.tight_layout()
plt.show()

plt.figure(figsize=(9, 6))

sns.scatterplot(
    data=customer_summary,
    x="total_orders",
    y="total_revenue"
)

plt.title("Customer Orders vs Revenue")
plt.xlabel("Total Orders")
plt.ylabel("Total Revenue")

plt.tight_layout()
plt.show()

plt.figure(figsize=(8, 5))

sns.histplot(
    data=customer_summary,
    x="total_orders",
    bins=20,
    discrete=True
)

plt.title("Distribution of Orders per Customer")
plt.xlabel("Number of Orders")
plt.ylabel("Number of Customers")

plt.tight_layout()
plt.show()

# ==========================================
# SAVE EDA SUMMARY TABLES
# ==========================================

os.makedirs("Data/eda_outputs", exist_ok=True)

customer_summary.to_csv(
    "Data/eda_outputs/customer_summary.csv",
    index=False
)

age_group_analysis.to_csv(
    "Data/eda_outputs/age_group_analysis.csv",
    index=False
)

gender_analysis.to_csv(
    "Data/eda_outputs/gender_analysis.csv",
    index=False
)

regional_analysis.to_csv(
    "Data/eda_outputs/regional_analysis.csv",
    index=False
)

city_analysis.to_csv(
    "Data/eda_outputs/city_analysis.csv",
    index=False
)

print("\nEDA summary tables saved successfully!")




# ==========================================
# RETURN ANALYSIS
# ==========================================

return_reason_analysis = (
    returns
    .groupby("return_reason")
    .size()
    .sort_values(ascending=False)
    .reset_index(name="return_count")
)

print("\n========== RETURN REASONS ==========")
print(return_reason_analysis)

plt.figure(figsize=(10, 6))

sns.barplot(
    data=return_reason_analysis,
    x="return_count",
    y="return_reason"
)

plt.title("Orders by Return Reason")
plt.xlabel("Number of Returns")
plt.ylabel("Return Reason")

plt.tight_layout()
plt.show()

total_orders = orders["order_id"].nunique()

returned_orders = orders["is_returned"].sum()

return_rate = (
    returned_orders / total_orders
) * 100

print("\n========== RETURN SUMMARY ==========")

print("Total Orders:", total_orders)
print("Returned Orders:", returned_orders)
print("Return Rate:", round(return_rate, 2), "%")


return_status_analysis = (
    orders
    .groupby("is_returned")
    .agg(
        orders=("order_id", "count"),
        revenue=("net_revenue", "sum"),
        profit=("profit", "sum"),
        average_profit=("profit", "mean")
    )
    .reset_index()
)

return_status_analysis["return_status"] = (
    return_status_analysis["is_returned"]
    .map({
        False: "Not Returned",
        True: "Returned"
    })
)

print("\n========== RETURNED VS NON-RETURNED ==========")

print(
    return_status_analysis[
        [
            "return_status",
            "orders",
            "revenue",
            "profit",
            "average_profit"
        ]
    ]
)

category_return_analysis = (
    orders_with_product
    .groupby("category")
    .agg(
        total_orders=("order_id", "count"),
        returned_orders=("is_returned", "sum"),
        revenue=("net_revenue", "sum"),
        profit=("profit", "sum")
    )
    .reset_index()
)

category_return_analysis["return_rate_%"] = (
    category_return_analysis["returned_orders"]
    / category_return_analysis["total_orders"]
) * 100

print("\n========== RETURN RATE BY CATEGORY ==========")

print(
    category_return_analysis.sort_values(
        "return_rate_%",
        ascending=False
    )
)

plt.figure(figsize=(9, 5))

sns.barplot(
    data=category_return_analysis.sort_values(
        "return_rate_%",
        ascending=False
    ),
    x="category",
    y="return_rate_%"
)

plt.title("Return Rate by Product Category")
plt.xlabel("Category")
plt.ylabel("Return Rate (%)")

plt.xticks(rotation=30)

plt.tight_layout()
plt.show()

return_reason_analysis["return_percentage_%"] = (
    return_reason_analysis["return_count"]
    / return_reason_analysis["return_count"].sum()
) * 100

print("\n========== RETURN REASON CONTRIBUTION ==========")

print(return_reason_analysis)

returns_with_orders = returns.merge(
    orders[
        [
            "order_id",
            "order_date"
        ]
    ],
    on="order_id",
    how="left"
)

returns_with_orders["return_delay_days"] = (
    returns_with_orders["return_date"]
    - returns_with_orders["order_date"]
).dt.days

print("\n========== RETURN DELAY ==========")

print(
    returns_with_orders["return_delay_days"].describe()
)

plt.figure(figsize=(9, 5))

sns.histplot(
    data=returns_with_orders,
    x="return_delay_days",
    bins=30
)

plt.title("Return Delay Distribution")
plt.xlabel("Days Between Order and Return")
plt.ylabel("Number of Returns")

plt.tight_layout()
plt.show()

discount_analysis = (
    orders
    .groupby(
        "discount_category",
        observed=False
    )
    .agg(
        orders=("order_id", "count"),
        units=("quantity", "sum"),
        gross_sales=("gross_sales", "sum"),
        discount_amount=("discount_amount", "sum"),
        net_revenue=("net_revenue", "sum"),
        profit=("profit", "sum")
    )
    .reset_index()
)

discount_analysis["profit_margin_%"] = (
    discount_analysis["profit"]
    / discount_analysis["net_revenue"]
) * 100

print("\n========== DISCOUNT ANALYSIS ==========")

print(discount_analysis)


discount_profit_analysis = (
    orders
    .groupby(
        "discount_category",
        observed=False
    )
    .agg(
        average_discount=("discount", "mean"),
        average_revenue=("net_revenue", "mean"),
        average_profit=("profit", "mean"),
        orders=("order_id", "count")
    )
    .reset_index()
)

print("\n========== DISCOUNT VS PROFIT ==========")

print(discount_profit_analysis)

plt.figure(figsize=(9, 5))

sns.barplot(
    data=discount_profit_analysis,
    x="discount_category",
    y="average_profit"
)

plt.title("Average Profit by Discount Category")
plt.xlabel("Discount Category")
plt.ylabel("Average Profit")

plt.xticks(rotation=20)

plt.tight_layout()
plt.show()

plt.figure(figsize=(9, 6))

sns.scatterplot(
    data=orders,
    x="discount",
    y="profit",
    alpha=0.4
)

plt.title("Discount vs Order-Level Profit")
plt.xlabel("Discount")
plt.ylabel("Profit")

plt.tight_layout()
plt.show()

correlation_data = orders[
    [
        "quantity",
        "discount",
        "shipping_cost",
        "selling_price",
        "gross_sales",
        "discount_amount",
        "net_revenue",
        "product_cost",
        "profit",
        "profit_margin"
    ]
]

correlation_matrix = correlation_data.corr()

print("\n========== CORRELATION MATRIX ==========")

print(correlation_matrix.round(2))

plt.figure(figsize=(12, 8))

sns.heatmap(
    correlation_matrix,
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    center=0
)

plt.title("Correlation Matrix of Key Numerical Variables")

plt.tight_layout()
plt.show()

plt.figure(figsize=(9, 5))

sns.boxplot(
    x=orders["net_revenue"]
)

plt.title("Net Revenue Outliers")
plt.xlabel("Net Revenue")

plt.tight_layout()
plt.show()

plt.figure(figsize=(9, 5))

sns.boxplot(
    x=orders["profit"]
)

plt.title("Profit Outliers")
plt.xlabel("Profit")

plt.tight_layout()
plt.show()

lowest_profit_orders = (
    orders
    .sort_values("profit")
    .head(10)
)

print("\n========== LOWEST PROFIT ORDERS ==========")

print(
    lowest_profit_orders[
        [
            "order_id",
            "quantity",
            "discount",
            "shipping_cost",
            "net_revenue",
            "product_cost",
            "profit"
        ]
    ]
)

highest_profit_orders = (
    orders
    .sort_values(
        "profit",
        ascending=False
    )
    .head(10)
)

print("\n========== HIGHEST PROFIT ORDERS ==========")

print(
    highest_profit_orders[
        [
            "order_id",
            "quantity",
            "discount",
            "shipping_cost",
            "net_revenue",
            "product_cost",
            "profit"
        ]
    ]
)

return_reason_analysis.to_csv(
    "Data/eda_outputs/return_reason_analysis.csv",
    index=False
)

category_return_analysis.to_csv(
    "Data/eda_outputs/category_return_analysis.csv",
    index=False
)

discount_analysis.to_csv(
    "Data/eda_outputs/discount_analysis.csv",
    index=False
)

discount_profit_analysis.to_csv(
    "Data/eda_outputs/discount_profit_analysis.csv",
    index=False
)

print("\nReturn and discount analysis tables saved successfully!")

# ==========================================
# FINAL EDA SUMMARY
# ==========================================

print("\n")
print("=" * 60)
print("NOVACART - FINAL EDA SUMMARY")
print("=" * 60)

print("\nBusiness Metrics")
print("----------------")
print("Customers:", total_customers)
print("Products:", total_products)
print("Orders:", total_orders)
print("Returned Orders:", returned_orders)

print(
    "Net Revenue:",
    round(total_net_revenue, 2)
)

print(
    "Total Profit:",
    round(total_profit, 2)
)

print(
    "Profit Margin:",
    round(overall_profit_margin, 2),
    "%"
)

print(
    "Return Rate:",
    round(return_rate, 2),
    "%"
)

print(
    "Average Order Value:",
    round(aov, 2)
)

print("\nEDA completed successfully!")
