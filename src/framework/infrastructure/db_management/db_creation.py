import db_conection
import db_structure
from sqlalchemy_utils import database_exists, create_database

if not database_exists(db_conection.engine.url):
    create_database(db_conection.engine.url)
    
db_structure.base.metadata.create_all(db_conection.engine)