#!/usr/bin/env bash

alembic upgrade head
gunicorn app:app --bind 0.0.0.0 --workers 4 --log-file -
