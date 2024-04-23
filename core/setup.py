from core.entities.eager_broker import EagerBroker
from core.entities.stock_exchange import StockExchange
from core.factories.stock_exchange_factory import StockExchangeFactory

from typing import Tuple

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

def run():
    # Setup stock exchanges
    stock_exchanges = setup_stock_exchanges({
        "StockExchange1": ('AAPLE', 'Apple', 100.0),
        "StockExchange2": ('AMZN', 'Amazon', 120.0)
    })

    # Setup EagerBroker
    eager_broker = setup_eager_broker(stock_exchanges)

    while True:
        data_from_stock_exchange1 = stock_exchanges[0].get_data_from_queue()
        data_from_stock_exchange2 = stock_exchanges[1].get_data_from_queue()

        if data_from_stock_exchange1 or data_from_stock_exchange2:
            print(f"{data_from_stock_exchange1}")
            print(f"{data_from_stock_exchange2}")

        # Make decision based on data from both exchanges
        broker_on_stock_exchange1 = eager_broker.make_decision(data_from_stock_exchange1)
        broker_on_stock_exchange2 = eager_broker.make_decision(data_from_stock_exchange2)

        if broker_on_stock_exchange1 or broker_on_stock_exchange2:
            print(f'{broker_on_stock_exchange1}')
            print(f'{broker_on_stock_exchange2}')