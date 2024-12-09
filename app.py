import subprocess
import os


def run_test_module(module_name):
    """
    Run a test module using `python -m`.

    Args:
        module_name (str): The module name to run (e.g., 'tests.test_h1_tag').

    Returns:
        None
    """
    try:
        print(f"\nRunning {module_name}...")
        subprocess.run(["python", "-m", module_name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error while running {module_name}: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def main():
    """
    Main function to call all the test modules.
    """
    print("Starting test execution...\n")

    # List of test modules to run
    test_modules = [
        "tests.test_h1_tag",
        "tests.test_html_sequence",
        "tests.test_image_alt",
        "tests.test_url_status_404",
        "tests.test_currency_filtering",
        "tests.test_script_data_scrape",
    ]

    # Run each test module
    for module in test_modules:
        run_test_module(module)

    print("\nAll tests completed.")


if __name__ == "__main__":
    main()
