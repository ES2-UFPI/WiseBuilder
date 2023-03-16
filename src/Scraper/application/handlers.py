from typing import Dict, Type, List
from smtplib import SMTP
from ssl import create_default_context
from email.mime.text import MIMEText
from config import mail, mail_passwd

from framework.infrastructure.connection_util import get_message_bus
from SearchEngine.domain.commands import GetComponentByUID
from SearchEngine.application.handlers import (
    SE_COMMAND_HANDLER_MAPPER,
    SE_EVENT_HANDLER_MAPPER,
)
from SearchEngine.application.unit_of_work import SQLAlchemyUnitOfWork
from framework.domain.components import Component
from framework.application.handler import MessageHandler, Command
from ..domain.events import LowerPriceRegisteredEvent
from framework.domain.events import DomainEvent
from ..domain.commands import *


# Provisório. Mover para microsserviço de usuários.
class LowerPriceRegisteredHandler(MessageHandler):
    def __call__(self, event: LowerPriceRegisteredEvent):
        sender, passwd = mail, mail_passwd
        recv_list = ['wesleyvitor37417@gmail.com']

        message_bus = get_message_bus(
            SE_EVENT_HANDLER_MAPPER, SE_COMMAND_HANDLER_MAPPER, SQLAlchemyUnitOfWork
        )

        component: Component = message_bus.handle(
            GetComponentByUID(event.component_uid)
        )

        msg = f"Produto com preço reduzido!" f"{component}" f"{event.price}"

        message = MIMEText(msg, "plain")

        message[
            "Subject"
        ] = f"Preço reduzido: {component.manufacturer} {component.model}!"
        message["From"] = sender
        context = create_default_context()
        with SMTP("smtp.gmail.com", 587) as server:
            server.starttls(context=context)
            server.login(sender, passwd)
            server.send_message(message, sender, recv_list)
        


class AddCategoryURLHandler(MessageHandler):
    def __call__(self, cmd: AddCategoryURL):
        with self.uow:
            self.uow.repository.add(cmd.category_url)


class GetAllDomainsHandler(MessageHandler):
    def __call__(self, cmd: GetAllDomains):
        with self.uow:
            return self.uow.repository.get_all_domains()


class GetVolatileDataByDomainHandler(MessageHandler):
    def __call__(self, cmd: GetCategoryURLByDomain):
        with self.uow:
            return self.uow.repository.get(filters_eq={"domain": cmd.domain})


class AddVolatileDataHandler(MessageHandler):
    def __call__(self, cmd: AddVolatileData):
        with self.uow:
            self.uow.repository.add(cmd.volatile_data)


CURL_COMMAND_HANDLER_MAPPER: Dict[Type[Command], Type[MessageHandler]] = {
    AddCategoryURL: AddCategoryURLHandler,
    GetCategoryURLByDomain: GetVolatileDataByDomainHandler,
    GetAllDomains: GetAllDomainsHandler,
}

CURL_EVENT_HANDLER_MAPPER: Dict[Type[DomainEvent], List[Type[MessageHandler]]] = {}

VD_COMMAND_HANDLER_MAPPER: Dict[Type[Command], Type[MessageHandler]] = {
    AddVolatileData: AddVolatileDataHandler
}

VD_EVENT_HANDLER_MAPPER: Dict[Type[DomainEvent], List[Type[MessageHandler]]] = {
    LowerPriceRegisteredEvent: [
        LowerPriceRegisteredHandler,
    ]
}
