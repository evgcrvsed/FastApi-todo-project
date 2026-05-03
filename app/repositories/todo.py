from .base import BaseRepository
from models.todo import Todo
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

class TodoRepository(BaseRepository[Todo]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Todo)

    async def get_by_completed(self, completed: bool | None = None):
        stmt = select(Todo)
        if completed is not None:
            stmt = stmt.where(Todo.completed == completed)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())