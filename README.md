# Blandskron Signals

Plataforma editorial tecnológica de Blandskron, operada por agentes mediante un servidor MCP. El MVP mantiene a Django como fuente de verdad y usa Django Templates para el sitio público.

## Requisitos

- Docker Desktop con Docker Compose
- Git
- PowerShell 7 (Windows) o Bash (Linux/macOS)

## Inicio local

```bash
cp .env.example .env
docker compose up --build
```

Servicios locales: sitio/API Django en `http://localhost:8000`, MCP en `http://localhost:8100/health`, Mailpit en `http://localhost:8025` y PostgreSQL en `localhost:5432`. Para cPanel consulta [docs/deployment/cpanel.md](docs/deployment/cpanel.md).

En Windows: `Copy-Item .env.example .env` y `./scripts/start-local.ps1`.

El contenedor local aplica migraciones y datos iniciales automáticamente al iniciar.

## Comandos

`make setup`, `make up`, `make migrate`, `make seed`, `make test` y `make down`.

Los equivalentes PowerShell están en `scripts/`.

Consulta [docs/architecture/overview.md](docs/architecture/overview.md) para la arquitectura. Las Fases 0 a 8 del plan maestro ya tienen su base implementada; la ejecución integral queda pendiente de iniciar Docker Desktop.

## Principios

- No se integra la API de OpenAI en este repositorio.
- Django concentra la lógica de negocio y el acceso a PostgreSQL.
- El MCP solo consume la API interna de Django.
- Toda publicación debe estar autorizada y auditada.
