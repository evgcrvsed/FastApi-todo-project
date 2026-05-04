from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr = Field(..., description="Email пользователя")

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="Пароль (минимум 8 символов)")

class UserRead(UserBase):
    id: int
    is_active: bool
    created_at: datetime

class UserInDB(UserBase):
    id: int
    hashed_password: str
    is_active: bool