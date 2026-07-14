# Herramientas MCP

El servidor MCP se ejecuta en `http://localhost:8100/mcp` con transporte Streamable HTTP sin estado. Cada conexión requiere autenticación, el `Host` debe pertenecer a `MCP_ALLOWED_HOSTS` y, cuando se envía, el encabezado `Origin` debe pertenecer a `MCP_ALLOWED_ORIGINS`. Expone herramientas que llaman exclusivamente a la API interna de Django.

Autenticación entre servicios:

```text
Authorization: Bearer ${MCP_INTERNAL_API_TOKEN}
```

Herramientas iniciales:

- `get_site_configuration`: configuración y guía editorial.
- `get_content_requirements`: campos y estados válidos.
- `list_recent_articles`: contexto editorial reciente.
- `search_articles`: búsqueda de artículos.
- `get_article`: detalle y fuentes.
- `list_trends`: radar de tendencias.
- `get_trend`: detalle de una tendencia.
- `list_categories`: categorías disponibles.
- `list_tags`: etiquetas existentes.
- `list_recent_sources`: fuentes recientes.
- `get_newsletter_schedule`: ediciones y estados de newsletter.
- `create_source`: registrar una fuente.
- `create_article_draft`: crear un borrador validado por Django.
- `update_article`: actualizar campos editoriales.
- `mark_article_for_review`: enviar un borrador a revisión.
- `update_editorial_task`: actualizar o cerrar una tarea editorial.

El servidor no importa modelos Django, no abre conexiones PostgreSQL y no publica automáticamente. La API Django vuelve a validar autenticación, permisos, fuentes y requisitos editoriales.
