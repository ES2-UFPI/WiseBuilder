from sqlalchemy.exc import NoResultFound, IntegrityError
from sqlalchemy.orm.session import Session
from typing import List
from operator import lt, gt, eq

from framework.domain.value_object import UUID
from framework.infrastructure.db_management.db_structure import (
    CategoryURLInstance,
    AttrsCategoryURLInstance,
)
from framework.domain.components import EComponentType
from Scraper.domain.entity import CategoryURL, AttrsCategoryURL
from framework.infrastructure.db_management.db_mapping import map_from_to
from framework.domain.value_object import URL, AttrsURL
from Scraper.domain.repositories import (
    ICategoryURLRepository,
    EntityUIDNotFoundException,
    EntityUIDCollisionException,
)


class SQLAlchemyCategoryURL(ICategoryURLRepository):
    _filters_ops: dict = {"filters_eq": eq}

    def __init__(self, session):
        self._session: Session = session

    def _url_to_db(self, category_url: CategoryURL):
        url_instance = CategoryURLInstance()
        url = category_url.url

        category_url_attrs = AttrsCategoryURL.copy()
        category_url_attrs.remove("url")

        mapped = map_from_to(category_url, category_url_attrs, AttrsCategoryURLInstance)
        mapped.update(
            map_from_to(
                url, AttrsURL[1:], AttrsCategoryURLInstance[len(category_url_attrs) :]
            )
        )

        url_instance = CategoryURLInstance(**mapped)

        return url_instance

    def _db_to_category_url(self, url_instance: CategoryURLInstance):
        url_str = f"{url_instance.scheme}://{url_instance.domain}/{url_instance.path}"

        url = URL(
            url_str,
            str(url_instance.scheme),
            str(url_instance.domain),
            str(url_instance.path),
        )
        category_url = CategoryURL(
            _id=url_instance.uid,
            url=url,
            category=EComponentType(url_instance.category),
        )

        return category_url

    def _parse_filters(self, **kwargs) -> List:
        ret = []

        for filter_type, filters in kwargs.items():
            if filter_type in self._filters_ops.keys():
                op = self._filters_ops[filter_type]

                [
                    ret.append(op(getattr(CategoryURLInstance, prop), value))
                    for prop, value in filters.items()
                ]

        return ret

    def _filter_category_url_from_db(self, filters: List) -> List[CategoryURL]:
        url_instances: List[CategoryURLInstance] = (
            self._session.query(CategoryURLInstance).filter(*filters).all()
        )

        urls = [self._db_to_category_url(instance) for instance in url_instances]

        return urls

    def _add(self, category_url: CategoryURL):
        url_instance = self._url_to_db(category_url)

        try:
            self._session.add(url_instance)
            self._session.commit()
        except IntegrityError:
            raise EntityUIDCollisionException(category_url.uid)

    def _get(self, **kwargs) -> List[CategoryURL]:
        ret = []

        filters = self._parse_filters(**kwargs)

        urls = self._filter_category_url_from_db(filters)
        ret.extend(urls)

        return ret

    def _get_by_uid(self, ref: UUID):
        query_filter = [CategoryURLInstance.uid == ref]

        try:
            category_url: CategoryURLInstance = (
                self._session.query(CategoryURLInstance).filter(*query_filter).one()
            )

            url = self._db_to_category_url(category_url)

        except NoResultFound:
            raise EntityUIDNotFoundException(ref)

        return url

    def _get_all_domains(self) -> List[tuple[str, str]]:
        params = [CategoryURLInstance.scheme, CategoryURLInstance.domain]

        query = self._session.query(*params).distinct(CategoryURLInstance.domain)
        urls = [url for url in query]
        return urls
