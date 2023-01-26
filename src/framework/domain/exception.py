class DomainException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class InvalidUrlException(DomainException):
    def __init__(self) -> None:
        super().__init__(message="A url informada é inválida.")
