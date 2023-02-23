from time import time
from typing import List, Tuple

from framework.domain.value_object import URL, Money
from framework.domain.components import Component
from Scraper.domain.service import FactoryScraper
from Scraper.domain.aggragate import VolatileData
from framework.infrastructure.db_management.db_structure import VolatileDataInstance

seconds_between_requests = 1
urls: List[URL]
scraper_factory = FactoryScraper()


def convert_to_db_volatile_data(volatile_data: VolatileData) -> VolatileDataInstance:
    # TODO: converter objeto 'volatile_data' para intancia do banco de dados

    return VolatileDataInstance()


def store_volatile_data_on_db(volatile_data: VolatileData):
    db_volatile_data = convert_to_db_volatile_data(volatile_data)

    # TODO: armazenar o dado volátil no banco de dados


def store_volatile_datas_on_db(volatile_datas: List[VolatileData]):
    [store_volatile_data_on_db(volatile_data) for volatile_data in volatile_datas]


def run_scrapers():
    for url in urls:
        # TODO: implementar temporização randomizada em um intervalo de segundos
        scraper = scraper_factory.build_scraper(domain=url.url)
        current_url: URL = url
        volatile_data_values: List[Tuple[str, Money, bool]]

        while current_url != None:
            next_url, volatile_datas_values = scraper.get_volatile_data(current_url)

            for name, price, availability in volatile_datas_values:
                # TODO: fazer chamada da engine de busca para classificar o componente
                component: Component
                # component = SearchEngine.classificate(name)
                volatile_data: VolatileData
                # Volatile_data = VolatileData(component_id=component.uid, uid(current_url), current_url, cost, availability)
                # store_volatile_data_on_db(volatile_data)

            current_url = next_url
