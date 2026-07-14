# Scheduler local

Los trabajos recurrentes son comandos Django idempotentes y no publican contenido automáticamente.

```text
Diario:   run_daily_research
Semanal:  prepare_weekly_signals
Mensual:  review_living_articles
```

En Windows pueden ejecutarse mediante Task Scheduler usando `scripts/run-editorial-jobs.ps1`. En Linux/macOS, cron puede invocar `scripts/run-editorial-jobs.sh`.

Cada ejecución queda registrada en `audit.AutomationRun` con estado, tiempos, cantidad de elementos creados, metadatos y error si corresponde. Las alertas productivas se dejan para la Fase 8.
