from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
import hashlib
from app.models.token import Token

def hash_token(token: str) -> str:
    """Genera un hash SHA-256 para no guardar el token en texto plano."""
    return hashlib.sha256(token.encode()).hexdigest()

def save_refresh_token(user_id: int, refresh_token:str, expires_in: int, db: Session, client_ip: str | None = None, user_agent: str | None = None) -> Token:
    """Guarda el refresh token en la base de datos con hash y fecha de expiracion."""
    hashed = hash_token(refresh_token)
    
    token_obj = Token(
        user_id=user_id,
        token_hash=hashed,
        is_active=True,
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=expires_in),
        ip_address=client_ip,
        user_agent=user_agent
    )

    db.add(token_obj)
    db.commit()
    db.refresh(token_obj)
    return token_obj