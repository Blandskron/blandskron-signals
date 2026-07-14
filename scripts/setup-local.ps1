if (-not (Test-Path .env)) { Copy-Item .env.example .env }
docker compose build
docker compose run --rm backend python manage.py migrate
