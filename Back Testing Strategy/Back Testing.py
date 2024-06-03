import pandas as pd
import plotly.graph_objects as go
import tkinter as tk
from tkinter import ttk

from Retrieve_Data import *
from Strategy import *
from Chart_Signals import *

# Symbol to fetch data
symbol = 'AAPL'
# Start Date of data retrieval
start_date = '2020-01-01'
# End Date of data retrieval
end_date = '2024-06-01'

# Fetch data
df = get_yahoo_data(symbol, start_date, end_date)

# Apply EMA strategy
ema_period = 200
metrics, trades, df = ema_strategy(df, ema_period)

# Chart signal analysis
plot_trading_signals(df, ema_period, symbol)


# Metrics Framework
def show_metrics_and_trades(metrics, trades):
    """
    A function that opens a new window with the investment return metrics and all the taken trades of the strategy

    :param metrics: various metrics to display
    :param trades: all trades taken based on the given strategy
    :return metrics and trades:
        1. A new window with the statistics and the trades based on the strategy
        2. A new browser window with the chart and the past/current signals
    """

    root = tk.Tk()
    root.title("Backtesting Results")

    frame = ttk.Frame(root, padding="10")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    # ******** Strategy Return Details **********
    returns_frame = ttk.LabelFrame(frame, text="Returns & Trades", padding="15")
    returns_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)

    ttk.Label(returns_frame, text="Initial Capital: ", font="Helvetica 10 bold").grid(row=0, column=0, sticky=tk.W)
    ttk.Label(returns_frame, text="${:.2f}".format(metrics['Initial Capital'])).grid(row=0, column=1, sticky=tk.W)

    ttk.Label(returns_frame, text="Ending Capital: ", font="Helvetica 10 bold").grid(row=1, column=0, sticky=tk.W)
    ttk.Label(returns_frame, text="${:.2f}".format(metrics['Ending Capital'])).grid(row=1, column=1, sticky=tk.W)

    ttk.Label(returns_frame, text="Net Profit: ", font="Helvetica 10 bold").grid(row=2, column=0, sticky=tk.W)
    net_profit_label = ttk.Label(returns_frame, text="${:.2f}".format(metrics['Net Profit']))
    net_profit_label.grid(row=2, column=1, sticky=tk.W)
    if metrics['Net Profit'] > 0:
        net_profit_label.configure(foreground='green')
    elif metrics['Net Profit'] < 0:
        net_profit_label.configure(foreground='red')

    ttk.Label(returns_frame, text="PnL %: ", font="Helvetica 10 bold").grid(row=3, column=0, sticky=tk.W)
    pnl_label = ttk.Label(returns_frame, text="{:.2f}%".format(metrics['PnL %']))
    pnl_label.grid(row=3, column=1, sticky=tk.W)
    if metrics['PnL %'] > 0:
        pnl_label.configure(foreground='green')
    elif metrics['PnL %'] < 0:
        pnl_label.configure(foreground='red')

    ttk.Label(returns_frame, text="Total Transactions Costs (Fees): ", font="Helvetica 10 bold").grid(row=4, column=0, sticky=tk.W)
    ttk.Label(returns_frame, text="${:.2f}".format(metrics['Total Transactions Costs (Fees)'])).grid(row=4, column=1, sticky=tk.W)

    ttk.Label(returns_frame, text="Winning Trades %: ", font="Helvetica 10 bold").grid(row=5, column=0, sticky=tk.W)
    winning_trades = ttk.Label(returns_frame, text="{:.2f}%".format(metrics['Winning Trades %']))
    winning_trades.grid(row=5, column=1, sticky=tk.W)
    if metrics['Winning Trades %'] > 50:
        winning_trades.configure(foreground='green')
    elif metrics['Winning Trades %'] <= 50:
        winning_trades.configure(foreground='red')

    ttk.Label(returns_frame, text=f"Total Trades: ", font="Helvetica 10 bold").grid(row=6, column=0, sticky=tk.W)
    ttk.Label(returns_frame, text=metrics['Total Trades']).grid(row=6, column=1, sticky=tk.W)

    ttk.Label(returns_frame, text=f"Number of Winners: ", font="Helvetica 10 bold").grid(row=7, column=0, sticky=tk.W)
    ttk.Label(returns_frame, text=metrics['Number of Winners']).grid(row=7, column=1, sticky=tk.W)

    ttk.Label(returns_frame, text=f"Number of Losers: ", font="Helvetica 10 bold").grid(row=8, column=0, sticky=tk.W)
    ttk.Label(returns_frame, text=metrics['Number of Losers']).grid(row=8, column=1, sticky=tk.W)

    ttk.Label(returns_frame, text=f"Average Bars Held: ", font="Helvetica 10 bold").grid(row=9, column=0, sticky=tk.W)
    ttk.Label(returns_frame, text=int(metrics['Average Bars Held'])).grid(row=9, column=1, sticky=tk.W)

    # ********** All Trades section **********
    trades_frame = ttk.LabelFrame(frame, text="All Trades", padding="10")
    trades_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)

    # Columns in the trading data rows
    cols = ('Type', 'Price', 'Date', 'Return %')
    tree = ttk.Treeview(trades_frame, columns=cols, show='headings')
    tree.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))

    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, minwidth=0, width=100)

    for i, trade in enumerate(trades):
        if trade['Type'] == 'SELL':
            buy_trade = trades[i-1]
            return_percentage = ((trade['Price'] - buy_trade['Price']) / buy_trade['Price']) * 100
            tree.insert("", "end", values=(trade['Type'], f"${trade['Price']:.2f}", trade['Index'].strftime('%Y-%m-%d'), f"{return_percentage:.2f}%"))

            # Dynamic colouring of the trading data rows
            # Winner Green
            if return_percentage > 0:
                tree.tag_configure('winner', background='lightgreen')
                tree.item(tree.get_children()[-1], tags=('winner',))
                tree.item(tree.get_children()[-2], tags=('winner',))
            # Loser Red
            else:
                tree.tag_configure('loser', background='lightcoral')
                tree.item(tree.get_children()[-1], tags=('loser',))
                tree.item(tree.get_children()[-2], tags=('loser',))
        else:
            tree.insert("", "end", values=(trade['Type'], f"${trade['Price']:.2f}", trade['Index'].strftime('%Y-%m-%d'), ''))

    # Configure grid layout
    for i in range(6):
        trades_frame.rowconfigure(i, weight=1)
    trades_frame.columnconfigure(0, weight=1)

    root.mainloop()

# Show metrics and all trades
show_metrics_and_trades(metrics, trades)