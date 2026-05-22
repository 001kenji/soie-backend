#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py makemigrations accounts orders payments products shipping 
python manage.py migrate
# python manage.py loaddata soie_data.json
# Create superuser if it doesn't exist
python manage.py shell -c "
from apps.accounts.models import User
if not User.objects.filter(email='kenjicladia@gmail.com').exists():
    User.objects.create_superuser(
        email='kenjicladia@gmail.com',
        password='kenjicladia',
        first_name='kenji',
        last_name='cladia'
    )
    print('Superuser created successfully')
else:
    print('Superuser already exists')