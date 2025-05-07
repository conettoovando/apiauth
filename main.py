# main.py
from fastapi import FastAPI
from auth import auth_routes
from database.connection import engine
import users.user_model
from auth import jwt_routes

app = FastAPI()

# Crear las tablas de la base de datos
users.user_model.Base.metadata.create_all(bind=engine)

# Incluir rutas de autenticación
app.include_router(auth_routes.router)
app.include_router(jwt_routes.router)
