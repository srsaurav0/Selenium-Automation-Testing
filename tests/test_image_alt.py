import pandas as pd
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.browser import get_driver
from utils.reporter import save_report
from utils.config import BASE_URL, WAIT_TIME


def validate_image_alt_attributes(driver):
    """Validate the alt attributes of all images on the page."""
    missing_alt_images = []  # To collect image srcs with missing alt attributes

    try:
        driver.get(BASE_URL)

        # Wait for up to WAIT_TIME seconds to find any image tag
        WebDriverWait(driver, WAIT_TIME).until(
            EC.presence_of_element_located((By.TAG_NAME, "img"))
        )
        images = driver.find_elements(By.TAG_NAME, "img")

        # Check alt attributes for each image
        for img in images:
            src = img.get_attribute("src")
            alt = img.get_attribute("alt")

            # Collect src if alt attribute is missing
            if not alt:
                missing_alt_images.append(src)

    except TimeoutException:
        return {
            "Test Case": "Image Alt Attribute Test",
            "Status": "Fail",
            "Page URL": BASE_URL,
            "Comments": "No images found on the page.",
        }

    # Determine the overall status and comments
    if not missing_alt_images:
        return {
            "Test Case": "Image Alt Attribute Test",
            "Status": "Passed",
            "Page URL": BASE_URL,
            "Comments": "All images have alt attributes.",
        }
    else:
        return {
            "Test Case": "Image Alt Attribute Test",
            "Status": "Fail",
            "Page URL": BASE_URL,
            "Comments": f"Missing alt attributes for images: {', '.join(missing_alt_images)}",
        }


def test_image_alt_attributes():
    """Test for image alt attributes on the specified page."""
    driver = get_driver()

    try:
        print(f"Testing image alt attributes on: {BASE_URL}")
        result = validate_image_alt_attributes(driver)  # Single result dictionary
    finally:
        driver.quit()

    # Save the single-row result to the main report
    results_df = pd.DataFrame([result])  # Wrap the dictionary in a list
    save_report(results_df, sheet_name="Image Alt Attribute Test")


if __name__ == "__main__":
    test_image_alt_attributes()
