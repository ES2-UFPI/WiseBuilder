from dataclasses import dataclass
from typing import Tuple
from framework.domain.value_object import URL, ValueObject
from abc import ABC, abstractmethod


@dataclass
class CategoricalUrl(URL):
    component_name: str


@dataclass
class AbstractScraper(ABC, ValueObject):
    @abstractmethod
    def get_volatile_data(self) -> Tuple[URL, str, float, int]:
        pass
