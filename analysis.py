import pandas as pd
import argparse


def analyze(output_file, csv_file="cleaned_data.csv"):
    results = {}

    # Read CSV
    df = pd.read_csv(csv_file)

    # 1. Average price per location
    if "price_numeric" in df.columns and "location" in df.columns:
        results["avg_price_per_location"] = (
            df.groupby("location")["price_numeric"]
            .mean()
            .round(2)
            .reset_index()
            .sort_values("price_numeric", ascending=False)
        )

    # 2. Top 10 most reviewed hotels
    if "review_count_numeric" in df.columns and "hotel_name" in df.columns:
        results["top_hotels_by_reviews"] = (
            df[["hotel_name", "location", "review_count_numeric"]]
            .dropna(subset=["review_count_numeric"])
            .sort_values("review_count_numeric", ascending=False)
            .head(10)
        )

    # 3. Average rating by location
    if "rating" in df.columns and "location" in df.columns:
        df["rating_numeric"] = pd.to_numeric(df["rating"], errors="coerce")
        results["avg_rating_per_location"] = (
            df.groupby("location")["rating_numeric"]
            .mean()
            .round(2)
            .reset_index()
            .sort_values("rating_numeric", ascending=False)
        )

    # 4. Price vs Reviews correlation
    if "price_numeric" in df.columns and "review_count_numeric" in df.columns:
        corr_df = df[["price_numeric", "review_count_numeric"]].dropna()
        results["price_reviews_corr"] = corr_df.corr().iloc[0, 1]

    # Save results to Excel
    with pd.ExcelWriter(output_file) as writer:
        for name, df_or_val in results.items():
            if isinstance(df_or_val, pd.DataFrame):
                df_or_val.to_excel(writer, sheet_name=name, index=False)
            else:
                pd.DataFrame([{"correlation": df_or_val}]).to_excel(
                    writer, sheet_name=name, index=False
                )

    print(f"✅ Analysis results saved to {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="analysis_results.xlsx")
    args = parser.parse_args()

    analyze(args.output)
