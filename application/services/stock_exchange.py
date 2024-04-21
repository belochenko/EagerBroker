from core.entities.stock_exchange import StockExchange
from core.factories.stock_symbol_factory import StockSymbolFactory

import time

list_of_symbols_data = [('AAPLE', 'Apple', 150.0), ('AMZN', 'Amazon', 150.0)] # Could be replaced with DB

listed_symbols = [StockSymbolFactory.create_stock_symbol(*data) for data in list_of_symbols_data]

stock_exchange1 = StockExchange("StockExchange1", listed_symbols[0])
stock_exchange2 = StockExchange("StockExchange2", listed_symbols[1])

# Function to handle the data stream from StockExchange instances
def handle_data_stream(stock_exchange):
    while True:
        # Retrieve data from StockExchange's data queue
        data = stock_exchange.get_data_from_queue()

        # Process the data as needed
        if data:
            print(f"Received data from StockExchange: {data}")

        # Add any additional processing or handling of the data here
        time.sleep(10)  # Adjust sleep time as needed
