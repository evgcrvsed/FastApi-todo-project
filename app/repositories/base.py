from typing import TypeVar, Generic, Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.sql import Select

T = TypeVar("T")

class BaseRepository(Generic[T]):
    def __init__(self, session: AsyncSession, model: Type[T]):
        self.session = session
        self.model = model

    async def add(self, obj: T) -> T:
        self.session.add(obj)
        await self.session.flush()
        return obj

    async def get_by_id(self, id_: int) -> T | None:
        return await self.session.get(self.model, id_)

    async def get_all(self) -> list[T]:
        result = await self.session.execute(select(self.model))
        return list(result.scalars().all())

    async def delete(self, obj: T) -> None:
        await self.session.delete(obj)