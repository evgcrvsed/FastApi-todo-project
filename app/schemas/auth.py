from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)

class UserCreate(User):
    pass

class UserLogin(User):
    pass

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
