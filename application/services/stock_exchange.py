from core.entities.stock_exchange import StockExchange
from core.factories.stock_symbol_factory import StockSymbolFactory

import time

list_of_symbols_data = [('AAPLE', 'Apple', 150.0), ('AMZN', 'Amazon', 150.0)] # Could be replaced with DB

listed_symbols = [StockSymbolFactory.create_stock_symbol(*data) for data in list_of_symbols_data]

stock_exchange1 = StockExchange("StockExchange1", listed_symbols[0])
stock_exchange2 = StockExchange("StockExchange2", listed_symbols[1])
