from typing import List
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.dialects.mysql import (
    INTEGER,
    VARCHAR,
    BOOLEAN,
    ENUM,
    DATE,
    DATETIME,
    FLOAT,
)

from .binaryUUID import BinaryUUID
from framework.domain.components import *


def get_attrs(ctype: EComponentType) -> List[str]:
    ret = _component_attrs_idx[EComponentType._BASE].copy()

    if ctype != EComponentType._BASE:
        ret.extend(_component_attrs_idx[ctype])

    return ret


base = declarative_base()


class UserInstance(base):
    __tablename__ = "users"
    uid = Column(INTEGER(5), primary_key=True, autoincrement=False)
    is_admin = Column(BOOLEAN())
    email = Column(VARCHAR(150))
    password = Column(VARCHAR(20))
    name = Column(VARCHAR(128))


_AttrsComponent = ["uid", "type", "manufacturer", "model"]


class ComponentInstance(base):
    __tablename__ = "components"
    uid = Column(BinaryUUID, primary_key=True)
    component_uid = None
    type = Column(ENUM(EComponentType))
    manufacturer = Column(VARCHAR(20))
    model = Column(VARCHAR(10))


class VolatileDataInstance(base):
    __tablename__ = "volatile_datas"
    url_id = Column(BinaryUUID, primary_key=True)
    url = Column(VARCHAR(255))
    component_uid = Column(BinaryUUID, ForeignKey(ComponentInstance.uid))
    cost = Column(FLOAT(7, 2, False))
    availability = Column(BOOLEAN())
    timestamp = Column(DATETIME(timezone=False, fsp=0))

AttrsVolatileData = [
    'url_id',
    'url',
    'component_uid',
    'cost',
    'availability',
    'timestamp',
]

class PriceHistoryInstance(base):
    __tablename__ = "prices_history"
    uid = Column(BinaryUUID, primary_key=True)
    component_uid = Column(BinaryUUID, ForeignKey(ComponentInstance.uid))
    price = Column(FLOAT(7, 2, False))
    price_mean = Column(FLOAT(7, 2, False))
    timestamp = Column(DATE)


_AttrsMotherboard = [
    "chipset",
    "board_size",
    "n_ram_slots",
    "consumption",
    "n_usb2",
    "n_usb3x",
    "n_vga",
    "n_hdmi",
    "n_display_port",
    "pcie_gen",
    "n_pcie_x1",
    "n_pcie_x4",
    "n_pcie_x8",
    "n_pcie_x16",
]


class MotherboardInstance(ComponentInstance):
    __tablename__ = "motherboards"
    component_uid = Column(
        BinaryUUID, ForeignKey(ComponentInstance.uid), primary_key=True
    )
    consumption = Column(INTEGER(5))
    chipset = Column(ENUM(EChipsetType))
    board_size = Column(ENUM(EBoardSize))
    n_ram_slots = Column(INTEGER(1))

    n_usb2 = Column(INTEGER(1))
    n_usb3x = Column(INTEGER(1))

    n_vga = Column(INTEGER(1))
    n_hdmi = Column(INTEGER(1))
    n_display_port = Column(INTEGER(1))

    pcie_gen = Column(ENUM(EPCIeGeneration))
    n_pcie_x1 = Column(INTEGER(1))
    n_pcie_x4 = Column(INTEGER(1))
    n_pcie_x8 = Column(INTEGER(1))
    n_pcie_x16 = Column(INTEGER(1))


_AttrsCPU = [
    "socket",
    "n_cores",
    "base_clock_spd",
    "boost_clock_spd",
    "ram_clock_max",
    "consumption",
    "integrated_gpu",
    "overclock",
]


class CPUInstance(ComponentInstance):
    __tablename__ = "CPUs"
    component_uid = Column(
        BinaryUUID, ForeignKey(ComponentInstance.uid), primary_key=True
    )
    consumption = Column(INTEGER(5))
    socket = Column(ENUM(ESocketType))
    n_cores = Column(INTEGER(1))
    base_clock_spd = Column(FLOAT(4, 2, True))
    boost_clock_spd = Column(FLOAT(4, 2, False))
    ram_clock_max = Column(INTEGER(5))
    integrated_gpu = Column(VARCHAR(30))
    overclock = Column(BOOLEAN())


_AttrsGPU = ["consumption", "vram", "vram_spd"]


class GPUInstance(ComponentInstance):
    __tablename__ = "GPUs"
    component_uid = Column(
        BinaryUUID, ForeignKey(ComponentInstance.uid), primary_key=True
    )
    consumption = Column(INTEGER(5))
    vram = Column(INTEGER(2))
    vram_spd = Column(INTEGER(5))


_AttrsRAM = ["generation", "frequency"]


class RAMInstance(ComponentInstance):
    __tablename__ = "RAMs"
    component_uid = Column(
        BinaryUUID, ForeignKey(ComponentInstance.uid), primary_key=True
    )
    generation = Column(ENUM(ERAMGeneration))
    frequency = Column(INTEGER(5))


_AttrsPersistence = ["storage", "spd", "io", "is_HDD"]


class PersistenceInstance(ComponentInstance):
    __tablename__ = "persistences"
    component_uid = Column(
        BinaryUUID, ForeignKey(ComponentInstance.uid), primary_key=True
    )
    is_HDD = Column(BOOLEAN())
    storage = Column(INTEGER(5))
    spd = Column(INTEGER(5))
    io = Column(ENUM(EPersistenceIOType))


_AttrsPSU = ["power", "rate", "modularity"]


class PSUInstance(ComponentInstance):
    __tablename__ = "PSUs"
    component_uid = Column(
        BinaryUUID, ForeignKey(ComponentInstance.uid), primary_key=True
    )
    power = Column(INTEGER(4))
    rate = Column(ENUM(EPSURate))
    modularity = Column(ENUM(EPSUModularity))


class ComputerInstance(base):
    __tablename__ = "computers"
    uid = Column(INTEGER(6), primary_key=True, autoincrement=False)
    user = Column(INTEGER(5), ForeignKey("users.uid"))
    total_consumption = Column(INTEGER(5))
    price = Column(FLOAT(7, 2, False))
    motherboard_uid = Column(BinaryUUID, ForeignKey(MotherboardInstance.component_uid))
    CPU_uid = Column(BinaryUUID, ForeignKey(CPUInstance.component_uid))
    GPU_uid = Column(BinaryUUID, ForeignKey(GPUInstance.component_uid))
    RAM_uid = Column(BinaryUUID, ForeignKey(RAMInstance.component_uid))
    ram_quant = Column(INTEGER(1))
    PSU_uid = Column(BinaryUUID, ForeignKey(PSUInstance.component_uid))


computer_persistence_relation = Table(
    "computer_persistence",
    base.metadata,
    Column("computer_uid", ForeignKey(ComputerInstance.uid)),
    Column("persistence_uid", ForeignKey(PersistenceInstance.component_uid)),
)


class CategoryUrlInstance(base):
    __tablename__ = "category_url"
    uid = Column(INTEGER(5), primary_key=True, autoincrement=False)
    domain = Column(VARCHAR(100))
    path = Column(VARCHAR(150))
    type = Column(ENUM(EComponentType))


component_inst_idx = [
    ComponentInstance,
    MotherboardInstance,
    CPUInstance,
    GPUInstance,
    RAMInstance,
    PersistenceInstance,
    PSUInstance,
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
