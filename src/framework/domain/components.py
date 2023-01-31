from enum import IntEnum
from dataclasses import dataclass

from .entity import AggregateRoot

__all__ = ['Component',
           
           'GPUComponent',
           'CPUComponent',
           'MotherboardComponent',
           'RAMComponent',
           'PersistenceComponent',
           'PSUComponent',
           
           'EComponentType',
           'EChipsetType',
           'EBoardSize',
           'EPersistenceIOType',
           'EPSURate',
           'ERAMGeneration',
           'ESocketType',
           'EPCIeGeneration',
           'EPSUModularity',
           
           'component_cls_idx']


class EComponentType(IntEnum):
    _BASE       = 0
    MOTHERBOARD = 1
    CPU         = 2
    GPU         = 3
    RAM         = 4
    PERSISTENCE = 5
    PSU         = 6


class EPCIeGeneration(IntEnum):
    GEN3 = 0
    GEN4 = 1
    GEN5 = 2


class EPSURate(IntEnum):
    WHITE       = 0
    BRONZE      = 1
    SILVER      = 2
    GOLD        = 3
    PLATINUM    = 4
    TITANIUM    = 5


class EPersistenceIOType(IntEnum):
    SATA = 0
    M2   = 1
    NVME = 2


class ERAMGeneration(IntEnum):
    DDR3 = 0
    DDR4 = 1
    DDR5 = 2


class EBoardSize(IntEnum):
    PICO_ITX  = 0
    NANO_ITX  = 1
    MINI_ITX  = 2
    MICRO_ATX = 3
    STANDARD  = 4


class EChipsetType(IntEnum):
    TIPO = 0


class ESocketType(IntEnum):
    TIPO = 0


class EPSUModularity(IntEnum):
    NON  = 0
    SEMI = 1
    FULL = 2


@dataclass(kw_only=True, eq=False)
class Component(AggregateRoot):
    type        : EComponentType = EComponentType._BASE
    manufacturer: str
    model       : str
    
    def __hash__(self):
        return hash(self.uid)


@dataclass(kw_only=True, eq=False)
class MotherboardComponent(Component):
    type            : EComponentType = EComponentType.MOTHERBOARD
    chipset         : EChipsetType
    board_size      : EBoardSize
    n_ram_slots     : int
    consumption     : int
    
    n_usb2          : int
    n_usb3x         : int
    
    n_vga           : int
    n_hdmi          : int
    n_display_port  : int
    
    pcie_gen        : EPCIeGeneration
    n_pcie_x1       : int
    n_pcie_x4       : int
    n_pcie_x8       : int
    n_pcie_x16      : int


@dataclass(kw_only=True, eq=False)
class CPUComponent(Component):
    type            : EComponentType = EComponentType.CPU
    socket          : ESocketType
    n_cores         : int
    
    base_clock_spd  : float
    boost_clock_spd : float
    ram_clock_max   : int
    consumption     : int
    
    integrated_gpu  : str
    overclock       : bool


@dataclass(kw_only=True, eq=False)
class GPUComponent(Component):
    type: EComponentType = EComponentType.GPU
    consumption : int
    vram        : int
    vram_spd    : int


@dataclass(kw_only=True, eq=False)
class RAMComponent(Component):
    type        : EComponentType = EComponentType.RAM
    generation  : ERAMGeneration
    frequency   : int


@dataclass(kw_only=True, eq=False)
class PersistenceComponent(Component):
    type    : EComponentType = EComponentType.PERSISTENCE
    storage : int
    spd     : int
    io      : EPersistenceIOType
    is_HDD  : bool


@dataclass(kw_only=True, eq=False)
class PSUComponent(Component):
    type        : EComponentType = EComponentType.PSU
    power       : int
    rate        : EPSURate
    modularity  : EPSUModularity


component_cls_idx = [
    Component,
    MotherboardComponent,
    CPUComponent,
    GPUComponent,
    RAMComponent,
    PersistenceComponent,
    PSUComponent
]