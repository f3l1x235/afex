# Migration vers GitHub - Instructions

Le projet ASFEX Formation Tchad est maintenant prêt pour être poussé vers GitHub.

## ✅ Ce qui a été préparé

- ✅ Documentation complète (README.md, CONTRIBUTING.md, DEPLOYMENT.md)
- ✅ Configuration de déploiement (Dockerfile, docker-compose.yml, Procfile)
- ✅ .gitignore correctement configuré
- ✅ Git initialisé avec commits
- ✅ Production-ready settings

## 📋 Historique Git actuel

Le projet contient 3 commits :
1. `premier commit` - Initialisation du projet
2. `Add Dockerfile, Procfile, and docker-compose.yml...` - Fichiers de déploiement
3. `docs: ajouter documentation complète...` - Documentation

## 🚀 Étapes pour pousser vers GitHub

### 1. Créer un repository sur GitHub

1. Aller à https://github.com/new
2. Remplir :
   - **Repository name** : `asfex_2` (ou `asfex-formation-tchad`)
   - **Description** : Formation professionnelle et expertise au Tchad
   - **Visibility** : Private (si c'est propriétaire) ou Public
3. Cliquer "Create repository"

### 2. Ajouter la remote GitHub

Remplacer `votre-username` par votre nom d'utilisateur GitHub :

```bash
cd c:\Users\PowerTIC\Desktop\asfex_2
git remote add origin https://github.com/votre-username/asfex_2.git
git branch -M main
git push -u origin main
```

### 3. Configurer l'authentification

**Avec Token (recommandé)**
```bash
git config --global user.email "votre-email@example.com"
git config --global user.name "Votre Nom"
```

Si vous utilisez 2FA sur GitHub, créer un Personal Access Token :
1. GitHub → Settings → Developer settings → Personal access tokens
2. Cliquer "Generate new token"
3. Cocher `repo` et `workflow`
4. Générer et copier le token
5. Utiliser le token à la place du mot de passe

### 4. Vérifier que tout est poussé

```bash
git remote -v
git log --oneline
git status
```

## 📁 Structure du repository sur GitHub

```
asfex_2/
├── README.md           ← Accueil du projet
├── CONTRIBUTING.md     ← Guide de contribution
├── DEPLOYMENT.md       ← Guide de déploiement
├── requirements.txt    ← Dépendances
├── manage.py
├── Dockerfile
├── docker-compose.yml
├── Procfile
├── .env.example        ← NE PAS pousser .env réel
├── .gitignore          ← Configure quoi ignorer
├── asfex/              ← Configuration Django
├── siteapp/            ← Application principale
├── templates/          ← HTML templates
└── static/             ← CSS, JS, images
```

## 🔒 Points de sécurité

✅ **Correctement configurés** :
- `.env` n'est pas tracké (dans .gitignore)
- `db.sqlite3` n'est pas tracké
- `__pycache__/` n'est pas tracké
- Clés secrètes en variables d'environnement
- Production settings activés avec `DJANGO_ENV=production`

⚠️ **À faire avant le vrai déploiement** :
1. Générer une vraie clé secrète : `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
2. Créer un `.env` réel avec config production
3. Définir les secrets GitHub (Settings → Secrets and variables)

## 🔄 Workflow recommandé après GitHub

### Pour les mises à jour :

```bash
# Faire des modifications
git add .
git commit -m "type: description"
git push origin main
```

### Pour les nouvelles fonctionnalités :

```bash
# Créer une branche
git checkout -b feature/ma-feature

# Faire les modifications
git add .
git commit -m "feat: description"

# Pousser la branche
git push origin feature/ma-feature

# Sur GitHub : créer un Pull Request
```

### Branches recommandées :

- `main` - Version stable
- `develop` - Version de développement
- `feature/*` - Nouvelles fonctionnalités
- `bugfix/*` - Corrections de bugs

## 📊 GitHub Pages (optionnel)

Pour avoir un site de documentation :

1. Settings → Pages
2. Sélectionner source : "main branch /docs folder"
3. Créer un dossier `/docs` avec index.html

## 🔔 Notifications GitHub

Recommandé :
- Watch les Issues et Discussions
- Configurer les notifications pour les PRs
- Configurer les Actions (CI/CD)

## 📝 Next Steps

1. **Pousser vers GitHub** : Suivre les étapes 1-4 ci-dessus
2. **Configurer les protections** :
   - Require pull request reviews
   - Require status checks to pass
3. **Ajouter des collaborateurs** : Settings → Collaborators
4. **Configurer les secrets** pour CI/CD (si besoin)

## ❓ Questions courantes

**Q: Comment cloner le projet ?**
```bash
git clone https://github.com/votre-username/asfex_2.git
cd asfex_2
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

**Q: Comment mettre à jour le .env sur le serveur de production ?**
```bash
# NE JAMAIS commiter .env !
# Le copier manuellement ou avec un outil sécurisé (AWS Secrets Manager, Vault, etc.)
scp .env utilisateur@serveur:/var/www/asfex_2/
```

**Q: Que faire si j'ai accidentellement commité un secret ?**
```bash
# Signaler immédiatement et régénérer les secrets
git log --all --full-history "secret"
# Ou utiliser git-filter-branch ou BFG Repo-Cleaner
```

---

Bon courage pour le déploiement! 🚀

Pour toute question : contact@asfex-formation-tchad.com
