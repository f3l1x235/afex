import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'asfex.settings')
import django
django.setup()
from siteapp.models import Resource
print('MODULE', Resource.__module__)
print('FILE', __import__('siteapp.models', fromlist=['*']).__file__)
print('FIELDS', [f.name for f in Resource._meta.get_fields()])
print('HAS_FILES', 'files' in [f.name for f in Resource._meta.get_fields()])
