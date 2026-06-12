#!/bin/bash
set -e

PG_HOST=$1
PG_PORT=$2
PG_USER=$3
PG_PASS=$4
PG_DB=$5

until psql "host=$PG_HOST port=$PG_PORT user=$PG_USER password=$PG_PASS dbname=$PG_DB" -c "SELECT 1"; do
  >&2 echo "Postgres is unavailable - sleeping (shared)"
  sleep 1

done
>&2 echo "Postgres is up - executing command"
