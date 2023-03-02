from framework.application.uow import AbstractUnitOfWork

from ..domain.repositories import MockRepository
from ..infrastructure.ComponentManagment.SQL_alchemy_repository import (
    SQLAlchemyRepository,
)


class MockUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session):
        self.repository = SQLAlchemyRepository(session)
        self.commited = False

    def commit(self):
        self.commited = True

    def rollback(self):
        pass
