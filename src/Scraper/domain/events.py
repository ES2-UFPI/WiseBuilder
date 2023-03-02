from dataclasses import dataclass

from framework.domain.components import Component
from framework.domain.value_object import Money
from framework.domain.events import DomainEvent


@dataclass
class LowerPriceRegisteredEvent(DomainEvent):
    component: Component
    price: Money
