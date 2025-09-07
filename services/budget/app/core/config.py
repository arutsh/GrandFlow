from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent  # services/budget/app/core
ENV_FILE = BASE_DIR.parent / ".env.budget.dev"
print(f"Base dir-envfile: {BASE_DIR}, {ENV_FILE}")


class Settings(BaseSettings):
    env: str = "development"
    debug: bool = True

    # Service URLs
    customer_service_url: str

    # Databases
    budget_database_url: str

    model_config = SettingsConfigDict(env_file=ENV_FILE, case_sensitive=False, extra="ignore")


settings = Settings()  # type: ignore[call-arg]
print(f"Base dir: {BASE_DIR}")
print(f"settings.debug: {settings.debug}")
print(f"settings.budget_database_url: {settings.budget_database_url}")
print(f"settings.customer_service_url: {settings.customer_service_url}")
