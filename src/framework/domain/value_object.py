from dataclasses import dataclass, field
from typing import Tuple, NoReturn
from urllib.parse import ParseResult, urlparse
from exception import InvalidUrlException
import uuid

UUID = uuid.UUID
UUID.v4 = uuid.uuid4


class ValueObject:
    pass


@dataclass
class Url(ValueObject):
    url: str
    domain: str = field(init=False)
    path: str = field(init=False)
    _min_attributes: Tuple[str, str] = field(
        init=False, repr=False, default_factory=lambda: ("scheme", "netloc")
    )

    def __post_init__(self) -> None | NoReturn:
        token: ParseResult = urlparse(self.url)
        if all([getattr(token, attr) for attr in self._min_attributes]):
            raise InvalidUrlException()
        else:
            self.domain = token.netloc
            self.path = token.path
