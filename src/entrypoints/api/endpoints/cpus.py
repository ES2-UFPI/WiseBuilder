from typing import List
from flask_restx import Namespace, Resource, fields
from flask import request

cpu_namespace = Namespace("CPUs", description="Operações relacionadas à CPUs.")
cpu = cpu_namespace.model(
    "CPU",
    {
        "id": fields.Integer(description="Identificador da CPU."),
        "consumption": fields.Integer(required=True, description="Consumo da CPU."),
        "socket": fields.String(required=True, description="Socket da CPU."),
        "cores": fields.Integer(required=True, description="Número de nucleos."),
        "clock_base": fields.Float(
            required=True, description="Velocidade de clock base da CPU."
        ),
        "clock_max": fields.Float(
            required=True, description="Velocidade de clock máxima da CPU."
        ),
        "ram_max_clock": fields.Integer(required=True, description=""),
        "intergrated_gpu": fields.String(
            required=True, description="Placa de vídeo integrada."
        ),
        "overclock": fields.Boolean(
            required=True, description="Possibilidade de overclock."
        ),
    },
)


CPUS = [
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


@cpu_namespace.route("/")
class CPUList(Resource):
    @cpu_namespace.doc("list_comp")
    @cpu_namespace.marshal_list_with(cpu)
    def get(self):
        return CPUS

    @cpu_namespace.expect(cpu)
    def post(self):
        cpu = request.json
        index, _cpu = search(CPUS, cpu["id"])
        if _cpu is None:
            CPUS.append(cpu)
        else:
            cpu_namespace.abort(400)
        return CPUS[-1], 201

    def delete(self):
        CPUS.clear()
        return 204


@cpu_namespace.route("/<int:cpu_id>")
class CPU(Resource):
    @cpu_namespace.marshal_with(cpu)
    def get(self, cpu_id: int):
        index, cpu = search(CPUS, cpu_id)
        if cpu is None:
            cpu_namespace.abort(404)
        else:
            return cpu

    def delete(self, cpu_id: int):
        index, cpu = search(CPUS, cpu_id)
        if cpu is None:
            cpu_namespace.abort(404)
        else:
            CPUS.pop(index)

        return 204

    @cpu_namespace.expect(cpu)
    def put(self, cpu_id):
        index, cpu = search(CPUS, cpu_id)
        if cpu is None:
            cpu_namespace.abort(404)
        else:
            CPUS[index] = request.json
            return CPUS[index], 200
