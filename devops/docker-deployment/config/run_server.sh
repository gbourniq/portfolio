#!/bin/bash

python manage.py collectstatic --no-input -v 0
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:8080

# su -m app_user -c "python manage.py collectstatic --no-input -v 0"
# su -m app_user -c "python manage.py makemigrations"
# su -m app_user -c "python manage.py migrate"
# su -m app_user -c "python manage.py runserver 0.0.0.0:8080"