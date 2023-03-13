import sys, os

sys.path.insert(0, os.getcwd())

import csv

from framework.infrastructure.connection_util import get_message_bus
from Scraper.application.handlers import (
    CURL_COMMAND_HANDLER_MAPPER,
    CURL_EVENT_HANDLER_MAPPER,
)
from Scraper.application.unit_of_work import SQLAlchemyCategoryURLUnitOfWork
from Scraper.domain.value_object import URL
from framework.domain.components import EComponentType
from framework.domain.value_object import UUIDv5
from Scraper.domain.entity import CategoryURL
from Scraper.domain.commands import AddCategoryURL
from Scraper.domain.repositories import EntityUIDCollisionException

_csv_file_dir = r"C:\Users\wesle\OneDrive\Documentos\UFPI\ESII\WiseBuilder\res\data\raw\category_urls.csv"


def store_components_from_csv(csv_dir: str):
    category_url_message_bus = get_message_bus(
        CURL_EVENT_HANDLER_MAPPER,
        CURL_COMMAND_HANDLER_MAPPER,
        SQLAlchemyCategoryURLUnitOfWork,
    )

    with open(csv_dir, "r") as csv_file:
        reader = csv.reader(csv_file, skipinitialspace=True)

        for url, category_name in reader:
            category_url = CategoryURL(
                _id=UUIDv5(url),
                url=URL.get_URL(url),
                category=EComponentType[category_name],
            )

            try:
                category_url_message_bus.handle(AddCategoryURL(category_url))
            except EntityUIDCollisionException:
                print(f"url {url} já existe no banco de dados.")


def main():
    store_components_from_csv(_csv_file_dir)


if __name__ == "__main__":
    main()
