# auth/auth_routes.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session
from database.connection import get_db
from auth.jwt_handler import create_access_token, verify_token, get_payload
import controllers.user_controller as user_controller, schemas.user_schema as user_schema
import bcrypt
import jwt
from datetime import timedelta

ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

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
    
    payload = {
        "sub": db_user.id,
        "username": db_user.username,
        "role": db_user.role
    }

    access_token = create_access_token(
        data=payload,
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    refresh_token = create_access_token(
        data=payload,
        expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post('/refresh')
async def refresh_token(request: user_schema.RefreshToken):
    try:
        payload = get_payload(refresh_token=request.refresh_token)
        print("payload", payload)

        new_access_token = create_access_token(
            {"sub": payload["sub"], "username": payload["username"]},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )

        return {"access_token": new_access_token, "token_type": "bearer"}
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Refresh token invalido")

@router.get("/me")
async def me(token: str = Depends(oauth2_scheme)):
    print("Token-------")
    print(token)
    try:
        user = verify_token(token)
        print("user", user)
        return {"msg": "Token válido", "user": user, "token": token}
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
