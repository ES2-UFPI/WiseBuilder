from dataclasses import dataclass
from value_object import AbstractScraper
from framework.domain.value_object import URL, Money
from bs4 import BeautifulSoup
import requests as rq


@dataclass
class KabumScraper(AbstractScraper):
    raw_url = "https://www.kabum.com.br"

    def get_volatile_data(self, URL: str) -> Tuple[URL, str, Money, int]:
        html = rq.get(URL).content
        soup = BeautifulSoup(html, "html.parser")
        availability = [
            if element.string == "COMPRAR"
            for element in soup.select(
                "div.sc-6061e719-4.sc-6061e719-6.flAjw.gvThCo.availableFooterCard button"
            )
        ]

        prices = [
            Money(float(element.string))
            for element in soup.select("span.sc-3b515ca1-2.eqqhbT.priceCard")
        ]

        names = [
            element.string
            for element in soup.select(
                "span.sc-d99ca57-0.cpPIRA.sc-ff8a9791-16.dubjqF.nameCard"
            )
        ]

        links = [element["href"] for element in soup.select("a.sc-ff8a9791-10.htpbqG")]
        
        volatile_data = []
        for link, name, price, availability in zip(links, names, prices, availability):
            volatile_data.append(tuple(link, name, price, availability))


        return volatile_data
