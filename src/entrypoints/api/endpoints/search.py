from dataclasses import dataclass
from functools import reduce, partial

from flask_restx import Namespace, Resource, reqparse, fields

from SearchEngine.domain.commands import SearchByName
from Scraper.application.handlers import (
    CURL_COMMAND_HANDLER_MAPPER,
    CURL_EVENT_HANDLER_MAPPER,
    VD_COMMAND_HANDLER_MAPPER,
    VD_EVENT_HANDLER_MAPPER,
)
from Scraper.application.unit_of_work import (
    SQLAlchemyCategoryURLUnitOfWork,
    SQLAlchemyVolatileDataUnitOfWork,
)
from SearchEngine.application.handlers import SE_COMMAND_HANDLER_MAPPER
from SearchEngine.application.unit_of_work import (
    DataFrameUnitOfWork,
    SQLAlchemyUnitOfWork,
)
from framework.infrastructure.connection_util import get_message_bus
from Scraper.domain.commands import GetVolatileDataByComponentUID
from SearchEngine.domain.commands import GetComponentByUID

search_namespace = Namespace("Search")

result_model = search_namespace.model(
    "search",
    {
        "_id": fields.String(description="Identificador do componente."),
        "model": fields.String(required=True, description="Modelo do componente."),
        "type": fields.String(description="Tipo do componente."),
        "price": fields.Float(required=True, description="Preço do componente."),
        "available": fields.Boolean(
            required=True, description="Disponibilidade do componente."
        ),
    },
)
parser = reqparse.RequestParser()
parser.add_argument("name", type=str, help="", required=True)
parser.add_argument("component_type", type=str)
parser.add_argument("price", type=float)


mock_components: list[dict] = [
    {
        "_id": 21309123,
        "model": "Modelo de Teste 01",
        "price": 300.00,
        "available": True,
    },
    {
        "_id": 53309123,
        "model": "Modelo de Teste 02",
        "price": 100.00,
        "available": True,
    },
    {
        "_id": 89309123,
        "model": "Modelo de Teste 03",
        "price": 20.00,
        "available": True,
    },
    {
        "_id": 8930912213,
        "model": "Modelo de Teste 04",
        "price": 20.00,
        "available": True,
    },
]

_volatile_data_message_bus = get_message_bus(
    VD_EVENT_HANDLER_MAPPER,
    VD_COMMAND_HANDLER_MAPPER,
    SQLAlchemyVolatileDataUnitOfWork,
)

_sse_message_bus = get_message_bus(
    {}, SE_COMMAND_HANDLER_MAPPER, DataFrameUnitOfWork, "../res/data/run"
)

_search_message_bus = get_message_bus(
    {}, SE_COMMAND_HANDLER_MAPPER, SQLAlchemyUnitOfWork
)


@dataclass
class AbstractSearchEngine:
    @classmethod
    def search(cls, name="", **kwargs):
        matchs = [
            component for component in mock_components if name in component["model"]
        ]
        return matchs


@search_namespace.route("")
class SearchList(Resource):
    @search_namespace.marshal_list_with(result_model)
    @search_namespace.doc(parser=parser)
    def get(self):
        args = parser.parse_args()
        name = args.get("name")
        matches = _sse_message_bus.handle(SearchByName(name))
        components = [
            _search_message_bus.handle(GetComponentByUID(match_)) for match_ in matches
        ]
        vol_data = [
            _volatile_data_message_bus.handle(
                GetVolatileDataByComponentUID(component.uid)
            )
            for component in components
        ]
        vol_data = [reduce(lambda x, y: x < y, l) for l in vol_data]
        return [
            {
                "_id": component.uid,
                "model": component.model,
                "price": vol.price,
                "available": vol.aval,
            }
            for component, vol in zip(components, vol_data)
        ]
