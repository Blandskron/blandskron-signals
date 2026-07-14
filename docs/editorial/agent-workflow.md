# Flujo del agente editorial

El agente trabaja en dos niveles:

1. **Contexto:** configuración, guía, requisitos, artículos recientes y radar.
2. **Ejecución:** fuentes, borrador, revisión y tarea auditable.

Las tareas editoriales registran tipo, estado, instrucciones, artículo relacionado y fecha objetivo. Los newsletters se dejan en estado `draft`. El agente no tiene una herramienta de envío ni de publicación.

Rutina recomendada:

```text
get_site_configuration
→ get_content_requirements
→ list_categories / list_tags / list_recent_sources
→ list_recent_articles / search_articles
→ list_trends / get_trend
→ get_pending_editorial_tasks
→ create_source
→ create_article_draft
→ mark_article_for_review
→ create_editorial_task(state=pending, task_type=review)
→ update_editorial_task(state=completed)
```
