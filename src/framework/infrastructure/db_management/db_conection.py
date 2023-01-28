from sqlalchemy.engine.base import Engine
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_username = 'root'
db_password = '12345678'
db_address = '127.0.0.1'
db_port = '3306'
db_name = 'wisebuilder'

engine : Engine = None

def get_engine() -> Engine:
    
    global engine
    if engine == None:
        engine = create_engine(f'mariadb+mariadbconnector://{db_username}:{db_password}@{db_address}:{db_port}/{db_name}')
    return engine

def create_session(engine : Engine):
    session = sessionmaker()
    session.configure(bind=engine)
    session = session()