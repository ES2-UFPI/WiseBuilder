from dataclasses import dataclass, field
from typing import List, Dict, Any

from framework.domain.components import Component, EComponentType, component_cls_idx
from framework.domain.value_object import UUID, UUIDv4
from framework.domain.events import Command

__all__ = [
    "GetComponentByUID",
    "ListComponentsByType",
    "AddComponent",
    "SearchByName",
    "MatchName",
]


@dataclass
class GetComponentByUID(Command):
    uid: UUID


@dataclass
class ListComponentsByType(Command):
    ctype: EComponentType
    qsize: int = field(init=False, default=10)
    _attrs: List[str] = field(init=False)

    _filters_lt: Dict[str, Any] = field(init=False, default_factory=dict)
    _filters_eq: Dict[str, Any] = field(init=False, default_factory=dict)
    _filters_gt: Dict[str, Any] = field(init=False, default_factory=dict)

    def __post_init__(self):
        self._attrs = Component.get_attrs(self.ctype)

    @classmethod
    def Motherboard(cls) -> "ListComponentsByType":
        return ListComponentsByType(EComponentType.MOTHERBOARD)

    @classmethod
    def CPU(cls) -> "ListComponentsByType":
        return ListComponentsByType(EComponentType.CPU)

    @classmethod
    def GPU(cls) -> "ListComponentsByType":
        return ListComponentsByType(EComponentType.GPU)

    @classmethod
    def RAM(cls) -> "ListComponentsByType":
        return ListComponentsByType(EComponentType.RAM)

    @classmethod
    def Persistence(cls) -> "ListComponentsByType":
        return ListComponentsByType(EComponentType.PERSISTENCE)

    @classmethod
    def PSU(cls) -> "ListComponentsByType":
        return ListComponentsByType(EComponentType.PSU)

    def _parse_filters(self, **kwargs) -> Dict[str, Any]:
        return {
            k: v for k, v in ((attr, kwargs.get(attr)) for attr in self._attrs) if v
        }

    def FilterLT(self, **kwargs) -> "ListComponentsByType":
        self._filters_gt = self._parse_filters(**kwargs)
        return self

    def FilterEq(self, **kwargs) -> "ListComponentsByType":
        self._filters_eq = self._parse_filters(**kwargs)
        return self

    def FilterGT(self, **kwargs) -> "ListComponentsByType":
        self._filters_lt = self._parse_filters(**kwargs)
        return self

    def setQuerySize(self, qsize: int):
        self.qsize = qsize if qsize > 0 else 0
        return self


@dataclass
class AddComponent(Command):
    component: Component

    @classmethod
    def _from_kwargs(cls, type, specs_dict):
        # Comparar com a base?
        specs_dict["_id"] = UUIDv4()
        built = component_cls_idx[type](**specs_dict)
        return AddComponent(built)

    @classmethod
    def buildMotherboard(cls, **kwargs):
        return cls._from_kwargs(EComponentType.MOTHERBOARD, kwargs)

    @classmethod
    def buildCPU(cls, **kwargs):
        return cls._from_kwargs(EComponentType.CPU, kwargs)

    @classmethod
    def buildGPU(cls, **kwargs):
        return cls._from_kwargs(EComponentType.GPU, kwargs)

    @classmethod
    def buildRAM(cls, **kwargs):
        return cls._from_kwargs(EComponentType.RAM, kwargs)

    @classmethod
    def buildPersistence(cls, **kwargs):
        return cls._from_kwargs(EComponentType.PERSISTENCE, kwargs)

    @classmethod
    def buildPSU(cls, **kwargs):
        return cls._from_kwargs(EComponentType.PSU, kwargs)


@dataclass
class SearchByName(Command):
    name: str
    ctype: EComponentType | None = None

    @classmethod
    def Motherboard(cls, query) -> "SearchByName":
        return SearchByName(query, EComponentType.MOTHERBOARD)

    @classmethod
    def CPU(cls, query) -> "SearchByName":
        return SearchByName(query, EComponentType.CPU)

    @classmethod
    def GPU(cls, query) -> "SearchByName":
        return SearchByName(query, EComponentType.GPU)

    @classmethod
    def RAM(cls, query) -> "SearchByName":
        return SearchByName(query, EComponentType.RAM)

    @classmethod
    def Persistence(cls, query) -> "SearchByName":
        return SearchByName(query, EComponentType.PERSISTENCE)

    @classmethod
    def PSU(cls, query) -> "SearchByName":
        return SearchByName(query, EComponentType.PSU)


@dataclass
class MatchName(Command):
    name: str
    ctype: EComponentType | None = None

    @classmethod
    def Motherboard(cls, query) -> "MatchName":
        return MatchName(query, EComponentType.MOTHERBOARD)

    @classmethod
    def CPU(cls, query) -> "MatchName":
        return MatchName(query, EComponentType.CPU)

    @classmethod
    def GPU(cls, query) -> "MatchName":
        return MatchName(query, EComponentType.GPU)

    @classmethod
    def RAM(cls, query) -> "MatchName":
        return MatchName(query, EComponentType.RAM)

    @classmethod
    def Persistence(cls, query) -> "MatchName":
        return MatchName(query, EComponentType.PERSISTENCE)

    @classmethod
    def PSU(cls, query) -> "MatchName":
        return MatchName(query, EComponentType.PSU)
