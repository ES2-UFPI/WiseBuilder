from dataclasses import dataclass

from framework.domain.components import Component
from framework.domain.value_object import Money

from .exception import KnapsackBurst

__all__ = ["Knapsack"]


@dataclass
class Knapsack:
    components: list[Component]
    max_price: Money
    current_price: Money

    def push(self, component: Component, price: Money):
        if self.current_price + price > self.max_price:
            raise KnapsackBurst()

        # TODO checar restrições
        self.components.append(component)
