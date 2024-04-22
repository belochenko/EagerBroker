import unittest
from core.dto.stock_symbol import StockSymbolDTO
from core.factories.stock_symbol_factory import StockSymbolFactory

class TestStockSymbolFactory(unittest.TestCase):
    def test_create_stock_symbol(self):
        symbol = "AAPL"
        name = "Apple"
        initial_price = 150.0
        stock_symbol = StockSymbolFactory.create_stock_symbol(symbol, name, initial_price)
        self.assertIsInstance(stock_symbol, StockSymbolDTO)
        self.assertEqual(stock_symbol.symbol, symbol)
        self.assertEqual(stock_symbol.name, name)
        self.assertEqual(stock_symbol.initial_price, initial_price)
