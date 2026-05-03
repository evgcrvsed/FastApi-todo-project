from fastapi import FastAPI
from routers.todo import router as todos_router
from routers.health_check import router as health_router

from db.engine import engine
from models.base import Base

app = FastAPI(title="Simple Todo API")

app.include_router(todos_router)
app.include_router(health_router)


@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ База данных инициализирована")


@app.get("/")
async def root():
    return {"message": "Todo API работает! Перейди на /docs"}