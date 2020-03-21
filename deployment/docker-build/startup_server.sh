#!/bin/sh

cd /home/portfolio/app/

python manage.py collectstatic --no-input -v 0
python manage.py makemigrations
python manage.py migrate
# python manage.py runserver 0.0.0.0:8080 #dev
gunicorn portfolio.wsgi:application --bind 0.0.0.0:8080 # prod

# suid -m app_user -c "python manage.py collectstatic --no-input -v 0"
# suid -m app_user -c "python manage.py makemigrations"
# suid -m app_user -c "python manage.py migrate"
# suid -m app_user -c "python manage.py runserver 0.0.0.0:8080"
# su -m app_user -c "gunicorn portfolio.wsgi:application --bind 0.0.0.0:8080" # prod