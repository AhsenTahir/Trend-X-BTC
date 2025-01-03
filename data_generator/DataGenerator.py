import requests
import pandas as pd
from datetime import datetime
import hmac
import hashlib
import time
import configparser
import os
from datetime import datetime, timedelta
import sys
from pandas_datareader import data as pdr
from packaging.version import Version as LooseVersion
from google.cloud import bigquery

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "blockchain_data.json"

from config import Binance_api_key, Binance_secret_key, News_sentiment_api_key, RSI_api_key, Fred_api_key
# Initialize the config parser



# Your API key and secret key from Binance
API_KEY = Binance_api_key
SECRET_KEY = Binance_secret_key
print(API_KEY)
print(SECRET_KEY)
print(News_sentiment_api_key)
# Base URL for Binance API
BASE_URL = 'https://api.binance.com'




def get_combined_fear_greed_data():
    # Step 1: Load historical data
    historical_url = 'https://raw.githubusercontent.com/gman4774/Fear_and_Greed_Index/main/all_fng_csv.csv'
    df_historical = pd.read_csv(historical_url)

    # Ensure consistent column names and datetime format
    df_historical = df_historical.rename(columns={'Fear Greed': 'value'})
    df_historical['Date'] = pd.to_datetime(df_historical['Date'])
    
    # Define the date range you are working with
    start_date = pd.to_datetime('2017-08-17')
    end_date = datetime.now()
    df_historical = df_historical[(df_historical['Date'] >= start_date) & (df_historical['Date'] <= end_date)]

    # Step 2: Fetch recent data from alternative.me
    def fetch_fear_greed_alternative():
        api_url = 'https://api.alternative.me/fng/?limit=1000'
        response = requests.get(api_url)
        data = response.json()

        # Convert the JSON data into a DataFrame
        df = pd.DataFrame(data['data'])
        df['timestamp'] = pd.to_numeric(df['timestamp'], errors='coerce')
        df.dropna(subset=['timestamp'], inplace=True)
        df['Date'] = pd.to_datetime(df['timestamp'], unit='s')
        
        # Format and filter the real-time data
        df = df.rename(columns={'value': 'value'})
        df['value'] = pd.to_numeric(df['value'], errors='coerce')
        return df[['Date', 'value']]

    # Fetch and filter real-time data to avoid duplicates
    df_realtime = fetch_fear_greed_alternative()
    df_realtime = df_realtime[df_realtime['Date'] > df_historical['Date'].max()]

    # Step 3: Merge historical and recent data
    df_merged = pd.concat([df_historical[['Date', 'value']], df_realtime], ignore_index=True)

    # Generate a complete date range from 17th August 2017 to current date
    full_date_range = pd.date_range(start=start_date, end=end_date)
    df_merged = pd.merge(pd.DataFrame(full_date_range, columns=['Date']), df_merged, on='Date', how='left')

    # Fill missing values
    df_merged['value'] = df_merged['value'].replace(0, pd.NA).ffill()

    # Classify Fear and Greed levels
    def classify_fear_greed(value):
        if value <= 24:
            return 'Extreme Fear'
        elif 25 <= value <= 49:
            return 'Fear'
        elif value == 50:
            return 'Neutral'
        elif 51 <= value <= 74:
            return 'Greed'
        elif value >= 75:
            return 'Extreme Greed'

    df_merged['classification'] = df_merged['value'].apply(classify_fear_greed)

    # Sort and clean the data
    df_merged.sort_values('Date', inplace=True)
    df_merged = df_merged[df_merged['Date'] <= end_date]

    return df_merged



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
start_date = "17 Aug, 2017"
end_date = "1 Jan, 2024"
interval = Client.KLINE_INTERVAL_1DAY  # Daily intervals

# btc_data = fetch_and_clean_binance_data(symbol, start_date, end_date, interval)
# print(btc_data.head())


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





def Binance_Data(symbol='BTCUSDT', interval='1d'):
    client = Client(API_KEY, SECRET_KEY)
    
    # Define the time range for the API call
    end_date = datetime.now()
    start_date = datetime.strptime("17 Aug, 2017", "%d %b, %Y")
    #start_date = end_date - timedelta(days=365 * 10)  # Start date 10 years ago

    # Fetch data in a single call
    data = fetch_and_clean_binance_data(
        symbol, 
        start_date.strftime("%d %b, %Y"), 
        end_date.strftime("%d %b, %Y"), 
        interval
    )
    
    print("Binance data overall")
    print(data.shape[0])
    return data

# Function to get the current date
def get_current_date():
    return datetime.now().date()

# CPI function (changed)
def get_cpi_data(News_sentiment_api_key, start_date='2017-08-17', end_date=None):
    if end_date is None:
        end_date = get_current_date()
    
    # Define the URL with your API key
    url = f'https://www.alphavantage.co/query?function=CPI&interval=monthly&apikey={News_sentiment_api_key}'
    
    # Fetch the data
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data: {response.status_code}")
    
    # Parse the JSON response
    data = response.json()
    
    # Check if data is valid
    if 'data' not in data:
        raise Exception("Invalid data received from the API")
    
    # Convert the data into a DataFrame
    df = pd.DataFrame(data['data'])
    df.rename(columns={'value': 'CPI'}, inplace=True)
    
    # Convert the 'date' column to datetime format and sort the DataFrame
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    
    # Filter data from the start_date to end_date
    df = df[(df['date'] >= pd.to_datetime(start_date)) & (df['date'] <= pd.to_datetime(end_date))]
    
    # Since the data is monthly, we'll forward fill the missing days to create a daily DataFrame
    df.set_index('date', inplace=True)
    df = df.resample('D').ffill().reset_index()  # Forward fill to get daily values

    return df

def get_inflation_data(start_date='2017-08-17', end_date=None):
    if end_date is None:
        end_date = datetime.now()
    
    # Define the start and end years for the detailed data range
    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    end_dt = end_date

    # Fetch the CPI data using the FRED API key (Note: you should have this key configured)
    cpi_data = pdr.get_data_fred('CPIAUCSL', start_dt, end_dt)
    
    # Calculate yearly inflation rate based on CPI changes
    cpi_data['Inflation Rate'] = cpi_data['CPIAUCSL'].pct_change(12) * 100  # Annual percentage change
    
    # Resample the data annually and take the last available data each year
    annual_inflation_rate = cpi_data['Inflation Rate'].resample('YE').last().dropna()
    
    # Create a date range for each day from the start date to the end date
    daily_date_range = pd.date_range(start=start_date, end=end_date.strftime("%Y-%m-%d"))
    
    # Create a daily dataframe from the annual data
    daily_inflation_rate = pd.DataFrame(index=daily_date_range, columns=['Inflation Rate'])
    
    # Convert annual_inflation_rate to a Series with the year as its index for easier access
    annual_inflation_rate.index = annual_inflation_rate.index.year
    
    # Assign the annual inflation rate to each day of the respective year
    for year in range(start_dt.year, end_dt.year + 1):
        if year in annual_inflation_rate.index:
            # Mask to identify dates within the current year
            mask = (daily_inflation_rate.index.year == year)
            # Assign the yearly inflation rate to each day in the year
            daily_inflation_rate.loc[mask, 'Inflation Rate'] = annual_inflation_rate.loc[year]
    
    daily_inflation_rate.reset_index(inplace=True)
    daily_inflation_rate.rename(columns={'index': 'Date'}, inplace=True)
    
    return daily_inflation_rate

#RSI DATA

def calculate_rsi(data, window=14):
    change = data.diff()
    gains = (change.where(change > 0, 0)).rolling(window=window).mean()
    losses = (-change.where(change < 0, 0)).rolling(window=window).mean()
    rs = gains / losses
    rsi = 100 - (100 / (1 + rs))
    return rsi

def fetch_data_segment(api_key, fsym, tsym, to_timestamp):
    url = "https://min-api.cryptocompare.com/data/v2/histoday"
    parameters = {
        "fsym": fsym,
        "tsym": tsym,
        "limit": 2000,
        "toTs": to_timestamp,
        "api_key": api_key,
    }
    response = requests.get(url, params=parameters)
    if response.status_code == 200:
        data = response.json()
        if 'Data' in data and 'Data' in data['Data']:
            df = pd.DataFrame(data['Data']['Data'])
            df['time'] = pd.to_datetime(df['time'], unit='s')
            return df
        else:
            return pd.DataFrame()
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return pd.DataFrame()

def fetch_and_calculate_rsi(api_key, fsym="BTC", tsym="USD", start_date="2017-08-17"):
    end_date = datetime.now()
    start_timestamp = int(datetime.strptime(start_date, "%Y-%m-%d").timestamp())
    end_timestamp = int(end_date.timestamp())
    
    df_full = pd.DataFrame()
    current_timestamp = end_timestamp

    while current_timestamp > start_timestamp:
        df_segment = fetch_data_segment(api_key, fsym, tsym, current_timestamp)
        if df_segment.empty:
            break
        df_full = pd.concat([df_full, df_segment], ignore_index=True)
        current_timestamp = df_segment['time'].min().timestamp() - 1  # Ensure no overlap and cover all days
        
    if not df_full.empty:
        df_full.sort_values('time', inplace=True)
        df_full.set_index('time', inplace=True)
        df_full['RSI'] = calculate_rsi(df_full['close']).bfill()
        return df_full[['close', 'RSI']]
    else:
        return "No data found or error in fetching data."
    
def fetch_bigquery_data():
    client = bigquery.Client()
    
    # Define the query
    query = """
    SELECT
      DATE(transactions.block_timestamp) AS date,
      AVG(CAST(blocks.size AS INT64)) AS avg_block_size,
      COUNT(DISTINCT inputs.spent_transaction_hash) AS num_user_addresses,
      COUNT(DISTINCT transactions.hash) AS num_transactions,
      SUM(CAST(transactions.fee AS INT64) + 
          IF(DATE(transactions.block_timestamp) < '2016-07-09', 50 * 100000000,
          IF(DATE(transactions.block_timestamp) < '2020-05-11', 12.5 * 100000000, 6.25 * 100000000))) AS miners_revenue
    FROM
      `bigquery-public-data.crypto_bitcoin.blocks` AS blocks
    JOIN
      `bigquery-public-data.crypto_bitcoin.transactions` AS transactions
      ON blocks.hash = transactions.block_hash
    JOIN
      UNNEST(transactions.inputs) AS inputs
    WHERE
      DATE(transactions.block_timestamp) >= '2017-08-17' AND DATE(transactions.block_timestamp) <= CURRENT_DATE()
    GROUP BY
      date
    ORDER BY
      date ASC;
    """

    # Run the query and collect results
    query_job = client.query(query)
    results = query_job.result()  # Wait for the query to finish

    # Process results into DataFrame
    data = []
    for row in results:
        data.append({
            'Date': row.date,
            'avg_block_size': row.avg_block_size,
            'num_user_addresses': row.num_user_addresses,
            'num_transactions': row.num_transactions,
            'miners_revenue': row.miners_revenue
        })

    df_bigquery = pd.DataFrame(data)
    return df_bigquery

def Data_Generator():
    # Fetch Binance Data
    btc_full_data = Binance_Data(symbol='BTCUSDT', interval='1d')
    btc_full_data.rename(columns={'Open time': 'Date'}, inplace=True)

    # Daily Order Flow Data
    frames = []
    for start, end in intervals:
        order_flow_data = fetch_daily_order_flow('BTCUSDT', start, end)
        frames.append(order_flow_data)
    full_order_flow_data = pd.concat(frames)
    full_order_flow_data.reset_index(inplace=True)
    full_order_flow_data.rename(columns={'open_time': 'Date'}, inplace=True)

    # RSI Data
    rsi_data = fetch_and_calculate_rsi(RSI_api_key, start_date="2017-08-17")
    rsi_data.reset_index(inplace=True)
    rsi_data.rename(columns={'time': 'Date'}, inplace=True)

    # Inflation Data
    inflation_data = get_inflation_data(start_date='2017-08-17')
    inflation_data.rename(columns={'Date': 'Date', 'Inflation Rate': 'Inflation Rate'}, inplace=True)

    # CPI Data
    cpi_data = get_cpi_data(News_sentiment_api_key, start_date='2017-08-17')
    cpi_data.rename(columns={'date': 'Date', 'cpi_value': 'CPI'}, inplace=True)

    # Fear and Greed Index Data
    fear_greed_data = get_combined_fear_greed_data()

    # **BigQuery Data**
    bigquery_data = fetch_bigquery_data()

    # Merge DataFrames
    combined_df = pd.merge(btc_full_data, full_order_flow_data, on='Date', how='outer')
    combined_df = pd.merge(combined_df, rsi_data, on='Date', how='outer')
    combined_df = pd.merge(combined_df, inflation_data, on='Date', how='outer')
    combined_df = pd.merge(combined_df, cpi_data, on='Date', how='outer')
    combined_df = pd.merge(combined_df, fear_greed_data[['Date', 'value', 'classification']], on='Date', how='outer')

    # **Merge BigQuery Data**: Integrate the new dataset with the combined DataFrame
    bigquery_data['Date'] = pd.to_datetime(bigquery_data['Date'])
    combined_df = pd.merge(combined_df, bigquery_data, on='Date', how='outer')

    # Sort by date to maintain consistency and order
    combined_df.sort_values('Date', inplace=True)

    # Filter data from August 17, 2017, onwards
    start_date = pd.to_datetime('2017-08-17')
    combined_df = combined_df[combined_df['Date'] >= start_date]

    # Fill missing values using forward fill and backward fill as needed
    combined_df.ffill(inplace=True)
    combined_df.bfill(inplace=True)

    print(combined_df.shape)
    print(combined_df.columns)
    return combined_df
