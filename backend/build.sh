#!/bin/bash
rm -rf */migrations
python manage.py makemigrations users
python manage.py makemigrations networks
python manage.py migrate
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', '', 'admin')" | python manage.py shell
