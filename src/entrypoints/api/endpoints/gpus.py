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

gpu_namespace = Namespace("GPUs", description="Operações relacionadas à GPUs.")
gpu_model = gpu_namespace.model(
    "GPU",
    {
        "_id": fields.String(description="Identificador da GPU."),
        "type": fields.String(description="Tipo do componente."),
        "manufacturer": fields.String(required=True, description="Fabricante da GPU."),
        "model": fields.String(required=True, description="Modelo da GPU"),
        "consumption": fields.Integer(required=True, description="Consumo da GPU."),
        "vram": fields.Integer(
            required=True, description="Capacidade da memória ram da GPU."
        ),
        "vram_spd": fields.Integer(
            required=True, description="Velocidade da memória ram da GPU."
        ),
    },
)


@gpu_namespace.route("/")
class GPUList(Resource):
    @gpu_namespace.doc("list_comp")
    @gpu_namespace.marshal_list_with(gpu_model)
    def get(self):
        _gpus = message_bus.handle(ListComponentsByType.GPU())
        for _gpu in _gpus:
            _gpu.type = _gpu.type._name_
        return _gpus

    @gpu_namespace.expect(gpu_model)
    def post(self):
        body: dict = request.json
        gpu = dict((key, body[key]) for key in list(gpu_model.keys())[2:])
        try:
            _ = message_bus.handle(AddComponent.buildGPU(**gpu))
            return gpu, 201
        except EntityUIDCollisionException as err:
            return str(err), 409


@gpu_namespace.route("/<gpu_id>")
class GPU(Resource):
    @gpu_namespace.marshal_with(gpu_model)
    def get(self, gpu_id: str):
        try:
            component = message_bus.handle(GetComponentByUID(UUID(gpu_id)))
            return component
        except EntityUIDNotFoundException as err:
            return str(err), 404


#
#     def delete(self, gpu_id: int):
#         index, gpu = search(GPUS, gpu_id)
#         if gpu is None:
#             gpu_namespace.abort(404)
#         else:
#             GPUS.pop(index)
#
#         return 204
#
#     @gpu_namespace.expect(gpu)
#     def put(self, gpu_id):
#         index, gpu = search(GPUS, gpu_id)
#         if gpu is None:
#             gpu_namespace.abort(404)
#         else:
#             GPUS[index] = request.json
#             return GPUS[index], 200
