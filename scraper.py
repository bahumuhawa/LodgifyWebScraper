import re
import csv
import time
import argparse
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def init_driver(headless=True):
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=options)


def parse_listing(card):
    data = {
        "hotel_name": None,
        "location": None,
        "price_display": None,
        "rating": None,
        "review_count": None,
        "scrape_time": time.strftime("%Y-%m-%d %H:%M:%S"),
    }

    # Hotel name
    name = card.select_one("[data-testid='title']")
    if name:
        data["hotel_name"] = name.get_text(strip=True)

    # Location
    loc = card.select_one("[data-testid='address']")
    if loc:
        data["location"] = loc.get_text(strip=True)

    # Price (try multiple selectors for safety)
    price = (
        card.select_one("[data-testid='price-and-discounted-price']")
        or card.select_one("span[data-testid='price']")
        or card.select_one("div[data-testid='price-display']")
    )
    if price:
        data["price_display"] = price.get_text(strip=True)

    # Rating (fix "Scored" issue → only number)
    rating = card.select_one("[data-testid='review-score'] .bui-review-score__badge")
    if rating:
        rating_text = rating.get_text(strip=True)
        match = re.search(r"\d+(\.\d+)?", rating_text)
        if match:
            data["rating"] = match.group()

    # Review count (extract numbers reliably)
    reviews = card.select_one("[data-testid='review-score'] .bui-review-score__text")
    if reviews:
        review_text = reviews.get_text(strip=True)
        match = re.search(r"\d[\d,]*", review_text)
        if match:
            data["review_count"] = match.group().replace(",", "")

    return data


def scrape(url, pages):
    driver = init_driver(
        headless=False
    )  # headless=True if you don’t want the browser window
    results = []

    driver.get(url)

    for page in range(1, pages + 1):
        print(f"Scraping page {page}...")

        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "[data-testid='property-card']")
            )
        )

        soup = BeautifulSoup(driver.page_source, "lxml")
        cards = soup.select("[data-testid='property-card']")

        for card in cards:
            results.append(parse_listing(card))

        # Next page button
        try:
            next_btn = driver.find_element(
                By.CSS_SELECTOR, "button[aria-label='Next page']"
            )
            driver.execute_script("arguments[0].click();", next_btn)
            time.sleep(3)
        except:
            print("No more pages found.")
            break

    driver.quit()
    return results


def save_csv(data, filename):
    keys = data[0].keys()
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)
    print(f"Saved {len(data)} records to {filename}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    parser.add_argument("--pages", type=int, default=1)
    parser.add_argument("--output", default="raw_data.csv")
    args = parser.parse_args()

    scraped_data = scrape(args.url, args.pages)
    if scraped_data:
        save_csv(scraped_data, args.output)
