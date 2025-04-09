# auth/auth_routes.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db
from auth.jwt_handler import create_access_token, verify_token
import controllers.user_controller as user_controller, schemas.user_schema as user_schema
import bcrypt
import jwt

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: user_schema.User, db: Session = Depends(get_db)):
    db_user = user_controller.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="El nombre de usuario ya existe")

    db_user = await user_controller.create_user(db, user)
    return {"msg": "Usuario registrado correctamente", "user": user.username}

@router.post("/login")
async def login(user: user_schema.User, db: Session = Depends(get_db)):
    db_user = user_controller.get_user_by_username(db, user.username)
    if db_user is None or not bcrypt.checkpw(user.password.encode('utf-8'), db_user.password.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    token = create_access_token({"sub": db_user.id, "username": db_user.username})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me")
async def me(token: str = Depends(oauth2_scheme)):
    try:
        user = verify_token(token)
        return {"msg": "Token válido", "user": user}
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
