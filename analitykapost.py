import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def main():
    parser = argparse.ArgumentParser(description="Supply analytics script")
    parser.add_argument("input_csv", help="Path to input CSV file")
    args = parser.parse_args()

    df = pd.read_csv(args.input_csv)

    avg_price = np.mean(df["price_per_unit"])
    median_quantity = np.median(df["quantity"])
    std_price = np.std(df["price_per_unit"], ddof=1)  

    df["total_price"] = df["quantity"] * df["price_per_unit"]
    supplier_profit = df.groupby("supplier")["total_price"].sum()
    top_supplier = supplier_profit.idxmax()

    category_totals = df.groupby("category")["quantity"].sum()

    low_supply = df[df["quantity"] < 100]
    low_supply_file = "low_supply.csv"
    low_supply.to_csv(low_supply_file, index=False)

    sorted_df = df.sort_values("total_price", ascending=False)
    print("Top 3 records by total_price:")
    print(sorted_df.head(3))

    report_text = (
        f"АНАЛІТИЧНИЙ ЗВІТ\n"
        f"===================\n\n"
        f"Середня ціна продуктів: {avg_price:.2f}\n"
        f"Медіана quantity: {median_quantity}\n"
        f"Стандартне відхилення ціни: {std_price:.2f}\n\n"
        f"Постачальник з найбільшим прибутком: {top_supplier}\n"
        f"Файл з дефіцитними поставками: {low_supply_file}\n"
    )

    with open("report.txt", "w", encoding="utf-8") as f:
        f.write(report_text)

    print("\nReport saved as report.txt")

    plt.figure(figsize=(8, 5))
    category_totals.plot(kind="bar")
    plt.title("Quantity distribution by category")
    plt.xlabel("Category")
    plt.ylabel("Total quantity")
    plt.tight_layout()
    plt.savefig("category_distribution.png")
    print("Chart saved as category_distribution.png")


if name == "__main__":
    main()