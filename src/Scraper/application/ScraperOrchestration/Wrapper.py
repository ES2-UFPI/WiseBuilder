from sqlalchemy.orm.session import Session
from typing import List
from random import uniform
import asyncio

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
from Scraper.infrastructure.VolatileDataManagment.SQL_alchemy_volatile_data import (
    SQLAlchemyVolatileData,
)
from Scraper.application.ScraperOrchestration.category_URL_manager import (
    CategoryURLManager,
)


engine = _get_engine()


class Wrapper:
    _volatile_data_manager: SQLAlchemyVolatileData
    domain: str
    scraper: AbstractScraper
    domain_urls: List[CategoryURL]
    session: Session

    max_sleep_seconds = 3

    def __init__(self, scheme: str, domain: str):
        self.domain = domain
        self.session = create_session(engine)
        self._volatile_data_manager = SQLAlchemyVolatileData(self.session)

        factory_scraper = FactoryScraper()
        url_manager = CategoryURLManager(self.session)
        self.scraper = factory_scraper.build_scraper(f"{scheme}://{domain}")
        self.domain_urls = url_manager.get(filters_eq={"domain": domain})

    async def run_scraping(self):
        for domain_url in self.domain_urls:
            next_url: URL = domain_url.url

            while next_url != None:
                next_url, volatile_datas = self.scraper.get_volatile_data(
                    url=next_url.url
                )

                for url, name, cost, availability in volatile_datas:
                    # TODO: fazer chamada da engine de busca para classificar o componente
                    # component = SearchEngine.classifie(name)
                    component_manager = SQLAlchemyRepository(
                        self.session
                    )  # placeholder
                    component = component_manager.get(filters_gt={"consumption": -1})[
                        0
                    ]  # placeholder

                    volatile_data = VolatileData(
                        _id=UUIDv5(url.url),
                        component_id=component.uid,
                        url=url,
                        cost=cost,
                        availability=availability,
                    )

                    self._volatile_data_manager.add(volatile_data)

                sleep_seconds = uniform(1.0, self.max_sleep_seconds)
                await asyncio.sleep(sleep_seconds)
