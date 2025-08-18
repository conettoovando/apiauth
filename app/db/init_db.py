import os
from sqlalchemy import text
from app.db.session import engine
from app.core.config import settings
from app.db.session import Base
from app.models.user import User

def reset_if_demo():
    if settings.DEMO_RESET and settings.SQLITE_URL.startswith("sqlite"):
        path = settings.SQLITE_URL.replace("sqlite:///", "")
        if os.path.exists(path):
            os.remove(path)

def init_db():
    Base.metadata.create_all(bind=engine)
    with engine.connect() as conn:
        conn.execute(text("select 1")) # Seleccionar para verificar la conexión
    