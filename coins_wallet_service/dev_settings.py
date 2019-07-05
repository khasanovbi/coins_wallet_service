from .base_settings import *  # noqa: F401, F403

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

if DEBUG:
    INSTALLED_APPS += ["debug_toolbar"]  # noqa: F405

    MIDDLEWARE.insert(  # noqa: F405
        0, "debug_toolbar.middleware.DebugToolbarMiddleware"
    )
    INTERNAL_IPS = ["127.0.0.1", "localhost"]

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

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
