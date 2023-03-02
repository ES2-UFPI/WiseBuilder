from framework.infrastructure.connection_util import get_message_bus
from ..application.handlers import SE_COMMAND_HANDLER_MAPPER, SE_EVENT_HANDLER_MAPPER

__all__ = ["se_message_bus"]

se_message_bus = get_message_bus(SE_EVENT_HANDLER_MAPPER, SE_COMMAND_HANDLER_MAPPER)
