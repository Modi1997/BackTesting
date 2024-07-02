import pandas as pd
import yfinance as yf
from binance import Client

def get_yahoo_data(symbol, start_date, end_date, interval):
    """
    Get dataframe from Yahoo Finance API with given symbol and start date and end date

    :param symbol: symbol to get data from
    :param start_date: start date in a format of YYYY-MM-DD
    :param end_date: end date in a format of YYYY-MM-DD
    :param interval: interval either 1d or 1wk
    :return: df
    """

    return yf.download(symbol, start=start_date, end=end_date, interval=interval)



# API Key & Secret
api_key = 'siP2VBOq44rbgvHfnfWomRb4dcDY7QbVNwAxauetYXGsG9rqCg7YODo3Cn5I57KS'
api_secret = 'fwgN7NuEXn8hgpBkjVsGs8sYCyqcWRWFv1OkC7jqAepQLLJ5Tehs3vKmifHD7jaS'

# Client Request
client = Client(api_key, api_secret)
# Account Info
client_account = client.get_account()
# Keys of Client Dictionary
client_keys = client.get_account().keys()
# Get Holdings
account_info = client_account["balances"]

def get_data(symbol, interval, lookback):
    """
    This function takes a symbol, an interval, and lookback and returns
    a dataframe with the ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
    for the given symbol within the lookback timeframe
    (rows of data = interval / lookback)

    :param symbol: pair symbol such as BTCUSDT
    :param interval: bar or time interval (seconds, minutes or hours)
    :param lookback: seconds, minutes or hours of data to look back
    :return: dataframe
    """

    # Create a DF with the client.get_historical_klines() binance function
    frame = pd.DataFrame(client.get_historical_klines(symbol, interval, lookback+' min ago GMT'))
    # Get Only First 6 Columns from client.get_historical_klines()
    frame = frame.iloc[:,:6]

    # Rename Columns
    frame.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
    # Create Date Column
    frame['Date'] = frame['Time']

    # Set index to Time (ms) and convert type to float
    frame = frame.set_index('Time')
    frame.index = pd.to_datetime(frame.index, unit='ms')
    frame = frame.astype(float)

    # Creating % Change Column
    frame['Change'] = round(frame['Close'].pct_change() * 100, 2)
    # Rounding Volume to 2 Decimals
    frame['Volume'] = round(frame['Volume'], 2)

    return frame