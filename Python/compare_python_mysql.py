r"""Compare Python cleaned orders with a complete MySQL order export.

Run from the project root:
    python. \Python\compare_python_mysql.py
Optional:
    python. \Python\compare_python_mysql.py --mysql "path\to\mysql_orders_reconciled.csv"
"""
import argparse
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PYTHON_FILE = ROOT / "Data" / "processed" / "orders_cleaned.csv"
DEFAULT_MYSQL_FILE = ROOT / "Data" / "analysis_outputs" / "mysql_orders_reconciled.csv"
OUTPUT_FILE = ROOT / "Data" / "analysis_outputs" / "python_mysql_comparison.csv"
FINANCIAL_COLUMNS = [
    "gross_sales", "discount_amount", "net_revenue", "product_cost", "profit"
]
REQUIRED_COLUMNS = ["order_id", *FINANCIAL_COLUMNS]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mysql", type=Path, default=DEFAULT_MYSQL_FILE,
                        help="Path to complete MySQL CSV export (default: Data/analysis_outputs/mysql_orders_reconciled.csv)")
    args = parser.parse_args()

    if not PYTHON_FILE.exists():
        raise FileNotFoundError(f"Python cleaned dataset not found: {PYTHON_FILE}")
    if not args.mysql.exists():
        raise FileNotFoundError(
            f"MySQL export not found: {args.mysql}\n"
            "Export all 50,000 rows from MySQL and save it at the default path, "
            "or pass its path with --mysql."
        )

    py = pd.read_csv(PYTHON_FILE)
    sql = pd.read_csv(args.mysql)
    py.columns = py.columns.str.strip().str.lower()
    sql.columns = sql.columns.str.strip().str.lower()

    for label, df in (("Python", py), ("MySQL", sql)):
        missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
        if missing:
            raise ValueError(f"{label} export is missing required columns: {missing}")
        df["order_id"] = df["order_id"].astype(str).str.strip()
        if df["order_id"].duplicated().any():
            examples = df.loc[df["order_id"].duplicated(), "order_id"].head().tolist()
            raise ValueError(f"{label} export has duplicate order IDs, e.g. {examples}")

    merged = py[REQUIRED_COLUMNS].merge(
        sql[REQUIRED_COLUMNS], on="order_id", how="outer",
        suffixes=("_python", "_mysql"), indicator=True, validate="one_to_one"
    )
    print(f"Python rows: {len(py):,} | unique order IDs: {py.order_id.nunique():,}")
    print(f"MySQL rows:  {len(sql):,} | unique order IDs: {sql.order_id.nunique():,}")
    print("\nOrder matching:")
    print(merged["_merge"].value_counts().to_string())

    matched = merged[merged["_merge"] == "both"].copy()
    print("\nFinancial comparison (matched orders only):")
    rows = []
    for col in FINANCIAL_COLUMNS:
        a = pd.to_numeric(matched[f"{col}_python"], errors="coerce")
        b = pd.to_numeric(matched[f"{col}_mysql"], errors="coerce")
        diff = b - a
        rows.append({
            "metric": col,
            "python_total": round(a.sum(), 2),
            "mysql_total_matched_orders": round(b.sum(), 2),
            "difference_mysql_minus_python": round(diff.sum(), 2),
            "orders_different_exactly": int((diff.abs() > 1e-9).sum()),
            "orders_difference_over_1_paisa": int((diff.abs() > 0.01 + 1e-9).sum()),
            "max_absolute_order_difference": round(diff.abs().max(), 6) if len(diff) else None,
        })
    result = pd.DataFrame(rows)
    print(result.to_string(index=False))

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    merged.to_csv(OUTPUT_FILE, index=False)
    result.to_csv(OUTPUT_FILE.with_name("python_mysql_financial_summary.csv"), index=False)
    print(f"\nDetailed row-level report: {OUTPUT_FILE}")
    print(f"Financial summary: {OUTPUT_FILE.with_name('python_mysql_financial_summary.csv')}")

    if (merged["_merge"] != "both").any():
        raise SystemExit("\nRECONCILIATION FAILED: order coverage is incomplete. See matching counts above.")
    if not (result["orders_different_exactly"] == 0).all():
        raise SystemExit("\nRECONCILIATION FAILED: financial values differ for matched orders.")
    print("\nRECONCILIATION PASSED: all order IDs and financial values match exactly.")

if __name__ == "__main__":
    main()
