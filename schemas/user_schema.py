from pydantic import BaseModel, EmailStr

class User(BaseModel):
    id: str | None = None
    username: str | None = None
    email: EmailStr 
    password: str
    is_active: bool = False
    role: str | None = None
    confirmation_token: str | None = None

class CreateUser(BaseModel):
    id: str
    username: str
    email: EmailStr

class RefreshToken(BaseModel):
    refresh_token: str