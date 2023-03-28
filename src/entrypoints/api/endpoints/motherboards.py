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

motherboard_namespace = Namespace(
    "MotherBoards", description="Operações relacionadas à Placa-Mãe."
)
motherboard_model = motherboard_namespace.model(
    "MotherBoard",
    {
        "_id": fields.String(description="Identificador da Placa-Mãe."),
        "type": fields.String(description="Tipo do componente."),
        "manufacturer": fields.String(
            required=True, description="Fabricante da Placa-Mãe."
        ),
        "model": fields.String(required=True, description="Modelo da Placa-Mãe."),
        "chipset": fields.Integer(required=True),
        "board_size": fields.Integer(required=True),
        "n_ram_slots": fields.Integer(required=True),
        "consumption": fields.Integer(
            required=True, description="Consumo da Placa-Mãe."
        ),
        "n_usb2": fields.Integer(required=True),
        "n_usb3x": fields.Integer(required=True),
        "n_vga": fields.Integer(required=True),
        "n_hdmi": fields.Integer(required=True),
        "n_display_port": fields.Integer(required=True),
        "pcie_gen": fields.Integer(required=True),
        "n_pcie_x1": fields.Integer(required=True),
        "n_pcie_x4": fields.Integer(required=True),
        "n_pcie_x8": fields.Integer(required=True),
        "n_pcie_x16": fields.Integer(required=True),
    },
)


@motherboard_namespace.route("/")
class MotherBoardList(Resource):
    @motherboard_namespace.doc("list_comp")
    @motherboard_namespace.marshal_list_with(motherboard_model)
    def get(self):
        _motherboards = message_bus.handle(ListComponentsByType.Motherboard())
        for _motherboard in _motherboards:
            _motherboard.type = _motherboard.type._name_
        return _motherboards

    @motherboard_namespace.expect(motherboard_model)
    def post(self):
        body = request.json
        motherboard = dict(
            (key, body[key]) for key in list(motherboard_model.keys())[2:]
        )
        try:
            _ = message_bus.handle(AddComponent.buildMotherboard(**motherboard))
            return motherboard, 201
        except EntityUIDCollisionException as err:
            return str(err), 409


@motherboard_namespace.route("/<motherboard_id>")
class MotherBoard(Resource):
    @motherboard_namespace.marshal_with(motherboard_model)
    def get(self, motherboard_id: str):
        try:
            component = message_bus.handle(GetComponentByUID(UUID(motherboard_id)))
            return component
        except EntityUIDNotFoundException as err:
            return str(err), 404

    #
    # def delete(self, motherboard_id: int):
    #     index, motherboard = search(MotherBoards, motherboard_id)
    #     if motherboard is None:
    #         motherboard_namespace.abort(404)
    #     else:
    #         MotherBoards.pop(index)
    #
    #     return 204
    #
    # @motherboard_namespace.expect(motherboard)
    # def put(self, motherboard_id):
    #     index, motherboard = search(MotherBoards, motherboard_id)
    #     if motherboard is None:
    #         motherboard_namespace.abort(404)
    #     else:
    #         MotherBoards[index] = request.json
    #         return MotherBoards[index], 200
