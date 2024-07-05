from Live_Data.Retrieve_Data import *
from Indicators.Technical_Indicators import *

# Show All Columns
pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 2000)

# Retrieve Data
coin_df = get_data('BTCUSDT','1d', '22500d').drop(columns='Date')

# Create Trend Features
# coin_df['Change'] = round(coin_df['Close'].pct_change() * 100, 2)
coin_df['EMA'] = round(EMA(50, coin_df['Close']), 2)

print(coin_df)

#TODO
# 1m timeframe 50 EMA - conditions on 15m and 1d
# uptrend daily EMA + Change positive then find a time to buy risk/reward 1/4
# downtrend -//- -//- -//-   negative -//- sell -//- -//- -//-
# maybe condition on % Change e.g. if +3% BTC then easier long on alts