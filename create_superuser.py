#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.accounts.models import User

email = 'kenjicladia@gmail.com'
password = 'kenjicladia'
first_name = 'kenji'
last_name = 'cladia'

if not User.objects.filter(email=email).exists():
    User.objects.create_superuser(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name
    )
    print('Superuser created successfully')
else:
    print('Superuser already exists')