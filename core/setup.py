from core.entities.eager_broker import EagerBroker
from application.services import stock_exchange as se

def setup_stock_exchanges():
    stock_exchange1 = se.stock_exchange1.start()
    stock_exchange2 = se.stock_exchange2.start()
    return stock_exchange1, stock_exchange2

def setup_eager_broker():
    eager_broker = EagerBroker("EagerBroker AMZA and APLE")
    eager_broker.subscribe_to_stock_exchange(se.stock_exchange1)
    eager_broker.subscribe_to_stock_exchange(se.stock_exchange2)
    return eager_broker

def run():
    stock_exchange1, stock_exchange2 = setup_stock_exchanges()
    eager_broker = setup_eager_broker()

    print('Here will be data')
    while True:
        data_from_stock_exchange1 = se.stock_exchange1.get_data_from_queue()
        data_from_stock_exchange2 = se.stock_exchange2.get_data_from_queue()

        if data_from_stock_exchange1 is not None or data_from_stock_exchange2 is not None:
            print(data_from_stock_exchange1, data_from_stock_exchange2)

        # Make decision based on data from both exchanges
        eager_broker.make_decision(data_from_stock_exchange1)
        eager_broker.make_decision(data_from_stock_exchange2)
