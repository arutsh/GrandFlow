from contextlib import asynccontextmanager
from fastapi.security import OAuth2PasswordBearer
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from pydantic_settings import BaseSettings
from services.users_client import (
    init_urls as init_users_url,
    close_urls as close_users_url,
)

from fastapi.middleware.cors import CORSMiddleware
from api.user_router import router as user_router

import debugpy


# --- Debugging support (VS Code Remote Debugger) ---
debugpy.listen(("0.0.0.0", 5682))
print("✅ VS Code debugger is listening on port 5682")


# --- Settings ---
class Settings(BaseSettings):
    USERS_SERVICE_URL: str = ""
    BUDGETS_SERVICE_URL: str = ""
    REDIS_URL: str | None = None

    class Config:
        env_file = ".env.gateway.dev"


settings = Settings()


# --- Lifespan context manager (replaces deprecated @on_event) ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup

    await init_users_url(settings.model_dump())

    print("✅ Gateway initialized external service URLs")

    yield  # Application runs here

    # Shutdown

    await close_users_url()

    print("🛑 Gateway connections closed")


# --- FastAPI app instance ---
app = FastAPI(title="GrandFlow API Gateway", lifespan=lifespan)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

allowed_origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:3001",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Routes ---


app.include_router(user_router, prefix="/api")


# --- Custom OpenAPI schema with Bearer auth ---
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="GrandFlow API Gateway",
        version="1.0.0",
        description="Gateway that aggregates users & budgets data.",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
    }

    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
