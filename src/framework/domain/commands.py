from framework.domain.events import Command
from dataclasses import dataclass

from ..domain.users import User
from framework.domain.value_object import UUID, UUIDv4

__all__ = [
    "AddUser",
    "GetUserByUID",
    "GetUserByCredentials",
]


@dataclass
class AddUser(Command):
    user: User
    password: str


@dataclass
class GetUserByUID(Command):
    uid: UUID


@dataclass
class GetUserByCredentials(Command):
    email: str
    password: str
