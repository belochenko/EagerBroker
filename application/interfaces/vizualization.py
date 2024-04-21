from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import random

app = Dash(__name__)

app.layout = html.Div([
    html.H4('Real-Time Candlestick Charts for Stock Symbols'),
    dcc.Graph(id="candlestick_amzn"),
    dcc.Graph(id="candlestick_aapl"),
    html.Div(id="alerts"),
    dcc.Interval(
        id='interval',
        interval=60000,  # Interval in milliseconds (update every second)
        n_intervals=0
    )
])

@app.callback(
    Output("candlestick_amzn", "figure"),
    Output("candlestick_aapl", "figure"),
    Output("alerts", "children"),
    Input("interval", "n_intervals"))
def update_candlestick_charts(n):
    # Retrieve real-time data from StockExchange instances
    data_amzn = fetch_real_time_data("AMZN")
    data_aapl = fetch_real_time_data("AAPL")

    # Create candlestick charts for both stock symbols
    fig_amzn = create_candlestick_chart(data_amzn, "Amazon (AMZN)")
    fig_aapl = create_candlestick_chart(data_aapl, "Apple (AAPL)")

    # Check for buy/sell signals and generate alerts
    alerts = generate_alerts(data_amzn, data_aapl)

    return fig_amzn, fig_aapl, alerts

def fetch_real_time_data(stock_exchange):
     if not stock_exchange.data_queue.empty():
         data = stock_exchange.data_queue.get()
         symbol = data.symbol
         share_price = data['share_price']

def create_candlestick_chart(data, title):
    fig = go.Figure(data=[go.Candlestick(x=[x[0] for x in data],
                                         open=[x[1] for x in data],
                                         high=[x[2] for x in data],
                                         low=[x[3] for x in data],
                                         close=[x[4] for x in data])])
    fig.update_layout(title=title)
    return fig

def generate_alerts(data_amzn, data_aapl):
    # Replace with logic to generate buy/sell alerts based on data
    # For demonstration, generate random alerts
    alerts = []
    if random.random() < 0.5:
        alerts.append(html.Div("Buy signal for Amazon (AMZN)", style={"color": "green"}))
    if random.random() < 0.5:
        alerts.append(html.Div("Sell signal for Apple (AAPL)", style={"color": "red"}))
    return alerts
