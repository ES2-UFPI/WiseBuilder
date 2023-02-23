from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.engine.base import Engine

from .db_structure import base


def create_db(engine: Engine):
    if not database_exists(engine.url):
        create_database(engine.url)

    base.metadata.create_all(engine)
