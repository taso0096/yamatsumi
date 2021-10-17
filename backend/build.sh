#!/bin/bash
rm -rf */migrations
python manage.py makemigrations users
python manage.py makemigrations cyberspaces
python manage.py makemigrations exercises
python manage.py migrate
