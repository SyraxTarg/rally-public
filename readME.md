# 🏁 Rally – Plateforme de Gestion d'Événements

Bienvenue dans **Rally**, une plateforme web pour organiser, découvrir et gérer des événements. Ce projet est découpé en deux parties : le **back-end** (`rally-back`) et le **front-end** (`rally-front`).

---

## 📁 Structure du projet

```
rally/
├── rally-back/      # API FastAPI (Python)
├── rally-front/     # Frontend Next.js (React)
└── README.md
```

---

## ⚙️ Installation rapide

### 1. Cloner le projet

```bash
git clone <your-repo-url>
cd rally
```

---

### 2. Configuration des variables d’environnement

#### 🔧 Back-end (`rally-back/`)

1. Copier le fichier `.env.sample` en `.env`
2. Remplir les variables nécessaires :

```bash
cp rally-back/.env.sample rally-back/.env
```

Exemple :

```env
# Sécurité
SECRET_KEY="votre_clé_secrète"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7

# Stripe
STRIPE_SECRET_KEY="sk_test_..."
STRIPE_WEBHOOK_SECRET="whsec_..."
STRIPE_SUCCESS_URL="http://localhost:3000/events"
STRIPE_CANCEL_URL="http://localhost:3000/events"
STRIPE_REFRESH_URL="http://localhost:3000/events"
STRIPE_RETURN_URL="http://localhost:3000/profiles/me"

# Emails
EMAIL_SENDER="noreply@example.com"
SMTP_SENDER="smtp.example.com"
SMTP_PORT=587
EMAIL_PASSWORD="motdepasse"

# Modération
BANNED_TERMS_PATH="errors/banned_words.txt"

# Hôtes
RALLY_HOST="https://127.0.0.1:8000/api/v1/"
RALLY_BACK_HOST="http://rally-back:8000/api/v1"
NEXT_PUBLIC_RALLY_BACK_HOST="http://127.0.0.1:8000/api/v1"
RALLY_FRONT_HOST="http://localhost:3000"

# Cloudinary
CLOUDINARY_CLOUD_NAME="cloud_name"
CLOUDINARY_API_KEY="api_key"
CLOUDINARY_API_SECRET="api_secret"
```

---

#### 🔧 Front-end (`rally-front/`)

1. Copier le `.env` :

```bash
cp rally-front/.env.example rally-front/.env
```

2. Modifier si besoin :

```env
RALLY_BACK_HOST="http://rally-back:8000/api/v1"
NEXT_PUBLIC_RALLY_BACK_HOST="http://localhost:8000/api/v1"
RALLY_FRONT_HOST="http://localhost:3000"

# Sécurité
SECRET_KEY="votre_clé_secrète"
ALGORITHM="HS256"
```
#### Les deux SECRET_KEY doivent être les mêmes

## ▶️ Lancer le projet

### 📦 Back-end

```bash
docker compose up --build
```

### 💻 Front-end

```bash
cd rally-front
npm install
npm run dev
```

---

## 🧪 Stack technique

* **Back-end** : Python, FastAPI, PostgreSQL, Stripe, Cloudinary
* **Front-end** : Next.js (React), Tailwind CSS
* **Authentification** : JWT
* **Emails** : SMTP
* **Déploiement** : Docker (pas terminé)

---
