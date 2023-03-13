from dataclasses import dataclass

from framework.domain.entity import Entity
from framework.domain.value_object import URL
from framework.domain.components import EComponentType


@dataclass
class CategoryURL(Entity):
    url: URL
    category: EComponentType

    def __hash__(self):
        return hash(self.uid)


AttrsCategoryURL = ["uid", "url", "category"]
