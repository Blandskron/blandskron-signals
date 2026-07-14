import hmac
import os
from contextlib import asynccontextmanager
from typing import Any

import httpx
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.server import TransportSecuritySettings

DJANGO_URL = os.getenv("DJANGO_INTERNAL_URL", "http://localhost:8000").rstrip("/")
API_TOKEN = os.getenv("MCP_INTERNAL_API_TOKEN", "")
ALLOWED_HOSTS = [value.strip() for value in os.getenv("MCP_ALLOWED_HOSTS", "localhost:8100,127.0.0.1:8100,localhost,127.0.0.1").split(",") if value.strip()]
ALLOWED_ORIGINS = [value.strip() for value in os.getenv("MCP_ALLOWED_ORIGINS", "").split(",") if value.strip()]

mcp = FastMCP("Blandskron Signals", stateless_http=True, json_response=True, transport_security=TransportSecuritySettings(allowed_hosts=ALLOWED_HOSTS, allowed_origins=ALLOWED_ORIGINS))


async def django_request(method: str, path: str, **kwargs: Any) -> Any:
    headers = kwargs.pop("headers", {})
    headers["Authorization"] = f"Bearer {API_TOKEN}"
    headers["Accept"] = "application/json"
    async with httpx.AsyncClient(base_url=DJANGO_URL, timeout=20) as client:
        response = await client.request(method, path, headers=headers, **kwargs)
    if response.status_code >= 400:
        detail = response.text[:1000]
        raise RuntimeError(f"Django API {response.status_code}: {detail}")
    return response.json() if response.content else {}


@mcp.tool()
async def get_site_configuration() -> dict[str, Any]:
    """Obtiene la configuración del sitio y la guía editorial activa."""
    return await django_request("GET", "/api/site-configuration/")


@mcp.tool()
async def get_content_requirements() -> dict[str, Any]:
    """Obtiene requisitos de borradores y publicaciones."""
    return await django_request("GET", "/api/content-requirements/")


@mcp.tool()
async def list_recent_articles(limit: int = 10) -> dict[str, Any]:
    """Lista artículos recientes para detectar duplicados y contexto editorial."""
    limit = max(1, min(limit, 50))
    return await django_request("GET", f"/api/articles/?ordering=-updated_at&page_size={limit}")


@mcp.tool()
async def search_articles(query: str) -> dict[str, Any]:
    """Busca artículos por título, resumen o contenido."""
    if not query.strip():
        raise ValueError("La búsqueda no puede estar vacía.")
    return await django_request("GET", "/api/articles/", params={"search": query[:200]})


@mcp.tool()
async def get_article(article_id: int) -> dict[str, Any]:
    """Obtiene un artículo y sus fuentes."""
    return await django_request("GET", f"/api/articles/{article_id}/")


@mcp.tool()
async def list_trends() -> dict[str, Any]:
    """Lista las tendencias registradas en el radar."""
    return await django_request("GET", "/api/trends/")


@mcp.tool()
async def get_trend(trend_id: int) -> dict[str, Any]:
    """Obtiene una tendencia específica del radar."""
    return await django_request("GET", f"/api/trends/{trend_id}/")


@mcp.tool()
async def list_categories() -> dict[str, Any]:
    """Lista categorías disponibles para clasificar borradores."""
    return await django_request("GET", "/api/categories/?ordering=name")


@mcp.tool()
async def list_tags() -> dict[str, Any]:
    """Lista etiquetas existentes."""
    return await django_request("GET", "/api/tags/?ordering=name")


@mcp.tool()
async def list_recent_sources(limit: int = 20) -> dict[str, Any]:
    """Lista fuentes recientes para reutilizar referencias verificadas."""
    limit = max(1, min(limit, 50))
    return await django_request("GET", f"/api/sources/?ordering=-consulted_at&page_size={limit}")


@mcp.tool()
async def get_newsletter_schedule() -> dict[str, Any]:
    """Consulta ediciones de newsletter y sus estados; no envía campañas."""
    return await django_request("GET", "/api/newsletter-editions/?ordering=scheduled_at")


@mcp.tool()
async def get_pending_editorial_tasks() -> dict[str, Any]:
    """Consulta tareas editoriales pendientes o en curso."""
    return await django_request("GET", "/api/editorial-tasks/?ordering=due_at")


@mcp.tool()
async def create_editorial_task(task: dict[str, Any]) -> dict[str, Any]:
    """Registra una tarea editorial para seguimiento del agente o del equipo."""
    required = {"site", "task_type", "title"}
    missing = sorted(required - task.keys())
    if missing:
        raise ValueError(f"Faltan campos obligatorios: {', '.join(missing)}")
    return await django_request("POST", "/api/editorial-tasks/", json=task)


@mcp.tool()
async def update_editorial_task(task_id: int, changes: dict[str, Any]) -> dict[str, Any]:
    """Actualiza el estado o instrucciones de una tarea editorial."""
    allowed = {"state", "instructions", "assigned_to", "due_at", "article"}
    safe_changes = {key: value for key, value in changes.items() if key in allowed}
    if not safe_changes:
        raise ValueError("No hay cambios permitidos para la tarea.")
    return await django_request("PATCH", f"/api/editorial-tasks/{task_id}/", json=safe_changes)


@mcp.tool()
async def create_newsletter_draft(edition: dict[str, Any]) -> dict[str, Any]:
    """Prepara un borrador de newsletter; no lo envía."""
    required = {"campaign", "subject", "content_markdown"}
    missing = sorted(required - edition.keys())
    if missing:
        raise ValueError(f"Faltan campos obligatorios: {', '.join(missing)}")
    payload = dict(edition)
    payload["state"] = "draft"
    return await django_request("POST", "/api/newsletter-editions/", json=payload)


@mcp.tool()
async def create_source(title: str, url: str, publisher: str, source_type: str, published_at: str | None = None) -> dict[str, Any]:
    """Registra una fuente editorial verificable."""
    payload = {"title": title, "url": url, "publisher": publisher, "source_type": source_type}
    if published_at:
        payload["published_at"] = published_at
    return await django_request("POST", "/api/sources/", json=payload)


@mcp.tool()
async def create_article_draft(payload: dict[str, Any]) -> dict[str, Any]:
    """Crea un borrador editorial completo mediante el contrato de Django."""
    required = {"site", "category", "title", "slug", "excerpt", "content_markdown", "content_type", "meta_title", "meta_description"}
    missing = sorted(required - payload.keys())
    if missing:
        raise ValueError(f"Faltan campos obligatorios: {', '.join(missing)}")
    payload = dict(payload)
    payload["state"] = "draft"
    return await django_request("POST", "/api/articles/", json=payload)


@mcp.tool()
async def update_article(article_id: int, changes: dict[str, Any]) -> dict[str, Any]:
    """Actualiza campos permitidos de un artículo."""
    forbidden = {"id", "created_at", "updated_at", "published_at", "sources"}
    safe_changes = {key: value for key, value in changes.items() if key not in forbidden}
    if not safe_changes:
        raise ValueError("No hay campos actualizables.")
    return await django_request("PATCH", f"/api/articles/{article_id}/", json=safe_changes)


@mcp.tool()
async def mark_article_for_review(article_id: int) -> dict[str, Any]:
    """Envía un borrador a revisión editorial."""
    return await django_request("PATCH", f"/api/articles/{article_id}/", json={"state": "review"})


mcp_http_app = mcp.streamable_http_app()


@asynccontextmanager
async def lifespan(_app):
    async with mcp.session_manager.run():
        yield


app = FastAPI(title="Blandskron Signals MCP", version="0.2.0", lifespan=lifespan)


@app.middleware("http")
async def protect_mcp(request: Request, call_next):
    if request.url.path.startswith("/mcp"):
        authorization = request.headers.get("Authorization", "")
        supplied = authorization.removeprefix("Bearer ").strip() if authorization.startswith("Bearer ") else ""
        if not API_TOKEN or not supplied or not hmac.compare_digest(supplied, API_TOKEN):
            return JSONResponse({"detail": "Autenticación MCP requerida."}, status_code=401)
        allowed_origins = set(ALLOWED_ORIGINS)
        origin = request.headers.get("Origin")
        if allowed_origins and origin and origin not in allowed_origins:
            return JSONResponse({"detail": "Origen MCP no permitido."}, status_code=403)
    return await call_next(request)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "mcp", "django_url": DJANGO_URL, "transport": "streamable-http"}


# FastMCP ya define la ruta interna `/mcp`; montarlo en `/` evita duplicarla.
app.mount("/", mcp_http_app)
