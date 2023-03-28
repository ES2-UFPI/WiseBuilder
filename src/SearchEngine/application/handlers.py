from typing import Dict, Type, List

from SearchEngine.domain.commands import *

from framework.domain.events import Command, DomainEvent
from framework.application.handler import MessageHandler
from SearchEngine.application.unit_of_work import DataFrameUnitOfWork
from SearchEngine.infrastructure.dataframe_repository import DataFrameRepository
from framework.domain.components import EComponentType
from framework.domain.value_object import UUID


class GetComponentByUIDHandler(MessageHandler):
    def __call__(self, cmd: GetComponentByUID):
        with self.uow:
            return self.uow.repository.get_by_uid(cmd.uid)


class ListComponentsByTypeHandler(MessageHandler):
    def __call__(self, cmd: ListComponentsByType):
        with self.uow:
            return self.uow.repository.get(
                ctype=cmd.ctype,
                qsize=cmd.qsize,
                filters_eq=cmd._filters_eq,
                filters_gt=cmd._filters_gt,
                filters_lt=cmd._filters_lt,
            )


class AddComponentHandler(MessageHandler):
    def __call__(self, cmd: AddComponent):
        with self.uow:
            self.uow.repository.add(cmd.component)
            return True


class SearchByNameHandler(MessageHandler):
    def __call__(self, cmd: SearchByName):
        with self.uow:
            if isinstance(self.uow.repository, DataFrameRepository):
                match cmd.ctype:
                    case EComponentType.CPU:
                        df = self.uow.repository.cpus
                    case EComponentType.GPU:
                        df = self.uow.repository.gpus
                    case EComponentType.PSU:
                        df = self.uow.repository.psus
                    case EComponentType.RAM:
                        df = self.uow.repository.rams
                    case EComponentType.MOTHERBOARD:
                        df = self.uow.repository.motherboards
                    case EComponentType.PERSISTENCE:
                        df = self.uow.repository.ssds
                    case _:
                        df = self.uow.repository.all

                return self._get_best_matches(df, cmd.name)

    def _get_best_matches(self, df, query):
        from thefuzz import fuzz
        from thefuzz.utils import full_process

        query = full_process(query)

        w_ratio = df.model.apply(lambda x: fuzz.WRatio(x, query))
        if "rank" in df.columns:
            df.sort_values(by="rank", inplace=True)

        return df[w_ratio > w_ratio.max()].uid


class MatchNameHandler(MessageHandler):
    def __call__(self, cmd: MatchName):
        with self.uow:
            if isinstance(self.uow.repository, DataFrameRepository):
                self.uow.repository.tfidf.match(
                    [cmd.name], self.uow.repository.all.model.to_list()
                )
                print(cmd.name)
                matched = self.uow.repository.tfidf.get_matches().To.values[0]
                print(matched)
                return UUID(
                    str(
                        self.uow.repository.all[
                            self.uow.repository.all.model == matched
                        ].uid.values[0]
                    )
                )


SE_COMMAND_HANDLER_MAPPER: Dict[Type[Command], Type[MessageHandler]] = {
    GetComponentByUID: GetComponentByUIDHandler,
    ListComponentsByType: ListComponentsByTypeHandler,
    AddComponent: AddComponentHandler,
    SearchByName: SearchByNameHandler,
    MatchName: MatchNameHandler,
}


SE_EVENT_HANDLER_MAPPER: Dict[Type[DomainEvent], List[Type[MessageHandler]]] = {}
