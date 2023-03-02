import sys

sys.path.insert(0, r"C:\Users\wesle\OneDrive\Documentos\UFPI\ESII\WiseBuilder\src")

import asyncio
from Scraper.infrastructure.ScraperOrchestration.category_URL_manager import (
    CategoryURLManager,
)
from framework.infrastructure.db_management.db_connection import create_session
from entrypoints.api.endpoints.connection_util import engine
from Scraper.infrastructure.ScraperOrchestration.Wrapper import Wrapper

_category_url_manager = CategoryURLManager(create_session(engine))
_sleep_minutes = 0.1


async def run_scrapers():
    while True:
        domains = _category_url_manager.get_domains()

        tasks = []

        for domain in domains:
            wrapper = Wrapper(domain)
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
