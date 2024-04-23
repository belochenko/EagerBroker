import threading, time
from core.dto.eager_broker import EagerBrokerDecisionDTO
from core.dto.stock_exchange import BroadcastingSharePriceDTO, StockExchangeEmitTypeDTO
import dash
import dash_core_components as dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from datetime import datetime

from core.setup import common_queue

# Initialize empty dataframes to store the data
amazon_stock_exchange_df = pd.DataFrame(columns=['time_of_emission', 'total_shares_bought', 'total_shares_sold'])
apple_stock_exchange_df = pd.DataFrame(columns=['time_of_emission', 'total_shares_bought', 'total_shares_sold'])
amazon_broadcasting_share_price_df = pd.DataFrame(columns=['time_of_broadcasting', 'share_price'])
apple_broadcasting_share_price_df = pd.DataFrame(columns=['time_of_broadcasting', 'share_price'])
amazon_eager_broker_decision_df = pd.DataFrame(columns=['time_of_decision', 'share_price', 'decision'])
apple_eager_broker_decision_df = pd.DataFrame(columns=['time_of_decision', 'share_price', 'decision'])

# Create the Dash app
app = dash.Dash(__name__)

# Create the layout
app.layout = html.Div([
    html.H1('Stock Exchange Dashboard'),
    html.Div([
        html.H2('Amazon'),
        dcc.Graph(id='amazon-share-price-chart'),
        html.Div(id='amazon-alerts', style={'border': '1px solid black', 'padding': '10px'})
    ]),
    html.Div([
        html.H2('Apple'),
        dcc.Graph(id='apple-share-price-chart'),
        html.Div(id='apple-alerts', style={'border': '1px solid black', 'padding': '10px'})
    ]),
    dcc.Interval(id='interval-component', interval=1000, n_intervals=0)  # update every second
])

# Callback to update the Amazon share price chart
@app.callback(
    Output('amazon-share-price-chart', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_amazon_share_price_chart(n):
    global amazon_broadcasting_share_price_df, amazon_eager_broker_decision_df
    
    fig = go.Figure(data=[go.Scatter(x=amazon_broadcasting_share_price_df['time_of_broadcasting'], y=amazon_broadcasting_share_price_df['share_price'])])
    fig.update_layout(title='Amazon Share Price', xaxis_title='Time', yaxis_title='Share Price')
    
    # Add markers for decision points
    decision_points = amazon_eager_broker_decision_df[amazon_eager_broker_decision_df['decision'] != 'DecisionType.HOLD']
    fig.add_trace(go.Scatter(x=decision_points['time_of_decision'], y=decision_points['share_price'], mode='markers', marker=dict(size=10, color=decision_points['decision'].map({'DecisionType.BUY': 'green', 'DecisionType.SELL': 'red'}))))
    
    return fig

# Callback to update the Apple share price chart
@app.callback(
    Output('apple-share-price-chart', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_apple_share_price_chart(n):
    global apple_broadcasting_share_price_df, apple_eager_broker_decision_df
    
    fig = go.Figure(data=[go.Scatter(x=apple_broadcasting_share_price_df['time_of_broadcasting'], y=apple_broadcasting_share_price_df['share_price'])])
    fig.update_layout(title='Apple Share Price', xaxis_title='Time', yaxis_title='Share Price')
    
    # Add markers for decision points
    decision_points = apple_eager_broker_decision_df[apple_eager_broker_decision_df['decision'] != 'DecisionType.HOLD']
    fig.add_trace(go.Scatter(x=decision_points['time_of_decision'], y=decision_points['share_price'], mode='markers', marker=dict(size=10, color=decision_points['decision'].map({'DecisionType.BUY': 'green', 'DecisionType.SELL': 'red'}))))
    
    return fig

# Callback to update the Amazon alerts
@app.callback(
    Output('amazon-alerts', 'children'),
    [Input('interval-component', 'n_intervals')]
)
def update_amazon_alerts(n):
    global amazon_eager_broker_decision_df

    alerts = []
    for index, row in amazon_eager_broker_decision_df.iterrows():
        alerts.append(html.P(f"{row['decision']} alert at {row['time_of_decision']}"))
    return alerts

# Callback to update the Apple alerts
@app.callback(
    Output('apple-alerts', 'children'),
    [Input('interval-component', 'n_intervals')]
)
def update_apple_alerts(n):
    global apple_eager_broker_decision_df

    alerts = []
    for index, row in apple_eager_broker_decision_df.iterrows():
        alerts.append(html.P(f"Alert: {row['decision']} at {row['time_of_decision']}"))
    return alerts

def get_new_data():
    global common_queue, amazon_broadcasting_share_price_df, apple_broadcasting_share_price_df, amazon_eager_broker_decision_df, apple_eager_broker_decision_df
    
    while not common_queue.empty():
        data_stream = common_queue.get()
        if isinstance(data_stream, EagerBrokerDecisionDTO):
            formatted_date = datetime.fromtimestamp(data_stream.time_of_decision).strftime("%d/%m/%y %H:%M:%S")
            if data_stream.based_of_data.symbol.symbol_name == 'AMZN':
                amazon_eager_broker_decision_df = pd.concat([amazon_eager_broker_decision_df,
                    pd.DataFrame({'time_of_decision': [formatted_date], 
                                  'share_price': [str(data_stream.based_of_data.share_price)], 
                                  'decision': [data_stream.decision]})])
            elif data_stream.based_of_data.symbol.symbol_name == 'AAPLE':
                apple_eager_broker_decision_df = pd.concat([apple_eager_broker_decision_df, 
                    pd.DataFrame({'time_of_decision': [formatted_date], 
                                  'share_price': [str(data_stream.based_of_data.share_price)], 
                                  'decision': [data_stream.decision]})])
        elif isinstance(data_stream, BroadcastingSharePriceDTO):
            formatted_date = datetime.fromtimestamp(data_stream.time_of_broadcasting).strftime("%d/%m/%y %H:%M:%S")
            if data_stream.symbol.symbol_name == 'AMZN':
                amazon_broadcasting_share_price_df = pd.concat([amazon_broadcasting_share_price_df, 
                    pd.DataFrame({'time_of_broadcasting': [formatted_date], 
                                  'share_price': [data_stream.share_price]})])
            elif data_stream.symbol.symbol_name == 'AAPLE':
                apple_broadcasting_share_price_df = pd.concat([apple_broadcasting_share_price_df, 
                    pd.DataFrame({'time_of_broadcasting': [formatted_date], 
                                  'share_price': [data_stream.share_price]})])


def process_queue():
    while True:
        if not common_queue.empty():
            get_new_data()
        # Adjust sleep time as needed to control the frequency of checking the queue
        time.sleep(1)

# Start the thread to continuously process the queue
queue_thread = threading.Thread(target=process_queue)
queue_thread.daemon = True  # Daemonize the thread to exit when the main program exits
queue_thread.start()