from dataclasses import dataclass, field
from typing import Dict
from abc import ABCMeta, abstractmethod

from framework.domain.repository import AbstractUserRepository
from framework.domain.users import User
from framework.domain.value_object import UUID
from framework.domain.exception import DomainException


@dataclass
class EntityUIDNotFoundException(DomainException):
    entity_id: UUID
    _message: str = field(init=False)

    def __post_init__(self):
        self._message = f"{self.__class__.__name__}: "
        f"Usuário com UID {self.entity_id} não existe."


@dataclass
class EntityCollisionException(DomainException):
    email: str
    _message: str = field(init=False)

    def __post_init__(self):
        self._message = f"{self.__class__.__name__}: "
        f"Usuário com email {self.email} já existe."


@dataclass
class InvalidUserCredentialsException(DomainException):
    _message: str = field(init=False)

    def __post_init__(self):
        self._message = f"{self.__class__.__name__}: "
        f"Não existe um usuário com as credenciais informadas."


class IUsersSQLAlchemyRepository(AbstractUserRepository, metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, session):
        raise NotImplemented

    @abstractmethod
    def _add(self, user: User, password: str):
        raise NotImplemented

    @abstractmethod
    def _get_by_uid(self, ref: UUID):
        raise NotImplemented

    @abstractmethod
    def _get(self, **kwargs):
        raise NotImplemented

    def __repr__(self):
        raise NotImplemented
