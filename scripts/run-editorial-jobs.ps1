param([ValidateSet('daily','weekly','monthly')][string]$Frequency = 'daily')

switch ($Frequency) {
  'daily' { docker compose run --rm backend python manage.py run_daily_research }
  'weekly' { docker compose run --rm backend python manage.py prepare_weekly_signals }
  'monthly' { docker compose run --rm backend python manage.py review_living_articles }
}
