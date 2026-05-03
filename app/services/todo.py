from sqlalchemy.ext.asyncio import AsyncSession
from repositories.todo import TodoRepository
from schemas.todo import TodoCreate, TodoRead
from models.todo import Todo

class TodoService:
    def __init__(self, session: AsyncSession):
        self.repo = TodoRepository(session)

    async def create(self, data: TodoCreate) -> TodoRead:
        todo = Todo(**data.model_dump())
        await self.repo.add(todo)
        return TodoRead.model_validate(todo)

    async def get_all(self, completed: bool | None = None) -> list[TodoRead]:
        todos = await self.repo.get_by_completed(completed)
        return [TodoRead.model_validate(t) for t in todos]
    