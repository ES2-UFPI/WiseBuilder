from sqlalchemy.orm.session import Session
from sqlalchemy.exc import NoResultFound
from sqlalchemy import func
from sqlalchemy import Column
from datetime import datetime, timedelta

from framework.domain.value_object import UUID, Money
from framework.infrastructure.db_management.db_mapping import (
    map_from_to,
    parse_filters,
    filter_instance_from_db,
)
from framework.infrastructure.db_management.db_structure import (
    VolatileDataInstance,
    LowerCostsInstance,
    AttrsVolatileData,
)
from Scraper.domain.events import LowerPriceRegisteredEvent
from Scraper.domain.aggragate import VolatileData
from Scraper.domain.repositories import (
    IVolatileDataRepository,
    EntityUIDNotFoundException,
)


class SQLAlchemyVolatileData(IVolatileDataRepository):
    def __init__(self, session):
        self._session: Session = session

    def _volatile_data_to_db_object(
        self, volatile_data: VolatileData
    ) -> VolatileDataInstance:
        mapped_vol_data = map_from_to(
            volatile_data, VolatileData.get_attrs(), AttrsVolatileData
        )

        return VolatileDataInstance(**mapped_vol_data)

    def _db_object_to_volatile_data(
        self, volatile_data_instance: VolatileDataInstance
    ) -> VolatileData:
        mapped_vol_data = map_from_to(
            volatile_data_instance, AttrsVolatileData, VolatileData.get_attrs()
        )

        volatile_data = VolatileData(**mapped_vol_data)
        volatile_data.cost = Money(volatile_data_instance.cost)

        return volatile_data

    def _db_volatile_data_to_lower_cost(
        self, volatile_data: VolatileData
    ) -> LowerCostsInstance:
        lower = LowerCostsInstance()
        lower.component_uid = volatile_data.component_id
        lower.component_type = volatile_data.component_type
        lower.volatile_data_uid = volatile_data.uid
        lower.cost = volatile_data.cost.amount
        lower.timestamp = volatile_data.timestamp

        return lower

    def _get_instance_by_uid(self, ref: UUID) -> VolatileDataInstance:
        query_filter = [VolatileDataInstance.url_id == ref]

        try:
            vol_data_inst: VolatileDataInstance = (
                self._session.query(VolatileDataInstance).filter(*query_filter).one()
            )

        except NoResultFound:
            raise EntityUIDNotFoundException(ref)

        return vol_data_inst

    def _get_lower_cost_by_uid(self, ref: UUID | Column) -> LowerCostsInstance | None:
        query_filter = [LowerCostsInstance.component_uid == ref]

        try:
            vol_data_inst: LowerCostsInstance = (
                self._session.query(LowerCostsInstance).filter(*query_filter).one()
            )

        except Exception:
            return None

        return vol_data_inst

    def _update_lower_cost(self, volatile_data: VolatileData) -> None:
        current_lower = self._get_lower_cost_by_uid(volatile_data.component_id)
        min_timestamp = datetime.now() - timedelta(days=1)

        if current_lower is None:
            lower = self._db_volatile_data_to_lower_cost(volatile_data)
            self._session.add(lower)
            return

        price_reduced = volatile_data.cost.amount + 0.1 < current_lower.cost
        current_outdate = current_lower.timestamp < min_timestamp.date()

        if (
            (price_reduced or current_outdate) and volatile_data.availability
        ) or current_lower.volatile_data_uid == volatile_data:
            current_lower.cost = volatile_data.cost.amount
            current_lower.volatile_data_uid = volatile_data.uid
            current_lower.timestamp = volatile_data.timestamp

            if price_reduced:
                volatile_data.events.append(
                    LowerPriceRegisteredEvent(
                        volatile_data.component_id, volatile_data.cost
                    )
                )

    def _add(self, volatile_data: VolatileData):
        db_volatile_data: VolatileDataInstance = self._volatile_data_to_db_object(
            volatile_data
        )

        db_volatile_data.url = volatile_data.url.url  # TODO modificar dicionário
        db_volatile_data.cost = volatile_data.cost.amount

        try:
            current_volatile_data = self._get_instance_by_uid(volatile_data.uid)
            current_volatile_data.cost = db_volatile_data.cost
            current_volatile_data.timestamp = db_volatile_data.timestamp

        except EntityUIDNotFoundException:
            self._session.add(db_volatile_data)

        self._update_lower_cost(volatile_data)
        self._session.commit()

    def _get(self, **kwargs):
        filters = parse_filters(VolatileDataInstance, **kwargs)

        volatile_datas_instances = filter_instance_from_db(
            self._session, VolatileDataInstance, filters
        )
        volatile_datas = [
            self._db_object_to_volatile_data(instance)
            for instance in volatile_datas_instances
        ]

        return volatile_datas

    def _get_by_uid(self, ref: UUID):
        volatile_data_instance = self._get_instance_by_uid(ref)
        volatile_data = self._db_object_to_volatile_data(volatile_data_instance)

        return volatile_data

    def _get_lower_costs(self, **kwargs):
        filters = parse_filters(LowerCostsInstance, **kwargs)

        lower_costs = filter_instance_from_db(
            self._session, LowerCostsInstance.volatile_data_uid, filters
        )
        volatile_datas = [self._get_by_uid(vd_uid[0]) for vd_uid in lower_costs]

        return volatile_datas
