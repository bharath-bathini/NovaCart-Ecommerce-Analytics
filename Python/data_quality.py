import pandas as pd

print("========================================")
print("NOVACART DATA QUALITY ASSESSMENT")
print("========================================\n")

# Load datasets
customers = pd.read_csv("Data/raw/customers.csv")
products = pd.read_csv("Data/raw/products.csv")
orders = pd.read_csv("Data/raw/orders.csv")
returns = pd.read_csv("Data/raw/returns.csv")

print("All datasets loaded successfully!\n")

print("Dataset Shapes")
print("----------------")

print("Customers:", customers.shape)
print("Products :", products.shape)
print("Orders   :", orders.shape)
print("Returns  :", returns.shape)

print("\nMissing Values")
print("----------------")

print("\nCustomers:")
print(customers.isnull().sum())

print("\nProducts:")
print(products.isnull().sum())

print("\nOrders:")
print(orders.isnull().sum())

print("\nReturns:")
print(returns.isnull().sum())

print("\nDuplicate Records")
print("-------------------")

print("Customers:", customers.duplicated().sum())
print("Products :", products.duplicated().sum())
print("Orders   :", orders.duplicated().sum())
print("Returns  :", returns.duplicated().sum())

print("\nCustomers Data Types")
print("---------------------")
print(customers.dtypes)

print("\nProducts Data Types")
print("--------------------")
print(products.dtypes)

print("\nOrders Data Types")
print("-------------------")
print(orders.dtypes)

print("\nReturns Data Types")
print("--------------------")
print(returns.dtypes)

print("\nCustomer Gender Values:")
print(customers["gender"].unique())

print("\nCustomer Regions:")
print(customers["region"].unique())


print("\nProduct Categories:")
print(products["category"].unique())

print("\nProduct Sub-Categories:")
print(products["sub_category"].unique())


print("\nPayment Methods:")
print(orders["payment_method"].unique())

print("\nOrder Status:")
print(orders["order_status"].unique())

print("\nReturn Reasons:")
print(returns["return_reason"].unique())

print("\nCustomer Age Range")
print("-------------------")

print("Minimum age:", customers["age"].min())
print("Maximum age:", customers["age"].max())

print("\nProduct Price Range")
print("--------------------")

print("Minimum cost price:",
      products["cost_price"].min())

print("Maximum cost price:",
      products["cost_price"].max())

print("Minimum selling price:",
      products["selling_price"].min())

print("Maximum selling price:",
      products["selling_price"].max())

print("\nOrder Quantity")
print("----------------")

print("Minimum quantity:",
      orders["quantity"].min())

print("Maximum quantity:",
      orders["quantity"].max())

print("\nOrder Discount")
print("----------------")

print("Minimum discount:",
      orders["discount"].min())

print("Maximum discount:",
      orders["discount"].max())

print("\nShipping Cost")
print("----------------")

print("Minimum shipping cost:",
      orders["shipping_cost"].min())

print("Maximum shipping cost:",
      orders["shipping_cost"].max())

print("\nPrimary Key Checks")
print("-------------------")

print(
    "Customer IDs unique:",
    customers["customer_id"].is_unique
)

print(
    "Product IDs unique:",
    products["product_id"].is_unique
)

print(
    "Order IDs unique:",
    orders["order_id"].is_unique
)

print(
    "Return IDs unique:",
    returns["return_id"].is_unique
)

invalid_customer_ids = orders[
    ~orders["customer_id"].isin(customers["customer_id"])
]

print("\nInvalid Customer IDs:",
      len(invalid_customer_ids))

invalid_product_ids = orders[
    ~orders["product_id"].isin(products["product_id"])
]

print("Invalid Product IDs:",
      len(invalid_product_ids))

invalid_return_orders = returns[
    ~returns["order_id"].isin(orders["order_id"])
]

print("Invalid Return Order IDs:",
      len(invalid_return_orders))

print(customers["signup_date"].dtype)
print(orders["order_date"].dtype)
print(returns["return_date"].dtype)


customers["signup_date"] = pd.to_datetime(
    customers["signup_date"]
)

orders["order_date"] = pd.to_datetime(
    orders["order_date"]
)

returns["return_date"] = pd.to_datetime(
    returns["return_date"]
)

print("\nDate Ranges")

print(
    "Customer signup:",
    customers["signup_date"].min(),
    "to",
    customers["signup_date"].max()
)

print(
    "Orders:",
    orders["order_date"].min(),
    "to",
    orders["order_date"].max()
)

print(
    "Returns:",
    returns["return_date"].min(),
    "to",
    returns["return_date"].max()
)

# Calculate number of days between order and return
return_check = returns.merge(
    orders[["order_id", "order_date"]],
    on="order_id",
    how="left"
)

return_check["return_delay_days"] = (
    return_check["return_date"] -
    return_check["order_date"]
).dt.days

print("\nReturn Delay Check")
print("------------------")

print("Minimum return delay:",
      return_check["return_delay_days"].min())

print("Maximum return delay:",
      return_check["return_delay_days"].max())

print("Returns within 1-30 days:",
      ((return_check["return_delay_days"] >= 1) &
       (return_check["return_delay_days"] <= 30)).sum())

print("Returns outside 1-30 days:",
      ((return_check["return_delay_days"] < 1) |
       (return_check["return_delay_days"] > 30)).sum())

order_customer_check = orders.merge(
    customers[["customer_id", "signup_date"]],
    on="customer_id",
    how="left"
)

orders_before_signup = (
    order_customer_check["order_date"] <
    order_customer_check["signup_date"]
)

print("\nCustomer Signup Validation")
print("-------------------------")

print("Orders before customer signup:",
      orders_before_signup.sum())

print("Orders on/after customer signup:",
      (~orders_before_signup).sum())

# Check whether customers placed orders before signing up

order_customer_check = orders.merge(
    customers[["customer_id", "signup_date"]],
    on="customer_id",
    how="left"
)

orders_before_signup = (
    order_customer_check["order_date"] <
    order_customer_check["signup_date"]
)

print("\nCustomer Signup Validation")
print("-------------------------")

print("Orders before customer signup:",
      orders_before_signup.sum())

print("Orders on/after customer signup:",
      (~orders_before_signup).sum())

orders = []