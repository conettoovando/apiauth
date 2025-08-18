from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.user import User
from app.schemas.user import UserCreate, TokenPair
from app.utils.password import hash_password, verify_password
from app.core.security import create_access_token, decode_token
from app.core.config import settings
from jose import JWTError

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

def issue_tokens(user: User) -> TokenPair:
    access = create_access_token(str(user.id), settings.ACCESS_TOKEN_EXPIRE_MINUTES, "access")
    refresh = create_access_token(str(user.id), settings.REFRESH_TOKEN_EXPIRE_MINUTES, "refresh")
    return TokenPair(access_token=access, refresh_token=refresh)

def refresh_access_token(refresh_token: str) -> str:
    try:
        payload = decode_token(refresh_token)
        if payload.get("type") != "refresh":
            raise JWTError("Invalid token type")
        user_id = payload.get("sub")
        if not isinstance(user_id, str) or not user_id:
            raise ValueError("Invalid user id in token")
        return create_access_token(user_id, settings.ACCESS_TOKEN_EXPIRE_MINUTES, "access")
    except JWTError:
        raise ValueError("Invalid refresh token") from None