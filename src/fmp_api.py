"""
Module for interacting with the Financial Modeling Prep (FMP) API.

This module contains functions to fetch stock data from the FMP API,
including real-time prices and historical data.
It handles API authentication using environment variables.
"""
from requests.exceptions import HTTPError
import requests
from config import get_api_key, get_base_url


def fetch_fmp_data(endpoint):
    """Fetches data from Financial Modeling Prep API."""
    API_KEY = get_api_key()  # Get API key using config function
    BASE_URL = get_base_url()  # Get base URL using config function
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
    # print(f"DEBUG - profile_data for symbol {symbol}: {profile_data}")
    if profile_data and isinstance(
            profile_data,
            dict) and 'profile' in profile_data and isinstance(
            profile_data['profile'],
            dict) and 'companyName' in profile_data['profile']:
        return profile_data['profile']['companyName']
    return None


def get_company_key_ratios(symbol):
    """
    Fetches key financial ratios for a given stock symbol from Financial Modeling Prep API.
    Returns the JSON response containing key ratios, or None if data cannot be fetched.
    """
    endpoint = f"ratios/{symbol}"  # API endpoint for financial ratios
    ratios_data = fetch_fmp_data(endpoint)  # Fetch ratios data
    # print(f"DEBUG - ratios_data for symbol {symbol}: {ratios_data}") # Debug
    # print
    if ratios_data and isinstance(
            ratios_data,
            list):  # Check if data is a valid list and not empty
        return ratios_data  # Return the ratios data as JSON
    return None  # Return None if ratios data cannot be retrieved


def get_realtime_price(symbol):
    """
    Fetches real-time price data for a given stock symbol from Financial Modeling Prep API.
    Returns the JSON response containing real-time price, or None if data cannot be fetched.
    """
    endpoint = f"quote/{symbol}"  # API endpoint for real-time quote
    price_data = fetch_fmp_data(endpoint)  # Fetch price data
    # print(f"DEBUG - realtime_price_data for symbol {symbol}: {price_data}")
    # # Debug print
    if price_data and isinstance(price_data, list) and len(
            price_data) > 0:  # Check if data is valid list and not empty
        # Return the first element of the list, which contains the quote
        return price_data[0]
    return None  # Return None if real-time price data cannot be retrieved


def get_historical_price(symbol):
    """Fetches historical daily price data for a given stock symbol."""
    endpoint = f"historical-price-full/{symbol}"  # API endpoint for historical prices
    data = fetch_fmp_data(endpoint)  # Re-use our fetch_fmp_data function
    if data and 'historical' in data:  # Check if data and 'historical' key exist
        return data['historical']  # Return the list of historical price data
    return None  # Return None if there's an issue fetching data


# def get_earnings_growth_rate(symbol):
#     """
#     Fetches historical earnings calendar data for a given stock symbol from FMP API.
#     Attempts to extract and return the latest annual earnings growth rate.
#     Returns the growth rate as a float (e.g., 0.10 for 10% growth), or None if not available.
#     """
#     endpoint = f"historical-earnings-calendar/{symbol}"  # API endpoint for earnings calendar
#     try: # Try to fetch earnings data and handle specific HTTPError for this endpoint
#         earnings_calendar_data = fetch_fmp_data(endpoint)  # Fetch earnings calendar data
#         # print(f"DEBUG - earnings_calendar_data for symbol {symbol}: {earnings_calendar_data}") # Removed debug print - no debug prints in final version
#         if earnings_calendar_data and isinstance(earnings_calendar_data, list):  # Check if data is valid list and not empty
#             # Assuming the latest earnings announcement is the first in the list (check API docs)
#             if earnings_calendar_data:  # Check if the list is not empty
#                 latest_earnings = earnings_calendar_data[
#                     0]  # Get the latest earnings data
#                 # Look for a key related to earnings growth in the response.
#                 # The key might be named differently, you might need to inspect the actual API response.
#                 # Let's tentatively assume it's 'earningsGrowthYOY' (Year-over-Year Earnings Growth)
#                 earnings_growth_rate = latest_earnings.get(
#                     'earningsGrowthYOY')  # Get growth rate, handle missing key

#                 if earnings_growth_rate is not None:
#                     return earnings_growth_rate  # Return the growth rate if found
# return None  # Return None if earnings growth rate cannot be retrieved

#     except HTTPError as e: # Catch HTTP errors specifically
#         if e.response.status_code == 403: # Check for 403 Forbidden specifically
#             print(f"\nWarning: Could not retrieve Earnings Growth Rate data due to API access restrictions (HTTP 403 Forbidden).") # User-friendly warning
#         else: # For other HTTP errors, print a generic error (already handled by fetch_fmp_data but can add more specific logging if needed)
#             print(f"\nWarning: Could not retrieve Earnings Growth Rate data. HTTP Error: {e}") # More generic warning, could be removed if fetch_fmp_data's error is sufficient
#         return None # Return None in case of error

#     except Exception as err: # Catch any other exceptions during earnings data fetch
#         print(f"\nWarning: Error retrieving Earnings Growth Rate data: {err}") # Generic error message
#         return None # Return None in case of error

def get_earnings_growth_rate(symbol):
    """
    Fetches historical earnings calendar data to extract earnings growth rate.
    Returns earnings growth rate or None if data cannot be fetched or is not available.
    Handles 403 Forbidden error gracefully within this function.
    """
    endpoint = f"historical-earnings-calendar/{symbol}"
    earnings_calendar_data = fetch_fmp_data(endpoint)

    if earnings_calendar_data and isinstance(earnings_calendar_data, list):
        if earnings_calendar_data:
            latest_earnings = earnings_calendar_data[0]
            earnings_growth_rate = latest_earnings.get('earningsGrowthYOY')
            if earnings_growth_rate is not None:
                return earnings_growth_rate
    return None


def main():
    """
    This fmp_api.py module's main function is for testing API function calls.
    It's not part of the primary application flow but useful for development/testing.
    """
    print("fmp_api.py: This module is for fetching data from the FMP API.")
    print("It is used by stock.py to get financial data.")
    print("This main function is for testing API calls and is not needed for normal operation.")

    # Example usage (for testing):
    api_key_check = get_api_key  # Accessing the API key to trigger loading/check
    if api_key_check:
        print("API_KEY loaded successfully from environment variables.")
    else:
        print("Error: API_KEY not found in environment variables. Please set it!")

    symbol_to_check = "AAPL"  # Example symbol for testing

    profile = get_company_profile(symbol_to_check)
    if profile:
        print(f"\nCompany Profile for {symbol_to_check}: {profile}")
    else:
        print(f"\nCould not retrieve company profile for {symbol_to_check}")

    realtime_price = get_realtime_price(
        symbol_to_check)  # Test real-time price function
    if realtime_price:
        print(f"\nReal-time Price for {symbol_to_check}: {realtime_price}")
    else:
        print(f"\nCould not retrieve real-time price for {symbol_to_check}")

    # Test historical price function
    historical = get_historical_price(symbol_to_check)
    if historical:
        print(f"\nHistorical Data for {symbol_to_check}: (first 2 records)")
        print(historical[:2])  # Print first 2 records for brevity
    else:
        print(f"\nCould not retrieve historical data for {symbol_to_check}")

    key_ratios = get_company_key_ratios(
        symbol_to_check)  # Test key ratios function
    if key_ratios:
        print(f"\nKey Ratios for {symbol_to_check}: (first record)")
        print(key_ratios[0])  # Print first record for brevity
    else:
        print(f"\nCould not retrieve key ratios for {symbol_to_check}")

    earnings_growth = get_earnings_growth_rate(
        symbol_to_check)  # Test earnings growth function
    if earnings_growth is not None:  # Check for None explicitly
        print(
            f"\nEarnings Growth Rate for {symbol_to_check}: {earnings_growth}")
    else:
        print(
            f"\nCould not retrieve Earnings Growth Rate for {symbol_to_check}")


if __name__ == '__main__':
    main()
