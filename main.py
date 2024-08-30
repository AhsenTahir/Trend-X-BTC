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


from binance.client import Client

def fetch_and_clean_binance_data(symbol, start_date, end_date, interval):

    client = Client(API_KEY, SECRET_KEY)
    
    # Fetching historical candlestick data
    klines = client.get_historical_klines(symbol, interval, start_date, end_date)
    
    # Creating a DataFrame
    df = pd.DataFrame(klines, columns=['Open time', 'Open', 'High', 'Low', 'Close', 'Volume',
                                       'Close time', 'Quote asset volume', 'Number of trades',
                                       'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore'])
    
    # Convert timestamp to readable date
    df['Open time'] = pd.to_datetime(df['Open time'], unit='ms')
    df['Close time'] = pd.to_datetime(df['Close time'], unit='ms')
    
    # Convert numeric values to float
    for col in ['Open', 'High', 'Low', 'Close', 'Volume', 'Quote asset volume',
                'Taker buy base asset volume', 'Taker buy quote asset volume']:
        df[col] = df[col].astype(float)
    
    # Data cleaning
    # Drop columns that are not required (e.g., 'Ignore')
    df.drop(columns=['Ignore', 'Close time'], inplace=True)
    
    # Handling missing values by forward filling
    df.ffill(inplace=True)
    
    return df

# Example usage
symbol = 'BTCUSDT'  # Bitcoin to USD Tether
start_date = "1 Jan, 2014"
end_date = "1 Jan, 2024"
interval = Client.KLINE_INTERVAL_1DAY  # Daily intervals

btc_data = fetch_and_clean_binance_data(symbol, start_date, end_date, interval)
print(btc_data.head())





# Initialize the Binance client
client = Client(API_KEY, SECRET_KEY)

# Function to fetch daily order flow data
def fetch_daily_order_flow(symbol, start_date, end_date):
    # Convert dates to milliseconds
    start_str = int(start_date.timestamp() * 1000)
    end_str = int(end_date.timestamp() * 1000)

    # Fetch historical klines data
    klines = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1DAY, start_str, end_str)
    
    # Create a DataFrame
    df = pd.DataFrame(klines, columns=['open_time', 'open', 'high', 'low', 'close', 'volume',
                                       'close_time', 'quote_asset_volume', 'number_of_trades',
                                       'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
    df['open_time'] = pd.to_datetime(df['open_time'], unit='ms')
    df.set_index('open_time', inplace=True)
    
    # Convert relevant columns to numeric
    df['volume'] = pd.to_numeric(df['volume'])
    df['taker_buy_base_asset_volume'] = pd.to_numeric(df['taker_buy_base_asset_volume'])

    # Calculate net order flow
    df['net_order_flow'] = df['taker_buy_base_asset_volume'] - (df['volume'] - df['taker_buy_base_asset_volume'])
    
    return df[['volume', 'taker_buy_base_asset_volume', 'net_order_flow']]

# Define the time periods
end_date = datetime.now()
intervals = [
    (end_date - timedelta(days=3652), end_date - timedelta(days=2434)),
    (end_date - timedelta(days=2435), end_date - timedelta(days=1217)),
    (end_date - timedelta(days=1218), end_date)
]

# Collect data over each interval
frames = []
for start, end in intervals:
    order_flow_data = fetch_daily_order_flow('BTCUSDT', start, end)
    frames.append(order_flow_data)
    print(f"Data fetched from {start.date()} to {end.date()}")

# Concatenate all data frames
full_data = pd.concat(frames)

# Basic EDA and Data Correction
print("\nBasic Exploratory Data Analysis:")
print("Data Summary:\n", full_data.describe())
print("Missing Values:\n", full_data.isnull().sum())

# Handling missing values, if any
full_data.ffill(inplace=True)  # forward fill to handle missing data

# Display the corrected DataFrame head
print("\nCorrected Data Head:\n", full_data.head())

