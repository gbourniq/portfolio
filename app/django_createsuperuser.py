from django.contrib.auth import get_user_model

from static_settings import (
    DJANGO_SUPERUSER_EMAIL,
    DJANGO_SUPERUSER_PASSWORD,
    DJANGO_SUPERUSER_USER,
)

User = get_user_model()

User.objects.create_superuser(
    DJANGO_SUPERUSER_USER, DJANGO_SUPERUSER_EMAIL, DJANGO_SUPERUSER_PASSWORD
)
