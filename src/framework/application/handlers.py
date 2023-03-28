from typing import Dict, Type, List

from ..domain.commands import *

from framework.domain.repositories import (
    IUsersSQLAlchemyRepository,
    InvalidUserCredentialsException,
)
from framework.domain.events import Command, DomainEvent
from framework.application.handler import MessageHandler


class AddUserHandler(MessageHandler):
    def __call__(self, cmd: AddUser):
        with self.uow:
            if isinstance(self.uow.repository, IUsersSQLAlchemyRepository):
                self.uow.repository.add(cmd.user, cmd.password)


class GetUserByUIDHandler(MessageHandler):
    def __call__(self, cmd: GetUserByUID):
        with self.uow:
            return self.uow.repository.get_by_uid(cmd.uid)


class GetUserByCredentialsHandler(MessageHandler):
    def __call__(self, cmd: GetUserByCredentials):
        with self.uow:
            user = self.uow.repository.get(email=cmd.email, password=cmd.password)

            if len(user) == 1:
                return user[0]

            raise InvalidUserCredentialsException()


USER_COMMAND_HANDLER_MAPPER: Dict[Type[Command], Type[MessageHandler]] = {
    AddUser: AddUserHandler,
    GetUserByUID: GetUserByUIDHandler,
    GetUserByCredentials: GetUserByCredentialsHandler,
}

USER_EVENT_HANDLER_MAPPER: Dict[Type[DomainEvent], List[Type[MessageHandler]]] = {}
