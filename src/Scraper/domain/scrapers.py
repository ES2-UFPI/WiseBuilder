from dataclasses import dataclass, field
from Scraper.domain.value_object  import AbstractScraper
from framework.domain.value_object import URL, Money
from bs4 import BeautifulSoup
import requests as rq


@dataclass
class KabumScraper(AbstractScraper):
    raw_url: str = field(default="https://www.kabum.com.br", init=False)
    query_string: str = field(
        default="?page_number={page_number}&page_size=100&facet_filters=&sort=most_searched",
        init=False,
    )

    def get_volatile_data(
        self, url: str
    ) -> tuple[URL | None, list[tuple[URL, str, Money, int]]]:
        headers = {
            "User-Agent": "Mozilla/5.0",
        }
        html = rq.get(url, headers=headers).content
        soup = BeautifulSoup(html, "html.parser")

        prices = [
            Money(
                float(
                    element.string.split("\u00A0")[-1]
                    .replace(".", "")
                    .replace(",", ".")
                )
            )
            if not element.string.split("\u00A0")[-1] == "---"
            else Money(-1)
            for element in soup.select("span.sc-3b515ca1-2")
        ]

        availability = [
            False if element.string.split("\u00A0")[-1] == "---" else True
            for element in soup.select("span.sc-3b515ca1-2")
        ]

        names = [
            element.string
            for element in soup.select(
                "span.sc-d99ca57-0.cpPIRA.sc-ff8a9791-16.dubjqF.nameCard"
            )
        ]

        links = [
            URL.get_URL(str(self.raw_url + element["href"]))
            for element in soup.select("a.sc-ff8a9791-10.htpbqG")
        ]

        volatile_data = []
        for link, name, price, availability in zip(links, names, prices, availability):
            volatile_data.append(tuple([link, name, price, availability]))

        number_of_pages = [int(element.string) for element in soup.select("a.page")]

        n_actual_page = int(soup.select_one("a.page.active").string)

        n_next_page = n_actual_page + 1

        if n_next_page in number_of_pages:
            next_page = url.split("?")[0] + self.query_string.format(
                page_number=n_next_page
            )
        else:
            next_page = None

        return next_page, volatile_data
