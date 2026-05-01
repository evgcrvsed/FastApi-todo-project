from fastapi import FastAPI
from routers.todo import router as todos_router
from routers.health_check import router as health_router

app = FastAPI(title="Simple Todo API")

app.include_router(todos_router)
app.include_router(health_router)

@app.get("/")
async def root():
    return {"message": "Todo API работает! Перейди на /docs"}
