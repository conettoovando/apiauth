from sqlalchemy import Column, CHAR, String, text, Boolean
from database.connection import Base
from sqlalchemy.dialects.postgresql import UUID

class User(Base):
    __tablename__="users"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, server_default=text("gen_random_uuid()"))
    email = Column(String(255), unique=True, index=True, nullable=True)
    username = Column(String(255), index=True)
    password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=False)
    role = Column(String(50), nullable=True)
    confirmation_token = Column(String(255), nullable=True)

