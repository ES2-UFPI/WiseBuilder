from typing import Type, Dict, List
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
from framework.domain.events import Command, DomainEvent
from framework.application.handler import MessageHandler
from Scraper.domain.aggragate import VolatileData
from ..domain.repositories import ICategoryURLRepository, IVolatileDataRepository
from ..domain.events import LowerPriceRegisteredEvent
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


class GetLowerCostVolatileDatasHandler(MessageHandler):
    def __call__(self, cmd: GetLowerCostVolatileDatas):
        with self.uow:
            cost_filter = {} if cmd.cost >= 0 else {"filters_lt": {"cost": cmd.cost}}
            if isinstance(self.uow.repository, IVolatileDataRepository):
                return self.uow.repository.get_lower_costs(**cost_filter)


class GetVolatileDataByComponentUIDHandler(MessageHandler):
    def __call__(self, cmd: GetVolatileDataByComponentUID):
        with self.uow:
            return self.uow.repository.get(
                filters_eq={"component_uid": cmd.component_uid}
            )


def _get_components_from_volatile_data(volatile_data: list[VolatileData]):
    message_bus = get_message_bus(
        SE_EVENT_HANDLER_MAPPER, SE_COMMAND_HANDLER_MAPPER, SQLAlchemyUnitOfWork
    )

    components = [
        message_bus.handle(GetComponentByUID(vd.component_id)) for vd in volatile_data
    ]

    return components


class GetComponentsFromVolatileDataHandler(MessageHandler):
    def __call__(self, cmd: GetComponentsFromVolatileData):
        with self.uow:
            return _get_components_from_volatile_data(cmd.volatile_data)


class GetVolatileDataByCostIntervalHandler(MessageHandler):
    def __call__(self, cmd: GetVolatileDataByCostInterval):
        with self.uow:
            filters_lt = {"cost": cmd.max_cost}
            filters_gt = {"cost": cmd.min_cost}
            filters_eq = {"component_type": cmd.component_type}

            volatile_data: list = self.uow.repository.get_lower_costs(
                filters_eq=filters_eq,
                filters_lt=filters_lt,
                filters_gt=filters_gt,
            )

            components = _get_components_from_volatile_data(volatile_data)

            for i, component in enumerate(components):
                if component.rank is None:
                    del volatile_data[i]
                    del components[i]

            return components, volatile_data


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
    GetLowerCostVolatileDatas: GetLowerCostVolatileDatasHandler,
    GetComponentsFromVolatileData: GetComponentsFromVolatileDataHandler,
    GetVolatileDataByCostInterval: GetVolatileDataByCostIntervalHandler,
}

VD_EVENT_HANDLER_MAPPER: Dict[Type[DomainEvent], List[Type[MessageHandler]]] = {
    LowerPriceRegisteredEvent: [
        LowerPriceRegisteredHandler,
    ]
}
