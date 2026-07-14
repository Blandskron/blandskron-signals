#!/usr/bin/env bash
set -euo pipefail
frequency="${1:-daily}"
case "$frequency" in
  daily) docker compose run --rm backend python manage.py run_daily_research ;;
  weekly) docker compose run --rm backend python manage.py prepare_weekly_signals ;;
  monthly) docker compose run --rm backend python manage.py review_living_articles ;;
  *) echo "Uso: $0 daily|weekly|monthly" >&2; exit 2 ;;
esac
