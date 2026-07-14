# ADR-001: Django como fuente de verdad

- Estado: aceptada
- Decisión: Django concentra modelos, validaciones, permisos y auditoría.
- Motivo: reduce duplicación y mantiene un único flujo de negocio.
- Consecuencia: MCP solo accede a Django mediante HTTP.
