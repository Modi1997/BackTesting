import plotly.graph_objects as go

def plot_trading_signals(df, symbol, ema_period=100):
    """
    This function opens a new window on a browser and displays the chart based on the selected symbol and timeframe.
    It also shows the buy and sell signals based on the strategy

    :param df: df of the symbol
    :param ema_period: integer for the EMA to define uptrend or downtrend
    :param symbol: selected symbol
    :return: interactive visualization
    """

    # Create a new figure
    fig = go.Figure()

    # Add candlestick chart
    fig.add_trace(go.Candlestick(x=df.index,
                                 open=df['Open'],
                                 high=df['High'],
                                 low=df['Low'],
                                 close=df['Close'],
                                 increasing_line_color='green',
                                 decreasing_line_color='purple',
                                 name='Market Data'))

    # Add EMA trace
    fig.add_trace(go.Scatter(x=df.index, y=df['EMA'],
                             mode='lines',
                             name=f'EMA {ema_period}',
                             line=dict(dash='dash', color='blue')))

    # Add Buy signals
    buy_signals = df[df['Signal'] == 1]
    fig.add_trace(go.Scatter(x=buy_signals.index, y=buy_signals['Close'] * 0.95,
                             mode='markers',
                             name='Buy Signal',
                             marker=dict(symbol='triangle-up', color='green', size=12)))

    # Add Sell signals
    sell_signals = df[df['Signal'] == -1]
    fig.add_trace(go.Scatter(x=sell_signals.index, y=sell_signals['Close'] * 1.05,
                             mode='markers',
                             name='Sell Signal',
                             marker=dict(symbol='triangle-down', color='red', size=12)))

    # Customize layout
    fig.update_layout(
        title=f'{symbol} Price Chart with Signals',
        xaxis_title='Date',
        yaxis_title='Price',
        legend_title='Legend',
        plot_bgcolor='rgba(255, 255, 227, 0.9)',  # white background
        xaxis_rangeslider_visible=False  # Hide the range slider
    )

    # Show the figure
    fig.show()