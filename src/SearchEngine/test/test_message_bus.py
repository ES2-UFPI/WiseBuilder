import pytest

from framework.domain.value_object import UUIDv4
from framework.application.handler import MessageBus

from framework.domain.components import GPUComponent, CPUComponent
from SearchEngine.domain.commands import *
from SearchEngine.domain.repositories import (
    EntityUIDCollisionException,
    EntityUIDNotFoundException
)

from SearchEngine.application.unit_of_work import MockUnitOfWork
from SearchEngine.application.handlers import COMMAND_HANDLER_MAPPER


@pytest.fixture
def message_bus():
    uow = MockUnitOfWork({})
    COMMAND_HANDLER_MAPPER_CALLABLE = {}
    for c, h in COMMAND_HANDLER_MAPPER.items():
        COMMAND_HANDLER_MAPPER_CALLABLE[c] = h(uow)
    
    return MessageBus(uow, {}, COMMAND_HANDLER_MAPPER_CALLABLE)

@pytest.fixture
def add_commands():
    uuid = UUIDv4()
    component = CPUComponent(**{
            '_id'            : uuid,
            'manufacturer'   : 'intel',
            'model'          : 'i710310',
            
            'socket'         : 'lga1200',
            'n_cores'        : '6',

            'base_clock_spd' : 3.8,
            'boost_clock_spd': 4.6,
            'ram_clock_max'  : 3200,
            'consumption'    : 100,

            'integrated_gpu'  : '',
            'overclock'      : True,
        }
    )
    
    direct_add = AddComponent(component)
    
    indirect_add = AddComponent.buildGPU(**
        {
            'manufacturer': 'nvidia',
            'model'       : '1070',
            
            'consumption' : 10,
            'vram'        : 8,
            'vram_spd'    : 4,
        }
    )
    
    return direct_add, indirect_add, component, uuid

@pytest.mark.unit
def test_add_component(message_bus, add_commands):
    direct_add, indirect_add, *_ = add_commands
    
    assert message_bus.handle(direct_add)
    assert message_bus.handle(indirect_add)
    
    with pytest.raises(EntityUIDCollisionException) as exc:
        message_bus.handle(direct_add)

@pytest.mark.unit
def test_read_component(message_bus, add_commands):
    direct_add, indirect_add, component, uuid = add_commands
    
    message_bus.handle(direct_add)
    message_bus.handle(indirect_add)
    
    gpu_list = message_bus.handle(ListComponentsByType.GPU())
    
    assert len(gpu_list) == 1 \
        and isinstance(gpu_list[0], GPUComponent)
    
    assert message_bus.handle(GetComponentByUID(uuid)) == component
    
    with pytest.raises(EntityUIDNotFoundException):
        message_bus.handle(GetComponentByUID(UUIDv4()))
