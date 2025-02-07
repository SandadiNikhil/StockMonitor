from dotenv import load_dotenv
import os
import requests

load_dotenv(dotenv_path='env/key.env')

API_KEY = os.environ.get("apikey") 
URL = os.environ.get("base_url")  

print(f"API Key from env: {API_KEY}")  #
print(f"Base URL from env: {URL}")

def fetch_fmp_data(endpoint):
    params = {'apikey': API_KEY}
    url = f"{URL}/{endpoint}"  
    response = requests.get(url, params=params)
    return response.json()

def get_historical_price(symbol):
    endpoint = f"historical-price-full/{symbol}" # API endpoint for historical prices
    data = fetch_fmp_data(endpoint) # Re-use our fetch_fmp_data function
    if data and 'historical' in data: # Check if data and 'historical' key exist
        return data['historical'] # Return the list of historical price data
    return None # Return None if there's an issue fetching data

if __name__ == "__main__":
    
    symbol_input = input("Enter the stock symbol you want to monitor (e.g., AAPL, TSLA): ").upper() # Get user input and convert to uppercase
    if not symbol_input:
        print("No symbol provided. Exiting.")
        exit()

    endpoint_example = f"stock/real-time-price/{symbol_input}"    
    realtime_price_data = fetch_fmp_data(endpoint_example)

    if realtime_price_data:
        print("Real-time price data for AAPL:")
        print(realtime_price_data)
    else:
        print("Failed to fetch real-time price data for AAPL.")

    symbol = "AAPL"
    historical_data = get_historical_price(symbol)

    if realtime_price_data and realtime_price_data.get('companiesPriceList'): 
        price_info = realtime_price_data['companiesPriceList'][0] 
        if price_info:
            print(f"Real-time price data for {price_info['symbol']}:") 
            print(f"  Price: {price_info['price']}") 
        else:
            print(f"Could not retrieve real-time price for symbol: {symbol_input}")

    else:
        print(f"Failed to fetch real-time price data for symbol: {symbol_input}. Please check the symbol and API.")

    symbol_to_test = symbol_input 
    historical_data_aapl = get_historical_price(symbol_to_test)