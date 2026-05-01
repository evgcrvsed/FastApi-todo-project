from datetime import datetime
from fastapi import APIRouter

router = APIRouter(tags=["health"])

@router.get("/health", tags=["health"])
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        # можно добавить проверки:
        # "database": "connected" / "error",
        # "redis": "ok",
        # "disk_space": "12.5GB free"
    }