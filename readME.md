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

## 🛠️ Création manuelle du Super Admin

Actuellement, la création automatique du **super administrateur** n’est pas encore disponible. Voici donc les étapes manuelles à suivre pour l’installer correctement :

---

### 1. 📝 Créer un Super Admin

**URL :**

```http
POST http://127.0.0.1:8000/api/v1/authent/register/super-admin
```

**Body (JSON) :**

```json
{
  "email": "votre_email@example.com",
  "password": "Password.123",
  "first_name": "Prénom",
  "last_name": "Nom",
  "phone_number": "02145674",
  "photo": "/pfps/default.jpg"
}
```

---

### 2. ✉️ Recevoir le Token de Validation par Email

**URL :**

```http
GET http://127.0.0.1:8000/api/v1/authent/send-token?user_email=votre_email@example.com
```

> Cette requête enverra un email avec un **token à 6 chiffres**.

---

### 3. ✅ Vérifier le Compte

**URL :**

```http
GET http://127.0.0.1:8000/api/v1/authent/verify-token?user_email=votre_email@example.com&token=XXXXXX
```

Remplacez `XXXXXX` par le **token reçu par mail**.

---

### 4. 🔐 Connexion (Login)

**URL :**

```http
POST http://localhost:8000/api/v1/authent/login
```

**Body :**

```json
{
  "email": "votre_email@example.com",
  "password": "Password.123"
}
```

> La réponse contiendra un **access token** (JWT). Conservez-le précieusement !

---

### 5. 🏷️ Créer un Type d'Événement

**URL :**

```http
POST http://localhost:8000/api/v1/super-admin/types
```

**Header :**

```http
Authorization: Bearer VOTRE_ACCESS_TOKEN
Content-Type: application/json
```

**Body :**

```json
{
  "type": "anniversaire"
}
```

---

### ✅ Vous êtes prêt

Vous avez maintenant un **super admin** et au moins **un type d’événement**, ce qui permet de créer un **compte utilisateur standard** via le **front-end**.
