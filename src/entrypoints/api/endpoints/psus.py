from typing import List
from flask_restx import Namespace, Resource, fields
from flask import request

psu_namespace = Namespace("PSUs", description="Operações relacionadas à PSUs.")
psu = psu_namespace.model(
    "PSU",
    {
        "id": fields.Integer(description="Identificador da PSU."),
        "wattage": fields.Integer(required=True, description="Potência da fonte."),
        "classification": fields.String(required=True, description="..."),
    },
)

PSUS = [
    {
        "id": 0,
        "wattage": 700,
        "classification": "algo",
    }
]

id = 1


def search(mat: List[dict], id: int):
    for index, element in enumerate(mat):
        if element["id"] == id:
            return index, element
    return None, None


@psu_namespace.route("/")
class PSUList(Resource):
    @psu_namespace.doc("list_comp")
    @psu_namespace.marshal_list_with(psu)
    def get(self):
        return PSUS

    @psu_namespace.expect(psu)
    def post(self):
        psu = request.json
        index, _psu = search(PSUS, psu["id"])
        if _psu is None:
            PSUS.append(psu)
        else:
            psu_namespace.abort(409)
        return PSUS[-1], 201


@psu_namespace.route("/<int:psu_id>")
class PSU(Resource):
    @psu_namespace.marshal_with(psu)
    def get(self, psu_id: int):
        index, psu = search(PSUS, psu_id)
        if psu is None:
            psu_namespace.abort(404)
        else:
            return psu

    def delete(self, psu_id: int):
        index, psu = search(PSUS, psu_id)
        if psu is None:
            psu_namespace.abort(404)
        else:
            PSUS.pop(index)

        return 204

    @psu_namespace.expect(psu)
    def put(self, psu_id):
        index, psu = search(PSUS, psu_id)
        if psu is None:
            psu_namespace.abort(404)
        else:
            PSUS[index] = request.json
            return PSUS[index], 200
