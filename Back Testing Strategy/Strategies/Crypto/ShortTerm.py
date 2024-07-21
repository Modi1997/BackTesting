from Live_Data.Retrieve_Data import *
from Indicators.Technical_Indicators import *

# Show All Columns
pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 2000)

# Daily BTC Data and Daily BTC Trend
btc_daily, daily_trend = Daily_Trend()
# Symbol, Timeframe and Depth to Get Data
coin_df = get_data('ETHUSDT', '1m', '200m')

# print(btc_daily.tail(5)) # BTC Daily Data
# print(daily_trend) # Daily BTC (Market) Trend (-5,5)
# print(coin_df) # DF for the selected symbol

#TODO BUILD A STRATEGY FOR 1/3m and 15m confirmation (1,2,3 steps for flipping Buy if Higher High and 50% drop of range and other way around for Sell)
# 1m timeframe 50 EMA - conditions on 15m and 1d
# uptrend daily EMA + Change positive then find a time to buy risk/reward 1/3