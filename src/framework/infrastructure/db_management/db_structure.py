from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, BOOLEAN, ENUM, DATE, DATETIME, FLOAT

from .binaryUUID import BinaryUUID
from ....framework.domain.components import *

base = declarative_base()

class UserInstance(base):
    __tablename__ = 'users'
    uid = Column(INTEGER(5), primary_key = True, autoincrement = False)
    is_admin = Column(BOOLEAN())
    email = Column(VARCHAR(150))
    password = Column(VARCHAR(20))
    name = Column(VARCHAR(128))

class ComponentInstance(base):
    __tablename__ = 'components'
    uid = Column(BinaryUUID, primary_key = True)
    type = Column(ENUM(EComponentType))
    manufacturer = Column(VARCHAR(20))
    model = Column(VARCHAR(10))

class VolatileDataInstance(base):
    __tablename__ = 'volatile_datas'
    url_id = Column(BinaryUUID, primary_key = True)
    url = Column(VARCHAR(255))
    component_uid = Column(BinaryUUID, ForeignKey(ComponentInstance.uid))
    price = Column(FLOAT(7, 2, False))
    availability = Column(BOOLEAN())
    timestamp = Column(DATETIME(timezone=False, fsp=0))

class PriceHistoryInstance(base):
    __tablename__ = 'prices_history'
    uid = Column(BinaryUUID, primary_key = True)
    component_uid = Column(BinaryUUID, ForeignKey(ComponentInstance.uid))
    price = Column(FLOAT(7, 2, False))
    price_mean = Column(FLOAT(7, 2, False))
    timestamp = Column(DATE)

class MotherboardInstance(base):
    __tablename__ = 'motherboards'
    component_uid = Column(BinaryUUID, ForeignKey(ComponentInstance.uid), primary_key = True)
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
    
class CPUInstance(base):
    __tablename__ = 'CPUs'
    component_uid = Column(BinaryUUID, ForeignKey(ComponentInstance.uid), primary_key = True)
    consumption = Column(INTEGER(5))
    socket = Column(ENUM(ESocketType))
    n_cores = Column(INTEGER(1))
    base_clock_spd = Column(FLOAT(4, 2, True))
    boost_clock_spd = Column(FLOAT(4, 2, False))
    ram_clock_max = Column(INTEGER(5))
    integrated_gpu = Column(VARCHAR(30))
    overclock = Column(BOOLEAN())

class GPUInstance(base):
    __tablename__ = 'GPUs'
    component_uid = Column(BinaryUUID, ForeignKey(ComponentInstance.uid), primary_key = True)
    consumption = Column(INTEGER(5))
    vram = Column(INTEGER(2))
    vram_spd = Column(INTEGER(5))

class RAMInstance(base):
    __tablename__ = 'RAMs'
    component_uid = Column(BinaryUUID, ForeignKey(ComponentInstance.uid), primary_key = True)
    generation = Column(ENUM(ERAMGeneration))
    frequency = Column(INTEGER(5))

class PersistenceInstance(base):
    __tablename__ = 'persistences'
    component_uid = Column(BinaryUUID, ForeignKey(ComponentInstance.uid), primary_key = True)
    is_HDD = Column(BOOLEAN())
    storage = Column(INTEGER(5))
    spd = Column(INTEGER(5))
    io = Column(ENUM(EPersistenceIOType))

class PSUInstance(base):
    __tablename__ = 'PSUs'
    component_uid = Column(BinaryUUID, ForeignKey(ComponentInstance.uid), primary_key = True)
    power = Column(INTEGER(4))
    rate = Column(ENUM(EPSURate))
    modularity = Column(ENUM(EPSUModularity))

class ComputerInstance(base):
    __tablename__ = 'computers'
    uid = Column(INTEGER(6), primary_key = True, autoincrement = False)
    user = Column(INTEGER(5), ForeignKey('users.uid'))
    total_consumption = Column(INTEGER(5))
    price = Column(FLOAT(7, 2, False))
    motherboard_uid = Column(BinaryUUID, ForeignKey(MotherboardInstance.component_uid))
    CPU_uid = Column(BinaryUUID, ForeignKey(CPUInstance.component_uid))
    GPU_uid = Column(BinaryUUID, ForeignKey(GPUInstance.component_uid))
    RAM_uid = Column(BinaryUUID, ForeignKey(RAMInstance.component_uid))
    ram_quant = Column(INTEGER(1))
    PSU_uid = Column(BinaryUUID, ForeignKey(PSUInstance.component_uid))

computer_persistence_relation = Table(
    'computer_persistence',
    base.metadata,
    Column('computer_uid', ForeignKey(ComputerInstance.uid)),
    Column('persistence_uid', ForeignKey(PersistenceInstance.component_uid))
)

class CategoryUrlInstance(base):
    __tablename__ = 'category_url'
    uid = Column(INTEGER(5), primary_key = True, autoincrement = False)
    domain = Column(VARCHAR(100))
    path = Column(VARCHAR(150))
    type = Column(ENUM(EComponentType))
