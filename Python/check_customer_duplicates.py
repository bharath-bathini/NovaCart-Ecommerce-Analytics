
from pathlib import Path
import pandas as pd

# Locate the project folder and customer CSV file
project_folder = Path(__file__).resolve().parent.parent

file_path = (
    project_folder
    / "Data"
    / "feature_engineered"
    / "customers_features.csv"
)

print("=" * 60)
print("NOVACART - CUSTOMER ID DUPLICATE CHECK")
print("=" * 60)

# Check whether the CSV file exists
if not file_path.exists():
    print("ERROR: Customer CSV file was not found.")
    print("Expected location:", file_path)
else:
    # Load the dataset
    customers = pd.read_csv(file_path)

    # Remove accidental spaces around column names
    customers.columns = customers.columns.str.strip()

    # Check whether customer_id exists
    if "customer_id" not in customers.columns:
        print("ERROR: customer_id column was not found.")
        print("Available columns:", customers.columns.tolist())

    else:
        # Basic dataset information
        print("\n1. DATASET SUMMARY")
        print("Total rows:", len(customers))
        print(
            "Unique customer IDs:",
            customers["customer_id"].nunique()
        )
        print(
            "Missing customer IDs:",
            customers["customer_id"].isna().sum()
        )

        # Find all rows belonging to duplicated customer IDs
        duplicate_mask = customers["customer_id"].duplicated(
            keep=False
        )

        duplicates = customers.loc[duplicate_mask].sort_values(
            "customer_id"
        )

        print("\n2. DUPLICATE CUSTOMER ID CHECK")

        if duplicates.empty:
            print("No duplicate customer IDs found.")
        else:
            print("Rows involved in duplicate IDs:", len(duplicates))
            print(
                "Number of duplicated IDs:",
                duplicates["customer_id"].nunique()
            )

            print("\nDuplicate customer records:")
            print(duplicates.to_string(index=False))

        # Check whether entire records are identical
        print("\n3. EXACT DUPLICATE ROW CHECK")
        print(
            "Entire duplicate rows:",
            customers.duplicated().sum()
        )

        # Check specifically for the ID shown in Power BI
        print("\n4. CHECK CUSTOMER C04925")

        customer = customers[
            customers["customer_id"].astype("string").str.strip()
            == "C04925"
        ]

        if customer.empty:
            print("C04925 was not found in this CSV.")
        else:
            print("Number of records for C04925:", len(customer))
            print(customer.to_string(index=False))

        print("\nCHECK COMPLETED")
