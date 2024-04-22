import unittest
from unittest.mock import MagicMock
import threading
import time
from queue import Queue
from core.dto.stock_exchange import BroadcastingSharePriceDTO, StockExchangeEmitTypeDTO
from core.entities.stock_exchange import StockExchange
from core.dto.eager_broker import EagerBrokerDecisionDTO, BuyAction, SellAction, HoldAction
from core.entities.eager_broker import EagerBroker

class TestEagerBroker(unittest.TestCase):
    def test_subscribe_to_stock_exchange(self):
        stock_exchange = MagicMock(spec=StockExchange)
        eager_broker = EagerBroker("Test Eager Broker")
        eager_broker.subscribe_to_stock_exchange(stock_exchange)
        stock_exchange.running = False

        # Give some time for the thread to finish
        time.sleep(0.1)

        self.assertEqual(stock_exchange.get_data_from_queue.call_count, 0)

    def test_make_decision_buy_action(self):
        symbol = MagicMock()
        symbol.initial_price = 100.0
        data = StockExchangeEmitTypeDTO(symbol, 90.0, 3000, 1000)
        decision = EagerBroker.make_decision(data)
        self.assertIsInstance(decision, EagerBrokerDecisionDTO)
        self.assertEqual(decision.decision, BuyAction)

    def test_make_decision_sell_action(self):
        symbol = MagicMock()
        symbol.initial_price = 100.0
        data = StockExchangeEmitTypeDTO(symbol, 110.0, 1000, 3000)
        decision = EagerBroker.make_decision(data)
        self.assertIsInstance(decision, EagerBrokerDecisionDTO)
        self.assertEqual(decision.decision, SellAction)

    def test_make_decision_hold_action(self):
        symbol = MagicMock()
        symbol.initial_price = 100.0
        data = StockExchangeEmitTypeDTO(symbol, 95.0, 1000, 1000)
        decision = EagerBroker.make_decision(data)
        self.assertIsInstance(decision, EagerBrokerDecisionDTO)
        self.assertEqual(decision.decision, HoldAction)
