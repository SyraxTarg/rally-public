if (-not (Test-Path "./docker-compose.yml")) {
    Write-Host "❌ Erreur : Ce script doit être lancé depuis la racine du projet (docker-compose.yml introuvable)"
    exit 1
}

Write-Host "✅ docker-compose.yml trouvé. Lancement du build..."

docker compose up --build

# stripe listen --forward-to localhost:8000/api/v1/payments/webhook/stripe
# docker exec -it postgres-db psql -U root -d rally
