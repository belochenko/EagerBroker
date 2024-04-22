from queue import Queue

from core.entities.stock_exchange import StockExchange
from core.dto.eager_broker import EagerBrokerDecisionDTO

import threading

class EagerBroker:
    def __init__(self, name):
        self.name = name
        self.eager_broker_queue = Queue()

    def subscribe_to_stock_exchange(self, stock_exchange: StockExchange):
        # Subscribe to a stock exchange for data updates
        thread = threading.Thread(target=self._subscribe_thread, args=(stock_exchange,))
        thread.start()

    def _subscribe_thread(self, stock_exchange: StockExchange):
        
        while stock_exchange.running:
            stock_exchange_data = stock_exchange.get_data_from_queue()
            if stock_exchange_data:
                self.eager_broker_queue.put(stock_exchange_data)

    def receive_data_update(self, data):
        # Receive data updates from subscribed stock exchanges
        for data_queue in self.data_queues:
            data_queue.put(data)

    def make_decision(self, data):
        if data:
            symbol, share_price, total_shares_sold, total_shares_bought = data

            initial_share_price = symbol.initial_price

            # Calculate the percentage change in share price
            percentage_change = ((share_price - initial_share_price) / initial_share_price) * 100

            # Decide whether to buy or sell based on the algorithm
            decision = ""
            if total_shares_sold > 2000 and percentage_change < -10:
                decision = "buy"
            elif total_shares_bought > 2000 and percentage_change > 10:
                decision = "sell"
            else:
                decision = "hold"

            # Create a tuple containing the decision and the original data
            decision_data = (decision, data)

            print(decision_data)
            # Put the decision data into the eager_broker_queue
            self.eager_broker_queue.put(decision_data)
