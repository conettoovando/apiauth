from pydantic import BaseModel

class User(BaseModel):
    id: str | None = None
    username: str
    password: str