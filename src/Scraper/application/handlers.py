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
from ..domain.repositories import ICategoryURLRepository
from ..domain.events import LowerPriceRegisteredEvent
from framework.domain.events import DomainEvent
from ..domain.commands import *


# Provisório. Mover para microsserviço de usuários.
class LowerPriceRegisteredHandler(MessageHandler):
    def __call__(self, event: LowerPriceRegisteredEvent):
        sender, passwd = mail, mail_passwd
        recv_list = [sender]

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

        print("email sended")


class AddCategoryURLHandler(MessageHandler):
    def __call__(self, cmd: AddCategoryURL):
        with self.uow:
            self.uow.repository.add(cmd.category_url)


class GetAllDomainsHandler(MessageHandler):
    def __call__(self, cmd: GetAllDomains):
        with self.uow:
            if isinstance(self.uow.repository, ICategoryURLRepository):
                return self.uow.repository.get_all_domains()


class AddVolatileDataHandler(MessageHandler):
    def __call__(self, cmd: AddVolatileData):
        with self.uow:
            self.uow.repository.add(cmd.volatile_data)


class GetVolatileDataByDomainHandler(MessageHandler):
    def __call__(self, cmd: GetCategoryURLByDomain):
        with self.uow:
            return self.uow.repository.get(filters_eq={"domain": cmd.domain})


class GetVolatileDataByMaxCostHandler(MessageHandler):
    def __call__(self, cmd: GetVolatileDataByMaxCost):
        with self.uow:
            return self.uow.repository.get(filters_lt={"cost": cmd.cost})


class GetVolatileDataByComponentUIDHandler(MessageHandler):
    def __call__(self, cmd: GetVolatileDataByComponentUID):
        with self.uow:
            return self.uow.repository.get(
                filters_eq={"component_uid": cmd.component_uid}
            )


CURL_COMMAND_HANDLER_MAPPER: Dict[Type[Command], Type[MessageHandler]] = {
    AddCategoryURL: AddCategoryURLHandler,
    GetCategoryURLByDomain: GetVolatileDataByDomainHandler,
    GetAllDomains: GetAllDomainsHandler,
}

CURL_EVENT_HANDLER_MAPPER: Dict[Type[DomainEvent], List[Type[MessageHandler]]] = {}

VD_COMMAND_HANDLER_MAPPER: Dict[Type[Command], Type[MessageHandler]] = {
    AddVolatileData: AddVolatileDataHandler,
    GetVolatileDataByMaxCost: GetVolatileDataByMaxCostHandler,
    GetVolatileDataByComponentUID: GetVolatileDataByComponentUIDHandler,
}

VD_EVENT_HANDLER_MAPPER: Dict[Type[DomainEvent], List[Type[MessageHandler]]] = {
    LowerPriceRegisteredEvent: [
        LowerPriceRegisteredHandler,
    ]
}
