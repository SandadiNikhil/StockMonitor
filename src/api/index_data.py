"""
Module for getting stock index lists (S&P 500, NASDAQ 100).
Reads stock symbols from CSV files (sp500_stocks.csv, nasdaq100_stocks.csv)
instead of fetching from API or web scraping.
"""

import csv
import os

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # Project base directory (StockMonitor/src/..)
_SCRIPTS_DIR = os.path.join(_BASE_DIR, 'scripts')  # Path to scripts directory

SP500_CSV_FILE = os.path.join(_SCRIPTS_DIR, 's&p500.csv')
NASDAQ100_CSV_FILE = os.path.join(_SCRIPTS_DIR, 'nasdaq100.csv')


def _read_symbols_from_csv(csv_filepath):
    """
    Reads stock symbols from a CSV file.
    Assumes the CSV file has a header row and a 'Symbol' column.
    Returns a list of symbols or None if file not found or empty.
    """
    symbols = []
    if not os.path.exists(csv_filepath):
        print(f"Warning: CSV file not found: {csv_filepath}")
        return None

    try:
        with open(csv_filepath, 'r') as csvfile:
            csv_reader = csv.reader(csvfile) # Use csv.reader instead of DictReader
            for row in csv_reader:
                if row: 
                    symbol = row[0] 
                    symbols.append(symbol.strip()) # Strip whitespace
    except Exception as e:
        print(f"Error reading CSV file {csv_filepath}: {e}")
        return None

    if not symbols:
        print(f"Warning: No symbols found in CSV file: {csv_filepath}")
        return None

    return symbols


def get_sp500_symbols():
    """
    Gets S&P 500 symbols from the sp500_stocks.csv file.
    Returns a list of symbols or None if CSV file is not found or empty.
    """
    symbols = _read_symbols_from_csv(SP500_CSV_FILE)
    if symbols:
        print(f"Successfully loaded {len(symbols)} S&P 500 symbols from CSV: {SP500_CSV_FILE}")
        return symbols
    else:
        print(f"Error: Could not retrieve S&P 500 symbols from CSV file: {SP500_CSV_FILE}")
        return None


def get_nasdaq100_symbols():
    """
    Gets NASDAQ-100 symbols from the nasdaq100_stocks.csv file.
    Returns a list of symbols or None if CSV file is not found or empty.
    """
    symbols = _read_symbols_from_csv(NASDAQ100_CSV_FILE)
    if symbols:
        print(f"Successfully loaded {len(symbols)} NASDAQ-100 symbols from CSV: {NASDAQ100_CSV_FILE}")
        return symbols
    else:
        print(f"Error: Could not retrieve NASDAQ-100 symbols from CSV file: {NASDAQ100_CSV_FILE}")
        return None


def get_sp500_symbols_from_api():
    """
    Placeholder - API function is no longer used to get S&P 500 symbols in this version.
    Returns None and prints a warning.
    """
    print("Warning: get_sp500_symbols_from_api() is now a placeholder and not used for CSV-based symbol loading.")
    return None


def get_nasdaq100_symbols_from_nasdaq_api():
    """
    Placeholder - API function is no longer used to get NASDAQ 100 symbols in this version.
    Returns None and prints a warning.
    """
    print("Warning: get_nasdaq100_symbols_from_nasdaq_api() is now a placeholder and not used for CSV-based symbol loading.")
    return None


def get_sp500_symbols_from_wikipedia():
    """
    Placeholder - Wikipedia scraping function is no longer used in this CSV-based version.
    Returns None and prints a warning.
    """
    print("Warning: get_sp500_symbols_from_wikipedia() is now a placeholder and not used for CSV-based symbol loading.")
    return None


def get_nasdaq100_symbols_from_wikipedia():
    """
    Placeholder - Wikipedia scraping function is no longer used in this CSV-based version.
    Returns None and prints a warning.
    """
    print("Warning: get_nasdaq100_symbols_from_wikipedia() is now a placeholder and not used for CSV-based symbol loading.")
    return None


def main():
    """
    Main function for index_data.py - testing CSV-based index list retrieval.
    """
    print("index_data.py: Module for getting stock index lists from CSV files.")
    print("This main function is for testing CSV file reading.")

    # --- Test NASDAQ 100 Symbols from CSV ---
    nasdaq_symbols_csv = get_nasdaq100_symbols()
    if nasdaq_symbols_csv:
        print("\nNASDAQ-100 Symbols from CSV (first 10):")
        print(nasdaq_symbols_csv[:10])
        print(f"Total NASDAQ-100 symbols retrieved from CSV: {len(nasdaq_symbols_csv)}")
    else:
        print("\nCould not retrieve NASDAQ-100 symbols from CSV.")

    # --- Test S&P 500 Symbols from CSV ---
    sp500_symbols_csv = get_sp500_symbols()
    if sp500_symbols_csv:
        print("\nS&P 500 Symbols from CSV (first 10):")
        print(sp500_symbols_csv[:10])
        print(f"Total S&P 500 symbols retrieved from CSV: {len(sp500_symbols_csv)}")
    else:
        print("\nCould not retrieve S&P 500 symbols from CSV.")


if __name__ == '__main__':
    main()