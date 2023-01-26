from dataclasses import dataclass, field
from .value_object import AbstractScraper
from typing import Dict, Union, NoReturn


@dataclass
class FactoryScraper:
    _scrapers: Dict[str, AbstractScraper] = field(init=False, default_factory=dict)

    def build_scraper(self, domain: str) -> Union[AbstractScraper, NoReturn]:
        _scraper: AbstractScraper | None = self._scrapers.get(domain)
        if _scraper is None:
            raise ScraperNotFoundException()
        else:
            return _scraper

class ScraperNotFoundException(Exception):
    def __init__(self) -> None:
        super().__init__("Scraper não encontrado.")



