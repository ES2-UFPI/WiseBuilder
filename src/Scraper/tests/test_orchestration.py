import pytest
from uuid import UUID
from sqlalchemy_utils import drop_database

from framework.domain.value_object import URL
from framework.infrastructure.db_management.db_connection import (
    create_new_engine,
    create_session,
)
from framework.infrastructure.db_management.db_creation import create_db
from SearchEngine.infrastructure.ComponentManagment.SQL_alchemy_repository import (
    SQLAlchemyRepository,
)
from Scraper.infrastructure.VolatileDataManagment.SQL_alchemy_volatile_data import (
    SQLAlchemyVolatileData,
)
from framework.domain.value_object import UUIDv5
from framework.domain.components import Component
from Scraper.domain.aggragate import VolatileData
from framework.domain.value_object import Money

session = None


@pytest.fixture
def get_session():
    engine = create_new_engine(
        "root", "12345678", "127.0.0.1", "3306", "Wisebuilder_test"
    )

    try:
        drop_database(engine.url)
    except:
        pass

    create_db(engine)
    global session
    if session == None:
        session = create_session(engine)

    return session


@pytest.fixture
def get_component(get_session):
    sql_a = SQLAlchemyRepository(get_session)
    component = None

    try:
        component = Component(_id=UUID(int=0), manufacturer="Intel", model="Core i3")
        sql_a.add(component)
    except Exception:
        component = sql_a.get_by_uid(UUID(int=0))

    return component


@pytest.fixture
def get_volatile_data(get_component):
    url = URL("https://www.kabum.com/teste", "http", "www.kabum.com.br", "test")
    cost = Money(amount=1000.0)
    component = get_component
    volatile_data = VolatileData(
        _id=UUIDv5(url.url),
        url=url,
        component_id=component.uid,
        cost=cost,
        availability=True,
    )
    return volatile_data


@pytest.mark.integration
def test_volatile_data_creation(get_session, get_volatile_data):
    volatile_data = get_volatile_data
    sql_v = SQLAlchemyVolatileData(get_session)
    sql_v.add(volatile_data)  # adiciona com custo 1000

    volatile_data_db: VolatileData = sql_v.get_by_uid(volatile_data.uid)

    assert volatile_data_db.cost == 1000.0

    new_cost = Money(900.0)
    volatile_data.cost = new_cost
    sql_v.add(volatile_data)  # atualiza para custo 900

    volatile_data_db: VolatileData = sql_v.get_by_uid(volatile_data.uid)
    assert volatile_data_db.cost == 900.0
