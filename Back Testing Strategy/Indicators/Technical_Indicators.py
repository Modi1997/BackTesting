import talib
import pandas as pd
from typing import Tuple
from pandas import DataFrame
from Live_Data.Retrieve_Data import *


def frame(symbol, interval, lookback):
    """
    This function takes a symbol, an interval, and lookback,
    creates a frame (df) and returns the close value that can be used

    :param symbol: pair symbol such as BTCUSDT
    :param interval: bar or time interval (seconds, minutes or hours)
    :param lookback: seconds, minutes or hours of data to look back
    :return: close price only of the dataframe
    """

    # creating a df with the client.get_historical_klines() binance function
    frame = pd.DataFrame(client.get_historical_klines(symbol, interval, lookback + ' min ago GMT'))
    # get only the 6 first columns from the client.get_historical_klines()
    frame = frame.iloc[:, :5]
    # name these columns as their headers are just numbers
    frame.columns = ['Time', 'Open', 'High', 'Low', 'Close']

    # set index to time (ms) and convert type to float
    frame = frame.set_index('Time')
    frame.index = pd.to_datetime(frame.index, unit='ms')
    frame = frame.astype(float)
    # return only the close (plus the index)
    close = frame['Close']

    return close


def RSI(close: object) -> pd.DataFrame:
    """
    This function is creating a technical indicator called RSI (Related Strength Index) and indicates whether the
    asset is over bought or over sold. The 14 first values are NaN as it needs at least 14 values to read. The last 3
    indexes are the most important in order to determine whether there is a turn around or continuation of the trend.

    :param close: input close column
    :return: dataframe with datetime and RSI index (value range: 0,100)
    """

    rsi = talib.RSI(close)
    return rsi


def EMA(ema_period: int, close: object) -> pd.DataFrame:
    """
    This function is creating a technical indicator called EMA (Exponential Moving Average) and indicates whether the
    asset is on an uptrend or downtrend. The 30 first values are NaN as it needs at least 14 values to read. As long
    as the actual value is above the EMA then we have an uptrend and respectively below, then a downtrend.

    :param ema_period: length of EMA
    :param close: input close column
    :return: dataframe with datetime and EMA value
    """

    ema = close.ewm(span=ema_period, adjust=False).mean()
    return ema


def MACD(close: object) -> pd.DataFrame:
    """
    This function is creating a technical indicator called MACD (Moving Average Convergence/Divergence) and indicates
    where the cross-over of the trend happens (turn around). The first 33 values are NaN as this technical indicator
    needs data from at least 33 points. Please note that it provides 3 arrays:
        . 1 for the buy
        . 2 for the sell
        . 3 difference between buy-sell.
    The cross-over happens when the 2nd value from the MACD_total is negative
    and the latest one becomes positive

    :param close: input close column
    :return: dataframe with datetime and MACD
    """

    macd = talib.MACD(close)
    return macd


def STOCHASTIC_RSI(df: pd.DataFrame, rsi_col: str = 'RSI') -> pd.DataFrame:
    """
    Calculate the Stochastic RSI for a given DataFrame containing RSI values.

    :param df: DataFrame containing 'RSI' values.
    :param rsi_col: Column name of the RSI values in the DataFrame.
    :return: DataFrame with Stochastic RSI (%K and %D) added.
    """

    # Parameters
    stochastic_length = 14
    k_period = 3
    d_period = 3

    # Calculate StochRSI
    df['Lowest_RSI'] = df[rsi_col].rolling(window=stochastic_length).min()
    df['Highest_RSI'] = df[rsi_col].rolling(window=stochastic_length).max()
    df['StochRSI'] = (df[rsi_col] - df['Lowest_RSI']) / (df['Highest_RSI'] - df['Lowest_RSI'])

    # Calculate %K
    df['%K'] = df['StochRSI'].rolling(window=k_period).mean()
    # Calculate %D
    df['%D'] = df['%K'].rolling(window=d_period).mean()

    # Drop intermediate columns and NaN values for clean output
    df.drop(columns=['Lowest_RSI', 'Highest_RSI', 'StochRSI'], inplace=True)
    df.dropna(inplace=True)

    return df


def get_data(symbol: str, interval: str, lookback: str) -> pd.DataFrame:
    """
    This function gets the raw data from the get_data function and adds the technical indicators as new features

    :param symbol: cryptocurrency pair
    :param interval: timeframe of the chart
    :param lookback: data depth
    :return: DataFrame with indicators EMA, RSI and MACD
    """

    # Retrieve Data
    df = data(symbol, interval, lookback).drop(columns='Date')

    # Get EMA
    df['EMA'] = round(EMA(50, df['Close']), 2)
    # Get RSI
    df['RSI'] = round(RSI(df['Close']), 2)
    # Get MACD Total
    macd = MACD(df['Close'])
    df['MACD'] = round(macd[-3], 2)
    # Get STOCHASTIC_RSI
    df = STOCHASTIC_RSI(df)

    return df


def Daily_Trend(Change: str = 'Change', Close: str = 'Close',
                RSI: str = 'RSI', EMA: str = 'EMA',
                K: str = '%K', D: str = '%D') -> tuple[DataFrame, int]:
    """
    Gets a dataframe with the required parameters as existing columns and returns the trend of the day
    (+5 Strong Buy to -5 Strong Sell)

    :param df: DataFrame of the asset
    :param Change: Daily % Change
    :param Close: Actual Close Price
    :param RSI: Relative Strength Index
    :param EMA: Exponential Moving Average
    :param K: Current Price of the Security in % of the difference between highest and lowest point over selected time
    :param D: 3-day average of the K
    :return: BTC DataFrame with the K & D
    :return: Trend in a range of (-5,5)
    """

    btc_daily = get_data('BTCUSDT', '1d', '100d')

    # Defining Daily BTC Trend (-5 Strong Sell, +5 Strong Buy, if 0 then it is Neutral)
    trend = 0

    # Buying Signal
    if btc_daily[Change].iloc[-1] > (0.3):
        trend += 1
        if btc_daily[EMA].iloc[-1] < btc_daily[Close].iloc[-1]:
            trend += 1
        if btc_daily[RSI].iloc[-1] > btc_daily[RSI].iloc[-2]:
            trend += 1
        if btc_daily[K].iloc[-1] > btc_daily[D].iloc[-1]:
            trend += 1
        if btc_daily[K].iloc[-1] < 50:
            trend += 1

    # Selling Signal
    elif btc_daily[Change].iloc[-1] < (-0.5):
        trend -= 1
        if btc_daily[EMA].iloc[-1] > btc_daily[Close].iloc[-1]:
            trend -= 1
        if btc_daily[RSI].iloc[-1] < btc_daily[RSI].iloc[-2]:
            trend -= 1
        if btc_daily[K].iloc[-1] < btc_daily[D].iloc[-1]:
            trend -= 1
        if btc_daily[D].iloc[-1] > 70:
            trend -= 1

    return btc_daily, trend