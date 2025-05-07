from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")
DBNAMEDEV = os.getenv("dbnamedev")
APPTYPE = os.getenv('application_type')
DEV_PASSWORD = str(os.getenv('devpass'))
USER_DEV = str(os.getenv("userdev"))
DATABASE_URL = (
    f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"
    if APPTYPE == 'prod' 
    else f"postgresql+psycopg2://{USER_DEV}:{DEV_PASSWORD}@localhost:{PORT}/{DBNAMEDEV}"
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autoflush=False,bind=engine)

Base = declarative_base()