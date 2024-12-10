#   Selenium Web Automation Testing Assignment

##  Table of Contents
-   [Project Overview](#project-overview)
-   [Features](#features)
-   [Project Structure](#project-structure)
-   [Installation](#installation)
-   [Usage](#usage)
-   [Test Results](#test-results)
-   [Key Aspects of Reusability](#key-aspects-of-reusability)


---


##  Project Overview

This project automates testing of a vacation rental website's details page for SEO-related elements and currency filtering functionality. It uses Python, Selenium, and Pandas to validate key aspects of the page, ensuring a smooth user experience and adherence to best practices. It follows good software development practices like modularity, configuration separation, and utility-based design, making it easy to adapt and extend.


---


##  Features

1.  **H1 Tag Test:** Validates the presence of a single H1 tag on the page.
2.  **HTML Sequence Test:** Checks for proper ordering of header tags (H1 through H6) and identifies missing tags or sequence mismatches.
3.  **Image Alt Attribute Test:** Ensures all images on the page have valid alt attributes.
4.  **404 Test:** Validates all links on the page, ensuring none return 404 or other unexpected errors.
5.  **Currency Filtering Test:** Verifies the functionality of currency selection and ensures price elements update correctly.
6.  **Script Data Scraping:** Scrapes data from by analyzing the scripts in the webpage.
7.  **Reusable Code and Method:** Code is reusable to a significant extent.


---


## Project Structure

    ```bash
    Selenium-Web-Automation-Testing/
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
    git clone https://github.com/srsaurav0/Selenium-Automation-Testing.git
    cd Selenium-Automation-Testing
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
    -   Create (if not exists) a folder named ***drivers*** at the root of the project.
    -   Download ChromeDriver from website:
        -   For Linux: *https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.87/linux64/chromedriver-linux64.zip*
        -   For Win32: *https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.87/win32/chromedriver-win32.zip*
        -   For Win64: *https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.87/win64/chromedriver-win64.zip*
    -   Now copy the `chromedriver` file inside the ***drivers*** folder.
4.  Install Dependencies:
    ```bash
    pip install -r requirements.txt
    ```
5.  Update Configuration:
    -   Edit ***utils/config.py*** to set the `BASE_URL`, `WAIT_TIME`, and other constants as per your requirements.
6.  Setup Output Folder:
    -   Create an output folder named ***output*** at the root of the project.


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
    -   To see all the links being checked, uncomment line 56 (`print(f"Checking link: {link}")`)
-   **Currency Filtering Test:**
    ```bash
    python -m tests.test_currency_filtering
    ```
    -   To see the changed currencies, uncomment line 60 (`print(price_text)`)

-   **Script Data Scrape:**
    ```bash
    python -m tests.test_script_data_scrape
    ```


---


##  Test Results

### Output

-   All test results are saved in the ***output/*** directory as **Excel** files with ***.xlsx*** extension.
-   Each test writes its results to a separate sheet in the same Excel file (`test_results.xlsx`).
-   The test results are appended automatically in the Excel sheet.
-   To view the output .xlsx files in VS Code, **Excel Viewer** extension is recommended.
-   To change the test webpage, simply change the `BASE_URL` in the ***utils/config.py*** file.

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


---


##  Key Aspects of Reusability

### Modular Design

Code is divided into smaller modules (`utils/` and `tests/`) based on their responsibilities:
-   **Browser Setup (`utils/browser.py`)**: Encapsulates the WebDriver setup, making it reusable across all test scripts.
-   **Reporting (`utils/reporter.py`)**: Handles Excel report generation in a reusable way.
-   **Configuration (`utils/config.py`)**: Centralized configuration management makes code adaptable for other test cases or environments.

**Advantage**: Modules can be reused independently in new projects or extended without affecting unrelated code.

### Parameterized Configurations

Parameters like `BASE_URL`, `WAIT_TIME`, and other constants are managed in `utils/config.py`.

**Advantage**: The tests can be reused for other URLs or websites by simply updating the `BASE_URL` or `CURRENCY_MAP`. This avoids hardcoding and enhances flexibility.

### Generic Utility Functions

Utility functions like `get_driver()` and `save_report()` are decoupled from specific test logic.

**Advantage**: These functions can be used in other Selenium projects. For example:
-   `get_driver()`: Reusable across any Selenium-based test automation.
-   `save_report()`: Can be used to generate Excel reports in any data-driven testing scenario.

### Separation of Concerns

Test scripts can be reused independently. For instance:
-   The **H1 Tag Test** can be reused in another project to validate header tags.
-   The **404 Test** can validate link integrity for any website without modifications.