import configparser
import pathlib

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from models import Base

file_config = pathlib.Path(__file__).parent.parent.joinpath('config.ini')
config = configparser.ConfigParser()
config.read(file_config)

username = config.get('DB', 'USER')
password = config.get('DB', 'PASSWORD')
database_name = config.get('DB', 'DB_NAME')
domain = config.get('DB', 'DOMAIN')
port = config.get('DB', 'PORT')
url = f'postgresql://{username}:{password}@{domain}:{port}/{database_name}'

try:
    engine = create_engine(url)
    Base.metadata.create_all(engine)
    print("Таблиці успішно створено.")

except SQLAlchemyError as e:
    print("Помилка при створенні таблиць:", e)
