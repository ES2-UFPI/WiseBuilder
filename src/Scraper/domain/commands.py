from framework.domain.events import Command
from dataclasses import dataclass

from Scraper.domain.entity import CategoryURL
from Scraper.domain.aggragate import VolatileData
from framework.domain.value_object import UUID, Money
from framework.domain.components import Component
from framework.domain.components_enums import *

__all__ = [
    "AddCategoryURL",
    "GetAllDomains",
    "GetCategoryURLByDomain",
    "AddVolatileData",
    "GetVolatileDataByMaxCost",
    "GetVolatileDataByComponentUID",
    "GetLowerCostVolatileDatas",
    "GetComponentsFromVolatileData",
    "GetVolatileDataByCostInterval",
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


@dataclass
class GetLowerCostVolatileDatas(Command):
    cost: float = -1
    pass


@dataclass
class GetVolatileDataByComponentUID(Command):
    component_uid: UUID


@dataclass
class GetComponentsFromVolatileData(Command):
    volatile_data: list[VolatileData]


@dataclass
class GetVolatileDataByCostInterval(Command):
    component_type: EComponentType
    min_cost: float
    max_cost: float
