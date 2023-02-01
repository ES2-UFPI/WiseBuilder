from uuid import UUID
from typing import List
from flask_restx import Namespace, Resource, fields
from flask import request
from framework.domain.components import PersistenceComponent
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

persistence_namespace = Namespace(
    "Persistences", description="Operações relacionadas à Persistência."
)
persistence_model = persistence_namespace.model(
    "persistence",
    {
        "_id": fields.String(description="Identificador da Persistência."),
        "manufacturer": fields.String(
            required=True, description="Fabricante da Persistência."
        ),
        "model": fields.String(required=True, description="Modelo da PSU"),
        "storage": fields.Integer(
            required=True, description="Capacidade de armazenamento da Persistência."
        ),
        "spd": fields.Integer(
            required=True, description="Velocidade de Leitura/Escrita."
        ),
        "io": fields.Integer(required=True),
        "is_HDD": fields.Boolean(required=True),
    },
)


def _message_bus():
    uow = MockUnitOfWork({})
    COMMAND_HANDLER_MAPPER_CALLABLE = {}
    for c, h in COMMAND_HANDLER_MAPPER.items():
        COMMAND_HANDLER_MAPPER_CALLABLE[c] = h(uow)

    return MessageBus(uow, {}, COMMAND_HANDLER_MAPPER_CALLABLE)


message_bus = _message_bus()


@persistence_namespace.route("/")
class persistenceList(Resource):
    @persistence_namespace.doc("list_comp")
    @persistence_namespace.marshal_list_with(persistence_model)
    def get(self):
        _persistences = message_bus.handle(ListComponentsByType.Persistence())
        return _persistences

    @persistence_namespace.expect(persistence_model)
    def post(self):
        body = request.json
        persistence = dict(
            (key, body[key]) for key in list(persistence_model.keys())[1:]
        )
        try:
            _ = message_bus.handle(AddComponent.buildPersistence(**persistence))
            return persistence, 201
        except EntityUIDCollisionException as err:
            return str(err), 409


@persistence_namespace.route("/<persistence_id>")
class persistence(Resource):
    @persistence_namespace.marshal_with(persistence_model)
    def get(self, persistence_id: str):
        try:
            component = message_bus.handle(GetComponentByUID(UUID(persistence_id)))
            return component
        except EntityUIDNotFoundException as err:
            return str(err), 404

    # def delete(self, persistence_id: int):
    #     index, persistence = search(persistences, persistence_id)
    #     if persistence is None:
    #         persistence_namespace.abort(404)
    #     else:
    #         persistences.pop(index)
    #
    #     return 204
    #
    # @persistence_namespace.expect(persistence)
    # def put(self, persistence_id):
    #     index, persistence = search(persistences, persistence_id)
    #     if persistence is None:
    #         persistence_namespace.abort(404)
    #     else:
    #         persistences[index] = request.json
    #         return persistences[index], 200
