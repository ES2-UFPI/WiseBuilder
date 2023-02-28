from dataclasses import dataclass, field
from typing import Dict
from abc import ABCMeta, abstractmethod

from framework.domain.value_object import UUID
from framework.domain.repository import AbstractRepository
from framework.domain.exception import DomainException
from Scraper.domain.aggragate import VolatileData


@dataclass
class EntityUIDNotFoundException(DomainException):
    entity_id: UUID
    _message: str = field(init=False)

    def __post_init__(self):
        self._message = f"{self.__class__.__name__}: "
        f"Componente com UID {self.entity_id} não existe."


class MockRepository(AbstractRepository):
    def __init__(self, volatile_datas: Dict[UUID, VolatileData]):
        self._volatile_data = volatile_datas

    def _add(self, volatile_data: VolatileData):
        self._volatile_data[volatile_data.uid] = volatile_data

    def _get_by_uid(self, ref: UUID):
        ret = self._volatile_data.get(ref, None)
        if ret:
            return self._volatile_data[ref]
        raise EntityUIDNotFoundException(ref)

    def _get(self, **kwargs):
        qsize = kwargs.get("qsize", 10)
        ctype = kwargs.get("availability", None)

        ret = list()
        if ctype:
            for v in self._volatile_data.values():
                if v.availability == True:
                    ret.append(v)
                if len(ret) == qsize:
                    break

        return ret

    def __repr__(self):
        return str(self._volatile_data)


class ISQLAlchemyRepository(AbstractRepository, metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, session):
        raise NotImplemented

    @abstractmethod
    def _add(self, volatile_data: VolatileData):
        raise NotImplemented

    @abstractmethod
    def _get_by_uid(self, ref: UUID):
        raise NotImplemented

    @abstractmethod
    def _get(self, **kwargs):
        raise NotImplemented

    def __repr__(self):
        raise NotImplemented
