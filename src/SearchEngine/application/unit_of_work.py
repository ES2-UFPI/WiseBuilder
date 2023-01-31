from ...framework.application.uow import AbstractUnitOfWork

from ..domain.repositories import MockRepository

class MockUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session):
        self.repository = MockRepository(session)
        self.commited = False
    
    
    def commit(self):
        self.commited = True
    
    
    def rollback(self):
        pass