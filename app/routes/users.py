from fastapi import APIRouter, Depends, HTTPException
from app.core.security import decode_token
from app.dependecies import get_current_user
from app.schemas.user import UserOut
from app.models.user import User
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.middleware import require_admin

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserOut)
def me(current: User = Depends(get_current_user)):
    return current

@router.patch("/{user_id}/role")
def update_user_role(user_id: int, role: str, db: Session = Depends(get_db), current_user = Depends(require_admin)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.role = role
    db.commit()
    db.refresh(user)
    return {"msg": f"User {user_id} role updated to {role}"}

@router.get("/{user_id}/verify")
def verify_user_email(user_id: int, token: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.is_verified:
        return {"msg": "User already verified"}
    
    _token = decode_token(token)

    if not _token:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    
    if _token.get("sub") != str(user_id) or _token.get("type") != "email_verification":
        raise HTTPException(status_code=400, detail="Invalid token")
    
    user.is_verified = True
    db.commit()
    db.refresh(user)
    return {"msg": "User email verified successfully"}
    