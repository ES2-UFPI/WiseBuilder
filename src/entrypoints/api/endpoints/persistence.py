from typing import List
from flask_restx import Namespace, Resource, fields
from flask import request

percistence_namespace = Namespace(
    "Percistences", description="Operações relacionadas à Percistência."
)
percistence = percistence_namespace.model(
    "Percistence",
    {
        "id": fields.Integer(description="Identificador da Percistência."),
        "type": fields.String(required=True, description="Tipo de Percistência."),
        "storage": fields.Integer(
            required=True, description="Capacidade de armazenamento da Percistência."
        ),
        "speed": fields.Integer(
            required=True, description="Velocidade de Leitura/Escrita."
        ),
    },
)


Percistences = [
    {
        "id": 0,
        "type": "HDD",
        "storage": 1000,
        "speed": 500,
    }
]

id = 1


def search(mat: List[dict], id: int):
    for index, element in enumerate(mat):
        if element["id"] == id:
            return index, element
    return None, None


@percistence_namespace.route("/")
class PercistenceList(Resource):
    @percistence_namespace.doc("list_comp")
    @percistence_namespace.marshal_list_with(percistence)
    def get(self):
        return Percistences

    @percistence_namespace.expect(percistence)
    def post(self):
        percistence = request.json
        index, _persistence = search(Percistences, percistence["id"])
        if _persistence is None:
            Percistences.append(percistence)
            return Percistences[-1], 201
        else:
            percistence_namespace.abort(409)

    def delete(self):
        Percistences.clear()
        return 204


@percistence_namespace.route("/<int:percistence_id>")
class Percistence(Resource):
    @percistence_namespace.marshal_with(percistence)
    def get(self, percistence_id: int):
        index, percistence = search(Percistences, percistence_id)
        if percistence is None:
            percistence_namespace.abort(404)
        else:
            return percistence

    def delete(self, percistence_id: int):
        index, percistence = search(Percistences, percistence_id)
        if percistence is None:
            percistence_namespace.abort(404)
        else:
            Percistences.pop(index)

        return 204

    @percistence_namespace.expect(percistence)
    def put(self, percistence_id):
        index, percistence = search(Percistences, percistence_id)
        if percistence is None:
            percistence_namespace.abort(404)
        else:
            Percistences[index] = request.json
            return Percistences[index], 200
