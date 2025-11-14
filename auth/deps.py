from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pony.orm import db_session
from .models import User
from .security import decode_token
from app.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@db_session
def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token, settings.SECRET_KEY, settings.ALGORITHM)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user = User.get(id=int(payload["sub"]))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user
