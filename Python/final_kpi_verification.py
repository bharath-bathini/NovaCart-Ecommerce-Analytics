
from pathlib import Path
import pandas as pd

# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Load the processed orders dataset
file_path = PROJECT_ROOT / "Data" / "processed" / "orders_cleaned.csv"
orders = pd.read_csv(file_path)

# Required columns
required_columns = [
    "gross_sales",
    "discount_amount",
    "net_revenue",
    "product_cost",
    "profit",
    "profit_margin",
]

missing_columns = [col for col in required_columns if col not in orders.columns]

if missing_columns:
    print("Missing required columns:", missing_columns)
    raise SystemExit("Verification stopped. Check the dataset columns.")

# Convert financial columns to numeric values
for col in required_columns:
    orders[col] = pd.to_numeric(orders[col], errors="coerce")

if orders[required_columns].isna().any().any():
    raise SystemExit("Verification stopped: missing or non-numeric KPI values found.")

# Calculate KPI totals
total_orders = len(orders)
total_gross_sales = orders["gross_sales"].sum()
total_discounts = orders["discount_amount"].sum()
total_net_revenue = orders["net_revenue"].sum()
total_product_cost = orders["product_cost"].sum()
total_profit = orders["profit"].sum()

# Calculate the overall weighted profit margin
overall_profit_margin = (
    total_profit / total_net_revenue * 100
    if total_net_revenue != 0
    else 0
)

average_order_value = (
    total_net_revenue / total_orders
    if total_orders != 0
    else 0
)

print("\n========== NOVACART FINAL KPI VERIFICATION ==========")
print(f"Total Orders:           {total_orders:,}")
print(f"Gross Sales:             ₹{total_gross_sales:,.2f}")
print(f"Discount Amount:         ₹{total_discounts:,.2f}")
print(f"Net Revenue:             ₹{total_net_revenue:,.2f}")
print(f"Product Cost:            ₹{total_product_cost:,.2f}")
print(f"Total Profit:            ₹{total_profit:,.2f}")
print(f"Profit Margin:           {overall_profit_margin:.2f}%")
print(f"Average Order Value:     ₹{average_order_value:,.2f}")

# Basic financial consistency checks
print("\n========== VALIDATION CHECKS ==========")

print(
    "Net revenue = gross sales - discounts:",
    (
        orders["net_revenue"]
        - (orders["gross_sales"] - orders["discount_amount"])
    ).abs().max() < 0.02
)

print(
    "Profit = net revenue - product cost - shipping cost:",
    (
        orders["profit"]
        - (
            orders["net_revenue"]
            - orders["product_cost"]
            - orders["shipping_cost"]
        )
    ).abs().max() < 0.02
)

print("=====================================================")