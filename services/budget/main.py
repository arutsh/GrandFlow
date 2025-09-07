# /services/budget/app/main.py
from fastapi import FastAPI
from app.api import budget_routes, budget_line_routes
from app.models.budget import Base
from app.db.session import engine

from fastapi.openapi.utils import get_openapi
import debugpy

debugpy.listen(("0.0.0.0", 5680))
print("✅ VS Code debugger is listening on port 5680")

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(budget_routes.router, prefix="/api")
app.include_router(budget_line_routes.router, prefix="/api")


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
