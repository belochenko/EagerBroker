from core.entities.eager_broker import EagerBroker
from core.entities.stock_exchange import StockExchange
from core.factories.stock_exchange_factory import StockExchangeFactory

from typing import Tuple
from queue import Queue

import threading

common_queue = Queue()

stock_exchange_data = {
        "StockExchange1": ('AAPLE', 'Apple', 100.0),
        "StockExchange2": ('AMZN', 'Amazon', 120.0)
    }

def setup_stock_exchanges(stock_exchange_data) -> Tuple[StockExchange]:
    """
    Setup and start the stock exchanges based on the provided data.
    """
    stock_exchanges = StockExchangeFactory.create_stock_exchanges(stock_exchange_data)
    for exchange in stock_exchanges:
        exchange.start()
    return tuple(stock_exchanges)

def setup_eager_broker(stock_exchanges) -> EagerBroker:
    """
    Setup the EagerBroker and subscribe to the provided stock exchanges.
    """
    eager_broker = EagerBroker("EagerBroker AMZA and APLE")
    for exchange in stock_exchanges:
        eager_broker.subscribe_to_stock_exchange(exchange)
    return eager_broker

def _run_in_thread(stock_exchange_data: dict):
    # Setup stock exchanges
    stock_exchanges = setup_stock_exchanges(stock_exchange_data)

    # Setup EagerBroker
    eager_broker = setup_eager_broker(stock_exchanges)

    print('Setup is completed. Data stream is comming...')
    while True:
        # Retrieve data from stock exchanges
        for exchange in stock_exchanges:
            exchange_data = exchange.get_data_from_queue()
            decision_data = eager_broker.make_decision(exchange_data)
            if exchange_data or decision_data:
                print(exchange_data, decision_data)
                common_queue.put(exchange_data)
                common_queue.put(decision_data)

def run():
    t = threading.Thread(target=_run_in_thread, args=(stock_exchange_data,), daemon=True)
    t.start()
    t.join()
