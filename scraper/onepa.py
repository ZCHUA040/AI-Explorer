import pandas as pd

#Chrome driver version 134
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# Configure Chrome options
options = webdriver.ChromeOptions()
options.headless = False  # Enable headless mode
options.add_argument("--window-sizea=1920,1200")  # Set the window size

# Set the path to the Chromedriver
DRIVER_PATH = './chromedriver.exe'


def activesg():
    """
    Function to get all ActiveSG facilities from the webpage by handling pagination.
    
    Output: pandas dataframe
    """
    # Initialize the Chrome driver with the specified options
    service = Service(executable_path=DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)

    # Open the ActiveSG facilities page
    driver.get("https://www.onepa.gov.sg/events/search?events=&aoi=Parenting%20%26%20Education&sort=rel")

    try:
        # Wait for the facilities list to load
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "btnNext"))
        )
    except Exception:
        pass
    # Create a list to store all facility data
    all_facility_data = []

    # Start pagination loop to go through all pages
    while True:
        # Extract all the rows containing facility information (adjust CSS selector based on actual structure)
        facilities = driver.find_elements(By.CLASS_NAME, "serp-grid__item")
        # Extract facility details for this page
        for facility in facilities:
            name = facility.find_element(By.CLASS_NAME, "serp-grid__item__left__label").text
            location = facility.find_element(By.CLASS_NAME, "serp-grid__item__left__location").text
            if "workshop" in name.lower() or "course" in name.lower() or "class" in name.lower():
                type_ = "Workshops & Classes"
            else:
                type_ = "Social & Community Events"
            time = facility.find_element(By.CSS_SELECTOR, ".serp-grid__item__left__icons span:nth-of-type(2) span").text
            price = facility.find_element(By.CLASS_NAME, "serp-grid__item__right__discount--member").text
            # Store the data in a dictionary
            facility_info = {
                "Name": name,
                "Location": location,
                "Type": type_,
                "Time": time,
                "Price": price
            }
            
            all_facility_data.append(facility_info)
        # Try to click the "Next" button to go to the next page (adjust the button selector if needed)
        try:
            next_button = driver.find_element(By.XPATH, "//span[@class='btnNext']")
            if next_button.is_enabled():
                ActionChains(driver).move_to_element(next_button).click().perform()
                WebDriverWait(driver, 10).until(
                    EC.staleness_of(facilities[0])  # Wait for the page to reload
                )
            else:
                break  # No more pages, exit the loop
        except Exception as e:
            print("Error or reached the last page:", e)
            break

    # Convert the data into a pandas DataFrame
    df = pd.DataFrame(all_facility_data)

    # Close the browser
    driver.quit()

    return df

facilities_df = activesg()

# Save the DataFrame to a CSV file
facilities_df.to_csv("onepa_events.csv", mode='a', index=False, header=False)