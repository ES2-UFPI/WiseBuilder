from time import time
from typing import List, Tuple

from framework.domain.value_object import UUID
from framework.domain.value_object import URL
from framework.domain.components import Component
from Scraper.domain.service import FactoryScraper
from Scraper.domain.aggragate import VolatileData
from Scraper.infrastructure.VolatileDataManagment.SQL_alchemy_volatile_data import (
    SQLAlchemyVolatile_data,
)

seconds_between_requests = 1
urls: List[URL] = [URL("www.google.com", "", "", "")]  # category
scraper_factory = FactoryScraper()


def run_scrapers(session):
    volatile_data_manager = SQLAlchemyVolatile_data(session)

    for category_url in urls:
        # TODO: implementar temporização randomizada em um intervalo de segundos
        scraper = scraper_factory.build_scraper(domain=category_url.url)
        page_url: URL = category_url

        while page_url != None:
            page_url, volatile_datas_values = scraper.get_volatile_data(page_url)

            for url, name, cost, availability in volatile_datas_values:
                # TODO: fazer chamada da engine de busca para classificar o componente
                # component = SearchEngine.classifie(name)

                component = Component(
                    _id=Component.next_id(), manufacturer="1", model="2"
                )  # placeholder

                volatile_data = VolatileData(
                    _id=UUID(url.url),
                    component_id=component.uid,
                    url=url,
                    cost=cost,
                    availability=availability,
                )

                volatile_data_manager.add(volatile_data)
