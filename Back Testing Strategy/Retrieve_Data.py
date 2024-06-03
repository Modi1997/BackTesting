import yfinance as yf

def get_yahoo_data(symbol, start_date, end_date):
    """
    Get dataframe from Yahoo Finance API with given symbol and start date and end date

    :param symbol: symbol to get data from
    :param start_date: start date in a format of YYYY-MM-DD
    :param end_date: end date in a format of YYYY-MM-DD
    :return: df
    """
    return yf.download(symbol, start=start_date, end=end_date)