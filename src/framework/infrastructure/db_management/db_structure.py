from typing import List
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.types import LargeBinary
from sqlalchemy.dialects.mysql import (
    INTEGER,
    VARCHAR,
    BOOLEAN,
    ENUM,
    DATE,
    DATETIME,
    FLOAT,
)

from framework.domain.components_enums import *
from .binaryUUID import BinaryUUID
from framework.domain.components import *
from framework.domain.components_enums import *


def get_attrs(ctype: EComponentType) -> List[str]:
    ret = _component_attrs_idx[EComponentType._BASE].copy()

    if ctype != EComponentType._BASE:
        ret.extend(_component_attrs_idx[ctype])

    return ret


base = declarative_base()

AttrsUserInstance = ["uid", "email", "name", "is_admin"]


class UserInstance(base):
    __tablename__ = "users"
    uid = Column(BinaryUUID, primary_key=True)
    email = Column(VARCHAR(150))
    name = Column(VARCHAR(128))
    password = Column(LargeBinary())
    salt = Column(LargeBinary())
    is_admin = Column(BOOLEAN())


_AttrsComponent = ["uid", "type", "manufacturer", "model", "rank"]


class ComponentInstance(base):
    __tablename__ = "components"
    uid = Column(BinaryUUID, primary_key=True)
    component_uid = None
    type = Column(ENUM(EComponentType))
    manufacturer = Column(VARCHAR(50))
    model = Column(VARCHAR(100))
    rank = Column(INTEGER(4))


AttrsVolatileData = [
    "url_id",
    "url",
    "component_uid",
    "component_type",
    "cost",
    "availability",
    "timestamp",
]


class VolatileDataInstance(base):
    __tablename__ = "volatile_data"
    url_id = Column(BinaryUUID, primary_key=True)
    url = Column(VARCHAR(255))
    component_uid = Column(BinaryUUID, ForeignKey(ComponentInstance.uid))
    component_type = Column(ENUM(EComponentType))
    cost = Column(FLOAT(7, 2, False))
    availability = Column(BOOLEAN())
    timestamp = Column(DATETIME(timezone=False, fsp=0))


class LowerCostsInstance(base):
    __tablename__ = "lower_costs"
    component_uid = Column(
        BinaryUUID, ForeignKey(ComponentInstance.uid), primary_key=True
    )
    volatile_data_uid = Column(BinaryUUID, ForeignKey(VolatileDataInstance.url_id))
    component_type = Column(ENUM(EComponentType))
    cost = Column(FLOAT(7, 2, False))
    timestamp = Column(DATE)


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


class MotherboardInstance(ComponentInstance):
    __tablename__ = "motherboards"
    component_uid = Column(
        BinaryUUID, ForeignKey(ComponentInstance.uid), primary_key=True
    )
    chipset = Column(VARCHAR(10))
    board_size = Column(ENUM(EBoardSize))
    n_ram_slots = Column(INTEGER(1))

    n_usb = Column(INTEGER(1))

    memory_type = Column(ENUM(ERAMGeneration))

    sata = Column(INTEGER(2))

    n_vga = Column(INTEGER(1))
    n_hdmi = Column(INTEGER(1))
    n_display_port = Column(INTEGER(1))

    n_pcie_x1 = Column(INTEGER(1))
    n_pcie_x4 = Column(INTEGER(1))
    n_pcie_x8 = Column(INTEGER(1))
    n_pcie_x16 = Column(INTEGER(1))


_AttrsCPU = [
    "socket",
    "n_cores",
    "base_clock_spd",
    "boost_clock_spd",
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
    socket = Column(VARCHAR(10))
    n_cores = Column(INTEGER(1))
    base_clock_spd = Column(FLOAT(4, 2, True))
    boost_clock_spd = Column(FLOAT(4, 2, False))
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


_AttrsRAM = [
    # "msize",
    "generation",
    "frequency",
]


class RAMInstance(ComponentInstance):
    __tablename__ = "RAMs"
    component_uid = Column(
        BinaryUUID, ForeignKey(ComponentInstance.uid), primary_key=True
    )
    # msize = Column(INTEGER(3))
    generation = Column(ENUM(ERAMGeneration))
    frequency = Column(INTEGER(5))


_AttrsPersistence = ["storage", "rpm", "io", "is_HDD"]


class PersistenceInstance(ComponentInstance):
    __tablename__ = "persistences"
    component_uid = Column(
        BinaryUUID, ForeignKey(ComponentInstance.uid), primary_key=True
    )
    is_HDD = Column(BOOLEAN())
    storage = Column(INTEGER(5))
    rpm = Column(INTEGER(5))
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
    uid = Column(BinaryUUID, primary_key=True)
    user = Column(BinaryUUID, ForeignKey("users.uid"))
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


class CategoryURLInstance(base):
    __tablename__ = "category_url"
    uid = Column(BinaryUUID, primary_key=True, autoincrement=False)
    category = Column(ENUM(EComponentType))
    scheme = Column(VARCHAR(8))
    domain = Column(VARCHAR(100))
    path = Column(VARCHAR(150))


AttrsCategoryURLInstance = ["uid", "category", "scheme", "domain", "path"]


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
