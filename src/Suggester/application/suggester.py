from enum import Enum

import pygad
import numpy as np
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
        # EComponentType.CPU: (0.1, 0.3),
        EComponentType.CPU: (0, 1),
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

    def _get_components_by_cost_interval(
        self,
        priorities: dict[EComponentType, tuple],
        component_type: EComponentType,
        need_rank=False,
    ) -> tuple[list[Component], list[VolatileData]]:
        priority = priorities[component_type]

        component, volatile_data = self.vd_message_bus.handle(
            GetVolatileDataByCostInterval(
                component_type,
                self.budget * priority[0],
                self.budget * priority[1],
                need_rank,
            )
        )

        return component, volatile_data

    def fit_func(self, components, volatile_data, xs):
        rank = np.sum(
            [
                comp[int(i) % len(comp)].rank
                for comp, i in zip(components, xs)
                if len(comp) != 0
            ]
        )

        cost = np.sum(
            [
                vd[int(i) % len(vd)].cost.amount
                for vd, i in zip(volatile_data, xs)
                if len(vd) != 0
            ]
        )

        if cost > self.budget:
            return -1
        else:
            return rank

    def generate_computer(self) -> list[Component]:
        component_priorities = _component_priorities[self.purpose]

        cpus, cpus_vd = self._get_components_by_cost_interval(
            component_priorities, EComponentType.CPU, True
        )
        gpus, gpus_vd = self._get_components_by_cost_interval(
            component_priorities, EComponentType.GPU, True
        )
        rams, rams_vd = self._get_components_by_cost_interval(
            component_priorities, EComponentType.RAM, True
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

        components = [cpus, gpus, rams, motherboards, persistences, psus]
        volatile_data = [
            cpus_vd,
            gpus_vd,
            rams_vd,
            motherboards_vd,
            persistences_vd,
            psus_vd,
        ]

        for i, cpu in enumerate(cpus):
            if isinstance(cpu, CPUComponent) and self.budget < _gpu_price_thresh:
                if cpu.integrated_gpu is None or len(cpu.integrated_gpu) == 0:
                    del cpus[i]
                    del cpus_vd[i]

        fitness_func = lambda xs, _: self.fit_func(components, volatile_data, xs)

        fitness_function = fitness_func
        num_generations = 100
        num_parents_mating = 4
        sol_per_pop = 8
        num_genes = len(components)
        init_range_low = -2
        init_range_high = 5
        parent_selection_type = "sss"
        keep_parents = 1
        crossover_type = "single_point"
        mutation_type = "random"
        mutation_percent_genes = 10

        ga_instance = pygad.GA(
            num_generations=num_generations,
            num_parents_mating=num_parents_mating,
            fitness_func=fitness_function,
            sol_per_pop=sol_per_pop,
            num_genes=num_genes,
            init_range_low=init_range_low,
            init_range_high=init_range_high,
            parent_selection_type=parent_selection_type,
            keep_parents=keep_parents,
            crossover_type=crossover_type,
            mutation_type=mutation_type,
            mutation_percent_genes=mutation_percent_genes,
        )

        ga_instance.run()
        solution, solution_fitness, solution_idx = ga_instance.best_solution()

        print(solution)
        print(solution_fitness)

        return []
