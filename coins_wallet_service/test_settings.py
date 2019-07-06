from .base_settings import *  # noqa: F401, F403

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "cws_db",
        "USER": "cws_user",
        "PASSWORD": "cws_password",
        "HOST": "localhost",
        "PORT": "5432",
    }
}
