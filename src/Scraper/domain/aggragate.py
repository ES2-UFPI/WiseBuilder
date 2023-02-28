from datetime import datetime
from dataclasses import dataclass, field
from typing import List

from framework.domain.entity import AggregateRoot
from framework.domain.value_object import UUID, Money, URL

_AttrsVolatileData = ["_id", "url", "component_id", "cost", "availability", "timestamp"]


@dataclass(kw_only=True)
class VolatileData(AggregateRoot):
    # url_id: UUID
    url: URL
    component_id: UUID
    cost: Money
    availability: bool

    timestamp: datetime = field(default=datetime.utcnow())

    @classmethod
    def get_attrs(cls) -> List[str]:
        return _AttrsVolatileData.copy()

    def generateVolatileDataPoint(
        self,
        _id: UUID,
        component_id: UUID,
        url: URL,
        cost: Money,
        availability: bool,
    ):
        return VolatileData(
            _id=_id,
            component_id=component_id,
            url=url,
            cost=cost,
            availability=availability,
        )
