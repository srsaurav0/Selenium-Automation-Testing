import pandas as pd
import re
import json
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.browser import get_driver
from utils.config import BASE_URL, WAIT_TIME


def preprocess_js_object(js_object):
    """
    Convert a JavaScript object string to valid JSON.

    Args:
        js_object (str): The JavaScript object as a string.

    Returns:
        str: The valid JSON string.
    """
    # Add double quotes around unquoted property names
    js_object = re.sub(r"([{,])\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*:", r'\1"\2":', js_object)

    # Replace JavaScript-specific values with JSON-compatible values
    js_object = (
        js_object.replace("null", "null")
        .replace("true", "true")
        .replace("false", "false")
    )

    return js_object


def extract_script_data(driver):
    """
    Extract the required data from the <script> tags.

    Returns:
        A dictionary containing extracted fields.
    """
    data = {
        "SiteURL": None,
        "CampaignID": None,
        "SiteName": None,
        "Browser": None,
        "CountryCode": None,
        "IP": None,
    }

    try:
        driver.get(BASE_URL)

        # Wait for the page to load and the script tag to appear
        WebDriverWait(driver, WAIT_TIME).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "script"))
        )

        # Find all <script> tags
        scripts = driver.find_elements(By.TAG_NAME, "script")

        for script in scripts:
            script_content = script.get_attribute("innerHTML")

            # Extract CampaignID from the body script
            if "CampaignId" in script_content:
                try:
                    # Parse as JSON-like content using regex
                    match = re.search(
                        r"CampaignId\s*:\s*['\"](.*?)['\"]", script_content
                    )
                    if match:
                        data["CampaignID"] = match.group(1)
                except Exception as e:
                    print(f"Error parsing CampaignID: {str(e)}")

            # Look for the ScriptData variable in other scripts
            if "var ScriptData =" in script_content:
                # Extract the JSON-like content using regex
                match = re.search(
                    r"var ScriptData = ({.*?});", script_content, re.DOTALL
                )
                if match:
                    script_data = match.group(1)

                    # Preprocess the JavaScript object to be valid JSON
                    script_data = preprocess_js_object(script_data)

                    # Parse as JSON
                    script_data_dict = json.loads(script_data)

                    # Extract required fields
                    data["SiteURL"] = script_data_dict["config"]["SiteUrl"]
                    data["SiteName"] = script_data_dict["config"]["SiteName"]
                    data["Browser"] = script_data_dict["userInfo"]["Browser"]
                    data["CountryCode"] = script_data_dict["userInfo"]["CountryCode"]
                    data["IP"] = script_data_dict["userInfo"]["IP"]

    except TimeoutException:
        print(f"Timeout: Unable to extract script data after {WAIT_TIME} seconds.")
    except Exception as e:
        print(f"Error while extracting script data: {str(e)}")

    return data


def scrape_script_data():
    """Scrape data from <script> tags and save to Excel."""
    driver = get_driver()
    results = []

    try:
        print(f"Scraping script data from: {BASE_URL}")
        data = extract_script_data(driver)
        results.append(data)
    finally:
        driver.quit()

    # Save results to Excel
    results_df = pd.DataFrame(results)
    results_df.to_excel(
        "./output/script_data.xlsx", index=False, sheet_name="Script Data"
    )
    print("Script data saved to ./output/script_data.xlsx")


if __name__ == "__main__":
    scrape_script_data()
