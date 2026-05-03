from sqlalchemy import String, Boolean, Text
from .base import Base
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

class Todo(Base):
    __tablename__ = "todos"

    title: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
