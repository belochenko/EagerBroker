from dataclasses import dataclass

@dataclass
class StockSymbolDTO:
    symbol_name: str
    name: str
    initial_price: float
