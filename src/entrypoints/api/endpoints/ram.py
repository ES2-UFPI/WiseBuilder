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

ram_namespace = Namespace("RAMs", description="Operações relacionadas à RAMs.")
ram_model = ram_namespace.model(
    "RAM",
    {
        "_id": fields.String(description="Identificador da memória RAM."),
        "manufacturer": fields.String(required=True, description="Fabricante da GPU."),
        "type": fields.String(required=True, description="Tipo do componente."),
        "model": fields.String(required=True, description="Modelo da GPU"),
        "generation": fields.Integer(
            required=True, description="Geração da memória RAM."
        ),
        "frequency": fields.Integer(
            required=True, description="Frequência da memória RAM."
        ),
    },
)


@ram_namespace.route("/")
class RAMList(Resource):
    @ram_namespace.doc("list_comp")
    @ram_namespace.marshal_list_with(ram_model)
    def get(self):
        _rams = message_bus.handle(ListComponentsByType.RAM())
        return _rams

    @ram_namespace.expect(ram_model)
    def post(self):
        body = request.json
        ram = dict((key, body[key]) for key in list(ram_model.keys())[1:])
        try:
            _ = message_bus.handle(AddComponent.buildRAM(**ram))
            return ram, 201
        except EntityUIDCollisionException as err:
            return str(err), 409


@ram_namespace.route("/<ram_id>")
class RAM(Resource):
    @ram_namespace.marshal_with(ram_model)
    def get(self, ram_id: str):
        try:
            component = message_bus.handle(GetComponentByUID(UUID(ram_id)))
            return component
        except EntityUIDNotFoundException as err:
            return str(err), 404


#
#     def delete(self, ram_id: int):
#         index, ram = search(RAMS, ram_id)
#         if ram is None:
#             ram_namespace.abort(404)
#         else:
#             RAMS.pop(index)
#
#         return 204
#
#     @ram_namespace.expect(ram)
#     def put(self, ram_id):
#         index, ram = search(RAMS, ram_id)
#         if ram is None:
#             ram_namespace.abort(404)
#         else:
#             RAMS[index] = request.json
#             return RAMS[index], 200
