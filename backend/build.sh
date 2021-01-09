#!/bin/bash
rm -rf */migrations
python manage.py makemigrations users
python manage.py makemigrations networks
python manage.py migrate
