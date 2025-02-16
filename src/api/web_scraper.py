"""
    Module for web scraping functions, specifically for fetching stock index lists from Wikipedia.
"""

import requests
from bs4 import BeautifulSoup
from src.utils import config
from src.api import core_api

def get_sp500_symbols_from_wikipedia():
    """
    Scrapes the list of S&P 500 company symbols from Wikipedia.
    Returns a list of stock symbols, or None if scraping fails.
    """
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the table - inspect Wikipedia page to confirm table ID/class
        table = soup.find('table', {'id': 'constituents'}) # Using table ID

        if not table:
            print("Error: Could not find the S&P 500 companies table on Wikipedia.")
            return None

        symbols = []
        # Extract symbols from the first column of each table row (skipping header)
        for row in table.find_all('tr')[1:]:  # Skip header row
            cells = row.find_all('td')
            if cells and len(cells) > 0:
                symbol_element = cells[0].find('a') # Look for the link in the first cell
                if symbol_element:
                    symbol = symbol_element.text.strip() # Get text from link, and clean whitespace
                    symbols.append(symbol)
        return symbols

    except requests.exceptions.RequestException as e:
        print(f"Error fetching Wikipedia page: {e}")
        return None
    except Exception as e:
        print(f"Error parsing Wikipedia page: {e}")
        return None


def get_sp500_symbols_from_api(): # Renamed original API function to differentiate
    """
    Fetches a list of S&P 500 constituent symbols from Financial Modeling Prep API.
    Returns a list of stock symbols, or None if there's an error.
    """
    endpoint = "sp500_constituent"  # Or the correct FMP API endpoint for S&P 500 list
    sp500_data = core_api.fetch_fmp_data(endpoint) # Use your existing fetch_fmp_data function

    if sp500_data and isinstance(sp500_data, list):
        symbols = [item['symbol'] for item in sp500_data] # Extract symbols from the data - adjust based on API response structure
        return symbols
    return None
