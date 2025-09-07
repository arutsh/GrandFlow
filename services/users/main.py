import debugpy
from fastapi import FastAPI
from app.api import user_routes, customer_routes, auth_routes

from app.db.init_db import init_db

debugpy.listen(("0.0.0.0", 5678))
print("✅ VS Code debugger is listening on port 5678")


init_db()

app = FastAPI()
app.include_router(user_routes.router, prefix="/api")
app.include_router(customer_routes.router, prefix="/api")
app.include_router(auth_routes.router, prefix="/api")
