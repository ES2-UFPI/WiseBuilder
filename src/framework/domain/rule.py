from dataclasses import dataclass
from abc import ABC, abstractmethod

__all__ = [ "Rule", "BusinessRuleValidationException" ]

@dataclass(kw_only=True)
class Rule(ABC):
    '''Classe base para as regras de negócio do domínio.'''
    _message: str = 'Regra de negócio violada.'
    
    def get_message(self) -> str:
        return self._message
    
    @abstractmethod
    def is_broken(self) -> bool:
        pass
    
    def __str__(self):
        return f"{self.__class__.__name__}: {self._message}"


@dataclass
class BusinessRuleValidationException(Exception):
    rule: Rule
    
    def __repr__(self):
        return f"{self.__class__.__name__}: ({str(self.rule)})"


class BussinessAssertionExtension:
    @classmethod
    def check_rule(cls, rule: Rule):
        if rule.is_broken():
            raise BusinessRuleValidationException(rule)