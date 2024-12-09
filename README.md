#   Vacation Rental Home Page Automation Testing Assignment

##  Table of Contents
-   [Project Overview](#project-overview)
-   [Features](#features)
-   [Project Structure](#project-structure)
-   [Installation](#installation)
-   [Usage](#usage)
-   [Test Results](#test-results)


---


##  Project Overview

This project automates testing of a vacation rental website's details page for SEO-related elements and currency filtering functionality. It uses Python, Selenium, and Pandas to validate key aspects of the page, ensuring a smooth user experience and adherence to best practices.


---


##  Features

1.  **H1 Tag Test:** Validates the presence of a single H1 tag on the page.
2.  **HTML Sequence Test:** Checks for proper ordering of header tags (H1 through H6) and identifies missing tags or sequence mismatches.
3.  **Image Alt Attribute Test:** Ensures all images on the page have valid alt attributes.
4.  **404 Test:** Validates all links on the page, ensuring none return 404 or other unexpected errors.
5.  **Currency Filtering Test:** Verifies the functionality of currency selection and ensures price elements update correctly.
6.  **Script Data Scraping:** Scrapes data from by analyzing the scripts in the webpage.


---


## Project Structure

    ```bash
        VacationRentalAutomation/
        │
        ├── output/                             # Directory for storing test results (Excel files)
        │
        ├── drivers/                            # Directory for drivers (chromedriver)
        │
        ├── tests/                              # Directory containing test scripts
        │   ├── test_h1_tag.py                  # H1 tag validation script
        │   ├── test_html_sequence.py           # HTML sequence validation script
        │   ├── test_image_alt.py               # Image alt attribute validation script
        │   ├── test_404.py                     # 404 error validation script
        │   ├── test_currency_filtering.py      # Currency filtering test script
        │   ├── test_script_data_scrape.py      # Script data scraping test
        │   └── __init__.py                     # Test package initialization
        │
        ├── utils/                              # Utility scripts
        │   ├── browser.py                      # Browser setup utility
        │   ├── config.py                       # Configuration file for constants (e.g., BASE_URL, WAIT_TIME)
        │   ├── reporter.py                     # Handles Excel report generation
        │   └── __init__.py                     # Utility package initialization
        │
        ├── app.py                              # Main file to execute all test scripts
        ├── requirements.txt                    # Python dependencies for the project
        ├── .gitignore                          # Environment variables (optional)
        └── README.md                           # Project documentation
    ```


---


## Installation

### Prerequisites

-   Python (>= 3.8)
-   Google Chrome or Firefox (Chrome recommended)
-   ChromeDriver or GeckoDriver (ChromeDriver recommended)

### Steps

1.  Clone the repository:
    ```bash
    git clone https://github.com/srsaurav0/Selenium-Automation-Testing-Assignment.git
    cd Selenium-Automation-Testing-Assignment
    ```
2.  Create and activate a virtual environment:
    On Linux:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
    On Windows:
    ```bash
    python -m venv .venv
    Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
    .venv\Scripts\activate
    ```
3.  Setup ChromeDriver:
    -   Create (if not exists) a folder named *drivers* at the root of the project.
    -   Download ChromeDriver from website:
        -   For Linux: *https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.87/linux64/chromedriver-linux64.zip*
        -   For Win32: *https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.87/win32/chromedriver-win32.zip*
        -   For Win64: *https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.87/win64/chromedriver-win64.zip*
    -   Now copy the `chromedriver` file inside the *drivers* folder.
4.  Install Dependencies:
    ```bash
    pip install -r requirements.txt
    ```
5.  Update Configuration:
    -   Edit utils/config.py to set the BASE_URL, WAIT_TIME, and other constants as per your requirements.


---


## Usage

### Run All Tests

To run all tests, execute the app.py file:
    ```bash
    python app.py
    ```

### Run Individual Tests

Run each test separately using the following commands:
-   **H1 Tag Test:**
    ```bash
    python -m tests.test_h1_tag
    ```
-   **HTML Sequence Test:**
    ```bash
    python -m tests.test_html_sequence
    ```
-   **Image Alt Attribute Test:**
    ```bash
    python -m tests.test_image_alt
    ```
-   **URL Status Code Test of URLs:**
    ```bash
    python -m tests.test_404
    ```
-   **Currency Filtering Test:**
    ```bash
    python -m tests.test_currency_filtering
    ```
-   **Script Data Scrape:**
    ```bash
    python -m tests.test_script_data_scrape
    ```


---


##  Test Results

### Output

-   All test results are saved in the *output/* directory as **Excel** files with *.xlsx* extension.
-   Each test (except `test_script_data_scrape.py`) writes its results to a separate sheet in the same Excel file (`test_results.xlsx`).
-   The test `test_script_data_scrape.py` writes its output in `script_data.xlsx` file because of its different output structure.
-   The test results are appended automatically in the Excel sheet.
-   To change the test webpage, simply change the *BASE_URL* in the *utils/config.py* file.

### Report Structure

-   **Columns:**
    -   **Test Case**: Name of the test performed.
    -   **Status**: `Passed` or `Fail`.
    -   **Page URL**: The URL of the page tested.
    -   **Comments**: Additional details about the test result.
        -   In **Image Alt Attribute Test**, if the test fails, it will show all the `image srcs` of the images that are responsible for the test failure.
        -   In **URL Status Code Test of URLs**, if the test fails, it will show all the `URLs` of the base page along with `error codes` and `error explanations` that are responsible for the test failure.
        -   In **Currency Filtering Test**, if the test fails, it will show all the `URLs` of the base page along with `error codes` and `error explanations` that are responsible for the test failure.

-   **Columns of Script Data Scrape Test:**
    -   **SiteURL**
    -   **CampaignID**
    -   **SiteName**
    -   **Browser**
    -   **CountryCode**
    -   **IP**