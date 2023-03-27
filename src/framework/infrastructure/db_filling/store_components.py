import sys, os

sys.path.insert(0, os.getcwd())

from typing import Type
import json

from framework.domain.repositories import EntityCollisionException
from framework.domain.components import *
from framework.domain.components_enums import *
from framework.infrastructure.connection_util import get_message_bus
from SearchEngine.application.handlers import (
    SE_COMMAND_HANDLER_MAPPER,
    SE_EVENT_HANDLER_MAPPER,
)
from SearchEngine.application.unit_of_work import SQLAlchemyUnitOfWork
from SearchEngine.domain.commands import AddComponent

_enumerators = {
    "board_size": EBoardSize,
    "pcie_gen": EPCIeGeneration,
    "generation": ERAMGeneration,
    "io": EPersistenceIOType,
    "rate": EPSURate,
    "modularity": EPSUModularity,
}


def store_components_from_json(json_dir: str, component_cls: Type[Component], **kwargs):
    component_message_bus = get_message_bus(
        SE_EVENT_HANDLER_MAPPER, SE_COMMAND_HANDLER_MAPPER, SQLAlchemyUnitOfWork
    )

    with open(json_dir, "r") as json_file:
        json_objects = json.load(json_file)

        for json_object in json_objects:
            json_filtered = {
                k: v for k, v in json_object.items() if k not in _enumerators
            }
            json_modified = {
                k: _enumerators[k][v]
                for k, v in json_object.items()
                if k in _enumerators
            }
            component = component_cls(
                _id=Component.next_id(), **json_filtered, **json_modified, **kwargs
            )
            print(component)
            try:
                component_message_bus.handle(AddComponent(component))
            except EntityCollisionException:
                pass


def main():
    json_dirs = {
        GPUComponent: r"..\res\data\raw\gpu.json",
        CPUComponent: r"..\res\data\raw\cpu.json",
        RAMComponent: r"..\res\data\raw\ram.json",
        # PSUComponent: r"..\res\data\raw\psu.json",
    }

    [
        store_components_from_json(json_dir, component_cls)
        for component_cls, json_dir in json_dirs.items()
    ]


if __name__ == "__main__":
    main()
