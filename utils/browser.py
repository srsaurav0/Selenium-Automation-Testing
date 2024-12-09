from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from utils.config import WEBDRIVER_PATH


def get_driver():
    """Set up and return the Chrome WebDriver."""
    options = ChromeOptions()
    # options.add_argument("--headless")  # Optional: Run browser in background
    options.add_argument("--start-maximized")  # Open browser in maximized mode
    service = ChromeService(WEBDRIVER_PATH)
    return webdriver.Chrome(service=service, options=options)
