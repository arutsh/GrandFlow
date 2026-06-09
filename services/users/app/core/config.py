import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent  # services/users/app/core

# Environment-aware env file selection
ENV = os.getenv("ENV", "development")
if ENV == "local":
    ENV_FILE = BASE_DIR.parent / ".env.users.local"
else:
    ENV_FILE = BASE_DIR.parent / ".env.users.dev"

print(f"Base dir-envfile: {BASE_DIR}, {ENV_FILE}")


class Settings(BaseSettings):
    env: str = "development"
    debug: bool = True
    users_database_url: str
    REDIS_URL: str
    model_config = SettingsConfigDict(env_file=ENV_FILE, case_sensitive=False, extra="ignore")


settings = Settings()  # type: ignore[call-arg]
print(f"Base dir: {BASE_DIR}")
print(f"settings.users_database_url: {settings.users_database_url}")
print(f"settings.debug: {settings.debug}")
