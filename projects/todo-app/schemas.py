from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class TodoBase(BaseModel):
    title: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Заголовок задачи, минимум 3 символа"
    )
    description: Optional[str] = Field(None, max_length=500)
    completed: bool = False

class TodoCreate(TodoBase):
    pass

# Новая модель специально для PATCH
class TodoUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    completed: Optional[bool] = None

class Todo(TodoBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True