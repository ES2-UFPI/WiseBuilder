from enum import Enum

import pygad
from framework.domain.components import Component, EComponentType, CPUComponent
from Scraper.domain.aggragate import VolatileData
from framework.infrastructure.connection_util import get_message_bus
from Scraper.domain.commands import *
from SearchEngine.domain.commands import *
from Scraper.application.handlers import (
    VD_COMMAND_HANDLER_MAPPER,
    VD_EVENT_HANDLER_MAPPER,
)
from SearchEngine.application.handlers import (
    SE_COMMAND_HANDLER_MAPPER,
    SE_EVENT_HANDLER_MAPPER,
)
from Scraper.application.unit_of_work import SQLAlchemyVolatileDataUnitOfWork
from SearchEngine.application.unit_of_work import SQLAlchemyUnitOfWork


class EComputerPurposes(Enum):
    GAMING = 0
    STUDYING = 1
    PROGRAMMING = 2
    WEB_BROWSING = 3


_component_priorities = {
    EComputerPurposes.GAMING: {
        EComponentType.GPU: (0.2, 0.5),
        EComponentType.CPU: (0.1, 0.3),
        EComponentType.RAM: (0.05, 0.2),
        EComponentType.PERSISTENCE: (0.1, 0.25),
        EComponentType.MOTHERBOARD: (0.05, 0.25),
        EComponentType.PSU: (0.1, 0.4),
    },
    # TODO completar o dicionário com as prioridades
}

_gpu_price_thresh = 3500


class ComponentSuggester:
    def __init__(self, budget: float, purpose: EComputerPurposes):
        self.budget = budget
        self.purpose = purpose

        self.vd_message_bus = get_message_bus(
            VD_EVENT_HANDLER_MAPPER,
            VD_COMMAND_HANDLER_MAPPER,
            SQLAlchemyVolatileDataUnitOfWork,
        )

        self.se_message_bus = get_message_bus(
            SE_EVENT_HANDLER_MAPPER, SE_COMMAND_HANDLER_MAPPER, SQLAlchemyUnitOfWork
        )

    # def fitness_func(solution, solution_idx):
    #     output = numpy.sum(solution*function_inputs)
    #     fitness = 1.0 / numpy.abs(output - desired_output)
    #     return fitness

    def _get_components_by_cost_interval(
        self, priorities: dict[EComponentType, tuple], component_type: EComponentType
    ) -> tuple[list[Component], list[VolatileData]]:
        priority = priorities[component_type]

        component, volatile_data = self.vd_message_bus.handle(
            GetVolatileDataByCostInterval(
                component_type,
                self.budget * priority[0],
                self.budget * priority[1],
                True,
            )
        )

        return component, volatile_data

    def generate_computer(self) -> list[Component]:
        component_priorities = _component_priorities[self.purpose]

        cpus, cpus_vd = self._get_components_by_cost_interval(
            component_priorities, EComponentType.CPU
        )
        gpus, gpus_vd = self._get_components_by_cost_interval(
            component_priorities, EComponentType.GPU
        )
        rams, rams_vd = self._get_components_by_cost_interval(
            component_priorities, EComponentType.RAM
        )
        motherboards, motherboards_vd = self._get_components_by_cost_interval(
            component_priorities, EComponentType.MOTHERBOARD
        )
        persistences, persistences_vd = self._get_components_by_cost_interval(
            component_priorities, EComponentType.PERSISTENCE
        )
        psus, psus_vd = self._get_components_by_cost_interval(
            component_priorities, EComponentType.PSU
        )

        for i, cpu in enumerate(cpus):
            if isinstance(cpu, CPUComponent):
                if cpu.integrated_gpu is None or len(cpu.integrated_gpu) == 0:
                    del cpus[i]
                    del cpus_vd[i]

        # TODO Executa problema da mochila, restringindo com base na compatibilidade.
        # TODO somar consumo total e definir fonte com o orçamento estabelecido.
        # TODO caso o orçamento não seja totalmente preenchido, aumentar o orçamento do item prioritário, mantendo as compatibilidades anteriores

        return []
