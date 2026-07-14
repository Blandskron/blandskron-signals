# API interna

La API vive en `/api/` y solo acepta el encabezado:

```text
Authorization: Bearer <MCP_INTERNAL_API_TOKEN>
```

El token se compara en memoria con la variable de entorno y se asocia al primer superusuario activo. No se devuelve el token en respuestas ni logs.

Endpoints principales:

- `GET/POST /api/articles/`
- `GET/PATCH/DELETE /api/articles/<id>/`
- `GET/POST /api/sources/`
- `GET/POST /api/trends/`
- `GET /api/categories/`
- `GET /api/site-configuration/`
- `GET /api/content-requirements/`

Los borradores pueden crearse mediante API. `approved`, `scheduled` y `published` requieren un usuario con permisos elevados; la validación de fuentes y SEO permanece en Django.
