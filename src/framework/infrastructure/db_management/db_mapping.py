from operator import eq, lt, gt
from typing import List
from sqlalchemy import Column
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.query import Query


_filters_ops: dict = {"filters_eq": eq, "filters_lt": lt, "filters_gt": gt}


def parse_filters(instance_cls, **kwargs) -> List:
    ret = []

    for filter_type, filters in kwargs.items():
        if filter_type in _filters_ops.keys():
            op = _filters_ops[filter_type]

            [
                ret.append(op(getattr(instance_cls, prop), value))
                for prop, value in filters.items()
            ]

    return ret


def map_from_to(
    original_object: object, from_attrs: List, to_attrs: List, ignores=[]
) -> dict:
    mapped = {
        t: getattr(original_object, f)
        for t, f in zip(to_attrs, from_attrs)
        if t not in ignores
    }

    return mapped


def filter_instance_from_db(
    session: Session,
    instance_cls,
    filters: List,
    qsize: int | None = None,
    group_by: Column | None = None,
) -> List:
    query: Query = (
        session.query(instance_cls).filter(*filters).group_by(group_by).limit(qsize)
    )

    db_instances: List[instance_cls] = query.all()

    return db_instances
