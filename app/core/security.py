"""
Утилиты для работы с JWT(JSON WEB TOKEN) и папрлями.
"""
from datetime import datetime, timezone, timedelta

import jwt
import hashlib
from app.core.config import settings
from passlib.context import CryptContext

# pwd_contex = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()
    # return pwd_contex.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return hashlib.sha256(plain_password.encode()).hexdigest() == hashed_password
    # return pwd_contex.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    exp = (datetime.now(timezone.utc) # Текущее время
           + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))  # Добавление минут жизни токена
    to_encode.update({"exp": exp, "type": "access"})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    return encoded_jwt

def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    exp = (datetime.now(timezone.utc)  # Текущее время
           + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS))  # Добавление минут жизни токена
    to_encode.update({"exp": exp, "type": "refresh"})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    return encoded_jwt

def decode_token(token: str) -> dict:
    payload = jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM]
    )
    return payload


