from abc import ABC, abstractmethod

class DomainEvent:
    pass


class EventPublisher(ABC):
    @abstractmethod
    def publish(self, event: DomainEvent):
        raise NotImplementedError