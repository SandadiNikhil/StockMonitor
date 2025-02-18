# src/api/core_api.py
"""
Core module for interacting with the Financial Modeling Prep (FMP) API.
Contains the central fetch_fmp_data function.
"""

import requests
from utils import config 
from requests.exceptions import HTTPError


def fetch_fmp_data(endpoint):
    """
    Fetches data from Financial Modeling Prep API using rotating API keys.
    This is the core function for making API requests.
    """
    api_key = config.get_api_key()  # Get API key from config module
    if not api_key:
        print("Error: No FMP API keys available from config in core_api.py.")
        return None

    BASE_URL = config.get_base_url()
    url = f"{BASE_URL}/{endpoint}?apikey={api_key}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except HTTPError as e:
        if e.response.status_code == 429:
            print(f"Warning: Rate limit exceeded with API key in core_api.py. HTTP Error: {e}")
        return None
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")
    except Exception:
        return None