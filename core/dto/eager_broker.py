from dataclasses import dataclass
from typing import Union

from enum import Enum

from core.dto.stock_exchange import StockExchangeEmitTypeDTO

class DecisionType(Enum):
    BUY = "ActionToBuy"
    SELL = "ActionToSell"
    HOLD = "ActionToHold"

@dataclass
class EagerBrokerDecisionDTO:
    decision: DecisionType
    based_of_data: StockExchangeEmitTypeDTO
    time_of_decision: float