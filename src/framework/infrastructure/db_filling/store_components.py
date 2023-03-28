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
    "memory_type": ERAMGeneration,
}


def store_components_from_json(
    json_dir: str, component_cls: Type[Component], save_dataframe=False, **kwargs
):
    component_message_bus = get_message_bus(
        SE_EVENT_HANDLER_MAPPER, SE_COMMAND_HANDLER_MAPPER, SQLAlchemyUnitOfWork
    )

    save_path = json_dir.replace("raw", "run")
    data_frame = []

    with open(json_dir, "r") as json_file:
        json_objects = json.load(json_file)

        for json_object in json_objects:
            print(json_object)

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

            try:
                component_message_bus.handle(AddComponent(component))

                if save_dataframe:
                    json_object["uid"] = component.uid.hex
                    data_frame.append(json_object)

            except EntityCollisionException:
                pass

    if save_dataframe:
        with open(save_path, "w") as f:
            json.dump(data_frame, f, indent=4)


def main():
    hdd_dir = r"..\res\data\raw\hdd.json"
    store_components_from_json(
        hdd_dir,
        PersistenceComponent,
        save_dataframe=True,
        is_HDD=True,
        io=EPersistenceIOType.SATA,
    )

    json_dirs = {
        MotherboardComponent: r"..\res\data\raw\motherboard.json",
        CPUComponent: r"..\res\data\raw\cpu.json",
        GPUComponent: r"..\res\data\raw\gpu.json",
        RAMComponent: r"..\res\data\raw\ram.json",
        PSUComponent: r"..\res\data\raw\psu.json",
        PersistenceComponent: r"..\res\data\raw\ssd.json",
    }

    [
        store_components_from_json(json_dir, component_cls, save_dataframe=True)
        for component_cls, json_dir in json_dirs.items()
    ]


if __name__ == "__main__":
    main()
