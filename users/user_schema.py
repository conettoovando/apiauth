from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import Optional

class User(BaseModel):
    id: UUID | None = None
    username: str | None = None
    email: EmailStr 
    password: str
    is_active: bool = False
    role: str | None = None
    confirmation_token: str | None = None

class CreateUser(BaseModel):
    id: UUID
    username: Optional[str] = None
    email: EmailStr

class RefreshToken(BaseModel):
    refresh_token: str