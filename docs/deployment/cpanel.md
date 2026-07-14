# Despliegue en cPanel

El objetivo de producción es ejecutar Django como aplicación Python de cPanel/Passenger, usar MySQL del mismo hosting y enviar correo por SMTP. PostgreSQL y Docker quedan para desarrollo local.

## Preparación en cPanel

1. Crear una base MySQL y un usuario desde cPanel.
2. Asignar el usuario a la base con todos los permisos necesarios.
3. Crear una aplicación Python con Python 3.12 o la versión compatible disponible.
4. Configurar el directorio de aplicación apuntando al contenido de `apps/backend`.
5. Instalar `apps/backend/requirements.txt` desde el entorno virtual de cPanel.
6. Copiar `.env.cpanel.example` como variables de entorno de la aplicación y reemplazar todos los valores de ejemplo.
7. Configurar `passenger_wsgi.py` como archivo de inicio.
8. Ejecutar migraciones y seed desde el terminal de cPanel:

```bash
python manage.py migrate --settings=config.settings.production
python manage.py seed_data --settings=config.settings.production
python manage.py collectstatic --noinput --settings=config.settings.production
```

## Base de datos

No se deben copiar credenciales desde phpMyAdmin al repositorio. El nombre real de la base y del usuario se obtienen desde cPanel y se configuran únicamente como `DB_NAME`, `DB_USER` y `DB_PASSWORD`.

La configuración usa `DB_HOST=localhost` y `DB_PORT=3306` por defecto, pero ambos valores pueden ajustarse si el proveedor entrega un host distinto.

## SMTP

Configurar `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_USE_TLS`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD` y `DEFAULT_FROM_EMAIL` con el proveedor de correo del hosting. Mailpit solo se usa en local.

## MCP

El MCP puede ejecutarse como una segunda aplicación Python de cPanel, con su propio entorno y `MCP_INTERNAL_API_TOKEN`, o mantenerse en un servicio separado. Debe consumir la API Django por HTTPS y nunca acceder a MySQL directamente.

## Estáticos y seguridad

Configurar el document root para servir `staticfiles/` y `media/` según las opciones de cPanel. Activar HTTPS antes de dejar `DJANGO_SECURE_SSL_REDIRECT=true`. No exponer el archivo `.env`, el entorno virtual ni backups desde el document root.
