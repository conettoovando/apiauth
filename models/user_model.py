from sqlalchemy import Column, CHAR, String, text, Boolean
from database.connection import Base

class User(Base):
    __tablename__="users"

    id = Column(CHAR(36), primary_key=True, index=True, server_default=text("UUID()"))
    username = Column(String(255), unique=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=True)
    password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=False)
    role = Column(String(50), nullable=True)
    confirmation_token = Column(String(255), nullable=True)

