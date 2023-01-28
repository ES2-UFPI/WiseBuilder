from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, BOOLEAN, DOUBLE

base = declarative_base()

class UserInstance(base):
    __tablename__ = 'users'
    id = Column(INTEGER(5), primary_key = True, autoincrement = False)
    is_admin = Column(BOOLEAN(1))
    email = Column(VARCHAR(150))
    password = Column(VARCHAR(20))
    name = Column(VARCHAR(128))
    
class ComponentType(base):
    __tablename__ = 'component_types'
    id = Column(INTEGER(1), primary_key = True, autoincrement = False)
    name = Column(VARCHAR(15))

class RamClasses(base):
    __tablename__ = 'ram_classes'
    id = Column(INTEGER(2), primary_key = True, autoincrement = False)
    name = Column(VARCHAR(10))

class PSUClasses(base):
    __tablename__ = 'psu_classes'
    id = Column(INTEGER(2), primary_key = True, autoincrement = False)
    name = Column(VARCHAR(20))

class MotherboardOutputTypesInstance(base):
    __tablename__ = 'motherboard_output_types'
    id = Column(INTEGER(2), primary_key = True, autoincrement = False)
    name = Column(VARCHAR(20))

class VolatileDataInstance(base):
    __tablename__ = 'volatile_datas'
    id = Column(INTEGER(5), primary_key = True, autoincrement = False)
    component = Column(INTEGER(5), ForeignKey('components.id'))
    domain = Column(VARCHAR(100))
    path = Column(VARCHAR(150))
    price = Column(DOUBLE(5, 2))
    disponibible = Column(BOOLEAN(1))

class ComponentInstance(base):
    __tablename__ = 'components'
    id = Column(INTEGER(5), primary_key = True, autoincrement = False)
    type = Column(INTEGER(1), ForeignKey('component_types.id'))
    manufacturer = Column(VARCHAR(20))
    model = Column(VARCHAR(10))

class MotherboardInstance(base):
    __tablename__ = 'motherboards'
    id = Column(INTEGER(5), primary_key = True, autoincrement = False)
    component = Column(INTEGER(5), ForeignKey('components.id'))
    consumption = Column(INTEGER(5))
    socket = Column(VARCHAR(10))
    size = Column(VARCHAR(16))
    ram_slots = Column(INTEGER(1))
    pcie_generation = Column(VARCHAR(10))
    pcie_ports = Column(INTEGER(1))
    outputs = Column(INTEGER(2), ForeignKey('motherboard_output_types.id'))

class CPUInstance(base):
    __tablename__ = 'cpu'
    id = Column(INTEGER(5), primary_key = True, autoincrement = False)
    component_id = Column(INTEGER(5), ForeignKey('components.id'))
    consumption = Column(INTEGER(5))
    socket = Column(VARCHAR(10))
    cores_count = Column(INTEGER(1))
    clock_base_vel = Column(DOUBLE(2, 2))
    clock_max_vel = Column(DOUBLE(2, 2))
    ram_max_clock = Column(INTEGER(5))
    integrated_gpu = Column(VARCHAR(25))
    overclock = Column(BOOLEAN(1))

class GPUInstance(base):
    __tablename__ = 'gpu'
    id = Column(INTEGER(5), primary_key = True, autoincrement = False)
    component_id = Column(INTEGER(5), ForeignKey('components.id'))
    consumption = Column(INTEGER(5))
    vram = Column(INTEGER(2))
    vram_vel = Column(INTEGER(5))

class RamInstance(base):
    __tablename__ = 'ram'
    id = Column(INTEGER(5), primary_key = True, autoincrement = False)
    component_id = Column(INTEGER(5), ForeignKey('components.id'))
    classification = Column(INTEGER(2), ForeignKey('ram_classes.id'))
    frequency = Column(INTEGER(5))

class PersistenceInstance(base):
    __tablename__ = 'persistences'
    id = Column(INTEGER(5), primary_key = True, autoincrement = False)
    component_id = Column(INTEGER(5), ForeignKey('components.id'))
    is_HDD = Column(BOOLEAN(1))
    storage = Column(INTEGER(5))
    velocity = Column(INTEGER(5))

class PSUInstance(base):
    __tablename__ = 'psu'
    id = Column(INTEGER(5), primary_key = True, autoincrement = False)
    component_id = Column(INTEGER(5), ForeignKey('components.id'))
    wattage = Column(INTEGER(4))
    classification = Column(INTEGER(2), ForeignKey('psu_classes.id'))

class ComputerInstance(base):
    __tablename__ = 'computers'
    id = Column(INTEGER(6), primary_key = True, autoincrement = False)
    user = Column(INTEGER(5), ForeignKey('users.id'))
    total_consumption = Column(INTEGER(5))
    price = Column(DOUBLE(6, 2))
    motherboard_id = Column(INTEGER(5), ForeignKey('motherboards.id'))
    CPU_id = Column(INTEGER(5), ForeignKey('cpu.id'))
    GPU_id = Column(INTEGER(5), ForeignKey('gpu.id'))
    ram_id = Column(INTEGER(5), ForeignKey('ram.id'))
    ram_quant = Column(INTEGER(1))
    PSU_id = Column(INTEGER(5), ForeignKey('psu.id'))

computer_persistence_relation = Table(
    'computer_persistence',
    base.metadata,
    Column('computer_id', ForeignKey('computers.id')),
    Column('persistence_id', ForeignKey('persistences.id'))
)

class CategoryUrlInstance(base):
    __tablename__ = 'category_url'
    id = Column(INTEGER(5), primary_key = True, autoincrement = False)
    domain = Column(VARCHAR(100))
    path = Column(VARCHAR(150))
    type = Column(INTEGER(1), ForeignKey('component_types.id'))