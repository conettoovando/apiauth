from sqlalchemy import String, Integer, Column, CHAR, VARCHAR, text
from database import Base

class User(Base):
    __tablename__="users"
    id = Column(CHAR(30), primary_key=True, index=True, server_default=text("UUID()"))
    username = Column(VARCHAR(30), nullable=False)
    password = Column(VARCHAR(255), nullable=False)