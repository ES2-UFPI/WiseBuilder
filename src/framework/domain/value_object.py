import uuid
from urllib.parse import urlsplit, SplitResult
from dataclasses import dataclass, field
from typing import Tuple

from .rule import Rule, BusinessRuleValidationException

UUID = uuid.UUID
UUID.v4 = uuid.uuid4

class ValueObject:
    """
    Classe base de objetos valorados.
    """
    def check_rule(self, rule: Rule):
        if rule.is_broken():
            raise BusinessRuleValidationException(rule)


@dataclass(frozen=True)
class Money(ValueObject):
    amount: float = 0
    currency: str = "BRL"
    
    def __repr__(self):
        return f"{self.currency} {self.amount:.2f}"


@dataclass(frozen=True)
class URL(ValueObject):
    """
    Classe de URL.
    """
    url: str
    domain: str = field(init=False)
    path: str = field(init=False)
    
    def __post_init__(self, url: str):
        parsed_url = urlsplit(url)
        
        self.check_rule(MinimalURLRule(parsed_url))
        
        self.domain = parsed_url.netloc
        self.path = parsed_url.path


@dataclass
class MinimalURLRule(Rule):
    '''
    URL must include, at least, scheme and netloc.
    '''
    parsed_url: SplitResult
    _min_attributes: Tuple[str,...] = ("scheme", "netloc")
    __message: str = "URL não possui atributos mínimos."
    
    def is_broken(self):
        return all([getattr(self.parsed_url, attr) 
                    for attr in self._min_attributes])