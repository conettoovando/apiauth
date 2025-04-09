# auth/jwt_handler.py
import jwt
from cryptography.hazmat.primitives import serialization
from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()

PRIVATE_KEY_PATH = Path(os.getenv("PRIVATE_KEY_PATH"))
PUBLIC_KEY_PATH = Path(os.getenv("PUBLIC_KEY_PATH"))

def load_private_key():
    with open(PRIVATE_KEY_PATH, 'r') as file:
        return serialization.load_ssh_private_key(file.read().encode(), password=b'')

def load_public_key():
    with open(PUBLIC_KEY_PATH, 'r') as file:
        return serialization.load_ssh_public_key(file.read().encode())

def create_access_token(data: dict):
    key = load_private_key()
    return jwt.encode(data, key=key, algorithm='RS256')

def verify_token(token: str):
    key = load_public_key()
    return jwt.decode(token, key=key, algorithms=['RS256'])
