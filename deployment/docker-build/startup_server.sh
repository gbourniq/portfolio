#!/bin/sh

cd /home/portfolio/app/

echo "Collecting static files"
python manage.py collectstatic --no-input -v 0

echo "Running migrations"
python manage.py makemigrations main
python manage.py migrate

echo "Starting webserver"
# dev
# python manage.py runserver 0.0.0.0:8080

# prod
gunicorn portfolio.wsgi:application --bind 0.0.0.0:8080
