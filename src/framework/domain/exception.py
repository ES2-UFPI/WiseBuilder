from dataclasses import dataclass

__all__ = ["DomainException"]


@dataclass
class DomainException(Exception):
    _message: str

    def __repr__(self):
        return f"{self.__class__.__name__}: {self._message}"


@dataclass
class CurrencyNotEqual(DomainException):
    _message: str = "As moedas são diferentes"
