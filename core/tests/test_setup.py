import unittest
from unittest.mock import MagicMock
from main import setup_stock_exchanges, setup_eager_broker, run

class TestRun(unittest.TestCase):
    def setUp(self):
        # Mock the behavior of stock exchanges and eager broker
        self.stock_exchange1 = MagicMock()
        self.stock_exchange2 = MagicMock()
        self.eager_broker = MagicMock()

    def test_setup_stock_exchanges(self):
        stock_exchange1, stock_exchange2 = setup_stock_exchanges()
        self.assertIsInstance(stock_exchange1, MagicMock)
        self.assertIsInstance(stock_exchange2, MagicMock)

    def test_setup_eager_broker(self):
        eager_broker = setup_eager_broker()
        self.assertIsInstance(eager_broker, MagicMock)

    def test_run(self):
        # Mock the behavior of stock exchanges
        self.stock_exchange1.get_data_from_queue.return_value = None
        self.stock_exchange2.get_data_from_queue.return_value = None

        # Mock the behavior of the eager broker
        self.eager_broker.make_decision.return_value = None

        # Call the run function and assert expected behavior
        run()

