from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseModel):
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev_secret_change_me")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 15))
    REFRESH_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES", 60 * 24))
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    DEMO_RESET: bool = os.getenv("DEMO_RESET", "1") == "1"
    SQLITE_URL: str = os.getenv("SQLITE_URL", "sqlite:///./db.sqlite3")

settings = Settings()
print(settings.model_dump())