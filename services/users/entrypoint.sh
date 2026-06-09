#!/bin/bash
set -e

# Debug: Print all environment variables related to database
echo "=== DEBUG: Environment Variables ==="
echo "POSTGRES_HOST: $POSTGRES_HOST"
echo "POSTGRES_PORT: $POSTGRES_PORT"
echo "POSTGRES_USER: $POSTGRES_USER"
echo "POSTGRES_PASSWORD: $POSTGRES_PASSWORD"
echo "POSTGRES_DB: $POSTGRES_DB"
echo "===================================="

DB_HOST="${POSTGRES_HOST}"
DB_PORT="${POSTGRES_PORT}"
DB_USER="${POSTGRES_USER}"
DB_PASS="${POSTGRES_PASSWORD}"
DB_NAME="grandflow_users"

echo "Waiting for database at $DB_HOST:$DB_PORT..."
echo "Using credentials - User: $DB_USER, Database: $DB_NAME"

# Wait for the database to be ready
/app/shared/healthcheck.sh  "$DB_HOST" "$DB_PORT" "$DB_USER" "$DB_PASS" "$DB_NAME"

echo "Database is ready. Running migrations..."

# Run migrations
alembic upgrade head

echo "Migrations complete. Starting FastAPI application..."

# Start the FastAPI application
exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload