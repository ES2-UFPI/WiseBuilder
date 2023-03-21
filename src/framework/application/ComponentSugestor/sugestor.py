from enum import Enum

from framework.domain.components import EComponentType, Component


class EComputerPurposes(Enum):
    GAMING = 0
    STUDYING = 1
    PROGRAMMING = 2
    WEB_BROWSING = 3


_component_priorities = {
    EComputerPurposes.GAMING: {
        EComponentType.GPU: 1,
        EComponentType.CPU: 0.8,
        EComponentType.RAM: 0.7,
        EComponentType.PERSISTENCE: 0.5,
    },
    EComputerPurposes.STUDYING: {
        EComponentType.GPU: 0.2,
        EComponentType.CPU: 1,
        EComponentType.RAM: 0.7,
        EComponentType.PERSISTENCE: 0.6,
    },
    # TODO completar o dicionário com as prioridades
}

_component_specs_priorities = {
    EComponentType.GPU: {
        "vram": 1,
        "consumption": 0.8,
    },
    EComponentType.CPU: {
        "base_clock_spd": 1,
        "n_cores": 0.7,
        "ram_clock_max": 0.7,
        "consumption": 0.5,
    }
    # TODO completar o dicionário com as prioridade de especificações
}


class ComponentSugestor:
    def __init__(self, budget: float, purpose: EComputerPurposes):
        self.budget = budget
        self.purpose = purpose

    def generate_computer() -> dict[EComponentType, Component]:
        # TODO restringe o custo por componente.
        # TODO define custo estimado para PS
        # TODO Fitra componentes abaixo de seus custos limite.
        # TODO if prioridade GPU == 0, filtrar CPUS com GPU integrada
        # TODO calcula sua 'pontuação' com base na prioridade de suas especificações.
        # TODO Executa problema da mochila, restringindo com base na compatibilidade.
        # TODO somar consumo total e definir fonte com o orçamento estabelecido.
        # TODO caso o orçamento não seja totalmente preenchido, aumentar o orçamento do item prioritário, mantendo as compatibilidades anteriores

        pass
