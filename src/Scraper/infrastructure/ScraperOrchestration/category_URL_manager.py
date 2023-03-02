from sqlalchemy.orm.session import Session
from sqlalchemy.exc import NoResultFound
from typing import List
from operator import lt, gt, eq

from framework.domain.value_object import UUID
from framework.infrastructure.db_management.db_structure import CategoryUrlInstance
from Scraper.domain.category_url import CategoryURL
from framework.domain.value_object import URL
from framework.domain.components import EComponentType
from Scraper.domain.repositories import (
    ISQLAlchemyRepository,
    EntityUIDNotFoundException,
)


class CategoryURLManager(ISQLAlchemyRepository):
    _filters_ops: dict = {"filters_eq": eq, "filters_lt": lt, "filters_gt": gt}

    def __init__(self, session):
        self._session: Session = session

    def _url_to_db(self, category_url: CategoryURL):
        url_instance = CategoryUrlInstance()
        url = category_url.url

        url_instance.uid = category_url.uid
        url_instance.domain = url.domain
        url_instance.path = url.path
        url_instance.scheme = url.scheme
        url_instance.type = category_url.category

        return url_instance

    def _db_to_category_url(self, url_instance: CategoryUrlInstance):
        url_str = f"{url_instance.scheme}://{url_instance.domain}/{url_instance.path}"
        url = URL(url_str, url_instance.scheme, url_instance.domain, url_instance.path)
        category_url = CategoryURL(
            _id=url_instance.uid, url=url, category=url_instance.type
        )

        return category_url

    def _parse_filters(self, **kwargs) -> List:
        ret = []

        for filter_type, filters in kwargs.items():
            if filter_type in self._filters_ops.keys():
                op = self._filters_ops[filter_type]

                [
                    ret.append(op(getattr(CategoryUrlInstance, prop), value))
                    for prop, value in filters.items()
                ]

        return ret

    def _filter_components_from_db(self, filters: List) -> List[CategoryURL]:
        url_instances: List[CategoryUrlInstance] = (
            self._session.query(CategoryUrlInstance).filter(*filters).all()
        )

        urls = [self._db_to_category_url(instance) for instance in url_instances]

        return urls

    def _add(self, category_url: CategoryURL):
        url = category_url.url
        url_instance = self._url_to_db(url, category_url.category)
        self._session.add(url_instance)
        self._session.commit()

    def _get(self, **kwargs) -> List[CategoryURL]:
        ret = []

        filters = self._parse_filters(**kwargs)

        urls = self._filter_components_from_db(filters)
        ret.extend(urls)

        return ret

    def _get_by_uid(self, ref: UUID):
        query_filter = [CategoryUrlInstance.uid == ref]

        try:
            category_url: CategoryUrlInstance = (
                self._session.query(CategoryUrlInstance).filter(*query_filter).one()
            )

            url = self._db_to_category_url(category_url)

        except NoResultFound:
            raise EntityUIDNotFoundException(ref)

        return url

    def get_domains(self) -> List[str]:
        query = self._session.query(CategoryUrlInstance.domain).distinct(
            CategoryUrlInstance.domain
        )
        domains = [domain[0] for domain in query]

        return domains
