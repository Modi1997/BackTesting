from Live_Data.Retrieve_Data import *
from Indicators.Technical_Indicators import *

# Show All Columns
pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 2000)

# BTC Daily Data
btc_daily = get_data('BTCUSDT','1d', '100d').drop(columns='Date')

# Create Trend Features
# Get EMA
btc_daily['EMA'] = round(EMA(50, btc_daily['Close']), 2)
# Get EMA
btc_daily['RSI'] = round(RSI(btc_daily['Close']), 2)
# Get MACD Total
macd = MACD(btc_daily['Close'])
btc_daily['MACD'] = round(macd[-3], 2)
# Get STOCHASTIC_RSI
btc_daily = STOCHASTIC_RSI(btc_daily)


# Defining Daily BTC Trend (-5 Strong Sell, +5 Strong Buy)
trend = 0

# Buying Signal
if btc_daily['Change'].iloc[-1] > 0:
    trend += 1
    if btc_daily['EMA'].iloc[-1] < btc_daily['Close'].iloc[-1]:
        trend += 1
    if btc_daily['RSI'].iloc[-1] > btc_daily['RSI'].iloc[-2]:
        trend += 1
    if btc_daily['%K'].iloc[-1] > btc_daily['%D'].iloc[-1]:
        trend += 1
    if btc_daily['%K'].iloc[-1] < 50:
        trend += 1
# Selling Signal
elif btc_daily['Change'].iloc[-1] < 0:
    trend -= 1
    if btc_daily['EMA'].iloc[-1] > btc_daily['Close'].iloc[-1]:
        trend -= 1
    if btc_daily['RSI'].iloc[-1] < btc_daily['RSI'].iloc[-2]:
        trend -= 1
    if btc_daily['%K'].iloc[-1] < btc_daily['%D'].iloc[-1]:
        trend -= 1
    if btc_daily['%D'].iloc[-1] > 70:
        trend -= 1

coin_df = get_data('BTCUSDT', '1m', '200m')
coin_df['EMA'] = round(EMA(50, coin_df['Close']), 2)

print(btc_daily.tail(20))
print(trend)

#TODO`
# 1m timeframe 50 EMA - conditions on 15m and 1d
# uptrend daily EMA + Change positive then find a time to buy risk/reward 1/4