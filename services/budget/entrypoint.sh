#!/bin/bash
set -e

# Extract hostname and port from DATABASE_URL
# Expected format: postgresql://user:pass@host:port/dbname
DB_URL="${BUDGET_DATABASE_URL}"
echo "DB_URL url is  $DB_URL... : "

# Remove the protocol (postgresql://)
DB_URL_NO_PROTO="${DB_URL#postgresql://}"

# Extract user:pass@host:port/dbname part
DB_URL_NO_PROTO="${DB_URL_NO_PROTO#*@}"  # Remove user:pass@

# Now we have host:port/dbname
# Extract host
DB_HOST="${DB_URL_NO_PROTO%%:*}"

# Extract port
DB_PORT="${DB_URL_NO_PROTO#*:}"
DB_PORT="${DB_PORT%%/*}"

DB_USER="postgres"
DB_PASS="postgres"
DB_NAME="grandflow_budget"

echo "Waiting for database at $DB_HOST:$DB_PORT..."

# Wait for the database to be ready
/app/shared/healthcheck.sh  "$DB_HOST" "$DB_PORT" "$DB_USER" "$DB_PASS" "$DB_NAME"

echo "Database is ready. Running migrations..."

# Run migrations
alembic upgrade head

echo "Migrations complete. Starting FastAPI application..."

# Start the FastAPI application
exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload
