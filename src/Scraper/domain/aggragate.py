from datetime import datetime
from dataclasses import dataclass, field
from framework.domain.entity import AggregateRoot
from framework.domain.value_object import UUID, Money, URL
from .entity import MatchesTrackedComponent


@dataclass(kw_only=True)
class VolatileData(AggregateRoot):
    component_id: UUID
    url_id: UUID
    url: URL
    cost: Money
    availability: bool

    timestamp: datetime = field(default=datetime.utcnow())

    def generateVolatileDataPoint(
        self,
        _id: UUID,
        component_id: UUID,
        url_id: UUID,
        url: URL,
        cost: Money,
        availability: bool,
    ):

        return VolatileData(
            _id=_id,
            component_id=component_id,
            url_id=url_id,
            url=url,
            cost=cost,
            availability=availability,
        )
