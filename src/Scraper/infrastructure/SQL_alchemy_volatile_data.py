from sqlalchemy.orm.session import Session
from sqlalchemy.exc import NoResultFound
from sqlalchemy import update

from framework.domain.value_object import UUID
from framework.infrastructure.db_management.db_mapping import map_from_to
from framework.infrastructure.db_management.db_structure import (
    VolatileDataInstance,
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

    def volatile_data_to_db_object(
        self, volatile_data: VolatileData
    ) -> VolatileDataInstance:
        mapped_vol_data = map_from_to(
            volatile_data, VolatileData.get_attrs(), AttrsVolatileData
        )

        return VolatileDataInstance(**mapped_vol_data)

    def db_object_to_volatile_data(
        self, volatile_data_instance: VolatileDataInstance
    ) -> VolatileData:
        mapped_vol_data = map_from_to(
            volatile_data_instance, AttrsVolatileData, VolatileData.get_attrs()
        )

        return VolatileData(**mapped_vol_data)

    def _get_instance_by_uid(self, ref: UUID) -> VolatileDataInstance:
        query_filter = [VolatileDataInstance.url_id == ref]

        try:
            vol_data_inst: VolatileDataInstance = (
                self._session.query(VolatileDataInstance).filter(*query_filter).one()
            )

        except NoResultFound:
            raise EntityUIDNotFoundException(ref)

        return vol_data_inst

    def _add(self, volatile_data: VolatileData):
        db_volatile_data: VolatileDataInstance = self.volatile_data_to_db_object(
            volatile_data
        )

        db_volatile_data.url = volatile_data.url.url  # TODO modificar dicionário
        db_volatile_data.cost = volatile_data.cost.amount

        try:
            current_volatile_data = self._get_instance_by_uid(volatile_data.uid)

            if (
                db_volatile_data.cost + 0.1 < current_volatile_data.cost
                and db_volatile_data.availability
            ):
                volatile_data.events.append(LowerPriceRegisteredEvent(volatile_data.component_id, volatile_data.cost))
                print(
                    f"preço reduzido de {current_volatile_data.cost} para {db_volatile_data.cost}."
                )

            current_volatile_data.cost = db_volatile_data.cost
            current_volatile_data.timestamp = db_volatile_data.timestamp

        except EntityUIDNotFoundException:
            self._session.add(db_volatile_data)

        self._session.commit()

    def _get(self, **kwargs):
        return super()._get(**kwargs)

    def _get_by_uid(self, ref: UUID):
        volatile_data_instance = self._get_instance_by_uid(ref)
        volatile_data = self.db_object_to_volatile_data(volatile_data_instance)

        return volatile_data
