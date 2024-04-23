from queue import Queue
from core.dto.stock_exchange import BroadcastingSharePriceDTO, StockExchangeEmitTypeDTO

from core.entities.stock_exchange import StockExchange
from core.dto.eager_broker import EagerBrokerDecisionDTO, DecisionType

from typing import Union
import threading
import time


class EagerBroker:
    def __init__(self, name: str):
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

    @staticmethod
    def make_decision(data: Union[StockExchangeEmitTypeDTO, BroadcastingSharePriceDTO]) -> EagerBrokerDecisionDTO:
        if isinstance(data, StockExchangeEmitTypeDTO):
            symbol, curr_share_price, total_shares_sold, total_shares_bought = data
            
            initial_share_price = symbol.initial_price

            # Calculate the percentage change in share price
            percentage_change = int(((curr_share_price - initial_share_price) / initial_share_price) * 100)

            # Decide whether to buy or sell based on the algorithm
            decision = None
            if (total_shares_bought + total_shares_sold) < -2000 and percentage_change < -10:
                decision = EagerBrokerDecisionDTO(decision=DecisionType.BUY, based_of_data=data, time_of_decision=time.time())
            # if the overall number of shares since the last share price update exceeds a total of 2K shares bought, 
            # Eagy Broker will suggest to sell a given share, as long as the current share price is at least 10% higher 
            # than the initial share price.
            elif (total_shares_sold + total_shares_bought) > 2000 and percentage_change > 10:
                decision = EagerBrokerDecisionDTO(decision=DecisionType.SELL, based_of_data=data, time_of_decision=time.time())
            else:
                decision = EagerBrokerDecisionDTO(decision=DecisionType.HOLD, based_of_data=data, time_of_decision=time.time())

            return decision
        
        elif isinstance(data, BroadcastingSharePriceDTO):
            # Handle BroadcastingSharePriceDTO (emitted every minute)
            symbol = data.symbol
            share_price = data.share_price