import pandas as pd
import yfinance as yf
import plotly.express as px
import plotly.graph_objects as go
import tkinter as tk
from tkinter import ttk

# Fetching data
def get_yahoo_data(symbol, start_date, end_date):
    return yf.download(symbol, start=start_date, end=end_date)

# Implementing the strategy
def simple_strategy(df, ema_period, initial_capital=10000, qty=1):
    df['EMA'] = df['Close'].ewm(span=ema_period, adjust=False).mean()
    df['Signal'] = 0  # 1 for buy, -1 for sell

    entried = False
    capital = initial_capital
    position = 0
    trades = []
    fees = 0
    fee_rate = 0.001  # Example fee rate

    for i in range(1, len(df)):
        if not entried and df['Close'].iloc[i] > df['EMA'].iloc[i]:
            # Buy signal
            entry_price = df['Close'].iloc[i]
            capital -= entry_price * qty * (1 + fee_rate)
            fees += entry_price * qty * fee_rate
            position = qty
            entried = True
            trades.append({'Type': 'BUY', 'Price': entry_price, 'Index': df.index[i]})
            df['Signal'].iloc[i] = 1
        elif entried and df['Close'].iloc[i] < df['EMA'].iloc[i]:
            # Sell signal
            exit_price = df['Close'].iloc[i]
            capital += exit_price * qty * (1 - fee_rate)
            fees += exit_price * qty * fee_rate
            position = 0
            entried = False
            trades.append({'Type': 'SELL', 'Price': exit_price, 'Index': df.index[i]})
            df['Signal'].iloc[i] = -1

    # Calculate metrics
    ending_capital = capital + position * df['Close'].iloc[-1]
    net_profit = ending_capital - initial_capital
    pnl_percentage = (net_profit / initial_capital) * 100
    total_trades = len(trades)
    winning_trades = sum(1 for t in trades if t['Type'] == 'SELL' and t['Price'] > trades[trades.index(t)-1]['Price'])
    losing_trades = total_trades // 2 - winning_trades
    winning_percentage = (winning_trades / (total_trades // 2)) * 100 if total_trades > 0 else 0
    average_bars_held = len(df) / (total_trades // 2) if total_trades > 0 else 0
    total_trades = int(total_trades/2)

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

# Fetch TSLA data
symbol = 'TSLA'
start_date = '2022-01-01'
end_date = '2023-01-01'
df = get_yahoo_data(symbol, start_date, end_date)

# Apply the strategy
ema_period = 50  # Example EMA period
metrics, trades, df = simple_strategy(df, ema_period)

# Visualization
fig = go.Figure()

# Add Close price trace
fig.add_trace(go.Scatter(x=df.index, y=df['Close'], mode='lines', name='Close Price'))

# Add EMA trace
fig.add_trace(go.Scatter(x=df.index, y=df['EMA'], mode='lines', name=f'EMA {ema_period}', line=dict(dash='dash')))

# Add Buy signals
buy_signals = df[df['Signal'] == 1]
fig.add_trace(go.Scatter(x=buy_signals.index, y=buy_signals['Close'], mode='markers', name='Buy Signal',
                         marker=dict(symbol='triangle-up', color='green', size=10)))

# Add Sell signals
sell_signals = df[df['Signal'] == -1]
fig.add_trace(go.Scatter(x=sell_signals.index, y=sell_signals['Close'], mode='markers', name='Sell Signal',
                         marker=dict(symbol='triangle-down', color='red', size=10)))

# Customize layout
fig.update_layout(title=f'{symbol} Price Chart with Buy/Sell Signals',
                  xaxis_title='Date',
                  yaxis_title='Price',
                  legend_title='Legend')

# Show interactive plot
fig.show()

# Display metrics and trades in a new window
# Display metrics and trades in a new window
# Display metrics and trades in a new window
def show_metrics_and_trades(metrics, trades):
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
    pnl_label = ttk.Label(returns_frame, text="{:.2f}%".format(metrics['Winning Trades %']))
    pnl_label.grid(row=5, column=1, sticky=tk.W)
    if metrics['Winning Trades %'] > 50:
        pnl_label.configure(foreground='green')
    elif metrics['Winning Trades %'] <= 50:
        pnl_label.configure(foreground='red')

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
            if return_percentage > 0:
                tree.tag_configure('winner', background='lightgreen')
                tree.item(tree.get_children()[-1], tags=('winner',))
                tree.item(tree.get_children()[-2], tags=('winner',))
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

# Show metrics and trades in a new window
show_metrics_and_trades(metrics, trades)