from a2wsgi import WSGIMiddleware
from main import app as asgi_app
from main import mcp


async def request_scoped_app(scope, receive, send):
    async with mcp.session_manager.run():
        await asgi_app(scope, receive, send)


application = WSGIMiddleware(request_scoped_app)
