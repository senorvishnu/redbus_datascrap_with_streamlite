from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

# Predefined city IDs
CITY_IDS = {
    "Bangalore": 122,
    "Chennai": 123,
    "Coimbatore": 124,
    "Hyderabad": 125,
    "Mumbai": 126,
    "Pune": 127,
    "Delhi": 128,
    "Kolkata": 129,
    "Ahmedabad": 130,
    "Jaipur": 131
}

# Function to get user input
def get_user_input():
    source = input("Enter Source City: ").strip()
    destination = input("Enter Destination City: ").strip()
    travel_date = input("Enter Travel Date (YYYY-MM-DD): ").strip()
    print(f"User Input - Source: {source}, Destination: {destination}, Travel Date: {travel_date}")
    return source, destination, travel_date

# Function to construct the RedBus URL dynamically
def get_redbus_url(source, destination, travel_date):
    source_id = CITY_IDS.get(source, None)
    destination_id = CITY_IDS.get(destination, None)
    
    if source_id is None or destination_id is None:
        print("Invalid city name. Please use a predefined city.")
        return None
    
    base_url = "https://www.redbus.in/search?fromCityName={}&fromCityId={}&toCityName={}&toCityId={}&busType=Any&opId=0&rDoj=&returnDoj=&isReturn=false&onward={}&srcCountry=IND&destCountry=IND"
    url = base_url.format(source.replace(" ", "%20"), source_id, destination.replace(" ", "%20"), destination_id, travel_date)
    print(f"Constructed URL: {url}")
    return url

# Function to initialize Selenium WebDriver
def initialize_driver():
    print("Initializing WebDriver...")
    driver = webdriver.Chrome()
    driver.maximize_window()
    return driver

# Function to scrape bus details
def scrape_bus_details(driver, url):
    if url is None:
        return []
    
    try:
        print("Opening RedBus URL...")
        driver.get(url)
        time.sleep(5)  # Allow the page to load

        print("Scrolling down to load all bus items...")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)

        print("Extracting bus details...")
        bus_name_elements = driver.find_elements(By.CLASS_NAME, "travels.lh-24.f-bold.d-color")
        bus_type_elements = driver.find_elements(By.CLASS_NAME, "bus-type.f-12.m-top-16.l-color.evBus")
        departing_time_elements = driver.find_elements(By.CLASS_NAME, "dp-time.f-19.d-color.f-bold")
        duration_elements = driver.find_elements(By.CLASS_NAME, "dur.l-color.lh-24")
        reaching_time_elements = driver.find_elements(By.CLASS_NAME, "bp-time.f-19.d-color.disp-Inline")
        star_rating_elements = driver.find_elements(By.XPATH, "//div[@class='rating-sec lh-24']")
        price_elements = driver.find_elements(By.CLASS_NAME, "fare.d-block")

        seat_availability_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'seat-left m-top-30') or contains(@class, 'seat-left m-top-16')]")

        bus_details = []
        for i in range(len(bus_name_elements)):
            bus_detail = {
                "Bus_Name": bus_name_elements[i].text,
                "Bus_Type": bus_type_elements[i].text,
                "Departing_Time": departing_time_elements[i].text,
                "Duration": duration_elements[i].text,
                "Reaching_Time": reaching_time_elements[i].text,
                "Star_Rating": star_rating_elements[i].text if i < len(star_rating_elements) else '0',
                "Price": price_elements[i].text,
                "Seat_Availability": seat_availability_elements[i].text if i < len(seat_availability_elements) else '0'
            }
            bus_details.append(bus_detail)
        
        print(f"Total Buses Found: {len(bus_details)}")
        return bus_details

    except Exception as e:
        print(f"Error while scraping: {str(e)}")
        return []

# Main script execution
if __name__ == "__main__":
    source, destination, travel_date = get_user_input()
    url = get_redbus_url(source, destination, travel_date)

    driver = initialize_driver()
    bus_data = scrape_bus_details(driver, url)

    df = pd.DataFrame(bus_data)
    df.to_csv('bus_details.csv', index=False)
    
    print("Bus details saved to bus_details.csv")
    driver.quit()