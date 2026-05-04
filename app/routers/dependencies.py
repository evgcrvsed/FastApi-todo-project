from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.security import get_current_user
from db.session import get_db
from models.user import User
from repositories.todo import TodoRepository
from repositories.user import UserRepository


def get_todo_repo(db: AsyncSession = Depends(get_db)) -> TodoRepository:
    return TodoRepository(db)


def get_user_repo(db: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(db)


CurrentUser = Depends(get_current_user)