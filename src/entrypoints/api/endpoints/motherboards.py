from typing import List
from flask_restx import Namespace, Resource, fields
from flask import request

motherboard_namespace = Namespace(
    "MotherBoards", description="Operações relacionadas à Placa-Mãe."
)
motherboard = motherboard_namespace.model(
    "MotherBoard",
    {
        "id": fields.Integer(description="Identificador da Placa-Mãe."),
        "consumption": fields.Integer(
            required=True, description="Consumo da Placa-Mãe."
        ),
        "socket": fields.String(required=True, description="Socket da Placa-Mãe."),
        "size": fields.String(required=True, description="..."),
        "ram_slots": fields.Integer(
            required=True, description="Quantidade de memórias rams suportada."
        ),
        "pcie_generation": fields.String(required=True, description=""),
        "pcie_ports": fields.Integer(required=True, description="..."),
        "outputs": fields.String(required=True, description="Saídas da Placa-mãe."),
    },
)

MotherBoards = [
    {
        "id": 0,
        "consumption": 40,
        "socket": "sla",
        "cores": 16,
        "clock_base": 4.0,
        "clock_max": 6.0,
        "ram_max_clock": 300,
        "intergrated_gpu": "nenhuma",
        "overclock": True,
    }
]

id = 1


def search(mat: List[dict], id: int):
    for index, element in enumerate(mat):
        if element["id"] == id:
            return index, element
    return None, None


@motherboard_namespace.route("/")
class MotherBoardList(Resource):
    @motherboard_namespace.doc("list_comp")
    @motherboard_namespace.marshal_list_with(motherboard)
    def get(self):
        return MotherBoards

    @motherboard_namespace.expect(motherboard)
    def post(self):
        motherboard = request.json
        index, _motherboard = search(MotherBoards, motherboard["id"])
        if motherboard is None:
            MotherBoards.append(motherboard)
        else:
            motherboard_namespace.abort(409)
        return MotherBoards[-1], 201

    def delete(self):
        MotherBoards.clear()
        return 204


@motherboard_namespace.route("/<int:motherboard_id>")
class MotherBoard(Resource):
    @motherboard_namespace.marshal_with(motherboard)
    def get(self, motherboard_id: int):
        index, motherboard = search(MotherBoards, motherboard_id)
        if motherboard is None:
            motherboard_namespace.abort(404)
        else:
            return motherboard

    def delete(self, motherboard_id: int):
        index, motherboard = search(MotherBoards, motherboard_id)
        if motherboard is None:
            motherboard_namespace.abort(404)
        else:
            MotherBoards.pop(index)

        return 204

    @motherboard_namespace.expect(motherboard)
    def put(self, motherboard_id):
        index, motherboard = search(MotherBoards, motherboard_id)
        if motherboard is None:
            motherboard_namespace.abort(404)
        else:
            MotherBoards[index] = request.json
            return MotherBoards[index], 200
