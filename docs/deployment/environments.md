# Entornos oficiales

## Local

Usa Docker Compose, PostgreSQL y Mailpit:

```bash
Copy-Item .env.local.example .env
docker compose up --build
```

El contenedor aplica automáticamente migraciones y `seed_data`. La configuración local se carga desde `config.settings.local` y utiliza `POSTGRES_*`.

## cPanel

Usa Passenger, MySQL del hosting y SMTP real:

```bash
python manage.py migrate --settings=config.settings.production
python manage.py seed_data --settings=config.settings.production
python manage.py collectstatic --noinput --settings=config.settings.production
```

La configuración cPanel se carga desde `config.settings.production` y utiliza `DB_*`. No requiere Docker, PostgreSQL ni Mailpit.

Ambos entornos comparten modelos, migraciones, API, MCP y lógica editorial; solo cambia la infraestructura mediante variables de entorno.
