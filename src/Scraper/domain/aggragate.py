from datetime import datetime
from dataclasses import dataclass, field
from typing import List

from framework.domain.components_enums import EComponentType
from framework.domain.entity import AggregateRoot
from framework.domain.value_object import UUID, Money, URL

_AttrsVolatileData = [
    "_id",
    "url",
    "component_id",
    "component_type",
    "cost",
    "availability",
    "timestamp",
]


@dataclass(kw_only=True)
class VolatileData(AggregateRoot):
    url: URL
    component_id: UUID
    component_type: EComponentType
    cost: Money
    availability: bool

    timestamp: datetime = field(default=datetime.utcnow())

    def __hash__(self):
        return hash(self.uid)

    @classmethod
    def get_attrs(cls) -> List[str]:
        return _AttrsVolatileData.copy()

    def generateVolatileDataPoint(
        self,
        _id: UUID,
        component_id: UUID,
        component_type: EComponentType,
        url: URL,
        cost: Money,
        availability: bool,
    ):
        return VolatileData(
            _id=_id,
            component_id=component_id,
            component_type=component_type,
            url=url,
            cost=cost,
            availability=availability,
        )
