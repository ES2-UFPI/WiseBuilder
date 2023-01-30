from typing import Dict, List, Union, Type, Callable, Any
from dataclasses import dataclass
from abc import ABC, abstractmethod

from .uow import AbstractUnitOfWork
from ..domain.events import DomainEvent, Command

__all__ = [ "Message", "MessageBus", "MessageHandler" ]

Message = Union[ Command, DomainEvent ]


@dataclass
class MessageBus:
    uow: AbstractUnitOfWork
    event_mapper: Dict[Type[DomainEvent], List[Callable]]
    command_mapper: Dict[Type[Command], Callable]
    
    def handle(self, message: Message) -> Any:
        self.queue = [message]
        while self.queue:
            message = self.queue.pop(0)
            if isinstance(message, DomainEvent):
                return self.handle_event(message)
            elif isinstance(message, Command):
                return self.handle_command(message)
            else:
                raise Exception(f"{message} de tipo {message.__class__} não é um evento ou comando.")
    
    
    def handle_event(self, event: DomainEvent) -> Any:
        for handler in self.event_mapper[type(event)]:
            try:
                retval = handler(event)
                self.queue.extend(self.uow.collect_messages())
                return retval
            except Exception:
                continue
    
    
    def handle_command(self, command: Command) -> Any:
        try:
            handler = self.command_mapper[type(command)]
            retval = handler(command)
            self.queue.extend(self.uow.collect_messages())
            return retval
        except Exception:
            raise


@dataclass
class MessageHandler(ABC):
    uow: AbstractUnitOfWork
    
    @abstractmethod
    def __call__(self, message: Message):
        raise NotImplementedError