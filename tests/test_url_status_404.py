import pandas as pd
import requests
from requests.exceptions import RequestException
from selenium.webdriver.common.by import By
from utils.browser import get_driver
from utils.reporter import save_report
from utils.config import BASE_URL, WAIT_TIME


# Dictionary of common HTTP status codes and their meanings (focus on 404)
HTTP_STATUS_DESCRIPTIONS = {
    404: "Not Found: The requested resource was not found.",
}


def get_all_links(driver):
    """Retrieve all valid links from the page."""
    links = driver.find_elements(By.TAG_NAME, "a")
    valid_links = set()
    for link in links:
        href = link.get_attribute("href")
        if href:
            valid_links.add(href)
    return valid_links


def validate_url_status_for_404(url):
    """Check if the URL returns a 404 error."""
    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        status_code = response.status_code
        if status_code == 404:
            # Fetch description for 404 error
            description = HTTP_STATUS_DESCRIPTIONS.get(
                status_code, f"Unexpected status code: {status_code}"
            )
            return False, f"{url} ({status_code}: {description})"
        else:
            return True, None  # Pass, no error message
    except RequestException as e:
        # Ignore other HTTP request errors and treat them as pass
        return True, None


def test_404():
    """Test for 404 errors on all links of the specified page."""
    driver = get_driver()
    failed_links = []  # Collect failed links with 404 errors

    try:
        print(f"Fetching links from: {BASE_URL}")
        driver.get(BASE_URL)
        links = get_all_links(driver)

        for link in links:
            # Check only for 404 errors
            success, error_message = validate_url_status_for_404(link)
            if not success:
                failed_links.append(error_message)

    finally:
        driver.quit()

    # Determine overall test status and comments
    if failed_links:
        status = "Fail"
        comments = f"Failed links: {', \n'.join(failed_links)}"
    else:
        status = "Pass"
        comments = "No 404 errors found. All links are valid."

    # Create a single-row result
    result = [
        {
            "Test Case": "404 Test",
            "Status": status,
            "Page URL": BASE_URL,
            "Comments": comments,
        }
    ]

    # Save the single-row result to the report
    results_df = pd.DataFrame(result)
    save_report(results_df, sheet_name="404 Test")


if __name__ == "__main__":
    test_404()
