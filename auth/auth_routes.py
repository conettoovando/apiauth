# auth/auth_routes.py
from fastapi import APIRouter, Depends, HTTPException, Request, status, Response
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session
from database.connection import get_db
from auth.jwt_handler import create_access_token, verify_token, get_payload
import users.user_controller as user_controller, users.user_schema as user_schema
import bcrypt
import jwt
from datetime import timedelta

ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: user_schema.User, db: Session = Depends(get_db)):
    db_user = user_controller.get_user_by_email(db, user.email)

    if db_user:
        raise HTTPException(status_code=400, detail="El email de usuario ya existe")

    db_user = await user_controller.create_user(db, user)

    return {
        "success": "Usuario creado correctamente"
    }

@router.post("/login")
async def login(user: user_schema.User, db: Session = Depends(get_db), response: Response = Response()):
    db_user = user_controller.get_user_by_email(db, user.email)

    if db_user is None or not bcrypt.checkpw(user.password.encode('utf-8'), db_user.password.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    
    payload = {
        "id": str(db_user.id),
        "email": db_user.email,
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

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="none",
        max_age=60 * 60 * 24 * 7
    )

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="none"
    )

    response.set_cookie(
        key="token_type",
        value="bearer",
        httponly=False,
        secure=True,
        samesite="none"
    )

    return {
        "id": db_user.id
    }

@router.post('/refresh', status_code=status.HTTP_204_NO_CONTENT)
async def refresh_token(request: Request, response: Response = Response()):
    try :
        refresh = request.cookies.get("refresh_token")
        if refresh:
            payload = get_payload(refresh_token=refresh)

            new_access_token = create_access_token(
                payload,
                expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            )

            response.set_cookie(
                key="access_token",
                value=new_access_token,
                httponly=True,
                secure=True,
                samesite="none",
                max_age=60 * 60 * 24 * 7
            )

            return
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error en la información")
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Refresh token invalido")

@router.get("/me")
async def me(request: Request):
    try:
        #user = verify_token(token)
        token_ = request.cookies.get("access_token")
        if token_:
            user = verify_token(token_)
        
            return {"msg": "Token válido", "user": user}
        
        return {}
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def cerrar_session(response: Response):
    cookie_settings = {
        "httponly": True,
        "secure": True,
        "samesite": "none",
        "path": "/",  # opcional si lo usaste en set_cookie
    }

    response.delete_cookie("access_token", **cookie_settings)
    response.delete_cookie("refresh_token", **cookie_settings)
    
    # token_type era httponly=False, así que debe ir separado
    response.delete_cookie("token_type", secure=True, samesite="none", path="/")

    return {"message": "Sesión cerrada"}