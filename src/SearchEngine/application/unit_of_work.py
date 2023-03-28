from framework.application.uow import AbstractUnitOfWork, AbstractDBUnitOfWork

from ..domain.repositories import MockRepository
from ..infrastructure.ComponentManagment.SQL_alchemy_repository import (
    SQLAlchemyRepository,
)
from ..infrastructure.dataframe_repository import DataFrameRepository


class MockUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session):
        self.repository = MockRepository({})
        self.commited = False

    def commit(self):
        self.commited = True

    def rollback(self):
        pass


class SQLAlchemyUnitOfWork(AbstractDBUnitOfWork):
    def __init__(self, session):
        self.repository = SQLAlchemyRepository(session)
        self.commited = False

    def commit(self):
        self.commited = True

    def rollback(self):
        pass


class DataFrameUnitOfWork(AbstractDBUnitOfWork):
    def __init__(self, path):
        self.repository = DataFrameRepository(path)
        self.commited = False
    
    def commit(self):
        self.commited = True
    
    def rollback(self):
        pass