import os
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from app.api import parse_routes
from app.core.config import settings
from app.core.logging import setup_logging, get_logger

setup_logging(settings.LOG_LEVEL)
logger = get_logger(__name__)

if os.getenv("VSCODE_DEBUGGER") == "1":
    try:
        import debugpy

        debugpy.listen(("0.0.0.0", 5682))
        print("✅ VS Code debugger is listening on port 5682")
    except Exception:
        pass


app = FastAPI(title="AI Service")

app.include_router(parse_routes.router, prefix="/api/v1")


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="AI Service API",
        version="1.0.0",
        description="AI-powered budget parsing service",
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


app.openapi = custom_openapi  # type: ignore
