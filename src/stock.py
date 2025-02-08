from fmp_api import fetch_fmp_data, get_historical_price, get_company_profile
import os


print(f"Current Working Directory: {os.getcwd()}")

if __name__ == "__main__":
    # Get user input and convert to uppercase
    symbol_input = input(
        "Enter the stock symbol you want to monitor (e.g., AAPL, TSLA): ").upper()
    if not symbol_input:  # Basic input validation: check if input is empty
        print("No stock symbol entered. Exiting.")
        exit()  # Exit the script if no symbol is provided

    # --- Fetch Real-time Price and Company Profile ---
    endpoint_example = f"stock/real-time-price/{symbol_input}"
    realtime_price_data = fetch_fmp_data(endpoint_example)
    # Get company profile and extract name
    company_name = get_company_profile(symbol_input)

    if realtime_price_data and realtime_price_data.get(
            'companiesPriceList'):  # Check if data and companiesPriceList are not empty
        price_info = realtime_price_data['companiesPriceList'][0]
        if price_info:
            # Display company name and symbol
            if company_name:
                print(f"Company Name: {company_name} ({price_info['symbol']})")
            else:
                print(f"Real-time price data for {price_info['symbol']}:")

            print(f"  Price: {price_info['price']}")
        else:
            print(
                f"Could not retrieve real-time price for symbol: {symbol_input}")
    else:
        print(
            f"Failed to fetch real-time price data for symbol: {symbol_input}. Please check the symbol and API.")
    # --- Testing get_historical_price function ---
    # Use the symbol entered by the user for historical data
    symbol_to_test = symbol_input
    historical_data_aapl = get_historical_price(symbol_to_test)

    if historical_data_aapl:
        print(f"\nHistorical price data for {symbol_to_test}:")
        # Print just the first few historical data points to avoid too much
        for i in range(min(5, len(historical_data_aapl)
                           )):  # Print up to 5 entries
            print(historical_data_aapl[i])
        # Indicate total count
        print(
            f"... (Total {
                len(historical_data_aapl)} historical data points)")
    else:
        print(f"Failed to fetch historical price data for {symbol_to_test}.")