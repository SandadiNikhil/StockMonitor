"""
Module for interacting with the Financial Modeling Prep (FMP) API.

This module contains functions to fetch stock data from the FMP API,
including real-time prices and historical data.
It handles API authentication using environment variables.
"""

from bs4 import BeautifulSoup
from src.utils import config 
from requests.exceptions import HTTPError
from src.api import core_api  


def get_company_profile(symbol):
    """
    Fetches company profile data for a given stock symbol and extracts the company name.
    Returns the company name as a string, or None if profile data or company name is not found.
    """
    endpoint = f"company/profile/{symbol}"  # API endpoint for company profile
    profile_data = core_api.fetch_fmp_data(endpoint)
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
    ratios_data = core_api.fetch_fmp_data(endpoint)  # Fetch ratios data
    # print(f"DEBUG - ratios_data for symbol {symbol}: {ratios_data}") # Debug
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
    price_data = core_api.fetch_fmp_data(endpoint)  # Fetch price data
    # print(f"DEBUG - realtime_price_data for symbol {symbol}: {price_data}")
    if price_data and isinstance(price_data, list) and len(
            price_data) > 0:  # Check if data is valid list and not empty
        # Return the first element of the list, which contains the quote
        return price_data[0]
    return None  # Return None if real-time price data cannot be retrieved


def get_historical_price(symbol):
    """Fetches historical daily price data for a given stock symbol."""
    endpoint = f"historical-price-full/{symbol}"  # API endpoint for historical prices
    data = core_api.fetch_fmp_data(endpoint)  # Re-use our fetch_fmp_data function
    if data and 'historical' in data:  # Check if data and 'historical' key exist
        return data['historical']  # Return the list of historical price data
    return None  # Return None if there's an issue fetching data


def get_earnings_growth_rate(symbol):
    """
    Fetches historical earnings calendar data to extract earnings growth rate.
    """
    endpoint = f"historical-earnings-calendar/{symbol}"
    earnings_calendar_data = core_api.fetch_fmp_data(endpoint)

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
    print("This main function is for testing API calls and is not needed for normal operation.")

    symbol_to_check = "AAPL"  # Example symbol for testing

    profile = get_company_profile(symbol_to_check)
    print(f"\nCompany Profile for {symbol_to_check}: {profile}")

    realtime_price = get_realtime_price(symbol_to_check)
    print(f"\nReal-time Price for {symbol_to_check}: {realtime_price}")

    # historical = get_historical_price(symbol_to_check)
    # if historical:
    #     print(f"\nHistorical Data for {symbol_to_check}: (first 2 records)")
    #     print(historical[:2])  
    # else:
    #     print(f"\nCould not retrieve historical data for {symbol_to_check}")

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