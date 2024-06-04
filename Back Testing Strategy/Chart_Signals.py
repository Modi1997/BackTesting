import plotly.graph_objects as go

def plot_trading_signals(df, ema_period, symbol):
    """
    This function opens a new window on a browser and displays the chart based on the selected symbol and timeframe.
    It also shows the buy and sell signals based on the strategy

    :param df: df of the symbol
    :param ema_period: integer for the EMA to define uptrend or downtrend
    :param symbol: selected symbol
    :return: interactive visualization
    """

    #TODO: Make the chart better (preferably with bar chart green/red)

    # Create a new figure
    fig = go.Figure()

    # Add Close price trace
    fig.add_trace(go.Scatter(x=df.index, y=df['Close'],
                             mode='lines',
                             name='Close Price'))

    # Add EMA trace
    fig.add_trace(go.Scatter(x=df.index, y=df['EMA'],
                             mode='lines',
                             name=f'EMA {ema_period}', line=dict(dash='dash')))

    # Add Buy signals
    buy_signals = df[df['Signal'] == 1]
    fig.add_trace(go.Scatter(x=buy_signals.index, y=buy_signals['Close'],
                             mode='markers',
                             name='Buy Signal',
                             marker=dict(symbol='triangle-up', color='green', size=10)))

    # Add Sell signals
    sell_signals = df[df['Signal'] == -1]
    fig.add_trace(go.Scatter(x=sell_signals.index, y=sell_signals['Close'],
                             mode='markers',
                             name='Sell Signal',
                             marker=dict(symbol='triangle-down', color='red', size=10)))

    # Customize layout
    fig.update_layout(title=f'{symbol} Price Chart with Buy/Sell Signals',
                      xaxis_title='Date',
                      yaxis_title='Price',
                      legend_title='Legend')

    # Show the figure
    fig.show()