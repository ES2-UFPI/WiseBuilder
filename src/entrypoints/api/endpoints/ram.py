from uuid import UUID
from typing import List
from flask import request
from flask_restx import Namespace, Resource, fields
from framework.domain.components import CPUComponent
from framework.application.handler import MessageBus
from SearchEngine.application.handlers import COMMAND_HANDLER_MAPPER
from SearchEngine.application.unit_of_work import MockUnitOfWork
from SearchEngine.domain.repositories import (
    EntityUIDNotFoundException,
    EntityUIDCollisionException,
)
from SearchEngine.domain.commands import (
    AddComponent,
    ListComponentsByType,
    GetComponentByUID,
)

ram_namespace = Namespace("RAMs", description="Operações relacionadas à RAMs.")
ram_model = ram_namespace.model(
    "RAM",
    {
        "_id": fields.String(description="Identificador da memória RAM."),
        "manufacturer": fields.String(required=True, description="Fabricante da GPU."),
        "model": fields.String(required=True, description="Modelo da GPU"),
        "generation": fields.Integer(
            required=True, description="Geração da memória RAM."
        ),
        "frequency": fields.Integer(
            required=True, description="Frequência da memória RAM."
        ),
    },
)


def _message_bus():
    uow = MockUnitOfWork({})
    COMMAND_HANDLER_MAPPER_CALLABLE = {}
    for c, h in COMMAND_HANDLER_MAPPER.items():
        COMMAND_HANDLER_MAPPER_CALLABLE[c] = h(uow)

    return MessageBus(uow, {}, COMMAND_HANDLER_MAPPER_CALLABLE)


message_bus = _message_bus()


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
