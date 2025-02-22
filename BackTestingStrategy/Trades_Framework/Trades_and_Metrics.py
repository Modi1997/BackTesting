from BackTestingStrategy.Strategies.Strategy_Test import *
def trades_and_metrics(df, initial_capital=100):
    """
    This function gets the DF, other indicators or values and initial capital and returns performance metrics

    :param df: dataframe of the stock/crypto/commodity
    :param initial_capital: default = 100
    :return: metrics, trades, df
    """

    # Initialization of variables
    capital = initial_capital
    returns = []
    trades = []
    fees = 0
    fee_rate = 0.01

    # Call the strategy
    capital, fees, trades, position, entried, df = strategy(df, capital, fees, fee_rate, trades, 100)

    # Metrics calculations
    ending_capital = capital + position * df['Close'].iloc[-1]
    net_profit = ending_capital - initial_capital
    pnl_percentage = (net_profit / initial_capital) * 100
    total_trades = len(trades)
    # Fix by ensuring 'Price' comparison is done on scalar values
    winning_trades = sum(
        1 for i, t in enumerate(trades)
        if t['Type'] == 'SELL' and i > 0 and t['Price'].item() > trades[i - 1]['Price'].item()
    )
    losing_trades = (total_trades // 2) - winning_trades
    winning_percentage = (winning_trades / (total_trades // 2)) * 100 if total_trades > 0 else 0
    average_bars_held = len(df) / (total_trades // 2) if total_trades > 0 else 0
    total_trades = int(total_trades / 2)

    for i in range(1, len(trades), 2):
        entry_trade = trades[i - 1]
        exit_trade = trades[i]
        if entry_trade['Type'] == 'BUY' and exit_trade['Type'] == 'SELL':
            return_percentage = ((exit_trade['Price'] - entry_trade['Price']) / entry_trade['Price']) * 100
            returns.append(return_percentage.item() if hasattr(return_percentage, "item") else return_percentage)

    highest_return = max(returns) if returns else 0
    lowest_return = min(returns) if returns else 0

    # Metrics to display on the Framework
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
        'Average Bars Held': average_bars_held,
        'Highest Return %': highest_return,
        'Lowest Return %': lowest_return
    }

    return metrics, trades, df