import random
import time

class StockExchange:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol
        self.share_price = random.uniform(100, 500)
        self.total_shares_sold = 0
        self.total_shares_bought = 0
        self.share_price_update_probability = 0.37

    def update_share_price(self):
        if random.random() < self.share_price_update_probability:
            self.share_price *= 1.1  # Increase share price by 10%

    def generate_random_data(self):
        while True:
            # Generate random share sales or purchases
            share_change = random.randint(-1000, 1000)
            if share_change > 0:
                self.total_shares_bought += share_change
            else:
                self.total_shares_sold += abs(share_change)

            # Update share price
            self.update_share_price()

            # Emit data
            print(f"{self.symbol}: Share price - ${self.share_price}, "
                  f"Total shares sold - {self.total_shares_sold}, "
                  f"Total shares bought - {self.total_shares_bought}")

            time.sleep(1)  # Simulate data streaming every second
