# ============================================
# NOVACART - E-COMMERCE DATASET GENERATOR
# ============================================

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# --------------------------------------------
# 1. SET RANDOM SEED
# --------------------------------------------

random.seed(42)
np.random.seed(42)

print("NovaCart Dataset Generation Started...")

# ============================================
# 2. GENERATE CUSTOMERS
# ============================================

print("\nGenerating customers...")

# Number of customers
NUM_CUSTOMERS = 5000

# Indian customer names
first_names = [
    "Rahul", "Priya", "Amit", "Sneha", "Arjun",
    "Anjali", "Vikram", "Neha", "Rohit", "Pooja",
    "Kiran", "Suresh", "Kavya", "Ravi", "Divya",
    "Manish", "Swathi", "Aditya", "Meena", "Varun",
    "Nikhil", "Lakshmi", "Sai", "Harsha", "Deepika"
]

last_names = [
    "Sharma", "Reddy", "Patel", "Kumar", "Singh",
    "Verma", "Rao", "Gupta", "Mehta", "Iyer",
    "Nair", "Das", "Joshi", "Choudhary", "Naidu"
]

# Indian cities and their states/regions
locations = [
    ("Hyderabad", "Telangana", "South"),
    ("Bengaluru", "Karnataka", "South"),
    ("Chennai", "Tamil Nadu", "South"),
    ("Mumbai", "Maharashtra", "West"),
    ("Pune", "Maharashtra", "West"),
    ("Ahmedabad", "Gujarat", "West"),
    ("Delhi", "Delhi", "North"),
    ("Jaipur", "Rajasthan", "North"),
    ("Lucknow", "Uttar Pradesh", "North"),
    ("Kolkata", "West Bengal", "East"),
    ("Bhubaneswar", "Odisha", "East"),
    ("Patna", "Bihar", "East")
]

genders = ["Male", "Female"]

customers = []

for i in range(1, NUM_CUSTOMERS + 1):

    first_name = random.choice(first_names)
    last_name = random.choice(last_names)

    city, state, region = random.choice(locations)

    age = random.randint(18, 65)

    signup_start = datetime(2021, 1, 1)
    signup_end = datetime(2025, 12, 31)

    days_difference = (signup_end - signup_start).days

    signup_date = signup_start + timedelta(
        days=random.randint(0, days_difference)
    )

    customer = {
        "customer_id": f"C{i:05d}",
        "customer_name": f"{first_name} {last_name}",
        "gender": random.choice(genders),
        "age": age,
        "city": city,
        "state": state,
        "region": region,
        "signup_date": signup_date.strftime("%Y-%m-%d")
    }

    customers.append(customer)


# Convert to DataFrame
customers_df = pd.DataFrame(customers)

# Save customers dataset
customers_df.to_csv(
    "Data/raw/customers.csv",
    index=False
)

print(f"Customers generated: {len(customers_df)}")
print("customers.csv saved successfully!")

# ============================================
# 3. GENERATE PRODUCTS
# ============================================

print("\nGenerating products...")

NUM_PRODUCTS = 200

product_categories = {
    "Electronics": [
        "Smartphones",
        "Laptops",
        "Headphones",
        "Smart Watches",
        "Accessories"
    ],
    "Home & Kitchen": [
        "Kitchen Appliances",
        "Cookware",
        "Home Decor",
        "Storage",
        "Furniture"
    ],
    "Fashion": [
        "Men Clothing",
        "Women Clothing",
        "Footwear",
        "Bags",
        "Accessories"
    ],
    "Beauty": [
        "Skincare",
        "Haircare",
        "Makeup",
        "Personal Care"
    ],
    "Sports": [
        "Fitness Equipment",
        "Sportswear",
        "Outdoor",
        "Yoga"
    ]
}

product_prefixes = [
    "Premium", "Classic", "Smart", "Pro", "Elite",
    "Essential", "Modern", "Advanced", "Ultra", "Eco"
]

product_items = [
    "Product", "Series", "Collection", "Model", "Edition"
]

products = []

for i in range(1, NUM_PRODUCTS + 1):

    category = random.choice(list(product_categories.keys()))

    sub_category = random.choice(
        product_categories[category]
    )

    prefix = random.choice(product_prefixes)
    item = random.choice(product_items)

    product_name = f"{prefix} {sub_category} {item} {i}"

    # Generate cost price
    cost_price = round(random.uniform(200, 50000), 2)

    # Selling price is higher than cost price
    markup = random.uniform(1.10, 1.60)

    selling_price = round(
        cost_price * markup,
        2
    )

    product = {
        "product_id": f"P{i:04d}",
        "product_name": product_name,
        "category": category,
        "sub_category": sub_category,
        "cost_price": cost_price,
        "selling_price": selling_price
    }

    products.append(product)


products_df = pd.DataFrame(products)

products_df.to_csv(
    "Data/raw/products.csv",
    index=False
)

print(f"Products generated: {len(products_df)}")
print("products.csv saved successfully!")

# ============================================
# 4. GENERATE ORDERS
# ============================================

print("\nGenerating orders...")

NUM_ORDERS = 50000

payment_methods = [
    "UPI",
    "Credit Card",
    "Debit Card",
    "Cash on Delivery",
    "Net Banking",
    "Wallet"
]

order_statuses = [
    "Delivered",
    "Delivered",
    "Delivered",
    "Delivered",
    "Shipped",
    "Processing",
    "Cancelled"
]

orders = []

order_start_date = datetime(2024, 1, 1)
order_end_date = datetime(2025, 12, 31)

for i in range(1, NUM_ORDERS + 1):

    # Select an existing customer and product
    customer_row = customers_df.sample(
        n=1
    ).iloc[0]

    customer_id = customer_row["customer_id"]
    signup_date = datetime.strptime(
        customer_row["signup_date"],
        "%Y-%m-%d"
    )

    product_id = random.choice(
        products_df["product_id"].tolist()
    )

    # Order date must be after customer signup date
    earliest_order_date = max(
        signup_date,
        order_start_date
    )

    # Make sure there is a valid date range
    order_days_difference = (
        order_end_date - earliest_order_date
    ).days

    if order_days_difference < 0:
        continue

    order_date = earliest_order_date + timedelta(
        days=random.randint(
            0,
            order_days_difference
        )
    )

    # Generate quantity between 1 and 5
    quantity = random.randint(1, 5)

    # Discount between 0% and 30%
    discount = round(
        random.choice([
            0,
            0.05,
            0.10,
            0.15,
            0.20,
            0.25,
            0.30
        ]),
        2
    )

    # Generate shipping cost
    shipping_cost = round(
        random.uniform(40, 500),
        2
    )

    order = {
        "order_id": f"O{i:06d}",
        "order_date": order_date.strftime("%Y-%m-%d"),
        "customer_id": customer_id,
        "product_id": product_id,
        "quantity": quantity,
        "discount": discount,
        "payment_method": random.choice(
            payment_methods
        ),
        "shipping_cost": shipping_cost,
        "order_status": random.choice(
            order_statuses
        )
    }

    orders.append(order)

# Convert orders into a DataFrame
orders_df = pd.DataFrame(orders)

# Save orders dataset
orders_df.to_csv(
    "Data/raw/orders.csv",
    index=False
)

print(f"Orders generated: {len(orders_df)}")
print("orders.csv saved successfully!")

# ============================================
# 5. GENERATE RETURNS
# ============================================

print("\nGenerating returns...")

return_reasons = [
    "Damaged Product",
    "Wrong Product",
    "Product Not as Expected",
    "Late Delivery",
    "Size Issue",
    "Quality Issue",
    "Changed Mind"
]

returns = []

# Select approximately 8% of orders for returns
number_of_returns = int(NUM_ORDERS * 0.08)

returned_orders = random.sample(
    orders_df["order_id"].tolist(),
    number_of_returns
)

returned_orders = random.sample(
    orders_df["order_id"].tolist(),
    number_of_returns
)

for i, order_id in enumerate(returned_orders, start=1):

    # Find the original order date
    order_row = orders_df[
        orders_df["order_id"] == order_id
    ].iloc[0]

    order_date = datetime.strptime(
        order_row["order_date"],
        "%Y-%m-%d"
    )

    # Return happens 1–30 days after order
    return_date = order_date + timedelta(
        days=random.randint(1, 30)
    )

    return_record = {
        "return_id": f"R{i:05d}",
        "order_id": order_id,
        "return_date": return_date.strftime("%Y-%m-%d"),
        "return_reason": random.choice(return_reasons)
    }

    returns.append(return_record)

returns_df = pd.DataFrame(returns)

# Save returns dataset
returns_df.to_csv(
    "Data/raw/returns.csv",
    index=False
)

print(f"Returns generated: {len(returns_df)}")
print("returns.csv saved successfully!")



print("\n============================================")
print("NOVACART DATASET GENERATION COMPLETED!")
print("============================================")