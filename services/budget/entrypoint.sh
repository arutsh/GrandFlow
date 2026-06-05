#!/bin/bash
set -e

# Wait for the database to be ready
/app/shared/healthcheck.sh grandflow-db 5432 postgres postgres grandflow_budget

# Run migrations
alembic upgrade head

# Start the FastAPI application
exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload
