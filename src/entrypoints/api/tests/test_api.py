import pytest
import requests
from entrypoints.api.endpoints import cpus

url = "http://127.0.0.1:5000/api/v1"


@pytest.fixture()
def create_components():
    headers = {"Content-Type": "application/json"}
    cpu = {
        "manufacturer": "intel",
        "model": "i710310",
        "socket": "lga1200",
        "n_cores": 6,
        "base_clock_spd": 3.8,
        "boost_clock_spd": 4.6,
        "ram_clock_max": 3200,
        "consumption": 100,
        "integrated_gpu": "",
        "overclock": True,
    }

    gpu = {
        "manufacturer": "nvidia",
        "model": "1070",
        "consumption": 10,
        "vram": 8,
        "vram_spd": 4,
    }

    motherboard = {
        "manufacturer": "MSI",
        "model": "B560M-A PRO",
        "chipset": 0,
        "board_size": 0,
        "n_ram_slots": 4,
        "consumption": 20,
        "n_usb2": 2,
        "n_usb3x": 1,
        "n_vga": 0,
        "n_hdmi": 1,
        "n_display_port": 0,
        "pcie_gen": 0,
        "n_pcie_x1": 0,
        "n_pcie_x4": 1,
        "n_pcie_x8": 0,
        "n_pcie_x16": 0,
    }
    persistence = {
        "manufacturer": "Kingston",
        "model": "SA400S37/240G",
        "storage": 240,
        "spd": 500,
        "io": 0,
        "is_HDD": False,
    }
    psu = {
        "manufacturer": "XPG",
        "model": "XPG 650W",
        "power": 650,
        "rate": 0,
        "modularity": 0,
    }
    ram = {
        "manufacturer": "Rise Mode Gamer",
        "model": "Z Series 8GB Preta ",
        "generation": 0,
        "frequency": 3200,
    }

    return headers, cpu, gpu, motherboard, persistence, psu, ram


@pytest.mark.unit
def test_gets_post_cpu(create_components):
    headers, cpu, gpu, motherboard, persistence, psu, ram = create_components
    result = requests.post(f"{url}/cpus/", headers=headers, json=cpu)
    # CPU Testes
    assert result.json() == cpu
    assert result.status_code == 201

    result = requests.get(f"{url}/cpus/")

    cpu_list = result.json()
    _cpu = cpu_list[0]
    cpu_id = _cpu.pop("_id")

    assert len(cpu_list) == 1
    assert _cpu == cpu

    result = requests.get(f"{url}/cpus/{cpu_id}")

    _cpu = result.json()
    _cpu.pop("_id")

    assert _cpu == cpu

    # GPU Testes
    result = requests.post(f"{url}/gpus/", headers=headers, json=gpu)

    assert result.json() == gpu
    assert result.status_code == 201

    result = requests.get(f"{url}/gpus/")

    gpu_list = result.json()
    _gpu = gpu_list[0]
    gpu_id = _gpu.pop("_id")

    assert len(gpu_list) == 1
    assert _gpu == gpu

    result = requests.get(f"{url}/gpus/{gpu_id}")

    _gpu = result.json()
    _gpu.pop("_id")
    assert _gpu == gpu

    # PSU Testes
    result = requests.post(f"{url}/psus/", headers=headers, json=psu)

    assert result.json() == psu
    assert result.status_code == 201

    result = requests.get(f"{url}/psus/")

    psu_list = result.json()
    _psu = psu_list[0]
    psu_id = _psu.pop("_id")

    assert len(psu_list) == 1
    assert _psu == psu
    result = requests.get(f"{url}/psus/{psu_id}")

    _psu = result.json()
    _psu.pop("_id")
    assert psu == _psu

    # Persistence Testes
    result = requests.post(f"{url}/persistences/", headers=headers, json=persistence)

    assert result.json() == persistence
    assert result.status_code == 201

    result = requests.get(f"{url}/persistences/")

    persistence_list = result.json()
    _persistence = persistence_list[0]
    persistence_id = _persistence.pop("_id")

    assert len(persistence_list) == 1
    assert _persistence == persistence
    result = requests.get(f"{url}/persistences/{persistence_id}")

    _persistence = result.json()
    _persistence.pop("_id")

    # motherboard Testes
    result = requests.post(f"{url}/motherboards/", headers=headers, json=motherboard)

    assert result.json() == motherboard
    assert result.status_code == 201

    result = requests.get(f"{url}/motherboards/")

    motherboard_list = result.json()
    _motherboard = motherboard_list[0]
    motherboard_id = _motherboard.pop("_id")

    assert len(motherboard_list) == 1
    assert _motherboard == motherboard
    result = requests.get(f"{url}/motherboards/{motherboard_id}")

    _motherboard = result.json()
    _motherboard.pop("_id")
    assert motherboard == _motherboard

    # RAM Testes
    result = requests.post(f"{url}/rams/", headers=headers, json=ram)

    assert result.json() == ram
    assert result.status_code == 201

    result = requests.get(f"{url}/rams/")
    ram_list = result.json()
    _ram = ram_list[0]
    ram_id = _ram.pop("_id")

    assert len(ram_list) == 1
    assert _ram == ram

    result = requests.get(f"{url}/rams/{ram_id}")
    _ram = result.json()
    _ram.pop("_id")

    assert _ram == ram
