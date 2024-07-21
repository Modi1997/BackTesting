from Strategies.Strategy_Test import *

def trades_and_metrics(df, initial_capital=100):
    """
    This function gets the DF, other indicators or values and initial capital and returns performance metrics

    :param df: dataframe of the stock/crypto/commodity
    :param initial_capital: default = 100
    :return: metrics, trades, df
    """

    # Initialization of variables
    capital = initial_capital
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
    winning_trades = sum(1 for t in trades if t['Type'] == 'SELL' and t['Price'] > trades[trades.index(t) - 1]['Price'])
    losing_trades = (total_trades // 2) - winning_trades
    winning_percentage = (winning_trades / (total_trades // 2)) * 100 if total_trades > 0 else 0
    average_bars_held = len(df) / (total_trades // 2) if total_trades > 0 else 0
    total_trades = int(total_trades / 2)

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
        'Average Bars Held': average_bars_held
    }

    return metrics, trades, df