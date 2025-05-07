# auth/jwt_handler.py
import jwt
from cryptography.hazmat.primitives import serialization
from dotenv import load_dotenv
import os
from pathlib import Path
from datetime import datetime, timedelta, timezone
from fastapi.exceptions import HTTPException
from fastapi.responses import Response

load_dotenv()

PRIVATE_KEY_PATH = Path(os.getenv("PRIVATE_KEY_PATH"))
PUBLIC_KEY_PATH = Path(os.getenv("PUBLIC_KEY_PATH"))

def load_private_key():
    with open(PRIVATE_KEY_PATH, 'r') as file:
        return serialization.load_ssh_private_key(file.read().encode(), password=b'')

def load_public_key():
    with open(PUBLIC_KEY_PATH, 'r') as file:
        return serialization.load_ssh_public_key(file.read().encode())

def create_access_token(data: dict, expires_delta: timedelta):
    key = load_private_key()

    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, key=key, algorithm='RS256')
    return encoded_jwt

def verify_token(token: str):
    try:
        key = load_public_key()
        token = jwt.decode(token, key=key, algorithms=['RS256'], options={"verify_exp": True})
        print(token)
        return token
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token invalido")
    
def get_public_key():
    with open(PUBLIC_KEY_PATH, "r") as file:
        public_key = file.read()
    return Response(content=public_key, media_type="text/plain")

def get_payload(refresh_token: str) -> dict:
    key = load_public_key()
    
    payload = jwt.decode(jwt=refresh_token, key=key, algorithms=['RS256'])

    return payload