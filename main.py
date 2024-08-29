import requests
import pandas as pd
from datetime import datetime
import hmac
import hashlib
import time
import configparser
import os
from datetime import datetime, timedelta
from config import Binance_api_key, Binance_secret_key, News_sentiment_api_key
# Initialize the config parser



# Your API key and secret key from Binance
API_KEY = Binance_api_key
SECRET_KEY = Binance_secret_key
print(API_KEY)
print(SECRET_KEY)
print(News_sentiment_api_key)
# Base URL for Binance API
BASE_URL = 'https://api.binance.com'

# Function to fetch historical data (e.g., last 1000 1-minute candles)
def fetch_historical_data(symbol='BTCUSDT', interval='1m', limit=1000):
    endpoint = f'/api/v3/klines'
    params = {
        'symbol': symbol,
        'interval': interval,
        'limit': limit
    }
    url = BASE_URL + endpoint
    response = requests.get(url, params=params)
    data = response.json()

    df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 
                                     'close_time', 'quote_asset_volume', 'number_of_trades', 
                                     'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]

# Function to fetch real-time data (24hr ticker price change statistics)
def fetch_real_time_data(symbol='BTCUSDT'):
    endpoint = '/api/v3/ticker/24hr'
    params = {'symbol': symbol}
    url = BASE_URL + endpoint
    response = requests.get(url, params=params)
    data = response.json()

    df = pd.DataFrame([{
        'timestamp': datetime.now(),
        'symbol': symbol,
        'last_price': data['lastPrice'],
        'price_change': data['priceChange'],
        'price_change_percent': data['priceChangePercent'],
        'volume': data['volume'],
        'quote_volume': data['quoteVolume'],
        'high_price': data['highPrice'],
        'low_price': data['lowPrice'],
        'bid_price': data['bidPrice'],
        'ask_price': data['askPrice']
    }])
    return df


def get_news_sentiment(api_key, tickers=None, topics=None):
    # Define the base URL for the API request
    base_url = "https://www.alphavantage.co/query"
    
    # Set the function parameter for the API request
    function = "NEWS_SENTIMENT"
    
    # Calculate the date range for the past 10 years
    end_date = datetime.now()
    start_date = end_date - timedelta(days=10 * 365)  # Approximate 10 years
    
    # Convert dates to the required format: YYYYMMDDTHHMM
    time_from = start_date.strftime("%Y%m%dT%H%M")
    time_to = end_date.strftime("%Y%m%dT%H%M")
    
    # Prepare the parameters for the API request
    params = {
        "function": function,
        "apikey": api_key,
        "time_from": time_from,
        "time_to": time_to,
        "sort": "EARLIEST",  # Retrieve data starting from the earliest date
        "limit": 1000  # Set a high limit to retrieve as much data as possible
    }
    
    # Add optional filters if provided
    if tickers:
        params["tickers"] = ",".join(tickers)
    if topics:
        params["topics"] = ",".join(topics)
    
    # Make the API request
    response = requests.get(base_url, params=params)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        
        # Extract data and convert it to a DataFrame
        if "feed" in data:
            news_data = data["feed"]
            df = pd.DataFrame(news_data)
            return df
        else:
            print("No data found.")
            return pd.DataFrame()  # Return an empty DataFrame if no data found
    else:
        # Handle errors
        print(f"Error: {response.status_code}")
        return pd.DataFrame()  # Return an empty DataFrame in case of an error


df_News_Data=get_news_sentiment(News_sentiment_api_key)
print(df_News_Data)
#commenting for a while
# Fetch historical data
# historical_df = fetch_historical_data()
# print("Historical Data:")
# print(historical_df.shape[0])

# # Fetch real-time data
# real_time_df = fetch_real_time_data()
# print("\nReal-Time Data:")
# print(real_time_df)
