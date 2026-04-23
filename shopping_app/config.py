from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    openai_api_key: str | None = None

    shopping_db_path: str = str(Path("shopping_app") / "shopping.db")
    email_to: str = "vino.lalith@gmail.com"
    email_from: str | None = None
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 465
    smtp_username: str | None = None
    smtp_app_password: str | None = None

    shipping_zip: str = "78229"
    allowed_platforms: list[str] = Field(default_factory=lambda: ["amazon", "walmart", "costco", "target"])
    recommender_model: str = "gpt-4o-mini"
    embedding_model: str = "text-embedding-3-small"
    max_recommendations: int = 1
    max_candidates_per_platform: int = 8
    history_purge_days: int = 60


settings = Settings()


def get_settings() -> Settings:
    return settings
