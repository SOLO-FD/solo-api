#!/bin/sh
set -e

# Wait a few second for setup database
sleep 5

# Run Alembic migrations
echo "Running Alembic migrations..."
alembic -c alembic.ini upgrade head

# Start the FastAPI app
echo "Starting FastAPI app..."
exec uvicorn api.main:app --host 0.0.0.0 --port 8088