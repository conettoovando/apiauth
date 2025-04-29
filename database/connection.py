from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

URL_DATABASE = "mysql+pymysql://root:1972@localhost:3306/auth"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

engine = create_engine(URL_DATABASE)
SessionLocal = sessionmaker(autoflush=True, bind=engine)

Base = declarative_base()