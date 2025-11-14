from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(user_id: int, secret_key: str, algorithm: str, expire_minutes: int):
    expire = datetime.utcnow() + timedelta(minutes=expire_minutes)
    payload = {"sub": str(user_id), "exp": expire}
    return jwt.encode(payload, secret_key, algorithm=algorithm)


def decode_token(token: str, secret_key: str, algorithm: str):
    try:
        return jwt.decode(token, secret_key, algorithms=[algorithm])
    except JWTError:
        return None
