def strategy(df, capital, fees, fee_rate, trades, ema_period):
    """
    This is the buy and sell strategy function that needs to be called within the trades_and_matrics

    :return: 1. capital -> capital after trades
             2. fees -> total fees
             3. trades -> list of trades
             4. position -> 0 (not entered) or 1 (entered)
             5. entried -> Boolean
             6. df -> final DataFrame
    """

    # EMA
    df['EMA'] = df['Close'].ewm(span=ema_period, adjust=False).mean()
    # Signal: 1 Buy, -1 Sell, 0 Initialization
    df['Signal'] = 0

    # Initialisation of variables
    entried = False
    position = 0

    # Get in - Get out
    for i in range(1, len(df)):

        # Buy signal
        if not entried and df['Close'].iloc[i].item() > df['EMA'].iloc[i].item():
            entry_price = df['Close'].iloc[i]
            max_qty = capital / (entry_price * (1 + fee_rate))
            cost = entry_price * max_qty * (1 + fee_rate)
            capital -= cost
            fees += entry_price * max_qty * fee_rate
            position = max_qty
            entried = True
            trades.append({'Type': 'BUY', 'Price': entry_price, 'Index': df.index[i], 'Qty': max_qty})
            df.loc[df.index[i], 'Signal'] = 1


        # Sell signal
        elif entried and df['Close'].iloc[i].item() < df['EMA'].iloc[i].item():
            exit_price = df['Close'].iloc[i]
            sell_value = exit_price * position * (1 - fee_rate)
            capital += sell_value
            fees += exit_price * position * fee_rate
            trades.append({'Type': 'SELL', 'Price': exit_price, 'Index': df.index[i], 'Qty': position})
            position = 0
            entried = False
            df.loc[df.index[i], 'Signal'] = -1

    return capital, fees, trades, position, entried, df