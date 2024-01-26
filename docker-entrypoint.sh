#!/bin/bash

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

# Start server
echo "Starting server"
uvicorn core.asgi:application --host 0.0.0.0 --port 8000 --workers 4