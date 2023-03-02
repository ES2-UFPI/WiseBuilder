from uuid import UUID
from sqlalchemy.dialects.mysql import BINARY
from sqlalchemy.types import TypeDecorator


class BinaryUUID(TypeDecorator):
    impl = BINARY(16)
    cache_ok = True

    def process_bind_param(self, value: UUID, _):
        return value.bytes

    def process_result_value(self, value, _) -> UUID:
        return UUID(bytes=value)
