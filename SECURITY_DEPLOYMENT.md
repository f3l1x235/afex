# 🔒 Guide de Sécurité pour le Déploiement ASFEX

## ✅ Checklist de Sécurité Pré-Déploiement

### 1. **Gestion des Secrets** ✓
- [ ] `SECRET_KEY` généré et unique (minimum 50 caractères)
- [ ] Fichier `.env` créé mais **JAMAIS commité** sur Git
- [ ] `.env` listé dans `.gitignore`
- [ ] Aucun credential en dur dans le code

**Comment générer les secrets:**
```bash
python generate_secrets.py
```

### 2. **Variables d'Environnement**
- [ ] `DJANGO_ENV=production`
- [ ] `DEBUG=False`
- [ ] `ALLOWED_HOSTS` configuré avec votre domaine réel
- [ ] `CSRF_TRUSTED_ORIGINS` configuré avec votre domaine réel

### 3. **Base de Données**
- [ ] Utiliser MySQL 8.0+ en production (pas SQLite)
- [ ] Mot de passe base de données: **minimum 16 caractères**
- [ ] Utilisateur BD avec permissions limitées (pas root)
- [ ] Backup automatique configuré

### 4. **Email SMTP**
- [ ] Pour Gmail: Utiliser **App Passwords** (pas votre mot de passe principal)
- [ ] Utiliser SMTP avec TLS/SSL
- [ ] Tester l'envoi d'email avant déploiement

### 5. **Certificat SSL**
- [ ] Certificat HTTPS valide (Let's Encrypt gratuit)
- [ ] HSTS activé (automatique en production)
- [ ] Redirection HTTP→HTTPS configurée

### 6. **Configuration Nginx**
```nginx
# Exemple de configuration sécurisée
server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    # Redirection HTTP vers HTTPS
    error_page 497 https://$host$request_uri;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /static/ {
        alias /var/www/asfex_2/staticfiles/;
    }
}

# Redirection HTTPS
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}
```

### 7. **Permissions Fichiers**
```bash
# Propriétaire: www-data
sudo chown -R www-data:www-data /var/www/asfex_2

# Permissions: 755 pour dossiers, 644 pour fichiers
sudo find /var/www/asfex_2 -type d -exec chmod 755 {} \;
sudo find /var/www/asfex_2 -type f -exec chmod 644 {} \;

# Permissions spéciales: .env doit être lisible uniquement par www-data
sudo chmod 600 /var/www/asfex_2/.env
```

### 8. **Gunicorn Configuration**
Fichier `/etc/systemd/system/gunicorn-asfex.service`:
```ini
[Unit]
Description=Gunicorn ASFEX
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/asfex_2
Environment="PATH=/var/www/asfex_2/venv/bin"
ExecStart=/var/www/asfex_2/venv/bin/gunicorn \
    --workers 4 \
    --worker-class sync \
    --bind 127.0.0.1:8000 \
    asfex.wsgi:application

[Install]
WantedBy=multi-user.target
```

### 9. **Collectstatic et Migrations**
```bash
# En production sur le serveur
python manage.py collectstatic --noinput
python manage.py migrate
```

### 10. **Tests de Sécurité**
```bash
# Vérifier la configuration
python manage.py check --deploy

# Tester l'envoi d'email
python manage.py shell
>>> from django.core.mail import send_mail
>>> send_mail('Test', 'Message de test', 'from@example.com', ['to@example.com'])
```

---

## 🚨 Vulnérabilités Corrigées

✅ **Credentials supprimés du code:**
- ❌ AVANT: `'PASSWORD': 'S1n9t3ub3@700#'` en dur dans settings.py
- ✅ APRÈS: Lecture depuis les variables d'environnement

✅ **SECRET_KEY sécurisée:**
- ❌ AVANT: Clé visible par défaut
- ✅ APRÈS: Clé requise en production, exception levée sinon

✅ **Email en mode console en développement:**
- ❌ AVANT: Configuration SMTP avec credentials en dur
- ✅ APRÈS: Mode console en dev, SMTP en production avec variables d'env

---

## 📋 Checklist Final Avant Déploiement

- [ ] Tous les tests passent: `python manage.py test`
- [ ] Pas d'erreurs de sécurité: `python manage.py check --deploy`
- [ ] Fichier `.env` créé et configuré correctement
- [ ] `.env` non commité (vérifier avec `git status`)
- [ ] Base de données MySQL créée et testée
- [ ] Certificat SSL installé
- [ ] Nginx configuré
- [ ] Gunicorn configuré comme service systemd
- [ ] Permissions fichiers correctes
- [ ] Email SMTP testé
- [ ] Sauvegardes automatiques configurées
- [ ] Monitoring et logs configurés

---

## 📚 Ressources

- [Django Security Documentation](https://docs.djangoproject.com/en/6.1/topics/security/)
- [Django Check Deploy](https://docs.djangoproject.com/en/6.1/ref/django-admin/#check)
- [OWASP Checklist](https://cheatsheetseries.owasp.org/cheatsheets/Deployment_Checklist.html)
- [Let's Encrypt](https://letsencrypt.org/)
- [Nginx Security Best Practices](https://nginx.org/en/docs/)
