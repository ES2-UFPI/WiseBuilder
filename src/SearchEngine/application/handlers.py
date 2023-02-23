from SearchEngine.domain.commands import *

from framework.application.handler import MessageHandler


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


COMMAND_HANDLER_MAPPER = {
    GetComponentByUID: GetComponentByUIDHandler,
    ListComponentsByType: ListComponentsByTypeHandler,
    AddComponent: AddComponentHandler,
}
