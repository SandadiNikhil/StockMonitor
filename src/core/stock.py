"""
Module containing the Stock class and related functions for
fetching and analyzing stock data.
"""

import sys
sys.path.insert(0, '/Users/Nikhil/Downloads/StockMonitor/src')

from api import fmp_data_api  
from utils import config, formula, display 


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

    def get_company_profile(self): 
        """
        Fetches and stores the company profile from FMP API.
        """
        print(f"Fetching company profile for {self.symbol}...")
        profile_data = fmp_data_api.get_company_profile(self.symbol) # Corrected function call to get_company_profile
        if profile_data:
            # For now, just store the raw profile data, we can process it later
            self.company_profile = profile_data
            print(f"Company profile fetched for {self.symbol}")
        else:
            print(f"Could not fetch company profile for {self.symbol}")
            self.company_profile = None


    def get_key_ratios(self): 
        """
        Fetches and stores key ratios (P/E, P/B, D/E, ROE) from FMP API.
        """
        print(f"Fetching key ratios for {self.symbol}...")
        ratios_data = fmp_data_api.get_company_key_ratios(self.symbol) # Corrected function call to get_company_key_ratios
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


    def calculate_scores(self): # Renamed method to calculate_scores
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


    def perform_analysis(self): 
        """
        Orchestrates the stock analysis process.
        Fetches company profile and key ratios, then calculates financial scores.
        """
        self.get_company_profile() 
        self.get_key_ratios()      
        self.calculate_scores()    


def run_stock_analysis(symbol):
    """
    Creates a Stock object and runs the stock analysis workflow.
    """
    stock = Stock(symbol)
    stock.perform_analysis() 


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