import config
import pandas as pd
from binance import Client

client = Client(config.API_KEY, config.API_SECRET)

# Function to convert Binance API candlestick format to OHLC format
def convert_candlestick_format(candlestick):
    # Extract relevant data
    open_time, open, high, low, close, volume, close_time, _, _, _, _, _ = candlestick

    # Convert timestamps to human-readable format if needed
    # You can use pandas to_datetime or any other method for this

    # Return OHLC data as a list
    return [open_time, float(open), float(high), float(low), float(close), float(volume), close_time]

def collect_and_save_candle_data(symbol, interval, start_date, end_date, filename):
    # Get historical candlestick data
    candlesticks = client.get_historical_klines(symbol, interval, start_date, end_date)

    # Convert candlestick data to a DataFrame
    df = pd.DataFrame([convert_candlestick_format(candlestick) for candlestick in candlesticks],
                      columns=['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time'])

    # Convert timestamp columns to datetime
    df['Open Time'] = pd.to_datetime(df['Open Time'], unit='ms')
    df['Close Time'] = pd.to_datetime(df['Close Time'], unit='ms')

    # Set 'Open Time' as the DataFrame index
    df.set_index('Open Time', inplace=True)

    # Save the DataFrame to a new CSV file
    df.to_csv(filename)

# Example usage
symbol = 'BTCUSDT'
interval = Client.KLINE_INTERVAL_4HOUR
start_date = '2024-01-10'
end_date = '2024-01-19'
filename = 'btcusdt_4h_candles_2024-01-10_2024-01-19.csv'

# Call the function to collect and save candle data
collect_and_save_candle_data(symbol, interval, start_date, end_date, filename)
