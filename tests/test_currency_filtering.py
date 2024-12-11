import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from utils.browser import get_driver
from utils.reporter import save_report
from utils.config import BASE_URL, WAIT_TIME


CURRENCY_MAP = {
    "US": "USD",
    "CA": "CAD",
    "BE": "EUR",
    "IE": "GBP",
    "AU": "AUD",
    "SG": "SGD",
    "AE": "AED",
    "BD": "BDT",
}


def change_currency_and_verify_all(driver, country_code, currency_symbol):
    """
    Change the currency using the dropdown and verify that all price elements update.

    Args:
        driver: Selenium WebDriver instance.
        country_code: The 2-letter country code (e.g., 'US', 'CA').
        currency_symbol: The expected currency symbol (e.g., '$', '€').

    Returns:
        bool: True if all elements updated correctly, False otherwise.
        list: A list of error messages for elements that failed.
    """
    errors = []

    try:
        # Locate and interact with the dropdown
        dropdown = driver.find_element(By.ID, "js-currency-sort-footer")
        driver.execute_script("arguments[0].scrollIntoView(true);", dropdown)
        driver.execute_script("arguments[0].click();", dropdown)

        # Select the currency option
        option = WebDriverWait(driver, WAIT_TIME).until(
            EC.presence_of_element_located((By.XPATH, f"//li[@data-currency-country='{country_code}']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", option)
        driver.execute_script("arguments[0].click();", option)

        # Wait for the prices to update
        WebDriverWait(driver, WAIT_TIME).until(
            EC.text_to_be_present_in_element((By.CLASS_NAME, "js-price-value"), currency_symbol)
        )

        # Validate all price elements on the page
        price_elements = driver.find_elements(By.CLASS_NAME, "js-price-value")
        for element in price_elements:
            price_text = element.text
            # print(price_text)
            if currency_symbol not in price_text:
                errors.append(f"Currency mismatch in element: {price_text}")

    except TimeoutException:
        errors.append(f"Timeout: Failed to load or update currency for {CURRENCY_MAP[country_code]} ({currency_symbol}).")

    return len(errors) == 0, errors  # True if no errors, otherwise False and error list


def test_currency_filtering():
    """Test for currency filtering and property price updates across all price elements."""
    driver = get_driver()
    test_cases = [
        {"currency_code": "US", "currency_symbol": "$"},
        {"currency_code": "CA", "currency_symbol": "$"},
        {"currency_code": "BE", "currency_symbol": "€"},
        {"currency_code": "IE", "currency_symbol": "£"},
        {"currency_code": "AU", "currency_symbol": "$"},
        {"currency_code": "SG", "currency_symbol": "$"},
        {"currency_code": "AE", "currency_symbol": "د.إ."},
        {"currency_code": "BD", "currency_symbol": "৳"},
    ]

    failed_currencies = []  # Collect currencies that failed
    try:
        driver.get(BASE_URL)

        for case in test_cases:
            print(f"Testing currency: {CURRENCY_MAP[case['currency_code']]} ({case['currency_symbol']})")
            success, errors = change_currency_and_verify_all(driver, case["currency_code"], case["currency_symbol"])
            if not success:
                failed_currencies.append(f"{CURRENCY_MAP[case['currency_code']]} ({case['currency_symbol']}): {', '.join(errors)}")
    finally:
        driver.quit()

    # Determine overall status and comments
    if failed_currencies:
        status = "Fail"
        comments = f"Failed currencies: {', '.join(failed_currencies)}"
    else:
        status = "Passed"
        comments = "All currencies updated successfully for all price elements."

    # Create a single-row result
    result = [
        {
            "Test Case": "Currency Filtering Test",
            "Status": status,
            "Page URL": BASE_URL,
            "Comments": comments,
        }
    ]

    # Save the single-row result to the report
    results_df = pd.DataFrame(result)
    save_report(results_df, sheet_name="Currency Filtering Test")


if __name__ == "__main__":
    test_currency_filtering()
