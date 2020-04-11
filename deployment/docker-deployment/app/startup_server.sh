#!/bin/sh

cd /home/portfolio/app

if [[ $CREATE_DEFAULT_SUPERUSER == "True" ]]; then
    echo "[DEV BUILD] Creating default Django superuser admin/admin."
    echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'gbournique@gmail.com', 'admin')" | python manage.py shell || true
else
    echo "Django superuser must be create manually with python manage.py createsuperuser"
fi

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
