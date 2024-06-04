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



# secret key and api connection/pass provided by account on binance
api_key = 'siP2VBOq44rbgvHfnfWomRb4dcDY7QbVNwAxauetYXGsG9rqCg7YODo3Cn5I57KS'
api_secret = 'fwgN7NuEXn8hgpBkjVsGs8sYCyqcWRWFv1OkC7jqAepQLLJ5Tehs3vKmifHD7jaS'

# client request
client = Client(api_key, api_secret)
# client account all info
client_account = client.get_account()
# client_keys of the dictionary
client_keys = client.get_account().keys()
# get only the cryptocurrency assets
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

    # creating a df with the client.get_historical_klines() binance function
    frame = pd.DataFrame(client.get_historical_klines(symbol, interval, lookback+' min ago GMT'))
    # get only the 6 first columns from the client.get_historical_klines()
    frame = frame.iloc[:,:6]
    # name these columns as their headers are just numbers
    frame.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
    frame['Date'] = frame['Time']

    # set index to time (ms) and convert type to float
    frame = frame.set_index('Time')
    frame.index = pd.to_datetime(frame.index, unit='ms')
    frame = frame.astype(float)

    return frame