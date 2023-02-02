from typing import List
from ....framework.domain.components import *
from ....framework.infrastructure.db_management.db_structure import ComponentInstance, component_inst_idx, get_attrs

__all__ = ['component_to_bd_object', 'bd_object_to_component']

def _get_attrs_from(c_type : EComponentType):
    comp_attrs      = Component.get_attrs(EComponentType._BASE)
    specific_attrs  = Component.get_attrs(c_type)

    comp_inst_attrs = get_attrs(EComponentType._BASE)
    specific_inst_attrs = get_attrs(c_type)

    return (comp_attrs, specific_attrs), (comp_inst_attrs, specific_inst_attrs)

def _map_from_to(component : Component | ComponentInstance, from_attrs : List, to_attrs : List) -> dict:
    mapped = {t : getattr(component, f) for t, f in zip(to_attrs, from_attrs)}
    return mapped

def component_to_bd_object(component : Component):
    specific_inst_cls   = component_inst_idx[component.type]

    attrs = _get_attrs_from(component.type)

    comp_attrs, specific_attrs = attrs[0]
    comp_inst_attrs, specific_inst_attrs = attrs[1]

    mapped_comp_dict = _map_from_to(component, comp_attrs, comp_inst_attrs)
    mapped_specific_dict = _map_from_to(component, specific_attrs, specific_inst_attrs)
    
    return  (ComponentInstance(**mapped_comp_dict),\
             specific_inst_cls(**mapped_specific_dict))

def bd_object_to_component(component_base : ComponentInstance, component_specific) -> Component:
    specific_comp_cls   = component_cls_idx[component_base.type]

    attrs = _get_attrs_from(component_base.type)

    comp_attrs, specific_attrs = attrs[0]
    comp_inst_attrs, specific_inst_attrs = attrs[1]

    mapped_comp_dict        = _map_from_to(component_base, comp_inst_attrs, comp_attrs)
    mapped_specific_dict    = _map_from_to(component_specific, specific_inst_attrs, specific_attrs)

    return specific_comp_cls(**mapped_comp_dict | mapped_specific_dict)
    