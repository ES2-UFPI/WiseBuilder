from typing import Tuple
from dataclasses import dataclass
from framework.domain.value_object import URL, ValueObject, Money
from abc import ABC, abstractmethod


@dataclass
class CategoricalUrl(URL):
    component_name: str


@dataclass
class AbstractScraper(ABC, ValueObject):
    @abstractmethod
    def get_volatile_data(self) -> Tuple[URL, str, Money, int]:
        pass
