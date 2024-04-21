from core.dto.stock_symbol import StockSymbolDTO


class StockSymbolFactory:
    @staticmethod
    def create_stock_symbol(symbol: str, name: str, initial_price: float) -> StockSymbolDTO:
        return StockSymbolDTO(symbol, name, initial_price)
