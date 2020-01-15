from .base import *  # NOQA


# DJANGO DEFAULT SETTINGS
INSTALLED_APPS.append("django_extensions")  # NOQA
ALLOWED_HOSTS = ["*"]
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "project_testing",
        "USER": "postgres",
        "PASSWORD": "user",
        "HOST": "database",
        "PORT": "5432",
    }
}
