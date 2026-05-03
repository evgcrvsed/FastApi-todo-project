from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_db
from repositories.todo import TodoRepository

def get_todo_repo(db: AsyncSession = Depends(get_db)) -> TodoRepository:
    return TodoRepository(db)
