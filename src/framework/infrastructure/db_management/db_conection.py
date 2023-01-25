import sqlalchemy

db_user = 'root'
db_password = '12345678'
db_address = '127.0.0.1'
db_port = '3306'
db_name = 'wisebuilder'

engine = sqlalchemy.create_engine(f'mariadb+mariadbconnector://{db_user}:{db_password}@{db_address}:{db_port}/{db_name}')

def create_session():
    session = sqlalchemy.orm.sessionmaker()
    session.configure(bind=engine)
    session = session()