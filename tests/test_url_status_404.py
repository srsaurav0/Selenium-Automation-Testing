import pandas as pd
import requests
from requests.exceptions import RequestException
from selenium.webdriver.common.by import By
from utils.browser import get_driver
from utils.reporter import save_report
from utils.config import BASE_URL, WAIT_TIME


# Dictionary of common HTTP status codes and their meanings
HTTP_STATUS_DESCRIPTIONS = {
    404: "Not Found: The requested resource was not found.",
    400: "Bad Request: The server could not understand the request.",
    500: "Internal Server Error: The server encountered an error.",
    503: "Service Unavailable: The server is temporarily unable to handle the request.",
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


def validate_url_status(url):
    """Validate the status code of a URL for 404 and broken links."""
    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        status_code = response.status_code
        if status_code == 404:
            return False, f"{url} (404: {HTTP_STATUS_DESCRIPTIONS[404]})"
        elif status_code in HTTP_STATUS_DESCRIPTIONS:
            return False, f"{url} ({status_code}: {HTTP_STATUS_DESCRIPTIONS[status_code]})"
        else:
            return True, None  # Pass if status code is not 404 or broken
    except RequestException as e:
        return False, f"{url} (Request error: {str(e)})."


def test_404():
    """Test for 404 errors and broken links on all links of the specified page."""
    driver = get_driver()
    failed_links = []  # Collect failed links for comments

    try:
        print(f"Fetching links from: {BASE_URL}")
        driver.get(BASE_URL)
        links = get_all_links(driver)

        for link in links:
            # print(f"Checking link: {link}")
            success, error_message = validate_url_status(link)
            if not success:
                failed_links.append(error_message)

    finally:
        driver.quit()

    # Determine overall test status and comments
    if failed_links:
        status = "Fail"
        comments = f"Broken or 404 links: {', \n'.join(failed_links)}"
    else:
        status = "Pass"
        comments = "All links are accessible, no 404 errors found."

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
