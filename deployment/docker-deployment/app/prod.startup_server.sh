#!/bin/sh

cd /home/portfoliouser/portfolio/app

echo "Collecting static files"
python manage.py collectstatic --no-input -v 0

echo "Running migrations"
python manage.py makemigrations main
python manage.py migrate

echo "Django superuser must be create manually with python manage.py createsuperuser"

echo "Starting webserver"
gunicorn portfolio.wsgi:application --bind 0.0.0.0:8080
