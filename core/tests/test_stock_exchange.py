import unittest
from unittest.mock import MagicMock
from core.dto.stock_exchange import BroadcastingSharePriceDTO, StockExchangeEmitTypeDTO
from core.entities.stock_exchange import StockExchange

class TestStockExchange(unittest.TestCase):
    def setUp(self):
        self.stock_exchange = StockExchange("Test Stock Exchange", "TEST")

    def test_update_share_price(self):
        initial_price = self.stock_exchange.share_price
        self.stock_exchange.update_share_price()
        self.assertNotEqual(initial_price, self.stock_exchange.share_price)

    def test_generate_random_data(self):
        self.stock_exchange.start()
        data = self.stock_exchange.get_data_from_queue()
        self.assertIsNotNone(data)
        self.assertTrue(isinstance(data, (BroadcastingSharePriceDTO, StockExchangeEmitTypeDTO)))
        self.stock_exchange.stop()