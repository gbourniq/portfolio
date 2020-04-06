#!/bin/sh

cd /home/portfolio/app/

echo "Creating default Django superuser for development build"
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('${DJANGO_SUPERUSER_USER}', '${DJANGO_SUPERUSER_EMAIL}', '${DJANGO_SUPERUSER_PASSWORD}')" | python manage.py shell 2>/dev/null || true

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
