from dataclasses import dataclass

from core.dto.stock_symbol import StockSymbolDTO

@dataclass
class StockExchangeEmitTypeDTO:
    symbol: StockSymbolDTO
    share_price: float
    total_shares_sold: int
    total_shares_bought: int
    time_of_emission: float

    def __iter__(self):
        return iter([self.symbol, self.share_price, self.total_shares_sold, self.total_shares_bought])

@dataclass
class BroadcastingSharePriceDTO:
    symbol: StockSymbolDTO
    share_price: float
    time_of_broadcasting: float
