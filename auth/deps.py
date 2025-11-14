from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pony.orm import db_session

from app.config import settings
from db.models import User
from auth.security import decode_token

bearer_scheme = HTTPBearer()


@db_session
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = credentials.credentials

    # Декодируем и проверяем токен
    payload = decode_token(token, settings.SECRET_KEY, settings.ALGORITHM)
    if not payload or "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = User.get(id=int(payload["sub"]))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
