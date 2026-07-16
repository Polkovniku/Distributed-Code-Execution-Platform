from fastapi import APIRouter, Depends
from service.auth import AuthService
from core.dependencies import get_current_user, get_db
from schemas.user import UserResponse, UserCreate, UserLogin, TokenResponse, RefreshTokenRequest
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from models.user import User

router = APIRouter(prefix="/auth", tags=["auth"])

def get_user_service(db: Annotated[AsyncSession, Depends(get_db)]):
    return AuthService(db)

@router.get("/me", response_model=UserResponse)
async def get_me(user: Annotated[User, Depends(get_current_user)]):
    return user

@router.post("/register", response_model=UserResponse)
async def register(data: UserCreate, service: Annotated[AuthService, Depends(get_user_service)]):
    return await service.create_user(data)

@router.post("/login", response_model=TokenResponse)
async def log_in(data: UserLogin, service: Annotated[AuthService, Depends(get_user_service)]):
    return await service.log_in(data)

@router.post("/token", response_model=TokenResponse)
async def refresh_token(token: RefreshTokenRequest, service: Annotated[AuthService, Depends(get_user_service)]):
    return await service.update_token(token.refresh_token)