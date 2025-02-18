"""
    This module contains the display functions for the stock monitoring application.
    It formats and displays stock data in the console.
"""

from utils import formula

def display_stock_data(data):
    """
    Displays stock data in the console.
    Receives all data as a dictionary argument and formats it for console output.
    """
    symbol = data.get("symbol")
    company_name = data.get("company_name")
    real_time_price_data = data.get("real_time_price_data")
    historical_data = data.get("historical_data")
    key_ratios = data.get("key_ratios")
    ratio_scores = data.get("ratio_scores")
    weighted_scores = data.get("weighted_scores")
    total_fundamental_score_5yr_weight = data.get(
        "total_fundamental_score_5yr_weight")
    earnings_growth_data = data.get("earnings_growth_data")
    earnings_growth_score = data.get("earnings_growth_score")
    weighted_earnings_growth_score = data.get("weighted_earnings_growth_score")

    if company_name:
        print(f"Company Name: {company_name} ({symbol.upper()})")
    else:
        print(f"Company name not found for symbol: {symbol.upper()}")

    if real_time_price_data:
        print("\nReal-time price data for {}:".format(symbol.upper()))
        print(f"  Price: {real_time_price_data['price']:.2f}")
    else:
        print("\nCould not retrieve real-time price data for {}.".format(symbol.upper()))

    if historical_data:
        print("\nHistorical price data for {}:".format(symbol.upper()))
        # Display the latest 5 historical data points (for brevity)
        for data_point in historical_data[:5]:
            print(data_point)
        print(f"... (Total {len(historical_data)} historical data points) ...")
    else:
        print(
            "\nCould not retrieve historical price data for {}.".format(
                symbol.upper()))

    if key_ratios and len(key_ratios) > 0:
        key_ratios_data = key_ratios[0]  # Latest fiscal year ratios
        print("\nKey Ratios (Latest Fiscal Year):")
        print(f"  P/E Ratio: {key_ratios_data.get('priceEarningsRatio')}")
        print(f"  P/B Ratio: {key_ratios_data.get('priceBookValueRatio')}")
        print(f"  D/E Ratio: {key_ratios_data.get('debtEquityRatio')}")
        print(f"  ROE: {key_ratios_data.get('returnOnEquity')}")

        if ratio_scores:
            print("\nFundamental Ratio Scores (out of 10):")
            print(f"  P/E Ratio Score: {ratio_scores.get('pe_score')}")
            print(f"  P/B Ratio Score: {ratio_scores.get('pb_score')}")
            print(f"  D/E Ratio Score: {ratio_scores.get('de_score')}")
            print(f"  ROE Score: {ratio_scores.get('roe_score')}")

        if weighted_scores:
            # Show formula module name for clarity
            print(
                f"\nWeighted Fundamental Scores (using 5-Year Weights from {formula.__name__}.py):")
            print(
                f"  Weighted P/E Ratio Score: {weighted_scores.get('weighted_pe_score'):.2f}")
            print(
                f"  Weighted P/B Ratio Score: {weighted_scores.get('weighted_pb_score'):.2f}")
            print(
                f"  Weighted D/E Ratio Score: {weighted_scores.get('weighted_de_score'):.2f}")
            print(
                f"  Weighted ROE Score: {
                    weighted_scores.get('weighted_roe_score'):.2f}")

        if total_fundamental_score_5yr_weight is not None:  # Check if score is calculated before displaying
            print(
                f"\nTotal Fundamental Score (5-Year Weighting, out of 100): {
                    total_fundamental_score_5yr_weight:.2f}")
    else:
        print("\nCould not retrieve key ratios for {}.".format(symbol.upper()))

    # --- Earnings Growth Rate Section ---
    if earnings_growth_data:
        # Still placeholder message
        print(
            "\nEarnings Growth Rate Data (PLACEHOLDER - NOT YET IMPLEMENTED API FUNCTION):")
        print(earnings_growth_data)

        if earnings_growth_score is not None:  # Check if score is calculated before displaying
            print("\nEarnings Growth Rate Score (PLACEHOLDER - NOT YET IMPLEMENTED):")
            print(f"  Earnings Growth Rate Score: {earnings_growth_score}")
            print(
                f"  Weighted Earnings Growth Rate Score: {
                    weighted_earnings_growth_score:.2f}")
    else:
        print("\nCould not retrieve Earnings Growth Rate data (PLACEHOLDER - API function not yet implemented).".format(symbol.upper()))


def main():
    """
    This display.py module's main function could be used for testing display output.
    However, for the primary application flow, display is called by stock.py.
    This main function here is optional and for potential display-specific testing.
    """
    print("display.py: This module is for display functions and is called by stock.py.")
    print("It does not run independently in the main application flow for console output.")
    print("You might use this main function for testing display output if needed.")


if __name__ == "__main__":
    main()  # Optional: Main function for display module testing