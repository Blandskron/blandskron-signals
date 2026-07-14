# DNS y HTTPS

Registros previstos:

```text
blandskron.cl       → servidor web
www.blandskron.cl   → servidor web
api.blandskron.cl   → API Django
mcp.blandskron.cl   → gateway MCP
```

Nginx termina TLS y reenvía `X-Forwarded-Proto` a Django. La configuración de producción activa redirección HTTPS, cookies seguras, HSTS, `X-Frame-Options` y `nosniff`.

La emisión de certificados y la configuración DNS se deben realizar manualmente en el proveedor elegido; esta fase no crea recursos externos.
