
from datetime import datetime
from dataclasses import dataclass

from framework.domain.entity import Entity
from framework.domain.rule import Rule
from framework.domain.value_object import UUID, Money, URL


@dataclass(frozen=True)
class VolatileData(Entity):
    component_id: UUID
    url: URL
    cost: Money
    availability: bool
    timestamp: datetime = datetime.utcnow()

    def generateVolatileDataPoint(
        self, component_name: str, url: URL, cost: Money, availability: bool
    ):
        # Search for component name in SearchEngine-provided interface
        # SearchEngine.get_id_by_name(component_name)
        # Check if id was returned (if exists)

        self.check_rule(MatchesTrackedComponent(component_name))

        # component_id = SearchEngine.get_id_by_name(component_name)
        component_id = UUID("00000000-00000000-00000000-00000000")

        return VolatileData(
            component_id=component_id, url=url, cost=cost, availability=availability
        )


@dataclass
class MatchesTrackedComponent(Rule):
    # Verifica se o componente é um dos componentes observados
    component_name: str

    def is_broken(self) -> bool:
        # verificar se componente existe
        # return not SearchEngine.get_id_by_name(component_name)
        return False
