param(
    [string]$Action = "up"
)

switch ($Action) {
    "up"      { docker-compose up --build }
    "down"    { docker-compose down }
    "logs"    { docker-compose logs -f }
    "prune"   { docker system prune -f }
    "ps"      { docker-compose ps }
    "restart" { docker-compose restart }
    default   { Write-Host "Ação não reconhecida. Use: up, down, logs, prune, ps, restart" }
}
