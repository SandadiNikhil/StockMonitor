"""
Module for interacting with the Financial Modeling Prep (FMP) API.

This module contains functions to fetch stock data from the FMP API,
including real-time prices and historical data.
It handles API authentication using environment variables.
"""

import requests
from config import get_api_key, get_base_url


def fetch_fmp_data(endpoint):
    """Fetches data from Financial Modeling Prep API."""
    API_KEY = get_api_key()  # Get API key using config function
    BASE_URL = get_base_url()  # Get base URL using config function

    params = {'apikey': API_KEY}
    url = f"{BASE_URL}/{endpoint}"
    response = requests.get(url, params=params)
    return response.json()


def get_historical_price(symbol):
    """Fetches historical daily price data for a given stock symbol."""
    endpoint = f"historical-price-full/{symbol}"  # API endpoint for historical prices
    data = fetch_fmp_data(endpoint)  # Re-use our fetch_fmp_data function
    if data and 'historical' in data:  # Check if data and 'historical' key exist
        return data['historical']  # Return the list of historical price data
    return None  # Return None if there's an issue fetching data


def get_company_profile(symbol):
    """
    Fetches company profile data for a given stock symbol and extracts the company name.
    Returns the company name as a string, or None if profile data or company name is not found.
    """
    endpoint = f"company/profile/{symbol}"  # API endpoint for company profile
    profile_data = fetch_fmp_data(endpoint)
    print(f"DEBUG - profile_data for symbol {symbol}: {profile_data}")
    if profile_data and isinstance(profile_data, dict): # Check if data is a valid dictionary and not empty
        # Access the first element (list) and get 'profile' dict
        profile_info = profile_data.get('profile')
        if profile_info and isinstance(profile_info, dict): # Check if profile_info is valid dict
            company_name = profile_info.get(
                'companyName')  # Extract 'companyName'
            if company_name:  # Check if company_name is not None or empty
                return company_name  # Return the company name
    return None  # Return None if company profile or company name cannot be retrieved
