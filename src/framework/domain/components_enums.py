from enum import IntEnum, auto

__all__ = [
    "EComponentType",
    "EBoardSize",
    "EPersistenceIOType",
    "EPSURate",
    "ERAMGeneration",
    "EPCIeGeneration",
    "EPSUModularity",
]


class EComponentType(IntEnum):
    _BASE = 0
    MOTHERBOARD = 1
    CPU = 2
    GPU = 3
    RAM = 4
    PERSISTENCE = 5
    PSU = 6


class EPCIeGeneration(IntEnum):
    GEN3 = auto()
    GEN4 = auto()
    GEN5 = auto()


class EPSURate(IntEnum):
    Plus_Gold = auto()
    Plus_Platinum = auto()
    Plus_Bronze = auto()
    Plus_Titanium = auto()
    Plus = auto()
    Plus_Silver = auto()


class EPersistenceIOType(IntEnum):
    SATA = auto()
    NVM = auto()


class ERAMGeneration(IntEnum):
    DDR3 = auto()
    DDR3L = auto()
    DDR4 = auto()
    DDR5 = auto()


class EBoardSize(IntEnum):
    PICO_ITX = auto()
    NANO_ITX = auto()
    MINI_ITX = auto()
    MICRO_ATX = auto()
    STANDARD = auto()


class EPSUModularity(IntEnum):
    NON = auto()
    SEMI = auto()
    FULL = auto()
