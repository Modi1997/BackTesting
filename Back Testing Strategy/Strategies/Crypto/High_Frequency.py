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