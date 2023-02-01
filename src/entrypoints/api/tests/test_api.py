import pytest
import requests
from entrypoints.api.endpoints import cpus

url = "http://127.0.0.1:5000/api/v1"


@pytest.fixture()
def post_cpu():
    cpu = {
        "manufacturer": "intel",
        "model": "i710310",
        "socket": "lga1200",
        "n_cores": "6",
        "base_clock_spd": 3.8,
        "boost_clock_spd": 4.6,
        "ram_clock_max": 3200,
        "consumption": 100,
        "integrated_gpu": "",
        "overclock": True,
    }
    headers = {"Content-Type": "application/json"}

    return headers, cpu


@pytest.mark.unit
def test_post_cpu(post_cpu):
    headers, cpu = post_cpu
    result = requests.post(f"{url}/cpus/", headers=headers, json=cpu)

    assert result.json() == cpu
    assert result.status_code == 201
