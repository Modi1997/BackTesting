import plotly.graph_objects as go
from plotly.subplots import make_subplots

def plot_trading_signals(df, symbol, ema_period=100):
    """
    This function opens a new window on a browser and displays the chart based on the selected symbol and timeframe.
    It also shows the buy and sell signals based on the strategy.

    :param df: df of the symbol
    :param ema_period: integer for the EMA to define uptrend or downtrend
    :param symbol: selected symbol
    :return: interactive visualization
    """

    # This gets the symbol name (str) in MultiIndex
    ticker = df.columns.levels[1][0]

    # Create a new figure with two subplots: one for the price chart and one for the change
    fig = make_subplots(rows=2, cols=1,
                        row_heights=[0.8, 0.2],  # Define the height ratio of the two rows
                        shared_xaxes=True,
                        vertical_spacing=0.1,  # Space between the two plots
                        subplot_titles=(f'{symbol} Price Chart with Signals', 'Percentage Change'))

    # Add candlestick chart
    fig.add_trace(go.Candlestick(x=df.index,
                                 open=df[('Open', ticker)],
                                 high=df[('High', ticker)],
                                 low=df[('Low', ticker)],
                                 close=df[('Close', ticker)],
                                 increasing_line_color='green',
                                 decreasing_line_color='red',
                                 name='Market Data'),
                  row=1, col=1)

    # Add EMA trace
    fig.add_trace(go.Scatter(x=df.index, y=df[('EMA', '')],
                             mode='lines',
                             name=f'EMA {ema_period}',
                             line=dict(dash='dash', color='grey')),
                  row=1, col=1)

    # Add Buy signals
    buy_signals = df[df[('Signal', '')] == 1]
    if not buy_signals.empty:
        fig.add_trace(go.Scatter(x=buy_signals.index, y=buy_signals[('Close', ticker)] * 0.94,
                                 mode='markers',
                                 name='Buy Signal',
                                 marker=dict(symbol='triangle-up', color='blue', size=14)),
                      row=1, col=1)

    # Add Sell signals
    sell_signals = df[df[('Signal', '')] == -1]
    if not sell_signals.empty:
        fig.add_trace(go.Scatter(x=sell_signals.index, y=sell_signals[('Close', ticker)] * 1.06,
                                 mode='markers',
                                 name='Sell Signal',
                                 marker=dict(symbol='triangle-down', color='black', size=14)),
                      row=1, col=1)

    # Add change trace with conditional coloring
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df[('Change', '')],
        mode='lines+markers',
        name='Percentage Change',
        line=dict(color='orange'),
        marker=dict(
            color=df[('Change', '')].apply(lambda x: 'red' if x > 7 else ('green' if x < -7 else 'orange')),
            size=8
        )
    ), row=2, col=1)

    shapes = [
        dict(
            type='line',
            yref='y2',
            y0=0,
            y1=0,
            xref='x',
            x0=df.index.min(),
            x1=df.index.max(),
            line=dict(
                color='blue',
                width=1,
                dash='solid'
            )
        ),
        dict(
            type='line',
            xref='x',
            x0=df.index.min(),
            x1=df.index.max(),
            yref='paper',
            y0=0.17,
            y1=0.17,
            line=dict(
                color='black',
                width=2
            )
        )
    ]

    if (df[('Change', '')] > 7).any():
        shapes.append(
            dict(
                type='line',
                yref='y2',
                y0=7,
                y1=7,
                xref='x',
                x0=df.index.min(),
                x1=df.index.max(),
                line=dict(
                    color='red',
                    width=1,
                    dash='dot'
                )
            )
        )

    if (df[('Change', '')] < -7).any():
        shapes.append(
            dict(
                type='line',
                yref='y2',
                y0=-7,
                y1=-7,
                xref='x',
                x0=df.index.min(),
                x1=df.index.max(),
                line=dict(
                    color='green',
                    width=1,
                    dash='dot'
                )
            )
        )

    # Update layout with shapes
    fig.update_layout(
        shapes=shapes
    )

    # Customize layout
    fig.update_layout(
        title=f'{symbol} Price Chart with Signals and Percentage Change',
        xaxis_title='Date',
        yaxis_title='Price',
        yaxis2_title='Change (%)',
        legend_title='Legend',
        plot_bgcolor='rgba(255,255,255, 0.9)',  # white background
        xaxis_rangeslider_visible=False,  # Hide the range slider
        showlegend=True
    )

    # Show the figure
    fig.show()