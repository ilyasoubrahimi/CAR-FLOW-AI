from datetime import datetime, timedelta
from typing import Any, Union, Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(subject: Union[str, int], expires_delta: Optional[timedelta] = None) -> str:
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> Optional[dict]:
    try:
        decode = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return decode if decode.get("exp") else None
    except JWTError:
        return None
