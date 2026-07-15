from pwdlib import PasswordHash
from datetime import timedelta, datetime, timezone
import jwt
from core.config import settings

password_hasher = PasswordHash.recommended()

def hash_password(password):
    return password_hasher.hash(password)

def verify_password(hashed_password, password):
    return password_hasher.verify(password,  hashed_password)

def create_access_token(data: dict):
    payload = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    payload.update({"exp": expire, "type": "access"})
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    return token


def create_refresh_token(data: dict):
    payload = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=7)
    payload.update({"exp": expire, "type": "refresh"})
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    return token


def decode_token(token: str):
    return jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])