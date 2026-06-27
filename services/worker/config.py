import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

# Required env vars:
#   RABBITMQ_URL  — amqp://user:pass@host:5672//
#   REDIS_URL     — redis://host:6379/0
#   AI_DATABASE_URL — postgresql://user:pass@host:5432/grandflow_ai

BASE_DIR = Path(__file__).resolve().parent
env_mode = os.getenv("ENV", "development")
if env_mode == "local":
    ENV_FILE = BASE_DIR / ".env.worker.local"
elif env_mode == "production":
    ENV_FILE = BASE_DIR / ".env.worker.prod"
elif env_mode == "test":
    ENV_FILE = BASE_DIR / ".env.worker.test"
else:
    ENV_FILE = BASE_DIR / ".env.worker.dev"


class Settings(BaseSettings):
    env: str = "development"
    RABBITMQ_URL: str = "amqp://guest:guest@localhost:5672//"
    REDIS_URL: str = "redis://localhost:6379/0"
    AI_DATABASE_URL: str

    model_config = SettingsConfigDict(env_file=ENV_FILE, case_sensitive=False, extra="ignore")


settings = Settings()  # type: ignore[call-arg]
