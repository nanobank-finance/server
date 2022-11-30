from sqlalchemy import create_engine, URL, MetaData, Table, Column, Integer, String
from dotenv import load_dotenv
import os

load_dotenv()

db_connection_params = URL.create(
    os.environ["DB_TYPE"],
    username=os.environ["DB_USER"],
    password=os.environ["DB_PASS"],
    host=os.environ["DB_HOST"],
    database=os.environ["DB_NAME"],
)

engine = create_engine(db_connection_params)
