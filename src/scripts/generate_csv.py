"""
Generates CSV files for NASDAQ 100 and S&P 500 stock lists
and stores them in the output directory.
"""

import csv
import os
from src.api import index_data  # Import index_data to get the stock lists

OUTPUT_DIR = "src/output"  # Define the output directory relative to the script's location


def generate_index_csv(index_name, symbols, filename):
    """
    Generates a CSV file for a given stock index list.

    Args:
        index_name (str): Name of the index (e.g., "NASDAQ 100", "S&P 500").
        symbols (list): List of stock symbols for the index.
        filename (str): Name of the CSV file to create in the output directory.
    """
    output_path = os.path.join(OUTPUT_DIR, filename)

    # Ensure the output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    try:
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['Symbol'])  # Write header row
            for symbol in symbols:
                csv_writer.writerow([symbol])
        print(f"Successfully generated CSV file for {index_name}: {output_path}")
    except Exception as e:
        print(f"Error generating CSV file for {index_name}: {e}")


def generate_nasdaq100_csv():
    """
    Generates CSV file for NASDAQ 100 stock list.
    """
    nasdaq_symbols = index_data.get_nasdaq100_symbols()
    if nasdaq_symbols:
        generate_index_csv("NASDAQ 100", nasdaq_symbols, "nasdaq100_stocks.csv")
    else:
        print("Warning: Could not retrieve NASDAQ 100 symbols, CSV not generated.")


def generate_sp500_csv():
    """
    Generates CSV file for S&P 500 stock list.
    """
    sp500_symbols = index_data.get_sp500_symbols()
    if sp500_symbols:
        generate_index_csv("S&P 500", sp500_symbols, "sp500_stocks.csv")
    else:
        print("Warning: Could not retrieve S&P 500 symbols, CSV not generated.")


def main():
    """
    Main function to generate CSV files for both NASDAQ 100 and S&P 500.
    """
    print("Generating CSV files for NASDAQ 100 and S&P 500 stock lists...")
    generate_nasdaq100_csv()
    generate_sp500_csv()
    print("CSV file generation completed.")


if __name__ == "__main__":
    main()