from dataclasses import dataclass
from typing import Type

from ...framework.domain.components import Component, EComponentType, component_cls_idx

from ...framework.domain.value_object import UUID, UUIDv4
from ...framework.domain.events import Command

__all__ = [ 'GetComponentByUID', 'ListComponentsByType', 'AddComponent' ]

@dataclass
class GetComponentByUID(Command):
    uid: UUID


@dataclass
class ListComponentsByType(Command):
    type: EComponentType
    
    @classmethod
    def Motherboard(cls):
        return ListComponentsByType(EComponentType.MOTHERBOARD)
    
    
    @classmethod
    def CPU(cls):
        return ListComponentsByType(EComponentType.CPU)
    
    
    @classmethod
    def GPU(cls):
        return ListComponentsByType(EComponentType.GPU)
    
    
    @classmethod
    def RAM(cls):
        return ListComponentsByType(EComponentType.RAM)
    
    
    @classmethod
    def Persistence(cls):
        return ListComponentsByType(EComponentType.PERSISTENCE)
    
    
    @classmethod
    def PSU(cls):
        return ListComponentsByType(EComponentType.PSU)


class AddComponent(Command):
    component: Component
    
    def __init__(self, component: Component):
        self.component = component
    
    
    @classmethod
    def _from_kwargs(cls, type, specs_dict):
        # Comparar com a base?
        specs_dict['_id'] = UUIDv4()
        built = component_cls_idx[type](**specs_dict)
        return AddComponent(built)
    
    @classmethod
    def buildMotherboard(cls, **kwargs):
        return cls._from_kwargs(EComponentType.MOTHERBOARD, kwargs)
    
     
    @classmethod
    def buildCPU(cls, **kwargs):
        return cls._from_kwargs(EComponentType.CPU, kwargs)
    
     
    @classmethod
    def buildGPU(cls, **kwargs):
        return cls._from_kwargs(EComponentType.GPU, kwargs)
    
     
    @classmethod
    def buildRAM(cls, **kwargs):
        return cls._from_kwargs(EComponentType.RAM, kwargs)
    
     
    @classmethod
    def buildPersistence(cls, **kwargs):
        return cls._from_kwargs(EComponentType.PERSISTENCE, kwargs)
    
     
    @classmethod
    def buildPSU(cls, **kwargs):
        return cls._from_kwargs(EComponentType.PSU, kwargs)
    