#!/usr/bin/env python
"""Quick test to verify Django settings are loaded correctly."""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'asfex.settings')
django.setup()

from django.conf import settings

print("✓ Django settings loaded successfully")
print(f"  ENVIRONMENT: {settings.ENVIRONMENT}")
print(f"  DEBUG: {settings.DEBUG}")
print(f"  SECRET_KEY length: {len(settings.SECRET_KEY)} characters")
print(f"  Database engine: {settings.DATABASES['default']['ENGINE']}")
print(f"  Database name: {settings.DATABASES['default']['NAME']}")
print(f"  Email backend: {settings.MAILERS['default']['BACKEND']}")
print("\n✓ All settings validated!")
