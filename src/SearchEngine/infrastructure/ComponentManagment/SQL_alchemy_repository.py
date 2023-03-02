from sqlalchemy.orm.session import Session
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.engine import Row
from typing import List
from operator import lt, gt, eq

from framework.domain.components import *
from framework.domain.value_object import UUID
from SearchEngine.domain.repositories import (
    ISQLAlchemyRepository,
    EntityUIDCollisionException,
    EntityUIDNotFoundException,
)
from framework.infrastructure.db_management.db_structure import (
    ComponentInstance,
    component_inst_idx,
)
from SearchEngine.infrastructure.ComponentManagment.component_mapper import *


class SQLAlchemyRepository(ISQLAlchemyRepository):
    _filters_ops: dict = {"filters_eq": eq, "filters_lt": lt, "filters_gt": gt}

    def __init__(self, session):
        self._session: Session = session

    def _add(self, component: Component):
        component_instance = component_to_bd_object(component)

        try:
            self._session.add(component_instance)
            self._session.commit()
        except IntegrityError:
            raise EntityUIDCollisionException(component.uid)

    def _get_by_uid(self, ref: UUID) -> Component:
        query_filter = [ComponentInstance.uid == ref]

        try:
            ctype: Row = (
                self._session.query(ComponentInstance.type).filter(*query_filter).one()
            )

            component_inst: ComponentInstance = (
                self._session.query(component_inst_idx[ctype[0]])
                .filter(*query_filter)
                .one()
            )

            component = bd_object_to_component(component_inst)

        except NoResultFound:
            raise EntityUIDNotFoundException(ref)

        return component

    def _filter_components_from_db(
        self, filters: List, type_inst: ComponentInstance, qsize: int | None
    ) -> List[Component | ComponentInstance]:
        component_instances: List[ComponentInstance] = (
            self._session.query(type_inst).filter(*filters).limit(qsize).all()
        )

        components = [
            bd_object_to_component(instance) for instance in component_instances
        ]

        return components

    def _parse_filters(self, instance_type: ComponentInstance, **kwargs) -> List:
        ret = []

        for filter_type, filters in kwargs.items():
            if filter_type in self._filters_ops.keys():
                op = self._filters_ops[filter_type]

                [
                    ret.append(op(getattr(instance_type, prop), value))
                    for prop, value in filters.items()
                ]

        return ret

    def _get(self, **kwargs) -> List[Component]:
        qsize: int = kwargs.get("qsize", None)
        ctypes: List = kwargs.get("ctypes", [])
        ret = []

        if len(ctypes) == 0:
            ctypes = find_type_by_property_names(**kwargs)

        for ctype in ctypes:
            instance_cls = component_inst_idx[ctype]
            filters = self._parse_filters(instance_cls, **kwargs)

            components = self._filter_components_from_db(filters, instance_cls, qsize)
            ret.extend(components)

            if qsize != None:
                qsize -= len(components)

                if qsize <= 0:
                    break

        return ret
