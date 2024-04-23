import random
import time
import threading

from typing import Union, Any
from queue import Queue

from core.dto.stock_exchange import BroadcastingSharePriceDTO, StockExchangeEmitTypeDTO
from core.dto.stock_symbol import StockSymbolDTO
from core.entities.tools import timer_tool

class StockExchange:
    def __init__(self, name: str, symbol: StockSymbolDTO):
        self.name = name
        self.symbol = symbol
        self.share_price = symbol.initial_price  # Initial share price
        self.total_shares_sold = 0
        self.total_shares_bought = 0
        self.share_price_increase_probability = None  # Probability of share price increase
        self.share_price_decrease_probability = None  # Probability of share price decrease
        self.start_time = time.time()

        self.data_queue = Queue()
        self.running = False

        self.lock = threading.Lock()
        

    def _update_share_price(self):
        with self.lock:
            # Calculate probability of share price increase (p(I)) and decrease (p(D))
            self.share_price_increase_probability = int((self.total_shares_sold / (self.total_shares_bought + self.total_shares_sold)) * 100)
            self.share_price_decrease_probability = int((self.total_shares_bought / (self.total_shares_bought + self.total_shares_sold)) * 100)

            # Update share price based on probabilities
            if random.randint(0, 100) < self.share_price_increase_probability:
                self.share_price *= 1.1  # Increase share price by 10%
                self.share_price = round(self.share_price, 2)
            else:
                self.share_price *= 0.9  # Decrease share price by 10%
                self.share_price = round(self.share_price, 2)
    
    # Share price broadcast frequency in seconds
    @timer_tool.set_interval(60)
    def _broadcast_share_price(self):
        # Broadcast share price periodically
        with self.lock:
            self.data_queue.put(BroadcastingSharePriceDTO(
                symbol=self.symbol,
                share_price=self.share_price,
                time_of_broadcasting=time.time()
            ))

     # Update frequency in seconds
    @timer_tool.set_interval(1)
    def _stock_share_price_emission(self):
        # Generate random share sales or purchases every second
            share_change = int(random.uniform(1, 1000))
            # Define weights for buying and selling shares
            weights = [0.5, 0.5]  # 50% chance for buying and 50% chance for selling
            # Choose randomly based on weights
            # More control than random.random() < 0.5
            is_selling = random.choices([True, False], weights=weights)
            if is_selling: 
                self.total_shares_sold -= share_change
            else:
                self.total_shares_bought += share_change

            # Update share price
            self._update_share_price()
            
            with self.lock:
                self.data_queue.put(StockExchangeEmitTypeDTO(
                    symbol=self.symbol,
                    share_price=self.share_price,
                    total_shares_sold=self.total_shares_sold,
                    total_shares_bought=self.total_shares_bought,
                    time_of_emission=time.time()
                ))

    def get_data_from_queue(self) -> Union[Any, None]:
        if not self.data_queue.empty():
            return self.data_queue.get()
        return None
      
    def start(self):
        self.running = True
        threading.Thread(target=self._broadcast_share_price, daemon=True).start()
        threading.Thread(target=self._stock_share_price_emission, daemon=True).start()

    def stop(self):
        self.running = False
