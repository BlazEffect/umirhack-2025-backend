from fastapi import APIRouter, HTTPException, Depends
from pony.orm import db_session, commit

from app.config import settings
from auth.schemas import UserPublic, UserCreate, Token
from auth.security import hash_password, verify_password, create_access_token
from db.models import User
from auth.deps import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserPublic)
@db_session
def register_user(data: UserCreate):
    if User.get(email=data.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        email=data.email,
        password_hash=hash_password(data.password)
    )

    return user


@router.post("/login", response_model=Token)
@db_session
def login_user(data: UserCreate):
    user = User.get(email=data.email)
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    token = create_access_token(
        user.id,
        settings.SECRET_KEY,
        settings.ALGORITHM,
        settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=UserPublic)
def get_me(current_user=Depends(get_current_user)):
    return current_user
