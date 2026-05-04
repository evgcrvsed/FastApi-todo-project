from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr = Field(..., description="Email пользователя")


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=72, description="Пароль (8–72 символа)")


class UserRead(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)   # ← обязательно!


class UserInDB(UserBase):
    id: int
    hashed_password: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)