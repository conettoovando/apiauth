from pydantic import BaseModel

class User(BaseModel):
    id: str | None = None
    username: str
    email: str | None = None
    password: str
    is_active: bool = False
    role: str | None = None
    confirmation_token: str | None = None

class RefreshToken(BaseModel):
    refresh_token: str