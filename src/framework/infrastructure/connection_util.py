from typing import Callable, Dict, List, Type
from sqlalchemy.engine import Engine

from ..domain.events import DomainEvent, Command
from framework.infrastructure.db_management.db_connection import (
    create_new_engine,
    create_session,
)
from framework.infrastructure.db_management.db_creation import create_db
from framework.application.uow import AbstractDBUnitOfWork
from framework.application.handler import MessageBus

from config import db_username, db_password, db_address, db_port, db_name


def _get_engine() -> Engine:
    engine = create_new_engine(db_username, db_password, db_address, db_port, db_name)
    create_db(engine)
    return engine


def get_message_bus(
    event_mapper: Dict[Type[DomainEvent], List[Callable]],
    command_mapper: Dict[Type[Command], Callable],
    uow_cls: Type[AbstractDBUnitOfWork],
    engine=_get_engine(),
) -> MessageBus:
    uow = uow_cls(create_session(engine))

    event_handler_callables = {
        c: list(map(lambda han: han(uow), h)) for c, h in event_mapper.items()
    }

    command_handler_callables = {c: h(uow) for c, h in command_mapper.items()}

    return MessageBus(uow, event_handler_callables, command_handler_callables)
