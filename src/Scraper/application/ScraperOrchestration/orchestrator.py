import asyncio
import sys, os

sys.path.insert(0, os.getcwd())

from Scraper.application.ScraperOrchestration.category_URL_manager import (
    CategoryURLManager,
)
from framework.infrastructure.db_management.db_connection import create_session
from framework.infrastructure.connection_util import _get_engine
from Scraper.application.ScraperOrchestration.Wrapper import Wrapper


engine = _get_engine()
_category_url_manager = CategoryURLManager(create_session(engine))
_sleep_minutes = 60


async def run_scrapers():
    while True:
        urls = _category_url_manager.get_urls()

        tasks = []

        for scheme, domain in urls:
            wrapper = Wrapper(scheme, domain)
            tasks.append(wrapper.run_scraping())

        await asyncio.gather(*tasks)
        await asyncio.sleep(_sleep_minutes * 60)


def main():
    orchestrator_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(orchestrator_loop)
    orchestrator_loop.run_until_complete(run_scrapers())
    orchestrator_loop.close()


if __name__ == "__main__":
    main()
