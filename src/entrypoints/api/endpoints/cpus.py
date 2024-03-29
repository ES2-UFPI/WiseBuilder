import uuid
from typing import List
from uuid import UUID

from flask import request
from flask_restx import Namespace, Resource, fields
from SearchEngine.domain.commands import (
    AddComponent,
    GetComponentByUID,
    ListComponentsByType,
)
from SearchEngine.domain.repositories import (
    EntityUIDCollisionException,
    EntityUIDNotFoundException,
)
from SearchEngine.infrastructure.message_bus import se_message_bus as message_bus

cpu_namespace = Namespace("CPUs", description="Operações relacionadas à CPUs.")

cpu_model = cpu_namespace.model(
    "CPU",
    {
        "_id": fields.String(description="Identificador da CPU."),
        "type": fields.String(description="Tipo do componente."),
        "manufacturer": fields.String(required=True, description="Fabricante da CPU."),
        "model": fields.String(required=True, description="Modelo da CPU."),
        "socket": fields.String(required=True, description="Socket da CPU."),
        "n_cores": fields.Integer(required=True, description="Número de nucleos."),
        "base_clock_spd": fields.Float(
            required=True, description="Velocidade de clock base da CPU."
        ),
        "boost_clock_spd": fields.Float(
            required=True, description="Velocidade de clock máxima da CPU."
        ),
        "ram_clock_max": fields.Integer(required=True, description=""),
        "consumption": fields.Integer(required=True, description="Consumo da CPU."),
        "integrated_gpu": fields.String(
            required=True, description="Placa de vídeo integrada."
        ),
        "overclock": fields.Boolean(
            required=True, description="Possibilidade de overclock."
        ),
    },
)


@cpu_namespace.route("/")
class CPUList(Resource):
    @cpu_namespace.marshal_list_with(cpu_model)
    def get(self):
        _cpus = message_bus.handle(ListComponentsByType.CPU())
        for _cpu in _cpus:
            _cpu.type = _cpu.type._name_
        return _cpus

    @cpu_namespace.expect(cpu_model)
    def post(self):
        body: dict = request.json
        print(body)
        cpu = dict((key, body[key]) for key in list(cpu_model.keys())[2:])
        try:
            _ = message_bus.handle(AddComponent.buildCPU(**cpu))
            return cpu, 201
        except EntityUIDCollisionException as err:
            return str(err), 409


@cpu_namespace.route("/<cpu_id>")
class CPU(Resource):
    @cpu_namespace.marshal_with(cpu_model)
    def get(self, cpu_id: str):
        try:
            component = message_bus.handle(GetComponentByUID(UUID(cpu_id)))
            return component
        except EntityUIDNotFoundException as err:
            return str(err), 404

    # def delete(self, cpu_id: int):
    #     index, cpu = search(CPUS, cpu_id)
    #     if cpu is None:
    #         cpu_namespace.abort(404)
    #     else:
    #         CPUS.pop(index)
    #
    #     return 204
    #
    # @cpu_namespace.expect(cpu)
    # def put(self, cpu_id):
    #     index, cpu = search(CPUS, cpu_id)
    #     if cpu is None:
    #         cpu_namespace.abort(404)
    #     else:
    #         CPUS[index] = request.json
    #         return CPUS[index], 200
