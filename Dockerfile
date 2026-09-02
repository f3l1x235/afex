FROM python:3.13-slim

WORKDIR /app

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    mysql-client \
    && rm -rf /var/lib/apt/lists/*

# Copier les requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code de l'application
COPY . .

# Créer le répertoire pour les fichiers statiques
RUN mkdir -p /app/staticfiles

# Commande par défaut
CMD ["gunicorn", "asfex.wsgi:application", "--bind", "0.0.0.0:8000"]
