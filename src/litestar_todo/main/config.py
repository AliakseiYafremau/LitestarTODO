from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings for the application."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    DB_URL: str = "sqlite+aiosqlite:///test.sqlite"
    JWT_SECRET_KEY: str = "your_jwt_secret_key"
    JWT_ALGORITHM: str = "HS256"

settings = Settings()