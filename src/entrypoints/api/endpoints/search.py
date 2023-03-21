from dataclasses import dataclass

from flask_restx import Namespace, Resource, reqparse

search_namespace = Namespace("Search")

parser = reqparse.RequestParser()
parser.add_argument("find", type=str, help="", required=True)
parser.add_argument("component_type", type=str)


@dataclass
class AbstractSearchEngine:
    @classmethod
    def search(cls, **kwargs):
        return {"type": "gpu", "model": "gtx 1080"}


@search_namespace.route("")
class SearchList(Resource):
    @search_namespace.doc(parser=parser)
    def get(self):
        return AbstractSearchEngine.search(**parser.parse_args())
