from dataclasses import dataclass

from ...framework.domain.exception import DomainException


@dataclass
class KnapsackBurst(DomainException):
    _message: str = "A bolsa atingiu o limite de preço."
