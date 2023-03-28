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

psu_namespace = Namespace("PSUs", description="Operações relacionadas à PSUs.")
psu_model = psu_namespace.model(
    "PSU",
    {
        "_id": fields.String(description="Identificador da PSU."),
        "type": fields.String(description="Tipo do componente."),
        "manufacturer": fields.String(required=True, description="Fabricante da PSU."),
        "model": fields.String(required=True, description="Modelo da PSU"),
        "power": fields.Integer(required=True, description="Potência da fonte."),
        "rate": fields.Integer(required=True),
        "modularity": fields.Integer(required=True),
    },
)


@psu_namespace.route("/")
class PSUList(Resource):
    @psu_namespace.doc("list_comp")
    @psu_namespace.marshal_list_with(psu_model)
    def get(self):
        _psus = message_bus.handle(ListComponentsByType.PSU())
        for _psu in _psus:
            _psu.type = _psu.type._name_
        return _psus

    @psu_namespace.expect(psu_model)
    def post(self):
        body = request.json
        psu = dict((key, body[key]) for key in list(psu_model.keys())[2:])
        try:
            _ = message_bus.handle(AddComponent.buildPSU(**psu))
            return psu, 201
        except EntityUIDCollisionException as err:
            return str(err), 409


@psu_namespace.route("/<psu_id>")
class PSU(Resource):
    @psu_namespace.marshal_with(psu_model)
    def get(self, psu_id: str):
        try:
            component = message_bus.handle(GetComponentByUID(UUID(psu_id)))
            return component
        except EntityUIDNotFoundException as err:
            return str(err), 404

    # def delete(self, psu_id: int):
    #     index, psu = search(PSUS, psu_id)
    #     if psu is None:
    #         psu_namespace.abort(404)
    #     else:
    #         PSUS.pop(index)
    #
    #     return 204
    #
    # @psu_namespace.expect(psu)
    # def put(self, psu_id):
    #     index, psu = search(PSUS, psu_id)
    #     if psu is None:
    #         psu_namespace.abort(404)
    #     else:
    #         PSUS[index] = request.json
    #         return PSUS[index], 200
