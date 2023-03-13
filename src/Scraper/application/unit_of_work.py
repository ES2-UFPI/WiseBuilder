from framework.application.uow import AbstractDBUnitOfWork, AbstractUnitOfWork

from ..domain.repositories import MockRepository
from ..infrastructure.SQL_alchemy_category_url import SQLAlchemyCategoryURL
from ..infrastructure.SQL_alchemy_volatile_data import SQLAlchemyVolatileData


class MockUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session):
        self.repository = MockRepository({})
        self.commited = False

    def commit(self):
        self.commited = True

    def rollback(self):
        pass


class SQLAlchemyVolatileDataUnitOfWork(AbstractDBUnitOfWork):
    def __init__(self, session):
        self.repository = SQLAlchemyVolatileData(session)
        self.commited = False

    def commit(self):
        self.commited = True

    def rollback(self):
        pass


class SQLAlchemyCategoryURLUnitOfWork(AbstractDBUnitOfWork):
    def __init__(self, session):
        self.repository = SQLAlchemyCategoryURL(session)
        self.commited = False

    def commit(self):
        self.commited = True

    def rollback(self):
        pass
