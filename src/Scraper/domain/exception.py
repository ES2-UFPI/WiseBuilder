class ScraperNotFoundException(Exception):
    def __init__(self) -> None:
        super().__init__("Scraper não encontrado.")



