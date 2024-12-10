import os
import pandas as pd
from utils.config import EXCEL_OUTPUT


def initialize_report():
    """Initialize an empty DataFrame for the test results."""
    columns = ["Page URL", "Test Case", "Status", "Comments"]
    return pd.DataFrame(columns=columns)


def save_report(dataframe, sheet_name):
    """Save test results to an Excel file, appending to an existing sheet if necessary."""
    if os.path.exists(EXCEL_OUTPUT):
        # Load the existing workbook and check for the sheet
        with pd.ExcelWriter(EXCEL_OUTPUT, mode="a", engine="openpyxl", if_sheet_exists="overlay") as writer:
            try:
                # Load existing data if the sheet exists
                existing_data = pd.read_excel(EXCEL_OUTPUT, sheet_name=sheet_name)
                # Append the new data to the existing data
                updated_data = pd.concat([existing_data, dataframe], ignore_index=True)
                updated_data.to_excel(writer, index=False, sheet_name=sheet_name)
            except ValueError:
                # Sheet does not exist, so create it
                dataframe.to_excel(writer, index=False, sheet_name=sheet_name)
    else:
        # Create a new Excel file with the given sheet
        with pd.ExcelWriter(EXCEL_OUTPUT, engine="openpyxl") as writer:
            dataframe.to_excel(writer, index=False, sheet_name=sheet_name)
    print(f"Report saved to {EXCEL_OUTPUT} in sheet '{sheet_name}'")
