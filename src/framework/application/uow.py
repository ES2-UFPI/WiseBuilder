from abc import ABC, abstractmethod

from ..domain.entity import AggregateRoot
from ..domain.repository import AbstractRepository

__all__ = ["AbstractUnitOfWork"]


class AbstractUnitOfWork(ABC):
    repository: AbstractRepository

    def __enter__(self) -> "AbstractUnitOfWork":
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            self.commit()
        else:
            self.rollback()

    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError

    def collect_messages(self):
        for root in self.repository.seen:
            if isinstance(root, AggregateRoot):
                while root.events:
                    yield root.events.pop(0)
