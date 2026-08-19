import os
from typing import Optional
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Конфигурация приложения"""
    
    # App
    app_name: str = "Media Monitoring Kherson"
    app_version: str = "0.1.0"
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Database
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql://user:password@postgres:5432/media_monitoring"
    )
    
    # Redis
    redis_url: str = os.getenv("REDIS_URL", "redis://redis:6379/0")
    
    # API
    api_v1_prefix: str = "/api/v1"
    api_title: str = "Media Monitoring Kherson API"
    
    # Parsers
    parse_interval_minutes: int = 60  # Интервал парсинга в минутах
    max_articles_per_source: int = 100
    article_retention_days: int = 90  # Хранить статьи 90 дней
    
    # NLP
    nlp_confidence_threshold: float = 0.5
    use_natasha: bool = True
    
    # Telegram (опционально)
    telegram_api_id: Optional[str] = os.getenv("TELEGRAM_API_ID")
    telegram_api_hash: Optional[str] = os.getenv("TELEGRAM_API_HASH")
    telegram_phone: Optional[str] = os.getenv("TELEGRAM_PHONE")
    
    # CORS
    allowed_origins: list = ["http://localhost:3000", "http://localhost:8000"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings():
    return Settings()
