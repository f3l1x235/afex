# ASFEX Formation Tchad

Plateforme web de formation professionnelle et expertise au Tchad, construite avec Django.

## 📋 Caractéristiques

- **Formations** : Gestion complète des programmes de formation par catégorie
- **Catégories** : Organisation des formations par domaine métier
- **Actualités** : Blog pour publier des contenus et annonces
- **Gestion des contacts** : Formulaire de contact avec stockage des messages
- **Interface d'administration** : Tableau de bord complet pour gérer le contenu
- **Authentification** : Système de rôles et permissions (Superadmin, Gestionnaire, Support)
- **Responsive** : Design moderne et adapté mobile
- **SEO** : Optimisation pour les moteurs de recherche

## 🚀 Installation locale

### Prérequis
- Python 3.10+
- pip
- MySQL (ou SQLite pour le développement)

### 1. Cloner le repository
```bash
git clone https://github.com/votre-username/asfex_2.git
cd asfex_2
```

### 2. Créer un environnement virtuel
```bash
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Configurer les variables d'environnement
```bash
cp .env.example .env
# Éditer .env avec vos paramètres locaux
```

Pour le développement local, gardez :
- `DJANGO_ENV=development`
- `DEBUG=True`
- `DB_ENGINE=django.db.backends.sqlite3` (par défaut)

### 5. Appliquer les migrations
```bash
python manage.py migrate
```

### 6. Créer un compte admin
```bash
python manage.py createsuperuser
```

### 7. Lancer le serveur de développement
```bash
python manage.py runserver
```

Accédez à : http://localhost:8000

## 📚 Structure du projet

```
asfex_2/
├── asfex/              # Paramètres Django
│   ├── settings.py     # Configuration (base de données, applications, sécurité)
│   ├── urls.py         # Routage URL principal
│   ├── wsgi.py         # Point d'entrée WSGI
│   └── asgi.py         # Point d'entrée ASGI
├── siteapp/            # Application Django
│   ├── models.py       # Modèles (Category, Course, Article, ContactMessage)
│   ├── views.py        # Vues et logique métier
│   ├── forms.py        # Formulaires Django
│   ├── urls.py         # Routage de l'application
│   └── migrations/     # Migrations de base de données
├── templates/          # Templates HTML
│   ├── admin/          # Interface de gestion
│   ├── base.html       # Template de base
│   ├── home.html       # Accueil
│   ├── courses.html    # Formations
│   └── ...
├── static/             # Fichiers statiques (CSS, JS, images)
├── .env.example        # Exemple de configuration
├── .gitignore          # Fichiers à ignorer par git
├── manage.py           # CLI Django
└── requirements.txt    # Dépendances Python
```

## 🔧 Configuration

### Variables d'environnement importantes

**Développement local :**
```
DJANGO_ENV=development
DEBUG=True
SECRET_KEY=dev-key
ALLOWED_HOSTS=localhost,127.0.0.1
```

**Production :**
```
DJANGO_ENV=production
DEBUG=False
SECRET_KEY=<clé aléatoire sécurisée>
ALLOWED_HOSTS=exemple.com,www.exemple.com
CSRF_TRUSTED_ORIGINS=https://exemple.com,https://www.exemple.com
DB_NAME=asfex
DB_USER=user
DB_PASSWORD=password
DB_HOST=localhost
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.example.com
EMAIL_HOST_USER=contact@example.com
EMAIL_HOST_PASSWORD=password
```

## 📱 Utilisateurs et rôles

### Rôles disponibles
- **Superadmin** : Accès complet + gestion des comptes et rôles
- **Gestionnaire** : Gestion du contenu (formations, actualités)
- **Support** : Accès en lecture aux messages

### Connexion admin
Accédez à : http://localhost:8000/gestion/login/

## ✅ Tests

Exécuter les tests :
```bash
python manage.py test
```

Tests disponibles :
- Vérification des métadonnées SEO
- Formulaires de contact
- Authentification et autorisations
- Gestion du contenu (CRUD)
- Gestion des rôles

## 🌐 Déploiement

### Préparation pour la production

1. Générer une clé secrète forte :
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

2. Créer un fichier `.env` avec la config production

3. Collecter les fichiers statiques :
```bash
python manage.py collectstatic --noinput
```

4. Appliquer les migrations :
```bash
python manage.py migrate
```

### Avec Gunicorn + Nginx

```bash
pip install gunicorn
gunicorn asfex.wsgi:application --bind 0.0.0.0:8000
```

### Avec Docker

Créer un `Dockerfile` et `docker-compose.yml` pour faciliter le déploiement.

### Variables d'environnement production

Définir toutes les variables du `.env.example` avec les vraies valeurs de production.

## 🔐 Sécurité

- Les mots de passe ne sont jamais commités (`.env` dans `.gitignore`)
- HTTPS obligatoire en production
- Cookies sécurisés et CSRF protégé
- HSTS et X-Frame-Options activés en production
- Base de données MySQL avec charset utf8mb4

## 📞 Fonctionnalités principales

### 📚 Gestion des formations
- Créer, modifier, supprimer des formations
- Organiser par catégorie
- Définir durée et prix

### 🏷️ Catégories
- Créer les domaines métier
- Associer les formations aux catégories
- Vue agrégée des formations par catégorie

### 📰 Actualités
- Publier des articles et annonces
- Gestion des contenus éditoriaux
- Archives des articles

### 💬 Gestion des contacts
- Réception des demandes de formation
- Stockage des messages
- Historique des demandes

### 👥 Gestion des comptes
- Création et suppression de comptes administrateur
- Attribution de rôles et permissions
- Gestion des groupes

## 📝 Notes de développement

- Language : Python 3.13
- Framework : Django 6.1
- ORM : Django ORM
- Base de données : MySQL / SQLite
- Serveur d'application : Gunicorn
- Serveur web : Nginx (recommandé)

## 📄 Licence

Ce projet est propriétaire à ASFEX Formation Tchad.

## 👨‍💼 Support

Pour toute question ou problème, contacter : contact@asfex-formation-tchad.com

---

**Dernière mise à jour** : Septembre 2026
