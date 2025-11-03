# /services/budget/app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api import budget_routes, budget_line_routes, mapping_routes
from app.models.budget import Base
from app.db.session import engine
from fastapi.openapi.utils import get_openapi
import debugpy
from fastapi.middleware.cors import CORSMiddleware
from app.core.exceptions import DomainError, PermissionDenied
from app.core.error_handlers import domain_error_handler
from app.services.user_client import (
    init_urls as user_client_init_urls,
    close_urls as close_user_client_urls,
)

debugpy.listen(("0.0.0.0", 5680))
print("✅ VS Code debugger is listening on port 5680")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await user_client_init_urls()
    # await init_users_url(settings.model_dump())
    # await init_budget_lines_url(settings.model_dump())
    print("✅ Gateway initialized external service URLs")

    yield  # Application runs here

    # Shutdown
    await close_user_client_urls()
    # await close_users_url()
    # await close_budget_lines_url()
    print("🛑 Gateway connections closed")


Base.metadata.create_all(bind=engine)
app = FastAPI(title="Budget Service", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(budget_routes.router, prefix="/api/v1")
app.include_router(budget_routes.private_router, prefix="/api/private/v1")
app.include_router(budget_line_routes.router, prefix="/api/v1")
app.include_router(mapping_routes.router, prefix="/api/v1")

# Register global exception handler
app.add_exception_handler(DomainError, domain_error_handler)
app.add_exception_handler(PermissionDenied, domain_error_handler)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Budget Service API",
        version="1.0.0",
        description="API for managing budgets and budget lines",
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
