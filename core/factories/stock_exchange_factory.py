from core.entities.stock_exchange import StockExchange
from core.factories.stock_symbol_factory import StockSymbolFactory

class StockExchangeFactory:
    @staticmethod
    def create_stock_exchanges(stock_exchange_data):
        """
        Create multiple StockExchange instances based on the provided data.
        """
        stock_exchanges = []
        for name, symbol_data in stock_exchange_data.items():
            stock_symbol = StockSymbolFactory.create_stock_symbol(*symbol_data)
            stock_exchange = StockExchange(name, stock_symbol)
            stock_exchanges.append(stock_exchange)
        return stock_exchanges

