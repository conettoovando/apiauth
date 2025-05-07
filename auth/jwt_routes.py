from fastapi import APIRouter, HTTPException
from fastapi.security import OAuth2PasswordBearer
from auth.jwt_handler import get_public_key
import jwt

router = APIRouter(
    prefix='/auth'
)

@router.get('/public-key')
async def get_public_keys():
    try:
        response = get_public_key()
        return response
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token inválido")