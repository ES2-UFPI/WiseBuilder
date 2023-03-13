from dataclasses import dataclass

from framework.domain.value_object import UUID
from framework.domain.value_object import Money
from framework.domain.events import DomainEvent


@dataclass
class LowerPriceRegisteredEvent(DomainEvent):
    component_uid : UUID
    price: Money
