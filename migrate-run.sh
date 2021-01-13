#!/bin/bash
export CELERY_BROKER_URL=redis://localhost:6379/0

# make db migrations
python manage.py makemigrations

# migrate db
python manage.py migrate



# run server
python manage.py runserver 0.0.0.0:8000
