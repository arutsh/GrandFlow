import debugpy

debugpy.listen(("0.0.0.0", 5678))
print("✅ VS Code debugger is listening on port 5678")

from fastapi import FastAPI
from app.api import user_routes, customer_routes

from app.db.init_db import init_db


init_db()

app = FastAPI()
app.include_router(user_routes.router)
app.include_router(customer_routes.router)
