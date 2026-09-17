# ASFEX Formation Tchad

Plateforme Django de formation professionnelle, expertise et accompagnement au Tchad.

## Présentation

ASFEX Formation Tchad est une plateforme web destinée à présenter les offres de formation, les services d’expertise, les ressources pédagogiques et les demandes de contact. Le projet inclut également un espace d’administration complet pour gérer les formations, les actualités, les ressources, les messages et les demandes d’inscription.

## Fonctionnalités principales

- Gestion des formations et catégories
- Liste des formations publiques et vues détaillées
- Page “À propos”, “Expertise”, “Contact”, “Ressources”
- Gestion des actualités / articles
- Gestion des ressources avec type et fichier joint
- Tableau de bord d’administration avec indicateurs de performance
- Formulaires publics pour contact, devis et inscription
- SEO global et métadonnées par page
- Interface admin personnalisée avec thème ASFEX
- Favicon personnalisé

## Stack technique

- Python 3.13
- Django 6.1
- SQLite par défaut pour le développement
- MySQL pour la production
- Bootstrap 5
- HTML / CSS / JavaScript

## Structure du projet

```text
asfex_2/
├── asfex/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── siteapp/
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── tests.py
│   └── migrations/
├── templates/
│   ├── admin/
│   ├── includes/
│   ├── base.html
│   ├── home.html
│   ├── about.html
│   ├── courses.html
│   ├── course_detail.html
│   ├── training_calendar.html
│   ├── training_request.html
│   ├── contact.html
│   ├── articles.html
│   ├── resources.html
│   └── dashboard.html
├── static/
│   └── images/
│       └── asfex.ico
├── media/
├── .env
├── db.sqlite3
├── manage.py
├── requirements.txt
├── README.md
└── DEPLOYMENT.md
```

## Prérequis

- Python 3.10+
- pip
- Git
- Optionnel : MySQL pour la production

## Installation locale

### 1. Cloner le projet

```bash
git clone <url-du-repository>
cd asfex_2
```

### 2. Créer un environnement virtuel

```bash
python -m venv venv
```

Sur Windows :

```bash
venv\Scripts\activate
```

Sur Linux / macOS :

```bash
source venv/bin/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Configurer les variables d’environnement

Un fichier `.env` est déjà présent dans le projet. Pour le développement local, la configuration par défaut utilise SQLite.

Exemple de configuration locale :

```env
DJANGO_ENV=development
DEBUG=True
SECRET_KEY=dev-secret-key-change-me
ALLOWED_HOSTS=localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=asfex
DB_USER=
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=3306
```

Pour la production, utiliser MySQL avec les variables suivantes :

```env
DJANGO_ENV=production
DEBUG=False
DB_ENGINE=mysql
DB_NAME=asfex
DB_USER=asfex_user
DB_PASSWORD=votre_mot_de_passe
DB_HOST=localhost
DB_PORT=3306
```

### 5. Appliquer les migrations

```bash
python manage.py migrate
```

### 6. Créer un superadmin

```bash
python manage.py createsuperuser
```

### 7. Lancer le site

```bash
python manage.py runserver
```

Le projet est ensuite accessible sur :

```text
http://localhost:8000
```

## Accès administrateur

```text
http://localhost:8000/gestion/login/
```

## Commandes utiles

### Vérification Django

```bash
python manage.py check
```

### Collecte des fichiers statiques

```bash
python manage.py collectstatic --noinput
```

### Lancer les tests

```bash
python manage.py test
```

## Déploiement

Voir le fichier [DEPLOYMENT.md](DEPLOYMENT.md) pour la procédure complète de mise en production.

## Sécurité

- Clé secrète stockée dans le fichier `.env`
- Cookies sécurisés en production
- CSRF activé
- HTTPS recommandé en production
- Variables sensibles non commitées

## Contribution

Le projet est en cours d’évolution. Les changements doivent rester cohérents entre les modèles, vues, formulaires et templates.

## Licence

Projet propriétaire ASFEX Formation Tchad.

---

Dernière mise à jour : Septembre 2026
