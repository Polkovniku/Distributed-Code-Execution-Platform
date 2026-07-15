from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from models.user import User
from schemas.user import UserCreate, UserLogin
from core import security
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy import select

class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        
    async def get_user_by_id(self, user_id: UUID) -> User | None:
        return await self.db.get(User, user_id)
    
    async def get_user_by_email(self, email: str) -> User | None:
        return await self.db.scalar(select(User).where(User.email == email))
    
    async def create_user(self, data: UserCreate) -> User:
        data = data.model_dump()
        password = data.pop("password")
        user = User(hashed_password=security.hash_password(password), **data)
        
        try:
            self.db.add(user)
            await self.db.commit()
            await self.db.refresh(user)
            return user
        except IntegrityError:
            await self.db.rollback()
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")
        except SQLAlchemyError:
            await self.db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Invalid create user")
        
    async def log_in(self, data: UserLogin):
        user = await self.get_user_by_email(data.email)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User is not found")
        
        check_password = security.verify_password(user.hashed_password, data.password)
        if not check_password:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
        
        access_token = security.create_access_token({"sub": str(user.id)})
        refresh_token = security.create_refresh_token({"sub": str(user.id)})
        
        return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
        
    async def update_token(self, token: str):
        try:
            payload = security.decode_token(token)
        except Exception:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type")
        
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
        
        user = await self.get_user_by_id(UUID(user_id))
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User is not found")
             
        access_token = security.create_access_token({"sub": str(user.id)})
        refresh_token = security.create_refresh_token({"sub": str(user.id)})
        
        return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}