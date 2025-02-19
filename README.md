# redbus_datascrap_with_streamlite
This RedBus Data Scraper &amp; Analyzer automates bus data extraction using Selenium, stores it in an SQLite database, and analyzes it via Streamlit. It scrapes details like price, rating, and availability, saves them in bus_details.db, and provides insights on cheapest, fastest, and highest-rated buses for easy comparison.

Features
Automated Web Scraping: Extracts bus details (price, rating, availability, etc.) from RedBus.
Database Storage: Saves extracted data in an SQLite database (bus_details.db).
Data Analysis: Identifies the cheapest, fastest, and highest-rated buses.
Streamlit Dashboard: Provides an interactive UI for viewing and comparing results.

Installation
# Clone the repository
git clone https://github.com/your-repo/redbus_scraper.git
cd redbus_scraper

# Install dependencies
pip install -r requirements.txt

Usage
1. Run the Scraper
  python redbus_scraper.py
This launches Selenium, scrapes bus data, and saves it in bus_details.db.

2. Launch Streamlit Dashboard
  streamlit run redbus_dashboard.py
This starts an interactive dashboard to explore and analyze the data.

Requirements
Python 3.7+
Google Chrome & ChromeDriver
Dependencies (see requirements.txt)

Refer for Detailed Documentation - https://docs.google.com/document/d/1lCeWoNuBkFichOww_ZWamTo9NWYG6H5ZbhBgB3IkAyY/edit?usp=sharing
