import os
import fmp_api

def display_stock_data(symbol):
    """
    Fetches and displays stock data for a given symbol using functions from fmp_api.py.
    """
    company_name = fmp_api.get_company_profile(symbol) # Call function from fmp_api module
    if company_name:
        print(f"Company Name: {company_name} ({symbol.upper()})")
    else:
        print(f"Company name not found for symbol: {symbol.upper()}")

    real_time_price = fmp_api.get_realtime_price(symbol) # Call function from fmp_api module
    if real_time_price:
        print("\nReal-time price data for {}:".format(symbol.upper()))
        print(f"  Price: {real_time_price['price']:.2f}")
    else:
        print("\nCould not retrieve real-time price data for {}.".format(symbol.upper()))

    historical_data = fmp_api.get_historical_price(symbol) # Call function from fmp_api module
    if historical_data:
        print("\nHistorical price data for {}:".format(symbol.upper()))
        # Display the latest 5 historical data points (for brevity)
        for data_point in historical_data[:5]:
            print(data_point)
        print(f"... (Total {len(historical_data)} historical data points)")
    else:
        print("\nCould not retrieve historical price data for {}.".format(symbol.upper()))

    # --- NEW: Call get_company_key_ratios and display (optional for now, add if you want to test immediately) ---
    key_ratios = fmp_api.get_company_key_ratios(symbol) # Call function from fmp_api module
    if key_ratios:
        print("\nKey Ratios for {}:".format(symbol.upper()))
        # Print the first ratio to check (optional - can be removed later or expanded)
        if key_ratios and len(key_ratios) > 0: # Check if list is not empty before accessing index 0
            first_ratio_data = key_ratios[0]
            print(f"  Latest Ratios (Date: {first_ratio_data.get('date')}):") # Safely get date, might be missing
            print(f"    P/E Ratio: {first_ratio_data.get('priceEarningsRatio')}") # Safely get PE Ratio
            print(f"    P/B Ratio: {first_ratio_data.get('priceBookValueRatio')}") # Safely get PB Ratio
            print(f"    D/E Ratio: {first_ratio_data.get('debtEquityRatio')}")     # Safely get DE Ratio
            print(f"    ROE: {first_ratio_data.get('returnOnEquity')}")             # Safely get ROE
        else:
            print("  No ratios data available in response.")
    else:
        print("\nCould not retrieve key ratios for {}.".format(symbol.upper()))
    # --- END NEW SECTION ---


if __name__ == "__main__":
    current_dir = os.getcwd() # Keep if you use it, otherwise can remove os import and this line
    print(f"Current Working Directory: {current_dir}") # Keep if you want to show working directory

    stock_symbol = input("Enter the stock symbol you want to monitor (e.g., AAPL, TSLA): ").strip().upper() # Get input and uppercase

    if stock_symbol:
        display_stock_data(stock_symbol) # Call the function to display data for the entered symbol
    else:
        print("No stock symbol entered. Please run the script again and enter a symbol.")