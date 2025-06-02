#!/bin/bash

if [ ! -f "docker-compose.yml" ]; then
  echo "❌ Erreur : Ce script doit être lancé depuis la racine du projet (où se trouve docker-compose.yml)"
  exit 1
fi

echo "✅ docker-compose.yml trouvé. Lancement du build..."

docker compose up --build

# stripe listen --forward-to 127.0.0.1:8000/api/v1/payments/webhook/stripe