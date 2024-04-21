from dataclasses import dataclass

from core.dto.stock_symbol import StockSymbolDTO

@dataclass
class StockExchangeEmitTypeDTO:
    symbol: StockSymbolDTO
    share_price: float
    total_shares_sold: int
    total_shares_bought: int

@dataclass
class BroadcastingSharePriceDTO:
    symbol: StockSymbolDTO
    share_price: float
