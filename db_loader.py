import psycopg2
import pandas as pd
import argparse
import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("PGHOST", "localhost")
DB_PORT = os.getenv("PGPORT", "5432")
DB_NAME = os.getenv("PGDATABASE", "lodgify")
DB_USER = os.getenv("PGUSER", "postgres")
DB_PASS = os.getenv("PGPASSWORD", "postgres")


def connect_db():
    return psycopg2.connect(
        host=DB_HOST, port=DB_PORT, database=DB_NAME, user=DB_USER, password=DB_PASS
    )


def fetch_dataframe(query):
    conn = connect_db()
    df = pd.read_sql(query, conn)
    conn.close()
    return df


def analyze(output_file):
    results = {}

    # 1. Average price per location
    q1 = """
    SELECT location, ROUND(AVG(price_numeric),2) AS avg_price
    FROM booking_competitor_data
    WHERE price_numeric IS NOT NULL
    GROUP BY location
    ORDER BY avg_price DESC;
    """
    results["avg_price_per_location"] = fetch_dataframe(q1)

    # 2. Top 10 most reviewed hotels
    q2 = """
    SELECT hotel_name, location, review_count_numeric
    FROM booking_competitor_data
    WHERE review_count_numeric IS NOT NULL
    ORDER BY review_count_numeric DESC
    LIMIT 10;
    """
    results["top_hotels_by_reviews"] = fetch_dataframe(q2)

    # 3. Average rating by location
    q3 = """
    SELECT location, ROUND(AVG(rating),2) AS avg_rating
    FROM booking_competitor_data
    WHERE rating IS NOT NULL
    GROUP BY location
    ORDER BY avg_rating DESC;
    """
    results["avg_rating_per_location"] = fetch_dataframe(q3)

    # 4. Price vs Reviews correlation
    q4 = """
    SELECT price_numeric, review_count_numeric
    FROM booking_competitor_data
    WHERE price_numeric IS NOT NULL AND review_count_numeric IS NOT NULL;
    """
    corr_df = fetch_dataframe(q4)
    results["price_reviews_corr"] = corr_df.corr().iloc[0, 1]

    # Save results to Excel
    with pd.ExcelWriter(output_file) as writer:
        for name, df in results.items():
            if isinstance(df, pd.DataFrame):
                df.to_excel(writer, sheet_name=name, index=False)
            else:
                pd.DataFrame([{"correlation": df}]).to_excel(
                    writer, sheet_name=name, index=False
                )

    print(f"Analysis results saved to {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="analysis_results.xlsx")
    args = parser.parse_args()

    analyze(args.output)
