
import os
import pandas as pd
from decimal import Decimal, ROUND_HALF_UP

# ============================================================
# STEP 1: LOAD RAW DATASETS
# ============================================================

customers = pd.read_csv("Data/raw/customers.csv")
products = pd.read_csv("Data/raw/products.csv")
orders = pd.read_csv("Data/raw/orders.csv")
returns = pd.read_csv("Data/raw/returns.csv")

print("Customers:", customers.shape)
print("Products:", products.shape)
print("Orders:", orders.shape)
print("Returns:", returns.shape)


# ============================================================
# STEP 2: CONVERT DATE COLUMNS
# ============================================================

customers["signup_date"] = pd.to_datetime(customers["signup_date"])
orders["order_date"] = pd.to_datetime(orders["order_date"])
returns["return_date"] = pd.to_datetime(returns["return_date"])

print("\nDate Data Types:")
print("Customer signup date:", customers["signup_date"].dtype)
print("Order date:", orders["order_date"].dtype)
print("Return date:", returns["return_date"].dtype)


# ============================================================
# STEP 3: INSPECT CATEGORICAL VALUES
# ============================================================

print("\nCustomer Gender Values:")
print(customers["gender"].unique())

print("\nCustomer Regions:")
print(customers["region"].unique())

print("\nProduct Categories:")
print(products["category"].unique())

print("\nPayment Methods:")
print(orders["payment_method"].unique())

print("\nOrder Status:")
print(orders["order_status"].unique())

print("\nReturn Reasons:")
print(returns["return_reason"].unique())


# ============================================================
# STEP 4: STANDARDIZE CATEGORICAL COLUMNS
# ============================================================

customers["gender"] = customers["gender"].str.strip().str.title()
customers["city"] = customers["city"].str.strip().str.title()
customers["state"] = customers["state"].str.strip().str.title()
customers["region"] = customers["region"].str.strip().str.title()

products["category"] = products["category"].str.strip().str.title()
products["sub_category"] = products["sub_category"].str.strip().str.title()

orders["payment_method"] = orders["payment_method"].str.strip().str.title()
orders["order_status"] = orders["order_status"].str.strip().str.title()

returns["return_reason"] = returns["return_reason"].str.strip().str.title()

# Restore business-specific capitalization
orders["payment_method"] = orders["payment_method"].replace({
    "Upi": "UPI",
    "Cash On Delivery": "Cash on Delivery"
})

returns["return_reason"] = returns["return_reason"].replace({
    "Product Not As Expected": "Product Not as Expected"
})

print("\nStandardized Categories:")
print("Gender:", customers["gender"].unique())
print("Region:", customers["region"].unique())
print("Product Categories:", products["category"].unique())
print("Payment Methods:", orders["payment_method"].unique())
print("Order Status:", orders["order_status"].unique())
print("Return Reasons:", returns["return_reason"].unique())


# ============================================================
# STEP 5: VALIDATE CUSTOMER SIGNUP DATES
# ============================================================

order_customer_check = orders.merge(
    customers[["customer_id", "signup_date"]],
    on="customer_id",
    how="left",
    validate="many_to_one"
)

invalid_signup_orders = order_customer_check[
    order_customer_check["signup_date"].isna()
    | (order_customer_check["order_date"] < order_customer_check["signup_date"])
]

print("\nCustomer Signup Validation:")
print(
    "Orders before signup or with missing customer:",
    len(invalid_signup_orders)
)
print("Orders on/after signup:", len(orders) - len(invalid_signup_orders))


# ============================================================
# STEP 6: VALIDATE PRODUCT PRICING
# ============================================================

invalid_products = products[
    products["selling_price"] < products["cost_price"]
]

print("\nProduct Pricing Validation:")
print("Products with selling price below cost:", len(invalid_products))


# ============================================================
# STEP 7: VALIDATE ORDER QUANTITY
# ============================================================

invalid_quantities = orders[
    (orders["quantity"] <= 0)
    | (orders["quantity"] > 5)
]

print("\nQuantity Validation:")
print("Invalid quantities:", len(invalid_quantities))


# ============================================================
# STEP 8: VALIDATE DISCOUNTS
# ============================================================

invalid_discounts = orders[
    (orders["discount"] < 0)
    | (orders["discount"] > 0.30)
]

print("\nDiscount Validation:")
print("Invalid discounts:", len(invalid_discounts))


# ============================================================
# STEP 9: VALIDATE SHIPPING COSTS
# ============================================================

invalid_shipping = orders[
    (orders["shipping_cost"] < 40)
    | (orders["shipping_cost"] > 500)
]

print("\nShipping Cost Validation:")
print("Invalid shipping costs:", len(invalid_shipping))


# ============================================================
# STEP 10: VALIDATE RETURN DELAYS
# ============================================================

return_order_check = returns.merge(
    orders[["order_id", "order_date"]],
    on="order_id",
    how="left",
    validate="many_to_one"
)

return_order_check["return_delay_days"] = (
    return_order_check["return_date"]
    - return_order_check["order_date"]
).dt.days

invalid_returns = return_order_check[
    return_order_check["order_date"].isna()
    | (return_order_check["return_delay_days"] < 1)
    | (return_order_check["return_delay_days"] > 30)
]

print("\nReturn Date Validation:")
print(
    "Invalid return delays or missing orders:",
    len(invalid_returns)
)


# ============================================================
# STEP 11: PREPARE ORDER ANALYSIS DATA
# ============================================================

orders = orders.merge(
    products[["product_id", "cost_price", "selling_price"]],
    on="product_id",
    how="left",
    validate="many_to_one"
)

print("\nProduct Merge Validation:")
print("Orders after merge:", len(orders))
print("Missing cost prices:", orders["cost_price"].isna().sum())
print("Missing selling prices:", orders["selling_price"].isna().sum())


# ============================================================
# STEP 12: CREATE FINANCIAL ANALYTICAL COLUMNS
# ============================================================

CENT = Decimal("0.01")


def to_decimal(value):
    """Convert a value to Decimal without using binary float arithmetic."""
    return Decimal(str(value))


def round_money(value):
    """Round a monetary amount to two decimal places using half-up rounding."""
    return float(
        to_decimal(value).quantize(
            CENT,
            rounding=ROUND_HALF_UP
        )
    )


def calculate_money_column(values):
    """Apply the standard monetary rounding rule to a pandas Series."""
    return values.map(round_money)


# Convert numeric source columns to Decimal before financial calculations.
quantity_decimal = orders["quantity"].map(to_decimal)
selling_price_decimal = orders["selling_price"].map(to_decimal)
cost_price_decimal = orders["cost_price"].map(to_decimal)
discount_decimal = orders["discount"].map(to_decimal)
shipping_cost_decimal = orders["shipping_cost"].map(to_decimal)


# Gross sales: quantity × selling price
gross_sales_decimal = (
    quantity_decimal * selling_price_decimal
)

orders["gross_sales"] = gross_sales_decimal.map(round_money)


# Discount amount: rounded gross sales × discount rate
gross_sales_decimal = orders["gross_sales"].map(to_decimal)

discount_amount_decimal = (
    gross_sales_decimal * discount_decimal
)

orders["discount_amount"] = discount_amount_decimal.map(round_money)


# Net revenue: gross sales − discount amount
net_revenue_decimal = (
    gross_sales_decimal
    - orders["discount_amount"].map(to_decimal)
)

orders["net_revenue"] = net_revenue_decimal.map(round_money)


# Product cost: quantity × cost price
product_cost_decimal = (
    quantity_decimal * cost_price_decimal
)

orders["product_cost"] = product_cost_decimal.map(round_money)


# Profit: net revenue − product cost − shipping cost
profit_decimal = (
    orders["net_revenue"].map(to_decimal)
    - orders["product_cost"].map(to_decimal)
    - shipping_cost_decimal
)

orders["profit"] = profit_decimal.map(round_money)


# Profit margin: profit / net revenue × 100
orders["profit_margin"] = (
    orders["profit"] / orders["net_revenue"]
) * 100

# Avoid infinite values if net revenue is zero.
orders.loc[
    orders["net_revenue"] == 0,
    "profit_margin"
] = 0


print("\nAnalytical Columns Created:")
print(
    orders[
        [
            "order_id",
            "quantity",
            "selling_price",
            "cost_price",
            "discount",
            "gross_sales",
            "discount_amount",
            "net_revenue",
            "product_cost",
            "shipping_cost",
            "profit",
            "profit_margin"
        ]
    ].head().to_string(index=False)
)


# ============================================================
# STEP 13: VALIDATE ANALYTICAL COLUMNS
# ============================================================

print("\nAnalytical Column Validation:")

financial_columns = [
    "gross_sales",
    "discount_amount",
    "net_revenue",
    "product_cost",
    "profit",
    "profit_margin"
]

for column in financial_columns:
    print(
        f"Missing {column}:",
        orders[column].isna().sum()
    )

print("\nRevenue Validation:")
print(
    "Net Revenue <= Gross Sales:",
    (orders["net_revenue"] <= orders["gross_sales"]).all()
)

print("\nProfit Margin Range:")
print("Minimum:", orders["profit_margin"].min())
print("Maximum:", orders["profit_margin"].max())


print("\nFinancial Totals:")
for column in [
    "gross_sales",
    "discount_amount",
    "net_revenue",
    "product_cost",
    "profit"
]:
    print(
        f"{column}: "
        f"{orders[column].sum():,.2f}"
    )


# ============================================================
# STEP 14: SAVE PROCESSED DATASETS
# ============================================================

os.makedirs("Data/processed", exist_ok=True)

customers.to_csv(
    "Data/processed/customers_cleaned.csv",
    index=False
)

products.to_csv(
    "Data/processed/products_cleaned.csv",
    index=False
)

orders.to_csv(
    "Data/processed/orders_cleaned.csv",
    index=False
)

returns.to_csv(
    "Data/processed/returns_cleaned.csv",
    index=False
)

print("\nProcessed datasets saved successfully!")


# ============================================================
# STEP 15: VERIFY PROCESSED DATASETS
# ============================================================

customers_cleaned = pd.read_csv(
    "Data/processed/customers_cleaned.csv"
)

products_cleaned = pd.read_csv(
    "Data/processed/products_cleaned.csv"
)

orders_cleaned = pd.read_csv(
    "Data/processed/orders_cleaned.csv"
)

returns_cleaned = pd.read_csv(
    "Data/processed/returns_cleaned.csv"
)

print("\nProcessed Dataset Verification:")
print("Customers:", customers_cleaned.shape)
print("Products:", products_cleaned.shape)
print("Orders:", orders_cleaned.shape)
print("Returns:", returns_cleaned.shape)

print("\nOrders Cleaned Columns:")
print(orders_cleaned.columns.tolist())

print("\nProcessed Orders Data Types:")
print(orders_cleaned.dtypes)

print("\nDATA CLEANING AND VALIDATION COMPLETED SUCCESSFULLY!")