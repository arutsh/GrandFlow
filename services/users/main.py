import debugpy
from fastapi import FastAPI
from app.api import user_routes, customer_routes, auth_routes
from fastapi.middleware.cors import CORSMiddleware
from app.db.init_db import init_db
from fastapi.openapi.utils import get_openapi

debugpy.listen(("0.0.0.0", 5678))
print("✅ VS Code debugger is listening on port 5678")


init_db()

app = FastAPI()

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
app.include_router(user_routes.router, prefix="/api")
app.include_router(customer_routes.router, prefix="/api")
app.include_router(auth_routes.router, prefix="/api")


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="user Service API",
        version="1.0.0",
        description="API for managing users",
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
