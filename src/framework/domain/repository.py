from abc import ABC, abstractmethod
from typing import Set, List

from .entity import AggregateRoot
from .value_object import UUID

__all__ = [ 'AbstractRepository' ]

class AbstractRepository(ABC):
    seen: Set[AggregateRoot] = set()
    
    def add(self, item: AggregateRoot):
        self._add(item)
        self.seen.add(item)
    
    
    def get_by_uid(self, ref: UUID) -> AggregateRoot | None:
        _entity = self._get_by_uid(ref)
        if _entity:
            self.seen.add(_entity)
        return _entity
    
    
    def get(self, **kwargs) -> List[AggregateRoot]:
        _res = self._get(**kwargs)
        self.seen.update(_res)
        return _res
    
    
    @abstractmethod
    def _add(self, item: AggregateRoot):
        raise NotImplementedError
    
    
    @abstractmethod
    def _get_by_uid(self, ref: UUID) -> AggregateRoot | None:
        raise NotImplementedError
    
    
    @abstractmethod
    def _get(self, **kwargs) -> List[AggregateRoot]:
        raise NotImplementedError
    