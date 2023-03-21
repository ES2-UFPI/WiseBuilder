from flask import Blueprint
from flask_restx import Api

# from .cpus import cpu_namespace
# from .gpus import gpu_namespace
# from .psus import psu_namespace
# from .motherboards import motherboard_namespace
# from .persistence import persistence_namespace
# from .ram import ram_namespace
from .search import search_namespace

blueprint: Blueprint = Blueprint("api", __name__, url_prefix="/api/v1")
api: Api = Api(
    blueprint,
    version="1.0",
    title="WiseBuilder API",
    description="API para consulta e montagem de componentes",
)

# api.add_namespace(cpu_namespace, "/cpus")
# api.add_namespace(gpu_namespace, "/gpus")
# api.add_namespace(psu_namespace, "/psus")
# api.add_namespace(motherboard_namespace, "/motherboards")
# api.add_namespace(persistence_namespace, "/persistences")
# api.add_namespace(ram_namespace, "/rams")
api.add_namespace(search_namespace, "/search")
