from framework.domain.events import Command
from dataclasses import dataclass

from Scraper.domain.entity import CategoryURL
from Scraper.domain.aggragate import VolatileData
from framework.domain.value_object import UUID, Money

__all__ = [
    "AddCategoryURL",
    "GetAllDomains",
    "GetCategoryURLByDomain",
    "AddVolatileData",
    "GetVolatileDataByMaxCost",
    "GetVolatileDataByComponentUID",
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


@dataclass
class GetVolatileDataByUID(Command):
    uid: UUID


@dataclass
class GetVolatileDataByMaxCost(Command):
    cost: float


class GetVolatileDataByComponentUID(Command):
    component_uid: UUID
