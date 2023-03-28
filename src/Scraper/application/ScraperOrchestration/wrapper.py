from sqlalchemy.orm.session import Session
from typing import List
from random import uniform
import asyncio

from framework.infrastructure.connection_util import get_message_bus
from Scraper.application.handlers import (
    VD_EVENT_HANDLER_MAPPER,
    VD_COMMAND_HANDLER_MAPPER,
    CURL_COMMAND_HANDLER_MAPPER,
    CURL_EVENT_HANDLER_MAPPER,
)
from Scraper.application.unit_of_work import (
    SQLAlchemyVolatileDataUnitOfWork,
    SQLAlchemyCategoryURLUnitOfWork,
)
from SearchEngine.infrastructure.ComponentManagment.SQL_alchemy_repository import (
    SQLAlchemyRepository,
)
from Scraper.domain.value_object import AbstractScraper, URL
from Scraper.domain.entity import CategoryURL
from Scraper.domain.aggragate import VolatileData
from Scraper.domain.service import FactoryScraper
from framework.domain.value_object import UUIDv5
from framework.infrastructure.connection_util import _get_engine
from framework.infrastructure.db_management.db_connection import create_session
from Scraper.domain.commands import *
from framework.domain.components import Component
from framework.application.handler import MessageBus
from SearchEngine.application.handlers import SE_COMMAND_HANDLER_MAPPER
from SearchEngine.application.unit_of_work import (
    DataFrameUnitOfWork,
    SQLAlchemyUnitOfWork,
)
from SearchEngine.domain.commands import GetComponentByUID, MatchName


class Wrapper:
    _volatile_data_message_bus: MessageBus
    domain: str
    scraper: AbstractScraper
    domain_urls: List[CategoryURL]
    session: Session

    max_sleep_seconds = 3

    def __init__(self, scheme: str, domain: str):
        engine = _get_engine()
        self.domain = domain
        self.session = create_session(engine)

        self._volatile_data_message_bus = get_message_bus(
            VD_EVENT_HANDLER_MAPPER,
            VD_COMMAND_HANDLER_MAPPER,
            SQLAlchemyVolatileDataUnitOfWork,
        )

        self._category_url_message_bus = get_message_bus(
            CURL_EVENT_HANDLER_MAPPER,
            CURL_COMMAND_HANDLER_MAPPER,
            SQLAlchemyCategoryURLUnitOfWork,
        )

        self._sse_message_bus = get_message_bus(
            {}, SE_COMMAND_HANDLER_MAPPER, DataFrameUnitOfWork, "../res/data/run"
        )

        self._search_message_bus = get_message_bus(
            {}, SE_COMMAND_HANDLER_MAPPER, SQLAlchemyUnitOfWork
        )

        self.domain_urls = self._category_url_message_bus.handle(
            GetCategoryURLByDomain(domain)
        )

        factory_scraper = FactoryScraper()
        self.scraper = factory_scraper.build_scraper(f"{scheme}://{domain}")

    async def run_scraping(self):
        for domain_url in self.domain_urls:
            next_url: URL = domain_url.url

            while next_url != None:
                next_url, components_volatile_data = self.scraper.get_volatile_data(
                    url=next_url.url
                )

                for url, name, cost, availability in components_volatile_data:
                    # TODO: fazer chamada da engine de busca para classificar o componente
                    # component = SearchEngine.classifie(name)
                    component_id = self._sse_message_bus.handle(MatchName(name))
                    component = self._search_message_bus.handle(
                        GetComponentByUID(component_id)
                    )
                    volatile_data = VolatileData(
                        _id=UUIDv5(url.url),
                        component_id=component.uid,
                        component_type=component.type,
                        url=url,
                        cost=cost,
                        availability=availability,
                    )
                    self._volatile_data_message_bus.handle(
                        AddVolatileData(volatile_data)
                    )

                sleep_seconds = uniform(1.0, self.max_sleep_seconds)
                await asyncio.sleep(sleep_seconds)
