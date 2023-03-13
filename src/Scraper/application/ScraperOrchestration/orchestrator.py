import asyncio
import sys, os

sys.path.insert(0, os.getcwd())

from framework.infrastructure.connection_util import get_message_bus
from Scraper.application.unit_of_work import SQLAlchemyCategoryURLUnitOfWork
from Scraper.application.handlers import (
    CURL_COMMAND_HANDLER_MAPPER,
    CURL_EVENT_HANDLER_MAPPER,
)
from Scraper.domain.service import ScraperNotFoundException
from Scraper.application.unit_of_work import (
    SQLAlchemyCategoryURLUnitOfWork,
)
from Scraper.domain.commands import GetAllDomains
from framework.infrastructure.connection_util import get_message_bus
from Scraper.application.ScraperOrchestration.wrapper import Wrapper

_category_url_message_bus = get_message_bus(
    CURL_EVENT_HANDLER_MAPPER,
    CURL_COMMAND_HANDLER_MAPPER,
    SQLAlchemyCategoryURLUnitOfWork,
)
_sleep_minutes = 60


async def run_scrapers():
    while True:
        urls = _category_url_message_bus.handle(GetAllDomains())

        tasks = []

        for scheme, domain in urls:
            try:
                wrapper = Wrapper(scheme, domain)
                tasks.append(wrapper.run_scraping())
            except ScraperNotFoundException:
                print(f"Scraper não encontrado para o domínio {domain}.")

        await asyncio.gather(*tasks)
        await asyncio.sleep(_sleep_minutes * 60)


def main():
    orchestrator_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(orchestrator_loop)
    orchestrator_loop.run_until_complete(run_scrapers())
    orchestrator_loop.close()


if __name__ == "__main__":
    main()
