class EagerBroker:
    def __init__(self, name):
        self.name = name
        self.data_queues = []

    def subscribe_to_stock_exchange(self, stock_exchange):
        # Subscribe to a stock exchange for data updates
        data_queue = Queue()
        self.data_queues.append(data_queue)
        stock_exchange.subscribe(data_queue)

    def receive_data_update(self, data):
        # Receive data updates from subscribed stock exchanges
        for data_queue in self.data_queues:
            data_queue.put(data)

    def make_decision(self, data):
        total_shares_sold, total_shares_bought, share_price = data

        # Decide whether to buy or sell based on the algorithm
        decision = ""
        if total_shares_sold > 2000 and share_price < 0.9 * share_price:
            decision = "buy"
        elif total_shares_bought > 2000 and share_price > 1.1 * share_price:
            decision = "sell"
        else:
            decision = "hold"

        # Create a tuple containing the decision and the original data
        decision_data = (decision, data)

        # Put the decision data into the data queue
        for data_queue in self.data_queues:
            data_queue.put(decision_data)
