#!/usr/bin/env bash

echo "==> Updating database to latest"
alembic upgrade head

app_port="${PORT:-8000}"
echo "==> Starting gunicorn on port ${app_port}"
gunicorn app:app --bind 0.0.0.0:$app_port --workers 4 --log-file -
