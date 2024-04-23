"""
THE NEXT CODE IS SUPER DUMMY AND HAS BEEN CREATED ONLY FOR DEMO
"""

import threading, time
from core import setup

from core.dto.eager_broker import EagerBrokerDecisionDTO
from core.dto.stock_exchange import BroadcastingSharePriceDTO, StockExchangeEmitTypeDTO

import dash
import dash_core_components as dcc

import plotly.graph_objects as go
import pandas as pd

from dash import html
from dash.dependencies import Input, Output

from datetime import datetime

common_queue = setup.common_queue

# Initialize empty dataframes to store the data
amazon_stock_exchange_df = pd.DataFrame(columns=['time_of_emission', 'total_shares_bought', 'total_shares_sold', 'resulted_total_shares_sold_n_bought'])
apple_stock_exchange_df = pd.DataFrame(columns=['time_of_emission', 'total_shares_bought', 'total_shares_sold', 'resulted_total_shares_sold_n_bought'])
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
    global amazon_stock_exchange_df

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x=amazon_stock_exchange_df['time_of_emission'], y=amazon_stock_exchange_df['resulted_total_shares_sold_n_bought'],
                   mode='lines+markers',
                   name='sold+bought'
                   )
    )

    # fig = go.Figure(data=[go.Scatter(x=amazon_stock_exchange_df['time_of_emission'], y=amazon_stock_exchange_df['resulted_total_shares_sold_n_bought'])])
    fig.update_layout(title='Amazon Share Price', xaxis_title='Time', yaxis_title='Share Price')

    return fig

# Callback to update the Apple share price chart
@app.callback(
    Output('apple-share-price-chart', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_apple_share_price_chart(n):
    global apple_stock_exchange_df

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x=apple_stock_exchange_df['time_of_emission'], y=apple_stock_exchange_df['resulted_total_shares_sold_n_bought'],
                   mode='lines+markers',
                   name='sold+bought'
                   )
    )
    
    # fig = go.Figure(data=[go.Scatter(x=apple_broadcasting_share_price_df['time_of_broadcasting'], y=apple_broadcasting_share_price_df['share_price'])])
    fig.update_layout(title='Apple Share Price', xaxis_title='Time', yaxis_title='Share Price')
    
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
    global amazon_broadcasting_share_price_df, apple_broadcasting_share_price_df
    global amazon_eager_broker_decision_df, apple_eager_broker_decision_df
    global amazon_stock_exchange_df, apple_stock_exchange_df
    
    while not common_queue.empty():
        data_stream = common_queue.get()
        print(data_stream)
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
        elif isinstance(data_stream, StockExchangeEmitTypeDTO):
            formatted_date = datetime.fromtimestamp(data_stream.time_of_emission).strftime("%d/%m/%y %H:%M:%S")
            if data_stream.symbol.symbol_name == 'AMZN':
                amazon_stock_exchange_df = pd.concat([amazon_stock_exchange_df,
                    pd.DataFrame({'time_of_emission': [formatted_date], 
                                  'total_shares_bought': [data_stream.total_shares_bought], 
                                  'total_shares_sold': [data_stream.total_shares_sold],
                                  'resulted_total_shares_sold_n_bought': [data_stream.total_shares_sold - data_stream.total_shares_bought]
                                  })])
                print(amazon_stock_exchange_df)
            elif data_stream.symbol.symbol_name == 'AAPLE':
                apple_stock_exchange_df = pd.concat([apple_stock_exchange_df, 
                    pd.DataFrame({'time_of_emission': [formatted_date], 
                                  'total_shares_bought': [data_stream.total_shares_bought], 
                                  'total_shares_sold': [data_stream.total_shares_sold],
                                  'resulted_total_shares_sold_n_bought': [data_stream.total_shares_sold - data_stream.total_shares_bought]
                                  })])
                print(apple_stock_exchange_df)
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
        time.sleep(1)

# Start the thread to continuously process the queue
queue_thread = threading.Thread(target=process_queue)
queue_thread.daemon = True
queue_thread.start()