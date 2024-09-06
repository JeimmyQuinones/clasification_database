#! /usr/bin/env bash


python /app/api/backend_pre_start.py

# Run migrations
alembic upgrade head

fastapi run api/main.py --proxy-headers --port 8000