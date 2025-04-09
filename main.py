# main.py
from fastapi import FastAPI
from auth import auth_routes
import models
from database import engine

app = FastAPI()

# Crear las tablas de la base de datos
# models.Base.metadata.create_all(bind=engine)

# Incluir rutas de autenticación
app.include_router(auth_routes.router)
