from contextlib import asynccontextmanager
from fastapi import FastAPI

from db.engine import engine
from models.base import Base
from routers.todo import router as todos_router
from routers.health_check import router as health_router
from routers.auth import router as auth_router

from core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ База данных инициализирована")

    yield

    await engine.dispose()
    print("✅ База данных отключена")


app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan
)

app.include_router(todos_router)
app.include_router(health_router)
app.include_router(auth_router)


@app.get("/", description='И что ты ожидал тут увидеть?', tags=['index'])
async def root():
    return {"message": "Todo API работает! Перейди на /docs"}