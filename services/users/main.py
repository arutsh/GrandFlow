import debugpy
from fastapi import FastAPI
from app.api import user_routes, customer_routes, auth_routes
from fastapi.middleware.cors import CORSMiddleware
from app.db.init_db import init_db

debugpy.listen(("0.0.0.0", 5678))
print("✅ VS Code debugger is listening on port 5678")


init_db()

app = FastAPI()

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
