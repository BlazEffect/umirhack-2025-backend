from fastapi import APIRouter, HTTPException, Depends
from pony.orm import db_session, commit
from .models import User
from .schemas import UserCreate, UserPublic, Token
from .security import hash_password, verify_password, create_access_token
from .deps import get_current_user
from app.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserPublic)
@db_session
def register_user(data: UserCreate):
    if User.get(email=data.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(email=data.email, username=data.username, hashed_password=hash_password(data.password))
    commit()
    return user

@router.post("/login", response_model=Token)
@db_session
def login_user(data: UserCreate):
    user = User.get(email=data.email)
    if not user or not verify_password(data.password, user.hashed_password):
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
