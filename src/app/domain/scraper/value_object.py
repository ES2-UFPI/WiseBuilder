from dataclasses import dataclass
from typing import Tuple
from framework.domain.value_object import ValueObject, Url
from abc import ABC, abstractmethod


@dataclass
class CategoricalUrl(Url):
    component_name: str


@dataclass
class AbstractScraper(ABC, ValueObject):
    @abstractmethod
    def get_volatile_data(self) -> Tuple[Url, str, float, int]:
        pass
