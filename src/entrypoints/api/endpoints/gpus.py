from typing import List
from flask_restx import Namespace, Resource, fields
from flask import request

gpu_namespace = Namespace("GPUs", description="Operações relacionadas à GPUs.")
gpu = gpu_namespace.model(
    "GPU",
    {
        "id": fields.Integer(description="Identificador da GPU."),
        "consumption": fields.Integer(required=True, description="Consumo da GPU."),
        "vram": fields.Integer(required=True, description="Padrão da VRAM"),
        "vram_vel": fields.Integer(required=True, description="Velocidade da VRAM."),
    },
)

gpu_base = gpu_namespace.model(
    "GPU Base",
    {
        "id": fields.Integer(description="Identificador da GPU."),
        "socket": fields.String(description="Socket da GPU."),
        "cores": fields.Integer(description="Número de nucleos."),
    },
)

GPUS = [
    {
        "id": 0,
        "consumption": 100,
        "vram": 1000,
        "vram_vel": 100,
    }
]


id = 1


def search(mat: List[dict], id: int):
    for index, element in enumerate(mat):
        if element["id"] == id:
            return index, element
    return None, None


@gpu_namespace.route("/")
class GPUList(Resource):
    @gpu_namespace.doc("list_comp")
    @gpu_namespace.marshal_list_with(gpu)
    def get(self):
        return GPUS

    @gpu_namespace.expect(gpu)
    def post(self):
        index, _gpu = search(GPUS, gpu["id"])
        if _gpu is None:
            GPUS.append(gpu)
            return GPUS[-1], 201
        else:
            gpu_namespace.abort(409)

    def delete(self):
        GPUS.clear()
        return 204


@gpu_namespace.route("/<int:gpu_id>")
class GPU(Resource):
    @gpu_namespace.marshal_with(gpu)
    def get(self, gpu_id: int):
        index, gpu = search(GPUS, gpu_id)
        if gpu is None:
            gpu_namespace.abort(404)
        else:
            return gpu

    def delete(self, gpu_id: int):
        index, gpu = search(GPUS, gpu_id)
        if gpu is None:
            gpu_namespace.abort(404)
        else:
            GPUS.pop(index)

        return 204

    @gpu_namespace.expect(gpu)
    def put(self, gpu_id):
        index, gpu = search(GPUS, gpu_id)
        if gpu is None:
            gpu_namespace.abort(404)
        else:
            GPUS[index] = request.json
            return GPUS[index], 200
