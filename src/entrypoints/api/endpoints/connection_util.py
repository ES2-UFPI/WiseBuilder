from framework.infrastructure.db_management.db_connection import create_new_engine, create_session
from framework.infrastructure.db_management.db_creation import create_db
from SearchEngine.application.unit_of_work import MockUnitOfWork
from framework.application.handler import MessageBus
from SearchEngine.application.handlers import COMMAND_HANDLER_MAPPER

def _message_bus(engine):
    
    uow = MockUnitOfWork(create_session(engine))
    COMMAND_HANDLER_MAPPER_CALLABLE = {}
    for c, h in COMMAND_HANDLER_MAPPER.items():
        COMMAND_HANDLER_MAPPER_CALLABLE[c] = h(uow)
    
    return MessageBus(uow, {}, COMMAND_HANDLER_MAPPER_CALLABLE)

engine = create_new_engine()
create_db(engine)
message_bus = _message_bus(engine)