# Guide de déploiement ASFEX Formation Tchad

## 📋 Prérequis serveur

- Ubuntu 20.04+ ou CentOS 7+
- Python 3.10+
- MySQL 8.0+
- Nginx
- Supervisor ou systemd (pour gérer le service Gunicorn)

## 🚀 Déploiement sur serveur Linux

### 1. Préparation du serveur

```bash
# Mise à jour du système
sudo apt update && sudo apt upgrade -y

# Installer les dépendances
sudo apt install -y python3-pip python3-venv mysql-server nginx supervisor git curl
```

### 2. Cloner le repository

```bash
cd /var/www
sudo git clone https://github.com/votre-username/asfex_2.git
cd asfex_2
sudo chown -R www-data:www-data /var/www/asfex_2
```

### 3. Créer l'environnement virtuel

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configurer la base de données

```bash
# Créer la base de données MySQL
sudo mysql -u root -p << EOF
CREATE DATABASE asfex CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'asfex_user'@'localhost' IDENTIFIED BY 'votre_mot_de_passe';
GRANT ALL PRIVILEGES ON asfex.* TO 'asfex_user'@'localhost';
FLUSH PRIVILEGES;
EOF
```

### 5. Configurer les variables d'environnement

```bash
# Créer le fichier .env
nano .env
```

Ajouter :
```env
DJANGO_ENV=production
DEBUG=False
SECRET_KEY=votre_clé_secrète_aléatoire
ALLOWED_HOSTS=exemple.com,www.exemple.com
CSRF_TRUSTED_ORIGINS=https://exemple.com,https://www.exemple.com
DB_NAME=asfex
DB_USER=asfex_user
DB_PASSWORD=votre_mot_de_passe
DB_HOST=localhost
DB_PORT=3306
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.exemple.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=contact@exemple.com
EMAIL_HOST_PASSWORD=votre_mot_de_passe_email
DEFAULT_FROM_EMAIL=contact@exemple.com
```

### 6. Appliquer les migrations

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

### 7. Configurer Gunicorn

Créer le fichier de socket systemd :

```bash
sudo nano /etc/systemd/system/gunicorn-asfex.service
```

Contenu :
```ini
[Unit]
Description=Gunicorn ASFEX
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/var/www/asfex_2
Environment="PATH=/var/www/asfex_2/venv/bin"
ExecStart=/var/www/asfex_2/venv/bin/gunicorn \
    --workers 3 \
    --bind unix:/var/www/asfex_2/gunicorn.sock \
    --access-logfile - \
    --error-logfile - \
    asfex.wsgi:application
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
```

Activer le service :
```bash
sudo systemctl daemon-reload
sudo systemctl enable gunicorn-asfex.service
sudo systemctl start gunicorn-asfex.service
```

### 8. Configurer Nginx

Créer la configuration Nginx :

```bash
sudo nano /etc/nginx/sites-available/asfex
```

Contenu :
```nginx
upstream gunicorn_asfex {
    server unix:/var/www/asfex_2/gunicorn.sock fail_timeout=0;
}

server {
    listen 80;
    server_name exemple.com www.exemple.com;

    # Redirection HTTP vers HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name exemple.com www.exemple.com;

    # Certificats SSL (Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/exemple.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/exemple.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    client_max_body_size 10M;

    location /static/ {
        alias /var/www/asfex_2/staticfiles/;
        expires 30d;
    }

    location /media/ {
        alias /var/www/asfex_2/media/;
        expires 7d;
    }

    location / {
        proxy_pass http://gunicorn_asfex;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
}
```

Activer le site :
```bash
sudo ln -s /etc/nginx/sites-available/asfex /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 9. Configurer SSL avec Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot certonly --nginx -d exemple.com -d www.exemple.com
```

### 10. Backup automatique

Créer un script de backup :

```bash
sudo nano /usr/local/bin/backup-asfex.sh
```

Contenu :
```bash
#!/bin/bash
BACKUP_DIR="/var/backups/asfex"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup base de données
mysqldump -u asfex_user -p'mot_de_passe' asfex | gzip > $BACKUP_DIR/db_$DATE.sql.gz

# Backup fichiers
tar -czf $BACKUP_DIR/files_$DATE.tar.gz /var/www/asfex_2

# Garder seulement les 30 derniers jours
find $BACKUP_DIR -name "*.gz" -mtime +30 -delete
```

Rendre exécutable et ajouter à cron :
```bash
sudo chmod +x /usr/local/bin/backup-asfex.sh
sudo crontab -e

# Ajouter :
0 2 * * * /usr/local/bin/backup-asfex.sh
```

## 🐳 Déploiement avec Docker

### 1. Construire les images

```bash
docker-compose up -d --build
```

### 2. Appliquer les migrations

```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --noinput
```

### 3. Accéder à l'application

http://localhost:8000

## ☁️ Déploiement sur Heroku

### 1. Préparation

```bash
pip install heroku
heroku login
```

### 2. Créer l'application Heroku

```bash
heroku create votre-app-name
heroku addons:create cleardb:ignite  # Base de données MySQL
```

### 3. Configurer les variables d'environnement

```bash
heroku config:set DJANGO_ENV=production
heroku config:set DEBUG=False
heroku config:set SECRET_KEY='votre_clé_secrète'
heroku config:set ALLOWED_HOSTS='votre-app.herokuapp.com'
heroku config:set DATABASE_URL='mysql://...'
```

### 4. Déployer

```bash
git push heroku main
heroku run python manage.py migrate
```

## 🔍 Monitoring et logging

### Vérifier les logs

```bash
# Systemd
sudo journalctl -u gunicorn-asfex.service -n 50

# Nginx
sudo tail -f /var/log/nginx/error.log
```

### Mettre à jour l'application

```bash
cd /var/www/asfex_2
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart gunicorn-asfex.service
```

## 🚨 Troubleshooting

### Erreur de connexion à la base de données

```bash
sudo mysql -u asfex_user -p -e "SELECT 1"
```

### Permissions de fichiers

```bash
sudo chown -R www-data:www-data /var/www/asfex_2
sudo chmod -R 755 /var/www/asfex_2
```

### Vérifier la configuration Django

```bash
python manage.py check --deploy
```

---

**Support** : contact@asfex-formation-tchad.com
