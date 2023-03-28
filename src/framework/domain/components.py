from enum import IntEnum
from dataclasses import dataclass
from typing import List

from .entity import Entity
from .components_enums import *

__all__ = [
    "Component",
    "GPUComponent",
    "CPUComponent",
    "MotherboardComponent",
    "RAMComponent",
    "PersistenceComponent",
    "PSUComponent",
    "component_cls_idx",
    "_component_attrs_idx",
]


_AttrsComponent = ["type", "manufacturer", "model", "rank"]
_AttrsCommon = ["_id"]


@dataclass(kw_only=True, eq=False)
class Component(Entity):
    type: EComponentType = EComponentType._BASE
    manufacturer: str
    model: str

    rank: int = 0

    def __hash__(self):
        return hash(self.uid)

    @classmethod
    def get_attrs(cls, ctype: EComponentType) -> List[str]:
        ret = _AttrsCommon.copy()
        ret.extend(_AttrsComponent)

        if ctype != EComponentType._BASE:
            ret.extend(_component_attrs_idx[ctype].copy())

        return ret


_AttrsMotherboard = [
    "chipset",
    "board_size",
    "n_ram_slots",
    "memory_type",
    "sata",
    "n_usb",
    "n_vga",
    "n_hdmi",
    "n_display_port",
    "n_pcie_x1",
    "n_pcie_x4",
    "n_pcie_x8",
    "n_pcie_x16",
]


@dataclass(kw_only=True, eq=False)
class MotherboardComponent(Component):
    type: EComponentType = EComponentType.MOTHERBOARD
    chipset: str
    board_size: EBoardSize
    n_ram_slots: int

    memory_type: ERAMGeneration

    sata: int

    n_usb: int

    n_vga: int
    n_hdmi: int
    n_display_port: int

    n_pcie_x1: int
    n_pcie_x4: int
    n_pcie_x8: int
    n_pcie_x16: int


_AttrsCPU = [
    "socket",
    "n_cores",
    "base_clock_spd",
    "boost_clock_spd",
    "consumption",
    "integrated_gpu",
    "overclock",
]


@dataclass(kw_only=True, eq=False)
class CPUComponent(Component):
    type: EComponentType = EComponentType.CPU
    socket: str
    n_cores: int

    base_clock_spd: float
    boost_clock_spd: float
    consumption: int

    integrated_gpu: str
    overclock: bool


_AttrsGPU = ["consumption", "vram", "vram_spd"]


@dataclass(kw_only=True, eq=False)
class GPUComponent(Component):
    type: EComponentType = EComponentType.GPU
    consumption: int
    vram: int
    vram_spd: int


_AttrsRAM = ["msize", "generation", "frequency"]


@dataclass(kw_only=True, eq=False)
class RAMComponent(Component):
    type: EComponentType = EComponentType.RAM
    msize: int
    generation: ERAMGeneration
    frequency: int


_AttrsPersistence = ["storage", "rpm", "io", "is_HDD"]


@dataclass(kw_only=True, eq=False)
class PersistenceComponent(Component):
    type: EComponentType = EComponentType.PERSISTENCE
    storage: int
    io: EPersistenceIOType
    is_HDD: bool = False
    rpm: int = 0


_AttrsPSU = ["power", "rate", "modularity"]


@dataclass(kw_only=True, eq=False)
class PSUComponent(Component):
    type: EComponentType = EComponentType.PSU
    power: int
    rate: EPSURate
    modularity: EPSUModularity


component_cls_idx = [
    Component,
    MotherboardComponent,
    CPUComponent,
    GPUComponent,
    RAMComponent,
    PersistenceComponent,
    PSUComponent,
]

_component_attrs_idx = [
    _AttrsComponent,
    _AttrsMotherboard,
    _AttrsCPU,
    _AttrsGPU,
    _AttrsRAM,
    _AttrsPersistence,
    _AttrsPSU,
]
