from dataclasses import dataclass
from typing import Union

from enum import Enum

class DecisionType(Enum):
    BUY = "ActionToBuy"
    SELL = "ActionToSell"
    HOLD = "ActionToHold"

@dataclass
class EagerBrokerDecisionDTO:
    decision: DecisionType
    based_of_data: any
    time_of_decision: float