from framework.domain.events import Command
from dataclasses import dataclass

from Scraper.domain.entity import CategoryURL
from Scraper.domain.aggragate import VolatileData

__all__ = [
    "AddCategoryURL",
    "GetAllDomains",
    "GetCategoryURLByDomain",
    "AddVolatileData",
]


@dataclass
class AddCategoryURL(Command):
    category_url: CategoryURL


@dataclass
class GetAllDomains(Command):
    pass


@dataclass
class GetCategoryURLByDomain(Command):
    domain: str


@dataclass
class AddVolatileData(Command):
    volatile_data: VolatileData
