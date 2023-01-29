from typing import List
from flask_restx import Namespace, Resource, fields
from flask import request

ram_namespace = Namespace("RAMs", description="Operações relacionadas à RAMs.")
ram = ram_namespace.model(
    "RAM",
    {
        "id": fields.Integer(description="Identificador da RAM."),
        "classification": fields.String(required=True),
        "frequency": fields.Integer(required=True),
    },
)

RAMS = [{"id": 0, "classification": "algo", "frequency": 4000}]

id = 1


def search(mat: List[dict], id: int):
    for index, element in enumerate(mat):
        if element["id"] == id:
            return index, element
    return None, None


@ram_namespace.route("/")
class RAMList(Resource):
    @ram_namespace.doc("list_comp")
    @ram_namespace.marshal_list_with(ram)
    def get(self):
        return RAMS

    @ram_namespace.expect(ram)
    def post(self):
        ram = request.json
        index, _ram = search(RAMS, ram["id"])
        if ram is None:
            RAMS.append(ram)
        else:
            ram_namespace.abort(409)
        return RAMS[-1], 201

    def delete(self):
        RAMS.clear()
        return 204


@ram_namespace.route("/<int:ram_id>")
class RAM(Resource):
    @ram_namespace.marshal_with(ram)
    def get(self, ram_id: int):
        index, ram = search(RAMS, ram_id)
        if ram is None:
            ram_namespace.abort(404)
        else:
            return ram

    def delete(self, ram_id: int):
        index, ram = search(RAMS, ram_id)
        if ram is None:
            ram_namespace.abort(404)
        else:
            RAMS.pop(index)

        return 204

    @ram_namespace.expect(ram)
    def put(self, ram_id):
        index, ram = search(RAMS, ram_id)
        if ram is None:
            ram_namespace.abort(404)
        else:
            RAMS[index] = request.json
            return RAMS[index], 200
