from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.schemas.user import UserCreate, TokenPair
from app.services.auth import register_user, authenticate_user, issue_tokens, refresh_access_token
from app.db.session import get_db

router = APIRouter(prefix="/auth", tags=["auth"])

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/register", response_model=dict)
def register(data: UserCreate, db: Session = Depends(get_db)):
    try:
        user = register_user(db, data)
        return {"message": "User registered", "user_id": user.id}
    
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@router.post("/login", response_model=TokenPair)
def login(request: Request, payload: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, payload.email, payload.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    client_ip = request.client.host if request.client is not None else None
    user_agent = request.headers.get("User-Agent", "")
    if not client_ip or not user_agent:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Client IP not found")

    return issue_tokens(user, db, client_ip=client_ip, user_agent=user_agent)

class RefreshRequest(BaseModel):
    refresh_token: str

@router.post("/refresh", response_model=dict)
def refresh(data: RefreshRequest, db: Session = Depends(get_db)):
    try:
        new_access = refresh_access_token(refresh_token=data.refresh_token, db=db)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    return {"access_token": new_access, "token_type": "bearer"}