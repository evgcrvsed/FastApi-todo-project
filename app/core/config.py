from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///./todo.db"

    SECRET_KEY: str = "SIGMASIGMABOY" # потом вынести в .env
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15  # короткий
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7  # длинный

    PROJECT_NAME: str = "FastAPI Template"
    DEBUG: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore"
    )

settings = Settings()
