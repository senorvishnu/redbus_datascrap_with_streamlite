import streamlit as st
import sqlite3
import pandas as pd
from redbus import scrape_bus_details, get_redbus_url, initialize_driver
from database_utils import create_database, store_data_in_db

CITY_IDS = {
    "Bangalore": 122, "Chennai": 123, "Coimbatore": 124, "Hyderabad": 125,
    "Mumbai": 126, "Pune": 127, "Delhi": 128, "Kolkata": 129,
    "Ahmedabad": 130, "Jaipur": 131
}

def fetch_data_from_db(query):
    conn = sqlite3.connect("bus_details.db")
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

st.title("RedBus Data Scraper & Analyzer")

# User Input Section
st.header("Search for Buses")
from_city = st.selectbox("From City", list(CITY_IDS.keys()))
to_city = st.selectbox("To City", list(CITY_IDS.keys()))
travel_date = st.date_input("Travel Date")

if st.button("Scrape & Store Data"):
    url = get_redbus_url(from_city, to_city, str(travel_date))
    if url:
        driver = initialize_driver()
        bus_data = scrape_bus_details(driver, url)
        driver.quit()
        
        if bus_data:
            create_database()
            store_data_in_db([(
                bus["Bus_Name"], bus["Bus_Type"], bus["Departing_Time"],
                bus["Duration"], bus["Reaching_Time"], bus["Star_Rating"],
                bus["Price"], bus["Seat_Availability"]
            ) for bus in bus_data])
            st.success("Data Scraped & Stored Successfully!")
        else:
            st.error("No data found.")

st.header("Analyze Stored Data")
query_options = {
    "Show All Data": "SELECT * FROM bus_details",
    "Top 5 Cheapest Buses": "SELECT * FROM bus_details ORDER BY CAST(Price AS INTEGER) ASC LIMIT 5",
    "Top 5 Fastest Buses": "SELECT * FROM bus_details ORDER BY Duration ASC LIMIT 5",
    "Buses with Ratings Above 4.0": "SELECT * FROM bus_details WHERE CAST(Star_Rating AS FLOAT) > 4.0",
    "Buses with Available Seats": "SELECT * FROM bus_details WHERE CAST(Seat_Availability AS INTEGER) > 0",
    "Count of Buses per Type": "SELECT Bus_Type, COUNT(*) as count FROM bus_details GROUP BY Bus_Type",
    "Earliest Departing Bus": "SELECT * FROM bus_details ORDER BY Departing_Time ASC LIMIT 1",
    "Latest Departing Bus": "SELECT * FROM bus_details ORDER BY Departing_Time DESC LIMIT 1",
    "Most Expensive Bus": "SELECT * FROM bus_details ORDER BY CAST(Price AS INTEGER) DESC LIMIT 1",
    "Cheapest Bus": "SELECT * FROM bus_details ORDER BY CAST(Price AS INTEGER) ASC LIMIT 1"
}

selected_query = st.selectbox("Select a Query", list(query_options.keys()))
if st.button("Run Query"):
    result_df = fetch_data_from_db(query_options[selected_query])
    st.dataframe(result_df)
