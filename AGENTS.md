# Instrucciones para agentes

Este es un monorepo. `apps/backend` es la fuente de verdad del negocio y PostgreSQL es la base de datos. `apps/mcp-server` expone herramientas MCP y se comunica con Django por HTTP. No se permite acceso directo del MCP a PostgreSQL.

Antes de editar: leer `README.md`, este archivo y la documentación relevante; inspeccionar cambios existentes; mantener el alcance de la fase; añadir pruebas; y documentar decisiones.

No integrar la API de OpenAI, no publicar ni desplegar sin autorización, no registrar usuarios MCP públicamente y no introducir servicios innecesarios. Las variables sensibles solo viven en `.env`.

Una tarea se cierra cuando funciona localmente, tiene pruebas o justificación clara, está documentada y no rompe componentes existentes.
