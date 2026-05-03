from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from .engine import engine
from typing import AsyncGenerator
from fastapi import Depends

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
    autoflush=False,
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Зависимость для FastAPI"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()