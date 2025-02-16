"""
    This script runs stock.py for each S&P 500 company and compiles the output to a file.
"""

import subprocess
from api import fmp_data_api
import os
import time # Import time for delay

def run_stock_for_sp500(output_file="sp500_output.txt", delay_seconds=1.0): # Added delay parameter
    """
    Runs stock.py for each S&P 500 company, gets symbols from fmp_api.get_sp500_symbols(),
    and compiles the output to a file. Includes delay to be respectful of APIs and websites.
    """
    sp500_symbols = fmp_data_api.get_sp500_symbols() # Use the combined function that tries API then Wikipedia

    if not sp500_symbols:
        print("Error: Could not retrieve S&P 500 symbols. Aborting.")
        return

    print(f"Total S&P 500 symbols to process: {len(sp500_symbols)}")

    with open(output_file, "w") as outfile:
        for symbol in sp500_symbols:
            print(f"Processing symbol: {symbol}")
            outfile.write(f"---------- START OF OUTPUT FOR {symbol} ----------\n")

            try:
                process = subprocess.run(
                    ["python", "stock.py"],
                    input=symbol + "\n",
                    capture_output=True,
                    text=True,
                    cwd=os.path.dirname(os.path.abspath(__file__)),
                    check=True
                )
                outfile.write(process.stdout)
                if process.stderr:
                    outfile.write(f"\n---------- STDERR for {symbol} ----------\n")
                    outfile.write(process.stderr)

            except subprocess.CalledProcessError as e:
                outfile.write(f"\n---------- ERROR PROCESSING {symbol} ----------\n")
                outfile.write(f"Return code: {e.returncode}\n")
                outfile.write(f"Stderr: {e.stderr}\n")
            except FileNotFoundError:
                print("Error: stock.py not found.")
                return
            except Exception as e:
                outfile.write(f"\n---------- UNEXPECTED ERROR PROCESSING {symbol} ----------\n")
                outfile.write(f"Error details: {e}\n")

            outfile.write(f"---------- END OF OUTPUT FOR {symbol} ----------\n\n")
            print(f"Finished processing symbol: {symbol}")
            time.sleep(delay_seconds) # Add delay between requests


    print(f"Completed processing all S&P 500 symbols. Output written to: {output_file}")


if __name__ == "__main__":
    run_stock_for_sp500()