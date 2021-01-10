#!/bin/bash
export CELERY_BROKER_URL=redis://localhost:6379/0

# migrate db
python manage.py migrate

# make db migrations
python manage.py makemigrations

# run server
python manage.py runserver 0.0.0.0:8000
