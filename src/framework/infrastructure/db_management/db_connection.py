from sqlalchemy.engine.base import Engine
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def create_new_engine(db_username, db_password, db_address, db_port, db_name) -> Engine:
    engine : Engine = create_engine(f'mariadb+mariadbconnector://{db_username}:{db_password}@{db_address}:{db_port}/{db_name}')
    return engine

def create_session(engine : Engine):
    session = sessionmaker()
    session.configure(bind=engine)
    session = session()

    return session