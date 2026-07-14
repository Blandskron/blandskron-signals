#!/usr/bin/env bash
set -euo pipefail
[[ -f .env ]] || cp .env.example .env
docker compose build
docker compose run --rm backend python manage.py migrate
