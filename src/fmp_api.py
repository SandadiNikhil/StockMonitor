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
    url = f"{BASE_URL}/{endpoint}?apikey={API_KEY}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")
    except Exception as err:
        print(f"An unexpected error occurred: {err}")
    return None


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


def get_company_key_ratios(symbol):
    """
    Fetches key financial ratios for a given stock symbol from Financial Modeling Prep API.
    Returns the JSON response containing key ratios, or None if data cannot be fetched.
    """
    endpoint = f"ratios/{symbol}" # API endpoint for financial ratios
    ratios_data = fetch_fmp_data(endpoint) # Fetch ratios data
    print(f"DEBUG - ratios_data for symbol {symbol}: {ratios_data}") # Debug print
    if ratios_data and isinstance(ratios_data, list): # Check if data is a valid list and not empty
        return ratios_data # Return the ratios data as JSON
    return None # Return None if ratios data cannot be retrieved


def get_realtime_price(symbol):
    """
    Fetches real-time price data for a given stock symbol from Financial Modeling Prep API.
    Returns the JSON response containing real-time price, or None if data cannot be fetched.
    """
    endpoint = f"quote/{symbol}"  # API endpoint for real-time quote
    price_data = fetch_fmp_data(endpoint) # Fetch price data
    print(f"DEBUG - realtime_price_data for symbol {symbol}: {price_data}") # Debug print
    if price_data and isinstance(price_data, list) and len(price_data) > 0: # Check if data is valid list and not empty
        return price_data[0] # Return the first element of the list, which contains the quote
    return None # Return None if real-time price data cannot be retrieved


def get_historical_price(symbol):
    """Fetches historical daily price data for a given stock symbol."""
    endpoint = f"historical-price-full/{symbol}"  # API endpoint for historical prices
    data = fetch_fmp_data(endpoint)  # Re-use our fetch_fmp_data function
    if data and 'historical' in data:  # Check if data and 'historical' key exist
        return data['historical']  # Return the list of historical price data
    return None  # Return None if there's an issue fetching data


if __name__ == '__main__':
    # Example usage (for testing):
    api_key_check = get_api_key # Accessing the API key to trigger loading/check
    if api_key_check:
        print("API_KEY loaded successfully from environment variables.")
    else:
        print("Error: API_KEY not found in environment variables. Please set it!")

    symbol_to_check = "AAPL" # Example symbol for testing

    profile = get_company_profile(symbol_to_check)
    if profile:
        print(f"\nCompany Profile for {symbol_to_check}: {profile}")
    else:
        print(f"\nCould not retrieve company profile for {symbol_to_check}")

    realtime_price = get_realtime_price(symbol_to_check) # Test real-time price function
    if realtime_price:
        print(f"\nReal-time Price for {symbol_to_check}: {realtime_price}")
    else:
        print(f"\nCould not retrieve real-time price for {symbol_to_check}")


    historical = get_historical_price(symbol_to_check) # Test historical price function
    if historical:
        print(f"\nHistorical Data for {symbol_to_check}: (first 2 records)")
        print(historical[:2]) # Print first 2 records for brevity
    else:
        print(f"\nCould not retrieve historical data for {symbol_to_check}")


    key_ratios = get_company_key_ratios(symbol_to_check) # Test key ratios function
    if key_ratios:
        print(f"\nKey Ratios for {symbol_to_check}: (first record)")
        print(key_ratios[0]) # Print first record for brevity
    else:
        print(f"\nCould not retrieve key ratios for {symbol_to_check}")