from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.user import User
from app.models.token import Token
from app.schemas.user import UserCreate, TokenPair
from app.services.token import save_refresh_token, hash_token
from app.utils.password import hash_password, verify_password
from app.core.security import create_access_token, decode_token
from app.core.config import settings
from app.utils.methods import format_datetime, get_now_utc
from jose import JWTError
from jose.exceptions import ExpiredSignatureError

def register_user(db: Session, data: UserCreate) -> User:
    if db.scalar(select(User).where(User.email == data.email)):
        raise ValueError("Email already registered")
    user = User(
        email = data.email,
        hashed_password = hash_password(data.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user 

def authenticate_user(db: Session, email: str, password: str) -> User | None:
    user = db.scalar(select(User).where(User.email == email))
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def issue_tokens(user: User, db: Session, client_ip: str | None = None, user_agent: str | None = None) -> TokenPair:
    access = create_access_token(str(user.id), settings.ACCESS_TOKEN_EXPIRE_MINUTES, "access", user.role)
    refresh = create_access_token(str(user.id), settings.REFRESH_TOKEN_EXPIRE_MINUTES, "refresh", user.role)

    # Guardar el refresh token en la base de datos
    save_refresh_token(
        db=db,
        user_id=user.id,
        refresh_token=refresh,
        expires_in=settings.REFRESH_TOKEN_EXPIRE_MINUTES,
        client_ip=client_ip,
        user_agent=user_agent
    )

    return TokenPair(access_token=access, refresh_token=refresh)

def refresh_access_token(refresh_token: str, db: Session) -> str:
    try:
        payload = decode_token(refresh_token)
        
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401 ,detail="Invalid token type")
        
        user_id = payload.get("sub")
        role = payload.get("role")
        if not isinstance(user_id, str) or not user_id or not isinstance(role, str) or not role:
            raise ValueError("Invalid user id in token")
        
        hashed = hash_token(refresh_token)
        
        token_entry = db.scalar(
            select(Token).where(
                Token.token_hash == hashed,
                Token.user_id == user_id,
                Token.is_active == True
            )
        )

        if not token_entry:
            raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
        
        if format_datetime(token_entry.expires_at) < get_now_utc():
            token_entry.is_active = False
            db.commit()

            raise HTTPException(status_code=401, detail="Refresh token expired")

        return create_access_token(user_id, settings.ACCESS_TOKEN_EXPIRE_MINUTES, "access", role)
    
    except ExpiredSignatureError:
        db.query(Token).filter(Token.token_hash == hash_token(refresh_token)).update({"is_active": False})
        db.commit()
        raise ValueError("Refresh token expired") from None

    except JWTError:
        raise ValueError("Invalid refresh token") from None