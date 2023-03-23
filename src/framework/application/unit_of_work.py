from framework.application.uow import AbstractDBUnitOfWork, AbstractUnitOfWork

from ..infrastructure.SQL_alchemy_users import SQLAlchemyUser


class SQLAlchemyUserUnitOfWork(AbstractDBUnitOfWork):
    def __init__(self, session):
        self.repository = SQLAlchemyUser(session)
        self.commited = False

    def commit(self):
        self.commited = True

    def rollback(self):
        pass
