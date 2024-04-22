import random
import time
import threading

from typing import Generator
from queue import Queue

from core.dto.stock_exchange import BroadcastingSharePriceDTO, StockExchangeEmitTypeDTO


class StockExchange:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol
        self.share_price = random.uniform(100, 500)  # Initial share price
        self.total_shares_sold = 0
        self.total_shares_bought = 0
        self.share_price_increase_probability = None  # Probability of share price increase
        self.share_price_decrease_probability = None  # Probability of share price decrease
        self.update_frequency = 1  # Update frequency in seconds
        self.price_broadcast_frequency = 60  # Share price broadcast frequency in seconds
        self.start_time = time.time()

        self.data_queue = Queue()
        self.running = False

    def update_share_price(self):
        # Calculate probability of share price increase (p(I)) and decrease (p(D))
        self.share_price_increase_probability = self.total_shares_sold / (self.total_shares_bought + self.total_shares_sold)
        self.share_price_decrease_probability = self.total_shares_bought / (self.total_shares_bought + self.total_shares_sold)

        # Update share price based on probabilities
        if random.random() < self.share_price_increase_probability:
            self.share_price *= 1.1  # Increase share price by 10%
        elif random.random() < self.share_price_increase_probability:
            self.share_price *= 0.9  # Decrease share price by 10%

    def _generate_random_data(self) -> None:
        while True:
            current_time = time.time()
            elapsed_time = current_time - self.start_time

            # Emit share price update every minute
            if elapsed_time >= self.price_broadcast_frequency:
                print(f"{self.symbol}: Broadcasting share price - ${self.share_price}")

                self.start_time = current_time
                
                self.data_queue.put(BroadcastingSharePriceDTO(
                    symbol=self.symbol,
                    share_price=self.share_price,
                    time_of_broadcasting=time.time()
                    )
                )

            # Generate random share sales or purchases every second
            share_change = int(random.uniform(1, 1000))
            if random.random() < 0.5:
                self.total_shares_sold += share_change
            else:
                self.total_shares_bought += share_change

            # Update share price
            self.update_share_price()

            self.data_queue.put(StockExchangeEmitTypeDTO(
                symbol=self.symbol,
                share_price=self.share_price,
                total_shares_sold=self.total_shares_sold,
                total_shares_bought=self.total_shares_bought,
                time_of_emission=time.time()
            ))
            time.sleep(self.update_frequency)

    def get_data_from_queue(self):
        if not self.data_queue.empty():
            return self.data_queue.get()
        else:
            return None

    def start(self):
        self.running = True
        threading.Thread(target=self._generate_random_data, daemon=True).start()

    def stop(self):
        self.running = False
