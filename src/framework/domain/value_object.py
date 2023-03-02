import uuid
from functools import partial
from urllib.parse import urlsplit, SplitResult
from dataclasses import dataclass
from functools import total_ordering
from typing import Tuple

from .rule import Rule, BussinessAssertionExtension

__all__ = ["UUID", "UUIDv4", "UUIDv5", "ValueObject", "Money", "URL"]

UUID = uuid.UUID
UUIDv4 = uuid.uuid4
UUIDv5 = partial(uuid.uuid5, uuid.NAMESPACE_URL)


class ValueObject(BussinessAssertionExtension):
    """
    Classe base de objetos valorados.
    """


@total_ordering
@dataclass(frozen=True, eq=False)
class Money(ValueObject):
    amount: float = 0
    currency: str = "BRL"

    def __eq__(self, oMoney: "Money") -> bool:
        return self.currency == oMoney.currency and self.amount == oMoney.amount

    def __lt__(self, oMoney: "Money") -> bool:
        return self.currency == oMoney.currency and self.amount < oMoney.amount

    def __repr__(self):
        return f"{self.currency} {self.amount:.2f}"


@dataclass(frozen=True)
class URL(ValueObject):
    """
    Classe de URL.
    """

    url: str
    scheme: str
    domain: str
    path: str

    @classmethod
    def get_URL(cls, url: str) -> "URL":
        parsed_url = urlsplit(url)

        cls.check_rule(MinimalURLRule(parsed_url=parsed_url))

        return URL(url, parsed_url.scheme, parsed_url.netloc, parsed_url.path)

    def __repr__(self) -> str:
        return self.url


@dataclass
class MinimalURLRule(Rule):
    """
    URL deve incluir, no mínimo, scheme and netloc.
    """

    parsed_url: SplitResult
    _min_attributes: Tuple[str, ...] = ("scheme", "netloc")

    def __post_init__(self):
        self._message: str = "URL não possui atributos mínimos."

    def is_broken(self):
        return not all(
            [getattr(self.parsed_url, attr) for attr in self._min_attributes]
        )
