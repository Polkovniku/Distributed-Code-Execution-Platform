from datetime import datetime
from pydantic import BaseModel, Field, EmailStr, ConfigDict
from uuid import UUID

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    username: str
    email: EmailStr
    created_at: datetime

class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=72)

class UserCreate(UserLogin):
    username: str = Field(min_length=2, max_length=150)
    
class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    type_token: str = "bearer"
    
class RefreshTokenRequest(BaseModel):
    refresh_token: str