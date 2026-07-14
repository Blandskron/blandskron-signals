.PHONY: setup build up down restart logs migrate makemigrations superuser seed test test-pytest lint format shell backup restore check
setup:
	cp -n .env.example .env || true
build:
	docker compose build
up:
	docker compose up
down:
	docker compose down
restart:
	docker compose restart
logs:
	docker compose logs -f
migrate:
	docker compose run --rm backend python manage.py migrate
makemigrations:
	docker compose run --rm backend python manage.py makemigrations
superuser:
	docker compose run --rm backend python manage.py createsuperuser
seed:
	docker compose run --rm backend python manage.py seed_data
test:
	docker compose run --rm backend python manage.py test
test-pytest:
	docker compose run --rm backend pytest
check:
	python -m compileall -q apps
	git diff --check
lint:
	docker compose run --rm backend ruff check .
format:
	docker compose run --rm backend ruff format .
shell:
	docker compose run --rm backend python manage.py shell
backup:
	docker compose exec postgres pg_dump -U $${POSTGRES_USER:-blandskron} $${POSTGRES_DB:-blandskron_signals} > backup.sql
restore:
	docker compose exec -T postgres psql -U $${POSTGRES_USER:-blandskron} $${POSTGRES_DB:-blandskron_signals} < backup.sql
