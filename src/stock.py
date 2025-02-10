import os
import fmp_api

# --- Scoring Functions for Fundamental Ratios ---
def score_pe_ratio(pe_ratio):
    """Scores Price-to-Earnings Ratio. Lower P/E is generally better (undervalued)."""
    if pe_ratio is None:  # Handle missing data
        return 0
    if pe_ratio < 0: # Negative P/E can be tricky, treat cautiously for now, score low
        return 2
    if pe_ratio < 15:
        return 10
    elif 15 <= pe_ratio <= 25:
        return 5
    else:
        return 1

def score_pb_ratio(pb_ratio):
    """Scores Price-to-Book Ratio. Lower P/B is generally better (undervalued)."""
    if pb_ratio is None:  # Handle missing data
        return 0
    if pb_ratio < 1:
        return 10
    elif 1 <= pb_ratio <= 3:
        return 5
    else:
        return 1

def score_de_ratio(de_ratio):
    """Scores Debt-to-Equity Ratio. Lower D/E is generally better (less risky)."""
    if de_ratio is None:  # Handle missing data
        return 0
    if de_ratio < 1:
        return 10
    elif 1 <= de_ratio <= 2:
        return 5
    else:
        return 1

def score_roe(roe):
    """Scores Return on Equity. Higher ROE is generally better (more profitable)."""
    if roe is None:  # Handle missing data
        return 0
    roe_percentage = roe * 100 # Convert ROE to percentage
    if roe_percentage > 15:
        return 10
    elif 10 <= roe_percentage <= 15:
        return 5
    else:
        return 1

def score_earnings_growth_rate(growth_rate):
    """Scores Earnings Growth Rate. Higher growth is better."""
    if growth_rate is None:  # Handle missing data
        return 0
    growth_percentage = growth_rate * 100 # Convert to percentage if needed
    if growth_percentage > 10:
        return 10
    elif 5 <= growth_percentage <= 10:
        return 5
    else:
        return 1
# --- End of Scoring Functions ---


def display_stock_data(symbol):
    """
    Fetches and displays stock data for a given symbol using functions from fmp_api.py.
    Includes scoring of fundamental ratios.
    """
    company_name = fmp_api.get_company_profile(symbol)
    if company_name:
        print(f"Company Name: {company_name} ({symbol.upper()})")
    else:
        print(f"Company name not found for symbol: {symbol.upper()}")

    real_time_price = fmp_api.get_realtime_price(symbol)
    if real_time_price:
        print("\nReal-time price data for {}:".format(symbol.upper()))
        print(f"  Price: {real_time_price['price']:.2f}")
    else:
        print("\nCould not retrieve real-time price data for {}.".format(symbol.upper()))

    historical_data = fmp_api.get_historical_price(symbol)
    if historical_data:
        print("\nHistorical price data for {}:".format(symbol.upper()))
        # Display the latest 5 historical data points (for brevity)
        for data_point in historical_data[:5]:
            print(data_point)
        print(f"... (Total {len(historical_data)} historical data points)")
    else:
        print("\nCould not retrieve historical price data for {}.".format(symbol.upper()))

    # key_ratios_list = fmp_api.get_company_key_ratios(symbol) # Get ratios data as list
    # if key_ratios_list and len(key_ratios_list) > 0: # Check if list is valid and not empty
    #     key_ratios = key_ratios_list[0] # Assuming we want the latest ratios, take the first element
    #     print("\nKey Ratios (Latest Fiscal Year):")
    #     pe_ratio_value = key_ratios.get('priceEarningsRatio')
    #     pb_ratio_value = key_ratios.get('priceBookValueRatio')
    #     de_ratio_value = key_ratios.get('debtEquityRatio')
    #     roe_value = key_ratios.get('returnOnEquity')

    #     print(f"  P/E Ratio: {pe_ratio_value}")
    #     print(f"  P/B Ratio: {pb_ratio_value}")
    #     print(f"  D/E Ratio: {de_ratio_value}")
    #     print(f"  ROE: {roe_value}")

    #     # --- Calculate and display scores ---
    #     pe_score = score_pe_ratio(pe_ratio_value)
    #     pb_score = score_pb_ratio(pb_ratio_value)
    #     de_score = score_de_ratio(de_ratio_value)
    #     roe_score = score_roe(roe_value)

    #     print("\nFundamental Ratio Scores (out of 10):")
    #     print(f"  P/E Ratio Score: {pe_score}")
    #     print(f"  P/B Ratio Score: {pb_score}")
    #     print(f"  D/E Ratio Score: {de_score}")
    #     print(f"  ROE Score: {roe_score}")

    # else:
    #     print("\nCould not retrieve key ratios for {}.".format(symbol.upper()))


   # --- Calculate Ratio Scores ---
    pe_score = formula.score_pe_ratio(pe_ratio_value)  # Use formula.score_pe_ratio
    pb_score = formula.score_pb_ratio(pb_ratio_value)  # Use formula.score_pb_ratio
    de_score = formula.score_de_ratio(de_ratio_value)  # Use formula.score_de_ratio
    roe_score = formula.score_roe(roe_value)        # Use formula.score_roe

    print("\nFundamental Ratio Scores (out of 10):")
    print(f"  P/E Ratio Score: {pe_score}")
    print(f"  P/B Ratio Score: {pb_score}")
    print(f"  D/E Ratio Score: {de_score}")
    print(f"  ROE Score: {roe_score}")

    # --- Calculate Weighted Scores and Total Fundamental Score (using 5-Year Weights for now) ---
    weighted_pe_score = pe_score * formula.WEIGHTS_5_YEAR["pe_ratio"] # Use formula.WEIGHTS_5_YEAR
    weighted_pb_score = pb_score * formula.WEIGHTS_5_YEAR["pb_ratio"] # Use formula.WEIGHTS_5_YEAR
    weighted_de_score = de_score * formula.WEIGHTS_5_YEAR["de_ratio"] # Use formula.WEIGHTS_5_YEAR
    weighted_roe_score = roe_score * formula.WEIGHTS_5_YEAR["roe"]   # Use formula.WEIGHTS_5_YEAR

    total_fundamental_score_5yr_weight = (
        weighted_pe_score + weighted_pb_score + weighted_de_score + weighted_roe_score
    ) * 100

    print("\nWeighted Fundamental Scores (using 5-Year Weights):")
    print(f"  Weighted P/E Ratio Score: {weighted_pe_score:.2f}")
    print(f"  Weighted P/B Ratio Score: {weighted_pb_score:.2f}")
    print(f"  Weighted D/E Ratio Score: {weighted_de_score:.2f}")
    print(f"  Weighted ROE Score: {weighted_roe_score:.2f}")

    print(f"\nTotal Fundamental Score (5-Year Weighting, out of 100): {total_fundamental_score_5yr_weight:.2f}")

    # --- Earnings Growth Rate Section (placeholder) ---
    earnings_growth_data = fmp_api.get_earnings_growth_rate(symbol)
    if earnings_growth_data:
        print("\nEarnings Growth Rate Data (PLACEHOLDER - NOT YET IMPLEMENTED API FUNCTION):")
        print(earnings_growth_data)

        earnings_growth_rate_value = 0.05
        earnings_growth_score = formula.score_earnings_growth_rate(earnings_growth_rate_value) # Use formula.score_earnings_growth_rate
        weighted_earnings_growth_score = earnings_growth_score * formula.WEIGHTS_5_YEAR["earnings_growth"] # Use formula.WEIGHTS_5_YEAR

        print("\nEarnings Growth Rate Score (PLACEHOLDER - NOT YET IMPLEMENTED):")
        print(f"  Earnings Growth Rate Score: {earnings_growth_score}")
        print(f"  Weighted Earnings Growth Rate Score: {weighted_earnings_growth_score:.2f}")

    else:
        print("\nCould not retrieve key ratios for {}.".format(symbol.upper()))


if __name__ == "__main__":
    # Get user input and convert to uppercase
    print(f"Current Working Directory: {os.getcwd()}")

    stock_symbol = input("Enter the stock symbol you want to monitor (e.g., AAPL, TSLA): ").strip().upper()

    if stock_symbol:
        display_stock_data(stock_symbol)
    else:
        print("No stock symbol entered. Please run the script again and enter a symbol.")

    # symbol_input = input(
    #     "Enter the stock symbol you want to monitor (e.g., AAPL, TSLA): ").upper()
    # if not symbol_input:  # Basic input validation: check if input is empty
    #     print("No stock symbol entered. Exiting.")
    #     exit()  # Exit the script if no symbol is provided

    # # --- Fetch Real-time Price and Company Profile ---
    # endpoint_example = f"stock/real-time-price/{symbol_input}"
    # realtime_price_data = fetch_fmp_data(endpoint_example)
    # # Get company profile and extract name
    # company_name = get_company_profile(symbol_input)

    # if realtime_price_data and realtime_price_data.get(
    #         'companiesPriceList'):  # Check if data and companiesPriceList are not empty
    #     price_info = realtime_price_data['companiesPriceList'][0]
    #     if price_info:
    #         # Display company name and symbol
    #         if company_name:
    #             print(f"Company Name: {company_name} ({price_info['symbol']})")
    #         else:
    #             print(f"Real-time price data for {price_info['symbol']}:")

    #         print(f"  Price: {price_info['price']}")
    #     else:
    #         print(
    #             f"Could not retrieve real-time price for symbol: {symbol_input}")
    # else:
    #     print(
    #         f"Failed to fetch real-time price data for symbol: {symbol_input}. Please check the symbol and API.")
    # # --- Testing get_historical_price function ---
    # # Use the symbol entered by the user for historical data
    # symbol_to_test = symbol_input
    # historical_data_aapl = get_historical_price(symbol_to_test)

    # if historical_data_aapl:
    #     print(f"\nHistorical price data for {symbol_to_test}:")
    #     # Print just the first few historical data points to avoid too much
    #     for i in range(min(5, len(historical_data_aapl)
    #                        )):  # Print up to 5 entries
    #         print(historical_data_aapl[i])
    #     # Indicate total count
    #     print(
    #         f"... (Total {
    #             len(historical_data_aapl)} historical data points)")
    # else:
    #     print(f"Failed to fetch historical price data for {symbol_to_test}.")