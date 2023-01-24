from dataclasses import dataclass, field
from .value_objects import UUID

@dataclass
class Entity:
    id: UUID = field(hash=True)

    @classmethod
    def next_id(cls) -> UUID:
        return UUID.v4()
