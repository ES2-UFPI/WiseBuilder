import pytest
import requests as rq
from Scraper.domain.scrapers import KabumScraper
from framework.domain.value_object import Money, URL


@pytest.fixture()
def get_data_with_unvailable():
    kabum_scraper = KabumScraper()
    url = "https://www.kabum.com.br/hardware/ssd-2-5?page_number=8&page_size=100&facet_filters=&sort=most_searched"
    return kabum_scraper.get_volatile_data(url)


@pytest.mark.unit
def test_scraper_unvailable(get_data_with_unvailable):
    next_page, data = get_data_with_unvailable
    assert (
        next_page
        == "https://www.kabum.com.br/hardware/ssd-2-5?page_number=9&page_size=100&facet_filters=&sort=most_searched"
    )

    available_product = data[0]
    unavailable_product = [info for info in data if not info[-1]]

    test_available_product = (
        URL.get_URL(
            "https://www.kabum.com.br/produto/196886/ssd-imation-2-5-sata-iii-a320-240gb"
        ),
        "Ssd Imation 2.5 Sata Iii - A320 240gb",
        Money(485.99),
        True,
    )

    for data_scraper, data_test in zip(available_product, test_available_product):
        assert data_scraper == data_test

    test_unavailable_product = (
        URL.get_URL(
            "https://www.kabum.com.br/produto/314763/ssd-hikvision-240gb-2-5-sata-3-hs-ssd-c100-240g"
        ),
        'Ssd Hikvision 240gb 2,5" Sata 3 - Hs-ssd-c100/240g',
        Money(-1),
        False,
    )

    for data_scraper, data_test in zip(
        unavailable_product[0], test_unavailable_product
    ):
        assert data_scraper == data_test


@pytest.fixture()
def get_final_page():
    kabum_scraper = KabumScraper()
    url = "https://www.kabum.com.br/hardware/ssd-2-5?page_number=17&page_size=100&facet_filters=&sort=most_searched"
    return kabum_scraper.get_volatile_data(url)


@pytest.mark.unit
def test_final_page(get_final_page):
    next_page, data = get_final_page
    assert next_page is None
