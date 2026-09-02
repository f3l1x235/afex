#!/usr/bin/env python3
"""
Script to generate secure secrets for ASFEX deployment.
Generates SECRET_KEY and optional secure password.
"""

import secrets
import string
from pathlib import Path


def generate_secret_key(length=50):
    """Generate a secure Django SECRET_KEY."""
    chars = string.ascii_letters + string.digits + '!@#$%^&*(-_=+)'
    return ''.join(secrets.choice(chars) for _ in range(length))


def generate_password(length=16):
    """Generate a secure random password."""
    chars = string.ascii_letters + string.digits + '!@#$%^&*'
    return ''.join(secrets.choice(chars) for _ in range(length))


def create_env_file():
    """Create or update .env file with secure values."""
    env_path = Path(__file__).parent / '.env'
    
    # Check if .env already exists
    if env_path.exists():
        response = input('.env file already exists. Overwrite? (yes/no): ').strip().lower()
        if response not in ['yes', 'y']:
            print('Aborted.')
            return
    
    # Generate secrets
    secret_key = generate_secret_key()
    db_password = generate_password()
    email_password = generate_password()
    
    # Create .env content
    env_content = f"""# ========================================
# ASFEX Django Configuration
# Generated on {Path().cwd()}
# ========================================

# Environment
DJANGO_ENV=production
DEBUG=False

# Security
SECRET_KEY={secret_key}

# Allowed hosts (update with your domain)
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Database Configuration
DB_ENGINE=mysql
DB_NAME=asfex
DB_USER=asfex_user
DB_PASSWORD={db_password}
DB_HOST=localhost
DB_PORT=3306

# Email Configuration (update with your SMTP provider)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD={email_password}
DEFAULT_FROM_EMAIL=your-email@gmail.com
SERVER_EMAIL=your-email@gmail.com
"""
    
    # Write to file
    env_path.write_text(env_content)
    
    print(f'✓ .env file created successfully at {env_path}')
    print(f'\n⚠️  IMPORTANT: Update the following values:')
    print('   - ALLOWED_HOSTS: Set your actual domain')
    print('   - CSRF_TRUSTED_ORIGINS: Set your actual domain')
    print('   - EMAIL_HOST: Configure your SMTP server')
    print('   - EMAIL_HOST_USER: Set your email address')
    print('   - EMAIL_HOST_PASSWORD: Update with your email password or app token')
    print(f'\nGenerated secrets:')
    print(f'  - SECRET_KEY: (hidden for security)')
    print(f'  - DB_PASSWORD: (hidden for security)')
    print(f'\n✓ Keep this .env file secure and never commit it to version control!')


if __name__ == '__main__':
    create_env_file()
