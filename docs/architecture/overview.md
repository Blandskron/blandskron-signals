# Arquitectura

```text
Agente / ChatGPT Work
        ↓ MCP
FastAPI MCP (8100)
        ↓ HTTP interno
Django (8000)
        ↓ ORM
PostgreSQL
```

Durante el MVP Django es la única fuente de verdad de negocio. El servidor MCP no conoce credenciales de PostgreSQL ni escribe en la base de datos. Mailpit simula SMTP en desarrollo local.

La estructura de aplicaciones Django está reservada en `apps/backend/` para permitir que cada fase agregue un dominio sin duplicar lógica. El frontend público se servirá inicialmente desde Django Templates.
