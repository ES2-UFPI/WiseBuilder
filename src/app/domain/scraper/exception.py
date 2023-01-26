from framework.domain.exception import DomainException


class ScraperNotFoundException(DomainException):
    def __init__(self) -> None:
        super().__init__(message="Scraper não encontrado.")



