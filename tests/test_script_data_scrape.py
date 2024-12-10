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
    """Convert a JavaScript object string to valid JSON."""
    js_object = re.sub(r"([{,])\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*:", r'\1"\2":', js_object)
    js_object = js_object.replace("null", "null").replace("true", "true").replace("false", "false")
    return js_object


def extract_script_data(driver):
    """Extract the required data from the <script> tags."""
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
        WebDriverWait(driver, WAIT_TIME).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "script"))
        )

        scripts = driver.find_elements(By.TAG_NAME, "script")
        for script in scripts:
            script_content = script.get_attribute("innerHTML")

            # Extract CampaignID
            if "CampaignId" in script_content:
                match = re.search(r"CampaignId\s*:\s*['\"](.*?)['\"]", script_content)
                if match:
                    data["CampaignID"] = match.group(1)

            # Extract ScriptData
            if "var ScriptData =" in script_content:
                match = re.search(r"var ScriptData = ({.*?});", script_content, re.DOTALL)
                if match:
                    script_data = match.group(1)
                    script_data = preprocess_js_object(script_data)
                    script_data_dict = json.loads(script_data)

                    # Extract specific fields
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


def save_data_to_report(data, file_path, sheet_name):
    """
    Append data to an existing Excel file or create a new sheet.
    
    Args:
        data (list): Data to be saved.
        file_path (str): Path to the Excel file.
        sheet_name (str): Name of the sheet to save the data.
    """
    df = pd.DataFrame(data)

    try:
        with pd.ExcelWriter(file_path, engine="openpyxl", mode="a", if_sheet_exists="new") as writer:
            df.to_excel(writer, index=False, sheet_name=sheet_name)
        print(f"Data appended to {file_path} in sheet '{sheet_name}'.")
    except FileNotFoundError:
        print(f"File {file_path} not found. Creating a new one.")
        with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name=sheet_name)
        print(f"File created with data in sheet '{sheet_name}'.")


def scrape_script_data():
    """Scrape data from <script> tags and save to the main report."""
    driver = get_driver()
    results = []

    try:
        print(f"Scraping script data from: {BASE_URL}")
        data = extract_script_data(driver)
        results.append(data)
    finally:
        driver.quit()

    # Save data to the main report file
    save_data_to_report(results, "./output/test_results.xlsx", "Script Data")


if __name__ == "__main__":
    scrape_script_data()
