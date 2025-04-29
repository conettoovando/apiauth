from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from auth.jwt_handler import verify_token
import jwt

router = APIRouter(
    prefix='/auth'
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@router.get('/public_key')
async def me(token: str = Depends(oauth2_scheme)):
    try:
        user = verify_token(token)
        return {"msg": "Token válido", "user": user}
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token inválido")