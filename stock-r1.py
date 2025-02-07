import requests

FMP_API_KEY = 'beiGwJS2f85S2dTC7rAxR0qZ4aO8S9oB'
BASE_URL = 'https://financialmodelingprep.com/api/v3'

def fetch_fmp_data(endpoint):
    params= {'apikey': FMP_API_KEY}
    url = f"{BASE_URL}/{endpoint}"
    response = requests.get(url, params=params)
    return response.json()

if __name__ == "__main__":
    # Example endpoint to get real-time price of Apple (AAPL)
    endpoint_example = "stock/real-time-price/AAPL"
    realtime_price_data = fetch_fmp_data(endpoint_example)

    if realtime_price_data: # Check if we got data back
        print("Real-time price data for AAPL:")
        print(realtime_price_data)
    else:
        print("Failed to fetch real-time price data for AAPL.")
