from dataclasses import dataclass
from typing import Union

@dataclass
class BuyAction:
    pass


@dataclass
class SellAction:
    pass


@dataclass
class HoldAction:
    pass

@dataclass
class EagerBrokerDecisionDTO:
    desicion: Union[BuyAction, SellAction, HoldAction]
    based_of_data: any