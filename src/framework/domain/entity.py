from dataclasses import dataclass, field

from .value_object import UUID
from .rule import Rule, BusinessRuleValidationException

@dataclass
class Entity:
    id_: UUID = field(hash=True)
    
    @property
    def id_(self):
        return self.id_
    
    
    @classmethod
    def next_id(cls) -> UUID:
        return UUID.v4()
    
    
    def check_rule(self, rule: Rule):
        if rule.is_broken():
            raise BusinessRuleValidationException(rule)


@dataclass
class EntityNotFoundException(Exception):
    entity_id: UUID
    
    def __repr__(self):
        return f"{self.__class__.__name__} (Entity {self.entity_id} not found.)"