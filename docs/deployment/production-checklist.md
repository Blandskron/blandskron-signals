# Checklist de despliegue manual

## Antes del despliegue

- [ ] Crear `.env.production` fuera del repositorio.
- [ ] Generar un `DJANGO_SECRET_KEY` nuevo y aleatorio.
- [ ] Configurar `DJANGO_ALLOWED_HOSTS` y `DJANGO_CSRF_TRUSTED_ORIGINS`.
- [ ] Configurar credenciales PostgreSQL y SMTP.
- [ ] Configurar `MCP_INTERNAL_API_TOKEN` fuera de logs y control de versiones.
- [ ] Confirmar DNS para `blandskron.cl`, `api.blandskron.cl` y `mcp.blandskron.cl`.
- [ ] Revisar migraciones pendientes.
- [ ] Probar backup y restauración.

## Secuencia

1. Construir la imagen de backend con `Dockerfile.production`.
2. Ejecutar `python manage.py migrate`.
3. Ejecutar `python manage.py collectstatic --noinput`.
4. Levantar Gunicorn detrás de Nginx.
5. Emitir y configurar certificados HTTPS.
6. Crear o verificar el superusuario autorizado para la API/MCP.
7. Verificar `/health/`, `/api/` y `/mcp`.
8. Revisar logs y ejecutar una prueba de borrador.

## Después

- [ ] Confirmar headers de seguridad y redirección HTTPS.
- [ ] Confirmar que el Admin no está expuesto sin protección adicional.
- [ ] Confirmar entregas SMTP y double opt-in.
- [ ] Programar backups y revisión de restauración.
- [ ] No activar publicación automática.

Esta checklist prepara el despliegue, pero no lo ejecuta.
