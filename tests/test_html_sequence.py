import pandas as pd
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.browser import get_driver
from utils.reporter import initialize_report, save_report
from utils.config import BASE_URL, WAIT_TIME


def validate_header_sequence(driver):
    """Validate the sequence of header tags on the specified page."""
    try:
        driver.get(BASE_URL)

        # Wait for up to WAIT_TIME seconds to find any header tag
        WebDriverWait(driver, WAIT_TIME).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h1, h2, h3, h4, h5, h6"))
        )
        headers = driver.find_elements(By.CSS_SELECTOR, "h1, h2, h3, h4, h5, h6")
        header_levels = [int(header.tag_name[1]) for header in headers]

        # Check for missing tags
        all_levels = set(range(1, 7))  # h1 to h6
        found_levels = set(header_levels)
        missing_tags = sorted(all_levels - found_levels)

        # Validate sequence
        if header_levels == sorted(header_levels) and not missing_tags:
            return "Passed", "Header tags are in correct sequence with no missing tags."
        else:
            reason = []
            if header_levels != sorted(header_levels):
                reason.append(f"Header sequence mismatch: {header_levels}")
            if missing_tags:
                reason.append(
                    f"Missing tags: {', '.join(f'h{tag}' for tag in missing_tags)}"
                )
            return "Fail", "; ".join(reason)
    except TimeoutException:
        return "Fail", "No header tags found on the page."


def test_html_sequence():
    """Test for HTML header sequence on the specified page."""
    results = initialize_report()
    driver = get_driver()

    try:
        print(f"Testing HTML sequence on: {BASE_URL}")
        status, comments = validate_header_sequence(driver)

        # Add result for the current page
        new_row = pd.DataFrame(
            [
                {
                    "Test Case": "HTML Tag Sequence Test",
                    "Status": status,
                    "Page URL": BASE_URL,
                    "Comments": comments,
                }
            ]
        )
        results = pd.concat([results, new_row], ignore_index=True)
    finally:
        driver.quit()
        save_report(results, sheet_name="HTML Tag Sequence Test")


if __name__ == "__main__":
    test_html_sequence()
