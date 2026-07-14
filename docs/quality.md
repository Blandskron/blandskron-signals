# Calidad y validación

Checks locales:

- `scripts/check-project.ps1` o `scripts/check-project.sh`: compilación Python y whitespace de Git.
- `make test`: suite Django.
- `make test-pytest`: suite pytest cuando se instalan `requirements-dev.txt`.
- `make lint`: Ruff dentro del contenedor.
- `make seed`: datos iniciales idempotentes para desarrollo local.

El workflow `.github/workflows/quality.yml` ejecuta `django check`, migraciones implícitas de la suite Django, pruebas y Ruff contra PostgreSQL 16, además del smoke test del servidor MCP.

No se consideran suficientes los checks estáticos para cerrar una funcionalidad de alto riesgo: publicación, newsletter, autenticación y migraciones deben validarse también dentro del stack local.
