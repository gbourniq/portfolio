#!/usr/bin/env bash

# Note: This script must run it from root directory with `. ./scripts/reset_all.sh`

source .local.env
echo ".local.env has been sourced."

echo "Recreate Postgres database"
dropdb ${POSTGRES_DB}
createdb ${POSTGRES_DB}

# echo "Collecting static files"
# python manage.py collectstatic --no-input -v 0

echo "Run migrations"
# python app/manage.py makemigrations main
python app/manage.py makemigrations
python app/manage.py migrate

# python app/manage.py createsuperuser
echo "Create default Django superuser admin/admin."
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'gbournique@gmail.com', 'admin')" | python app/manage.py shell || true

