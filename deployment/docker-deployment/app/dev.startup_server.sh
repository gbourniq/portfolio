#!/bin/sh

cd /home/portfoliouser/portfolio/app

echo "Setting DJANGO_SETTINGS_MODULE to portfolio.settings.docker_settings"
export DJANGO_SETTINGS_MODULE=portfolio.settings.docker_settings

# echo "Collecting static files"
# python manage.py collectstatic --no-input -v 0

echo "Running migrations"
python manage.py makemigrations main
python manage.py migrate

echo "[DEV BUILD] Creating default Django superuser admin/admin."
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'gbournique@gmail.com', 'admin')" | python manage.py shell || true

echo "Starting webserver"
python manage.py runserver 0.0.0.0:8080

