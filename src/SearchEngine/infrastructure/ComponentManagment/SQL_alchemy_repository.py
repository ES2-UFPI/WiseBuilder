from sqlalchemy.orm.session import Session
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.engine import Row
from typing import List

from framework.domain.components import *
from framework.domain.components_enums import *
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
from framework.infrastructure.db_management.db_mapping import (
    parse_filters,
    filter_instance_from_db,
)


class SQLAlchemyRepository(ISQLAlchemyRepository):
    def __init__(self, session):
        self._session: Session = session

    def _add(self, component: Component):
        component_instance = component_to_db_object(component)

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

            component = db_object_to_component(component_inst)

        except NoResultFound:
            raise EntityUIDNotFoundException(ref)

        return component

    def _get(self, **kwargs) -> List[Component]:
        print(kwargs)
        qsize: int = kwargs.get("qsize", None)
        ctypes: List = kwargs.get("ctypes", [])
        ret = []

        if len(ctypes) == 0:
            ctypes = find_type_by_property_names(**kwargs)

        for ctype in ctypes:
            instance_cls = component_inst_idx[ctype]
            filters = parse_filters(instance_cls, **kwargs)

            component_instances = filter_instance_from_db(
                self._session, instance_cls, filters, qsize
            )
            components = [
                db_object_to_component(instance) for instance in component_instances
            ]
            ret.extend(components)

            if qsize != None:
                qsize -= len(components)

                if qsize <= 0:
                    break

        return ret
