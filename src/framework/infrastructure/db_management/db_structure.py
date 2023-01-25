from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.dialects import mysql
from sqlalchemy.orm import declarative_base

base = declarative_base()

class User_instance(base):
    __tablename__ = 'users'
    id = Column(mysql.INTEGER(5), primary_key = True, autoincrement = False)
    is_admin = Column(mysql.BOOLEAN(1))
    email = Column(mysql.VARCHAR(150))
    password = Column(mysql.VARCHAR(20))
    name = Column(mysql.VARCHAR(128))
    
class Component_type(base):
    __tablename__ = 'component_types'
    id = Column(mysql.INTEGER(1), primary_key = True, autoincrement = False)
    name = Column(mysql.VARCHAR(15))

class Ram_classes(base):
    __tablename__ = 'ram_classes'
    id = Column(mysql.INTEGER(2), primary_key = True, autoincrement = False)
    name = Column(mysql.VARCHAR(10))

class PSU_classes(base):
    __tablename__ = 'psu_classes'
    id = Column(mysql.INTEGER(2), primary_key = True, autoincrement = False)
    name = Column(mysql.VARCHAR(20))

class Motherboard_output_types_instance(base):
    __tablename__ = 'motherboard_output_types'
    id = Column(mysql.INTEGER(2), primary_key = True, autoincrement = False)
    name = Column(mysql.VARCHAR(20))

class Datasheet_instance(base):
    __tablename__ = 'datasheets'
    id = Column(mysql.INTEGER(5), primary_key = True, autoincrement = False)
    manufacturer = Column(mysql.VARCHAR(20))
    model = Column(mysql.VARCHAR(10))

class Volatile_data_instance(base):
    __tablename__ = 'volatile_datas'
    id = Column(mysql.INTEGER(5), primary_key = True, autoincrement = False)
    component = Column(mysql.INTEGER(5), ForeignKey('components.id'))
    domain = Column(mysql.VARCHAR(100))
    path = Column(mysql.VARCHAR(150))
    price = Column(mysql.DOUBLE(5, 2))
    disponibible = Column(mysql.BOOLEAN(1))

class Component_instance(base):
    __tablename__ = 'components'
    id = Column(mysql.INTEGER(5), primary_key = True, autoincrement = False)
    type = Column(mysql.INTEGER(1), ForeignKey('component_types.id'))
    datasheet = Column(mysql.INTEGER(5), ForeignKey('datasheets.id'))

class Motherboard_instance(base):
    __tablename__ = 'motherboards'
    id = Column(mysql.INTEGER(5), primary_key = True, autoincrement = False)
    component = Column(mysql.INTEGER(5), ForeignKey('components.id'))
    consumption = Column(mysql.INTEGER(5))
    socket = Column(mysql.VARCHAR(10))
    size = Column(mysql.VARCHAR(16))
    ram_slots = Column(mysql.INTEGER(1))
    pcie_generation = Column(mysql.VARCHAR(10))
    pcie_ports = Column(mysql.INTEGER(1))
    outputs = Column(mysql.INTEGER(2), ForeignKey('motherboard_output_types.id'))

class CPU_instance(base):
    __tablename__ = 'cpu'
    id = Column(mysql.INTEGER(5), primary_key = True, autoincrement = False)
    component_id = Column(mysql.INTEGER(5), ForeignKey('components.id'))
    consumption = Column(mysql.INTEGER(5))
    socket = Column(mysql.VARCHAR(10))
    cores_count = Column(mysql.INTEGER(1))
    clock_base_vel = Column(mysql.DOUBLE(2, 2))
    clock_max_vel = Column(mysql.DOUBLE(2, 2))
    ram_max_clock = Column(mysql.INTEGER(5))
    integrated_gpu = Column(mysql.VARCHAR(25))
    overclock = Column(mysql.BOOLEAN(1))

class GPU_instance(base):
    __tablename__ = 'gpu'
    id = Column(mysql.INTEGER(5), primary_key = True, autoincrement = False)
    component_id = Column(mysql.INTEGER(5), ForeignKey('components.id'))
    consumption = Column(mysql.INTEGER(5))
    vram = Column(mysql.INTEGER(2))
    vram_vel = Column(mysql.INTEGER(5))

class ram_instance(base):
    __tablename__ = 'ram'
    id = Column(mysql.INTEGER(5), primary_key = True, autoincrement = False)
    component_id = Column(mysql.INTEGER(5), ForeignKey('components.id'))
    classification = Column(mysql.INTEGER(2), ForeignKey('ram_classes.id'))
    frequency = Column(mysql.INTEGER(5))

class persistence_instance(base):
    __tablename__ = 'persistences'
    id = Column(mysql.INTEGER(5), primary_key = True, autoincrement = False)
    component_id = Column(mysql.INTEGER(5), ForeignKey('components.id'))
    is_HDD = Column(mysql.BOOLEAN(1))
    storage = Column(mysql.INTEGER(5))
    velocity = Column(mysql.INTEGER(5))

class PSU_instance(base):
    __tablename__ = 'psu'
    id = Column(mysql.INTEGER(5), primary_key = True, autoincrement = False)
    component_id = Column(mysql.INTEGER(5), ForeignKey('components.id'))
    wattage = Column(mysql.INTEGER(4))
    classification = Column(mysql.INTEGER(2), ForeignKey('psu_classes.id'))

class Computer_instance(base):
    __tablename__ = 'computers'
    id = Column(mysql.INTEGER(6), primary_key = True, autoincrement = False)
    user = Column(mysql.INTEGER(5), ForeignKey('users.id'))
    total_consumption = Column(mysql.INTEGER(5))
    price = Column(mysql.DOUBLE(6, 2))
    motherboard_id = Column(mysql.INTEGER(5), ForeignKey('motherboards.id'))
    CPU_id = Column(mysql.INTEGER(5), ForeignKey('cpu.id'))
    GPU_id = Column(mysql.INTEGER(5), ForeignKey('gpu.id'))
    ram_id = Column(mysql.INTEGER(5), ForeignKey('ram.id'))
    ram_quant = Column(mysql.INTEGER(1))
    PSU_id = Column(mysql.INTEGER(5), ForeignKey('psu.id'))

computer_persistence_relation = Table(
    'computer_persistence',
    base.metadata,
    Column('computer_id', ForeignKey('computers.id')),
    Column('persistence_id', ForeignKey('persistences.id'))
)

class Category_url_instance(base):
    __tablename__ = 'category_url'
    id = Column(mysql.INTEGER(5), primary_key = True, autoincrement = False)
    domain = Column(mysql.VARCHAR(100))
    path = Column(mysql.VARCHAR(150))
    type = Column(mysql.INTEGER(1), ForeignKey('component_types.id'))