from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    create_refresh_token,
)
from repositories.user_repository import UserRepository
from schemas.auth import UserCreate, UserLogin


class AuthService:
    def __init__(self, session: AsyncSession):   # ← session
        self.repo = UserRepository(session)

    async def register(self, user_in: UserCreate):
        if await self.repo.get_by_email(user_in.email):
            raise HTTPException(status_code=400, detail="Email already registered")

        hashed_password = get_password_hash(user_in.password)
        user = await self.repo.create(user_in.email, hashed_password)
        return user

    async def login(self, credentials: UserLogin):
        user = await self.repo.get_by_email(credentials.email)
        if not user or not verify_password(credentials.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token = create_access_token(user.email)
        refresh_token = create_refresh_token(user.email)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }