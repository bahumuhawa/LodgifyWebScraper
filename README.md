# 🏨 Lodgify Booking.com Data Intelligence

## 📌 Overview
This project is a **web scraping and data analysis tool** made to help hotel owners improve their pricing and revenue strategies. It collects hotel listings from **Booking.com**, cleans the data, saves it into a **PostgreSQL** database, and runs analysis to find useful market insights.

---

## ✨ Main Features
- 🔎 **Web Scraping** — Collect hotel names, locations, prices, ratings, and reviews from Booking.com using **Selenium + BeautifulSoup**.  
- 🧹 **Data Cleaning** — Clean and standardize messy data (prices, reviews, ratings) using **Pandas**.  
- 🗄 **Database Storage** — Save data into **PostgreSQL** with proper checks and indexes.  
- 📊 **Analysis** — Run SQL queries to find:
  - Average price per location  
  - Top 10 most reviewed hotels  
  - Average rating per location  
  - Relationship between price and review count  
- 📑 **Excel Export** — Save analysis results into an **Excel file** with multiple sheets.  

---

## 📂 Project Structure

WebScrapping/
- scraper.py # Scrapes hotel data from Booking.com
- transform.py # Cleans and transforms raw scraped data
- db_loader.py # Loads into PostgreSQL & runs analysis
- settings.py # Centralized environment configuration
- requirements.txt # Python dependencies
- .env # Environment variables (DB credentials, output dir)
- output/ # Generated CSV files
- README.md # Project documentation

---

## 🛠️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/bahumuhawa/LodgifyWebScraper
cd WebScrapping

2. Create a virtual environment
Using Conda (recommended):

conda create -n webscraper python=3.11
conda activate webscraper

3. Install dependencies
pip install -r requirements.txt

4. Configure environment variables
Create a .env file in the project root:

PGHOST=localhost
PGPORT=5432
PGDATABASE=lodgify
PGUSER=postgres
PGPASSWORD=postgres
OUTPUT_DIR=output

▶️ Usage
Step 1: Scrape hotel data
python scraper.py --url "https://www.booking.com/searchresults.html?ss=Oslo" --pages 2 --output raw_data.csv

Step 2: Clean & transform data
python transform.py --input raw_data.csv --output cleaned_data.csv

Step 3: Load into PostgreSQL & analyze
python db_loader.py --output analysis_results.xlsx

📊 Example Insights

- Average Price per Location — Compare pricing across different cities or regions.
- Top 10 Hotels by Reviews — Identify properties with the highest guest engagement.
- Average Rating per Location — Assess guest satisfaction trends by destination.
- Price vs Reviews Correlation — Measure the relationship between price levels and review volume.

⚠️ Disclaimer

This project is provided for academic purposes only (capstone project).
It is not intended for commercial use or large-scale scraping of Booking.com.
