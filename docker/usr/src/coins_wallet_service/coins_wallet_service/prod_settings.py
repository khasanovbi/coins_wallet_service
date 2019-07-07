from coins_wallet_service.base_settings import *  # noqa: F401, F403

ALLOWED_HOSTS = ["*"]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "dn!!bgtbzbodsqz1@sgxyv%259yrea@o@0rkq4dvh8if48!@$s"

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "prod_cws_db",
        "USER": "prod_cws_user",
        "PASSWORD": "prod_cws_password",
        "HOST": "postgres",
        "PORT": "5432",
    }
}


LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "root": {"level": "INFO", "handlers": ["console"]},
    "formatters": {
        "verbose": {
            "format": (
                "%(name)s %(levelname)s %(asctime)s %(module)s "
                "%(process)d %(thread)d %(message)s"
            )
        },
        "timed": {"format": "%(name)s %(levelname)s %(asctime)s %(message)s"},
    },
    "handlers": {
        "null": {"level": "DEBUG", "class": "logging.NullHandler"},
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "timed",
        },
    },
    "loggers": {
        "django": {"handlers": ["console"], "level": "INFO", "propagate": False},
        "django.db.backends": {
            "handlers": ["null"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}
