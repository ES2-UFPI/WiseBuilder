import sys, os

sys.path.insert(0, os.getcwd())

from typing import Type
import json

from framework.domain.components import *
from framework.infrastructure.connection_util import get_message_bus
from SearchEngine.application.handlers import (
    SE_COMMAND_HANDLER_MAPPER,
    SE_EVENT_HANDLER_MAPPER,
)
from SearchEngine.application.unit_of_work import SQLAlchemyUnitOfWork
from SearchEngine.domain.commands import AddComponent


def store_components_from_json(json_dir: str, component_cls: Type[Component]):
    component_message_bus = get_message_bus(
        SE_EVENT_HANDLER_MAPPER, SE_COMMAND_HANDLER_MAPPER, SQLAlchemyUnitOfWork
    )

    with open(json_dir, "r") as json_file:
        json_objects = json.load(json_file)

        for json_object in json_objects:
            component = component_cls(_id=Component.next_id(), **json_object)

            component_message_bus.handle(AddComponent(component))


def main():
    json_dirs = {GPUComponent: r"..\res\data\raw\gpu.json"}

    [
        store_components_from_json(json_dir, component_cls)
        for component_cls, json_dir in json_dirs.items()
    ]


if __name__ == "__main__":
    main()
