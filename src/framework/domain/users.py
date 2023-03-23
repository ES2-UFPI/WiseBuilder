from dataclasses import dataclass
from ..domain.entity import Entity


AttrsUser = ["_id", "email", "name", "is_admin"]


@dataclass(kw_only=True, eq=False)
class User(Entity):
    name: str
    email: str
    is_admin: bool

    def __hash__(self):
        return hash(self.uid)
