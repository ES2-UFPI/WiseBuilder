from dataclasses import dataclass, field
from typing import List, Union

from .value_object import UUID, UUIDv4
from .rule import BussinessAssertionExtension
from .events import DomainEvent

__all__ = ["Entity", "AggregateRoot", "UniqueObject"]


@dataclass(kw_only=True, eq=False)
class Entity:
    _id: UUID

    def __eq__(self, oEntity):
        return self._id == oEntity._id

    def __hash__(self):
        return hash(self._id)

    @property
    def uid(self):
        return self._id

    @classmethod
    def next_id(cls) -> UUID:
        return UUIDv4()


@dataclass
class AggregateRoot(BussinessAssertionExtension, Entity):
    events: List[DomainEvent] = field(default_factory=list, init=False)


UniqueObject = Union[Entity, AggregateRoot]
