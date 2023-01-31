from dataclasses import dataclass, field
from typing import Any, Dict
from abc import ABCMeta, abstractmethod

from ...framework.domain.value_object import UUID
from ...framework.domain.repository import AbstractRepository
from ...framework.domain.exception import DomainException
from ...framework.domain.components import Component, EComponentType

@dataclass
class EntityUIDNotFoundException(DomainException):
    entity_id: UUID
    _message: str = field(init=False)
    
    def __post_init__(self):
        self._message = f"{self.__class__.__name__}: "
        f"Componente com UID {self.entity_id} não existe."


@dataclass
class EntityUIDCollisionException(DomainException):
    entity_id: UUID
    _message: str = field(init=False)
    
    def __post_init__(self):
        self._message = f"{self.__class__.__name__}: "
        f"Componente com UID {self.entity_id} já existe."


class MockRepository(AbstractRepository):
    def __init__(self, components: Dict[UUID, Component]):
        self._components = components
    
    
    def _add(self, component: Component):
        if self._components.get(component.uid, None) is None:
            self._components[component.uid] = component
        else: 
            raise EntityUIDCollisionException(component.uid)
    
    
    def _get_by_uid(self, ref: UUID):
        ret = self._components.get(ref, None)
        if ret:
            return self._components[ref]
        raise EntityUIDNotFoundException(ref)
    
    
    def _get(self, **kwargs):
        qsize = kwargs.get('qsize', 10)
        ctype = kwargs.get('ctype', None)
        
        ret = list()
        if ctype:
            for c in self._components.values():
                if c.type == ctype:
                    ret.append(c)
                if len(ret) == qsize:
                    break
        
        return ret
    
    
    def __repr__(self):
        return str(self._components)
