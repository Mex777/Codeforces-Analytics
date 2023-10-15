import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_USERNAME = os.getenv("DATABASE_USERNAME")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_PORT = os.getenv("DATABASE_PORT")
POSTGRES_CONNECTION_URL = os.getenv("POSTGRESQL_DATABASE_CONNECTION_LINK")

DATABASE_CONNECTION_URL = f'mysql+mysqlconnector://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}'

DATABASE_CONFIG = {
  'user': DATABASE_USERNAME,
  'password': DATABASE_PASSWORD,
  'host': DATABASE_HOST,
  'database': DATABASE_NAME,
  'port': DATABASE_PORT
}
