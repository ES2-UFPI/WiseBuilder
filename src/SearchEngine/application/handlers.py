from SearchEngine.domain.commands import *

from framework.application.handler import MessageHandler


class GetComponentByUIDHandler(MessageHandler):
    def __call__(self, cmd: GetComponentByUID):
        with self.uow:
            return self.uow.repository.get_by_uid(cmd.uid)


class ListComponentsByTypeHandler(MessageHandler):
    def __call__(self, cmd: ListComponentsByType):
        with self.uow:
            return self.uow.repository.get(ctype=cmd.type, qsize=10)


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
