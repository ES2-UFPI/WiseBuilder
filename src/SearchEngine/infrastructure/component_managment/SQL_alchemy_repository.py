from sqlalchemy.orm.session import Session
from sqlalchemy.exc import IntegrityError
from typing import List

from framework.domain.components import *
from framework.domain.value_object import UUID
from SearchEngine.domain.repositories import ISQLAlchemyRepository, EntityUIDCollisionException, EntityUIDNotFoundException
from framework.infrastructure.db_management.db_structure import ComponentInstance, component_inst_idx
from SearchEngine.infrastructure.component_managment.component_mapper import *

class SQLAlchemyRepository(ISQLAlchemyRepository):

    def __init__(self, session):
        self._session : Session = session
    
    def _add(self, component: Component):
        component_instances = component_to_bd_object(component)

        for instance in component_instances:
            try:
                self._session.add(instance)
                self._session.commit()
            except IntegrityError:
                raise EntityUIDCollisionException(instance.uid)
        

    def _get_by_uid(self, ref: UUID):
        component = self._get(ctype = EComponentType._BASE, filters_eq = {'uid' : ref})

        if len(component) == 0:
            raise EntityUIDNotFoundException(ref)

        return component[0]

    def _find_type_by_property_names(self, **kwargs):

        ignore = set(['qsize', 'ctype'])
        types = []

        for k, v in kwargs.items():
            if k in ignore:
                continue

            for ctype in EComponentType:
                attrs = Component.get_attrs(ctype)
                if(all(key in attrs for key in v.keys())):
                    types.append(ctype)

        return types

    def _get_formed_object(self, filters : List, ctype : EComponentType, type_inst, qsize):
        query = self._session.query(type_inst).filter(*filters)
        
        if qsize != 0:
            query.limit(qsize)

        components = []

        for component in query:
            base_component = None
            specific_component = None

            if ctype == EComponentType._BASE:
                specific_table = component_inst_idx[component.type]

                base_component = component

                specific_component = self._session.query(specific_table)\
                    .filter(specific_table.component_uid == component.uid)\
                    .first()
                        
            else:
                base_component = self._session.query(ComponentInstance)\
                    .filter(ComponentInstance.uid == component.component_uid)\
                    .first()

                specific_component = component

            component = bd_object_to_component(base_component, specific_component)
            components.append(component)

        return components


    def _get(self, **kwargs):
        qsize = kwargs.get('qsize', 0)
        ctype = kwargs.get('ctype', None)

        c_types = []
        ret = []

        if ctype == None:
            c_types = self._find_type_by_property_names(**kwargs)
        else:
            c_types.append(ctype)

        for ct in c_types:
            type_inst = component_inst_idx[ct]
            filters = []

            for k, v in kwargs.items():
                match k:
                    case 'filters_eq':
                        [filters.append(getattr(type_inst, prop) == val) \
                            for prop, val in v.items()]

                    case 'filters_gt':
                        [filters.append(getattr(type_inst, prop) > val) \
                            for prop, val in v.items()]

                    case 'filters_lt':
                        [filters.append(getattr(type_inst, prop) < val) \
                            for prop, val in v.items()]
                    case _:
                        continue
            
            ret.extend(self._get_formed_object(filters, ct, type_inst, qsize))

        return ret