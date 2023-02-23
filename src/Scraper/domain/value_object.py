from typing import Tuple, List
from dataclasses import dataclass
from framework.domain.value_object import URL, ValueObject, Money
from abc import ABC, abstractmethod


@dataclass
class AbstractScraper(ABC, ValueObject):
    @abstractmethod
    def get_volatile_data(self, url: URL) -> Tuple[URL, List[Tuple[str, Money, bool]]]:
        pass
