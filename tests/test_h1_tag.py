import pandas as pd
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.browser import get_driver
from utils.reporter import initialize_report, save_report
from utils.config import BASE_URL, WAIT_TIME



def check_h1_tag(driver):
    """Check for H1 tag on the given page and ensure only one exists."""
    try:
        driver.get(BASE_URL)

        # Wait for up to WAIT_TIME seconds to find the H1 tag
        WebDriverWait(driver, WAIT_TIME).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        )
        h1_tags = driver.find_elements(By.TAG_NAME, "h1")

        # Check the number of H1 tags and set status and comments
        if len(h1_tags) == 1:
            return "Passed", "H1 tag exists."
        elif len(h1_tags) == 0:
            return "Fail", "No H1 tag found."
        else:
            return "Fail", f"Multiple H1 tags found: {len(h1_tags)}"
    except TimeoutException:
        return "Fail", "Timeout: Unable to find H1 tag."


def test_h1_tag():
    """Test for H1 tag on the specified page."""
    results = initialize_report()
    driver = get_driver()

    try:
        print(f"Testing H1 tag on: {BASE_URL}")
        status, comments = check_h1_tag(driver)

        # Add result for the current page
        new_row = pd.DataFrame(
            [
                {
                    "Test Case": "H1 Tag Test",
                    "Status": status,
                    "Page URL": BASE_URL,
                    "Comments": comments,
                }
            ]
        )
        results = pd.concat([results, new_row], ignore_index=True)
    finally:
        driver.quit()
        save_report(results, sheet_name="H1 Tag Test")


if __name__ == "__main__":
    test_h1_tag()
