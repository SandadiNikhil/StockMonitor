"""
    Module for loading and providing configuration settings.
"""

import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='env/key.env')  # load .env here

API_KEY = os.environ.get("FMP_API_KEYS")
BASE_URL = os.environ.get("FMP_BASE_URL")
NASDAQ_API_KEY = os.environ.get("NASDAQ_API_KEY")

api_key_list = [] # Initialize an empty list to hold API keys
api_key_index = 0  # Index to track which API key to use

if API_KEY:
    api_key_list = [key.strip() for key in API_KEY.split(',')]
else:
    print("Warning: FMP_API_KEYS environment variable not set. API access might be limited.")


def get_api_key():
    """Returns the Financial Modeling Prep API key from environment variables."""
    global api_key_index, api_key_list

    if not api_key_list:
        return None # No API keys available

    api_key = api_key_list[api_key_index % len(api_key_list)] # Cycle through keys using modulo
    api_key_index += 1 # Increment index for next call
    return api_key


def get_base_url():
    """Returns the base URL for the Financial Modeling Prep API from environment variables."""
    return BASE_URL


def get_nasdaq_datalink_api_key():
    """Returns the NASDAQ Data Link API key."""
    return NASDAQ_API_KEY # Function to get NASDAQ Data Link API Key


def main():
    """
    Main function for config.py - testing API key retrieval.
    """
    print("config.py: Module for configuration settings.")
    print("This main function is for testing configuration loading.")

    api_key = get_api_key()
    if not api_key:
        print(f"\nAPI Key retrieved: {api_key} (from list index {api_key_index - 1})") # Show which key was used
    # else:
    #     print("\nNo API Key is retrieved.")

    nasdaq_api_key = get_nasdaq_datalink_api_key() # Get NASDAQ API key
    if not nasdaq_api_key:
        print(f"NASDAQ Data Link API Key retrieved: {nasdaq_api_key}")
    # else:
    #     print("No NASDAQ Data Link API Key available (NASDAQ_API_KEY not set in .env).")

    base_url = get_base_url()
    print(f"Base URL: {base_url}")


if __name__ == "__main__":
    main()