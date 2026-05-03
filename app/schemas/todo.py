from pydantic import BaseModel, Field
from datetime import datetime

class TodoBase(BaseModel):
    title: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Заголовок задачи, минимум 3 символа"
    )
    description: str | None = Field(None, max_length=500)
    completed: bool = False

class TodoCreate(TodoBase):
    pass

class TodoUpdate(BaseModel):
    title: str | None = Field(None, min_length=3, max_length=100)
    description: str | None = Field(None, max_length=500)
    completed: bool | None = None

class Todo(TodoBase):
    id: int
    created_at: datetime

class TodoRead(TodoBase):
    id: int
