# main.py
from fastapi import FastAPI
from auth import auth_routes
from database.connection import engine
import models.user_model

app = FastAPI()

# Crear las tablas de la base de datos
models.user_model.Base.metadata.create_all(bind=engine)

# Incluir rutas de autenticación
app.include_router(auth_routes.router)
