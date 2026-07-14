# MCP en cPanel

El MCP se despliega como una segunda aplicación Python independiente de Django.

## Opción recomendada

Si el proveedor permite una aplicación ASGI, ejecutar `main:app` con Uvicorn y publicar `/mcp` detrás de HTTPS.

## Compatibilidad Passenger/WSGI

Si cPanel solo ofrece Passenger WSGI, usar `passenger_wsgi.py` y `a2wsgi`. El adaptador crea el contexto MCP por solicitud, compatible con el modo stateless utilizado por este proyecto.

Variables mínimas:

```env
DJANGO_INTERNAL_URL=https://blandskron.cl
MCP_INTERNAL_API_TOKEN=el-mismo-token-configurado-en-django
MCP_ALLOWED_HOSTS=mcp.blandskron.cl
MCP_ALLOWED_ORIGINS=https://blandskron.cl
```

El MCP debe poder resolver por HTTPS la URL de Django y el endpoint interno debe aceptar el Bearer token. No se deben configurar credenciales MySQL en la aplicación MCP.

Después de iniciar la aplicación, verificar `/health` y luego `/mcp` con un cliente MCP real. Si el proveedor bloquea el ciclo ASGI o las solicitudes POST necesarias para Streamable HTTP, el MCP debe alojarse en un servicio ASGI compatible separado; Django/WordPress no deben asumir ese protocolo.
