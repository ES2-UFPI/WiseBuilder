from abc import ABC, abstractmethod
from typing import Set, List

from .entity import UniqueObject
from .value_object import UUID

__all__ = ["AbstractRepository"]


class AbstractRepository(ABC):
    seen: Set[UniqueObject] = set()

    def add(self, item: UniqueObject):
        self._add(item)
        self.seen.add(item)

    def get_by_uid(self, ref: UUID) -> UniqueObject | None:
        _entity = self._get_by_uid(ref)
        if _entity:
            self.seen.add(_entity)
        return _entity

    def get(self, **kwargs) -> List[UniqueObject]:
        _res = self._get(**kwargs)
        self.seen.update(_res)
        return _res

    @abstractmethod
    def _add(self, item: UniqueObject):
        raise NotImplementedError

    @abstractmethod
    def _get_by_uid(self, ref: UUID) -> UniqueObject | None:
        raise NotImplementedError

    @abstractmethod
    def _get(self, **kwargs) -> List[UniqueObject]:
        raise NotImplementedError


class AbstractCategoryURLRepository(AbstractRepository):
    def get_all_domains(self):
        _res = self._get_all_domains()
        return _res

    @abstractmethod
    def _get_all_domains(self):
        raise NotImplemented
