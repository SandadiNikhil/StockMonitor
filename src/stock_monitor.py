# import requests
# import pandas as pd
# import matplotlib.pyplot as plt
# import numpy as np
# from talib import EMA, RSI, OBV, VWAP

# # --- Step 1: Fetch the list of stocks ---

# def fetch_stock_list(api_key):
#     """
#     Fetches a list of available stock symbols from the FMP API.
#     """
#     url = f"https://financialmodelingprep.com/api/v3/stock/list?apikey={api_key}"
#     response = requests.get(url)
#     response.raise_for_status()
#     stocks = response.json()
#     return pd.DataFrame(stocks)

# # --- Step 2: Define your scoring function ---

# def get_stock_score(symbol, api_key, date=None):
#     """
#     Calculates the score (1-100) for a given stock symbol.
#     """
#     # --- Fetch fundamental data ---
#     # ... (Fetch key ratios, historical earnings - same as before)

#     # --- Fetch historical prices ---
#     historical_prices_url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{symbol}?apikey={api_key}"
#     historical_prices_response = requests.get(historical_prices_url)
#     historical_prices_response.raise_for_status()
#     historical_prices = pd.DataFrame(historical_prices_response.json()['historical'])
#     historical_prices['date'] = pd.to_datetime(historical_prices['date'])
#     historical_prices.set_index('date', inplace=True)

#     # --- Calculate technical indicators ---
#     historical_prices['200_EMA'] = EMA(historical_prices['close'], timeperiod=200)
#     historical_prices['RSI'] = RSI(historical_prices['close'], timeperiod=14)
#     historical_prices['OBV'] = OBV(historical_prices['close'], historical_prices['volume'])
#     historical_prices['VWAP'] = VWAP(historical_prices['high'], historical_prices['low'], 
#                                      historical_prices['close'], historical_prices['volume'])

#     # --- Analyze historical data (last 5 years, 4 quarters) ---
#     # ... (Extract and analyze data for different timeframes)

#     # --- Analyze technical price movement and breakout indications ---
#     # ... (Implement logic to analyze price patterns and breakout signals)

#     # --- Option Chain Analysis ---
#     option_chain_url = f"https://financialmodelingprep.com/api/v3/option-chain/{symbol}?apikey={api_key}"
#     # ... (Fetch and analyze option chain data)

#     # --- Calculate and normalize each factor ---
#     # ... (Include calculations for technical indicators, breakout signals, and option chain analysis)

#     # --- Calculate weighted average score ---
#     score = (
#         # ... (Fundamental factors with weights)
#         + 0.10 * ema_200_score  # Weight for 200-day EMA
#         + 0.075 * rsi_score  # Weight for RSI
#         + 0.075 * obv_score  # Weight for OBV
#         + 0.05 * vwap_score  # Weight for VWAP
#         + 0.15 * breakout_score  # Weight for Price Breakout
#         + 0.10 * option_chain_score  # Weight for Option Chain Analysis
#     )

#     return score

# # --- Step 3: Iterate through stocks and calculate scores ---

# def calculate_stock_scores(stocks, api_key, date=None):
#     """
#     Calculates scores for all stocks in the given DataFrame.
#     """
#     stock_scores = {}
#     for symbol in stocks['symbol']:
#         try:
#             score = get_stock_score(symbol, api_key, date)
#             stock_scores = score  # Correctly assign score to the dictionary
#         except Exception as e:
#             print(f"Error calculating score for {symbol}: {e}")
#     return stock_scores

# # --- Step 4: Filter and rank stocks ---

# def filter_and_rank_stocks(stock_scores, buy_threshold=70, sell_threshold=30):
#     """
#     Filter stocks into buy/sell signals based on their scores.
#     """
#     buy_signals = {symbol: score for symbol, score in stock_scores.items() 
#                   if score >= buy_threshold}
#     sell_signals = {symbol: score for symbol, score in stock_scores.items() 
#                    if score <= sell_threshold}
    
#     # Sort by score
#     buy_signals = dict(sorted(buy_signals.items(), key=lambda x: x[1], reverse=True))
#     sell_signals = dict(sorted(sell_signals.items(), key=lambda x: x[1]))
    
#     return buy_signals, sell_signals

# # --- Step 5: Display the results ---

# def display_results(buy_signals, sell_signals):
#     """
#     Display the buy and sell signals in a formatted way.
#     """
#     print("\nBUY SIGNALS:")
#     for symbol, score in buy_signals.items():
#         print(f"{symbol}: {score:.2f}")
        
#     print("\nSELL SIGNALS:")
#     for symbol, score in sell_signals.items():
#         print(f"{symbol}: {score:.2f}")

# if __name__ == "__main__":
#     api_key = "YOUR_API_KEY"  # Replace with your actual API key
#     stocks = fetch_stock_list(api_key)

#     # Calculate scores for current date
#     stock_scores = calculate_stock_scores(stocks, api_key)
#     buy_signals, sell_signals = filter_and_rank_stocks(stock_scores)
#     display_results(buy_signals, sell_signals)

#     # Example: Calculate scores for a specific date
#     historical_date = "2024-01-01"
#     historical_stock_scores = calculate_stock_scores(stocks, api_key, date=historical_date)
#     # ... (Filter and display historical results)