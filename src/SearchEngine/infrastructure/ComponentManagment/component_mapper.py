from typing import List
from framework.domain.components import *
from framework.infrastructure.db_management.db_mapping import map_from_to
from framework.infrastructure.db_management.db_structure import (
    ComponentInstance,
    component_inst_idx,
    get_attrs,
)

__all__ = [
    "component_to_db_object",
    "db_object_to_component",
    "find_type_by_property_names",
]


def _get_attrs_from(c_type: EComponentType):
    comp_attrs = Component.get_attrs(c_type)
    comp_inst_attrs = get_attrs(c_type)

    return comp_attrs, comp_inst_attrs


def component_to_db_object(component: Component) -> ComponentInstance:
    specific_inst_cls = component_inst_idx[component.type.value]
    comp_attrs, comp_inst_attrs = _get_attrs_from(component.type)
    mapped_comp_dict = map_from_to(component, comp_attrs, comp_inst_attrs)

    return specific_inst_cls(**mapped_comp_dict)


def db_object_to_component(component_instance: ComponentInstance) -> Component:
    specific_comp_cls = component_cls_idx[component_instance.type]
    comp_attrs, comp_inst_attrs = _get_attrs_from(
        EComponentType(component_instance.type)
    )
    mapped_comp_dict = map_from_to(component_instance, comp_inst_attrs, comp_attrs)

    return specific_comp_cls(**mapped_comp_dict)


def find_type_by_property_names(**kwargs) -> List:
    ignore_propertys = set(["qsize", "ctype"])
    non_matchs = set()
    types = []

    for property_name, value in kwargs.items():
        if property_name in ignore_propertys:
            continue

        for ctype in EComponentType:
            attrs = Component.get_attrs(ctype)

            if all(key in attrs for key in value.keys()):
                types.append(ctype)
            else:
                non_matchs.add(ctype)

    return list(filter(lambda t: t not in non_matchs, types))
