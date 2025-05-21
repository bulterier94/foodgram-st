#!/bin/sh

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
find fixtures -name "*.json" -exec python manage.py loaddata {} +
gunicorn --bind 0.0.0.0:8000 foodgram_backend.wsgi