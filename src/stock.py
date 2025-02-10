# src/stock.py
import os
import fmp_api
import formula
import display  # Import the display module


def run_stock_monitor(symbol):
    """
    Orchestrates the stock monitoring process for a given symbol.
    Fetches data, calculates scores, and displays results using other modules.
    """
    # --- Fetch data using fmp_api module ---
    company_name = fmp_api.get_company_profile(symbol)
    real_time_price_data = fmp_api.get_realtime_price(symbol)
    historical_data = fmp_api.get_historical_price(symbol)
    key_ratios = fmp_api.get_company_key_ratios(symbol)
    earnings_growth_data = fmp_api.get_earnings_growth_rate(symbol) # Fetch earnings growth data

    if company_name is None:
        print(f"Warning: Could not retrieve company name for symbol: {symbol.upper()}.") # Warning if company name is None

    if real_time_price_data is None:
        print(f"Warning: Could not retrieve real-time price data for {symbol.upper()}.") # Warning if real-time price is None

    if historical_data is None:
        print(f"Warning: Could not retrieve historical price data for {symbol.upper()}.") # Warning if historical data is None

    if key_ratios is None:
        print(f"Warning: Could not retrieve key ratios for {symbol.upper()}. Fundamental scores will be limited.") # Warning if key ratios are None

    if earnings_growth_data is None:
        print(f"Warning: Could not retrieve Earnings Growth Rate data for {symbol.upper()}. This metric will be excluded from scoring.") # Specific warning for earnings growth


    # --- Prepare data for scoring and display ---
    ratio_scores = {}
    weighted_scores = {}
    total_fundamental_score_5yr_weight = None
    earnings_growth_score = None
    weighted_earnings_growth_score = None


    if key_ratios and len(key_ratios) > 0:
        key_ratios_data = key_ratios[0]  # Latest fiscal year ratios
        pe_ratio_value = key_ratios_data.get('priceEarningsRatio')
        pb_ratio_value = key_ratios_data.get('priceBookValueRatio')
        de_ratio_value = key_ratios_data.get('debtEquityRatio')
        roe_value = key_ratios_data.get('returnOnEquity')

        # --- Calculate Ratio Scores (using formula module) ---
        ratio_scores['pe_score'] = formula.score_pe_ratio(pe_ratio_value)
        ratio_scores['pb_score'] = formula.score_pb_ratio(pb_ratio_value)
        ratio_scores['de_score'] = formula.score_de_ratio(de_ratio_value)
        ratio_scores['roe_score'] = formula.score_roe(roe_value)

        # --- Calculate Weighted Scores and Total Fundamental Score (using formula module weights) ---
        weighted_scores['weighted_pe_score'] = ratio_scores['pe_score'] * formula.WEIGHTS_5_YEAR["pe_ratio"]
        weighted_scores['weighted_pb_score'] = ratio_scores['pb_score'] * formula.WEIGHTS_5_YEAR["pb_ratio"]
        weighted_scores['weighted_de_score'] = ratio_scores['de_score'] * formula.WEIGHTS_5_YEAR["de_ratio"]
        weighted_scores['weighted_roe_score'] = ratio_scores['roe_score'] * formula.WEIGHTS_5_YEAR["roe"]

        total_fundamental_score_5yr_weight = (
            weighted_scores['weighted_pe_score'] + weighted_scores['weighted_pb_score'] +
            weighted_scores['weighted_de_score'] + weighted_scores['weighted_roe_score']
        ) * 100

    # --- Earnings Growth Rate Section ---
    if earnings_growth_data:
        earnings_growth_rate_value = earnings_growth_data # Assuming API now returns growth rate as a float directly
        earnings_growth_score = formula.score_earnings_growth_rate(earnings_growth_rate_value)  # Score it
        weighted_earnings_growth_score = earnings_growth_score * formula.WEIGHTS_5_YEAR["earnings_growth"] # Apply weight
    else:
        earnings_growth_score = None
        weighted_earnings_growth_score = None


    # --- Prepare data dictionary for display ---
    display_data = {
        "symbol": symbol,
        "company_name": company_name,
        "real_time_price_data": real_time_price_data,
        "historical_data": historical_data,
        "key_ratios": key_ratios,
        "ratio_scores": ratio_scores,
        "weighted_scores": weighted_scores,
        "total_fundamental_score_5yr_weight": total_fundamental_score_5yr_weight,
        "earnings_growth_data": earnings_growth_data,
        "earnings_growth_score": earnings_growth_score,
        "weighted_earnings_growth_score": weighted_earnings_growth_score,
    }

    # --- Display data using display module ---
    display.display_stock_data(display_data) # Call display function in display.py


def main():
    """
    Main function to get user input and run the stock monitoring process.
    This function is the entry point when stock.py is executed.
    """
    # print(f"Current Working Directory: {os.getcwd()}")
    stock_symbol = input("Enter the stock symbol you want to monitor (e.g., AAPL, TSLA): ").strip().upper()

    if not stock_symbol:
        print("No stock symbol entered. Please run the script again and enter a symbol.")
        return 

    run_stock_monitor(stock_symbol) 


if __name__ == "__main__":
    main()