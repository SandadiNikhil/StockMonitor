"""
Module containing the Stock class and related functions for
fetching and analyzing stock data.
"""

from ..api import fmp_data_api
from src.utils import config, formula, display  # Import utils modules


class Stock:
    """
    Represents a stock and its financial data.
    """

    def __init__(self, symbol):
        """
        Initializes a Stock object with a stock symbol.
        """
        self.symbol = symbol
        self.financial_ratios = {}  # Dictionary to store financial ratios

    def fetch_company_profile(self):
        """
        Fetches and stores the company profile from FMP API.
        Currently, just prints the data.
        """
        print(f"Fetching company profile for {self.symbol}...")
        profile_data = fmp_data_api.fetch_company_profile(self.symbol)
        if profile_data:
            # For now, just store the raw profile data, we can process it later
            self.company_profile = profile_data
            print(f"Company profile fetched for {self.symbol}")
        else:
            print(f"Could not fetch company profile for {self.symbol}")
            self.company_profile = None


    def fetch_key_ratios(self):
        """
        Fetches and stores key ratios (P/E, P/B, D/E, ROE) from FMP API.
        """
        print(f"Fetching key ratios for {self.symbol}...")
        ratios_data = fmp_data_api.fetch_company_key_ratios(self.symbol)
        if ratios_data and ratios_data: # Check if ratios_data is not None and not empty list
            # Assuming ratios_data is a list, we take the most recent entry (index 0)
            ratios = ratios_data[0].get('ratios', {}) if isinstance(ratios_data[0], dict) else {}
            if ratios:
                self.financial_ratios['pe_ratio'] = ratios.get('peRatioTTM')
                self.financial_ratios['pb_ratio'] = ratios.get('priceToBookRatioTTM')
                self.financial_ratios['de_ratio'] = ratios.get('debtEquityRatioTTM')
                self.financial_ratios['roe'] = ratios.get('returnOnEquityTTM')
                print(f"Key ratios fetched for {self.symbol}")
            else:
                print(f"Warning: No ratios data found in key ratios response for {self.symbol}")
        else:
            print(f"Could not fetch key ratios for {self.symbol}")


    def calculate_financial_scores(self):
        """
        Calculates and stores financial scores based on fetched ratios.
        Currently, just a placeholder to print ratios.
        """
        print(f"\n--- Financial Ratios for {self.symbol} ---")
        if self.financial_ratios:
            print(f"  P/E Ratio: {self.financial_ratios.get('pe_ratio', 'N/A')}")
            print(f"  P/B Ratio: {self.financial_ratios.get('pb_ratio', 'N/A')}")
            print(f"  D/E Ratio: {self.financial_ratios.get('de_ratio', 'N/A')}")
            print(f"  ROE:       {self.financial_ratios.get('roe', 'N/A')}")
        else:
            print("  No financial ratios fetched.")


    def perform_stock_analysis(self):
        """
        Orchestrates the stock analysis process.
        Fetches company profile and key ratios, then calculates financial scores.
        """
        self.fetch_company_profile() # Fetch company profile data
        self.fetch_key_ratios()      # Fetch key ratios data
        self.calculate_financial_scores() # Calculate and display financial scores


def run_stock_analysis(symbol):
    """
    Creates a Stock object and runs the stock analysis workflow.
    """
    stock = Stock(symbol)
    stock.perform_stock_analysis() # Run the analysis workflow


def main():
    """
    Main function to run stock analysis for a given symbol from command line input.
    """
    symbol_input = input("Enter stock symbol to analyze: ").strip().upper()
    if symbol_input:
        run_stock_analysis(symbol_input)
    else:
        print("No stock symbol entered.")


if __name__ == "__main__":
    main()