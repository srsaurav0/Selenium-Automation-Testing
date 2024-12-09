import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse
from utils.browser import get_driver
from utils.reporter import initialize_report, save_report
from utils.config import BASE_URL

driver = get_driver()
driver.get(BASE_URL)
links = driver.find_elements(By.TAG_NAME, "a")

# Loop through each link and print its href attribute
for link in links:
    href = link.get_attribute("href")  # Get the href attribute
    if href:  # Print only if href is not None
        print(href)

print(f"Total links found: {len(links)}")  # Print the total count
driver.quit()
