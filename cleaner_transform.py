import pandas as pd
import re
import argparse


def clean_price(price):
    if pd.isna(price):
        return None
    price = re.sub(r"[^\d.]", "", str(price))
    return float(price) if price else None


def clean_reviews(reviews):
    if pd.isna(reviews):
        return None
    match = re.search(r"\d+", str(reviews).replace(",", ""))
    return int(match.group(0)) if match else None


def clean_rating(rating):
    if pd.isna(rating):
        return None
    match = re.search(r"\d+(\.\d+)?", str(rating))
    return float(match.group(0)) if match else None


def transform(df):
    df["price_numeric"] = df["price_display"].apply(clean_price)
    df["review_count_numeric"] = df["review_count"].apply(clean_reviews)
    df["rating"] = df["rating"].apply(clean_rating)
    df["hotel_name"] = df["hotel_name"].str.strip()
    df["location"] = df["location"].str.strip()
    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="raw_data.csv")
    parser.add_argument("--output", default="cleaned_data.csv")
    args = parser.parse_args()

    data = pd.read_csv(args.input)
    cleaned = transform(data)
    cleaned.to_csv(args.output, index=False)
    print(f"Cleaned data saved to {args.output}")
