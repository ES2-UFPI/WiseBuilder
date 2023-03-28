from dataclasses import dataclass
from Scraper.domain.value_object import AbstractScraper
from framework.domain.value_object import URL, Money
from bs4 import BeautifulSoup
from requests import get


@dataclass(init=False)
class KabumScraper(AbstractScraper):
    raw_url: str = "https://www.kabum.com.br"
    query_string: str = (
        "?page_number={page_number}&page_size=100&facet_filters=&sort=most_searched"
    )

    def get_volatile_data(
        self, url: str
    ) -> tuple[URL | None, list[tuple[URL, str, Money, bool]]]:
        headers = {
            "User-Agent": "Mozilla/5.0",
        }

        html = get(url, headers=headers).content

        soup = BeautifulSoup(html, "html.parser")

        links: list[URL] = [
            URL.get_URL(str(self.raw_url + element["href"]))
            for element in soup.select("a.sc-ff8a9791-10.htpbqG")
        ]

        names: list[str] = [
            element.string
            for element in soup.select(
                "span.sc-d99ca57-0.cpPIRA.sc-ff8a9791-16.dubjqF.nameCard"
            )
        ]

        prices: list[Money] = [
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

        availability: list[bool] = [
            False if element.string.split("\u00A0")[-1] == "---" else True
            for element in soup.select("span.sc-3b515ca1-2")
        ]

        volatile_data: list[tuple[URL, str, Money, int]] = []
        for link, name, price, availability in zip(
            links,
            names,
            prices,
            availability,
        ):
            volatile_data.append(tuple([link, name, price, availability]))

        number_of_pages: int = [
            int(element.string) for element in soup.select("a.page")
        ]

        n_actual_page: int = int(soup.select_one("a.page.active").string)

        n_next_page: int = n_actual_page + 1

        next_url: URL | None = None

        if n_next_page in number_of_pages:
            next_page = url.split("?")[0] + self.query_string.format(
                page_number=n_next_page
            )
            next_url = URL.get_URL(next_page)
        else:
            next_page = None

        return next_url, volatile_data
