def ema_strategy(df, ema_period, initial_capital=100):
    """
    This function gets the DF, other indicators or values and initial capital and returns performance metrics

    :param df: dataframe of the stock/crypto/commodity
    :param ema_period: indicator
    :param initial_capital: default = 100
    :return: metrics, trades, df
    """

    # EMA
    df['EMA'] = df['Close'].ewm(span=ema_period, adjust=False).mean()
    # Signal: 1 Buy, -1 Sell
    df['Signal'] = 0

    # Initialization of variables
    entried = False
    capital = initial_capital
    position = 0
    trades = []
    fees = 0
    fee_rate = 0.01

    # Get in - Get out
    for i in range(1, len(df)):

        # Buy signal
        if not entried and df['Close'].iloc[i] > df['EMA'].iloc[i]:
            entry_price = df['Close'].iloc[i]
            max_qty = capital / (entry_price * (1 + fee_rate))
            cost = entry_price * max_qty * (1 + fee_rate)
            capital -= cost
            fees += entry_price * max_qty * fee_rate
            position = max_qty
            entried = True
            trades.append({'Type': 'BUY', 'Price': entry_price, 'Index': df.index[i], 'Qty': max_qty})
            df['Signal'].iloc[i] = 1

        # Sell signal
        elif entried and df['Close'].iloc[i] < df['EMA'].iloc[i]:

            exit_price = df['Close'].iloc[i]
            sell_value = exit_price * position * (1 - fee_rate)
            capital += sell_value
            fees += exit_price * position * fee_rate
            trades.append({'Type': 'SELL', 'Price': exit_price, 'Index': df.index[i], 'Qty': position})
            position = 0
            entried = False
            df['Signal'].iloc[i] = -1

    # Metrics calculations
    ending_capital = capital + position * df['Close'].iloc[-1]
    net_profit = ending_capital - initial_capital
    pnl_percentage = (net_profit / initial_capital) * 100
    total_trades = len(trades)
    winning_trades = sum(1 for t in trades if t['Type'] == 'SELL' and t['Price'] > trades[trades.index(t)-1]['Price'])
    losing_trades = (total_trades // 2) - winning_trades
    winning_percentage = (winning_trades / (total_trades // 2)) * 100 if total_trades > 0 else 0
    average_bars_held = len(df) / (total_trades // 2) if total_trades > 0 else 0
    total_trades = int(total_trades / 2)

    metrics = {
        'Initial Capital': initial_capital,
        'Ending Capital': ending_capital,
        'Net Profit': net_profit,
        'PnL %': pnl_percentage,
        'Total Transactions Costs (Fees)': fees,
        'Total Trades': total_trades,
        'Winning Trades %': winning_percentage,
        'Number of Winners': winning_trades,
        'Number of Losers': losing_trades,
        'Average Bars Held': average_bars_held
    }

    return metrics, trades, df
