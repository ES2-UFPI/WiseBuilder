from dataclasses import dataclass

from flask_restx import Namespace, Resource, reqparse, fields

search_namespace = Namespace("Search")

result_model = search_namespace.model(
    "search",
    {
        "_id": fields.String(description="Identificador do componente."),
        "model": fields.String(required=True, description="Modelo do componente."),
        "type": fields.String(required=True, description="Tipo do componente."),
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
        sla = AbstractSearchEngine.search(
            name,
        )
        print(sla)
        return sla
