#!/usr/bin/env bash

alembic upgrade head
gunicorn app:app --bind 0.0.0.0:${POST:-8000} --workers 4 --log-file -
