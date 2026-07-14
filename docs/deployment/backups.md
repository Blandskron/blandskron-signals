# Backups y restauración

El backup de PostgreSQL debe ejecutarse con `pg_dump` y almacenarse cifrado fuera del servidor de aplicación. El Makefile incluye comandos locales `make backup` y `make restore` para el MVP.

Política mínima recomendada:

- backup diario incremental o lógico según el proveedor;
- retención de 30 días;
- copia fuera del host principal;
- prueba mensual de restauración;
- nunca guardar contraseñas en scripts ni en el repositorio.
