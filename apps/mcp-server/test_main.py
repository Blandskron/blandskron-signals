import ast
from pathlib import Path


def test_mcp_module_is_valid_python():
    source = Path(__file__).with_name("main.py").read_text(encoding="utf-8")
    ast.parse(source)


def test_mcp_module_does_not_reference_database_clients():
    source = Path(__file__).with_name("main.py").read_text(encoding="utf-8")
    assert "psycopg" not in source
    assert "django.db" not in source


def test_expected_editorial_tools_are_declared():
    source = Path(__file__).with_name("main.py").read_text(encoding="utf-8")
    assert "get_pending_editorial_tasks" in source
    assert "create_editorial_task" in source
    assert "create_newsletter_draft" in source
    assert "list_categories" in source
    assert "list_recent_sources" in source
    assert "update_editorial_task" in source


def test_health_and_mcp_auth(monkeypatch):
    monkeypatch.setenv("MCP_INTERNAL_API_TOKEN", "test-token")
    monkeypatch.setenv("MCP_ALLOWED_ORIGINS", "http://localhost:8000")
    monkeypatch.setenv("MCP_ALLOWED_HOSTS", "localhost,127.0.0.1")
    from fastapi.testclient import TestClient
    from main import app

    with TestClient(app, base_url="http://localhost") as client:
        assert client.get("/health").status_code == 200
        assert client.get("/mcp", follow_redirects=False).status_code == 401
        response = client.get("/mcp", headers={"Authorization": "Bearer test-token", "Origin": "http://localhost:8000"})
        assert response.status_code in (200, 400, 405, 406)
