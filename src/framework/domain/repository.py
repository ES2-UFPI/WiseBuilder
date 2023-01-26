from abc import ABC, abstractmethod

from .entity import Entity
from .value_object import UUID

class AbstractRepository(ABC):
    @abstractmethod
    def add(self, item: Entity):
        raise NotImplementedError
    
    
    @abstractmethod
    def get(self, ref: UUID) -> Entity:
        raise NotImplementedError
    